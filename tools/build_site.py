#!/usr/bin/env python3
"""Build the static Where to Play catalog. Original prose only. RAWG images and metadata."""
import html as html_lib
import json
import os
import re
import unicodedata
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "titles.json"
CACHE = ROOT / ".cache" / "rawg"
COVERS = ROOT / "images" / "covers"
SHOTS = ROOT / "images" / "in-game"
GAMES = ROOT / "games"
PLATS = ROOT / "platforms"

NSO = "https://www.nintendo.com/us/online/nintendo-switch-online/"
NIN = "https://www.nintendo.com/"
UA = "WhereToPlayCatalog/1.0 (static catalog; attribution https://rawg.io)"

SYSTEMS = [
    ("NES", "nes", "3rd generation", "8-bit home console"),
    ("SNES", "snes", "4th generation", "16-bit home console"),
    ("Nintendo 64", "nintendo-64", "5th generation", "3D home console"),
    ("Game Boy", "game-boy", "4th generation", "8-bit handheld"),
    ("Game Boy Color", "game-boy-color", "5th generation", "color handheld"),
    ("Game Boy Advance", "game-boy-advance", "6th generation", "32-bit handheld"),
    ("GameCube", "gamecube", "6th generation", "disc home console"),
    ("Wii", "wii", "7th generation", "motion home console"),
    ("Wii U", "wii-u", "8th generation", "HD home console"),
    ("Nintendo DS", "nintendo-ds", "7th generation", "dual-screen handheld"),
    ("Nintendo 3DS", "nintendo-3ds", "8th generation", "3D handheld"),
    ("Nintendo Switch", "nintendo-switch", "9th generation", "hybrid console"),
]
SYS_BY_NAME = {a: {"slug": b, "era": c, "kind": d} for a, b, c, d in SYSTEMS}

PLATFORM_INTRO = {
    "nes": "The Nintendo Entertainment System lineup in this catalog, from the mid-1980s 8-bit years. The usual official option now is Nintendo Switch Online's classics library. Confirm each title is still in the current library. Where to Play does not host these games.",
    "snes": "Super Nintendo games: 16-bit platformers, racers, and role-playing games. Nintendo Switch Online has carried a Super NES classics library. Confirm a title is still included before you count on it. Where to Play does not host these games.",
    "nintendo-64": "Nintendo 64 games from the first 3D home generation. Nintendo Switch Online has carried this library, often on a higher tier. Confirm the title is still in the current library. Where to Play does not host these games.",
    "game-boy": "Game Boy originals, the gray-brick handheld line. Nintendo Switch Online's classics library has included Game Boy games. Confirm the title is still listed. Where to Play does not host these games.",
    "game-boy-color": "Game Boy Color games, the color handheld follow-up to Game Boy. Some of these titles have appeared on Nintendo Switch Online. Confirm the current library with Nintendo. Where to Play does not host these games.",
    "game-boy-advance": "Game Boy Advance games from the early 2000s. Nintendo Switch Online has carried a Game Boy Advance library, often on a higher tier. Confirm the title is still included. Where to Play does not host these games.",
    "gamecube": "GameCube discs from Nintendo's sixth-generation home console. Nintendo has described a GameCube classics library on a higher membership tier. This page does not claim each title is in it. Where to Play does not host these games.",
    "wii": "Wii games, including motion-controlled hits and traditional pad games. This page records the Wii originals. It does not claim a current listing unless a later official re-release is named as history. Where to Play does not host these games.",
    "wii-u": "Wii U games from Nintendo's HD home console before Switch. The Wii U catalog itself is not treated here as a current way to get a game. Later ports are named as history. Where to Play does not host these games.",
    "nintendo-ds": "Nintendo DS games: dual screens, touch controls, and a huge first-party and third-party library. That system's digital catalog is closed. Confirm any later official re-release with Nintendo. Where to Play does not host these games.",
    "nintendo-3ds": "Nintendo 3DS games, including stereoscopic 3D titles and late handheld RPGs. Nintendo no longer runs that system's digital catalog. Confirm any later official re-release with Nintendo. Where to Play does not host these games.",
    "nintendo-switch": "Nintendo Switch games in this catalog, from launch onward. The official option is Nintendo's own listing, including the Nintendo eShop when the title is still offered. Where to Play does not host these games.",
}

PLATFORM_META = {
    "nes": "NES games and the official option: Nintendo Switch Online's classics library, when a title is still included. Where to Play does not host these games.",
    "snes": "SNES games and the official option: Nintendo Switch Online's Super NES classics, when a title is still included. Where to Play does not host these games.",
    "nintendo-64": "Nintendo 64 games and the official option: Nintendo Switch Online, often on a higher tier. Confirm the current library. Where to Play does not host these games.",
    "game-boy": "Game Boy games and the official option: Nintendo Switch Online's classics library, when a title is still included. Where to Play does not host these games.",
    "game-boy-color": "Game Boy Color games. Some have appeared on Nintendo Switch Online. Confirm the current library. Where to Play does not host these games.",
    "game-boy-advance": "Game Boy Advance games and the official option: Nintendo Switch Online, often on a higher tier. Confirm the current library. Where to Play does not host these games.",
    "gamecube": "GameCube games. Nintendo has described a classics library on a higher tier; this page does not claim each title is in it. Where to Play does not host these games.",
    "wii": "Wii games in this catalog, with official re-releases named only as history. Confirm anything current with Nintendo. Where to Play does not host these games.",
    "wii-u": "Wii U games in this catalog. Later official ports are history, not a promise of a current listing. Where to Play does not host these games.",
    "nintendo-ds": "Nintendo DS games. That digital catalog is closed. Confirm any official re-release with Nintendo. Where to Play does not host these games.",
    "nintendo-3ds": "Nintendo 3DS games. That digital catalog is closed. Confirm any official re-release with Nintendo. Where to Play does not host these games.",
    "nintendo-switch": "Nintendo Switch games and the official option: Nintendo's own listing, including the Nintendo eShop when still offered. Where to Play does not host these games.",
}

AVAIL = {
    "nso": (
        "Switch Online",
        "nso",
        "Official option",
        "Nintendo Switch Online classics",
        "Nintendo publishes a classics library for this era on Nintendo Switch Online. Confirm this title is still in the current library. Where to Play does not host this game.",
        NSO,
        "Nintendo Switch Online overview",
    ),
    "gbc": (
        "Switch Online",
        "nso",
        "Official option",
        "Nintendo Switch Online, if still listed",
        "Some Game Boy Color games have been part of Nintendo Switch Online. Confirm this title is still in the current library. Where to Play does not host this game.",
        NSO,
        "Nintendo Switch Online overview",
    ),
    "n64": (
        "Switch Online",
        "nso",
        "Official option",
        "Nintendo Switch Online, often a higher tier",
        "Nintendo Switch Online has carried Nintendo 64 games, often on a higher tier. Confirm this title is still in the current library. Where to Play does not host this game.",
        NSO,
        "Nintendo Switch Online overview",
    ),
    "gba": (
        "Switch Online",
        "nso",
        "Official option",
        "Nintendo Switch Online, often a higher tier",
        "Nintendo Switch Online has carried Game Boy Advance games, often on a higher tier. Confirm this title is still in the current library. Where to Play does not host this game.",
        NSO,
        "Nintendo Switch Online overview",
    ),
    "gc": (
        "Confirm with Nintendo",
        "check",
        "Official option",
        "Confirm with Nintendo",
        "Nintendo has described a GameCube classics library on a higher Nintendo Switch Online tier, including for newer hardware. This page does not claim this title is in that library. Where to Play does not host this game.",
        NSO,
        "Nintendo Switch Online overview",
    ),
    "legacy": (
        "Confirm with Nintendo",
        "check",
        "Official option",
        "Confirm any re-release with Nintendo",
        "No current listing is claimed here. This entry records the original hardware release. Confirm any official re-release on Nintendo's website. Where to Play does not host this game.",
        NIN,
        "Nintendo's website",
    ),
    "switch": (
        "On Switch",
        "sw",
        "Official option",
        "Nintendo Switch",
        "The official option is a Nintendo Switch listing, including the Nintendo eShop when Nintendo still offers it. Confirm the current listing on Nintendo's website. Where to Play does not host this game.",
        NIN,
        "Nintendo's website",
    ),
}

# Titles Nintendo's own Switch Online overview has cited as classics (project note, 3 Oct 2026).
CITED = {
    "super-mario-bros-3": "Nintendo's Switch Online overview has cited Super Mario Bros. 3 among classics. Confirm it is still in the current library.",
    "donkey-kong-country": "Nintendo's Switch Online overview has cited Donkey Kong Country among classics. Confirm it is still in the current library.",
    "links-awakening": "Nintendo's Switch Online overview has cited Link's Awakening among classics. Confirm it is still in the current library.",
}

