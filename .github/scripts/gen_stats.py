#!/usr/bin/env python3
"""Generate assets/stats.svg (a light, animated GitHub stats card) using only the standard library.

Run by .github/workflows/stats.yml. If the GitHub API is unreachable the existing card is left untouched.
Use --placeholder to render the initial "waiting for first refresh" card.
"""
import datetime
import html
import json
import os
import sys
import urllib.request

OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER") or "MaiCoderHoon"
TOKEN = os.environ.get("GITHUB_TOKEN")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "stats.svg")

INK = "#2B2140"
GRAY = "#8A7FA8"
BORDER = "#E9DFF7"
PALETTE = ["#7C5CFF", "#FF6B9D", "#2EC4A6", "#FFA35C", "#5B8DEF", "#B79CFF", "#8AD6C4"]
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'Courier New',monospace"


def esc(s):
    return html.escape(str(s), quote=False)


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats-card"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    req = urllib.request.Request("https://api.github.com" + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect():
    user = api(f"/users/{OWNER}")
    repos = [r for r in api(f"/users/{OWNER}/repos?per_page=100&type=owner")
             if not r.get("fork") and r["name"].lower() != OWNER.lower()]
    langs = {}
    for r in repos:
        try:
            for lang, size in api(f"/repos/{OWNER}/{r['name']}/languages").items():
                langs[lang] = langs.get(lang, 0) + size
        except Exception:
            continue
    return {
        "repos": len(repos),
        "stars": sum(r.get("stargazers_count", 0) for r in repos),
        "forks": sum(r.get("forks_count", 0) for r in repos),
        "followers": user.get("followers", 0),
        "langs": langs,
    }


def render(data, updated):
    tiles = [("Public repos", data["repos"], PALETTE[0]), ("Stars earned", data["stars"], PALETTE[1]),
             ("Forks", data["forks"], PALETTE[2]), ("Followers", data["followers"], PALETTE[3])]
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300">')
    out.append('<defs><clipPath id="bar"><rect x="60" y="196" width="880" height="20" rx="10"/></clipPath>'
               '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF7F0"/>'
               '<stop offset="1" stop-color="#F4EEFF"/></linearGradient></defs>')
    out.append('<rect width="1000" height="300" rx="22" fill="url(#bg)"/>')
    out.append(f'<rect x="1" y="1" width="998" height="298" rx="22" fill="none" stroke="{BORDER}" stroke-width="2"/>')
    out.append(f'<text x="60" y="48" font-family="{SANS}" font-size="22" font-weight="800" fill="{INK}">GitHub garden</text>')
    out.append(f'<text x="940" y="48" text-anchor="end" font-family="{MONO}" font-size="12" fill="{GRAY}">@{esc(OWNER)}</text>')

    for i, (label, value, color) in enumerate(tiles):
        x = 60 + i * 225
        out.append(f'<g><animate attributeName="opacity" values="0;1" dur="0.6s" begin="{i*0.15:.2f}s" fill="freeze"/>'
                   f'<rect x="{x}" y="70" width="205" height="86" rx="16" fill="#FFFFFF" stroke="{color}" stroke-opacity="0.55" stroke-width="2"/>'
                   f'<rect x="{x+2}" y="84" width="6" height="58" rx="3" fill="{color}"/>'
                   f'<text x="{x+28}" y="116" font-family="{SANS}" font-size="38" font-weight="800" fill="{color}">{esc(value)}</text>'
                   f'<text x="{x+28}" y="141" font-family="{SANS}" font-size="13" font-weight="600" fill="{INK}">{esc(label)}</text></g>')

    out.append(f'<text x="60" y="184" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="3" fill="{GRAY}">TOP LANGUAGES</text>')
    out.append(f'<rect x="60" y="196" width="880" height="20" rx="10" fill="#EFE9FF"/>')

    langs = sorted(data["langs"].items(), key=lambda kv: kv[1], reverse=True)
    total = sum(v for _, v in langs)
    if total:
        top = langs[:6]
        rest = total - sum(v for _, v in top)
        if rest > 0:
            top.append(("Other", rest))
        x = 60.0
        out.append('<g clip-path="url(#bar)">')
        for i, (name, size) in enumerate(top):
            w = 880.0 * size / total
            color = PALETTE[i % len(PALETTE)] if name != "Other" else "#CFC6E6"
            out.append(f'<rect x="{x:.1f}" y="196" width="{w:.1f}" height="20" fill="{color}">'
                       f'<animate attributeName="width" values="0;{w:.1f}" dur="0.9s" begin="{0.3 + i*0.15:.2f}s" fill="freeze"/></rect>')
            x += w
        out.append('</g>')
        lx = 60
        for i, (name, size) in enumerate(top):
            color = PALETTE[i % len(PALETTE)] if name != "Other" else "#CFC6E6"
            pct = 100.0 * size / total
            label = f"{name} {pct:.0f}%"
            out.append(f'<circle cx="{lx+6}" cy="244" r="6" fill="{color}"/>'
                       f'<text x="{lx+18}" y="249" font-family="{SANS}" font-size="13" font-weight="600" fill="{INK}">{esc(label)}</text>')
            lx += 18 + len(label) * 7.6 + 22
    else:
        out.append(f'<text x="60" y="250" font-family="{SANS}" font-size="13" fill="{GRAY}">Languages appear after the first automatic refresh.</text>')

    out.append(f'<text x="940" y="284" text-anchor="end" font-family="{MONO}" font-size="11" fill="{GRAY}">auto-updated {esc(updated)} by GitHub Actions</text>')
    out.append('</svg>')
    return "\n".join(out)


def main():
    if "--placeholder" in sys.argv:
        data = {"repos": "-", "stars": "-", "forks": "-", "followers": "-", "langs": {}}
        updated = "on first run"
    elif os.environ.get("MOCK_STATS"):
        data = {"repos": 3, "stars": 0, "forks": 0, "followers": 0,
                "langs": {"Kotlin": 61000, "Python": 48000, "Dart": 52000, "C++": 9000, "CMake": 4000}}
        updated = "preview"
    else:
        try:
            data = collect()
        except Exception as exc:  # keep the previous card if the API is unavailable
            print("stats refresh skipped:", exc)
            return 0
        updated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render(data, updated))
    print("wrote", os.path.normpath(OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
