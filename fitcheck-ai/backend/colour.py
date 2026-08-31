from colorthief import ColorThief

def get_dominant_colour(filepath):
    ct = ColorThief(filepath)
    r, g, b = ct.get_color(quality=1)
    return f"rgb({r},{g},{b})"