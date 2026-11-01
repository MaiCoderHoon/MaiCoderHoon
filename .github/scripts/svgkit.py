"""Small SVG toolkit shared by build_assets.py and gen_stats.py (standard library only).

Text is drawn as vector outlines from glyphs.json, so the profile art renders the
same on every device without relying on fonts installed on the viewer's machine.
"""
import html
import json
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))

W = 1500          # width of every poster row, in SVG units
MARGIN = 48       # left/right content margin
RADIUS = 28       # poster corner radius (first and last row)

C = {
    "bg": "#FBF6F0",
    "ink": "#0E0E0E",
    "text": "#2B2B2B",
    "muted": "#5C5A55",
    "pink": "#FC80D6",
    "pink_soft": "#FDB6DE",
    "pink_pale": "#FED3EE",
    "lime": "#C9FB10",
    "lime_soft": "#DAFA62",
    "lav": "#DAC1FC",
    "lav_card": "#E3A9FC",
    "dark": "#0D0D0D",
    "dark2": "#171717",
    "tile": "#FFFDF9",
    "tile_line": "#D9D2C7",
}


def fmt(v):
    s = f"{v:.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    return "0" if s == "-0" else s


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- text

class Font:
    def __init__(self, data):
        self.upm = data["upm"]
        self.cap = data["cap"] / data["upm"]
        self.kern = data["kern"]
        self.glyphs = {}
        for ch, (adv, path) in data["glyphs"].items():
            cmds = [(m.group(1), [float(v) for v in m.group(2).split()])
                    for m in re.finditer(r"([MLQCZ])([^MLQCZ]*)", path)]
            self.glyphs[ch] = (adv, cmds)

    def _layout(self, s, size, ls):
        k = size / self.upm
        x, out = 0.0, []
        for i, ch in enumerate(s):
            g = self.glyphs.get(ch) or self.glyphs["?"]
            out.append((x, g))
            adv = g[0] + (self.kern.get(ch + s[i + 1], 0) if i + 1 < len(s) else 0)
            x += adv * k + ls * size
        return out, (x - ls * size if s else 0.0)

    def width(self, s, size, ls=0.0):
        return self._layout(s, size, ls)[1]

    def d(self, s, x, y, size, ls=0.0, anchor="start"):
        k = size / self.upm
        layout, w = self._layout(s, size, ls)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        parts = []
        for gx, (_, cmds) in layout:
            ox = x + gx
            for c, nums in cmds:
                if c == "Z":
                    parts.append("Z")
                    continue
                pts = " ".join(f"{fmt(ox + nums[j] * k)} {fmt(y - nums[j + 1] * k)}" for j in range(0, len(nums), 2))
                parts.append(c + pts)
        return "".join(parts)


_FONTS = {}


def font(style):
    if not _FONTS:
        with open(os.path.join(HERE, "glyphs.json"), encoding="utf-8") as f:
            for name, data in json.load(f)["styles"].items():
                _FONTS[name] = Font(data)
    return _FONTS[style]


def text(style, s, x, y, size, fill, anchor="start", ls=0.0, extra=""):
    """Text as a filled outline path. (x, y) is the baseline origin."""
    d = font(style).d(s, x, y, size, ls, anchor)
    return f'<path d="{d}" fill="{fill}"{extra}/>' if d else ""


def tw(style, s, size, ls=0.0):
    return font(style).width(s, size, ls)


def cap(style, size):
    return font(style).cap * size


def fit(style, s, size, max_w, ls=0.0, min_size=10.0):
    """Largest font size <= size at which s fits in max_w."""
    w = tw(style, s, size, ls)
    return size if w <= max_w else max(min_size, size * max_w / w)


# ---------------------------------------------------------------- icons

LUCIDE = {  # lucide-static 0.460.0 (ISC licence), 24x24 grid
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "code": '<path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
    "sparkle": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "external": '<path d="M21 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6"/><path d="m21 3-9 9"/><path d="M15 3h6v6"/>',
    "arrow_up_right": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "arrow_right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "pencil": '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/><path d="m15 5 4 4"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
}

GITHUB_MARK = ("M12.5.75C6.146.75 1 5.896 1 12.25c0 5.089 3.292 9.387 7.863 10.91.575.101.79-.244.79-.546 0-.273-.014-1.178-.014-2.142"
               "-2.889.532-3.636-.704-3.866-1.35-.13-.331-.69-1.352-1.18-1.625-.402-.216-.977-.748-.014-.762.906-.014 1.553.834 1.769 1.179 "
               "1.035 1.74 2.688 1.25 3.349.948.1-.747.402-1.25.733-1.538-2.559-.287-5.232-1.279-5.232-5.678 0-1.25.445-2.285 1.178-3.09"
               "-.115-.288-.517-1.467.115-3.048 0 0 .963-.302 3.163 1.179.92-.259 1.897-.388 2.875-.388.977 0 1.955.13 2.875.388 2.2-1.495 "
               "3.162-1.179 3.162-1.179.633 1.581.23 2.76.115 3.048.733.805 1.179 1.825 1.179 3.09 0 4.413-2.688 5.39-5.247 5.678.417.36.776 "
               "1.05.776 2.128 0 1.538-.014 2.774-.014 3.162 0 .302.216.662.79.547C20.709 21.637 24 17.324 24 12.25 24 5.896 18.854.75 12.5.75Z")


