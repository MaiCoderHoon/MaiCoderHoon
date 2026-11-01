#!/usr/bin/env python3
"""Render the live GitHub stats used in the profile README.

    stats.svg          four sticker tiles: public repos, commits, pull requests, stars
    contributions.svg  the contribution graph for the last year

Run by .github/workflows/stats.yml every 10 minutes (standard library only); the
workflow publishes both files to the `output` branch, which the README embeds.
If GitHub can't be reached nothing is written, so the last good cards stay live.

    python gen_stats.py                     # writes dist/stats.svg + dist/contributions.svg
    python gen_stats.py --out-dir some/dir
    python gen_stats.py --placeholder       # empty data, for layout checks
"""
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from svgkit import C, doc, fmt, github_mark, icon, rect, text, tw

OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER") or "MaiCoderHoon"
TOKEN = os.environ.get("GITHUB_TOKEN")
INK, PAPER = C["ink"], C["paper"]
LEVELS = ["#ECE4D7", C["lime"], "#8EDB3A", "#4FAF3A", "#2A7A2E"]  # none, then brand lime -> deep green
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

# Only the "today" outline and the live dot pulse, and never below 25% opacity, so the
# cards are fully drawn in every frame (previews and thumbnails included).
STYLE = ("@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}"
         ".today,.live{animation:pulse 1.6s ease-in-out infinite}")


# ------------------------------------------------------------------ data

def request(url, data=None, accept="application/vnd.github+json"):
    headers = {"Accept": accept, "User-Agent": "profile-stats-card"}
    if TOKEN and "api.github.com" in url:
        headers["Authorization"] = "Bearer " + TOKEN
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def api(path):
    return json.loads(request("https://api.github.com" + path))


