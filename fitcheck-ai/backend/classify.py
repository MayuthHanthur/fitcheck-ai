import open_clip, torch
from PIL import Image

model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
tokenizer = open_clip.get_tokenizer('ViT-B-32')
model.eval()

CATEGORIES = ["t-shirt", "shirt", "jeans", "trousers", "shorts", "dress", "jacket", "sweater", "shoes", "sandals"]

def classify_image(filepath):
    image = preprocess(Image.open(filepath).convert("RGB")).unsqueeze(0)
    text = tokenizer([f"a photo of a {c}" for c in CATEGORIES])
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
    return CATEGORIES[similarity.argmax().item()]