#!/usr/bin/env python3
"""Build the profile poster (assets/*.svg) and README.md.

    python .github/scripts/build_assets.py

Change the copy or links below, then re-run. The poster is a stack of full-width
SVG rows; rows with buttons are cut into slices so each button can be its own
link. The stats row (assets/stats.svg) is refreshed by gen_stats.py on a schedule.
"""
import os
import random

from svgkit import (ASSETS, C, HERE, MARGIN, W, Scene, brand_icon, cap, esc, fit, fmt, github_mark, icon, line,
                    poly, poster_bg, rect, section_title, text, tw, write)

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
USER = "MaiCoderHoon"
GH = f"https://github.com/{USER}"
LINKS = {
    "profile": GH,
    "repos": f"{GH}?tab=repositories",
    "omni": f"{GH}?tab=repositories",        # Omni KIIT has no public repo yet; swap in its URL when it does
    "smartschedule": f"{GH}/SmartSelector",
    "rootrunner": f"{GH}/RootRunner",
    "email": "mailto:piyush993bisoi@outlook.com",
    "linkedin": "https://www.linkedin.com/in/piyush-bisoi",
    "portfolio": f"{GH}?tab=repositories",   # swap in a portfolio site when there is one
    "github": GH,
}

PROJECTS = [  # "short" = hero panel copy, "long" = selected-work card copy (one list item per line)
    {"key": "omni", "name": "Omni KIIT", "short": ["Campus super-app", "for KIIT students."],
     "long": ["A campus super-app", "for KIIT students."], "file": "card-omni-kiit.svg"},
    {"key": "smartschedule", "name": "SmartSchedule", "short": ["AI-driven section", "optimizer."],
     "long": ["AI-driven academic", "section optimizer."], "file": "card-smartschedule.svg"},
    {"key": "rootrunner", "name": "RootRunner", "short": ["Iterative DNS", "resolution engine."],
     "long": ["Iterative DNS", "resolution engine", "in Python."], "file": "card-rootrunner.svg"},
]

# Rebuilt every 10 minutes by .github/workflows/stats.yml and published to the `output` branch.
STATS_URL = f"https://raw.githubusercontent.com/{USER}/{USER}/output/stats.svg"

HERO_ALT = ("Piyush — designing and building digital products that matter. Product-minded designer and developer. "
            "Currently building Omni KIIT, SmartSchedule and RootRunner.")

WHITE = "#FFFFFF"
SOFT_WHITE = "#D4D4D4"


# ------------------------------------------------------------------ marks & logos

def pixel_mark(x, y, s, main, accent, dark=None):
    """The MaiCoderHoon / Omni pixel monogram in an s x s box."""
    u = s / 4
    out = []
    solid = [(0, 0), (0, 1), (0, 2), (0, 3), (2, 0), (3, 0), (1, 3), (2, 3)]
    soft = [(2, 1), (1, 2)]
    for cx, cy in solid:
        out.append(rect(x + cx * u, y + cy * u, u + 0.3, u + 0.3, main))
    for cx, cy in soft:
        out.append(rect(x + cx * u, y + cy * u, u + 0.3, u + 0.3, accent))
    tri = dark or main
    out.append(poly([(x + 2 * u, y + 2 * u), (x + 3 * u, y + 3 * u), (x + 2 * u, y + 3 * u)], tri))
    return "".join(out)


def smart_logo(x, y, s):
    u = s / 54
    out = rect(x, y, s, s, C["lime"], rx=11 * u)
    out += poly([(x + 15 * u, y + 18 * u), (x + 15 * u, y + 39 * u), (x + 36 * u, y + 39 * u)], C["ink"])
    out += rect(x + 29 * u, y + 17 * u, 9 * u, 9 * u, C["ink"])
    return out


def rings_logo(x, y, s, grad="ringTop"):
    out = []
    rx, ry = s * 0.44, s * 0.155
    cx = x + s / 2
    for i in (2, 1, 0):
        cy = y + s * 0.27 + i * s * 0.23
        out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy + s * 0.07)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="#5E5E5E"/>')
        out.append(f'<rect x="{fmt(cx - rx)}" y="{fmt(cy)}" width="{fmt(2 * rx)}" height="{fmt(s * 0.07)}" fill="#7A7A7A"/>')
        out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="url(#{grad})"/>')
        out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(rx * 0.46)}" ry="{fmt(ry * 0.46)}" fill="#3B3B3B"/>')
    return "".join(out)


RING_GRAD = ('<linearGradient id="ringTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FAFAFA"/>'
             '<stop offset=".55" stop-color="#C9C9C9"/><stop offset="1" stop-color="#8C8C8C"/></linearGradient>')


def project_logo(key, x, y, s):
    if key == "omni":
        return pixel_mark(x + s * 0.06, y + s * 0.06, s * 0.88, "#F2F2F2", "#B9B9B9", dark=C["ink"])
    if key == "smartschedule":
        return smart_logo(x, y, s)
    return rings_logo(x, y, s)


