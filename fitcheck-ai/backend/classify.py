import open_clip, torch
from PIL import Image

_model = None
_preprocess = None
_tokenizer = None

CATEGORIES = ["t-shirt", "shirt", "jeans", "trousers", "shorts", "dress", "jacket", "sweater", "shoes", "sandals"]

def _load_model():
    global _model, _preprocess, _tokenizer
    if _model is None:
        _model, _, _preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
        _tokenizer = open_clip.get_tokenizer('ViT-B-32')
        _model.eval()

def classify_image(filepath):
    _load_model()
    image = _preprocess(Image.open(filepath).convert("RGB")).unsqueeze(0)
    text = _tokenizer([f"a photo of a {c}" for c in CATEGORIES])
    with torch.no_grad():
        image_features = _model.encode_image(image)
        text_features = _model.encode_text(text)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
    return CATEGORIES[similarity.argmax().item()]