BRAND_SVG = """<svg class="brand-mark" width="40" height="36" viewBox="0 0 80 72" aria-hidden="true">
  <defs>
    <radialGradient id="wtpScreen" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#E9FFC8"/>
      <stop offset="28%" stop-color="#7DFF6A"/>
      <stop offset="58%" stop-color="#1FCB62"/>
      <stop offset="100%" stop-color="#0B3D28"/>
    </radialGradient>
  </defs>
  <path fill="#243038" stroke="#3C4A52" stroke-width="1" d="M20 3h40c8.8 0 16 7.2 16 16v22c0 9.2-5.4 16.2-13.2 20.2-4.2 2.2-9.2 3.6-14.8 4.2-2.6.3-5.4.6-8 .6s-5.4-.3-8-.6c-5.6-.6-10.6-2-14.8-4.2C9.4 57.2 4 50.2 4 41V19C4 10.2 11.2 3 20 3z"/>
  <path fill="#12181C" d="M16 10h48c2.2 0 4 1.8 4 4v22c0 2.2-1.8 4-4 4H16c-2.2 0-4-1.8-4-4V14c0-2.2 1.8-4 4-4z"/>
  <rect x="16" y="10" width="48" height="30" rx="4" fill="url(#wtpScreen)"/>
  <path fill="#F4FFE8" d="M35.2 17.2l14.2 7.8-14.2 7.8z"/>
  <g stroke="#5EEA8A" stroke-width="1.7" stroke-linecap="round">
    <path d="M10.2 16v3.4M10.2 21.6v3.4M10.2 27.2v3.4"/>
    <path d="M69.8 16v3.4M69.8 21.6v3.4M69.8 27.2v3.4"/>
  </g>
  <rect x="34.6" y="42.4" width="10.8" height="2.4" rx="1.2" fill="#0E1518"/>
  <g fill="#3DDC78">
    <rect x="15" y="49" width="14.4" height="4" rx="1.2"/>
    <rect x="20.2" y="43.8" width="4" height="14.4" rx="1.2"/>
    <circle cx="54.2" cy="51" r="3.5"/>
    <circle cx="63.4" cy="51" r="3.5"/>
  </g>
</svg>"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&amp;family=Oxanium:wght@500;600&amp;display=swap" rel="stylesheet">
<script>
try{var t=localStorage.getItem("wtp-theme");if(t!=="light"&&t!=="dark"){t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";}document.documentElement.setAttribute("data-theme",t);}catch(e){document.documentElement.setAttribute("data-theme","dark");}
</script>"""

BANNED = re.compile(r"download|\bROMs?\b|\bemulators?\b|\bISO\b|free play", re.I)


def esc(s):
    return html_lib.escape(s or "", quote=True)


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    stop = {"the", "of", "a", "an", "and", "for", "on", "in", "to", "edition"}
    return [t for t in s.split() if t not in stop]


def names_match(wanted, got):
    w, g = norm(wanted), norm(got)
    if not w or not g:
        return False
    if w == g:
        return True
    extra_bad = {"deluxe", "hd", "remastered", "remake", "remaster", "dx", "3d"}
    wset, gset = set(w), set(g)
    if extra_bad & gset - wset:
        return False
    if all(t in gset for t in wset):
        return True
    inter = len(wset & gset)
    return inter / max(len(wset), 1) >= 0.75 and w[0] == g[0]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=18) as res:
        final = res.geturl()
        body = res.read()
        code = res.status
    return code, final, body


def parse_rawg(body, slug_hint):
    text = body.decode("utf-8", "replace")
    m = re.search(r"window\.CLIENT_PARAMS = (\{.*?)</script>", text, re.S)
    if not m:
        raise ValueError("no CLIENT_PARAMS")
    data = json.loads(m.group(1))
    state = data["initialState"]
    games = state["entities"]["games"]
    final_slug = slug_hint
    g = games.get(f"g-{slug_hint}")
    if not g:
        # pick entity whose slug equals hint or the longest matching name later
        cands = [v for v in games.values() if isinstance(v, dict) and v.get("slug") == slug_hint]
        g = cands[0] if cands else None
    if not g:
        raise ValueError("game entity missing")
    shots = []
    sh = (state.get("game") or {}).get("screenshots") or {}
    for row in sh.get("results") or []:
        if row.get("is_deleted"):
            continue
        img = row.get("image")
        if img and "media.rawg.io" in img and "/screenshots/" in img:
            shots.append({"url": img, "width": row.get("width") or 0, "height": row.get("height") or 0})
    shots.sort(key=lambda r: (0 if r["width"] >= 480 else 1, -r["width"]))
    def names(key):
        out = []
        for item in g.get(key) or []:
            if isinstance(item, dict) and item.get("name"):
                out.append(item["name"])
        return out
    plats = []
    for p in g.get("platforms") or []:
        if isinstance(p, dict):
            inner = p.get("platform")
            if isinstance(inner, dict) and inner.get("name"):
                plats.append(inner["name"])
            elif p.get("name"):
                plats.append(p["name"])
        elif isinstance(p, str):
            plats.append(p)
    esrb = g.get("esrb_rating") or {}
    return {
        "slug": g.get("slug"),
        "name": g.get("name"),
        "released": g.get("released"),
        "rating": g.get("rating"),
        "ratings_count": g.get("ratings_count") or 0,
        "genres": names("genres"),
        "developers": names("developers"),
        "publishers": names("publishers"),
        "esrb": esrb.get("name") if isinstance(esrb, dict) else None,
        "platforms": plats,
        "background_image": g.get("background_image"),
        "screenshots": shots[:3],
        "page": f"https://rawg.io/games/{g.get('slug')}",
    }


def load_meta(rawg_slug):
    CACHE.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-z0-9-]+", "-", rawg_slug.lower())
    path = CACHE / f"{safe}.json"
    if path.exists():
        data = json.loads(path.read_text())
        if data.get("_error"):
            raise ValueError(data["_error"])
        return data
    try:
        code, final, body = fetch(f"https://rawg.io/games/{rawg_slug}")
        final_slug = final.rstrip("/").split("/")[-1]
        meta = parse_rawg(body, final_slug if final_slug else rawg_slug)
        if "arcade-archives" in (meta.get("slug") or "") or "arcade-archives" in final:
            raise ValueError("arcade archives redirect")
        if not meta.get("background_image"):
            raise ValueError("no background_image")
        path.write_text(json.dumps(meta))
        return meta
    except Exception as e:
        path.write_text(json.dumps({"_error": str(e)[:300]}))
        raise


def save_image(url, dest: Path, max_side):
    if dest.exists() and dest.stat().st_size > 1000:
        return
    code, final, body = fetch(url)
    im = Image.open(BytesIO(body))
    im = im.convert("RGB")
    im.thumbnail((max_side, max_side))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=68, optimize=True)


def find_cover(slug):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = COVERS / f"{slug}{ext}"
        if p.exists() and p.stat().st_size > 500:
            return p.name
    return None


def header(prefix, about_current=False):
    about = f'{prefix}about/'
    cur = ' aria-current="page"' if about_current else ""
    return f"""<a class="skip" href="#content">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{prefix}">
      {BRAND_SVG}
      <span>
        <span class="brand-name">Where <span class="brand-to">to</span> Play</span>
        <span class="brand-sub">Nintendo catalog</span>
      </span>
    </a>
    <nav class="nav"><button type="button" id="theme-toggle" class="theme-toggle" aria-pressed="true">Light mode</button><a href="{about}"{cur}>About</a></nav>
  </div>
</header>"""


def footer(prefix):
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p><strong>Where to Play.</strong> Nothing here is for sale. We don't host this catalog's games.</p>
    <p>Powered by <a href="https://rawg.io" target="_blank" rel="noopener noreferrer">RAWG</a>. Cover images and RAWG facts are RAWG's, used with attribution. <a href="https://rawg.io" target="_blank" rel="noopener noreferrer">rawg.io</a></p>
    <p>Game names are trademarks of their owners. This site is not affiliated with Nintendo.</p>
    <p>Official options point at Nintendo when a public page is known. Confirm a title is still offered. <a href="{NIN}" target="_blank" rel="noopener noreferrer">Nintendo's website</a>.</p>
  </div>
</footer>
<script src="{prefix}js/theme.js"></script>"""


def head(prefix, title, desc, css="css/site.css"):
    # css path is passed explicitly
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<link rel="canonical" href="./">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#110f0c">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{css}">
</head>
<body>
"""