#  Toolkit tiles, taken from the resume: languages on top, frameworks / ML / tools below.
#  (label, logo file in brand-icons/ or "sql" for the generic database icon)
TOOLKIT = [
    [("Python", "python"), ("SQL", "sql"), ("Kotlin", "kotlin"), ("Java", "java"), ("C++", "cplusplus"),
     ("Dart", "dart"), ("C", "c")],
    [("Flutter", "flutter"), ("Compose", "jetpackcompose"), ("FastAPI", "fastapi"), ("Pandas", "pandas"),
     ("scikit-learn", "scikitlearn"), ("Figma", "figma"), ("Git", "git")],
]


def checker(x, y, cell, n, colors, flip=False):
    """Pink stair-step checker; bottom-right aligned staircase."""
    out = []
    for r in range(n):
        for c in range(n - 1 - r, n):
            if (r + c) % 2 == (n - 1) % 2:
                col = colors[0]
            else:
                if len(colors) < 2:
                    continue
                col = colors[1]
            out.append(rect(x + c * cell, y + r * cell, cell + 0.2, cell + 0.2, col))
    return "".join(out)


# ------------------------------------------------------------------ rows

# Every exported strip is at least MIN_STRIP units tall: GitHub lays the strips out as
# lines of text, and a strip shorter than one line-height (24px) would leave a gap
# under it on narrow (320px+) screens.
MIN_STRIP = 116


def row_nav():
    h = MIN_STRIP
    sc = Scene(h)
    sc.add(poster_bg(W, h, top=True))
    cy = 62
    sc.add(rect(MARGIN, cy - 22, 44, 44, C["ink"], rx=7) + pixel_mark(MARGIN + 9, cy - 13, 26, C["pink"], C["pink_pale"]), 0, 120)
    bsize = 27
    bx = MARGIN + 60
    sc.add(text("display", "MaiCoderHoon", bx, cy + cap("display", bsize) / 2, bsize, C["ink"], ls=-0.02), 0, 400)
    brand_end = bx + tw("display", "MaiCoderHoon", bsize, -0.02)

    ax = W - MARGIN - 44
    sc.add(rect(ax, cy - 22, 44, 44, C["pink"], rx=4) + icon("arrow_up_right", ax + 8, cy - 14, 28, C["ink"], 2.6), ax - 5, W)

    labels = ["ABOUT", "PROJECTS", "TOOLKIT", "NOW", "CONNECT"]
    nsize, ls, gap = 18, 0.02, 20
    slash_w = tw("semi", "/", nsize)
    widths = [tw("semi", s, nsize, ls) for s in labels]
    total = sum(widths) + (len(labels) - 1) * (2 * gap + slash_w)
    x = ax - 34 - total
    base = cy + cap("semi", nsize) / 2
    starts = []
    for i, (label, w) in enumerate(zip(labels, widths)):
        starts.append(x)
        sc.add(text("semi", label, x, base, nsize, C["ink"], ls=ls), x - 2, x + w + 2)
        x += w
        if i < len(labels) - 1:
            sc.add(text("semi", "/", x + gap, base, nsize, C["ink"]), x + gap - 2, x + gap + slash_w + 2)
            x += 2 * gap + slash_w
    sc.add(line(brand_end + 26, cy, starts[0] - 30, cy, C["ink"], 1.6), brand_end, starts[0])

    b = [0] + [starts[0] - 15] + [s - gap / 2 for s in starts[1:]] + [W]
    targets = [("nav-brand.svg", LINKS["profile"], "MaiCoderHoon"),
               ("nav-about.svg", "#about", "About"),
               ("nav-projects.svg", "#projects", "Projects"),
               ("nav-toolkit.svg", "#toolkit", "Toolkit"),
               ("nav-now.svg", "#now", "Now"),
               ("nav-connect.svg", "#connect", "Connect")]
    return sc, [(f, b[i], b[i + 1], href, alt) for i, (f, href, alt) in enumerate(targets)]


