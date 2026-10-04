#!/usr/bin/env python3
"""Pull popular games from RAWG's public Nintendo platform pages and write titles.json."""
import json, re, unicodedata, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path("/workspace/where-to-play-nintendo")
UA = "WhereToPlayCatalog/1.0 (static catalog; attribution https://rawg.io)"
PAGES = [
    ("NES", "nes", "nso"),
    ("SNES", "snes", "nso"),
    ("Nintendo 64", "nintendo-64", "n64"),
    ("Game Boy", "game-boy", "nso"),
    ("Game Boy Color", "game-boy-color", "gbc"),
    ("Game Boy Advance", "game-boy-advance", "gba"),
    ("GameCube", "gamecube", "gc"),
    ("Wii", "wii", "legacy"),
    ("Wii U", "wii-u", "legacy"),
    ("Nintendo DS", "nintendo-ds", "legacy"),
    ("Nintendo 3DS", "nintendo-3ds", "legacy"),
    ("Nintendo Switch", "nintendo-switch", "switch"),
]
MAX_PAGE = 5  # 40 per page -> up to 200 per system before dedupe

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8", "replace")

def parse(html):
    m = re.search(r"window\.CLIENT_PARAMS = (\{.*?)</script>", html, re.S)
    if not m:
        raise ValueError("no params")
    return json.loads(m.group(1))["initialState"]

def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def names(items):
    out = []
    for item in items or []:
        if isinstance(item, dict) and item.get("name"):
            out.append(item["name"])
        elif isinstance(item, str):
            out.append(item)
    return out

def one_page(platform, path, page):
    url = f"https://rawg.io/games/{path}" + (f"?page={page}" if page > 1 else "")
    state = parse(fetch(url))
    block = state["games"]["games"]
    ents = state["entities"]["games"]
    rows = []
    for key in block.get("results") or []:
        g = ents.get(key) if isinstance(key, str) else None
        if not g:
            continue
        slug = g.get("slug") or ""
        if not slug or "arcade-archives" in slug:
            continue
        bg = g.get("background_image")
        if not bg or "media.rawg.io" not in bg:
            continue
        released = g.get("released") or ""
        year = released[:4] if re.match(r"19\d{2}|20\d{2}", released or "") else ""
        if not year:
            continue
        shots = []
        for s in g.get("short_screenshots") or []:
            img = s.get("image") if isinstance(s, dict) else None
            if not img or img == bg or "/screenshots/" not in img:
                continue
            shots.append({"url": img, "width": 0, "height": 0})
            if len(shots) == 2:
                break
        esrb = g.get("esrb_rating") or {}
        rows.append({
            "rawg_slug": slug,
            "name": g.get("name") or slug,
            "year": year,
            "platform": platform,
            "genres": [x["name"] for x in (g.get("genres") or []) if isinstance(x, dict) and x.get("name")],
            "developers": names(g.get("developers")),
            "publishers": names(g.get("publishers")),
            "esrb": esrb.get("name") if isinstance(esrb, dict) else None,
            "rating": g.get("rating"),
            "ratings_count": g.get("ratings_count") or 0,
            "released": released,
            "background_image": bg,
            "screenshots": shots,
            "rawg_platforms": names(g.get("platforms")),
        })
    return platform, page, block.get("count"), rows

def main():
    jobs = [(plat, path, avail, page) for plat, path, avail in PAGES for page in range(1, MAX_PAGE + 1)]
    found = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(one_page, plat, path, page): (plat, page) for plat, path, avail, page in jobs}
        for fut in as_completed(futs):
            plat, page = futs[fut]
            try:
                platform, pg, count, rows = fut.result()
                print(f"{platform} p{pg} count={count} rows={len(rows)}", flush=True)
                found.extend(rows)
            except Exception as e:
                print("fail", plat, page, e, flush=True)

    # merge same rawg slug across nintendo platforms
    merged = {}
    for row in found:
        cur = merged.get(row["rawg_slug"])
        if not cur:
            merged[row["rawg_slug"]] = row
            row["platforms"] = [row["platform"]]
        else:
            if row["platform"] not in cur["platforms"]:
                cur["platforms"].append(row["platform"])
    print("unique rawg", len(merged), flush=True)

    ns = {}
    exec(compile((ROOT / "data" / "titles_src.py").read_text(), "titles_src.py", "exec"), ns)
    hand = ns["G"]
    hand_by_rawg = {}
    for h in hand:
        hand_by_rawg[h["slug"]] = h
        for r in h["rawg"]:
            hand_by_rawg[r] = h

    avail_for = {plat: avail for plat, path, avail in PAGES}
    order = [p for p, _, _ in PAGES]
    used = set()
    out = []
    matched_hand = set()

    def history_for(name, year, platforms, genres):
        plat = " and ".join(platforms)
        g = ", ".join(genres[:3]) if genres else "mixed styles"
        return (
            f"{name} is a {year} release on {plat}. "
            f"RAWG files it among {g}.",
            f"This catalog keeps it on {plat}. Any later re-release is a different page when it is a separate game, not a guess about a current listing.",
        )

    for slug, row in merged.items():
        h = hand_by_rawg.get(slug)
        if h is None:
            # loose name match
            n = norm(row["name"])
            for cand in hand:
                if norm(cand["title"]) == n and abs(int(cand["year"]) - int(row["year"])) <= 1:
                    h = cand
                    break
        platforms = list(row["platforms"])
        if h:
            matched_hand.add(h["slug"])
            for p in h["platforms"]:
                if p not in platforms:
                    platforms.append(p)
            title = h["title"]
            year = h["year"]
            credit = h["credit"]
            our_slug = h["slug"]
            avail = h["avail"]
            history, lineup = h["history"], h["lineup"]
            rawg_slugs = h["rawg"]
        else:
            platforms.sort(key=lambda p: order.index(p) if p in order else 99)
            title = row["name"]
            year = row["year"]
            bits = row["developers"] or row["publishers"]
            credit = " / ".join(bits[:2]) if bits else "See the RAWG record"
            our_slug = slug[:72]
            avail = avail_for[platforms[0]]
            history, lineup = history_for(title, year, platforms, row["genres"])
            rawg_slugs = [slug]
        if our_slug in used:
            continue
        used.add(our_slug)
        meta = {
            "slug": row["rawg_slug"],
            "name": row["name"],
            "released": row["released"],
            "rating": row["rating"],
            "ratings_count": row["ratings_count"],
            "genres": row["genres"],
            "developers": row["developers"],
            "publishers": row["publishers"],
            "esrb": row["esrb"],
            "platforms": row["rawg_platforms"],
            "background_image": row["background_image"],
            "screenshots": row["screenshots"],
            "page": f"https://rawg.io/games/{row['rawg_slug']}",
        }
        out.append({
            "slug": our_slug,
            "title": title,
            "year": str(year),
            "platforms": platforms,
            "credit": credit[:140],
            "rawg": rawg_slugs,
            "avail": avail,
            "history": history,
            "lineup": lineup,
            "meta": meta,
        })

    # hand entries the popularity pages did not include
    for h in hand:
        if h["slug"] in matched_hand or h["slug"] in used:
            continue
        out.append(h)
        used.add(h["slug"])

    (ROOT / "data" / "titles.json").write_text(json.dumps(out, ensure_ascii=False))
    print("TITLES", len(out), "hand-only-extra", sum(1 for x in out if "meta" not in x), "with-art", sum(1 for x in out if x.get("meta")))

if __name__ == "__main__":
    main()
