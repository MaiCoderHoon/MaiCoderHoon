#!/usr/bin/env python3
"""Build the decorative SVGs used by the profile README (assets/**).

    python .github/scripts/build_assets.py

README.md is hand-written Markdown/HTML and this script never touches it. It only
(re)writes the graphics the README points at:

    assets/brand/        the MaiCoderHoon mark
    assets/doodles/      pink section markers, sparks, arrows and squiggles
    assets/notes/        sticky notes for the "Currently Building" projects
    assets/icons/        sticker icons for projects, contact links and info
    assets/approach/     the Discover / Design / Build / Iterate tiles
    assets/toolkit/      one tile per tool (Devicon logos, MIT)
    assets/illustrations/ the workspace hero and the campus footer (illustrations.py)

The live GitHub stats cards are built separately by gen_stats.py on a schedule.

Every doodle is drawn in pink or sits on its own paper/colour tile, so nothing
disappears on GitHub's dark theme.
"""
import os

from illustrations import campus, workspace
from svgkit import ASSETS, C, LUCIDE, TWINKLE, brand_icon, doc, github_mark, icon, m_mark, path, poly, rect, write

INK, PINK, LIME, PAPER = C["ink"], C["pink"], C["lime"], C["paper"]
WRITTEN = []


def out(name, svg):
    write(name, svg)
    WRITTEN.append(name)


def sticker(x, y, w, h, fill, rx=14, sw=2.5, lift=3):
    """A paper-cutout tile: a soft drop shadow, then the tile with an ink outline."""
    return (rect(x + 1, y + lift, w, h, INK, rx=rx, extra=' opacity=".14"')
            + rect(x, y, w, h, fill, rx=rx, stroke=INK, sw=sw))


# ------------------------------------------------------------------ brand

def brand():
    clip, g = m_mark(32, 32, 34)
    out("brand/mark.svg", doc(64, 64, rect(0, 0, 64, 64, INK, rx=16) + g, "MaiCoderHoon", defs=clip))


# ------------------------------------------------------------------ doodles

def doodles():
    pk = dict(stroke=PINK, sw=4.5)
    out("doodles/sparks.svg", doc(44, 44, path("M10 30 L5 17", **pk) + path("M18 26 L19 9", **pk)
                                  + path("M25 30 L37 20", **pk), "", decorative=True))
    out("doodles/underline.svg", doc(260, 24,
        path("M6 15 C 46 6, 92 19, 134 11 S 214 6, 252 13", stroke=PINK, sw=7)
        + path("M30 19 C 80 13, 140 20, 214 15", stroke=PINK, sw=3, extra=' opacity=".6"'), "", decorative=True))
    out("doodles/marker.svg", doc(34, 26, poly([(2, 24), (11, 2), (18, 2), (9, 24)], PINK)
                                  + poly([(14, 24), (23, 2), (30, 2), (21, 24)], PINK), "", decorative=True))
    # curls from the heading down and to the left, toward the contact links below it
    out("doodles/arrow.svg", doc(124, 74, '<g transform="translate(124 0) scale(-1 1)">'
        + path("M8 16 C 30 4, 54 8, 58 28 C 61 42, 44 48, 41 37 C 38 25, 64 19, 82 31 C 94 39, 102 50, 108 61",
               stroke=PINK, sw=3.5)
        + path("M109 62 L94 59 M109 62 L107 47", stroke=PINK, sw=3.5) + '</g>', "", decorative=True))


# ------------------------------------------------------------------ sticky notes

def note(fill, fold, rotate, content, title):
    """A 220 x 220 sticky note with a binder clip, a folded corner and some content."""
    x, y, s = 26, 34, 168
    sheet = (f'M{x} {y}H{x + s}V{y + s - 26}L{x + s - 26} {y + s}H{x}Z')
    corner = f'M{x + s} {y + s - 26}L{x + s - 26} {y + s}L{x + s - 22} {y + s - 22}Z'
    body = (f'<g transform="rotate({rotate} 110 118)">'
            + path(sheet, fill=INK, extra=' transform="translate(4 7)" opacity=".16"')
            + path(sheet, fill=fill, stroke=INK, sw=2.5)
            + path(corner, fill=fold, stroke=INK, sw=2.5)
            + content
            # binder clip
            + rect(92, 18, 36, 26, INK, rx=6)
            + rect(98, 8, 24, 14, "none", rx=5, stroke=INK, sw=3)
            + rect(97, 24, 26, 4, C["white"], rx=2, extra=' opacity=".25"')
            + '</g>')
    return doc(220, 220, body, title)