def building(sc):
    """Grayscale concrete building corner on a pink stepped backdrop."""
    AX, AY, LX, RX, BOT, SL = 738, 14, 572, 832, 418, 1.1
    rnd = random.Random(7)
    out = []
    # pink stepped backdrop
    out.append(poly([(668, 48), (RX, 48), (RX, BOT), (572, BOT), (572, 162), (600, 162), (600, 124),
                     (634, 124), (634, 86), (668, 86)], C["pink"]))

    def lp(u, v):
        return (AX - u * (AX - LX), AY + u * (AX - LX) * SL + v)

    def rp(u, v):
        return (AX + u * (RX - AX), AY + u * (RX - AX) * SL + v)

    left_face = [lp(0, 0), lp(1, 0), (LX, BOT), (AX, BOT)]
    right_face = [rp(0, 0), rp(1, 0), (RX, BOT), (AX, BOT)]
    sc.defs.append('<clipPath id="bldg"><path d="M' + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in
                   [lp(1, 0), lp(0, 0), rp(1, 0), (RX, BOT), (LX, BOT)]) + 'Z"/></clipPath>')
    sc.defs.append('<linearGradient id="lface" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B4B2AE"/>'
                   '<stop offset="1" stop-color="#9A9894"/></linearGradient>')
    sc.defs.append('<linearGradient id="rface" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A3A3A"/>'
                   '<stop offset="1" stop-color="#262626"/></linearGradient>')
    sc.defs.append('<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4A4F55"/>'
                   '<stop offset=".5" stop-color="#202326"/><stop offset="1" stop-color="#383C41"/></linearGradient>')
    sc.defs.append('<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C0C0C"/>'
                   '<stop offset="1" stop-color="#3A3A3A"/></linearGradient>')
    sc.defs.append('<filter id="grain" x="0" y="0" width="1" height="1"><feTurbulence type="fractalNoise" baseFrequency=".85" '
                   'numOctaves="2" seed="4"/><feColorMatrix type="matrix" values="0 0 0 0 .12  0 0 0 0 .12  0 0 0 0 .12  0 0 0 -2.2 1.12"/></filter>')

    g = ['<g clip-path="url(#bldg)">']
    g.append(poly(left_face, "url(#lface)"))
    g.append(poly(right_face, "url(#rface)"))

    def panels(pt, cols, v_rows, tone, skip=None):
        res = []
        for i in range(cols):
            u0, u1 = i / cols, (i + 1) / cols
            for v0, v1 in v_rows:
                if skip and skip(u0, u1, v0, v1):
                    continue
                t = tone + rnd.randint(-9, 9)
                col = f"#{t:02X}{t:02X}{max(0, t - 3):02X}"
                gp = 1.3
                a, b2 = pt(u0, v0 + gp), pt(u1, v0 + gp)
                c2, d2 = pt(u1, v1 - gp), pt(u0, v1 - gp)
                inset = 1.1
                res.append(poly([(a[0] - inset if pt is lp else a[0] + inset, a[1]),
                                 (b2[0] + inset if pt is lp else b2[0] - inset, b2[1]),
                                 (c2[0] + inset if pt is lp else c2[0] - inset, c2[1]),
                                 (d2[0] - inset if pt is lp else d2[0] + inset, d2[1])], col))
        return res

    band = (150, 180)
    upper = [(v, v + 37.5) for v in (0, 37.5, 75, 112.5)]
    lower = [(v, v + 38) for v in range(180, 420, 38)]
    # left face: light concrete panels, windows lower-left, recessed doorway
    g += panels(lp, 5, upper, 0xE2)
    g += panels(lp, 5, lower, 0xD9, skip=lambda u0, u1, v0, v1: (u0 >= 0.6 and v0 >= 218) or (0.2 <= u0 < 0.6 and v0 >= 332))
    # right face: dark panels
    g += panels(rp, 3, upper, 0x5C)
    g += panels(rp, 3, lower, 0x55, skip=lambda u0, u1, v0, v1: u0 >= 0.33 and 218 <= v0 < 294)
    # recessed band across both faces
    g.append(poly([lp(0, band[0]), lp(1, band[0]), lp(1, band[1]), lp(0, band[1])], "url(#band)"))
    g.append(poly([rp(0, band[0]), rp(1, band[0]), rp(1, band[1]), rp(0, band[1])], "#141414"))
    # glazing
    g.append(poly([lp(0.6, 218), lp(1, 218), lp(1, 420), lp(0.6, 420)], "url(#glass)"))
    for u in (0.68, 0.76, 0.84, 0.92):
        a, b2 = lp(u, 218), lp(u, 420)
        g.append(line(a[0], a[1], b2[0], b2[1], "#B9B9B9", 1.1))
    a, b2 = lp(0.6, 300), lp(1, 300)
    g.append(line(a[0], a[1], b2[0], b2[1], "#9C9C9C", 1))
    g.append(poly([lp(0.2, 332), lp(0.6, 332), lp(0.6, 420), lp(0.2, 420)], "#1B1C1E"))
    a = lp(0.4, 332)
    g.append(line(a[0], a[1], a[0], BOT, "#5A5A5A", 1))
    g.append(poly([rp(0.33, 218), rp(1, 218), rp(1, 294), rp(0.33, 294)], "#111214"))
    for u in (0.55, 0.78):
        a, b2 = rp(u, 218), rp(u, 294)
        g.append(line(a[0], a[1], b2[0], b2[1], "#4C4C4C", 1))
    # light grain
    g.append(f'<rect x="{LX}" y="{AY}" width="{RX - LX}" height="{BOT - AY}" filter="url(#grain)" opacity=".22"/>')
    g.append('</g>')
    out += g
    # crisp edges
    out.append(f'<path d="M{fmt(lp(1, 0)[0])} {fmt(lp(1, 0)[1])}L{AX} {AY}L{fmt(rp(1, 0)[0])} {fmt(rp(1, 0)[1])}" '
               f'fill="none" stroke="#141414" stroke-width="1.4" stroke-linejoin="round"/>')
    out.append(line(AX, AY, AX, BOT, "#F4F4F4", 1.1, ' stroke-opacity=".55"'))
    # pink checker + crosshair
    out.append(checker(RX - 4 * 14, BOT - 4 * 14, 14, 4, [C["pink"], C["pink_pale"]]))
    cx, cy = 590, 60
    out.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="{C["ink"]}" stroke-width="1.6"/>')
    out.append(line(cx - 25, cy, cx + 25, cy, C["ink"], 1.6) + line(cx, cy - 25, cx, cy + 25, C["ink"], 1.6))
    return "".join(out)