def schema_tag(obj):
    blob = json.dumps(obj, ensure_ascii=False)
    blob = blob.replace("<", "\\u003c")
    return f'<script type="application/ld+json">{blob}</script>'


def first_sentence(text):
    text = re.sub(r"\s+", " ", text).strip()
    # Keep "Bros." and similar abbreviations inside the sentence. Card blurbs
    # and meta descriptions use this cut.
    from unique_histories import split_sentences
    parts = split_sentences(text)
    return parts[0] if parts else text


def cover_html(src, title, rawg_page, mini=True):
    block = f"""<div class="cover">
  <img class="cover-blur" src="{esc(src)}" alt="" aria-hidden="true">
  <img class="cover-main" src="{esc(src)}" alt="{esc(title)} image from RAWG">
</div>"""
    credit = f'<p class="rawg-mini">Image from <a href="{esc(rawg_page)}" target="_blank" rel="noopener noreferrer">RAWG</a></p>' if mini else ""
    return block, credit


def card(g, prefix):
    src = f"{prefix}images/covers/{g['cover']}"
    plats = " and ".join(g["platforms"])
    hay = " ".join([
        g["title"], g["year"], plats, g["credit"], g["history"], g["lineup"],
        " ".join(g["meta"].get("genres") or []),
        SYS_BY_NAME[g["platforms"][0]]["era"],
    ])
    also = "|".join(g["platforms"][1:])
    badge, kind = AVAIL[g["avail"]][0], AVAIL[g["avail"]][1]
    block, _ = cover_html(src, g["title"], g["meta"]["page"], mini=False)
    blurb = first_sentence(g["history"])
    return f"""<article class="card" data-system="{esc(g['platforms'][0])}" data-also="{esc(also)}" data-hay="{esc(hay)}">
  <a class="card-link" href="{prefix}games/{g['slug']}/">
    {block}
    <h2>{esc(g['title'])}</h2>
    <p class="meta">{esc(g['year'])} · {esc(plats)}</p>
    <p class="blurb">{esc(blurb)}</p>
    <div class="badge-row"><span class="badge badge-{kind}">{esc(badge)}</span><span class="badge badge-check">{esc(SYS_BY_NAME[g['platforms'][0]]['era'])}</span></div>
  </a>
  <p class="rawg-mini">Image from <a href="{esc(g['meta']['page'])}" target="_blank" rel="noopener noreferrer">RAWG</a></p>
</article>"""


def crumbs(items):
    lis = []
    for i, (name, href) in enumerate(items):
        if href and i < len(items) - 1:
            lis.append(f'<li><a href="{esc(href)}">{esc(name)}</a></li>')
        else:
            lis.append(f'<li>{esc(name)}</li>')
    return '<ol class="crumbs">' + "".join(lis) + "</ol>"


def breadcrumb_schema(items):
    els = []
    for i, (name, href) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": name}
        if href and i < len(items):
            el["item"] = href
        els.append(el)
    return {"@type": "BreadcrumbList", "itemListElement": els}


def item_list(games, prefix):
    els = []
    for i, g in enumerate(games, 1):
        els.append({
            "@type": "ListItem",
            "position": i,
            "name": g["title"],
            "url": f"{prefix}games/{g['slug']}/",
        })
    return {"@type": "ItemList", "itemListElement": els}



FRANCHISES = [
    ("Paper Mario", ("paper mario",)),
    ("Mario Kart", ("mario kart",)),
    ("Mario Party", ("mario party",)),
    ("Mario Golf", ("mario golf",)),
    ("Mario Tennis", ("mario tennis",)),
    ("Dr. Mario", ("dr mario", "dr. mario")),
    ("Captain Toad", ("captain toad",)),
    ("Luigi's Mansion", ("luigi s mansion", "luigis mansion")),
    ("WarioWare", ("warioware", "wario ware")),
    ("Wario", ("wario",)),
    ("Yoshi", ("yoshi",)),
    ("Super Smash Bros.", ("smash bros", "super smash")),
    ("Donkey Kong", ("donkey kong", "diddy kong")),
    ("The Legend of Zelda", ("zelda", "link s awakening", "links awakening")),
    ("Pokemon", ("pokemon",)),
    ("Metroid", ("metroid",)),
    ("Kirby", ("kirby",)),
    ("Animal Crossing", ("animal crossing",)),
    ("Fire Emblem", ("fire emblem",)),
    ("Star Fox", ("star fox", "starfox")),
    ("F-Zero", ("f-zero", "f zero")),
    ("Pikmin", ("pikmin",)),
    ("Splatoon", ("splatoon",)),
    ("Xenoblade", ("xenoblade",)),
    ("Mother", ("earthbound", "mother 3", "mother 2")),
    ("Castlevania", ("castlevania",)),
    ("Mega Man", ("mega man", "megaman")),
    ("Final Fantasy", ("final fantasy",)),
    ("Dragon Quest", ("dragon quest", "dragon warrior")),
    ("Advance Wars", ("advance wars",)),
    ("Golden Sun", ("golden sun",)),
    ("Harvest Moon", ("harvest moon", "story of seasons", "rune factory")),
    ("Punch-Out!!", ("punch-out", "punch out")),
    ("Pilotwings", ("pilotwings", "pilot wings")),
    ("Kid Icarus", ("kid icarus",)),
    ("Sonic", ("sonic the hedgehog", "sonic")),
    ("Tetris", ("tetris",)),
    ("Bomberman", ("bomberman",)),
    ("Contra", ("contra", "probotector")),
    ("Ninja Gaiden", ("ninja gaiden",)),
    ("Street Fighter", ("street fighter",)),
    ("Resident Evil", ("resident evil",)),
    ("Monster Hunter", ("monster hunter",)),
    ("Professor Layton", ("professor layton",)),
    ("Ace Attorney", ("ace attorney", "phoenix wright")),
    ("Metal Gear", ("metal gear",)),
    ("Kingdom Hearts", ("kingdom hearts",)),
    ("Persona", ("persona",)),
    ("Shin Megami Tensei", ("shin megami", "devil survivor")),
    ("Star Wars", ("star wars",)),
    ("Batman", ("batman",)),
    ("LEGO", ("lego",)),
    ("Minecraft", ("minecraft",)),
    ("Pac-Man", ("pac-man", "pac man")),
    ("Crash Bandicoot", ("crash bandicoot", "crash ")),
    ("Spyro", ("spyro",)),
    ("Rayman", ("rayman",)),
    ("Shantae", ("shantae",)),
    ("Breath of Fire", ("breath of fire",)),
    ("Chrono", ("chrono trigger", "chrono cross")),
    ("Mana", ("secret of mana", "trials of mana", "legend of mana", "sword of mana", "children of mana")),
    ("Tales", ("tales of",)),
    ("Disgaea", ("disgaea",)),
    ("Atelier", ("atelier",)),
    ("Bravely", ("bravely",)),
    ("Etrian Odyssey", ("etrian odyssey",)),
    ("Yo-kai Watch", ("yo-kai watch", "yokai watch")),
    ("Inazuma Eleven", ("inazuma eleven",)),
    ("Cooking Mama", ("cooking mama",)),
    ("Nintendogs", ("nintendogs",)),
    ("Brain Age", ("brain age",)),
    ("Rhythm Heaven", ("rhythm heaven", "rhythm paradise")),
    ("Wii Sports", ("wii sports",)),
    ("Wii Fit", ("wii fit",)),
    ("Big Brain Academy", ("big brain academy",)),
    ("Famicom Detective Club", ("famicom detective",)),
    ("Danganronpa", ("danganronpa",)),
    ("The World Ends with You", ("the world ends with you",)),
    ("Custom Robo", ("custom robo",)),
    ("Chibi-Robo", ("chibi-robo", "chibi robo")),
    ("Ganbare Goemon", ("goemon", "mystical ninja")),
    ("Gradius", ("gradius",)),
    ("Ice Climber", ("ice climber",)),
    ("Balloon Fight", ("balloon fight",)),
    ("Excite", ("excitebike", "excite truck", "excitebots")),
    ("Wave Race", ("wave race",)),
    ("Mario", ("mario",)),
]

PARENT = {
    "Paper Mario": "Mario",
    "Mario Kart": "Mario",
    "Mario Party": "Mario",
    "Mario Golf": "Mario",
    "Mario Tennis": "Mario",
    "Dr. Mario": "Mario",
    "Captain Toad": "Mario",
    "Luigi's Mansion": "Mario",
    "WarioWare": "Wario",
    "Wario": "Mario",
    "Yoshi": "Mario",
    "Super Smash Bros.": "Nintendo crossover",
}

