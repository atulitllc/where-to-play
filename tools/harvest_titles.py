#!/usr/bin/env python3
"""Build data/titles.json from hand-written entries plus Wikipedia list facts.
Wikipedia supplies names, years, and credits only. Prose is not copied.
"""
import json, re, unicodedata, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "WhereToPlayCatalog/1.0 (static catalog; factual lists only)"

SEEDS = {
    "NES": ["List of Nintendo Entertainment System games"],
    "SNES": ["List of Super Nintendo Entertainment System games"],
    "Nintendo 64": ["List of Nintendo 64 games"],
    "Game Boy": ["List of Game Boy games"],
    "Game Boy Color": ["List of Game Boy Color games"],
    "Game Boy Advance": ["List of Game Boy Advance games"],
    "GameCube": ["List of GameCube games"],
    "Wii": ["List of Wii games"],
    "Wii U": ["List of Wii U games"],
    "Nintendo DS": ["List of Nintendo DS games"],
    "Nintendo 3DS": ["List of Nintendo 3DS games"],
    "Nintendo Switch": ["List of Nintendo Switch games"],
}

# Attempt order: Nintendo-credited and earlier years first, then cap.
CAP = {
    "NES": 200,
    "SNES": 200,
    "Nintendo 64": 250,
    "Game Boy": 160,
    "Game Boy Color": 180,
    "Game Boy Advance": 220,
    "GameCube": 180,
    "Wii": 180,
    "Wii U": 140,
    "Nintendo DS": 220,
    "Nintendo 3DS": 200,
    "Nintendo Switch": 400,
}

NINTENDOISH = re.compile(
    r"nintendo|game freak|hal laboratory|intelligent systems|retro studios|monolith soft|"
    r"camelot|next level|good-feel|alphadream|skip ltd|sora ltd|mercury steam|creatures",
    re.I,
)

def fetch_wiki(page):
    q = urllib.parse.urlencode({"action": "parse", "page": page, "prop": "wikitext", "format": "json", "redirects": 1})
    req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as res:
        data = json.load(res)
    if "error" in data:
        raise RuntimeError(data["error"])
    return data["parse"]["wikitext"]["*"]

