"""Genera el kit de publicidad de Anumara para Facebook e Instagram."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).parent.parent
FONTS = Path(__file__).parent / "fonts"
OUTPUT = Path(r"C:\Users\Rodrigo\OneDrive\Escritorio\Jefa\Publicidad Anumara")
SITE = "rodvalleac.github.io/anumara-joyeria"
PHONE_TEXT = "(+52) 777 189 90 45"

FOREST = (26, 38, 28)
FOREST_DEEP = (17, 26, 19)
GOLD = (210, 189, 138)
GOLD_DARK = (170, 135, 84)
CREAM = (239, 230, 214)


def font(name, size, weight=None, italic=False):
    if name == "display":
        path = FONTS / "Cinzel.ttf"
    else:
        path = FONTS / ("CormorantGaramond-Italic.ttf" if italic else "CormorantGaramond.ttf")
    loaded = ImageFont.truetype(str(path), size)
    if weight:
        try:
            loaded.set_variation_by_axes([weight])
        except Exception:
            pass
    return loaded


def tracked_width(text, typeface, tracking):
    if not text:
        return 0
    return sum(typeface.getlength(char) for char in text) + tracking * (len(text) - 1)


def draw_tracked(draw, center_x, y, text, typeface, fill, tracking=0):
    x = center_x - tracked_width(text, typeface, tracking) / 2
    for char in text:
        draw.text((x, y), char, font=typeface, fill=fill)
        x += typeface.getlength(char) + tracking


def wrap(text, typeface, max_width, tracking=0):
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if tracked_width(candidate, typeface, tracking) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def cover(path, size, focus=0.32):
    image = Image.open(path).convert("RGB")
    target = size[0] / size[1]
    ratio = image.width / image.height
    if ratio > target:
        width = int(image.height * target)
        image = image.crop(((image.width - width) // 2, 0, (image.width + width) // 2, image.height))
    else:
        height = int(image.width / target)
        top = int((image.height - height) * focus)
        image = image.crop((0, top, image.width, top + height))
    return image.resize(size, Image.Resampling.LANCZOS)


def canvas(size):
    base = Image.new("RGB", size, FOREST)
    gradient = Image.new("L", (1, size[1]))
    for y in range(size[1]):
        gradient.putpixel((0, y), int(70 * y / size[1]))
    overlay = Image.new("RGB", size, FOREST_DEEP)
    image = Image.composite(overlay, base, gradient.resize(size))
    draw = ImageDraw.Draw(image)
    margin = int(size[0] * 0.035)
    draw.rectangle([margin, margin, size[0] - margin, size[1] - margin], outline=GOLD_DARK, width=2)
    inner = margin + 9
    draw.rectangle([inner, inner, size[0] - inner, size[1] - inner], outline=(60, 78, 62), width=1)
    return image, draw


def paste_logo(image, width, center_y, variant="full"):
    logo = Image.open(REPO / "assets" / "logo.png").convert("RGBA")
    if variant == "emblem":
        logo = logo.crop((0, 0, logo.width, int(logo.height * 0.66)))
        logo = logo.crop(logo.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
    height = int(width * logo.height / logo.width)
    logo = logo.resize((width, height), Image.Resampling.LANCZOS)
    image.paste(logo, ((image.width - width) // 2, center_y - height // 2), logo)
    return height


def contain(path, size, background=(255, 255, 255)):
    """Muestra la fotografía completa, sin recortar la pieza."""
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    card = Image.new("RGB", size, background)
    card.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return card


def framed_photo(image, path, box, mode="cover"):
    x, y, width, height = box
    photo = cover(path, (width, height)) if mode == "cover" else contain(path, (width, height))
    image.paste(photo, (x, y))
    ImageDraw.Draw(image).rectangle([x - 4, y - 4, x + width + 3, y + height + 3], outline=GOLD, width=2)


def footer(draw, image, y=None, site_size=30, phone_size=34):
    y = y or image.height - 120
    draw_tracked(draw, image.width / 2, y, SITE.upper(), font("display", site_size, 500), GOLD, 3)
    draw.text((image.width / 2, y + site_size + 12), f"Pedidos por WhatsApp · {PHONE_TEXT}",
              font=font("serif", phone_size), fill=(173, 185, 169), anchor="ma")


def ornament(draw, center_x, y, half):
    draw.line([center_x - half, y, center_x - 16, y], fill=GOLD_DARK, width=2)
    draw.line([center_x + 16, y, center_x + half, y], fill=GOLD_DARK, width=2)
    draw.polygon([(center_x, y - 8), (center_x + 7, y), (center_x, y + 8), (center_x - 7, y)], fill=GOLD)


def products():
    raw = (REPO / "products.js").read_text(encoding="utf-8")
    return json.loads(raw[len("window.ANUMARA_PRODUCTS = "):-2])


def pick(items, product_id):
    return next(item for item in items if item["id"] == product_id)


def launch_post(items):
    image, draw = canvas((1080, 1080))
    paste_logo(image, 470, 400)
    ornament(draw, 540, 620, 190)
    draw_tracked(draw, 540, 648, "YA PUEDES COMPRAR EN LÍNEA", font("display", 36, 600), CREAM, 5)
    subtitle = font("serif", 40, italic=True)
    draw.text((540, 718), "181 piezas únicas en Plata Ley 925", font=subtitle, fill=GOLD, anchor="ma")
    draw.text((540, 772), "Gemas y piedras naturales", font=subtitle, fill=(150, 165, 148), anchor="ma")
    footer(draw, image, 912)
    image.save(OUTPUT / "01-publicacion-lanzamiento.jpg", quality=92)


def category_post(items, filename, title, subtitle, product_ids):
    image, draw = canvas((1080, 1080))
    paste_logo(image, 170, 108, "emblem")
    draw_tracked(draw, 540, 168, title.upper(), font("display", 58, 500), CREAM, 7)
    draw.text((540, 246), subtitle, font=font("serif", 34, italic=True), fill=GOLD, anchor="ma")
    gap, size = 22, 300
    start_x = (1080 - (size * 2 + gap)) // 2
    for index, product_id in enumerate(product_ids[:4]):
        product = pick(items, product_id)
        column, row = index % 2, index // 2
        use_model = len(product["images"]) > 1
        framed_photo(image, REPO / product["images"][1 if use_model else 0],
                     (start_x + column * (size + gap), 322 + row * (size + gap), size, size),
                     "cover" if use_model else "contain")
    footer(draw, image, 962)
    image.save(OUTPUT / filename, quality=92)


def piece_post(items, filename, product_id, image_index=1):
    product = pick(items, product_id)
    source = product["images"][min(image_index, len(product["images"]) - 1)]
    image = cover(REPO / source, (1080, 1080), focus=0.5)
    shade = Image.new("L", (1, 1080))
    for y in range(1080):
        shade.putpixel((0, y), 0 if y < 600 else min(242, int((y - 600) * 0.72)))
    image = Image.composite(Image.new("RGB", (1080, 1080), FOREST_DEEP), image, shade.resize((1080, 1080)))
    draw = ImageDraw.Draw(image)
    draw.rectangle([34, 34, 1046, 1046], outline=GOLD, width=2)
    title_font = font("display", 56, 500)
    lines = wrap(product["title"], title_font, 860, 3)
    y = 818 - (len(lines) - 1) * 34
    for line in lines:
        draw_tracked(draw, 540, y, line, title_font, CREAM, 3)
        y += 70
    materials = " · ".join(product["materials"][:3]) or "Pieza artesanal Anumara"
    draw.text((540, y + 2), materials, font=font("serif", 31, italic=True), fill=GOLD, anchor="ma")
    footer(draw, image, 958, 27, 31)
    image.save(OUTPUT / filename, quality=92)


def story(items, filename, product_id, headline, subline, image_index=0):
    product = pick(items, product_id)
    image = cover(REPO / product["images"][image_index], (1080, 1920))
    shade = Image.new("L", (1, 1920))
    for y in range(1920):
        if y < 330:
            value = 185
        elif y < 560:
            value = int(185 * (1 - (y - 330) / 230))
        elif y < 1060:
            value = 0
        else:
            value = min(243, int((y - 1060) * 0.42))
        shade.putpixel((0, y), value)
    image = Image.composite(Image.new("RGB", (1080, 1920), FOREST_DEEP), image, shade.resize((1080, 1920)))
    draw = ImageDraw.Draw(image)
    paste_logo(image, 330, 300)
    headline_font = font("display", 66, 500)
    y = 1320
    for line in wrap(headline.upper(), headline_font, 880, 5):
        draw_tracked(draw, 540, y, line, headline_font, CREAM, 5)
        y += 86
    ornament(draw, 540, y + 36, 150)
    draw.text((540, y + 76), subline, font=font("serif", 42, italic=True), fill=GOLD, anchor="ma")
    draw_tracked(draw, 540, 1690, SITE.upper(), font("display", 34, 500), GOLD, 4)
    draw.text((540, 1745), f"Pedidos por WhatsApp · {PHONE_TEXT}",
              font=font("serif", 36), fill=(170, 182, 166), anchor="ma")
    image.save(OUTPUT / filename, quality=92)


def share_image(items):
    image, draw = canvas((1200, 630))
    product = pick(items, "collares-corazon-radiante-3")
    photo = cover(REPO / product["images"][1], (470, 560))
    image.paste(photo, (688, 35))
    draw.rectangle([684, 31, 1162, 598], outline=GOLD, width=2)
    logo = Image.open(REPO / "assets" / "logo.png").convert("RGBA")
    logo_width = 300
    logo_height = int(logo_width * logo.height / logo.width)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    image.paste(logo, (353 - logo_width // 2, 108), logo)
    draw_tracked(draw, 353, 400, "TIENDA EN LÍNEA", font("display", 30, 600), CREAM, 5)
    draw.text((353, 452), "Plata Ley 925 · Gemas naturales", font=font("serif", 30),
              fill=(160, 175, 158), anchor="ma")
    draw_tracked(draw, 353, 516, SITE.upper(), font("display", 22, 500), GOLD, 2)
    image.save(REPO / "assets" / "share.jpg", quality=90)


def captions():
    url = f"https://{SITE}/"
    hashtags = ("#Anumara #JoyeriaConAlma #PlataLey925 #JoyeriaArtesanal #PiedrasNaturales "
                "#Cuarzos #JoyeriaMexicana #HechoAMano #RegalosConSignificado")
    text = f"""TEXTOS LISTOS PARA PUBLICAR · ANUMARA