HARDWARE = {
    "NES": "The NES is Nintendo's 8-bit home console, the Famicom in Japan. Games shipped on cartridges, and the library set the pattern for side-scrolling platformers.",
    "SNES": "The Super Nintendo is the 16-bit home console that followed, with a deeper color range and a library of platformers, racers, and role-playing games.",
    "Nintendo 64": "Nintendo 64 is the first 3D home console in this catalog. Games used cartridges, and a lot of the library is built around analog-stick movement.",
    "Game Boy": "Game Boy is the gray-brick handheld. Games are small cartridges meant for short sessions away from a television.",
    "Game Boy Color": "Game Boy Color is the color follow-up to Game Boy. It plays many older Game Boy cartridges and adds color-native games.",
    "Game Boy Advance": "Game Boy Advance is the widescreen handheld of the early 2000s, still on cartridges, with a library that sits between SNES-style games and later dual-screen designs.",
    "GameCube": "GameCube is Nintendo's disc home console of the sixth generation. This page records the disc release, not a later reissue.",
    "Wii": "Wii is the motion-control home console. Some games use the remote, and some are ordinary pad games that happen to be on that hardware.",
    "Wii U": "Wii U is the HD home console before Switch, with a tablet-style GamePad. Its own digital catalog is not treated here as a current way to get a game.",
    "Nintendo DS": "Nintendo DS is the dual-screen handheld. Touch and the second screen are part of how many of these games are built.",
    "Nintendo 3DS": "Nintendo 3DS is the later dual-screen handheld, including stereoscopic 3D on titles that use it. Nintendo no longer runs that system's digital catalog.",
    "Nintendo Switch": "Nintendo Switch is the hybrid console, played on a television or as a handheld. Current official listings, when they exist, are Nintendo's own.",
}

LAUNCH = {"NES":1983,"SNES":1990,"Nintendo 64":1996,"Game Boy":1989,"Game Boy Color":1998,"Game Boy Advance":2001,"GameCube":2001,"Wii":2006,"Wii U":2012,"Nintendo DS":2004,"Nintendo 3DS":2011,"Nintendo Switch":2017}

def franchise_of(title):
    n = " ".join(norm(title))
    for name, keys in FRANCHISES:
        if any(k in n for k in keys):
            return name
    return None

def _dev_key(g):
    devs = (g.get("meta") or {}).get("developers") or []
    if not devs:
        return None
    return devs[0].strip().lower()

def attach_related(games):
    by_fr = {}
    by_broad = {}
    by_sys = {}
    by_dev = {}
    for g in games:
        g["franchise"] = franchise_of(g["title"])
        g["broad"] = PARENT.get(g["franchise"]) if g["franchise"] else None
        by_fr.setdefault(g["franchise"], []).append(g)
        broad_key = g["broad"] or g["franchise"]
        if broad_key:
            by_broad.setdefault(broad_key, []).append(g)
        for p in g["platforms"]:
            by_sys.setdefault(p, []).append(g)
        dk = _dev_key(g)
        if dk:
            by_dev.setdefault(dk, []).append(g)
    for g in games:
        series = []
        if g["franchise"]:
            pool = [o for o in by_fr[g["franchise"]] if o["slug"] != g["slug"]]
            pool.sort(key=lambda o: (int(o["year"]), o["title"].lower()))
            series = pool[:18]
            g["series_more"] = max(0, len(pool) - len(series))
        else:
            g["series_more"] = 0
        used = {o["slug"] for o in series}
        used.add(g["slug"])
        broad_key = g["broad"] or g["franchise"]
        fr = []
        if broad_key:
            pool = [o for o in by_broad.get(broad_key, []) if o["slug"] not in used]
            # Child page (Mario Kart) also links the parent series (Mario).
            if g.get("broad"):
                for o in by_fr.get(g["broad"], []):
                    if o["slug"] not in used:
                        pool.append(o)
            # Parent page (Mario) already shares broad_key with its spin-offs.
            if g["franchise"] and not g["broad"]:
                for o in by_broad.get(g["franchise"], []):
                    if o["slug"] not in used:
                        pool.append(o)
            seen = set()
            uniq = []
            for o in pool:
                if o["slug"] in seen or o["slug"] == g["slug"]:
                    continue
                seen.add(o["slug"])
                uniq.append(o)
            uniq.sort(key=lambda o: (int(o["year"]), o["title"].lower()))
            fr = uniq[:18]
            g["franchise_more"] = max(0, len(uniq) - len(fr))
        else:
            g["franchise_more"] = 0
        used.update(o["slug"] for o in fr)
        plat_pool = []
        for p in g["platforms"]:
            for o in by_sys.get(p, []):
                if o["slug"] in used:
                    continue
                if g["franchise"] and o.get("franchise") == g["franchise"]:
                    continue
                plat_pool.append(o)
        plat_pool.sort(key=lambda o: (abs(int(o["year"]) - int(g["year"])), o["title"].lower()))
        plat = []
        seen = set()
        for o in plat_pool:
            if o["slug"] in seen:
                continue
            seen.add(o["slug"])
            plat.append(o)
            if len(plat) == 12:
                break
        used.update(o["slug"] for o in plat)
        dev = []
        dk = _dev_key(g)
        if dk:
            pool = [o for o in by_dev.get(dk, []) if o["slug"] not in used]
            pool.sort(key=lambda o: (abs(int(o["year"]) - int(g["year"])), o["title"].lower()))
            dev = pool[:8]
        g["rel_series"] = series
        g["rel_franchise"] = fr
        g["rel_platform"] = plat
        g["rel_dev"] = dev

def link_list(games, prefix, empty="None in this catalog yet."):
    if not games:
        return f'<p class="credit-line">{esc(empty)}</p>'
    items = []
    for o in games:
        plats = " / ".join(o["platforms"])
        items.append(
            f'<li><a href="{prefix}games/{esc(o["slug"])}/">{esc(o["title"])}</a>'
            f' <span>{esc(o["year"])} · {esc(plats)}</span></li>'
        )
    return '<ul class="rel-list">' + "".join(items) + "</ul>"

def _game_link(prefix, o):
    return f'<a href="{prefix}games/{esc(o["slug"])}/">{esc(o["title"])}</a>'

