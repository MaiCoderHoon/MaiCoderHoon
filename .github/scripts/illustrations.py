"""The two big illustrations in the profile README, drawn with flat shapes and ink outlines.

workspace()  hero: a developer coding at a desk by a sunset window
campus()     footer: a quiet, KIIT-inspired campus postcard

Both are self-contained SVG documents (no external fonts or images). The only text
is decorative handwriting/signage drawn as outlines; README.md carries the real copy.
"""
import math

from svgkit import TWINKLE, C, doc, fmt, m_mark, path, rect, text

INK, PINK, LIME, CREAM, WHITE = C["ink"], C["pink"], C["lime"], C["cream"], C["white"]
SKIN, SKIN_SHADE = "#F2C6A2", "#DFA882"
HOODIE, HOODIE_LIGHT = "#2B2A33", "#3B3A46"
WOOD, WOOD_EDGE = "#F1CB9C", "#DDA772"
LEAF, LEAF_DARK, LEAF_LIGHT = "#5DB86A", "#3C9752", "#B5EE63"


def circle(cx, cy, r, fill, stroke=None, sw=2.5, extra=""):
    st = f' stroke="{stroke}" stroke-width="{fmt(sw)}"' if stroke else ""
    return f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{fill}"{st}{extra}/>'


def leaf(x, y, angle, length, fill):
    """A pointed leaf with its stem at (x, y), pointing along `angle` degrees."""
    L = length
    d = (f"M0 0 C {fmt(L * .28)} {fmt(-L * .42)}, {fmt(L * .78)} {fmt(-L * .36)}, {fmt(L)} 0 "
         f"C {fmt(L * .78)} {fmt(L * .36)}, {fmt(L * .28)} {fmt(L * .42)}, 0 0 Z")
    return (f'<g transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(angle)})">'
            + path(d, fill=fill, stroke=INK, sw=2)
            + path(f"M{fmt(L * .12)} 0 L{fmt(L * .7)} 0", stroke=INK, sw=1.2, extra=' opacity=".45"')
            + '</g>')


