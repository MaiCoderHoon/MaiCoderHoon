#!/usr/bin/env python3
"""Build the profile poster (assets/*.svg) and README.md.

    python .github/scripts/build_assets.py

Change the copy or links below, then re-run. The poster is one W x H scene cut
into rows; rows with links are cut further into tiles so each card or button is
its own link. The "GitHub Stats" row is not built here: gen_stats.py renders it
every few minutes from live data (see .github/workflows/stats.yml).
"""
import math
import os

from svgkit import (ASSETS, C, H, HERE, W, Scene, brand_icon, cap, esc, fmt, github_mark, icon, line, logo, moon,
                    poly, poster_bg, raster, rect, section_title, strokes, text, tw, write)

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ART = os.path.join(HERE, "art")
USER = "MaiCoderHoon"
GH = f"https://github.com/{USER}"
LINKS = {
    "profile": GH,
    "repos": f"{GH}?tab=repositories",
    "omni": f"{GH}?tab=repositories",        # Omni KIIT has no public repo yet; swap in its URL when it does
    "smartschedule": f"{GH}/SmartSelector",
    "email": "mailto:piyush993bisoi@outlook.com",
    "linkedin": "https://www.linkedin.com/in/piyush-bisoi",
    "github": GH,
}
# Rebuilt every few minutes by .github/workflows/stats.yml and published to the `output` branch.
STATS_URL = f"https://raw.githubusercontent.com/{USER}/{USER}/output/stats.svg"
STATS_ROW = (1900, 2205)  # must match Y0, Y1 in gen_stats.py

ROLES = ["Designer", "Developer", "Builder"]
HEADLINE = ["Designing & Building", "Digital Products", "That Matter."]
INTRO = ["Product designer & developer, building useful,",
         "delightful and impactful digital products for",
         "students, creators and real-world problems."]
FACTS = [("map_pin", ["Bhubaneswar,", "India"]), ("grad_cap", ["KIIT", "University"]), ("calendar", ["3rd", "Year"])]
CHIPS = [("envelope", "Product Design"), ("code", "Full-Stack Dev"), ("sun", "AI/ML")]
NOTES = [  # "Currently building" sticky notes
    {"key": "omni", "name": "Omni KIIT", "lines": ["Campus super-app", "for KIIT students."]},
    {"key": "smartschedule", "name": "SmartSchedule", "lines": ["AI-driven academic", "section optimizer."]},
]
MORE = [  # "More projects" list (the whole list links to the repositories tab)
    {"name": "RootRunner", "desc": "Iterative DNS resolution engine."},
    {"name": "ScamBust", "desc": "AI-powered scam detection."},
    {"name": "Price Prediction", "desc": "Market price prediction using ML."},
    {"name": "Wakewise", "desc": "Habit-aware smart alarm."},
]
APPROACH = [("lightbulb", "#FDB0DD", "Discover", ["Understand", "the problem."]),
            ("pencil", "#DDB9FD", "Design", ["Explore &", "shape solutions."]),
            ("code", "#CFAAFC", "Build", ["Turn ideas", "into reality."]),
            ("refresh", C["lime"], "Iterate", ["Improve with", "real feedback."])]
TOOLKIT = [["python", "postgresql", "kotlin", "java", "cpp", "c"],
           ["flutter", "jetpackcompose", "android", "fastapi", "pandas", "scikitlearn", "figma"]]
TOOL_NAMES = {"python": "Python", "postgresql": "PostgreSQL", "kotlin": "Kotlin", "java": "Java", "cpp": "C++",
              "c": "C", "flutter": "Flutter", "jetpackcompose": "Jetpack Compose", "android": "Android",
              "fastapi": "FastAPI", "pandas": "pandas", "scikitlearn": "scikit-learn", "figma": "Figma"}
BUTTONS = [("email", "Email", 87, 190), ("linkedin", "LinkedIn", 293, 209), ("github", "GitHub", 518, 199)]