def extra_history(g):
    """Shared legal and RAWG paragraphs are not part of the history block."""
    return []
    prefix = "../../"
    primary = g["platforms"][0]
    info = SYS_BY_NAME[primary]
    raw = g.get("meta") or {}
    bits = []
    bits.append(
        f"{esc(g['title'])} is recorded here as a {esc(str(g['year']))} game. "
        f"The lead system is {esc(primary)}, {esc(info['era'])}, {esc(info['kind'])}. {esc(HARDWARE[primary])} "
        f"Every other {esc(primary)} game in this catalog is on the "
        f'<a href="{prefix}platforms/{esc(info["slug"])}/">{esc(primary)} page</a>.'
    )
    others = g["platforms"][1:]
    if others:
        links = []
        for name in others:
            inf = SYS_BY_NAME[name]
            links.append(f'<a href="{prefix}platforms/{esc(inf["slug"])}/">{esc(name)}</a>')
        bits.append(
            "This is one page for the same game on more than one Nintendo system. Also named here: "
            + " and ".join(links)
            + ". A remake, or a release that is a different work, gets its own page. The year goes in the name when two slugs would otherwise collide."
        )
    else:
        bits.append(
            f"This slug names {esc(primary)} only. RAWG sometimes tags the same record on other hardware. Those tags are not copied here unless this catalog treats them as the same Nintendo release."
        )
    devs = raw.get("developers") or []
    pubs = raw.get("publishers") or []
    if g["credit"] == "See the RAWG record" and (devs or pubs):
        credit_sentence = "The credit chip is taken from the RAWG card, because this entry does not have a shorter studio line written by hand."
    else:
        credit_sentence = f"The credit chip on this page reads {esc(g['credit'])}."
    who = []
    who.append("developer " + esc(", ".join(devs)) if devs else "no developer name")
    who.append("publisher " + esc(", ".join(pubs)) if pubs else "no publisher name")
    bits.append(
        credit_sentence
        + " RAWG lists "
        + " and ".join(who)
        + ". If those names disagree with the chip, both stay on the page so the record can be checked."
    )
    genres = raw.get("genres") or []
    if genres:
        bits.append(
            "RAWG's genre labels for this record are "
            + esc(", ".join(genres))
            + ". They are a filing aid, not a review written for this page, and not a description of how the game feels in your hands."
        )
    else:
        bits.append("RAWG does not list genres on this record. The page does not invent any.")
    parts = []
    if raw.get("released"):
        parts.append(f"the date field is {esc(str(raw['released']))}")
    rating = raw.get("rating")
    if isinstance(rating, (int, float)):
        count = int(raw.get("ratings_count") or 0)
        parts.append(f"the user rating is {rating:.2f} out of 5 from {count} ratings")
    if raw.get("esrb"):
        parts.append(f"the ESRB label on the card is {esc(str(raw['esrb']))}")
    if parts:
        sentence = "; ".join(parts)
        sentence = sentence[0].upper() + sentence[1:]
        bits.append(sentence + ". Those fields belong to RAWG. This page does not add a score of its own.")
    if g.get("franchise"):
        sib = g.get("rel_series") or []
        if sib:
            years = [int(o["year"]) for o in sib] + [int(g["year"])]
            names = ", ".join(_game_link(prefix, o) for o in sib[:5])
            more = g.get("series_more") or 0
            tail = f" {more} more {esc(g['franchise'])} pages exist here beyond the list." if more else ""
            bits.append(
                f"Series context: this title belongs with {esc(g['franchise'])}. "
                f"Other {esc(g['franchise'])} pages in the catalog run from {min(years)} to {max(years)}, including {names}.{tail}"
            )
        else:
            bits.append(
                f"Series context: this title belongs with {esc(g['franchise'])}. No other {esc(g['franchise'])} entry is in the catalog yet."
            )
        if g.get("broad"):
            bits.append(
                f"The wider family in this catalog is {esc(g['broad'])}. "
                f"Those pages are linked under Same franchise, separate from the tighter {esc(g['franchise'])} list."
            )
        else:
            bits.append(
                f"In this catalog, {esc(g['franchise'])} is the family name. "
                "Same franchise lists spin-offs filed under their own heading, plus any further entries that did not fit the series list."
            )
    else:
        bits.append(
            f"{esc(g['title'])} is not grouped under one of the series names this catalog matches by title. "
            f"The related links then point at other {esc(primary)} games from nearby years, and at games that share the first RAWG developer when one is listed."
        )
    raw_plats = raw.get("platforms") or []
    if raw_plats:
        bits.append(
            "RAWG's own platform list for this record is "
            + esc(", ".join(raw_plats))
            + ". This catalog keeps only the Nintendo systems named above. A personal computer, or another company's console, on that list is not a claim that this page covers that version."
        )
    y = int(g["year"])
    launch = min(LAUNCH.get(p, 1983) for p in g["platforms"])
    if y < launch - 1:
        bits.append(
            f"The year {y} is the date on the RAWG record. It is earlier than this Nintendo hardware, so it should not be read as the Nintendo release year. The RAWG grid below keeps that date for checking."
        )
    return bits

def game_page(g):
    prefix = "../../"
    primary = g["platforms"][0]
    info = SYS_BY_NAME[primary]
    plat_label = " and ".join(g["platforms"])
    title = f"{g['title']} on {primary} | Where to Play"
    sentence = first_sentence(g["history"])
    short_opt = AVAIL[g["avail"]][3]
    if g["slug"] in CITED:
        # keep meta free of over-claim; still point at the overview in the body
        pass
    desc = f"{sentence} Official option: {short_opt}. Where to Play does not host this game."
    if desc.lower().startswith("where to play"):
        raise SystemExit("bad meta " + g["slug"])
    if BANNED.search(desc):
        raise SystemExit("banned meta " + g["slug"] + " " + desc)
    css = prefix + "css/site.css"
    raw = g["meta"]
    credit_fact = g["credit"]
    if credit_fact == "See the RAWG record":
        named = (raw.get("developers") or [])[:1] + (raw.get("publishers") or [])[:1]
        if named:
            credit_fact = " / ".join(named)
    facts = [g["year"], plat_label, credit_fact, info["era"]]
    if len(g["platforms"]) == 1:
        facts.insert(3, info["kind"])
    fact_html = "".join(f"<li>{esc(x)}</li>" for x in facts)
    genres = ", ".join(raw.get("genres") or []) or "Not listed"
    devs = ", ".join(raw.get("developers") or []) or "Not listed"
    pubs = ", ".join(raw.get("publishers") or []) or "Not listed"
    rating = raw.get("rating")
    rating_txt = f"{rating:.2f} / 5" if isinstance(rating, (int, float)) else "Not listed"
    count = raw.get("ratings_count") or 0
    released = raw.get("released") or "Not listed"
    esrb = raw.get("esrb") or "Not listed"
    raw_plats = ", ".join(raw.get("platforms") or []) or "Not listed"
    cited = CITED.get(g["slug"])
    badge, kind, h, short, body, href, label = AVAIL[g["avail"]]
    if cited:
        body = cited + " Where to Play does not host this game."
    shots = g.get("shot_files") or []
    shot_html = ""
    if shots:
        imgs = []
        for fn in shots:
            imgs.append(f'<img src="{prefix}images/in-game/{esc(fn)}" alt="Screenshot of {esc(g["title"])} from RAWG">')
        shot_html = f"""<h2 class="section-title">Images from RAWG</h2>
<div class="shot-grid">{''.join(imgs)}</div>
<p class="credit-line">Screenshots from <a href="{esc(raw['page'])}" target="_blank" rel="noopener noreferrer">this RAWG record</a>. Powered by <a href="https://rawg.io" target="_blank" rel="noopener noreferrer">RAWG</a>.</p>"""
    cover_src = f"{prefix}images/covers/{g['cover']}"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            breadcrumb_schema([
                ("Home", prefix),
                (f"{primary} games", f"{prefix}platforms/{info['slug']}/"),
                (g["title"], None),
            ]),
            {
                "@type": "VideoGame",
                "name": g["title"],
                "description": desc,
                "datePublished": g["year"],
                "gamePlatform": g["platforms"] if len(g["platforms"]) > 1 else primary,
                "image": cover_src,
            },
        ],
    }
    paras = [f"<p>{esc(g['history'])}</p>"]
    lineup = (g.get("lineup") or "").strip()
    if lineup:
        paras.append(f"<p>{esc(lineup)}</p>")
    prose = "".join(paras)
    series_html = link_list(g.get("rel_series") or [], prefix)
    if g.get("franchise") and not g.get("rel_franchise"):
        fr_empty = "The series list above is the whole family set in this catalog."
    else:
        fr_empty = "No wider family is grouped for this title beyond the series list."
    franchise_html = link_list(g.get("rel_franchise") or [], prefix, fr_empty)
    plat_html = link_list(g.get("rel_platform") or [], prefix, "No other game on these systems is in the catalog yet.")
    devs_named = ", ".join((g.get("meta") or {}).get("developers") or [])
    dev_html = ""
    if g.get("rel_dev"):
        dev_html = (
            f'<h3 class="rel-h">Same developer</h3>'
            f'<p class="credit-line">First developer on the RAWG card: {esc(devs_named)}.</p>'
            + link_list(g["rel_dev"], prefix)
        )
    page = head(prefix, title, desc, css)
    page += header(prefix)
    page += f"""<main id="content">
  <div class="wrap detail">
    <div class="detail-cover">
      <div class="cover">
        <img class="cover-blur" src="{esc(cover_src)}" alt="" aria-hidden="true">
        <img class="cover-main" src="{esc(cover_src)}" alt="{esc(g['title'])} image from RAWG">
      </div>
      <p class="credit-line">Image from <a href="{esc(raw['page'])}" target="_blank" rel="noopener noreferrer">this RAWG record</a>. Powered by <a href="https://rawg.io" target="_blank" rel="noopener noreferrer">RAWG</a>.</p>
    </div>
    <div>
      {crumbs([("Home", prefix), (primary, f"{prefix}platforms/{info['slug']}/"), (g["title"], None)])}
      <h1>{esc(g['title'])}</h1>
      <ul class="facts">{fact_html}</ul>
      <h2 class="section-title">History</h2>
      <div class="prose">{prose}</div>
      <h2 class="section-title">Related in this catalog</h2>
      <p class="credit-line">Same series is the tight name match. Same franchise is the wider family. Same platform is other games on the systems named above.</p>
      <h3 class="rel-h">Same series</h3>
      {series_html}
      <h3 class="rel-h">Same franchise</h3>
      {franchise_html}
      <h3 class="rel-h">Same platform</h3>
      {plat_html}
      {dev_html}
      <h2 class="section-title">RAWG record</h2>
      <div class="stat-grid">
        <div class="stat"><b>RAWG rating</b>{esc(rating_txt)}</div>
        <div class="stat"><b>Ratings</b>{esc(str(count))}</div>
        <div class="stat"><b>RAWG date</b>{esc(str(released))}</div>
        <div class="stat"><b>ESRB on RAWG</b>{esc(str(esrb))}</div>
        <div class="stat"><b>Genres</b>{esc(genres)}</div>
        <div class="stat"><b>Developers</b>{esc(devs)}</div>
        <div class="stat"><b>Publishers</b>{esc(pubs)}</div>
        <div class="stat"><b>Platforms on RAWG</b>{esc(raw_plats)}</div>
      </div>
      <p class="credit-line">Facts in this grid are RAWG's, not our review. <a href="{esc(raw['page'])}" target="_blank" rel="noopener noreferrer">Open the RAWG record</a>. <a href="https://rawg.io" target="_blank" rel="noopener noreferrer">RAWG</a>.</p>
      {shot_html}
      <h2 class="section-title">Official option</h2>
      <div class="routes">
        <article class="route">
          <div class="route-top"><span class="badge badge-{kind}">{esc(badge)}</span></div>
          <h3>{esc(h)}</h3>
          <p>{esc(body)}</p>
          <a class="cta" href="{esc(href)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span>Official site</span></a>
        </article>
      </div>
      <p class="fine">We don't host this game. Confirm the title is still offered before you rely on a library note.</p>
    </div>
  </div>
</main>
"""
    page += footer(prefix)
    page += schema_tag(graph)
    page += "\n</body>\n</html>\n"
    return page


