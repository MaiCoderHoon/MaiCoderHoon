#!/usr/bin/env python3
"""Render assets/stats.svg: GitHub stats, contribution graph and "now exploring".

Run by .github/workflows/stats.yml (standard library only). If GitHub can't be
reached the existing card is left untouched. `--placeholder` renders empty data.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

from svgkit import C, MARGIN, W, Scene, cap, github_mark, icon, line, poster_bg, rect, section_title, text, tw, write

OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER") or "MaiCoderHoon"
TOKEN = os.environ.get("GITHUB_TOKEN")
LEVELS = ["#0B3D14", "#22802A", "#4BAE2C", "#97DE1A", C["lime"]]
EXPLORING = [("ML / AI", "sparkle"), ("Data Science", "database"), ("App Dev", "smartphone")]


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
             'totalContributions weeks{contributionDays{weekday contributionLevel}}}}}}')
    body = json.dumps({"query": query, "variables": {"login": OWNER}}).encode()
    cal = json.loads(request("https://api.github.com/graphql", data=body))["data"]["user"][
        "contributionsCollection"]["contributionCalendar"]
    names = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
    weeks = [[(d["weekday"], names.index(d["contributionLevel"])) for d in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def calendar_html():
    page = request(f"https://github.com/users/{urllib.parse.quote(OWNER)}/contributions", accept="text/html")
    cells = {}
    for tag in re.findall(r"<td[^>]*ContributionCalendar-day[^>]*>", page):
        m = re.search(r'id="contribution-day-component-(\d+)-(\d+)"', tag)
        lv = re.search(r'data-level="(\d)"', tag)
        if m and lv:
            cells.setdefault(int(m.group(2)), []).append((int(m.group(1)), int(lv.group(1))))
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", page)
    if not cells:
        raise RuntimeError("no calendar cells found")
    return (int(total.group(1).replace(",", "")) if total else None), [cells[k] for k in sorted(cells)]


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


def render(data):
    h = 200
    sc = Scene(h)
    sc.add(poster_bg(W, h))
    sc.add(line(MARGIN, 10, W - MARGIN, 10, C["ink"], 1.5))

    # GitHub stats
    sc.add(section_title(MARGIN, 62, "GITHUB STATS", mark="square", size=22))
    sc.add(github_mark(MARGIN + 2, 96, 60, C["ink"]))
    stats = [("Repos", data["repos"]), ("Commits", data["commits"]), ("PRs", data["prs"]), ("Stars", data["stars"])]
    for i, (label, value) in enumerate(stats):
        cx = 172 + i * 92
        sc.add(text("display", short(value), cx, 132, 31, C["ink"], anchor="middle", ls=-0.02))
        sc.add(text("body", label, cx, 160, 16.5, C["text"], anchor="middle"))
        if i:
            sc.add(f'<circle cx="{cx - 46}" cy="122" r="2.2" fill="{C["ink"]}"/>')
    sc.add(line(492, 34, 492, 186, C["ink"], 1.5))

    # contribution graph
    gx0, gx1, gy = 518, 1000, 88
    sc.add(section_title(gx0, 62, "CONTRIBUTION GRAPH", mark="square", size=22))
    weeks = data["weeks"] or [[(d, 0) for d in range(7)] for _ in range(53)]
    cell = (gx1 - gx0) / len(weeks)
    sc.add(rect(gx0, gy, gx1 - gx0, cell * 7, "#062B0D"))
    for i, week in enumerate(weeks):
        for day, level in week:
            sc.add(rect(gx0 + i * cell + 0.6, gy + day * cell + 0.6, cell - 1.2, cell - 1.2, LEVELS[level]))
    caption = (f"{data['total']:,} contributions in the last year" if isinstance(data.get("total"), int)
               else "Contributions in the last year")
    sc.add(text("body", caption, gx0, gy + cell * 7 + 30, 15, C["muted"]))
    sc.add(line(1026, 34, 1026, 186, C["ink"], 1.5))

    # now exploring
    nx0, nx1 = 1052, W - MARGIN
    sc.add(section_title(nx0, 62, "NOW EXPLORING", mark="square", size=22))
    size, pad, isz, gap, ph = 17, 15, 20, 10, 50

    def pw(label, s):
        return pad + isz + 9 + tw("semi", label, s) + pad

    while sum(pw(l, size) for l, _ in EXPLORING) + gap * (len(EXPLORING) - 1) > nx1 - nx0:
        size -= 0.25
    px, py = nx0, 94
    for label, ic in EXPLORING:
        w = pw(label, size)
        sc.add(rect(px + 0.75, py + 0.75, w - 1.5, ph - 1.5, C["tile"], rx=12, stroke=C["tile_line"], sw=1.5))
        sc.add(icon(ic, px + pad, py + (ph - isz) / 2, isz, C["ink"], 1.9))
        sc.add(text("semi", label, px + pad + isz + 9, py + ph / 2 + cap("semi", size) / 2, size, C["ink"]))
        px += w + gap
    return sc.svg(title="GitHub stats, contribution graph and what I'm exploring now")


def main():
    if "--placeholder" in sys.argv:
        data = {"repos": "–", "commits": "–", "prs": "–", "stars": "–", "total": None, "weeks": []}
    else:
        try:
            data = collect()
        except Exception as exc:
            print("stats refresh skipped:", exc)
            return 0
    print("wrote", write("stats.svg", render(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