def clean_cell(s):
    s = re.sub(r"\{\{[Dd]ts\|(\d{4})[^}]*\}\}", r" \1 ", s)
    s = re.sub(r"\{\{#invoke:[^}]*?((?:19|20)\d{2})[^}]*\}\}", r" \1 ", s)
    s = re.sub(r"scope=[^|]*\|", " ", s)
    s = re.sub(r'id="[^"]*"', " ", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<ref[^>/]*/>", " ", s, flags=re.I)
    s = re.sub(r"<sup[^>]*>.*?</sup>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"^id=\"[^\"]*\"\|", "", s.strip())
    def link(m):
        inner = m.group(1)
        inner = inner.split("#")[0] if "#" in inner and "|" not in inner else inner
        if "|" in inner:
            # [[page|label]] last part is label; file links skip
            if inner.lower().startswith("file:") or inner.lower().startswith("image:"):
                return " "
            return inner.split("|")[-1]
        if inner.lower().startswith("file:") or inner.lower().startswith("image:"):
            return " "
        return inner
    # nested templates roughly
    for _ in range(4):
        s2 = re.sub(r"\{\{[^{}]*\}\}", " ", s)
        if s2 == s:
            break
        s = s2
    s = re.sub(r"\[\[([^[\]]+)\]\]", link, s)
    s = s.replace("''", "")
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    s = re.sub(r"\s+", " ", s).strip(" |")
    return s

def rows_of_table(table):
    # drop caption
    lines = table.split("\n")
    rows = []
    cur = []
    started = False
    for line in lines:
        if line.startswith("|-"):
            if cur:
                rows.append(cur)
            cur = []
            started = True
            continue
        if line.startswith("|}") or line.startswith("|+"):
            continue
        if line.startswith("!"):
            # header cell
            if not started and cur and not any(c.startswith("!") for c in cur):
                pass
            cur.append(line)
            continue
        if line.startswith("|"):
            cur.append(line)
    if cur:
        rows.append(cur)
    return rows

def split_cells(row_lines):
    cells = []
    buf = ""
    for line in row_lines:
        if line.startswith("!") or line.startswith("|"):
            if buf:
                cells.append(buf)
            buf = line[1:].lstrip()
            # !! or || on same line
            if line.startswith("!"):
                parts = re.split(r"(?<!\|)\|\|", line[1:])
                # header may use !!
                parts = re.split(r"!!|\|\|", line[1:])
            else:
                parts = re.split(r"(?<!\{)\|\|", line[1:])
            if len(parts) > 1:
                cells.extend(p.strip() for p in parts)
                buf = ""
        else:
            buf += " " + line
    if buf:
        cells.append(buf)
    return cells

def tables(wt):
    out = []
    for m in re.finditer(r"\{\|", wt):
        start = m.start()
        # naive end at next \n|}
        end = wt.find("\n|}", start)
        if end == -1:
            continue
        out.append(wt[start:end])
    return out

def year_of(text):
    years = [int(y) for y in re.findall(r"(19\d{2}|20\d{2})", text)]
    years = [y for y in years if 1983 <= y <= 2026]
    return min(years) if years else None

def parse_page(wt, platform):
    found = []
    for table in tables(wt):
        rs = rows_of_table(table)
        header = None
        for row in rs:
            cells_raw = split_cells(row)
            cells = [clean_cell(c) for c in cells_raw]
            if not cells:
                continue
            joined = " ".join(cells).lower()
            if header is None and "title" in joined and ("developer" in joined or "publisher" in joined or "release" in joined):
                header = [c.lower() for c in cells]
                continue
            if header is None:
                continue
            if len(cells) < 2:
                continue
            title = cells[0]
            if not title or len(title) < 2:
                continue
            if title.lower() in {"title", "tba", "unreleased"}:
                continue
            if re.fullmatch(r"[0-9a-z]([–-][0-9a-z])?", title.lower()):
                continue
            low = title.lower()
            if any(w in low for w in ("unlicensed", "homebrew", "aftermarket", "reproduction", "bootleg")):
                continue
            raw_blob = re.sub(r"<ref[^>]*>.*?</ref>", " ", " ".join(cells_raw), flags=re.S|re.I)
            year = year_of(raw_blob)
            if not year:
                continue
            dev = pub = ""
            for i, h in enumerate(header):
                if i >= len(cells):
                    break
                if "developer" in h and not dev:
                    dev = cells[i]
                elif "publisher" in h and not pub:
                    pub = cells[i]
            if not dev and len(cells) > 1:
                dev = cells[1]
            if not pub and len(cells) > 2:
                pub = cells[2]
            dev = re.sub(r"\s*/\s*", " / ", dev)[:120]
            pub = re.sub(r"\s*/\s*", " / ", pub)[:120]
            # drop footnote leftovers
            if dev.lower() in {"developer", "developer(s)"}:
                dev = ""
            found.append({"title": title, "year": year, "developer": dev, "publisher": pub, "platform": platform})
    return found

def subpages(wt, platform):
    # follow split list pages only
    if platform == "Nintendo Switch":
        pat = r"\[\[(List of Nintendo Switch games \([^|\]]+\))"
    elif platform == "Wii":
        pat = r"\[\[(List of Wii games \([^|\]]+\))"
    elif platform == "Nintendo DS":
        pat = r"\[\[(List of Nintendo DS games \([^|\]]+\))"
    elif platform == "Nintendo 3DS":
        pat = r"\[\[(List of Nintendo 3DS games \([^|\]]+\))"
    elif platform == "Game Boy":
        pat = r"\[\[(List of Game Boy games \([^|\]]+\))"
    else:
        pat = None
    if not pat:
        return []
    return list(dict.fromkeys(re.findall(pat, wt)))

def priority(g):
    credit = f"{g['developer']} {g['publisher']}"
    nin = 0 if NINTENDOISH.search(credit) else 1
    return (nin, g["year"], g["title"].lower())

def main():
    all_rows = []
    for platform, seeds in SEEDS.items():
        pages = list(seeds)
        seen_pages = set()
        collected = []
        while pages:
            page = pages.pop(0)
            if page in seen_pages:
                continue
            seen_pages.add(page)
            print("wiki", platform, page, flush=True)
            try:
                wt = fetch_wiki(page)
            except Exception as e:
                print("  fail", e)
                continue
            got = parse_page(wt, platform)
            print("  rows", len(got), flush=True)
            collected.extend(got)
            if len(got) < 40:
                for sp in subpages(wt, platform):
                    if sp not in seen_pages:
                        pages.append(sp)
        # dedupe within platform by title+year
        uniq = {}
        for g in collected:
            key = (re.sub(r"[^a-z0-9]+", "", g["title"].lower()), g["year"])
            uniq[key] = g
        rows = list(uniq.values())
        rows.sort(key=priority)
        cap = CAP[platform]
        print(platform, "unique", len(rows), "taking", min(cap, len(rows)), flush=True)
        all_rows.extend(rows[:cap])

    # hand written
    ns = {}
    exec(compile((ROOT / "data" / "titles_src.py").read_text(), "titles_src.py", "exec"), ns)
    hand = ns["G"]

    def norm_tokens(s):
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
        s = s.lower().replace("&", " and ")
        s = re.sub(r"[^a-z0-9]+", " ", s)
        stop = {"the", "of", "a", "an", "and", "for", "on"}
        return [t for t in s.split() if t not in stop]

    hand_keys = []
    for h in hand:
        hand_keys.append((set(norm_tokens(h["title"])), int(h["year"]), set(h["platforms"])))

    def dominated(title, year, platform):
        bt = set(norm_tokens(title))
        for ht, hy, hp in hand_keys:
            if abs(year - hy) > 1:
                continue
            if platform not in hp and hp:
                # still skip if titles are almost the same game even if we only listed one platform
                pass
            inter = len(bt & ht)
            if inter >= 2 and (inter >= len(bt) or inter >= len(ht) - 1):
                return True
            if bt == ht:
                return True
        return False

    bulk = []
    for g in all_rows:
        if dominated(g["title"], g["year"], g["platform"]):
            continue
        bulk.append(g)

    # merge same title across platforms when years are within 1
    merged = []
    groups = {}
    for g in bulk:
        key = " ".join(norm_tokens(g["title"]))
        groups.setdefault(key, []).append(g)
    for key, items in groups.items():
        items.sort(key=lambda x: x["year"])
        clusters = []
        for g in items:
            if not clusters or g["year"] - clusters[-1][-1]["year"] > 1:
                clusters.append([g])
            else:
                clusters[-1].append(g)
        for cluster in clusters:
            plats = []
            for g in cluster:
                if g["platform"] not in plats:
                    plats.append(g["platform"])
            # original platform first: earliest year, then generation order
            base = min(cluster, key=lambda x: x["year"])
            dev = next((g["developer"] for g in cluster if g["developer"]), "")
            pub = next((g["publisher"] for g in cluster if g["publisher"]), "")
            if dev and pub and dev.lower() != pub.lower():
                credit = f"{dev} / {pub}"
            else:
                credit = dev or pub or "See the original release"
            credit = credit[:140]
            year = base["year"]
            title = base["title"]
            # if cluster years differ, keep base year and name both platforms (same release wave)
            if len({g["year"] for g in cluster}) > 1 and max(g["year"] for g in cluster) - year >= 2:
                # should not happen because cluster split at >1
                pass
            merged.append({
                "title": title,
                "year": str(year),
                "platforms": plats,
                "credit": credit,
                "rawg_hint": title,
            })

    # slugs
    used = {h["slug"] for h in hand}
    def slugify(title):
        s = unicodedata.normalize("NFKD", title)
        s = "".join(c for c in s if not unicodedata.combining(c))
        s = s.lower().replace("&", " and ").replace("+", " plus ")
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        return s[:72] or "game"

    avail_for = {
        "NES": "nso", "SNES": "nso", "Game Boy": "nso",
        "Game Boy Color": "gbc", "Nintendo 64": "n64", "Game Boy Advance": "gba",
        "GameCube": "gc", "Wii": "legacy", "Wii U": "legacy",
        "Nintendo DS": "legacy", "Nintendo 3DS": "legacy", "Nintendo Switch": "switch",
    }
    order = list(avail_for)
    out = list(hand)
    for g in merged:
        base = slugify(g["title"])
        slug = base
        if slug in used:
            slug = f"{base}-{g['year']}"
        if slug in used:
            slug = f"{base}-{g['year']}-{slugify(g['platforms'][0])}"
        if slug in used:
            continue
        used.add(slug)
        primary = sorted(g["platforms"], key=lambda p: order.index(p))[0]
        # prefer earliest-generation platform as primary for breadcrumb
        title = g["title"]
        # if slug carries a year because of a collision, put the year in the visible name when another entry shares the base name
        if slug != base and f"({g['year']})" not in title and str(g["year"]) not in title:
            title = f"{title} ({g['year']})"
        plat_phrase = " and ".join(g["platforms"])
        credit = g["credit"]
        from unique_histories import make_history_lineup
        history, lineup = make_history_lineup({
            "slug": slug,
            "title": title,
            "year": g["year"],
            "platforms": g["platforms"],
            "credit": credit,
            "meta": {"genres": [], "developers": [], "publishers": []},
        })
        rawg = [base]
        if slugify(title) != base:
            rawg.append(slugify(title))
        rawg.append(f"{base}-{g['year']}")
        # de-dup rawg candidates
        seen = set()
        rawg2 = []
        for r in rawg:
            if r and r not in seen:
                seen.add(r)
                rawg2.append(r)
        out.append({
            "slug": slug,
            "title": title,
            "year": g["year"],
            "platforms": g["platforms"],
            "credit": credit,
            "rawg": rawg2[:3],
            "avail": avail_for[primary],
            "history": history,
            "lineup": lineup,
        })

    # final dedupe slugs
    slugs = [x["slug"] for x in out]
    assert len(slugs) == len(set(slugs))
    (ROOT / "data" / "titles.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    from collections import Counter
    c = Counter(p for x in out for p in x["platforms"])
    print("TOTAL", len(out), "hand", len(hand), "bulk", len(out)-len(hand))
    print(dict(c))

if __name__ == "__main__":
    main()