def hv(size):
    """Extra outline for heavy headings, to match the mockup's black weight without closing up counters."""
    return size * 0.02


DEFS = [
    '<filter id="paper-shadow" x="-12%" y="-12%" width="126%" height="130%">'
    '<feDropShadow dx="-3" dy="7" stdDeviation="3" flood-color="#5E5650" flood-opacity=".34"/></filter>',
    '<filter id="soft-shadow" x="-15%" y="-15%" width="130%" height="140%">'
    '<feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#5B4335" flood-opacity=".13"/></filter>',
    '<linearGradient id="lime-paper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EDFD8E"/>'
    '<stop offset=".3" stop-color="#E2FC5C"/><stop offset="1" stop-color="#DCF94C"/></linearGradient>',
    '<linearGradient id="pink-paper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FEB4E0"/>'
    '<stop offset=".35" stop-color="#FDA2D9"/><stop offset="1" stop-color="#FC9BD5"/></linearGradient>',
    '<linearGradient id="ring-top" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FAFAFA"/>'
    '<stop offset=".55" stop-color="#C9C9C9"/><stop offset="1" stop-color="#8C8C8C"/></linearGradient>',
]


def g(svg, x=0, y=0, angle=0, sx=1, sy=1, skew=0, extra=""):
    """Wrap svg drawn around the origin: scale, skew, rotate (degrees), then move to (x, y)."""
    t = f"translate({fmt(x)} {fmt(y)})"
    if angle:
        t += f" rotate({fmt(angle)})"
    if skew:
        t += f" skewX({fmt(skew)})"
    if sx != 1 or sy != 1:
        t += f" scale({sx:.4f} {sy:.4f})"
    return f'<g transform="{t}"{extra}>{svg}</g>'


def hand(s, x, y, width, angle, color, weight=2.0, sx=0.9, skew=-7):
    """Handwritten text (Kalam) `width` units wide, thickened with a matching outline, rotated about its start."""
    size = width / (sx * tw("hand", s, 1))
    body = text("hand", s, 0, 0, size, color, heavy=weight / sx)
    return g(body, x, y, angle, sx, 1, skew)


def slash(x, baseline, h, w=12, lean=12):
    return poly([(x + lean, baseline - h), (x + lean + w, baseline - h), (x + w, baseline), (x, baseline)], C["pink"])


def arrow_ur(left, bottom, length, sw=4.4):
    """A north-east arrow whose visible shape is `length` units square, its bottom-left corner at (left, bottom)."""
    size = length * 2.4  # the Lucide glyph spans 10 of its 24 units
    return icon("arrow_up_right", left - size * 7 / 24, bottom - size * 17 / 24, size, C["ink"], sw)


def swoosh(x0, y0, cx, cy, x1, y1, w0, w1, color):
    """A brush stroke along a quadratic curve, tapering from width w0 to w1."""
    top, bot = [], []
    n = 16
    for i in range(n + 1):
        t = i / n
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1
        dx = 2 * (1 - t) * (cx - x0) + 2 * t * (x1 - cx)
        dy = 2 * (1 - t) * (cy - y0) + 2 * t * (y1 - cy)
        ln = math.hypot(dx, dy)
        hw = (w0 + (w1 - w0) * t) / 2
        top.append((px + dy / ln * hw, py - dx / ln * hw))
        bot.append((px - dy / ln * hw, py + dx / ln * hw))
    return poly(top + bot[::-1], color, extra=f' stroke="{color}" stroke-width="2" stroke-linejoin="round"')


def rings(cx, cy, s):
    """RootRunner's stacked-disc mark, centred at (cx, cy) in an s-wide box."""
    out = []
    rx, ry = s * 0.44, s * 0.15
    for i in (2, 1, 0):
        y = cy - s * 0.3 + i * s * 0.24
        out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(y + s * 0.075)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="#4E4E4E"/>')
        out.append(rect(cx - rx, y, 2 * rx, s * 0.075, "#6E6E6E"))
        out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(y)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="url(#ring-top)"/>')
        out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(y)}" rx="{fmt(rx * 0.45)}" ry="{fmt(ry * 0.45)}" fill="#3B3B3B"/>')
    return "".join(out)


