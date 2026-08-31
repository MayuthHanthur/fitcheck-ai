from rembg import new_session, remove
from PIL import Image

SITE_BG = (13, 15, 20)
CANVAS_SIZE = (600, 400)

_session = None

def _get_session():
    global _session
    if _session is None:
        _session = new_session("u2netp")
    return _session

def remove_and_pad(input_path, output_path):
    original = Image.open(input_path).convert("RGBA")

    cutout = remove(original, session=_get_session())

    cutout.thumbnail((CANVAS_SIZE[0] - 60, CANVAS_SIZE[1] - 60))

    canvas = Image.new("RGB", CANVAS_SIZE, SITE_BG)

    x = (CANVAS_SIZE[0] - cutout.width) // 2
    y = (CANVAS_SIZE[1] - cutout.height) // 2
    canvas.paste(cutout, (x, y), mask=cutout)

    canvas.save(output_path, "JPEG", quality=90)