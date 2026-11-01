"""Small SVG toolkit shared by build_assets.py, illustrations.py and gen_stats.py (standard library only).

Text inside the art is drawn as vector outlines from glyphs.json, so illustrations
render the same on every device without relying on fonts installed on the viewer's
machine. All README *copy* lives in README.md as real text; SVG text is limited to
decoration (handwritten notes in illustrations) and the live stats numbers.
"""
import html
import json
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))

# C1 "whimsical & playful" palette. The first five are the brand colours; the rest are
# tints used inside illustrations.
C = {
    "cream": "#FBF6F0",
    "ink": "#0E0E0E",
    "pink": "#FC80D6",
    "lime": "#C9FF3D",
    "white": "#FFFFFF",
    "paper": "#FFFDF8",       # sticky notes, tiles
    "pink_soft": "#FDB6DE",
    "pink_pale": "#FED3EE",
    "lav": "#DAC1FC",
    "lav_deep": "#B79AF2",
    "lime_soft": "#E4FF9E",
    "muted": "#6B655D",
    "line": "#E6DDD0",
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
    """Text as a filled outline path. (x, y) is the baseline origin.

    Styles: display / bold / semi / body (Inter Tight), mono / monob (JetBrains Mono),
    hand (Caveat, for handwritten notes)."""
    d = font(style).d(s, x, y, size, ls, anchor)
    return f'<path d="{d}" fill="{fill}"{extra}/>' if d else ""


def tw(style, s, size, ls=0.0):
    return font(style).width(s, size, ls)


def cap(style, size):
    return font(style).cap * size


# ---------------------------------------------------------------- icons

LUCIDE = {  # lucide-static (ISC licence), 24x24 grid
    "code": '<path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "pencil": '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/><path d="m15 5 4 4"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "map_pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "grad_cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
    "commit": '<circle cx="12" cy="12" r="3"/><path d="M3 12h6"/><path d="M15 12h6"/>',
    "pull_request": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M6 9v12"/>',
    "star": '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
}

GITHUB_MARK = ("M12.5.75C6.146.75 1 5.896 1 12.25c0 5.089 3.292 9.387 7.863 10.91.575.101.79-.244.79-.546 0-.273-.014-1.178-.014-2.142"
               "-2.889.532-3.636-.704-3.866-1.35-.13-.331-.69-1.352-1.18-1.625-.402-.216-.977-.748-.014-.762.906-.014 1.553.834 1.769 1.179 "
               "1.035 1.74 2.688 1.25 3.349.948.1-.747.402-1.25.733-1.538-2.559-.287-5.232-1.279-5.232-5.678 0-1.25.445-2.285 1.178-3.09"
               "-.115-.288-.517-1.467.115-3.048 0 0 .963-.302 3.163 1.179.92-.259 1.897-.388 2.875-.388.977 0 1.955.13 2.875.388 2.2-1.495 "
               "3.162-1.179 3.162-1.179.633 1.581.23 2.76.115 3.048.733.805 1.179 1.825 1.179 3.09 0 4.413-2.688 5.39-5.247 5.678.417.36.776 "
               "1.05.776 2.128 0 1.538-.014 2.774-.014 3.162 0 .302.216.662.79.547C20.709 21.637 24 17.324 24 12.25 24 5.896 18.854.75 12.5.75Z")


# A four-point twinkle star in a 32 x 32 box (lime fill + ink outline reads on light and dark).
TWINKLE = ("M16 2 C 17.2 11, 21 14.8 30 16 C 21 17.2, 17.2 21, 16 30 C 14.8 21, 11 17.2, 2 16 "
           "C 11 14.8, 14.8 11, 16 2 Z")


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
    return (f'<path d="M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}" stroke="{stroke}" stroke-width="{fmt(sw)}" '
            f'stroke-linecap="round"{extra}/>')


def poly(points, fill, extra=""):
    return f'<path d="M{"L".join(f"{fmt(x)} {fmt(y)}" for x, y in points)}Z" fill="{fill}"{extra}/>'


def path(d, fill="none", stroke=None, sw=2.5, extra=""):
    st = (f' stroke="{stroke}" stroke-width="{fmt(sw)}" stroke-linecap="round" stroke-linejoin="round"'
          if stroke else "")
    return f'<path d="{d}" fill="{fill}"{st}{extra}/>'


def m_mark(cx, cy, size, uid="m", main="#FFFFFF", accent=None):
    """The MaiCoderHoon 'M': two rounded peaks with a pink foot, slightly italic.

    Drawn centred on (cx, cy), `size` wide. Returns (defs, body); `uid` keeps the
    clip-path id unique when a document uses the mark more than once."""
    accent = accent or C["pink"]
    s = size / 40
    clip = f'<clipPath id="{uid}"><rect x="-6" y="-6" width="52" height="34"/></clipPath>'
    body = (f'<g transform="translate({fmt(cx)} {fmt(cy)}) skewX(-9) scale({s:.4f}) translate(-20 -14)" '
            f'clip-path="url(#{uid})">'
            f'<polyline points="0 30 9.5 1.5 20 22 30.5 1.5 34.6 13.8" fill="none" stroke="{main}" '
            f'stroke-width="8.5" stroke-linejoin="round"/>'
            f'<path d="M36 18 L40.5 31.5" stroke="{accent}" stroke-width="8.5"/></g>')
    return clip, body


# Motion is always optional: every animated SVG is fully drawn in its first frame
# and stops animating for viewers who ask for reduced motion.
REDUCED_MOTION = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def doc(w, h, body, title, defs="", style="", decorative=False):
    """A standalone SVG document sized w x h."""
    css = f"<style>{style}{REDUCED_MOTION}</style>" if style else ""
    d = f"<defs>{defs}</defs>" if defs else ""
    aria = ' aria-hidden="true"' if decorative else ' role="img"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(w)}" height="{fmt(h)}" '
            f'viewBox="0 0 {fmt(w)} {fmt(h)}"{aria}><title>{esc(title)}</title>{css}{d}{body}</svg>\n')


def write(name, content):
    """Write assets/<name>, creating sub-folders as needed."""
    path_ = os.path.join(ASSETS, *name.split("/"))
    os.makedirs(os.path.dirname(path_), exist_ok=True)
    for attempt in range(5):  # sync clients (e.g. OneDrive) can briefly lock a file they are uploading
        try:
            with open(path_, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            return path_
        except OSError:
            if attempt == 4:
                raise
            time.sleep(1)
