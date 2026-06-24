#!/usr/bin/env python3
"""Generate KubeJS item textures/models and FTB Quest icon PNGs."""
from __future__ import annotations

import colorsys
import json
import shutil
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "overrides" / "kubejs" / "assets"
TEX_ITEM = ASSETS / "kubejs" / "textures" / "item"
MODELS = ASSETS / "kubejs" / "models" / "item"
QUEST_TEX = ASSETS / "cooptech" / "textures" / "quests"


def rgba(h: str) -> tuple[int, int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4)) + (255,)  # type: ignore


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def model_json(texture: str) -> dict:
    return {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": f"kubejs:item/{texture}"},
    }


def write_model(name: str, texture: str | None = None) -> None:
    tex = texture or name
    path = MODELS / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(model_json(tex), indent=2), encoding="utf-8")


def fill(draw: ImageDraw.ImageDraw, xy, color) -> None:
    draw.rectangle(xy, fill=color)


def book_texture(base: tuple, accent: tuple, glow: bool = False) -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill(d, (3, 2, 12, 14), base)
    fill(d, (10, 2, 12, 14), accent)
    for y in range(4, 13, 2):
        d.line((5, y, 11, y), fill=(255, 255, 255, 40))
    if glow:
        d.rectangle((2, 1, 13, 14), outline=(120, 220, 255, 180))
    return img


def page_texture() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill(d, (4, 3, 12, 13), rgba("#e8dcc8"))
    fill(d, (4, 3, 5, 13), rgba("#b8a888"))
    for y in range(5, 12):
        d.line((6, y, 11, y), fill=(160, 140, 110, 200))
    d.point((7, 4), fill=rgba("#4488cc"))
    return img


def shard_texture(hue: float, stable: bool = False) -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r, g, b = colorsys.hsv_to_rgb(hue, 0.75, 0.95)
    core = (int(r * 255), int(g * 255), int(b * 255), 255)
    dark = (int(r * 180), int(g * 180), int(b * 180), 255)
    pts = [(8, 2), (12, 7), (10, 13), (6, 13), (4, 7)]
    d.polygon(pts, fill=core, outline=dark)
    d.line((8, 4, 8, 11), fill=(255, 255, 255, 120))
    if stable:
        d.rectangle((3, 10, 13, 12), fill=rgba("#d4af37"))
        d.point((8, 11), fill=rgba("#fff8dc"))
    return img


def core_texture() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((4, 4, 12, 12), fill=rgba("#8844cc"), outline=rgba("#cc88ff"))
    d.ellipse((6, 6, 10, 10), fill=rgba("#ffffff"))
    d.rectangle((7, 1, 9, 3), fill=rgba("#44ccff"))
    d.rectangle((7, 13, 9, 15), fill=rgba("#44ccff"))
    d.rectangle((1, 7, 3, 9), fill=rgba("#44ccff"))
    d.rectangle((13, 7, 15, 9), fill=rgba("#44ccff"))
    return img


def reliquary_texture(body: str, lid: str, gem: str) -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill(d, (4, 6, 12, 14), rgba(body))
    fill(d, (3, 4, 13, 7), rgba(lid))
    d.rectangle((7, 2, 9, 5), fill=rgba(gem))
    d.rectangle((5, 8, 11, 12), outline=rgba("#222222"))
    return img


def beacon_texture() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill(d, (7, 2, 9, 14), rgba("#666666"))
    fill(d, (5, 12, 11, 14), rgba("#444444"))
    d.polygon([(8, 1), (11, 5), (5, 5)], fill=rgba("#aa44ff"))
    d.point((8, 0), fill=rgba("#ffffff"))
    return img


def codex_texture() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill(d, (3, 3, 13, 14), rgba("#5a4a3a"))
    for x in range(5, 12, 2):
        d.line((x, 5, x, 12), fill=rgba("#3a2a1a"))
    d.line((5, 6, 11, 6), fill=rgba("#88ffaa"))
    d.line((5, 9, 10, 9), fill=rgba("#88ffaa"))
    return img


def quest_icon_gate() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(16, 2), (30, 16), (16, 30), (2, 16)], fill=rgba("#2ecc71"), outline=rgba("#ffffff"))
    d.line((10, 16, 22, 16), fill=rgba("#ffffff"), width=2)
    d.line((16, 10, 16, 22), fill=rgba("#ffffff"), width=2)
    return img