TOP_PLAY = [
    "super-mario-bros",
    "the-legend-of-zelda",
    "metroid",
    "super-mario-world",
    "a-link-to-the-past",
    "chrono-trigger",
    "super-metroid",
    "ocarina-of-time",
    "super-mario-64",
    "mario-kart-64",
    "goldeneye-007-1997",
    "pokemon-red",
    "pokemon-gold",
    "metroid-fusion",
    "legend-of-zelda-the-wind-waker",
    "super-smash-bros-melee",
    "super-mario-galaxy-2",
    "twilight-princess",
    "mario-kart-8",
    "breath-of-the-wild",
    "super-mario-odyssey",
    "mario-kart-8-deluxe",
    "animal-crossing-new-horizons",
    "tears-of-the-kingdom",
]
HOME_SHELVES = [
    ("NES", "nes", ["super-mario-bros", "super-mario-bros-3", "the-legend-of-zelda", "metroid", "tetris-1984", "super-mario-bros-2", "duck-hunt", "excitebike", "kid-icarus", "zelda-ii-the-adventure-of-link"]),
    ("SNES", "snes", ["super-mario-world", "a-link-to-the-past", "chrono-trigger", "super-metroid", "donkey-kong-country", "earthbound", "super-mario-world-2-yoshis-island", "f-zero", "super-mario-kart", "star-fox"]),
    ("Nintendo 64", "nintendo-64", ["ocarina-of-time", "super-mario-64", "majoras-mask", "mario-kart-64", "goldeneye-007-1997", "super-smash-bros-1999", "star-fox-64", "banjo-kazooie", "paper-mario", "perfect-dark"]),
    ("Nintendo Switch", "nintendo-switch", ["breath-of-the-wild", "tears-of-the-kingdom", "super-mario-odyssey", "mario-kart-8-deluxe", "animal-crossing-new-horizons", "metroid-dread", "super-mario-3d-world"]),
]


def _rank(g):
    meta = g.get("meta") or {}
    return (meta.get("ratings_count") or 0, meta.get("rating") or 0, g["title"].lower())


def _by_slug(games):
    return {g["slug"]: g for g in games}


def pick_games(games, seeds, limit, platform=None, skip=()):
    found = _by_slug(games)
    chosen = []
    seen = set(skip)
    for slug in seeds:
        g = found.get(slug)
        if not g or slug in seen:
            continue
        if platform and platform not in g["platforms"]:
            continue
        chosen.append(g)
        seen.add(slug)
        if len(chosen) == limit:
            return chosen
    pool = [g for g in games if g["slug"] not in seen and (not platform or platform in g["platforms"])]
    pool.sort(key=_rank, reverse=True)
    for g in pool:
        chosen.append(g)
        if len(chosen) == limit:
            break
    return chosen


def home_page(games):
    title = "Legal ways to play Nintendo games | Where to Play"
    desc = "A browse catalog of official options for Nintendo games from NES to Switch. Where to Play does not host games."
    if BANNED.search(desc):
        raise SystemExit("banned home meta")
    by_slug = _by_slug(games)
    top = pick_games(games, TOP_PLAY, 20)
    shelves = []
    for name, slug, seeds in HOME_SHELVES:
        shelves.append((name, slug, pick_games(games, seeds, 10, platform=name)))
    shown = []
    for g in top:
        shown.append(g)
    for _name, _slug, rows in shelves:
        shown.extend(rows)
    # hard cap: home is shelves, not the catalog
    if len(shown) > 80:
        raise SystemExit(f"home card cap exceeded: {len(shown)}")
    n = len(games)
    systems_human = ", ".join(name for name, *_ in SYSTEMS[:-1]) + ", and " + SYSTEMS[-1][0]
    plat_links = []
    opts = ['<option value="">Browse a system</option>']
    for name, slug, era, kind in SYSTEMS:
        plat_links.append(f'<a href="platforms/{slug}/">{esc(name)}</a>')
        opts.append(f'<option value="platforms/{slug}/">{esc(name)}</option>')
    def rail(rows):
        return "\n".join(card(g, "") for g in rows)
    shelf_html = []
    shelf_html.append(f"""<section class="shelf" aria-labelledby="top-play">
      <div class="shelf-head"><h2 id="top-play">Top Play</h2></div>
      <div class="rail">{rail(top)}</div>
    </section>""")
    for name, slug, rows in shelves:
        shelf_html.append(f"""<section class="shelf" aria-labelledby="shelf-{slug}">
      <div class="shelf-head"><h2 id="shelf-{slug}">{esc(name)}</h2><a class="see-all" href="platforms/{slug}/">See all</a></div>
      <div class="rail">{rail(rows)}</div>
    </section>""")
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "name": "Where to Play",
                "description": desc,
                "url": "./",
            },
            item_list(shown, ""),
        ],
    }
    page = head("", title, desc, "css/site.css")
    page += header("")
    page += f"""<main id="content">
  <div class="wrap">
    <section class="hero">
      <p class="kicker">Nintendo games, NES through Switch</p>
      <h1>Find the <em>official</em> way back.</h1>
      <p class="lede">Where to Play is a browse catalog of Nintendo games: when they came out, who made them, and the official option when one is public. Nothing here is hosted, and nothing is for sale.</p>
      <p class="hero-note">{n} games across {esc(systems_human)}. This page is a short set of shelves. Each system page lists that library.</p>
    </section>
    <div class="toolbar">
      <label class="search">
        <input id="q" type="search" placeholder="Search by name, system, or year" aria-label="Search by name, system, or year" autocomplete="off">
      </label>
      <label class="system-select">System
        <select id="system-select" aria-label="Open a system page">{''.join(opts)}</select>
      </label>
    </div>
    <nav class="plat-links" aria-label="System pages">{''.join(plat_links)}</nav>
    <p class="results-line" id="count" aria-live="polite"></p>
    <ul class="search-hits" id="hits" hidden></ul>
    <p class="empty" id="empty">No games match that search. Open a system page for the full list.</p>
    <div id="shelves">
      {''.join(shelf_html)}
    </div>
  </div>
</main>
"""
    page += footer("")
    page += schema_tag(graph)
    page += '\n<script src="js/catalog.js"></script>\n</body>\n</html>\n'
    missing = [slug for slug in TOP_PLAY if slug not in by_slug]
    if missing:
        print("top play missing", ", ".join(missing))
    return page


def write_search_index(games):
    rows = []
    for g in games:
        rows.append({
            "t": g["title"],
            "s": g["slug"],
            "y": g["year"],
            "p": " · ".join(g["platforms"][:4]),
        })
    (ROOT / "search.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")))