=======================================

Tienda en linea: {url}
WhatsApp: {PHONE_TEXT}

---------------------------------------
1. FACEBOOK · PUBLICACIÓN DE LANZAMIENTO
   Imagen: 01-publicacion-lanzamiento.jpg
---------------------------------------
✨ Ya puedes conocer toda la colección de Anumara en línea ✨

Joyería con alma: 181 piezas únicas creadas con Plata Ley 925, gemas y piedras naturales.
Collares, Mil Vueltas, pulseras y anillos; cada uno pensado como un talismán vivo que
acompaña tu historia.

Explora la colección completa aquí 👉 {url}
¿Te gustó una pieza? Escríbenos por WhatsApp al {PHONE_TEXT} y te atendemos personalmente.

{hashtags}

---------------------------------------
2. INSTAGRAM · PUBLICACIÓN DE LANZAMIENTO
   Imagen: 01-publicacion-lanzamiento.jpg
---------------------------------------
Cada joya es un eslabón. Cada piedra es un latido. ✨

Nuestra colección completa ya está en línea: 181 piezas en Plata Ley 925 con gemas y
piedras naturales, elegidas una a una por su energía.

🔗 Link en la biografía
💬 Pedidos por WhatsApp: {PHONE_TEXT}

{hashtags}

---------------------------------------
3. CARRUSEL (FACEBOOK E INSTAGRAM)
   Imágenes: 02, 03, 04 y 05 en ese orden