def vine(points, angle0, every=0.16, size=22):
    """Leaves alternating along a quadratic/cubic-ish polyline of points."""
    out = [f'<path d="M{" L".join(f"{fmt(x)} {fmt(y)}" for x, y in points)}" fill="none" stroke="{LEAF_DARK}" '
           f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>']
    segs = list(zip(points, points[1:]))
    total = sum(math.dist(a, b) for a, b in segs)
    t, side, i = total * every, 1, 0
    walked = 0
    for a, b in segs:
        seg = math.dist(a, b)
        while t <= walked + seg:
            f = (t - walked) / seg
            x, y = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            heading = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            col = [LEAF, LEAF_LIGHT, LEAF_DARK][i % 3]
            out.append(leaf(x, y, heading + side * 62 + angle0, size * (0.85 + 0.15 * (i % 2)), col))
            side, i, t = -side, i + 1, t + total * every
        walked += seg
    return "".join(out)


def check(x, y, s=1.0, sw=2.6):
    return path(f"M{fmt(x)} {fmt(y)} l{fmt(5 * s)} {fmt(5 * s)} l{fmt(10 * s)} {fmt(-12 * s)}", stroke=INK, sw=sw)


# ------------------------------------------------------------------ hero

WS_W, WS_H = 600, 520
BLOB = ("M78 16 C 210 6, 410 8, 530 18 C 574 22, 590 50, 588 100 L 586 410 C 584 470, 554 502, 494 504 "
        "L 110 506 C 52 506, 16 476, 14 418 L 12 108 C 12 52, 30 20, 78 16 Z")


def window():
    x0, y0, x1, y1 = 296, 34, 576, 300
    px0, py0, px1, py1 = x0 + 10, y0 + 10, x1 - 10, y1 - 10
    sky = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="#B7A2F4"/><stop offset=".42" stop-color="#E3A5E2"/>'
           f'<stop offset=".72" stop-color="#FDB4D0"/><stop offset="1" stop-color="#FFD9B6"/></linearGradient>'
           f'<clipPath id="panes"><rect x="{px0}" y="{py0}" width="{px1 - px0}" height="{py1 - py0}"/></clipPath>')
    city = []
    back = [(306, 30, 118), (334, 24, 92), (356, 34, 132), (392, 28, 84), (418, 40, 112), (456, 26, 96),
            (480, 36, 128), (514, 30, 100), (542, 30, 120)]
    for x, w, top in back:
        city.append(rect(x, top, w, 300 - top, "#C2A3F0"))
        city.append(rect(x + w / 2 - 1, top - 10, 2, 10, "#C2A3F0"))
    front = [(306, 38, 150), (350, 30, 124), (386, 44, 164), (436, 34, 112), (476, 40, 150), (522, 46, 134)]
    for j, (x, w, top) in enumerate(front):
        city.append(rect(x, top, w, 300 - top, "#8F6DD8"))
        for r in range(int((290 - top - 14) // 16)):
            for c in range(int((w - 8) // 11)):
                if (r * 3 + c + j) % 4:
                    city.append(rect(x + 6 + c * 11, top + 10 + r * 16, 5, 7, "#FFE3A0",
                                     extra=' opacity=".95"' if (r + c) % 3 else ' opacity=".5"'))
    glass = ('<g clip-path="url(#panes)">'
             + rect(px0, py0, px1 - px0, py1 - py0, "url(#sky)")
             + circle(498, 122, 44, "#FFE7CF", extra=' opacity=".45"')
             + circle(498, 122, 30, "#FFEBD6")
             + rect(326, 62, 70, 9, WHITE, rx=4.5, extra=' opacity=".5"')
             + rect(348, 76, 46, 7, WHITE, rx=3.5, extra=' opacity=".4"')
             + rect(452, 56, 58, 8, WHITE, rx=4, extra=' opacity=".45"')
             + "".join(city)
             + '</g>')
    frame = (path(f"M{x0} {y0}H{x1}V{y1}H{x0}Z M{px0} {py0}V{py1}H{px1}V{py0}Z", fill="#2E2739",
                  extra=' fill-rule="evenodd"')
             + rect(433, py0, 8, py1 - py0, "#2E2739")
             + rect(px0, 160, px1 - px0, 8, "#2E2739")
             + rect(x0, y0, x1 - x0, y1 - y0, "none", stroke=INK, sw=3)
             + rect(x0 - 10, y1 - 4, x1 - x0 + 20, 12, "#2E2739", rx=3, stroke=INK, sw=2.5))
    return sky, glass + frame


def shelf():
    books = [(28, 14, 54, PINK), (43, 12, 46, INK), (56, 17, 58, C["lav"]), (74, 11, 42, LIME),
             (86, 15, 50, C["pink_soft"])]
    out = []
    for x, w, h, col in books:
        out.append(rect(x, 300 - h, w, h, col, rx=2, stroke=INK, sw=2.2))
        out.append(rect(x + 3, 300 - h + 8, w - 6, 3, WHITE if col == INK else INK, rx=1.5, extra=' opacity=".35"'))
    # a leaning book and a tiny cactus pot
    out.append(f'<g transform="rotate(18 112 300)">{rect(104, 256, 13, 44, C["lav_deep"], rx=2, stroke=INK, sw=2.2)}</g>')
    out.append(path("M140 300 l-4 -22 h28 l-4 22 Z", fill=WHITE, stroke=INK, sw=2.2))
    out.append(rect(134, 276, 32, 6, PINK, rx=2, stroke=INK, sw=2))
    out.append(path("M150 276 C 146 262, 146 252, 150 246 C 154 252, 154 262, 150 276 Z", fill=LEAF, stroke=INK, sw=2))
    out.append(path("M144 268 C 138 262, 138 256, 141 252 M156 268 C 162 262, 162 256, 159 252", stroke=LEAF_DARK, sw=3))
    out.append(rect(18, 300, 162, 10, WOOD, rx=3, stroke=INK, sw=2.4))
    out.append(path("M36 310 l0 14 l14 -14 M150 310 l0 14 l14 -14", stroke=INK, sw=2.4))
    return "".join(out)


def hanging_plant():
    strings = path("M95 0 L76 70 M95 0 L114 70", stroke=INK, sw=1.8)
    pot = (path("M70 70 H120 L113 104 H77 Z", fill=PINK, stroke=INK, sw=2.5)
           + rect(66, 66, 58, 9, C["pink_soft"], rx=3, stroke=INK, sw=2.5))
    vines = (vine([(78, 100), (64, 140), (52, 190), (44, 240), (42, 280)], 0)
             + vine([(92, 104), (92, 150), (100, 196), (96, 232)], 0, every=.2, size=20)
             + vine([(110, 100), (118, 126)], 0, every=.5, size=18))
    top = "".join(leaf(95 + dx, 68, a, 22, col) for dx, a, col in
                  ((-14, -150, LEAF), (-4, -115, LEAF_DARK), (8, -70, LEAF_LIGHT), (16, -30, LEAF)))
    return strings + top + pot + vines


def checklist():
    items = ["Design", "Build", "Iterate", "Ship"]
    x, y, w, h = 126, 100, 100, 118
    lines = []
    for i, item in enumerate(items):
        by = y + 38 + i * 22
        lines.append(check(x + 12, by - 9, 0.8, 2.4))
        lines.append(text("hand", item, x + 32, by, 22, INK))
    lines.append(path(f"M{x + 32} {y + 38 + 3 * 22 + 5} q 22 5 44 -1", stroke=PINK, sw=3))
    return (f'<g transform="rotate(-5 {x + w / 2} {y + h / 2})">'
            + rect(x + 3, y + 5, w, h, INK, rx=3, extra=' opacity=".12"')
            + rect(x, y, w, h, "#FFFDF7", rx=3, stroke=INK, sw=2.4)
            + "".join(lines)
            + circle(x + w / 2, y + 8, 6, PINK, stroke=INK, sw=2.2)
            + '</g>')


def wall_bits():
    clip, mark = m_mark(250, 70, 34, uid="wallm")
    frame = rect(214, 44, 72, 52, INK, rx=6, stroke=INK, sw=2.5) + rect(219, 49, 62, 42, "#1A1A1F", rx=3) + mark
    stickies = (f'<g transform="rotate(-6 276 118)">{rect(262, 104, 28, 28, C["pink_soft"], rx=2, stroke=INK, sw=2.2)}'
                f'{path("M268 114 h15 M268 121 h10", stroke=INK, sw=2)}</g>')
    return clip, frame + stickies


def monitor_sticky():
    return (f'<g transform="rotate(8 506 184)">{rect(492, 170, 28, 28, LIME, rx=2, stroke=INK, sw=2.2)}'
            f'{path("M498 180 h14 M498 187 h9", stroke=INK, sw=2)}</g>')


def monitor():
    out = [rect(314, 186, 202, 136, "#1C1B22", rx=10, stroke=INK, sw=3),
           rect(322, 194, 186, 116, "#141319", rx=5)]
    out += [circle(331 + i * 8, 201, 2.4, col) for i, col in enumerate((PINK, LIME, "#EDEAF4"))]
    rows = [(0, [(18, PINK), (42, "#EDEAF4")]), (8, [(26, LIME), (30, C["lav"])]),
            (8, [(14, "#9E9AAB"), (34, PINK)]), (16, [(30, C["lav"]), (12, LIME)]),
            (8, [(22, "#9E9AAB")]), (0, [(10, PINK)]), (0, [(28, LIME), (20, "#EDEAF4")]),
            (8, [(34, C["lav"])])]
    y = 212
    for indent, segs in rows:
        x = 330 + indent
        for w, col in segs:
            out.append(rect(x, y, w, 5, col, rx=2.5))
            x += w + 5
        y += 11
    out.append(rect(x - 1, y - 14, 5, 9, LIME, extra=' class="cursor"'))
    # dashboard panel: a rising pink line over lime bars
    out.append(rect(440, 210, 60, 54, "#25232E", rx=4))
    out.append(path("M446 252 L456 243 L464 247 L476 231 L493 220 V258 H446 Z", fill=PINK, extra=' opacity=".25"'))
    out.append(path("M446 252 L456 243 L464 247 L476 231 L493 220", stroke=PINK, sw=2.4))
    out.append(rect(440, 270, 60, 32, "#25232E", rx=4))
    out += [rect(447 + i * 12, 296 - h, 7, h, LIME, rx=1.5) for i, h in enumerate((10, 16, 12, 20))]
    # stand
    out.append(rect(404, 322, 22, 24, "#2A2833", stroke=INK, sw=2.5))
    out.append(rect(378, 342, 74, 12, "#2A2833", rx=6, stroke=INK, sw=2.5))
    return "".join(out)


def desk():
    return (rect(-4, 352, 608, 18, WOOD, stroke=INK, sw=2.8)
            + rect(-4, 370, 608, 24, WOOD_EDGE, stroke=INK, sw=2.8)
            + rect(-4, 394, 608, 130, "#EBC6DE")
            + rect(-4, 394, 608, 18, INK, extra=' opacity=".08"'))


def lamp():
    glow = ('<linearGradient id="glow" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FFF3C4" stop-opacity=".85"/>'
            '<stop offset="1" stop-color="#FFF3C4" stop-opacity="0"/></linearGradient>')
    body = (path("M512 244 L470 352 H566 L540 236 Z", fill="url(#glow)")
            + path("M556 348 L568 268 L534 232", stroke=INK, sw=6)
            + circle(568, 268, 5, PINK, stroke=INK, sw=2)
            + path("M510 238 C 512 222, 530 212, 546 220 L 540 236 Z", fill=INK, stroke=INK, sw=2.5,
                   extra=' transform="rotate(-8 530 230)"')
            + rect(536, 344, 40, 10, INK, rx=5))
    return glow, body


def mug():
    steam = (path("M488 318 c -6 -8 6 -12 0 -20 c -5 -7 5 -10 1 -16", stroke="#8E8696", sw=2.4,
                  extra=' class="steam s1"')
             + path("M500 318 c -6 -8 6 -12 0 -20 c -5 -7 5 -10 1 -16", stroke="#8E8696", sw=2.4,
                    extra=' class="steam s2"'))
    return (steam
            + path("M507 332 c 12 0 12 16 0 16", stroke=INK, sw=3)
            + rect(482, 324, 26, 30, WHITE, rx=5, stroke=INK, sw=2.6)
            + rect(482, 334, 26, 7, PINK, extra=' opacity=".95"')
            + rect(482, 324, 26, 30, "none", rx=5, stroke=INK, sw=2.6))


def desk_plant():
    leaves = "".join(leaf(58, 322, a, l, col) for a, l, col in
                     ((-150, 30, LEAF), (-118, 34, LEAF_DARK), (-82, 36, LEAF_LIGHT), (-52, 32, LEAF), (-24, 26, LEAF_DARK)))
    return leaves + path("M40 322 H76 L71 354 H45 Z", fill=LIME, stroke=INK, sw=2.5)


def keyboard():
    keys = "".join(rect(346 + c * 9.6, 349 + r * 5, 7, 3, "#B9B2C9", rx=1) for r in range(2) for c in range(12))
    return (path("M338 356 L344 346 H468 L474 356 Z", fill="#E9E4F2", stroke=INK, sw=2.4) + keys)


def person():
    out = []
    # torso / hoodie
    out.append(path("M168 530 L170 372 C 170 330, 194 306, 232 300 L 290 298 C 326 300, 350 322, 352 360 L 356 530 Z",
                    fill=HOODIE, stroke=INK, sw=3))
    out.append(path("M190 340 C 196 320, 214 310, 236 306", stroke=HOODIE_LIGHT, sw=7, extra=' opacity=".9"'))
    out.append(path("M262 318 L264 400", stroke=INK, sw=2, extra=' opacity=".35"'))
    # hood bunched on the shoulders
    out.append(path("M206 306 C 200 280, 224 262, 258 262 C 292 262, 314 282, 308 308 C 290 320, 224 320, 206 306 Z",
                    fill=HOODIE_LIGHT, stroke=INK, sw=2.6))
    out.append(path("M222 304 C 236 290, 280 290, 294 304", stroke=INK, sw=2, extra=' opacity=".5"'))
    # neck
    out.append(rect(246, 262, 26, 26, SKIN_SHADE, rx=8, stroke=INK, sw=2.4))
    # head: face (seen from behind, turned toward the screen), ear, hair, glasses
    out.append(path("M226 230 C 226 200, 246 186, 266 186 C 292 186, 306 206, 306 230 C 306 238, 304 244, 302 250 "
                    "C 300 262, 292 272, 278 276 C 254 282, 230 268, 226 246 Z", fill=SKIN, stroke=INK, sw=2.6))
    out.append(path("M220 250 C 208 226, 214 196, 238 184 L 234 172 L 250 180 L 252 166 L 264 178 L 274 166 "
                    "L 280 180 L 294 174 L 292 190 C 304 198, 310 212, 306 224 C 298 216, 288 212, 280 216 "
                    "C 276 228, 272 242, 266 254 C 256 270, 232 270, 220 250 Z", fill="#18171D", stroke=INK, sw=2.6))
    out.append(path("M240 196 C 248 190, 258 188, 266 190", stroke="#3A3946", sw=3))
    out.append(path("M262 242 C 256 236, 256 228, 264 226 C 272 226, 276 236, 272 246 C 270 252, 264 252, 262 248 Z",
                    fill=SKIN, stroke=INK, sw=2.4))
    out.append(path("M265 234 C 268 236, 268 242, 266 244", stroke=INK, sw=1.6))
    out.append(path("M272 232 L 300 226", stroke=INK, sw=2.6))
    out.append(rect(296, 218, 14, 18, "none", rx=5, stroke=INK, sw=2.6))
    out.append(path("M299 220 L303 224", stroke=WHITE, sw=1.5, extra=' opacity=".7"'))
    # arm propped on the desk, hand under the chin
    out.append(path("M314 356 C 316 330, 312 300, 300 282 L 322 270 C 338 292, 346 326, 344 356 Z",
                    fill=HOODIE, stroke=INK, sw=2.8))
    out.append(path("M298 286 C 290 278, 292 266, 302 262 C 312 258, 322 264, 322 274 C 322 284, 310 292, 298 286 Z",
                    fill=SKIN, stroke=INK, sw=2.4))
    out.append(path("M304 268 C 308 266, 314 268, 316 272 M302 275 C 306 273, 312 275, 314 279", stroke=INK, sw=1.6))
    # chair back with the brand mark
    clip, mark = m_mark(262, 456, 46, uid="chairm")
    out.append(path("M184 530 L184 418 C 184 396, 198 384, 222 384 L 302 384 C 326 384, 340 396, 340 418 L 340 530 Z",
                    fill="#24232B", stroke=INK, sw=3))
    out.append(path("M198 418 C 198 404, 206 396, 222 396", stroke="#44434F", sw=4))
    out.append(mark)
    return clip, "".join(out)


def sparkle(x, y, s, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({s})"><g{c}>'
            f'{path(TWINKLE, fill=LIME, stroke=INK, sw=2 / s)}</g></g>')


WS_STYLE = (
    "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
    ".cursor{animation:blink 1.1s steps(1) infinite}"
    "@keyframes rise{0%{transform:translateY(0);opacity:.9}100%{transform:translateY(-10px);opacity:0}}"
    ".steam{animation:rise 2.6s ease-in infinite}.s2{animation-delay:1.3s}"
    "@keyframes twinkle{0%,100%{transform:scale(1)}50%{transform:scale(.6)}}"
    ".tw{transform-box:fill-box;transform-origin:center;animation:twinkle 2.4s ease-in-out infinite}"
    ".tw2{animation-delay:1.2s}"
)


def workspace():
    sky_defs, win = window()
    wall_clip, bits = wall_bits()
    glow_defs, lamp_svg = lamp()
    person_clip, who = person()
    defs = (f'<clipPath id="blob"><path d="{BLOB}"/></clipPath>'
            '<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4D4EA"/>'
            '<stop offset="1" stop-color="#FBE6F1"/></linearGradient>'
            + sky_defs + wall_clip + glow_defs + person_clip)
    scene = (rect(0, 0, WS_W, WS_H, "url(#wall)")
             + win + shelf() + bits + checklist() + hanging_plant()
             + desk() + lamp_svg + monitor() + monitor_sticky() + keyboard() + mug() + desk_plant()
             + who)
    body = (path(BLOB, fill=CREAM, extra=' transform="translate(5 7)" opacity=".0"')
            + f'<g clip-path="url(#blob)">{scene}</g>'
            + path(BLOB, stroke=INK, sw=3.5)
            + sparkle(552, 2, 1.0, "tw") + sparkle(8, 448, 0.8, "tw tw2"))
    return doc(WS_W, WS_H, body, "Illustration: a developer in a black hoodie coding at a desk by a sunset window",
               defs=defs, style=WS_STYLE)


# ------------------------------------------------------------------ footer campus

CP_W, CP_H = 900, 300


def cloud(x, y, s, cls):
    bumps = [(0, 0, 22), (24, -12, 26), (52, -4, 22), (72, 6, 16), (-20, 8, 15)]
    outline = "".join(circle(x + dx * s, y + dy * s, r * s, INK, extra="") for dx, dy, r in bumps)
    fill = "".join(circle(x + dx * s, y + dy * s, r * s - 2.6, C["pink_soft"]) for dx, dy, r in bumps)
    base = rect(x - 30 * s, y + 4 * s, 112 * s, 20 * s, C["pink_soft"], rx=10 * s)
    base_line = path(f"M{fmt(x - 30 * s + 8)} {fmt(y + 24 * s - 1.3)} H{fmt(x + 82 * s - 8)}", stroke=INK, sw=2.6)
    return f'<g class="{cls}">{outline}{rect(x - 31 * s, y + 3 * s, 114 * s, 22 * s, INK, rx=11 * s)}{fill}{base}{base_line}</g>'


def tree(x, base, s, tone=0):
    greens = [("#7CC75A", "#5AAE45"), ("#8ED163", "#62B44C")][tone]
    blobs = [(0, -60, 30), (-22, -44, 24), (22, -42, 25), (0, -34, 22)]
    outline = "".join(circle(x + dx * s, base + dy * s, r * s + 2.6, INK) for dx, dy, r in blobs)
    fill = "".join(circle(x + dx * s, base + dy * s, r * s, greens[0]) for dx, dy, r in blobs)
    shade = circle(x + 10 * s, base - 38 * s, 16 * s, greens[1]) + circle(x - 14 * s, base - 50 * s, 6 * s, "#C8F27A")
    trunk = rect(x - 5 * s, base - 22 * s, 10 * s, 24 * s, "#9A6A44", rx=3, stroke=INK, sw=2.4)
    return trunk + outline + fill + shade


def building():
    out = []
    # wings
    for x in (296, 504):
        out.append(rect(x, 132, 100, 118, "#FFFDF8", stroke=INK, sw=3))
        out.append(rect(x - 6, 124, 112, 12, C["lav"], rx=3, stroke=INK, sw=2.6))
        for r in range(3):
            for c in range(3):
                lit = (r + c + x) % 4 == 0
                out.append(rect(x + 12 + c * 28, 148 + r * 32, 18, 22, C["pink_soft"] if lit else C["lav"],
                                rx=2, stroke=INK, sw=2))
                out.append(path(f"M{x + 21 + c * 28} {148 + r * 32} v22", stroke=INK, sw=1.4, extra=' opacity=".5"'))
    # tower
    out.append(rect(396, 70, 108, 180, "#FFFDF8", stroke=INK, sw=3))
    out.append(rect(388, 60, 124, 14, PINK, rx=3, stroke=INK, sw=2.6))
    out.append(path("M450 60 V30", stroke=INK, sw=2.4))
    out.append(path("M450 30 L474 37 L450 44 Z", fill=PINK, stroke=INK, sw=2.2, extra=' class="flag"'))
    out.append(rect(412, 84, 76, 30, INK, rx=5))
    out.append(text("display", "KIIT", 450, 107, 22, WHITE, anchor="middle", ls=0.06))
    for r in range(2):
        for c in range(3):
            out.append(rect(410 + c * 30, 126 + r * 30, 20, 20, C["lav"], rx=2, stroke=INK, sw=2))
    out.append(path("M428 250 V208 a22 22 0 0 1 44 0 V250 Z", fill=C["lav_deep"], stroke=INK, sw=2.6))
    out.append(path("M450 188 V250", stroke=INK, sw=2))
    out.append(rect(416, 248, 68, 6, "#F2E7DA", stroke=INK, sw=2))
    out.append(rect(408, 254, 84, 6, "#F2E7DA", stroke=INK, sw=2))
    return "".join(out)


CP_STYLE = (
    "@keyframes drift{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}"
    ".c1{animation:drift 9s ease-in-out infinite}.c2{animation:drift 11s ease-in-out infinite reverse}"
    "@keyframes wave{0%,100%{transform:skewY(0)}50%{transform:skewY(-8deg)}}"
    ".flag{transform-box:fill-box;transform-origin:left center;animation:wave 2s ease-in-out infinite}"
)


def campus():
    defs = f'<clipPath id="card"><rect x="0" y="0" width="{CP_W}" height="{CP_H}" rx="28"/></clipPath>'
    ground = (path("M0 252 C 200 236, 700 236, 900 252 V300 H0 Z", fill="#E4FF9E", stroke=INK, sw=3)
              + path("M412 300 C 420 278, 428 266, 420 258 H480 C 472 266, 480 278, 488 300 Z", fill="#F6DCC8",
                     stroke=INK, sw=2.6))
    trees = (tree(70, 262, 1.15) + tree(150, 256, 0.9, 1) + tree(236, 254, 1.05)
             + tree(664, 254, 1.05, 1) + tree(750, 256, 0.9) + tree(830, 262, 1.15, 1))
    bushes = "".join(circle(x, 254, r, LEAF, stroke=INK, sw=2.4) + circle(x - r / 3, 250, 3, PINK) + circle(x + r / 3, 252, 2.6, PINK)
                     for x, r in ((300, 12), (384, 10), (516, 10), (600, 12)))
    birds = path("M226 70 q 7 -7 14 0 q 7 -7 14 0 M262 52 q 5 -5 10 0 q 5 -5 10 0", stroke=INK, sw=2.4)
    checker = "".join(rect(c * 14, CP_H - (r + 1) * 14, 14.2, 14.2, PINK if (r + c) % 2 == 0 else C["pink_pale"])
                      for r in range(3) for c in range(3 - r))
    scene = (rect(0, 0, CP_W, CP_H, CREAM)
             + cloud(120, 74, 1.0, "c1") + cloud(700, 58, 0.85, "c2") + cloud(560, 112, 0.5, "c1")
             + birds + building() + ground + bushes + trees + checker)
    body = (f'<g clip-path="url(#card)">{scene}</g>'
            + rect(1.5, 1.5, CP_W - 3, CP_H - 3, "none", rx=27, stroke=INK, sw=3))
    return doc(CP_W, CP_H, body, "Illustration: a campus building with a KIIT sign, trees and pink clouds",
               defs=defs, style=CP_STYLE)
