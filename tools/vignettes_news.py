"""Vignettes harmonisées des news : une image par thème (images/news/cat-<theme>.jpg).
Lancer : python3 tools/vignettes_news.py"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
F = "/root/.fonts/"
CAT = {  # thème : (image de fond, libellé, couleur)
 "donjons":   ("images/donjons-cover.jpg", "Donjons & raids", (150, 40, 40)),
 "metiers":   ("images/camping.jpg", "Métiers & économie", (40, 120, 70)),
 "jcj":       ("images/pvp-cover.jpg", "JcJ", (170, 60, 20)),
 "classes":   ("images/classes-cover.jpg", "Classes & builds", (110, 40, 150)),
 "races":     ("images/races-cover.jpg", "Races", (30, 110, 150)),
 "correctifs":("images/galerie/08.jpg", "Correctifs & patchs", (190, 120, 20)),
 "quetes":    ("images/feu-de-camp.jpg", "Quêtes & leveling", (60, 120, 40)),
 "objets":    ("images/monture-eolide.jpg", "Objets & montures", (30, 90, 170)),
 "general":   ("images/actus.jpg", "Actualités", (120, 30, 60)),
 "videos":    ("images/galerie/05.jpg", "Vidéos", (200, 30, 30)),
 "site":      ("images/news/carte.jpg", "Le site & outils", (50, 70, 90)),
}
W, H = 800, 450
def font(sz):
    f = ImageFont.truetype(F + "Cinzel[wght].ttf", sz)
    try: f.set_variation_by_axes([800])
    except Exception: pass
    return f
for k, (src, lab, col) in CAT.items():
    im = Image.open(src).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    im = ImageEnhance.Color(im).enhance(1.15)
    # dégradé bas + filet de couleur
    g = Image.new("L", (1, H)); [g.putpixel((0, j), int(200 * max(0, (j - H * 0.45) / (H * 0.55)) ** 1.4)) for j in range(H)]
    im = Image.composite(Image.new("RGB", (W, H), (10, 8, 12)), im, g.resize((W, H)))
    im.save(f"images/news/cat-{k}-grand.jpg", quality=84, optimize=True)  # sans étiquette, pour la grande news
    d = ImageDraw.Draw(im)
    fo = font(42); tw = d.textlength(lab, font=fo)
    x0 = (W - tw - 48) // 2  # centré : reste visible quand la vignette est recadrée
    d.rounded_rectangle((x0, H - 100, x0 + tw + 48, H - 36), 16, fill=col, outline=(255, 205, 80), width=3)
    d.text((W // 2, H - 68), lab, font=fo, fill=(255, 255, 255), anchor="mm")
    d.rectangle((0, H - 8, W, H), fill=col)
    if k == "videos":
        cx, cy = W // 2, H // 2 - 30
        d.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), fill=(200, 30, 30), outline=(255, 255, 255), width=4)
        d.polygon([(cx - 18, cy - 30), (cx - 18, cy + 30), (cx + 34, cy)], fill=(255, 255, 255))
    im.save(f"images/news/cat-{k}.jpg", quality=84, optimize=True)
print(len(CAT), "vignettes")
