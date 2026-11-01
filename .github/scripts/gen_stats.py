#!/usr/bin/env python3
"""Render the live "GitHub Stats" row of the poster: stat tiles and contribution graph.

Run by .github/workflows/stats.yml every few minutes (standard library only); the
workflow publishes the result to the `output` branch, which the README embeds.
If GitHub can't be reached nothing is written, so the last good card stays live.

    python gen_stats.py                  # writes assets/stats.svg
    python gen_stats.py --out dist/x.svg
    python gen_stats.py --placeholder    # empty data, for layout checks
"""
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from svgkit import C, W, Scene, github_mark, icon, poster_bg, rect, section_title, text, tw, write

OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER") or "MaiCoderHoon"
TOKEN = os.environ.get("GITHUB_TOKEN")

Y0, Y1 = 1900, 2205            # the row's place in the poster (see build_assets.py)
WEEKS = 38                     # columns shown in the graph (about nine months)
GX0, GX1, GY = 830, 1707, 2008  # graph area: left, right, top of the cells
# Contribution levels 0-4: deep green for quiet days, brightening to lime on busy ones.
LEVELS = ["#2F7B24", "#7DB942", "#B4DE2C", "#D3F916", "#EEFC94"]

STYLE = (
    "<style>"
    "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}"
    ".today{animation:pulse 1.6s ease-in-out infinite}"
    "@media (prefers-reduced-motion:reduce){.today{animation:none}}"
    "</style>"
)


def request(url, data=None, accept="application/vnd.github+json"):
    headers = {"Accept": accept, "User-Agent": "profile-stats-card"}
    if TOKEN and "api.github.com" in url:
        headers["Authorization"] = "Bearer " + TOKEN
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def api(path):
    return json.loads(request("https://api.github.com" + path))


def calendar_html():
    """The public calendar page: the same squares the profile shows (private work included if enabled)."""
    page = request(f"https://github.com/users/{urllib.parse.quote(OWNER)}/contributions", accept="text/html")
    cols = {}
    for tag in re.findall(r"<td[^>]*ContributionCalendar-day[^>]*>", page):
        m = re.search(r'id="contribution-day-component-(\d+)-(\d+)"', tag)
        lv = re.search(r'data-level="(\d)"', tag)
        dt = re.search(r'data-date="([\d-]+)"', tag)
        if m and lv and dt:
            cols.setdefault(int(m.group(2)), []).append((int(m.group(1)), int(lv.group(1)), dt.group(1)))
    if not cols:
        raise RuntimeError("no calendar cells found")
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", page)
    return (int(total.group(1).replace(",", "")) if total else None), [sorted(cols[k]) for k in sorted(cols)]


def calendar_graphql():
    query = ('query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{'
             'totalContributions weeks{contributionDays{weekday date contributionLevel}}}}}}')
    body = json.dumps({"query": query, "variables": {"login": OWNER}}).encode()
    cal = json.loads(request("https://api.github.com/graphql", data=body))["data"]["user"][
        "contributionsCollection"]["contributionCalendar"]
    names = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
    weeks = [[(d["weekday"], names.index(d["contributionLevel"]), d["date"]) for d in w["contributionDays"]]
             for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def collect():
    user = api(f"/users/{OWNER}")
    repos = [r for r in api(f"/users/{OWNER}/repos?per_page=100&type=owner") if not r.get("fork")]
    commits = api(f"/search/commits?q=author:{OWNER}&per_page=1")["total_count"]
    prs = api(f"/search/issues?q=author:{OWNER}+type:pr&per_page=1")["total_count"]
    try:
        total, weeks = calendar_html()
    except Exception as exc:
        if not TOKEN:
            raise
        print("calendar page failed, using GraphQL:", exc)
        total, weeks = calendar_graphql()
    return {"repos": user.get("public_repos", 0), "commits": commits, "prs": prs,
            "stars": sum(r.get("stargazers_count", 0) for r in repos), "total": total, "weeks": weeks}


def short(n):
    if not isinstance(n, int):
        return str(n)
    if n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "K+"
    return str(n)


def stat_icon(kind, cx, cy, size):
    x, y = cx - size / 2, cy - size / 2
    if kind == "repos":
        return github_mark(x, y, size, C["ink"])
    name = {"commits": "git_branch", "prs": "git_pr", "stars": "star"}[kind]
    return icon(name, x, y, size, C["ink"], 3.8)


def render(data):
    sc = Scene()
    sc.defs.append(STYLE)
    sc.add(poster_bg(W, Y1 - Y0, y0=Y0))
    sc.add(section_title(77, 1960, "GitHub Stats"))

    # stat tiles
    stats = [("repos", "Repos", data["repos"]), ("commits", "Commits", data["commits"]),
             ("prs", "PRs", data["prs"]), ("stars", "Stars", data["stars"])]
    for i, (kind, label, value) in enumerate(stats):
        x, y, w, h = 74 + i * 176, 1993, 158, 180
        cx = x + w / 2
        sc.add(rect(x, y, w, h, C["card"], rx=20, stroke=C["card_line"], sw=2.2))
        sc.add(stat_icon(kind, cx, y + 46, 46))
        sc.add(text("display", short(value), cx, y + 121, 38, C["ink"], anchor="middle", ls=-0.02, heavy=0.76))
        sc.add(text("body", label, cx, y + 156, 25.5, C["text"], anchor="middle", heavy=0.4))

    # contribution graph
    weeks = [w for w in data["weeks"] if w][-WEEKS:]
    pitch = (GX1 - GX0) / WEEKS
    size, rx = pitch - 3.6, 3.2
    x_left = GX1 - len(weeks) * pitch if weeks else GX0
    for i in range(WEEKS - len(weeks)):  # an empty grid until there's data
        for day in range(7):
            sc.add(rect(GX0 + i * pitch, GY + day * pitch, size, size, LEVELS[0], rx=rx, extra=' opacity=".35"'))
    last_label_x = -1e9
    prev_month = None
    for i, week in enumerate(weeks):
        x = x_left + i * pitch
        sc.add("".join(rect(x, GY + day * pitch, size, size, LEVELS[min(level, 4)], rx=rx)
                       for day, level, _ in week))
        first = datetime.date.fromisoformat(week[0][2])
        # label a month at the first column that starts in it, if there's room for the word
        if first.month != prev_month and (i > 0 or first.day <= 7):
            label = first.strftime("%b")
            if x - last_label_x > tw("semi", "May", 21) + 18 and x + tw("semi", label, 21) <= GX1 + 4:
                sc.add(text("semi", label, x + 2, 1980, 21, C["text"]))
                last_label_x = x
        prev_month = first.month
    if weeks:  # pulsing outline on the most recent day
        day = weeks[-1][-1][0]
        x = x_left + (len(weeks) - 1) * pitch
        sc.add(rect(x - 2, GY + day * pitch - 2, size + 4, size + 4, "none", rx=rx + 1.5, stroke=C["pink"], sw=3,
                    extra=' class="today"'))
    total = data.get("total")
    title = "GitHub stats: " + ", ".join(f"{short(v)} {lbl.lower()}" for _, lbl, v in stats)
    if isinstance(total, int):
        title += f"; {total:,} contributions in the last year"
    return sc.svg(0, Y0, W, Y1, title=title)


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    if "--placeholder" in sys.argv:
        data = {"repos": "–", "commits": "–", "prs": "–", "stars": "–", "total": None, "weeks": []}
    else:
        try:
            data = collect()
        except Exception as exc:
            print("stats refresh skipped:", exc)
            return 0
    svg = render(data)
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print("wrote", out)
    else:
        print("wrote", write("stats.svg", svg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