---------------------------------------
Desliza para recorrer nuestras cuatro colecciones 💫

· Collares: guirnaldas que guardan intenciones y recuerdos
· Mil Vueltas: la versatilidad de la Línea Iguazú
· Pulseras: una intención en cada eslabón
· Anillos: un latido que llevas contigo

Mira todas las piezas con sus fotos en {url}
Te ayudamos a elegir por WhatsApp: {PHONE_TEXT}

{hashtags}

---------------------------------------
4. PIEZA DESTACADA
   Imágenes: 06, 07 y 08
---------------------------------------
Hay piezas que eligen a quien las porta. ✨

Plata Ley 925 y piedras naturales seleccionadas por su vibración, trabajadas a mano para
convertirse en un amuleto que respira al mismo ritmo que tú.

Disponible ahora en {url}
💬 {PHONE_TEXT}

{hashtags}

---------------------------------------
5. HISTORIAS (INSTAGRAM Y FACEBOOK)
   Imágenes: historia-01, historia-02 e historia-03
---------------------------------------
· Historia 1: agrega el sticker de ENLACE con {url}
· Historia 2: agrega el sticker de ENCUESTA "¿Cuál te gusta más?"
· Historia 3: agrega el sticker de WHATSAPP con el número {PHONE_TEXT}