def bars(x, y, s, color):
    """Price-prediction mark: three rising columns on a base line, in an s x s box at (x, y)."""
    k = s / 80
    sw = 5.4
    out = strokes([((x + 2 * k, y + 76 * k), (x + 78 * k, y + 76 * k))], color, sw)
    for bx, top in ((8, 50), (30, 30), (54, 6)):
        out += rect(x + bx * k, y + top * k, 16 * k, (74 - top) * k, C["bg"], stroke=color, sw=sw, rx=1.5)
    out += strokes([((x + 10 * k, y + 32 * k), (x + 10 * k, y + 44 * k)), ((x + 4 * k, y + 38 * k), (x + 16 * k, y + 38 * k))],
                   color, 4.2)
    return out


def sparkle(cx, cy, s):
    """Four-point twinkle with a warm centre (the star on the Omni KIIT note)."""
    r, n = s / 2, s * 0.09
    pts = []
    for i in range(8):
        a = math.radians(i * 45 - 90)
        rr = r if i % 2 == 0 else n
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    star = poly(pts, "#FFE7CF", extra=' stroke="#2E211A" stroke-width="2.6" stroke-linejoin="round"')
    return star + f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(s * 0.11)}" fill="#F9B7D9"/>'


def lang_letter(kind, cx, cy, s):
    """C and C++ marks drawn as heavy letterforms, as on the mockup's toolkit tiles."""
    if kind == "c":
        size = s * 1.1
        return text("display", "C", cx, cy + cap("display", size) / 2, size, "#22409A", anchor="middle", heavy=2)
    size = s * 1.0
    w = tw("display", "C", size)
    pw, pt, gap = s * 0.27, s * 0.095, s * 0.02
    x0 = cx - (w + 2 * (pw + gap)) / 2
    out = text("display", "C", x0, cy + cap("display", size) / 2, size, "#1F7AE0", heavy=2)
    px = x0 + w + gap
    for _ in range(2):
        out += rect(px, cy - pt / 2, pw, pt, "#1F7AE0") + rect(px + pw / 2 - pt / 2, cy - pw / 2, pt, pw, "#1F7AE0")
        px += pw + gap
    return out


# ------------------------------------------------------------------ sections

def header(sc):
    sc.region = (0, W, 0, 110)
    sc.add(logo(72, 43, 60, C["ink"]))
    sc.add(line(248, 46, 248, 100, "#CFC7BE", 2.4))
    sc.add(text("display", USER, 280, 86, 40.3, C["ink"], ls=-0.02, heavy=hv(40.3)))
    size, gap = 29.7, 34
    total = sum(tw("semi", r, size) for r in ROLES) + (len(ROLES) - 1) * (2 * gap + 24)
    x = 1647 - total
    for i, role in enumerate(ROLES):
        if i:
            sc.add(slash(x + gap, 76, 23))
            x += 2 * gap + 24
        sc.add(text("semi", role, x, 76, size, C["text"]))
        x += tw("semi", role, size)


