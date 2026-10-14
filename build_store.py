import json
import os
import re
import unicodedata
from pathlib import Path

from PIL import Image, ImageCms, ImageOps


ROOT = Path(__file__).parent
SOURCE = Path(os.environ.get("ANUMARA_SOURCE", ROOT.parent))
ASSETS = ROOT / "assets"
PRODUCT_IMAGES = ASSETS / "products"
PHONE = "527771899045"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".jfif", ".png"}

CATEGORIES = {
    "collares terminado": ("collares", "Collares"),
    "pulsera terminado": ("pulseras", "Pulseras"),
    "anillos terminados": ("anillos", "Anillos"),
}

WORD_FIXES = {
    "agathas": "Ágatas",
    "agata": "Ágata",
    "amazonita": "Amazonita",
    "amazonitas": "Amazonitas",
    "amatista": "Amatista",
    "amatistas": "Amatistas",
    "apatita": "Apatita",
    "apatitas": "Apatitas",
    "aquamarina": "Aguamarina",
    "aventurina": "Aventurina",
    "aventurinas": "Aventurinas",
    "ceramica": "Cerámica",
    "circonia": "Circonia",
    "circonias": "Circonias",
    "citrino": "Citrino",
    "citrinos": "Citrinos",
    "corazon": "Corazón",
    "cristal": "Cristal",
    "cuarzo": "Cuarzo",
    "cuentas": "Cuentas",
    "diamante": "Diamante",
    "dije": "Dije",
    "dijes": "Dijes",
    "ematita": "Hematita",
    "fluorita": "Fluorita",
    "fluoritas": "Fluoritas",
    "granate": "Granate",
    "howlitas": "Howlitas",
    "jade": "Jade",
    "jaspe": "Jaspe",
    "labradorita": "Labradorita",
    "labradoritas": "Labradoritas",
    "lapizlazuli": "Lapislázuli",
    "lapislazuli": "Lapislázuli",
    "malaquita": "Malaquita",
    "murano": "Murano",
    "nacar": "Nácar",
    "onix": "Ónix",
    "peridoto": "Peridoto",
    "peridotos": "Peridotos",
    "perla": "Perla",
    "perlas": "Perlas",
    "perlabarroca": "Perla barroca",
    "perlacultivada": "Perla cultivada",
    "perlascultivadas": "Perlas cultivadas",
    "piedraluna": "Piedra luna",
    "pirita": "Pirita",
    "plata925": "Plata Ley 925",
    "porcelana": "Porcelana",
    "rubi": "Rubí",
    "selenita": "Selenita",
    "selenitas": "Selenitas",
    "sodalita": "Sodalita",
    "tourmalinas": "Turmalinas",
    "turquesa": "Turquesa",
    "turquesas": "Turquesas",
    "vidrioafricano": "Vidrio africano",
}

COMPACT_FIXES = {
    "abulon": "Abulón",
    "acuatica": "Acuática",
    "agavedelamor": "Agave del Amor",
    "agavedemicorazon": "Agave de mi Corazón",
    "agavepasion": "Agave Pasión",
    "agavepasionycomplemento": "Agave Pasión y Complemento",
    "amordelcielo": "Amor del Cielo",
    "amoreteno": "Amor Eterno",
    "amormio": "Amor Mío",
    "arcoiris": "Arcoíris",
    "aventura": "Aventura",
    "azulenflor": "Azul en Flor",
    "bugambilia": "Bugambilia",
    "carnaval": "Carnaval",
    "catrina": "Catrina",
    "cempazuchitl": "Cempasúchil",
    "cereza": "Cereza",
    "constelacion": "Constelación",
    "corazonbolita": "Corazón Bolita",
    "corazondeflorceleste": "Corazón de Flor Celeste",
    "corazondelimon": "Corazón de Limón",
    "corazondemelocoton": "Corazón de Melocotón",
    "corazondenopal": "Corazón de Nopal",
    "corazondepiedra": "Corazón de Piedra",
    "corazonderesplandor": "Corazón de Resplandor",
    "corazonresplandor": "Corazón Resplandor",
    "corazonenflor": "Corazón en Flor",
    "corazonluminoso": "Corazón Luminoso",
    "corazonradiante": "Corazón Radiante",
    "cuadrante": "Cuadrante",
    "delarosa": "De la Rosa",
    "delavida": "De la Vida",
    "dragonfly": "Dragonfly",
    "estrella": "Estrella",
    "feria": "Feria",
    "fiesta": "Fiesta",
    "flordemicorazon": "Flor de mi Corazón",
    "gatoestelar": "Gato Estelar",
    "gota": "Gota",
    "gotita": "Gotita",
    "jaguar": "Jaguar",
    "jadelimon": "Jade Limón",
    "lagrimas": "Lágrimas",
    "lasflores": "Las Flores",
    "laslunas": "Las Lunas",
    "lavanda": "Lavanda",
    "mexico": "México",
    "mimadre": "Mi Madre",
    "nikita": "Nikita",
    "nocturno": "Nocturno",
    "nopaldecorazon": "Nopal de Corazón",
    "nopalesdelcorazon": "Nopales del Corazón",
    "oceano": "Océano",
    "ojitodemicorazon": "Ojito de mi Corazón",
    "orientica": "Oríntica",
    "perlanegra": "Perla Negra",
    "playa": "Playa",
    "playamarina": "Playa Marina",
    "playasayulita": "Playa Sayulita",
    "puroamor": "Puro Amor",
    "radiante": "Radiante",
    "reinadelcielo": "Reina del Cielo",
    "rubi": "Rubí",
    "selva": "Selva",
    "selenita": "Selenita",
    "serena": "Serena",
    "sol": "Sol",
    "turquesa": "Turquesa",
    "virgencita": "Virgencita",
    "volando": "Volando",
}