def note_omni():
    # A phone with a campus app grid, a map pin and a little spark.
    tiles = [PINK, INK, C["lav"], LIME, C["pink_soft"], INK, C["lav"], PINK, C["cream"]]
    grid = "".join(rect(76 + (i % 3) * 18, 92 + (i // 3) * 18, 13, 13, col, rx=3.5, stroke=INK, sw=1.6)
                   for i, col in enumerate(tiles))
    phone = (rect(66, 64, 74, 120, C["white"], rx=14, stroke=INK, sw=2.8)
             + rect(92, 71, 22, 5, INK, rx=2.5)
             + rect(76, 82, 36, 5, INK, rx=2.5, extra=' opacity=".85"')
             + grid
             + rect(76, 152, 54, 16, PINK, rx=8, stroke=INK, sw=1.8)
             + path("M86 160 h22", stroke=INK, sw=2))
    pin = (path("M164 92 c0 12-14 24-14 24 s-14-12-14-24 a14 14 0 0 1 28 0Z", fill=PINK, stroke=INK, sw=2.5)
           + '<circle cx="150" cy="92" r="5" fill="#FFFFFF" stroke="#0E0E0E" stroke-width="2"/>')
    spark = path("M48 74 l-6 -10 M54 66 l1 -12 M60 74 l9 -7", stroke=INK, sw=3)
    return note(LIME, "#A6DB1E", -4, phone + pin + spark, "Sticky note: a phone showing a campus app grid")


def note_smart():
    # A weekly timetable with a highlighted best pick and an AI sparkle.
    x0, y0, cw, ch = 50, 82, 30, 22
    cells = []
    fills = [[C["white"], C["lav"], C["white"], LIME],
             [LIME, C["white"], C["lav"], C["white"]],
             [C["white"], LIME, C["white"], C["lav"]]]
    for r, row in enumerate(fills):
        for c, col in enumerate(row):
            cells.append(rect(x0 + c * cw, y0 + 20 + r * ch, cw, ch, col, stroke=INK, sw=1.6))
    table = (rect(x0, y0, cw * 4, 20, INK, rx=0)
             + "".join(rect(x0 + 8 + c * cw, y0 + 8, 14, 4, C["white"], rx=2) for c in range(4))
             + "".join(cells)
             + rect(x0, y0, cw * 4, 20 + ch * 3, "none", rx=3, stroke=INK, sw=2.6))
    best = (rect(x0 - 6, y0 + 20 + ch - 3, cw * 4 + 12, ch + 6, "none", rx=6, stroke=INK, sw=2.6,
                 extra=' stroke-dasharray="7 5"')
            + '<circle cx="178" cy="125" r="11" fill="#FFFFFF" stroke="#0E0E0E" stroke-width="2.4"/>'
            + path("M172 125 l4 4 8 -8", stroke=INK, sw=2.6))
    ai = f'<g transform="translate(150 50) scale(1.15)">{path(TWINKLE, fill=LIME, stroke=INK, sw=2)}</g>'
    bars = (rect(56, 170, 54, 8, INK, rx=4) + rect(56, 182, 34, 8, INK, rx=4, extra=' opacity=".55"'))
    return note(PINK, "#E35FBE", 3.5, table + best + ai + bars,
                "Sticky note: a timetable with the best section circled")


def notes():
    out("notes/omni-kiit.svg", note_omni())
    out("notes/smartschedule.svg", note_smart())


# ------------------------------------------------------------------ sticker icons

def icons():
    # Project stickers (64 x 64): each one hints at what the project does.
    def tile(content, title, fill=PAPER):
        return doc(64, 64, sticker(4, 3, 56, 56, fill, rx=15) + content, title)

    tree = (path("M32 18 L19 33 M32 18 L45 33 M19 33 L13 47 M19 33 L25 47 M45 33 L45 47", stroke=INK, sw=2.4)
            + '<circle cx="32" cy="16" r="6.5" fill="#FC80D6" stroke="#0E0E0E" stroke-width="2.4"/>'
            + "".join(f'<circle cx="{x}" cy="33" r="5" fill="#C9FF3D" stroke="#0E0E0E" stroke-width="2.2"/>'
                      for x in (19, 45))
            + "".join(rect(x - 4, 44, 8, 8, C["white"], rx=2, stroke=INK, sw=2) for x in (13, 25, 45)))
    out("icons/rootrunner.svg", tile(tree, "RootRunner: DNS resolution tree"))

    shield = ('<g transform="translate(14 12) scale(1.5)">'
              '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 '
              f'4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" fill="{PINK}" '
              f'stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
              f'<path d="m9 12 2 2 4-4" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" '
              'stroke-linejoin="round"/></g>')
    out("icons/scambust.svg", tile(shield, "ScamBust: shield with a check mark"))

    chart = ("".join(rect(x, 50 - h, 9, h, LIME, rx=2, stroke=INK, sw=2.2) for x, h in ((14, 12), (27.5, 20), (41, 28)))
             + path("M12 34 L24 26 L32 30 L49 14", stroke=PINK, sw=3.2)
             + path("M41 13 L50 13 L50 22", stroke=PINK, sw=3.2))
    out("icons/price-prediction.svg", tile(chart, "Price Prediction: bar chart with a rising trend"))

    clock = (path("M15 22 a8 8 0 0 1 11 -9 M49 22 a8 8 0 0 0 -11 -9", stroke=INK, sw=2.6)
             + path("M22 47 l-4 5 M42 47 l4 5", stroke=INK, sw=2.6)
             + '<circle cx="32" cy="34" r="15" fill="#FC80D6" stroke="#0E0E0E" stroke-width="2.4"/>'
             + '<circle cx="32" cy="34" r="10" fill="#FFFFFF" stroke="#0E0E0E" stroke-width="2"/>'
             + path("M32 28 V34 L36 37", stroke=INK, sw=2.4))
    out("icons/wakewise.svg", tile(clock, "WakeWise: alarm clock"))

    # Small round stickers (32 x 32) for inline use next to text.
    def badge(content, title, fill=PAPER):
        return doc(32, 32, f'<circle cx="16.5" cy="17.5" r="14" fill="{INK}" opacity=".14"/>'
                   f'<circle cx="16" cy="16" r="14" fill="{fill}" stroke="{INK}" stroke-width="2"/>' + content, title)

    out("icons/pin.svg", badge(f'<g transform="translate(8 7.5) scale(.68)"><path d="M20 10c0 4.993-5.539 10.193-7.399 '
                               f'11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0" fill="{PINK}" '
                               f'stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/><circle cx="12" cy="10" '
                               f'r="3" fill="{C["white"]}" stroke="{INK}" stroke-width="2.4"/></g>', "Location"))
    out("icons/campus.svg", badge(f'<g transform="translate(7.6 8) scale(.7)"><path d="M21.42 10.922a1 1 0 0 0-.019-1.838'
                                  f'L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z" '
                                  f'fill="{PINK}" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
                                  f'<path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5" fill="none" stroke="{INK}" '
                                  f'stroke-width="2.4"/><path d="M22 10v6" stroke="{INK}" stroke-width="2.4" '
                                  f'stroke-linecap="round"/></g>', "University"))
    out("icons/mail.svg", badge(icon("mail", 8.5, 8.5, 15, INK, 2.1), "Email", fill=C["pink_soft"]))
    out("icons/linkedin.svg", badge(icon("linkedin", 8.8, 8.3, 14.5, INK, 2.1), "LinkedIn", fill=LIME))
    out("icons/github.svg", badge(github_mark(8.6, 8.6, 14.8, INK), "GitHub", fill=C["lav"]))


# ------------------------------------------------------------------ approach + toolkit

def approach():
    steps = [("discover", "lightbulb", C["pink_soft"]), ("design", "pencil", C["lav"]),
             ("build", "code", C["lav_deep"]), ("iterate", "refresh", LIME)]
    for name, ic, fill in steps:
        out(f"approach/{name}.svg", doc(64, 64, sticker(4, 3, 56, 56, fill, rx=16) + icon(ic, 18, 16, 28, INK, 2.6),
                                        name.capitalize()))


#  Toolkit tiles, taken from the resume: languages first, then frameworks / ML / tools.
TOOLKIT = [("python", "Python"), ("sql", "SQL"), ("kotlin", "Kotlin"), ("java", "Java"), ("cplusplus", "C++"),
           ("dart", "Dart"), ("c", "C"), ("flutter", "Flutter"), ("jetpackcompose", "Jetpack Compose"),
           ("fastapi", "FastAPI"), ("pandas", "Pandas"), ("scikitlearn", "scikit-learn"), ("figma", "Figma"),
           ("git", "Git")]


def toolkit():
    for key, label in TOOLKIT:
        if key == "sql":
            logo = (f'<g transform="translate(16 15) scale(1.33)" fill="{C["lav"]}" stroke="{INK}" stroke-width="1.7" '
                    f'stroke-linecap="round" stroke-linejoin="round">{LUCIDE["database"]}</g>')
        else:
            logo = brand_icon(key, 14, 13, 36)
        out(f"toolkit/{key}.svg", doc(64, 64, sticker(3, 2, 58, 58, PAPER, rx=15, sw=2) + logo, label))


# ------------------------------------------------------------------ main

def clean():
    """Remove assets this script no longer produces (e.g. the old poster slices)."""
    keep = {os.path.normpath(os.path.join(ASSETS, *n.split("/"))) for n in WRITTEN}
    removed = 0
    for root, _, files in os.walk(ASSETS):
        for f in files:
            p = os.path.normpath(os.path.join(root, f))
            if f.endswith(".svg") and p not in keep:
                os.remove(p)
                removed += 1
    for root, dirs, files in sorted(os.walk(ASSETS), reverse=True):
        if root != ASSETS and not os.listdir(root):
            os.rmdir(root)
    return removed


def main():
    brand()
    doodles()
    notes()
    icons()
    approach()
    toolkit()
    out("illustrations/workspace.svg", workspace())
    out("illustrations/campus.svg", campus())
    removed = clean()
    print(f"wrote {len(WRITTEN)} files in assets/" + (f", removed {removed} stale" if removed else ""))


if __name__ == "__main__":
    main()