def platform_page(name, slug, games):
    prefix = "../../"
    info = SYS_BY_NAME[name]
    title = f"{name} games | Where to Play"
    desc = PLATFORM_META[slug]
    if BANNED.search(desc):
        raise SystemExit("banned plat meta " + slug)
    intro = PLATFORM_INTRO[slug]
    cards = "\n".join(card(g, prefix) for g in games)
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            breadcrumb_schema([("Home", prefix), (f"{name} games", None)]),
            item_list(games, prefix),
        ],
    }
    page = head(prefix, title, desc, prefix + "css/site.css")
    page += header(prefix)
    page += f"""<main id="content">
  <div class="wrap">
    {crumbs([("Home", prefix), (f"{name} games", None)])}
    <section class="hero">
      <p class="kicker">{esc(info['era'])} · {esc(info['kind'])}</p>
      <h1>{esc(name)} games</h1>
      <p class="lede">{esc(intro)}</p>
      <p class="hero-note">{len(games)} games on this page.</p>
    </section>
    <div class="grid">
      {cards}
    </div>
  </div>
</main>
"""
    page += footer(prefix)
    page += schema_tag(graph)
    page += "\n</body>\n</html>\n"
    return page


def about_page():
    prefix = "../"
    title = "About | Where to Play"
    desc = "Where to Play is a browse catalog of Nintendo games and official options from NES to Switch. The site does not host games."
    graph = {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "About",
        "description": desc,
        "url": "./",
    }
    page = head(prefix, title, desc, prefix + "css/site.css")
    page += header(prefix, about_current=True)
    page += f"""<main id="content">
  <div class="wrap about">
    {crumbs([("Home", prefix), ("About", None)])}
    <p class="kicker">About</p>
    <h1>A shelf, not a console.</h1>
    <p>Where to Play is a browse catalog of Nintendo games from NES through Switch. Each game page names the year, the Nintendo systems, the developer and publisher when RAWG lists them, the series, and other games in this catalog. Official options are named when they are public, usually Nintendo Switch Online or a Nintendo Switch listing. Confirm the title is still offered.</p>
    <p>Cover images and the facts in each RAWG grid come from <a href="https://rawg.io" target="_blank" rel="noopener noreferrer">RAWG</a>. Pages that show them name RAWG and link the record. Blurbs on this site are original. We do not paste RAWG's text.</p>
    <p>We don't host games. There is no in-browser player and nothing is for sale. Game names are trademarks of their owners. This site is not affiliated with Nintendo.</p>
    <p>Search on the home page stays in the browser and does not create a results URL. System pages live at their own addresses, such as <a href="{prefix}platforms/nes/">NES</a> and <a href="{prefix}platforms/nintendo-switch/">Nintendo Switch</a>.</p>
  </div>
</main>
"""
    page += footer(prefix)
    page += schema_tag(graph)
    page += "\n</body>\n</html>\n"
    return page