def icon(name, x, y, size, color, sw=2.0):
    """Lucide stroke icon in a size x size box at (x, y); sw is the stroke width in output units."""
    s = size / 24
    return (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({s:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw / s:.3f}" stroke-linecap="round" stroke-linejoin="round">{LUCIDE[name]}</g>')


def github_mark(x, y, size, color):
    s = size / 24
    return f'<path transform="translate({fmt(x)} {fmt(y)}) scale({s:.4f}) translate(-0.5 -0.5)" d="{GITHUB_MARK}" fill="{color}"/>'


def brand_icon(name, x, y, size):
    """Inline a Devicon logo (MIT) from brand-icons/, with ids made unique."""
    with open(os.path.join(HERE, "brand-icons", name + ".svg"), encoding="utf-8") as f:
        src = f.read()
    m = re.search(r'viewBox="([^"]+)"', src)
    inner = src[src.index(">") + 1: src.rindex("</svg>")]
    inner = re.sub(r'id="([^"]+)"', lambda g: f'id="{name}-{g.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda g: f'url(#{name}-{g.group(1)})', inner)
    return f'<svg x="{fmt(x)}" y="{fmt(y)}" width="{fmt(size)}" height="{fmt(size)}" viewBox="{m.group(1)}">{inner}</svg>'


# ---------------------------------------------------------------- shapes

def rect(x, y, w, h, fill="none", rx=0, stroke=None, sw=1.5, extra=""):
    st = f' stroke="{stroke}" stroke-width="{fmt(sw)}"' if stroke else ""
    r = f' rx="{fmt(rx)}"' if rx else ""
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}"{r} fill="{fill}"{st}{extra}/>'


def line(x1, y1, x2, y2, stroke, sw=1.5, extra=""):
    return f'<path d="M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}" stroke="{stroke}" stroke-width="{fmt(sw)}"{extra}/>'


def poly(points, fill, extra=""):
    return f'<path d="M{"L".join(f"{fmt(x)} {fmt(y)}" for x, y in points)}Z" fill="{fill}"{extra}/>'


def poster_bg(w, h, top=False, bottom=False, r=RADIUS, fill=None):
    fill = fill or C["bg"]
    tl = tr = r if top else 0
    bl = br = r if bottom else 0
    d = (f"M{tl} 0H{w - tr}" + (f"A{tr} {tr} 0 0 1 {w} {tr}" if tr else "") + f"V{h - br}"
         + (f"A{br} {br} 0 0 1 {w - br} {h}" if br else "") + f"H{bl}"
         + (f"A{bl} {bl} 0 0 1 0 {h - bl}" if bl else "") + f"V{tl}"
         + (f"A{tl} {tl} 0 0 1 {tl} 0" if tl else "") + "Z")
    return f'<path d="{d}" fill="{fill}"/>'


def section_title(x, baseline, label, mark="slash", size=26):
    """Section heading: pink slash (or lime square) + heavy uppercase label."""
    ch = cap("display", size)
    if mark == "slash":
        top, bot = baseline - ch - 1, baseline + 1
        out = poly([(x + 12, top), (x + 28, top), (x + 16, bot), (x, bot)], C["pink"])
        tx = x + 40
    else:
        sq = ch * 0.92
        out = rect(x, baseline - ch + (ch - sq) / 2, sq, sq, C["lime"])
        tx = x + sq + 14
    return out + text("display", label, tx, baseline, size, C["ink"], ls=-0.01)


# ---------------------------------------------------------------- scenes

class Scene:
    """A full-width poster row that can be exported whole or cropped into slices.

    Each item may declare the x/y extent it occupies so a crop only carries the
    items that are visible in it.
    """

    def __init__(self, h, w=W):
        self.w, self.h = w, h
        self.items, self.defs = [], []

    def add(self, svg, x0=-1e9, x1=1e9, y0=-1e9, y1=1e9):
        self.items.append((x0, x1, y0, y1, svg))

    def svg(self, x0=0, x1=None, title="", y0=0, y1=None):
        x1 = self.w if x1 is None else x1
        y1 = self.h if y1 is None else y1
        body = "".join(s for a, b, c, d, s in self.items if b > x0 and a < x1 and d > y0 and c < y1)
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        w, h = x1 - x0, y1 - y0
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(w)}" height="{fmt(h)}" '
                f'viewBox="{fmt(x0)} {fmt(y0)} {fmt(w)} {fmt(h)}" preserveAspectRatio="none" role="img">'
                f'<title>{esc(title)}</title>{defs}{body}</svg>\n')


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    for attempt in range(5):  # sync clients (e.g. OneDrive) can briefly lock a file they are uploading
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            return path
        except OSError:
            if attempt == 4:
                raise
            time.sleep(1)