MATERIAL_PATTERNS = sorted(
    {
        **WORD_FIXES,
        "amatistalavanda": "Amatista lavanda",
        "cuarzocereza": "Cuarzo cereza",
        "cuarzocristal": "Cuarzo cristal",
        "cuarzorosa": "Cuarzo rosa",
        "cristaldemurano": "Cristal de Murano",
        "conchanacar": "Concha nácar",
        "hematitanegra": "Hematita negra",
        "hematitanegraestrella": "Hematita negra estrella",
        "jadeafricano": "Jade africano",
        "jadeimperialrojo": "Jade imperial rojo",
        "jaspeafricano": "Jaspe africano",
        "jaspecafe": "Jaspe café",
        "jaspedalmata": "Jaspe dálmata",
        "jasperojo": "Jaspe rojo",
        "lapizlazulifacetado": "Lapislázuli facetado",
        "peridotonatural": "Peridoto natural",
        "piedravolcanica": "Piedra volcánica",
        "porcelanapintadaamano": "Porcelana pintada a mano",
        "rubifacetado": "Rubí facetado",
    }.items(),
    key=lambda item: len(item[0]),
    reverse=True,
)


def ascii_slug(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def split_group(stem):
    value = stem.replace("(otratoma)", "")
    value = re.sub(r"\s*\(\d+\)$", "", value)
    match = re.search(r"[_\s]*(modelo|morelo)(?:_(\d+))?$", value)
    if match:
        return value[: match.start()].strip(" _"), int(match.group(2) or 1)
    match = re.search(r"[_\s](\d+)$", value)
    if match:
        return value[: match.start()].strip(" _"), int(match.group(1))
    return value.strip(" _"), 0


def grouped_images(folder):
    files = sorted(
        path for path in (SOURCE / folder).iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS
    )
    by_stem = {path.stem: path for path in files}
    groups = {}
    order = []
    for stem, path in by_stem.items():
        if stem.endswith(" bueno"):
            continue
        if f"{stem} bueno" in by_stem:
            path = by_stem[f"{stem} bueno"]
        key, index = split_group(stem)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append((index, path))
    return [(key, [path for _, path in sorted(groups[key])]) for key in order]


def pretty_variant(key):
    match = re.search(r"\(([^)]+)\)", key)
    if not match:
        return ""
    value = match.group(1).replace("ycomplemento", " y complemento")
    return value.replace("alargado", "Alargado").replace("doble", "Doble").replace(
        "complemento", "Complemento"
    ).replace("corto", "Corto").replace("largo", "Largo").strip().title()


def product_title(key, category):
    raw = key.lower()
    raw = re.sub(r"^(collar|pulsera|pulseras|anillo)_", "", raw)
    raw = re.sub(r"\([^)]*\)", "", raw).strip("_ ")
    parts = [part for part in raw.split("_") if part]
    line_index = next((i for i, p in enumerate(parts) if p.startswith("linea")), None)
    if "milvueltas" in raw:
        color = parts[-1]
        color = {
            "azulmarino": "Azul Marino",
            "verdeydorado": "Verde y Dorado",
            "turquesita": "Turquesita",
            "conchitas": "Conchitas",
            "perlita": "Perlita",
            "rosita": "Rosita",
        }.get(color, color.title())
        title = f"Mil Vueltas Iguazú · {color}"
    elif line_index is not None:
        line = parts[line_index].replace("linea", "").strip() or (
            parts[line_index + 1] if line_index + 1 < len(parts) else ""
        )
        design = parts[-1]
        if design == line and len(parts) > line_index + 1:
            design = parts[line_index + 1]
        line_name = {
            "africa": "África",
            "diademuertos": "Día de Muertos",
            "iguazu": "Iguazú",
            "nautilus": "Nautilus",
        }.get(line, COMPACT_FIXES.get(line, line.title()))
        design_name = COMPACT_FIXES.get(design, design.title())
        title = f"Línea {line_name} · {design_name}"
    else:
        design = parts[-1]
        title = COMPACT_FIXES.get(design, design.replace("complemento", "Complemento ").title())
    variant = pretty_variant(key)
    if variant and variant.lower() not in title.lower():
        title += f" · {variant}"
    return title


def product_materials(key):
    raw = key.lower().replace("_", " ")
    found = []
    occupied = set()
    for pattern, label in MATERIAL_PATTERNS:
        start = raw.find(pattern)
        if start < 0:
            continue
        span = set(range(start, start + len(pattern)))
        if span & occupied or label in found:
            continue
        occupied |= span
        found.append(label)
    if "Plata Ley 925" not in found and ("plata" in raw or "anillo" in raw):
        found.append("Plata Ley 925")
    return found[:5]


def prepare_image(source, destination, max_size=1400, quality=84):
    with Image.open(source) as original:
        profile = original.info.get("icc_profile")
        image = ImageOps.exif_transpose(original)
        if image.mode in {"RGBA", "LA", "P"}:
            image = image.convert("RGBA")
            background = Image.new("RGBA", image.size, "white")
            image = Image.alpha_composite(background, image)
        image = image.convert("RGB")
        if profile:
            try:
                source_profile = ImageCms.ImageCmsProfile(profile)
                target_profile = ImageCms.createProfile("sRGB")
                image = ImageCms.profileToProfile(
                    image, source_profile, target_profile, outputMode="RGB"
                )
            except Exception:
                pass
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, "WEBP", quality=quality, method=6)


