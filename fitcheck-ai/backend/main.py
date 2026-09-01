from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, random
from background import remove_and_pad
from PIL import Image
from classify import classify_image
from colour import get_dominant_colour
from database import SessionLocal, ClothingItem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

session = SessionLocal()

@app.get("/")
def health_check():
    return {"status": "FitCheck.ai backend is running"}

@app.post("/upload")
async def upload_item(file: UploadFile = File(...)):
    filepath = f"uploads/{file.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    category = classify_image(filepath)
    colour = get_dominant_colour(filepath)

    img = Image.open(filepath).convert("RGB").resize((512, 512))
    img.save(filepath)

    item = ClothingItem(filename=file.filename, category=category, colour=colour)
    session.add(item)
    session.commit()

    return {"filename": file.filename, "category": category, "colour": colour}

@app.get("/items")
def get_items():
    items = session.query(ClothingItem).all()
    return [{"filename": i.filename, "category": i.category, "colour": i.colour} for i in items]

@app.get("/recommend")
def recommend_outfit():
    items = session.query(ClothingItem).all()
    tops = [i for i in items if i.category in ["t-shirt", "shirt", "sweater"]]
    bottoms = [i for i in items if i.category in ["jeans", "trousers", "shorts"]]
    shoes = [i for i in items if i.category in ["shoes", "sandals"]]

    if not (tops and bottoms and shoes):
        return {"error": "Upload at least one top, bottom, and pair of shoes first"}

    return {
        "top": random.choice(tops).filename,
        "bottom": random.choice(bottoms).filename,
        "shoes": random.choice(shoes).filename,
    }