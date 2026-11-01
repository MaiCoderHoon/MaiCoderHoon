"""Small SVG toolkit shared by build_assets.py and gen_stats.py (standard library only).

Text is drawn as vector outlines from glyphs.json, so the profile art renders the
same on every device without relying on fonts installed on the viewer's machine.
All coordinates are poster units: the poster is W x H units (2 units per pixel of
the 882 px wide mockup).
"""
import base64
import html
import json
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))

W = 1764          # poster width
H = 2588          # poster height
RADIUS = 38       # poster corner radius

C = {
    "bg": "#FDF5EE",
    "ink": "#0E0E0E",
    "text": "#171615",
    "muted": "#55524E",
    "pink": "#FC5AC6",       # highlights, section marks, doodles
    "pink_logo": "#FC6FD0",  # the corner of the M
    "lime": "#D8F948",
    "note_lime": "#E0FC53",
    "note_lime_hi": "#ECFD8A",
    "note_pink": "#FD9FD8",
    "note_pink_hi": "#FEB8E2",
    "tile_dark": "#0F0E13",
    "tape": "#302E30",
    "card": "#FFFBF7",
    "card_line": "#D3CEC8",
    "chip_line": "#5E5A56",
    "line": "#E6DFD7",
    "rule": "#8D8984",
    "white": "#FCF8F3",
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


def text(style, s, x, y, size, fill, anchor="start", ls=0.0, extra="", heavy=0.0):
    """Text as a filled outline path. (x, y) is the baseline origin; ls is letter spacing in em.

    heavy > 0 thickens the letters with a matching outline of that width (for an extra-black look).
    """
    d = font(style).d(s, x, y, size, ls, anchor)
    if heavy:
        extra += f' stroke="{fill}" stroke-width="{fmt(heavy)}" stroke-linejoin="round"'
    return f'<path d="{d}" fill="{fill}"{extra}/>' if d else ""


def tw(style, s, size, ls=0.0):
    return font(style).width(s, size, ls)


def cap(style, size):
    return font(style).cap * size


# ---------------------------------------------------------------- icons

LUCIDE = {  # lucide-static 0.460.0 (ISC licence), 24x24 grid
    "map_pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "grad_cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "envelope": '<rect width="20" height="16" x="2" y="4" rx="1.5"/><path d="M2.6 4.8 12 13l9.4-8.2"/><path d="m2.6 19.2 7-6.3"/><path d="m21.4 19.2-7-6.3"/>',
    "code": '<path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "git_branch": '<path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
    "git_pr": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M6 9v12"/>',
    "star": '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    "shield_check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "arrow_up_right": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "arrow_right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "pencil": '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/><path d="m15 5 4 4"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
}

MOON = "M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"

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


def moon(x, y, size, color):
    s = size / 24
    return f'<path transform="translate({fmt(x)} {fmt(y)}) scale({s:.4f})" d="{MOON}" fill="{color}"/>'


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


def raster(path, x, y, w, h, extra=""):
    """Embed an image file (webp/png) as a data URI; SVGs shown via <img> cannot load external files."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    mime = "image/webp" if path.endswith(".webp") else "image/png"
    return (f'<image x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" preserveAspectRatio="none" '
            f'href="data:{mime};base64,{data}"{extra}/>')


# ---------------------------------------------------------------- brand mark

# "Compute M": two slanted strokes and a pink corner, on a 225 x 100 grid.
LOGO_W, LOGO_H = 225, 100
LOGO_A = [(0, 100), (98, 0), (135, 0), (135, 52), (108, 52), (60, 100)]
LOGO_B = [(100, 100), (100, 88), (188, 0), (225, 0), (225, 52), (198, 52), (150, 100)]
LOGO_P = [(178, 100), (178, 89), (206, 61), (225, 61), (225, 100)]


def logo(x, y, h, color, accent=None):
    """The M mark with its top-left corner at (x, y) and height h (width is 2.25 h)."""
    k = h / LOGO_H
    r = max(0.6, h * 0.025)  # soft corners, as in the brand sheet

    def shape(pts, fill):
        d = "M" + "L".join(f"{fmt(x + px * k)} {fmt(y + py * k)}" for px, py in pts) + "Z"
        return f'<path d="{d}" fill="{fill}" stroke="{fill}" stroke-width="{fmt(r)}" stroke-linejoin="round"/>'

    return shape(LOGO_A, color) + shape(LOGO_B, color) + shape(LOGO_P, accent or C["pink_logo"])


# ---------------------------------------------------------------- shapes

def rect(x, y, w, h, fill="none", rx=0, stroke=None, sw=1.5, extra=""):
    st = f' stroke="{stroke}" stroke-width="{fmt(sw)}"' if stroke else ""
    r = f' rx="{fmt(rx)}"' if rx else ""
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}"{r} fill="{fill}"{st}{extra}/>'


def line(x1, y1, x2, y2, stroke, sw=1.5, extra=""):
    return f'<path d="M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}" stroke="{stroke}" stroke-width="{fmt(sw)}"{extra}/>'


def poly(points, fill, extra=""):
    return f'<path d="M{"L".join(f"{fmt(x)} {fmt(y)}" for x, y in points)}Z" fill="{fill}"{extra}/>'


def strokes(segments, color, sw, extra=""):
    """Round-capped strokes, e.g. doodles: [((x1, y1), (x2, y2)), ...] or path strings."""
    d = "".join(s if isinstance(s, str) else f"M{fmt(s[0][0])} {fmt(s[0][1])}L{fmt(s[1][0])} {fmt(s[1][1])}"
                for s in segments)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{fmt(sw)}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}/>')


def poster_bg(w, h, top=False, bottom=False, r=RADIUS, fill=None, x0=0, y0=0):
    fill = fill or C["bg"]
    tl = tr = r if top else 0
    bl = br = r if bottom else 0
    d = (f"M{x0 + tl} {y0}H{x0 + w - tr}" + (f"A{tr} {tr} 0 0 1 {x0 + w} {y0 + tr}" if tr else "")
         + f"V{y0 + h - br}" + (f"A{br} {br} 0 0 1 {x0 + w - br} {y0 + h}" if br else "") + f"H{x0 + bl}"
         + (f"A{bl} {bl} 0 0 1 {x0} {y0 + h - bl}" if bl else "") + f"V{y0 + tl}"
         + (f"A{tl} {tl} 0 0 1 {x0 + tl} {y0}" if tl else "") + "Z")
    return f'<path d="{d}" fill="{fill}"/>'


def section_title(x, baseline, label, size=45.5):
    """Section heading: pink slanted mark + heavy label."""
    ch = cap("display", size)
    top, bot = baseline - ch, baseline + 0.5
    mark = poly([(x + 18, top), (x + 45, top), (x + 27, bot), (x, bot)], C["pink"])
    return mark + text("display", label, x + 68, baseline, size, C["ink"], ls=-0.02, heavy=size * 0.02)


# ---------------------------------------------------------------- scenes

def _used(definition, body):
    """A <defs> entry is kept when it has no id or the body references that id."""
    m = re.search(r'id="([^"]+)"', definition)
    return not m or f"#{m.group(1)}" in body


class Scene:
    """Poster content in absolute poster coordinates, exportable as any rectangular crop.

    Each item may declare the x/y extent it occupies so a crop only carries the
    items that are visible in it; items that don't take the current `region`.
    """

    def __init__(self):
        self.items, self.defs = [], []
        self.region = (-1e9, 1e9, -1e9, 1e9)

    def add(self, svg, x0=None, x1=None, y0=None, y1=None):
        box = [r if v is None else v for v, r in zip((x0, x1, y0, y1), self.region)]
        self.items.append((*box, svg))

    def svg(self, x0, y0, x1, y1, title=""):
        body = "".join(s for a, b, c, d, s in self.items if b > x0 and a < x1 and d > y0 and c < y1)
        defs = "".join(d for d in self.defs if _used(d, body))
        defs = f"<defs>{defs}</defs>" if defs else ""
        w, h = x1 - x0, y1 - y0
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(w)}" height="{fmt(h)}" '
                f'viewBox="{fmt(x0)} {fmt(y0)} {fmt(w)} {fmt(h)}" role="img">'
                f'<title>{esc(title)}</title>{defs}{body}</svg>\n')


def write(name, content):
    path = os.path.join(ASSETS, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for attempt in range(5):  # sync clients (e.g. OneDrive) can briefly lock a file they are uploading
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            return path
        except OSError:
            if attempt == 4:
                raise
            time.sleep(1)