def quest_icon_lock() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((8, 14, 24, 28), fill=rgba("#7f8c8d"), outline=rgba("#ecf0f1"))
    d.arc((10, 4, 22, 18), 180, 0, fill=rgba("#bdc3c7"), width=3)
    d.rectangle((14, 18, 18, 22), fill=rgba("#2c3e50"))
    return img


def quest_icon_side_lock() -> Image.Image:
    img = quest_icon_lock()
    d = ImageDraw.Draw(img)
    d.line((6, 6, 26, 26), fill=rgba("#e74c3c"), width=3)
    d.line((26, 6, 6, 26), fill=rgba("#e74c3c"), width=3)
    return img


def quest_icon_pool() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((4, 4, 28, 28), fill=rgba("#3498db"), outline=rgba("#ecf0f1"))
    d.rectangle((11, 13, 21, 15), fill=rgba("#ffffff"))
    d.rectangle((15, 11, 17, 19), fill=rgba("#ffffff"))
    return img


def quest_icon_finale() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = []
    for i in range(8):
        import math

        ang = math.pi / 8 + i * math.pi / 4
        pts.append((16 + 14 * math.cos(ang), 16 + 14 * math.sin(ang)))
    d.polygon(pts, fill=rgba("#9b59b6"), outline=rgba("#f1c40f"))
    d.ellipse((12, 12, 20, 20), fill=rgba("#f39c12"))
    return img


def quest_icon_start() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(16, 4), (28, 28), (4, 28)], fill=rgba("#e67e22"), outline=rgba("#ffffff"))
    d.polygon([(16, 10), (22, 24), (10, 24)], fill=rgba("#f1c40f"))
    return img


def quest_icon_wave() -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((2, 14, 30, 26), fill=rgba("#1abc9c"), outline=rgba("#ffffff"))
    for x in range(4, 28, 6):
        d.arc((x, 8, x + 8, 20), 0, 180, fill=rgba("#16a085"))
    return img


def quest_icon_branch(color: str, symbol: str) -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(16, 2), (29, 9), (29, 23), (16, 30), (3, 23), (3, 9)], fill=rgba(color), outline=rgba("#ffffff"))
    if symbol == "+":
        d.line((10, 16, 22, 16), fill=rgba("#ffffff"), width=2)
        d.line((16, 10, 16, 22), fill=rgba("#ffffff"), width=2)
    elif symbol == "pick":
        d.line((10, 22, 22, 10), fill=rgba("#ffffff"), width=2)
        d.rectangle((18, 6, 24, 12), fill=rgba("#cccccc"))
    elif symbol == "eye":
        d.ellipse((10, 12, 22, 20), fill=rgba("#ffffff"))
        d.ellipse((14, 14, 18, 18), fill=rgba("#222222"))
    elif symbol == "hand":
        d.ellipse((12, 10, 20, 22), fill=rgba("#ffffff"))
    return img