def hero(sc):
    sc.region = (0, W, 110, 1000)
    sc.add(raster(os.path.join(ART, "workspace.webp"), 678, 112, 1078, 876), 678, 1756, 112, 988)

    sc.add(hand("Hi, I’m", 92, 250, 206, -12, C["pink"], 1.6))
    sc.add(strokes(["M331 150L321 172", "M337 181L368 171", "M340 199L366 204"], C["pink"], 4.8))
    size = 345 / tw("displayi", "Piyush", 1, -0.01)
    sc.add(g(text("displayi", "Piyush", 0, 0, size, C["ink"], ls=-0.01, heavy=3.2), 160, 326, -6.2))
    sc.add(swoosh(240, 362, 372, 334, 523, 316, 16, 5, C["pink"]))
    sc.add(strokes(["M560 274L546 294", "M562 303L593 293", "M565 322L588 331"], C["pink"], 4.8))

    hs = 67.5
    sc.add(text("display", HEADLINE[0], 105, 446, hs, C["ink"], ls=-0.02, heavy=hv(hs)))
    sc.add(text("display", HEADLINE[1], 105, 518, hs, C["ink"], ls=-0.02, heavy=hv(hs)))
    hs = 72
    hw = tw("display", HEADLINE[2], hs, -0.02)
    sc.add(rect(92, 537, hw + 44, 79, C["pink"], rx=12))
    sc.add(text("display", HEADLINE[2], 110, 603, hs, C["ink"], ls=-0.02, heavy=hv(hs)))
    sc.add(strokes(["M606 577L612 592L625 575", "M641 563L669 560L660 580"], C["pink"], 5.4))

    for i, s in enumerate(INTRO):
        sc.add(text("body", s, 104, 673 + i * 38.5, 29.5, C["text"], heavy=0.4))

    for (ic, lines), ix, tx in zip(FACTS, (97, 380, 658), (160, 454, 734)):
        isz = 48 if ic == "grad_cap" else 43
        sc.add(icon(ic, ix, 831 - isz / 2, isz, C["ink"], 3.8))
        for j, s in enumerate(lines):
            sc.add(text("body", s, tx, 829 + j * 35, 24, C["text"], heavy=0.4))

    x = 100
    for ic, label in CHIPS:
        w = 77 + tw("semi", label, 22.3) + 28
        sc.add(rect(x, 908, w, 58, C["card"], rx=29, stroke=C["chip_line"], sw=2.2))
        sc.add(icon(ic, x + 28, 937 - 16, 32, C["ink"], 3.3))
        sc.add(text("semi", label, x + 77, 937 + cap("semi", 22.3) / 2, 22.3, C["ink"], heavy=0.3))
        x += w + 27


def sticky_note(cx, cy, w, h, angle, paper, fold_color, fold, tape_dx, content):
    """A taped sticky note centred at (cx, cy); `content` is drawn in the note's own frame (origin = centre)."""
    f = 34
    l, t, r, b = -w / 2, -h / 2, w / 2, h / 2
    flaps = []
    if fold == "top-right":
        shape = [(l, t), (r - f, t), (r, t + f), (r, b), (l, b)]
        flaps.append([(r - f, t), (r - f + 3, t + f - 3), (r, t + f)])
    else:
        f2 = 22
        shape = [(l + f2, t), (r, t), (r, b - f), (r - f, b), (l, b), (l, t + f2)]
        flaps.append([(r, b - f), (r - f + 3, b - f + 3), (r - f, b)])
        flaps.append([(l + f2, t), (l + f2 - 2, t + f2 - 2), (l, t + f2)])
    paper_svg = poly(shape, f"url(#{paper})", extra=' filter="url(#paper-shadow)"')
    flap_svg = "".join(poly(fl, fold_color, extra=' stroke="#0000001A" stroke-width="1.5" stroke-linejoin="round"')
                       for fl in flaps)
    tape = (rect(-21, -30, 42, 60, C["tape"], rx=2) + rect(-21, -30, 42, 7, "#47444A") +
            rect(-21, 23, 42, 7, "#232124"))
    body = paper_svg + flap_svg + content + g(tape, tape_dx, t + 2, -2)
    return g(body, cx, cy, angle)


def note_tile(cx, cy, w, h):
    return rect(cx - w / 2, cy - h / 2, w, h, C["tile_dark"], rx=18) + logo(cx - 33.75, cy - 15, 30, C["white"])


