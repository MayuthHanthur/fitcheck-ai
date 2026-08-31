from rembg import remove
from PIL import Image

SITE_BG = (13, 15, 20)  # matches #0d0f14 from your CSS
CANVAS_SIZE = (600, 400)  # landscape shape

def remove_and_pad(input_path, output_path):
    original = Image.open(input_path).convert("RGBA")

    cutout = remove(original)

    cutout.thumbnail((CANVAS_SIZE[0] - 60, CANVAS_SIZE[1] - 60))

    canvas = Image.new("RGB", CANVAS_SIZE, SITE_BG)

    x = (CANVAS_SIZE[0] - cutout.width) // 2
    y = (CANVAS_SIZE[1] - cutout.height) // 2
    canvas.paste(cutout, (x, y), mask=cutout)

    canvas.save(output_path, "JPEG", quality=90)