def row_hero():
    """Hero plus the SELECTED WORK heading; cropped into a top strip and a two-slice bottom strip."""
    h = 440 + 80
    sc = Scene(h)
    sc.add(poster_bg(W, h))
    sc.defs.append(RING_GRAD)
    # pixel deco
    u = 9
    for ch, i, j in [("K", 0, 0), ("P", 3, 0), ("K", 1, 1), ("P", 2, 1), ("P", 3, 1), ("K", 0, 2), ("P", 1, 2),
                     ("K", 2, 2), ("K", 0, 3), ("K", 1, 3), ("K", 0, 4)]:
        sc.add(rect(42 + i * u, 26 + j * u, u + 0.2, u + 0.2, C["ink"] if ch == "K" else C["pink"]), y1=80)

    # headline
    hx, left = 98, 88
    lines = ["DESIGNING &", "BUILDING", "DIGITAL PRODUCTS", "THAT MATTER."]
    hls = -0.035
    hs = min(fit("display", s, 62, 562 - hx, hls) for s in lines)
    ch = cap("display", hs)
    lh = hs * 0.9
    bases = [48 + ch + i * lh for i in range(4)]
    bases[3] += 6
    w4 = tw("display", lines[3], hs, hls)
    sc.add(rect(left, bases[3] - ch - 8, hx - left + w4 + 10, ch + 17, C["pink"]), y1=bases[3] + 12)
    for s, b in zip(lines, bases):
        sc.add(text("display", s, hx, b, hs, C["ink"], ls=hls), y1=b + 12)

    sub = ["Product-minded designer & developer, turning ideas", "into useful, delightful and impactful products."]
    ss = min(fit("body", s, 20.5, 560 - left) for s in sub)
    sb = bases[3] + 52
    for i, s in enumerate(sub):
        sc.add(text("body", s, left, sb + i * ss * 1.38, ss, C["text"]), y1=sb + i * ss * 1.38 + 8)

    # pills
    pills = [("Product Design", "box", True), ("Full-Stack Dev", "code", False), ("AI/ML", "sparkles", False)]
    ps, ph, pad, isz, gap = 17.5, 44, 17, 20, 12

    def pill_w(label, size):
        return pad + isz + 9 + tw("semi", label, size) + pad

    while sum(pill_w(p[0], ps) for p in pills) + gap * 2 > 560 - left:
        ps -= 0.25
    px, py = left, sb + ss * 1.38 + 26
    for label, ic, filled in pills:
        w = pill_w(label, ps)
        fg = WHITE if filled else C["ink"]
        sc.add(rect(px + 0.75, py + 0.75, w - 1.5, ph - 1.5, C["ink"] if filled else "none", rx=ph / 2,
                    stroke=C["ink"], sw=1.5)
               + icon(ic, px + pad, py + (ph - isz) / 2, isz, fg, 1.9)
               + text("semi", label, px + pad + isz + 9, py + ph / 2 + cap("semi", ps) / 2, ps, fg), y0=py - 1, y1=py + ph + 1)
        px += w + gap

    sc.add(building(sc), 560, 860)
    sc.add(line(858, 34, 858, 418, C["ink"], 1.5))

    # name column
    nx = 884
    col = []
    col.append(icon("arrow_up_right", nx - 4, 22, 34, C["ink"], 2.8))
    col.append(text("display", "PIYUSH", nx + 40, 51, 34, C["ink"], ls=-0.01))
    mono = ["Design, code, iterate,", "and ship – end to end."]
    ms = min(fit("mono", s, 18, 1106 - nx) for s in mono)
    for i, s in enumerate(mono):
        col.append(text("mono", s, nx, 96 + i * 27, ms, C["text"]))
    col.append(line(nx, 148, 1106, 148, C["ink"], 1.3))
    focus = ["Product Thinking", "Interface Design", "Engineering", "User Experience", "Iteration & Impact"]
    fs = min(fit("mono", s, 18.5, 1106 - nx - 31) for s in focus)
    for i, s in enumerate(focus):
        y = 192 + i * 38
        col.append(rect(nx, y - cap("mono", fs) / 2 - 7, 14, 14, C["pink"]))
        col.append(text("mono", s, nx + 31, y, fs, C["ink"]))
    sc.add("".join(col), nx - 6, 1110, 0, 350)

    # currently building panel
    x0, y0, x1, y1, cut = 1128, 26, W - MARGIN, 418, 30
    sc.add(poly([(x0, y0), (x1 - cut, y0), (x1, y0 + cut), (x1, y1), (x0, y1)], C["dark"]))
    tsz = fit("display", "CURRENTLY BUILDING", 20, x1 - cut - 8 - (x0 + 58), 0.02)
    sc.add(rect(x0 + 26, 70 - 17, 17, 17, C["lime"])
           + text("display", "CURRENTLY BUILDING", x0 + 58, 70, tsz, WHITE, ls=0.02), x0, x1, 0, 80)
    for i, p in enumerate(PROJECTS):
        iy = 100 + i * 106
        item = [project_logo(p["key"], x0 + 24, iy + 8, 54),
                text("bold", p["name"], x0 + 96, iy + 28, 21, WHITE, ls=-0.01),
                icon("arrow_up_right", x1 - 40, iy + 10, 24, WHITE, 2.2)]
        for j, s in enumerate(p["short"]):
            item.append(text("body", s, x0 + 96, iy + 53 + j * 21, 15.5, SOFT_WHITE))
        if i < len(PROJECTS) - 1:
            item.append(line(x0 + 96, iy + 96, x1 - 18, iy + 96, "#3A3A3A", 1.2))
        sc.add("".join(item), x0, x1, iy, iy + 98)

    # SELECTED WORK heading
    ty = 440
    sc.add(line(MARGIN, ty + 10, W - MARGIN, ty + 10, C["ink"], 1.5), y0=ty)
    sc.add(section_title(MARGIN, ty + 60, "SELECTED WORK"), 0, 600, ty)
    label, size = "VIEW ALL PROJECTS", 16.5
    ax = W - MARGIN - 20
    vx = ax - 8 - tw("semi", label, size, 0.02)
    sc.add(text("semi", label, vx, ty + 60, size, C["ink"], ls=0.02)
           + icon("arrow_up_right", ax, ty + 44, 20, C["ink"], 2.4), vx - 5, W, ty)
    cut_y, cut_x = h - 120, vx - 24
    assert cut_y - 0 >= MIN_STRIP and h - cut_y >= MIN_STRIP
    return sc, [("hero.svg", 0, W, 0, cut_y, None, HERO_ALT)], [
        ("work-title.svg", 0, cut_x, cut_y, h, None, "Selected work"),
        ("work-all.svg", cut_x, W, cut_y, h, LINKS["repos"], "View all projects")]


