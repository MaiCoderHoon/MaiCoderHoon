#!/usr/bin/env python3
"""Generate assets/stats.svg using only the Python standard library.

Run by .github/workflows/stats.yml. If the GitHub API is unreachable the existing card is left untouched.
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
INK, GRAY, BORDER = "#151515", "#5E5A52", "#151515"
PALETTE = ["#D7FF3F", "#FF6B35", "#4B55E8", "#151515", "#D7FF3F", "#FF6B35", "#4B55E8"]
SANS, MONO = "'Arial',sans-serif", "'Courier New',monospace"

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
    return {"repos": len(repos), "stars": sum(r.get("stargazers_count", 0) for r in repos),
            "forks": sum(r.get("forks_count", 0) for r in repos),
            "followers": user.get("followers", 0), "langs": langs}

def render(data, updated):
    tiles = [("Public repos", data["repos"], PALETTE[0]), ("Stars earned", data["stars"], PALETTE[1]),
             ("Forks", data["forks"], PALETTE[2]), ("Followers", data["followers"], PALETTE[3])]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300">']
    out.append('<defs><clipPath id="bar"><rect x="60" y="196" width="880" height="20"/></clipPath><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#151515" stroke-opacity=".08"/></pattern></defs>')
    out.append('<rect width="1000" height="300" fill="#F3EFE6"/><rect width="1000" height="300" fill="url(#grid)"/>')
    out.append(f'<rect x="1" y="1" width="998" height="298" fill="none" stroke="{BORDER}" stroke-width="2"/>')
    out.append(f'<text x="60" y="48" font-family="{SANS}" font-size="22" font-weight="800" fill="{INK}">GITHUB / SNAPSHOT</text>')
    out.append(f'<text x="940" y="48" text-anchor="end" font-family="{MONO}" font-size="12" fill="{GRAY}">@{esc(OWNER)}</text>')
    for i, (label, value, color) in enumerate(tiles):
        x = 60 + i * 225
        out.append(f'<rect x="{x}" y="70" width="205" height="86" fill="#F3EFE6" stroke="{color}" stroke-width="3"/>')
        out.append(f'<rect x="{x+2}" y="84" width="6" height="58" fill="{color}"/>')
        out.append(f'<text x="{x+28}" y="116" font-family="{SANS}" font-size="38" font-weight="800" fill="{color}">{esc(value)}</text>')
        out.append(f'<text x="{x+28}" y="141" font-family="{SANS}" font-size="13" font-weight="600" fill="{INK}">{esc(label)}</text>')
    out.append(f'<text x="60" y="184" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="3" fill="{GRAY}">TOP LANGUAGES</text>')
    out.append('<rect x="60" y="196" width="880" height="20" fill="#E3DED3"/>')
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
            color = PALETTE[i % len(PALETTE)] if name != "Other" else "#B8B1A4"
            out.append(f'<rect x="{x:.1f}" y="196" width="{w:.1f}" height="20" fill="{color}"/>')
            x += w
        out.append('</g>')
        lx = 60
        for i, (name, size) in enumerate(top):
            color = PALETTE[i % len(PALETTE)] if name != "Other" else "#B8B1A4"
            label = f"{name} {100.0 * size / total:.0f}%"
            out.append(f'<circle cx="{lx+6}" cy="244" r="6" fill="{color}"/><text x="{lx+18}" y="249" font-family="{SANS}" font-size="13" font-weight="600" fill="{INK}">{esc(label)}</text>')
            lx += 18 + len(label) * 7.6 + 22
    else:
        out.append(f'<text x="60" y="250" font-family="{SANS}" font-size="13" fill="{GRAY}">Languages appear after the first automatic refresh.</text>')
    out.append(f'<text x="940" y="284" text-anchor="end" font-family="{MONO}" font-size="11" fill="{GRAY}">auto-updated {esc(updated)} by GitHub Actions</text>')
    out.append('</svg>')
    return "\\n".join(out)

def main():
    if "--placeholder" in sys.argv:
        data, updated = {"repos": "-", "stars": "-", "forks": "-", "followers": "-", "langs": {}}, "on first run"
    else:
        try:
            data = collect()
        except Exception as exc:
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