def projects(sc):
    y0, y1 = 1010, 1530
    sc.region = (0, W, y0, y1)
    sc.add(section_title(77, 1083, "Currently Building"), 0, 967, y0, 1110)
    sc.add(section_title(1017, 1083, "More Projects"), 967, W, y0, 1110)
    sc.add(line(967, 1050, 967, 1503, C["rule"], 2), 960, 975, y0, y1)

    # sticky notes
    omni, smart = NOTES
    c = note_tile(-95, -79, 100, 84) + sparkle(111, -91, 52)
    c += text("display", omni["name"], -135, 16, 39, C["ink"], ls=-0.02, heavy=hv(39))
    c += arrow_ur(-135 + tw("display", omni["name"], 39, -0.02) + 14, 14, 23)
    for i, s in enumerate(omni["lines"]):
        c += text("body", s, -134, 66 + i * 37, 28.5, C["ink"], heavy=0.4)
    sc.add(sticky_note(281, 1328, 371, 336, -3.9, "lime-paper", "#F4FEC4", "top-right", -6, c), 40, 500, 1100, y1)

    c = note_tile(-107, -88, 100, 82)
    c += text("displayi", smart["name"], -150, 12, 36, C["ink"], ls=-0.02, heavy=hv(36))
    c += arrow_ur(-150 + tw("displayi", smart["name"], 36, -0.02) + 14, 12, 23)
    for i, s in enumerate(smart["lines"]):
        c += text("body", s, -148, 65 + i * 40, 28.5, C["ink"], heavy=0.4)
    sc.add(sticky_note(703, 1338, 386, 316, 3.7, "pink-paper", "#FED3EC", "bottom-right", 26, c), 480, 960, 1100, y1)
    sc.add(strokes(["M833 1123L834 1139", "M872 1109L854 1142", "M893 1137L868 1151"], C["ink"], 4.8),
           820, 900, 1100, 1160)

    # more projects
    marks = [lambda cy: rings(1100, cy, 76),
             lambda cy: icon("shield_check", 1062, cy - 38, 76, C["ink"], 5.4),
             lambda cy: bars(1060, cy - 40, 80, C["ink"]),
             lambda cy: moon(1064, cy - 38, 76, C["ink"])]
    for i, (p, mark) in enumerate(zip(MORE, marks)):
        base = 1148 + i * 103.4
        top, bot = (1112, 1206, 1311, 1416)[i], (1206, 1311, 1416, 1530)[i]
        sc.add(mark(base + 10), 1040, 1160, top, bot)
        sc.add(text("display", p["name"], 1182, base, 29.5, C["ink"], ls=-0.015, heavy=hv(29.5)), 1170, 1600, top, bot)
        sc.add(arrow_ur(1182 + tw("display", p["name"], 29.5, -0.015) + 14, base - 1, 19, 4.2), 1170, 1600, top, bot)
        sc.add(text("body", p["desc"], 1182, base + 35, 24.5, C["text"], heavy=0.4), 1170, 1650, top, bot)
        sc.add(arrow_ur(1674, base + 13, 26, 4.4), 1660, 1710, top, bot)
        if i < 3:
            sc.add(line(1182, bot, 1707, bot, C["line"], 2.2), 1170, 1710, bot - 3, bot + 3)