def phone(sc, x, y, angle):
    sc.defs.append('<linearGradient id="omniImg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2C6FF"/>'
                   '<stop offset="1" stop-color="#9C78EC"/></linearGradient>')
    o = [f'<g transform="translate({fmt(x)} {fmt(y)}) rotate({angle} 94 170)">']
    o.append(rect(0, 0, 188, 340, "#232326", rx=32, stroke="#55555B", sw=1.4))
    o.append(rect(7, 7, 174, 326, "#0A0A0B", rx=26))
    o.append(rect(66, 16, 56, 16, "#000", rx=8))
    o.append(text("semi", "9:41", 22, 30, 12.5, WHITE))
    for i, hh in enumerate((4, 6, 8, 10)):
        o.append(rect(122 + i * 4, 29 - hh, 2.6, hh, WHITE, rx=0.6))
    o.append('<path d="M141 22.5a9 9 0 0 1 12 0M143.5 25.5a5 5 0 0 1 7 0" fill="none" stroke="#FFF" stroke-width="1.6" stroke-linecap="round"/>'
             '<circle cx="147.5" cy="28" r="1.4" fill="#FFF"/>')
    o.append(rect(157, 21, 17, 9, "none", rx=2.5, stroke=WHITE, sw=1.2) + rect(158.8, 22.8, 11.5, 5.4, WHITE, rx=1))
    sk = ' transform="translate(22 96) skewX(-10) translate(-22 -96)"'
    o.append(f'<g{sk}>' + text("bold", "Good Morning,", 22, 96, 15, WHITE) + '</g>')
    sk = ' transform="translate(22 122) skewX(-10) translate(-22 -122)"'
    o.append(f'<g{sk}>' + text("display", "Student", 22, 122, 19.5, WHITE) + '</g>')
    sw_ = tw("display", "Student", 19.5)
    o.append(f'<path transform="translate({fmt(sw_ - 74)} 6)" d="M108 105c2-6 7-6 8-1l2-7c1-3 5-2 4 1l-1 5 3-8c1-3 5-2 4 1'
             'l-3 9 3-5c2-2 5 0 3 3l-5 9c-3 5-9 6-13 3z" fill="#FFC83D"/>')
    for yy in (82, 106):
        o.append(rect(150, yy, 16, 16, "none", rx=4, stroke="#45D483", sw=1.4) + rect(155, yy + 5, 6, 6, "#45D483", rx=1))
    o.append(rect(18, 146, 152, 190, "url(#omniImg)", rx=14))
    o.append(poly([(26, 336), (26, 236), (46, 222), (46, 206), (58, 198), (70, 206), (70, 222), (90, 236), (90, 336)], "#7B57C8", ' opacity=".75"'))
    o.append(poly([(98, 336), (98, 226), (130, 200), (162, 226), (162, 336)], "#6C49BC", ' opacity=".7"'))
    for i in range(3):
        for j in range(4):
            o.append(rect(34 + i * 18, 246 + j * 22, 8, 10, "#E9D9FF", extra=' opacity=".55"'))
    o.append('</g>')
    return "".join(o)