def starfield_texture(size: int = 256) -> Image.Image:
    import random

    random.seed(42)
    img = Image.new("RGBA", (size, size), rgba("#06040F"))
    d = ImageDraw.Draw(img)
    for cx, cy, r, col in (
        (size // 3, size // 4, size // 3, "#1A0838"),
        (size * 2 // 3, size // 2, size // 4, "#120828"),
        (size // 2, size * 3 // 4, size // 5, "#0E1030"),
    ):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(col))
    blur = img.filter(ImageFilter.GaussianBlur(radius=size // 10))
    img = Image.alpha_composite(img, Image.blend(Image.new("RGBA", img.size, (0, 0, 0, 0)), blur, 0.55))
    d = ImageDraw.Draw(img)
    for _ in range(220):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        b = random.randint(180, 255)
        d.point((x, y), fill=(b, b, min(255, b + 50), random.randint(100, 230)))
    for _ in range(12):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=rgba("#AA66FFAA"))
    return img


def dependency_plain_texture() -> Image.Image:
    """Thin purple line tile — no chevron arrows (TechnoMagic-style)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((1, 30, 63, 34), radius=2, fill=rgba("#CCAA66FFCC"))
    return img


def dependency_glow_texture() -> Image.Image:
    """Soft glow around plain line (optional overlay)."""
    base = dependency_plain_texture()
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_fill = Image.new("RGBA", base.size, rgba("#AA44FF88"))
    glow_fill.putalpha(base.split()[3])
    glow = glow_fill.filter(ImageFilter.GaussianBlur(radius=2))
    return Image.alpha_composite(glow, base)


def dependency_glow_texture_legacy() -> Image.Image:
    """64x64 chevron tile like vanilla FTB dependency.png, with purple halo."""
    vanilla = ROOT / "scripts" / "_vanilla_dep.png"
    if vanilla.is_file():
        base = Image.open(vanilla).convert("RGBA")
    else:
        size = 64
        base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(base)
        for x in range(0, size, 16):
            pts = [(x + 4, size // 2), (x + 12, size // 4), (x + 12, size * 3 // 4)]
            d.polygon(pts, fill=rgba("#EEEEEEFF"))
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_fill = Image.new("RGBA", base.size, rgba("#AA44FFAA"))
    glow_fill.putalpha(base.split()[3])
    glow = glow_fill.filter(ImageFilter.GaussianBlur(radius=3))
    return Image.alpha_composite(glow, base)


def _glow_outline(src: Image.Image, glow_hex: str = "#CC55FF", blur: int = 4) -> Image.Image:
    w, h = src.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    alpha = src.split()[3]
    glow_fill = Image.new("RGBA", (w, h), rgba(glow_hex))
    glow_fill.putalpha(alpha)
    glow_fill = glow_fill.filter(ImageFilter.GaussianBlur(radius=blur))
    thick = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(thick)
    td.bitmap((0, 0), src.convert("1"), fill=rgba("#FFFFFF"))
    thick = thick.filter(ImageFilter.MaxFilter(3))
    thick.putalpha(thick.split()[3])
    halo = Image.new("RGBA", (w, h), rgba(glow_hex))
    halo.putalpha(thick.split()[3])
    halo = halo.filter(ImageFilter.GaussianBlur(radius=blur + 1))
    return Image.alpha_composite(halo, Image.alpha_composite(glow_fill, src))


def quest_shape_glow_outline(shape: str) -> Image.Image | None:
    ref = ROOT / "scripts" / "_ftb_shape_cache" / shape / "outline.png"
    if not ref.is_file():
        return None
    return _glow_outline(Image.open(ref).convert("RGBA"))


def quest_shape_dark_background(shape: str) -> Image.Image | None:
    ref = ROOT / "scripts" / "_ftb_shape_cache" / shape / "background.png"
    if not ref.is_file():
        return None
    src = Image.open(ref).convert("RGBA")
    dark = Image.new("RGBA", src.size, rgba("#141020EE"))
    dark.putalpha(src.split()[3])
    return Image.alpha_composite(dark, src)


def write_mcmeta_blur(path: Path) -> None:
    path.write_text('{\n  "texture": {\n    "blur": true\n  }\n}\n', encoding="utf-8")


def ensure_ftb_shape_cache() -> None:
    cache = ROOT / "scripts" / "_ftb_shape_cache"
    if (cache / "hexagon" / "outline.png").is_file():
        return
    jar = None
    mc = Path(r"C:\Users\GameOn_Dp\AppData\Roaming\.minecraft\versions")
    if mc.is_dir():
        for inst in mc.iterdir():
            mods = inst / "mods"
            if not mods.is_dir():
                continue
            hits = list(mods.glob("ftb-quests-forge-*.jar"))
            if hits:
                jar = hits[0]
                break
    if jar is None:
        print("  skip FTB shape glow: ftb-quests jar not found")
        return
    shapes = ("hexagon", "diamond", "gear")
    with zipfile.ZipFile(jar) as zf:
        for shape in shapes:
            for name in ("outline.png", "background.png", "shape.png"):
                arc = f"assets/ftbquests/textures/shapes/{shape}/{name}"
                try:
                    dest = cache / shape / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(zf.read(arc))
                except KeyError:
                    pass


def export_ftb_shapes(ftb_gui: Path, theme_gui: Path) -> None:
    cache = ROOT / "scripts" / "_ftb_shape_cache"
    shapes = ("hexagon", "diamond", "gear")
    for shape in shapes:
        outline = quest_shape_glow_outline(shape)
        bg = quest_shape_dark_background(shape)
        if outline is None:
            continue
        for base in (ftb_gui, theme_gui):
            tex_root = base.parent
            shape_dir = tex_root / "shapes" / shape
            shape_dir.mkdir(parents=True, exist_ok=True)
            save(outline, shape_dir / "outline.png")
            write_mcmeta_blur(shape_dir / "outline.png.mcmeta")
            if bg is not None:
                save(bg, shape_dir / "background.png")
                write_mcmeta_blur(shape_dir / "background.png.mcmeta")
            src_shape = cache / shape / "shape.png"
            if src_shape.is_file():
                save(Image.open(src_shape).convert("RGBA"), shape_dir / "shape.png")
                write_mcmeta_blur(shape_dir / "shape.png.mcmeta")


def main() -> None:
    save(book_texture(rgba("#5c4033"), rgba("#3d2817"), glow=True), TEX_ITEM / "expedition_journal.png")
    write_model("expedition_journal")

    save(page_texture(), TEX_ITEM / "journal_page.png")
    for i in range(13):
        name = f"journal_page_{str(i).zfill(2)}"
        write_model(name, "journal_page")

    for i in range(1, 13):
        n = str(i).zfill(2)
        hue = (i - 1) / 12.0
        save(shard_texture(hue, stable=False), TEX_ITEM / f"anchor_shard_{n}.png")
        save(shard_texture(hue, stable=True), TEX_ITEM / f"stabilized_shard_{n}.png")
        write_model(f"anchor_shard_{n}")
        write_model(f"stabilized_shard_{n}")

    save(core_texture(), TEX_ITEM / "reality_anchor_core.png")
    write_model("reality_anchor_core")

    reliquaries = {
        "reliquary_field": ("#4a7c59", "#2d5a3d", "#7dff9a"),
        "reliquary_resonant": ("#3a5a8c", "#2a4070", "#66ccff"),
        "reliquary_arcane": ("#5a3a8c", "#3a2060", "#cc88ff"),
        "reliquary_primordial": ("#8c6a3a", "#604820", "#ffcc66"),
        "reliquary_convergence": ("#8c3a7a", "#602050", "#ff88ee"),
    }
    for name, colors in reliquaries.items():
        save(reliquary_texture(*colors), TEX_ITEM / f"{name}.png")
        write_model(name)

    save(beacon_texture(), TEX_ITEM / "resonance_beacon.png")
    write_model("resonance_beacon")

    save(codex_texture(), TEX_ITEM / "decrypted_cave_codex.png")
    write_model("decrypted_cave_codex")

    quest_icons = {
        "gate": quest_icon_gate(),
        "lock": quest_icon_lock(),
        "side_lock": quest_icon_side_lock(),
        "pool": quest_icon_pool(),
        "finale": quest_icon_finale(),
        "chapter_start": quest_icon_start(),
        "wave": quest_icon_wave(),
        "branch_explore": quest_icon_branch("#44ccff", "eye"),
        "branch_mine": quest_icon_branch("#ff8844", "pick"),
        "branch_craft": quest_icon_branch("#88ff44", "+"),
        "branch_coop": quest_icon_branch("#cc66ff", "hand"),
    }
    for name, img in quest_icons.items():
        save(img, QUEST_TEX / f"{name}.png")

    quest_kubejs = ["gate", "side_lock", "lock", "pool", "finale", "chapter_start", "wave"]
    for name in quest_kubejs:
        src = QUEST_TEX / f"{name}.png"
        if not src.is_file():
            continue
        item_name = f"quest_{name}"
        shutil.copy2(src, TEX_ITEM / f"{item_name}.png")
        write_model(item_name)

    ftb_gui = ASSETS / "ftbquests" / "textures" / "gui"
    theme_gui = ROOT / "overrides" / "resourcepacks" / "CoopTechTheme" / "assets" / "ftbquests" / "textures" / "gui"
    stars = starfield_texture()
    dep = dependency_glow_texture_legacy()
    dep_glow = dependency_glow_texture()
    save(stars, ftb_gui / "stars_dark.png")
    save(stars, theme_gui / "stars_dark.png")
    for base in (ftb_gui, theme_gui):
        save(dep, base / "dependency.png")
    save(dep_glow, ftb_gui / "dependency_glow.png")
    save(dep_glow, theme_gui / "dependency_glow.png")
    write_mcmeta_blur(ftb_gui / "dependency_glow.png.mcmeta")
    write_mcmeta_blur(theme_gui / "dependency_glow.png.mcmeta")
    ensure_ftb_shape_cache()
    export_ftb_shapes(ftb_gui, theme_gui)

    print(f"Generated item textures in {TEX_ITEM}")
    print(f"Generated {len(list(MODELS.glob('*.json')))} item models")
    print(f"Generated quest icons in {QUEST_TEX}")


if __name__ == "__main__":
    main()