def approach_toolkit(sc):
    y0, y1 = 1530, 1900
    sc.region = (0, W, y0, y1)
    sc.add(line(72, 1543, 1707, 1543, C["line"], 2.4))
    sc.add(line(72, 1893, 1707, 1893, C["line"], 2.4))
    sc.add(section_title(77, 1615, "My Approach"))
    sc.add(section_title(1019, 1615, "Toolkit"))
    sc.add(line(970, 1585, 970, 1848, C["rule"], 2))

    for i, (ic, color, label, lines) in enumerate(APPROACH):
        x = (79, 309, 534, 761)[i]
        cx = x + 63
        sc.add(rect(x, 1645, 126, 95, color, rx=20))
        sc.add(icon(ic, cx - 27, 1692 - 27, 54, C["ink"], 4))
        if i < 3:
            sc.add(icon("arrow_right", (258, 482, 709)[i] - 26, 1694 - 26, 52, C["ink"], 4))
        sc.add(text("display", label, cx, 1783, 29.3, C["ink"], anchor="middle", ls=-0.01, heavy=hv(29.3)))
        for j, s in enumerate(lines):
            sc.add(text("body", s, cx, 1816 + j * 30, 23.2, C["text"], anchor="middle", heavy=0.4))

    # Tiles are sized to fit the longest row within [tx0, tx1], so the grid stays inside the
    # poster however many tools each row holds; shorter rows are centred under the longest one.
    tx0, tx1, gap, ygap = 1005, 1707, 14, 15
    cols = max(len(r) for r in TOOLKIT)
    tile = (tx1 - tx0 - (cols - 1) * gap) / cols
    th = tile * 0.95
    pitch = tile + gap
    isz = tile * 0.62
    for r, row in enumerate(TOOLKIT):
        y = 1645 + r * (th + ygap)
        row_w = len(row) * tile + (len(row) - 1) * gap
        rx0 = tx0 + (tx1 - tx0 - row_w) / 2
        for i, name in enumerate(row):
            x = rx0 + i * pitch
            sc.add(rect(x, y, tile, th, C["card"], rx=tile * 0.18, stroke=C["card_line"], sw=2,
                        extra=' filter="url(#soft-shadow)"'))
            if name in ("c", "cpp"):
                sc.add(lang_letter(name, x + tile / 2, y + th / 2, tile * 0.6))
            else:
                sc.add(brand_icon(name, x + tile / 2 - isz / 2, y + th / 2 - isz / 2, isz))


def footer(sc, clip):
    y0 = STATS_ROW[1]
    sc.region = (0, W, y0, H)
    sc.add(raster(os.path.join(ART, "campus.webp"), 652, 2198, 1108, 388, extra=clip), 652, W, y0, H)
    cells = (rect(32, 2520, 28, 27, C["pink"]) + rect(-2, 2547, 34, 26, C["pink"]) +
             poly([(60, 2547), (86, 2547), (69, 2573), (60, 2573)], C["pink"]) + rect(32, 2573, 28, 20, C["pink"]))
    sc.add(f'<g{clip}>{cells}</g>', 0, 100, 2500, H)

    sc.add(hand("Let’s Build", 90, 2321, 282, -10.5, C["ink"], 2.6), 0, 640, y0, 2430)
    sc.add(hand("Something", 101, 2388, 255, -10, C["ink"], 2.6), 0, 640, y0, 2430)
    box = rect(-77, -37, 154, 72, C["pink"], rx=10)
    cool = hand("Cool!", -63, 23, 126, 0, C["ink"], 2.6)
    sc.add(g(box + cool, 455, 2323, -8), 0, 640, y0, 2430)
    sc.add(strokes(["M542 2266L531 2285", "M568 2281L545 2291", "M548 2305L570 2309"], C["pink"], 4.8), 0, 640, y0, 2430)
    sc.add(strokes(["M494 2377C530 2360 576 2366 593 2416", "M571 2407L593 2419L596 2396"], C["ink"], 4.8),
           480, 610, y0, 2430)

    for key, label, x, w in BUTTONS:
        y, h = 2436, 67
        sc.add(rect(x, y, w, h, C["card"], rx=14, stroke="#262422", sw=2.8), x - 2, x + w + 2, y - 2, y + h + 2)
        lw = tw("semi", label, 26.5)
        isz = 36
        cx0 = x + (w - (isz + 14 + lw)) / 2
        cy = y + h / 2
        if key == "email":
            ic = icon("envelope", cx0, cy - isz / 2 + 1, isz, C["ink"], 3.4)
        elif key == "linkedin":
            ic = text("display", "in", cx0 + isz / 2, cy + cap("display", 38) / 2, 38, C["ink"], anchor="middle",
                      ls=-0.02, heavy=1)
        else:
            ic = github_mark(cx0, cy - isz / 2, isz, C["ink"])
        sc.add(ic + text("semi", label, cx0 + isz + 14, cy + cap("semi", 26.5) / 2, 26.5, C["ink"], heavy=0.4),
               x, x + w, y, y + h)


# ------------------------------------------------------------------ assembly