def ranking(x, y, angle):
    o = [f'<g transform="translate({fmt(x)} {fmt(y)}) rotate({angle} 100 100)">']
    o.append(rect(0, 0, 200, 210, "#141414", rx=14, stroke="#2E2E2E", sw=1.4))
    o.append(text("semi", "Section Ranking", 16, 34, 15, WHITE))
    rows = [("A1", 0.92, "#3CCB3C", "9.2", "#A8F25A"), ("B2", 0.72, "#F2D52E", "7.8", "#F6E7B8"),
            ("C1", 0.5, "#F6C9A0", "6.1", "#F7D3DD")]
    for i, (lab, frac, col, val, vcol) in enumerate(rows):
        yy = 72 + i * 38
        o.append(rect(9, yy - 17, 182, 32, "#1A1A1A", rx=8))
        o.append(text("semi", lab, 18, yy + 5, 14, WHITE))
        o.append(rect(50, yy - 4, 96, 9, "#2C2C2C", rx=4.5) + rect(50, yy - 4, 96 * frac, 9, col, rx=4.5))
        o.append(text("semi", val, 182, yy + 5, 14, vcol, anchor="end"))
    o.append('</g>')
    return "".join(o)


def terminal(x, y, angle):
    o = [f'<g transform="translate({fmt(x)} {fmt(y)}) rotate({angle} 110 100)">']
    o.append(rect(0, 0, 230, 210, "#111111", rx=14, stroke="#3E3E3E", sw=1.4))
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        o.append(f'<circle cx="{24 + i * 21}" cy="25" r="6.5" fill="{col}"/>')
    sz = 12.5
    lines = [[("> dig +trace ", "#F2F2F2"), ("kiit.ac.in", "#D9A9FF")],
             [(";;  <<>> root", "#E0E0E0")], [(";;  <<>> .in", "#E0E0E0")], [(";;  <<>> kiit.ac.in", "#E0E0E0")]]
    for i, parts in enumerate(lines):
        yy = 70 + i * 28 + (8 if i else 0)
        xx = 16
        seg = []
        for s, col in parts:
            seg.append(text("mono", s, xx, yy, sz, col))
            xx += tw("mono", s, sz)
        o.append(f'<g transform="translate(20 {yy}) skewX(-8) translate(-20 {-yy})">' + "".join(seg) + '</g>')
    o.append('</g>')
    return "".join(o)


def row_cards():
    h = 232
    sc = Scene(h)
    sc.add(poster_bg(W, h))
    sc.defs.append(RING_GRAD)
    gap, y, chh = 16, 4, 212
    cw = (W - 2 * MARGIN - 2 * gap) / 3
    slices = []
    for i, p in enumerate(PROJECTS):
        x = MARGIN + i * (cw + gap)
        cid = f"card{i}"
        sc.defs.append(f'<clipPath id="{cid}">{rect(x, y, cw, chh, rx=14)}</clipPath>')
        g = [f'<g clip-path="url(#{cid})">', rect(x, y, cw, chh, C["dark"])]
        if p["key"] == "omni":
            g.append(poly([(x + 0.7 * cw, y), (x + cw, y), (x + cw, y + chh), (x + 0.57 * cw, y + chh)], C["pink"]))
            g.append(poly([(x + 0.52 * cw, y + chh), (x + 0.62 * cw, y + 0.68 * chh), (x + 0.7 * cw, y + chh)], C["lav_card"]))
            g.append(phone(sc, x + 0.61 * cw, y + 24, -9))
        elif p["key"] == "smartschedule":
            g.append(poly([(x + 0.66 * cw, y), (x + cw, y), (x + cw, y + chh), (x + 0.52 * cw, y + chh)], C["lime"]))
            g.append(ranking(x + 0.565 * cw, y + 58, -5))
        else:
            g.append(poly([(x + 0.76 * cw, y), (x + cw, y), (x + cw, y + 0.42 * chh)], C["lav_card"]))
            g.append(poly([(x + 0.5 * cw, y + chh), (x + 0.66 * cw, y + 0.6 * chh), (x + 0.64 * cw, y + chh)], C["lav_card"]))
            g.append(terminal(x + 0.565 * cw, y + 44, -4))
        g.append('</g>')
        g.append(project_logo(p["key"], x + 22, y + 22, 46))
        g.append(text("bold", p["name"], x + 82, y + 52, 24, WHITE, ls=-0.015))
        for j, s in enumerate(p["long"]):
            g.append(text("body", s, x + 82, y + 82 + j * 21, 16, SOFT_WHITE))
        g.append(rect(x + 24, y + chh - 66, 46, 42, "none", rx=8, stroke="#E6E6E6", sw=1.5))
        g.append(icon("arrow_up_right", x + 35, y + chh - 57, 24, WHITE, 2.2))
        sc.add("".join(g), x - 1, x + cw + 1)
        x0 = 0 if i == 0 else x - gap / 2
        x1 = W if i == 2 else x + cw + gap / 2
        slices.append((p["file"], x0, x1, LINKS[p["key"]], f'{p["name"]} — {" ".join(p["long"])}'))
    return sc, slices