def calendar_graphql():
    query = ('query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{'
             'totalContributions weeks{contributionDays{date weekday contributionLevel}}}}}}')
    body = json.dumps({"query": query, "variables": {"login": OWNER}}).encode()
    cal = json.loads(request("https://api.github.com/graphql", data=body))["data"]["user"][
        "contributionsCollection"]["contributionCalendar"]
    names = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
    weeks = [[(d["weekday"], names.index(d["contributionLevel"]), d["date"]) for d in w["contributionDays"]]
             for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def calendar_html():
    page = request(f"https://github.com/users/{urllib.parse.quote(OWNER)}/contributions", accept="text/html")
    cells = {}
    for tag in re.findall(r"<td[^>]*ContributionCalendar-day[^>]*>", page):
        m = re.search(r'id="contribution-day-component-(\d+)-(\d+)"', tag)
        lv = re.search(r'data-level="(\d)"', tag)
        dt = re.search(r'data-date="([\d-]+)"', tag)
        if m and lv and dt:
            cells.setdefault(int(m.group(2)), []).append((int(m.group(1)), int(lv.group(1)), dt.group(1)))
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", page)
    if not cells:
        raise RuntimeError("no calendar cells found")
    weeks = [sorted(cells[k]) for k in sorted(cells)]
    return (int(total.group(1).replace(",", "")) if total else None), weeks


def collect():
    user = api(f"/users/{OWNER}")
    repos = [r for r in api(f"/users/{OWNER}/repos?per_page=100&type=owner") if not r.get("fork")]
    commits = api(f"/search/commits?q=author:{OWNER}&per_page=1")["total_count"]
    prs = api(f"/search/issues?q=author:{OWNER}+type:pr&per_page=1")["total_count"]
    try:
        total, weeks = calendar_graphql() if TOKEN else calendar_html()
    except Exception as exc:
        print("graphql calendar failed, using public page:", exc)
        total, weeks = calendar_html()
    return {"repos": user.get("public_repos", 0), "commits": commits, "prs": prs,
            "stars": sum(r.get("stargazers_count", 0) for r in repos), "total": total, "weeks": weeks}


def short(n):
    if not isinstance(n, int):
        return str(n)
    if n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "K+"
    return str(n)


# ------------------------------------------------------------------ cards

def sticker(x, y, w, h, rx=16):
    return (rect(x + 1, y + 3, w, h, INK, rx=rx, extra=' opacity=".14"')
            + rect(x, y, w, h, PAPER, rx=rx, stroke=INK, sw=2.2))


def render_stats(data):
    """Four tiles, 404 x 120. Labels stay short so they read at phone width."""
    tiles = [("Repos", data["repos"], "github"), ("Commits", data["commits"], "commit"),
             ("PRs", data["prs"], "pull_request"), ("Stars", data["stars"], "star")]
    tw_, gap, body = 91, 12, []
    for i, (label, value, ic) in enumerate(tiles):
        x = 2 + i * (tw_ + gap)
        cx = x + tw_ / 2
        body.append(sticker(x, 4, tw_, 108))
        if ic == "github":
            body.append(github_mark(cx - 12, 18, 24, INK))
        elif ic == "star":
            body.append(icon("star", cx - 13, 17, 26, INK, 2.2).replace('fill="none"', f'fill="{C["lime"]}"'))
        else:
            body.append(icon(ic, cx - 13, 17, 26, INK, 2.3))
        body.append(text("display", short(value), cx, 78, 27, INK, anchor="middle", ls=-0.02))
        body.append(text("body", label, cx, 99, 14.5, C["muted"], anchor="middle"))
    alt = ", ".join(f"{short(v)} {label.lower()}" for label, v, _ in tiles)
    return doc(406, 118, "".join(body), f"GitHub stats for {OWNER}: {alt}")


def render_graph(data, synced):
    """Contribution graph card, 440 x 118."""
    W, H = 440, 118
    weeks = data["weeks"] or [[(d, 0, None) for d in range(7)] for _ in range(53)]
    x0, x1, gy = 16, W - 16, 32
    pitch = (x1 - x0) / len(weeks)
    cell = pitch - 1.6
    body = [sticker(2, 4, W - 6, H - 10)]
    # month labels where a new month starts, skipping any that would collide or overflow
    last_label_end = -99
    for i, week in enumerate(weeks):
        first = week[0][2]
        if not first:
            continue
        d = datetime.date.fromisoformat(first)
        lx, label = x0 + i * pitch, MONTHS[d.month - 1]
        end = lx + tw("body", label, 10.5)
        if d.day <= 7 and lx - last_label_end > 6 and end <= x1:
            body.append(text("body", label, lx, 25, 10.5, C["muted"]))
            last_label_end = end
    for i, week in enumerate(weeks):
        body.append("".join(rect(x0 + i * pitch + 0.8, gy + day * pitch + 0.8, cell, cell, LEVELS[level], rx=1.6)
                            for day, level, _ in week))
    if data["weeks"] and data["weeks"][-1]:  # pulsing outline on the most recent day
        day = data["weeks"][-1][-1][0]
        body.append(rect(x0 + (len(weeks) - 1) * pitch, gy + day * pitch, pitch, pitch, "none",
                         rx=2, stroke=C["pink"], sw=1.8, extra=' class="today"'))
    cy = gy + 7 * pitch + 16
    total = data.get("total")
    caption = f"{total:,} contributions in the last year" if isinstance(total, int) else "Contributions in the last year"
    body.append(text("semi", caption, x0, cy, 11.5, INK))
    stamp = f"synced {synced}"
    body.append(text("mono", stamp, x1, cy, 10, C["muted"], anchor="end"))
    dot_x = x1 - tw("mono", stamp, 10) - 9
    body.append(f'<circle class="live" cx="{fmt(dot_x)}" cy="{fmt(cy - 3.5)}" r="3.4" fill="{C["pink"]}"/>')
    return doc(W, H, "".join(body), f"Contribution graph for {OWNER}: {caption.lower()}", style=STYLE)


# ------------------------------------------------------------------ main

def main():
    out_dir = sys.argv[sys.argv.index("--out-dir") + 1] if "--out-dir" in sys.argv else "dist"
    if "--placeholder" in sys.argv:
        data = {"repos": "–", "commits": "–", "prs": "–", "stars": "–", "total": None, "weeks": []}
        synced = "pending"
    else:
        try:
            data = collect()
        except Exception as exc:
            print("stats refresh skipped:", exc)
            return 0
        synced = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M UTC")
    os.makedirs(out_dir, exist_ok=True)
    for name, svg in (("stats.svg", render_stats(data)), ("contributions.svg", render_graph(data, synced))):
        dest = os.path.join(out_dir, name)
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