---------------------------------------
6. BIOGRAFÍA SUGERIDA
---------------------------------------
Anumara · Joyería con alma ✨
Plata Ley 925, gemas y piedras naturales
Talismanes vivos hechos a mano
📲 Pedidos: {PHONE_TEXT}
🔗 {url}
"""
    (OUTPUT / "textos-para-publicar.txt").write_text(text, encoding="utf-8")


def build():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    items = products()
    launch_post(items)
    category_post(items, "02-publicacion-collares.jpg", "Collares",
                  "Guirnaldas que guardan intenciones",
                  ["collares-corazon-radiante-3", "collares-corazon-en-flor-5",
                   "collares-de-la-vida-doble-16", "collares-playa-marina-13"])
    category_post(items, "03-publicacion-mil-vueltas.jpg", "Mil Vueltas", "Línea Iguazú",
                  [item["id"] for item in items if item["category"] == "mil-vueltas"][:4])
    category_post(items, "04-publicacion-pulseras.jpg", "Pulseras", "Una intención en cada eslabón",
                  [item["id"] for item in items if item["category"] == "pulseras"][:4])
    category_post(items, "05-publicacion-anillos.jpg", "Anillos", "Un latido que llevas contigo",
                  [item["id"] for item in items if item["category"] == "anillos"][:4])
    piece_post(items, "06-pieza-corazon-radiante.jpg", "collares-corazon-radiante-3")
    piece_post(items, "07-pieza-corazon-en-flor.jpg", "collares-corazon-en-flor-5")
    piece_post(items, "08-pieza-catrina.jpg", "collares-linea-dia-de-muertos-catrina-1")
    story(items, "historia-01-lanzamiento.jpg", "collares-corazon-radiante-3",
          "Tienda en línea", "181 piezas únicas te esperan", 1)
    story(items, "historia-02-coleccion.jpg", "collares-corazon-en-flor-5",
          "Joyería con alma", "Plata Ley 925 y piedras naturales", 1)
    story(items, "historia-03-whatsapp.jpg", "collares-volando-4",
          "Pide la tuya hoy", "Te atendemos por WhatsApp", 1)
    share_image(items)
    captions()
    print(f"Kit generado en {OUTPUT}")


if __name__ == "__main__":
    build()