def row_approach_toolkit():
    h = 262
    sc = Scene(h)
    sc.add(poster_bg(W, h))
    sc.add(line(MARGIN, 10, W - MARGIN, 10, C["ink"], 1.5))
    sc.add(section_title(MARGIN, 62, "MY APPROACH"))
    steps = [("Discover", ["Understand", "the problem"], "lightbulb", C["pink_soft"]),
             ("Design", ["Explore &", "shape solutions"], "pencil", C["pink_soft"]),
             ("Build", ["Turn ideas", "into reality"], "code", C["lav"]),
             ("Iterate", ["Improve with", "real feedback"], "refresh", C["lime_soft"])]
    tw_, th, ty, x, step = 118, 76, 86, 64, 168
    for i, (title, desc, ic, col) in enumerate(steps):
        tx = x + i * step
        cx = tx + tw_ / 2
        sc.add(rect(tx, ty, tw_, th, col, rx=14))
        sc.add(icon(ic, cx - 17, ty + th / 2 - 17, 34, C["ink"], 2.2))
        sc.add(text("monob", title, cx, ty + th + 36, 18.5, C["ink"], anchor="middle"))
        for j, s in enumerate(desc):
            sc.add(text("body", s, cx, ty + th + 62 + j * 21, 16, C["text"], anchor="middle"))
        if i < len(steps) - 1:
            sc.add(icon("arrow_right", tx + tw_ + (step - tw_) / 2 - 15, ty + th / 2 - 15, 30, C["ink"], 2))
    sc.add(line(732, 30, 732, 250, C["ink"], 1.5))
    sc.add(section_title(760, 62, "TOOLKIT"))
    gx0, gx1, g, rh = 760, W - MARGIN, 8, 76
    cw = (gx1 - gx0 - g * (len(TOOLKIT[0]) - 1)) / len(TOOLKIT[0])
    ls = min(fit("semi", label, 15, cw - 10) for row in TOOLKIT for label, _ in row)
    for r, row in enumerate(TOOLKIT):
        ry = ty + r * (rh + 10)
        for i, (label, key) in enumerate(row):
            tx = gx0 + i * (cw + g)
            sc.add(rect(tx + 0.75, ry + 0.75, cw - 1.5, rh - 1.5, C["tile"], rx=10, stroke=C["tile_line"], sw=1.5))
            if key == "sql":
                sc.add(icon("database", tx + cw / 2 - 15, ry + 11, 30, C["ink"], 2))
            else:
                sc.add(brand_icon(key, tx + cw / 2 - 16, ry + 10, 32))
            sc.add(text("semi", label, tx + cw / 2, ry + 63, ls, C["text"], anchor="middle"))
    return sc