def build_scene():
    sc = Scene()
    sc.defs.extend(DEFS)
    bg = poster_bg(W, H, top=True, bottom=True)
    sc.defs.append(f'<clipPath id="poster-clip">{bg.replace(" fill=", " data-fill=")}</clipPath>')
    sc.add(bg, 0, W, 0, H)
    header(sc)
    hero(sc)
    projects(sc)
    approach_toolkit(sc)
    footer(sc, ' clip-path="url(#poster-clip)"')
    return sc


def cut(sc, name, x0, y0, x1, y1, alt, href=None):
    write(name, sc.svg(x0, y0, x1, y1, title=alt))
    return {"src": f"assets/{name}", "w": x1 - x0, "alt": alt, "href": href}


def readme(rows):
    lines = []
    for row in rows:
        parts = []
        for t in row:
            img = f'<img src="{t["src"]}" width="{t["w"] / W * 99.9:.4f}%" align="top" alt="{esc(t["alt"])}">'
            parts.append(f'<a href="{t["href"]}">{img}</a>' if t["href"] else img)
        lines.append("".join(parts))
    body = "<br>\n".join(lines)
    return ("<!-- Generated by .github/scripts/build_assets.py: edit that file and re-run it to change this page. -->\n\n"
            f'<div align="center">\n{body}\n</div>\n')


def main():
    sc = build_scene()
    rows = []
    hero_alt = ("MaiCoderHoon. Hi, I'm Piyush: designing and building digital products that matter. "
                "Product designer and developer in Bhubaneswar, India; 3rd year at KIIT University. "
                "Product design, full-stack development, AI/ML.")
    rows.append([cut(sc, "hero.svg", 0, 0, W, 1010, hero_alt)])

    # Rows of tiles stay at least ~190 units tall: a shorter strip is padded out by the
    # page's line height on phones, which shows up as gaps. So the four "more projects"
    # share one link (the repositories tab) instead of one thin strip each.
    more = "; ".join(f'{p["name"]}: {p["desc"]}' for p in MORE)
    rows.append([
        cut(sc, "projects-omni.svg", 0, 1010, 490, 1530,
            "Currently building: Omni KIIT, a campus super-app for KIIT students.", LINKS["omni"]),
        cut(sc, "projects-smartschedule.svg", 490, 1010, 967, 1530,
            "SmartSchedule: AI-driven academic section optimizer.", LINKS["smartschedule"]),
        cut(sc, "projects-more.svg", 967, 1010, W, 1530, f"More projects. {more}", LINKS["repos"]),
    ])

    tools = ", ".join(TOOL_NAMES[n] for row in TOOLKIT for n in row)
    rows.append([cut(sc, "approach.svg", 0, 1530, W, STATS_ROW[0],
                     f"My approach: discover, design, build, iterate. Toolkit: {tools}.")])
    rows.append([{"src": STATS_URL, "w": W, "href": LINKS["profile"],
                  "alt": "Live GitHub stats (repos, commits, pull requests, stars) and contribution graph"}])

    y0 = STATS_ROW[1]
    rows.append([cut(sc, "footer-top.svg", 0, y0, W, 2400, "Let's build something cool!")])
    rows.append([cut(sc, "footer-l.svg", 0, 2400, 85, H, "")] +
                [cut(sc, f"footer-{k}.svg", x0, 2400, x1, H, label, LINKS[k])
                 for (k, label, _, _), (x0, x1) in zip(BUTTONS, ((85, 285), (285, 510), (510, 725)))] +
                [cut(sc, "footer-campus.svg", 725, 2400, W, H, "KIIT campus")])

    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(readme(rows))

    produced = {os.path.basename(t["src"]) for row in rows for t in row if t["src"].startswith("assets/")}
    for old in os.listdir(ASSETS):  # drop assets from earlier designs
        if old.endswith(".svg") and old not in produced and old != "stats.svg":
            os.remove(os.path.join(ASSETS, old))
    print("wrote README.md and", len(produced), "assets")


if __name__ == "__main__":
    main()