def build():
    PRODUCT_IMAGES.mkdir(parents=True, exist_ok=True)
    products = []

    for folder, (category, label) in CATEGORIES.items():
        for key, source_images in grouped_images(folder):
            is_mil_vueltas = "milvueltas" in key.lower()
            display_category = "mil-vueltas" if is_mil_vueltas else category
            display_label = "Mil Vueltas" if is_mil_vueltas else label
            title = product_title(key, category)
            slug = ascii_slug(f"{display_category}-{title}-{len(products) + 1}")
            images = []
            for index, source in enumerate(source_images):
                destination = PRODUCT_IMAGES / f"{slug}-{index + 1}.webp"
                prepare_image(source, destination)
                images.append(destination.relative_to(ROOT).as_posix())
            materials = product_materials(key)
            search = " ".join([title, display_label, *materials]).lower()
            products.append(
                {
                    "id": slug,
                    "title": title,
                    "category": display_category,
                    "categoryLabel": display_label,
                    "materials": materials,
                    "images": images,
                    "search": search,
                    "whatsapp": (
                        f"https://wa.me/{PHONE}?text="
                        f"Hola%20Anumara%2C%20me%20interesa%20la%20pieza%20"
                        f"{title.replace(' ', '%20')}%20(código%20{slug})."
                    ),
                }
            )

    with (ROOT / "products.js").open("w", encoding="utf-8") as file:
        file.write("window.ANUMARA_PRODUCTS = ")
        json.dump(products, file, ensure_ascii=False, separators=(",", ":"))
        file.write(";\n")

    if not (ASSETS / "logo.png").exists():
        raise FileNotFoundError("Falta assets/logo.png")
    with Image.open(SOURCE / "aaa marca.jpeg") as brand:
        brand = ImageOps.exif_transpose(brand).convert("RGB")
        brand.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
        brand.save(ASSETS / "brand.webp", "WEBP", quality=88, method=6)

    print(f"{len(products)} productos y {sum(len(p['images']) for p in products)} imágenes")


if __name__ == "__main__":
    build()