def row_footer():
    h = 162
    sc = Scene(h)
    sc.add(poster_bg(W, h, bottom=True))
    x0, y0, x1, y1 = MARGIN, 14, W - MARGIN, 124
    sc.defs.append(f'<clipPath id="bar">{rect(x0, y0, x1 - x0, y1 - y0, rx=14)}</clipPath>')
    sc.add(rect(x0, y0, x1 - x0, y1 - y0, C["dark"], rx=14))
    fs, ls = 30, -0.025
    lx = 84
    sc.add(text("display", "Let’s build", lx, 60, fs, WHITE, ls=ls), 0, 400)
    w_some = tw("display", "something ", fs, ls)
    w_cool = tw("display", "cool.", fs, ls)
    chh = cap("display", fs)
    sc.add(text("display", "something", lx, 98, fs, WHITE, ls=ls), 0, 400)
    sc.add(rect(lx + w_some - 4, 98 - chh - 7, w_cool + 10, chh + 15, C["pink"], rx=3), 0, 400)
    sc.add(text("display", "cool.", lx + w_some + 1, 98, fs, C["ink"], ls=ls), 0, 400)
    dx = lx + max(tw("display", "Let’s build", fs, ls), w_some + w_cool + 6) + 40
    sc.add(line(dx, 40, dx, 100, "#5E5E5E", 1.5), 0, dx + 2)
    tx = dx + 34
    body = ["Open to collaborations, product ideas,", "and internship opportunities."]
    text_end = tx + max(tw("body", s, 17) for s in body)
    for i, s in enumerate(body):
        sc.add(text("body", s, tx, 64 + i * 25, 17, "#DADADA"), tx - 1, text_end + 1)

    cell = 15
    cxk = x1 - 5 * cell
    sc.add(f'<g clip-path="url(#bar)">{checker(cxk, y1 - 5 * cell, cell, 5, [C["pink"]])}</g>', cxk - 1, W)

    buttons = [("Email", "mail", "email"), ("LinkedIn", "in", "linkedin"), ("Portfolio", "external", "portfolio"),
               ("GitHub", "gh", "github")]
    bs, bh, pad, isz, gap = 18, 52, 22, 22, 16

    def bw(label, ic):
        iw = tw("display", "in", 22) if ic == "in" else isz
        return pad + iw + 10 + tw("semi", label, bs) + pad

    total = sum(bw(l, i) for l, i, _ in buttons) + gap * (len(buttons) - 1)
    bx = cxk - 26 - total
    assert bx > text_end + 24, "footer buttons overlap the text"
    by = (y0 + y1) / 2 - bh / 2
    edges = []
    for label, ic, key in buttons:
        w = bw(label, ic)
        o = rect(bx + 0.75, by + 0.75, w - 1.5, bh - 1.5, "none", rx=10, stroke="#EDEDED", sw=1.5)
        iy = by + (bh - isz) / 2
        if ic == "in":
            o += text("display", "in", bx + pad, by + bh / 2 + cap("display", 22) / 2 + 1, 22, WHITE)
            iw = tw("display", "in", 22)
        elif ic == "gh":
            o += github_mark(bx + pad, iy, isz, WHITE)
            iw = isz
        else:
            o += icon(ic, bx + pad, iy, isz, WHITE, 1.8)
            iw = isz
        o += text("semi", label, bx + pad + iw + 10, by + bh / 2 + cap("semi", bs) / 2, bs, WHITE)
        sc.add(o, bx - 2, bx + w + 2)
        edges.append((key, label, bx, bx + w))
        bx += w + gap
    slices = [("footer-start.svg", 0, edges[0][2] - gap / 2, None,
               "Let’s build something cool. Open to collaborations, product ideas, and internship opportunities.")]
    for i, (key, label, a, b) in enumerate(edges):
        right = edges[i + 1][2] - gap / 2 if i + 1 < len(edges) else b + gap / 2
        slices.append((f"footer-{key}.svg", a - gap / 2, right, LINKS[key], label))
    slices.append(("footer-end.svg", edges[-1][3] + gap / 2, W, None, ""))
    return sc, slices


# ------------------------------------------------------------------ output

def img_tag(src, x0, x1, alt, href=None):
    pct = (x1 - x0) / W * 99.9
    url = src if src.startswith("http") else f"assets/{src}"
    tag = f'<img src="{url}" width="{pct:.4f}%" align="top" alt="{esc(alt)}">'
    return f'<a href="{href}">{tag}</a>' if href else tag


def emit_slices(sc, slices):
    """Write each slice. A slice is (file, x0, x1, href, alt) or (file, x0, x1, y0, y1, href, alt)."""
    tags = []
    for s in slices:
        name, x0, x1, y0, y1, href, alt = s if len(s) == 7 else (s[0], s[1], s[2], 0, sc.h, s[3], s[4])
        assert y1 - y0 >= MIN_STRIP, f"{name} is too short to stack without gaps"
        write(name, sc.svg(x0, x1, alt or "decoration", y0, y1))
        tags.append(img_tag(name, x0, x1, alt, href))
    return "".join(tags)


def emit_full(sc, name, alt, href=None):
    return emit_slices(sc, [(name, 0, W, href, alt)])


def main():
    hero, hero_top, hero_bottom = row_hero()
    rows = []
    rows.append(emit_slices(*row_nav()))
    rows.append('<a id="about"></a>' + emit_slices(hero, hero_top))
    rows.append('<a id="projects"></a>' + emit_slices(hero, hero_bottom))
    rows.append(emit_slices(*row_cards()))
    rows.append('<a id="toolkit"></a>' + emit_full(row_approach_toolkit(), "approach-toolkit.svg",
                "My approach: discover, design, build, iterate. Toolkit: "
                + ", ".join(label for row in TOOLKIT for label, _ in row) + "."))
    rows.append('<a id="now"></a>' + img_tag(STATS_URL, 0, W,
                "GitHub stats, live contribution graph, and what I'm exploring now: ML / AI, Data Science, App Dev.", GH))
    rows.append('<a id="connect"></a>' + emit_slices(*row_footer()))

    readme = ("<!-- The poster below is generated. Edit .github/scripts/build_assets.py and run it to change it. -->\n\n"
              '<div align="center">\n' + "<br>\n".join(rows) + "\n</div>\n")
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)
    print("wrote README.md and", len(os.listdir(ASSETS)), "files in assets/")


if __name__ == "__main__":
    main()