def credits_md(rows, skipped):
    lines = [
        "# Credits",
        "",
        "Working title: **Where to Play**.",
        "",
        "All interface art (wordmark, screen glyph, favicon) was drawn for this mock. It is not a Nintendo logo and not a cartridge trademark.",
        "",
        "Game images are from RAWG only (`https://rawg.io` and `media.rawg.io`). No Nintendo galleries, Wikimedia files, retailer photos, or manuals were collected from anywhere else. Each cover is the `background_image` on that game's public RAWG page. Screenshots, when shown, are RAWG-hosted screenshot files from the same page. Large files were resized for this static catalog. There was no RAWG API key in the environment, so records were read from public game pages rather than from `api.rawg.io`.",
        "",
        "RAWG's terms ask for attribution and a link on every page that uses their images or data. This catalog does that in the footer, beside every cover, and on the RAWG record section.",
        "",
        "Blurbs are original. RAWG description text is not copied onto the site.",
        "",
        "| Game | Local cover | RAWG page | RAWG cover | Screenshots |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        shots = "<br>".join(r["shots"]) if r["shots"] else "—"
        lines.append(f"| {r['title']} | `images/covers/{r['cover']}` | {r['page']} | {r['bg']} | {shots} |")
    lines += ["", "## Skipped (no usable RAWG cover)", ""]
    if not skipped:
        lines.append("None.")
    else:
        for s in skipped:
            lines.append(f"- {s}")
    lines += ["", "Nintendo names appear only as the subject of the catalog, in plain text.", ""]
    return "\n".join(lines)


def notes_md(counts, total):
    bits = ", ".join(f"{name} {counts[name]}" for name, *_ in SYSTEMS)
    return f"""# Notes

Working title: **Where to Play**. Browse catalog of Nintendo games. {total} games: {bits}.

## Product constraints

- Browse only. Detail pages name the year, Nintendo platforms, developer and publisher, genres, series context, a RAWG record, and related games in this catalog (same series, same franchise, same platform).
- Official option notes are soft. They name Nintendo Switch Online or a Nintendo Switch listing and tell the reader to confirm the title is still offered. A link is included only for a public Nintendo page we actually know (the Switch Online overview or Nintendo's website), not a guessed product URL.
- No ROMs, no emulator, no in-browser player, no file links.
- Nothing is for sale. No prices, cart, or checkout.
- Game names are trademarks of their owners. The site is not affiliated with Nintendo.
- One page per game slug. A game that launched on two Nintendo systems is one page that names both. Remakes use their own slug, with the year in the name when needed to tell them apart.
- System pages are real HTML at `platforms/{{slug}}/` only. There is no `?platform=` or `?q=` URL. Home search is client-side and does not change the URL.
- Every HTML page has `noindex` and a relative canonical (`./`). Canonicals do not point at a custom domain or at the GitHub path. No robots.txt and no sitemap. The brand stays Where to Play. The home title is `Legal ways to play Nintendo games | Where to Play`.
- Cover images and RAWG grids are RAWG's, attributed on every page that shows them. Blurbs are original. See CREDITS.md.
- No company mark and no company footer beyond the trademark and non-affiliation line.

## Local preview

Open `index.html` in a browser, or serve the folder so directory URLs resolve. Paths are relative, so the folder also fits a static host such as GitHub Pages.
"""


def nintendoish_platforms(meta, ours):
    plats = " ".join(meta.get("platforms") or []).lower()
    if not plats:
        return True
    hints = ["nintendo", "nes", "snes", "famicom", "game boy", "gamecube", "game cube", "wii", "switch", "3ds", "ds", "64"]
    if any(h in plats for h in hints):
        return True
    for p in ours:
        if p.lower() in plats:
            return True
    return False

def resolve_one(title):
    errors = []
    pre = title.get("meta")
    if isinstance(pre, dict) and pre.get("background_image"):
        return pre, None
    cands = []
    for slug in title["rawg"]:
        if slug and slug not in cands:
            cands.append(slug)
    base = cands[0]
    year = str(title.get("year") or "")
    extras = []
    if year.isdigit():
        extras += [f"{base}-{year}", f"{base}-{int(year)-1}", f"{base}-{int(year)+1}"]
    extras += [f"{base}-version"]
    for slug in extras:
        if slug not in cands:
            cands.append(slug)
    for slug in cands[:4]:
        try:
            meta = load_meta(slug)
        except Exception as e:
            errors.append(f"{slug}: {e}")
            continue
        if not meta.get("background_image"):
            errors.append(f"{slug}: no art")
            continue
        if not nintendoish_platforms(meta, title["platforms"]):
            errors.append(f"{slug}: non-nintendo record {meta.get('platforms')}")
            continue
        good_name = names_match(title["title"], meta.get("name") or "")
        same_slug = (meta.get("slug") == slug)
        overlap = len(set(norm(title["title"])) & set(norm(meta.get("name") or "")))
        if good_name or (same_slug and overlap >= 1):
            # reject edition drift when the slug itself is a different edition
            extra = {"deluxe", "hd", "remastered", "remake", "remaster"}
            w, g = set(norm(title["title"])), set(norm(meta.get("name") or ""))
            if extra & g - w and not same_slug:
                errors.append(f"{slug}: edition {meta.get('name')}")
                continue
            return meta, None
        errors.append(f"{slug}: name {meta.get('name')!r}")
    return None, "; ".join(errors)



def enforce_history_gate(titles):
    """Fail when two histories still share a sentence after the title is removed."""
    from unique_histories import history_gate_errors, load_hand
    errs = history_gate_errors(titles, set(load_hand()))
    if errs:
        preview = "\n".join(errs[:20])
        raise SystemExit(f"history uniqueness gate failed ({len(errs)}):\n{preview}")


def main():
    titles = json.loads(DATA.read_text())
    enforce_history_gate(titles)
    titles = [t for t in titles if not t["slug"].startswith("data-sort-value") and "data-sort-value" not in t["title"].lower()]
    slugs = [t["slug"] for t in titles]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("duplicate slug")
    resolved = []
    skipped = []
    print(f"resolving {len(titles)} titles")
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(resolve_one, t): t for t in titles}
        for fut in as_completed(futs):
            t = futs[fut]
            meta, err = fut.result()
            if not meta:
                cover = find_cover(t["slug"])
                if cover:
                    meta = {
                        "slug": t["rawg"][0],
                        "name": t["title"],
                        "released": None,
                        "rating": None,
                        "ratings_count": 0,
                        "genres": [],
                        "developers": [],
                        "publishers": [],
                        "esrb": None,
                        "platforms": [],
                        "background_image": None,
                        "screenshots": [],
                        "page": "https://rawg.io/games/" + t["rawg"][0],
                    }
                    print("KEEP local cover", t["slug"])
                else:
                    skipped.append(f"{t['title']} ({t['slug']}): {err}")
                    print("SKIP", t["slug"], flush=True)
                    continue
            t = dict(t)
            t["meta"] = meta
            resolved.append(t)
            if len(resolved) % 25 == 0:
                print("resolved", len(resolved), flush=True)
    print(f"resolved {len(resolved)} skipped {len(skipped)}")

    def dl_cover(t):
        existing = find_cover(t["slug"])
        if existing:
            t["cover"] = existing
            return
        url = t["meta"].get("background_image")
        if not url:
            return
        dest = COVERS / f"{t['slug']}.jpg"
        try:
            save_image(url, dest, 640)
            t["cover"] = dest.name
        except Exception as e:
            print("cover fail", t["slug"], e, flush=True)

    def dl_shots(t):
        files = []
        urls = []
        for i, shot in enumerate((t["meta"].get("screenshots") or [])[:2], 1):
            fn = f"{t['slug']}-{i}.jpg"
            dest = SHOTS / fn
            try:
                save_image(shot["url"], dest, 560)
                files.append(fn)
                urls.append(shot["url"])
            except Exception as e:
                print("shot fail", t["slug"], e, flush=True)
        t["shot_files"] = files
        t["shot_urls"] = urls

    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = []
        for t in resolved:
            futs.append(ex.submit(dl_cover, t))
        for fut in as_completed(futs):
            fut.result()
        futs = [ex.submit(dl_shots, t) for t in resolved]
        for fut in as_completed(futs):
            fut.result()

    # drop any that still lack a cover file
    kept = []
    for t in resolved:
        if not t.get("cover") or not (COVERS / t["cover"]).exists():
            skipped.append(f"{t['title']} ({t['slug']}): cover file missing")
            continue
        kept.append(t)
    start = {"NES":1983,"SNES":1990,"Nintendo 64":1996,"Game Boy":1989,"Game Boy Color":1998,"Game Boy Advance":2001,"GameCube":2001,"Wii":2006,"Wii U":2012,"Nintendo DS":2004,"Nintendo 3DS":2011,"Nintendo Switch":2017}
    def sort_key(g):
        primary = g["platforms"][0]
        y = int(g["year"])
        odd = 1 if y < start.get(primary, 1983) - 1 else 0
        return (start.get(primary, 9999), odd, y, g["title"].lower())
    kept.sort(key=sort_key)
    attach_related(kept)

    # write pages
    for old in GAMES.glob("*/index.html"):
        pass
    wanted = {t["slug"] for t in kept}
    for d in GAMES.iterdir() if GAMES.exists() else []:
        if d.is_dir() and d.name not in wanted:
            for p in d.rglob("*"):
                if p.is_file():
                    p.unlink()
            d.rmdir()
    for t in kept:
        dest = GAMES / t["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(game_page(t))
    (ROOT / "index.html").write_text(home_page(kept))
    write_search_index(kept)
    (ROOT / "about" / "index.html").write_text(about_page())
    for name, slug, era, kind in SYSTEMS:
        subset = [g for g in kept if name in g["platforms"]]
        dest = PLATS / slug / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not subset:
            # still a page but the rule says leave noindex until it has a real list; all pages are noindex
            raise SystemExit("empty platform " + slug)
        dest.write_text(platform_page(name, slug, subset))

    rows = [{
        "title": t["title"],
        "cover": t["cover"],
        "page": t["meta"]["page"],
        "bg": t["meta"]["background_image"],
        "shots": t.get("shot_urls") or [],
    } for t in kept]
    (ROOT / "CREDITS.md").write_text(credits_md(rows, skipped))
    counts = {name: sum(1 for g in kept if name in g["platforms"]) for name, *_ in SYSTEMS}
    (ROOT / "NOTES.md").write_text(notes_md(counts, len(kept)))
    (ROOT / "data" / "skipped.txt").write_text("\n".join(skipped) + ("\n" if skipped else ""))
    (ROOT / "data" / "counts.json").write_text(json.dumps({"total": len(kept), "by_system": counts, "skipped": len(skipped)}, indent=2))
    print("WROTE", len(kept))
    print(json.dumps(counts))


def render_from_json():
    """Rebuild HTML from titles.json + local covers without refetching RAWG."""
    titles = json.loads(DATA.read_text())
    enforce_history_gate(titles)
    titles = [t for t in titles if not t["slug"].startswith("data-sort-value") and "data-sort-value" not in t["title"].lower()]
    kept = []
    skipped = []
    for t in titles:
        if not t.get("meta"):
            skipped.append(f"{t['title']} ({t['slug']}): missing meta")
            continue
        cover = find_cover(t["slug"])
        if not cover:
            skipped.append(f"{t['title']} ({t['slug']}): cover file missing")
            continue
        t = dict(t)
        t["cover"] = cover
        # reuse existing shot files if present
        shots = []
        for i in (1, 2):
            fn = f"{t['slug']}-{i}.jpg"
            if (SHOTS / fn).exists():
                shots.append(fn)
        t["shot_files"] = shots
        t["shot_urls"] = []
        kept.append(t)
    start = {"NES":1983,"SNES":1990,"Nintendo 64":1996,"Game Boy":1989,"Game Boy Color":1998,"Game Boy Advance":2001,"GameCube":2001,"Wii":2006,"Wii U":2012,"Nintendo DS":2004,"Nintendo 3DS":2011,"Nintendo Switch":2017}
    def sort_key(g):
        primary = g["platforms"][0]
        y = int(g["year"])
        odd = 1 if y < start.get(primary, 1983) - 1 else 0
        return (start.get(primary, 9999), odd, y, g["title"].lower())
    kept.sort(key=sort_key)
    attach_related(kept)
    wanted = {t["slug"] for t in kept}
    for d in GAMES.iterdir() if GAMES.exists() else []:
        if d.is_dir() and d.name not in wanted:
            for p in d.rglob("*"):
                if p.is_file():
                    p.unlink()
            d.rmdir()
    for t in kept:
        dest = GAMES / t["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(game_page(t))
    (ROOT / "index.html").write_text(home_page(kept))
    write_search_index(kept)
    (ROOT / "about" / "index.html").write_text(about_page())
    for name, slug, era, kind in SYSTEMS:
        subset = [g for g in kept if name in g["platforms"]]
        dest = PLATS / slug / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not subset:
            raise SystemExit("empty platform " + slug)
        dest.write_text(platform_page(name, slug, subset))
    rows = [{
        "title": t["title"],
        "cover": t["cover"],
        "page": t["meta"]["page"],
        "bg": t["meta"].get("background_image"),
        "shots": t.get("shot_urls") or [],
    } for t in kept]
    (ROOT / "CREDITS.md").write_text(credits_md(rows, skipped))
    counts = {name: sum(1 for g in kept if name in g["platforms"]) for name, *_ in SYSTEMS}
    (ROOT / "NOTES.md").write_text(notes_md(counts, len(kept)))
    (ROOT / "data" / "skipped.txt").write_text("\n".join(skipped) + ("\n" if skipped else ""))
    (ROOT / "data" / "counts.json").write_text(json.dumps({"total": len(kept), "by_system": counts, "skipped": len(skipped)}, indent=2))
    print("RENDERED", len(kept), "skipped", len(skipped))
    print(json.dumps(counts))



def load_kept_local():
    titles = json.loads(DATA.read_text())
    titles = [t for t in titles if not t["slug"].startswith("data-sort-value") and "data-sort-value" not in t["title"].lower()]
    kept = []
    for t in titles:
        if not t.get("meta"):
            continue
        cover = find_cover(t["slug"])
        if not cover:
            continue
        t = dict(t)
        t["cover"] = cover
        kept.append(t)
    return kept


def render_home_only():
    kept = load_kept_local()
    page = home_page(kept)
    if page.count('class="card"') > 80:
        raise SystemExit("home DOM cap")
    (ROOT / "index.html").write_text(page)
    write_search_index(kept)
    print("HOME", page.count('class="card"'), "cards;", "search", len(kept))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--render-only":
        render_from_json()
    elif len(sys.argv) > 1 and sys.argv[1] == "--home-only":
        render_home_only()
    else:
        main()
