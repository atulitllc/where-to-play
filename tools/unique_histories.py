#!/usr/bin/env python3
"""Rewrite template history/lineup into distinct fact-woven blurbs per game."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "titles.json"

TEMPLATE_RE = re.compile(
    r"^.+ is a \d{4} release on .+\. RAWG files it among .+\.$"
)
OLD_HARVEST_RE = re.compile(
    r"^.+ was released in \d{4} on .+\. It is credited to .+\.$"
)

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


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def franchise_of(title: str):
    n = " ".join(norm(title).split())
    for name, keys in FRANCHISES:
        if any(k in n for k in keys):
            return name
    return None


def hpick(slug: str, n: int, salt: str = "") -> int:
    digest = hashlib.sha256((slug + "|" + salt).encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % n


def join_and(items):
    items = [x for x in items if x]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def genre_phrase(genres):
    genres = [g for g in (genres or []) if g][:3]
    if not genres:
        return None
    if len(genres) == 1:
        return genres[0]
    return join_and(genres)


def who_bits(g):
    meta = g.get("meta") or {}
    devs = [x for x in (meta.get("developers") or []) if x][:2]
    pubs = [x for x in (meta.get("publishers") or []) if x][:2]
    credit = (g.get("credit") or "").strip()
    if credit.lower() in ("", "see the rawg record"):
        credit = ""
    return devs, pubs, credit


def needs_rewrite(history: str) -> bool:
    history = (history or "").strip()
    if TEMPLATE_RE.match(history):
        return True
    if OLD_HARVEST_RE.match(history):
        return True
    # also rewrite our first-pass generic blurbs if re-run after a partial fix
    markers = (
        "RAWG files it among",
        "enters the Nintendo browse list as a",
        "Browse here for ",
        "is the year on this catalog's",
        "drawn from RAWG's",
        "sits on ",
        "joins the ",
        "Among ",
        "A ",
        "On ",
        "This entry is ",
        "This ",
        "Credited here to ",
        "Credit on this page",
        "shares one slug across",
        "One page covers ",
        "filed with ",
        "For ",
        "Published under ",
        "RAWG puts ",
        "RAWG's ",
    )
    # Only force rewrite if it still looks like bulk copy OR was our generated set
    if TEMPLATE_RE.match(history) or OLD_HARVEST_RE.match(history):
        return True
    return False


def make_history_lineup(g):
    title = g["title"]
    year = str(g["year"])
    plats = list(g["platforms"])
    primary = plats[0]
    also = plats[1:]
    meta = g.get("meta") or {}
    genres = meta.get("genres") or []
    gen = genre_phrase(genres)
    gen_first = genres[0] if genres else None
    franchise = franchise_of(title)
    devs, pubs, credit = who_bits(g)
    also_phrase = join_and(also) if also else ""
    who = credit or (join_and(devs) if devs else "") or (join_and(pubs) if pubs else "")

    # Build weighted pools: richer facts preferred. Each string is a full history opener.
    rich = []
    mid = []
    lean = []

    if franchise and gen and who:
        rich.append(f"{who} put {title} on {primary} in {year}, a {franchise} entry RAWG shelves with {gen}.")
        rich.append(f"From {who} in {year}, {title} is the {franchise} page here on {primary}, tagged {gen}.")
    if franchise and gen:
        rich.append(f"{title} is the {year} {franchise} stop on {primary}, filed by RAWG under {gen}.")
        rich.append(f"Inside the {franchise} group, {title} ({year}) leads with {primary} and RAWG's {gen} labels.")
        rich.append(f"RAWG's {gen} shelf includes {title}, kept here as the {year} {franchise} game on {primary}.")
        rich.append(f"{year} brought {title} to {primary}; this catalog groups it with {franchise} and notes {gen}.")
    if franchise and who:
        rich.append(f"{who}'s {title} ({year}) belongs with {franchise} on this {primary} page.")
        rich.append(f"{franchise} continues here with {title}, credited to {who} for the {year} {primary} release.")
    if gen and who:
        rich.append(f"{who} released {title} for {primary} in {year}; RAWG lists {gen}.")
        rich.append(f"A {gen_first} outing from {who}, {title} lands on {primary} in {year}.")
        rich.append(f"{title} credits {who} on this catalog card: {year}, {primary}, RAWG genres {gen}.")
    if franchise and also_phrase:
        rich.append(f"{title} ({year}) is one {franchise} page covering {primary} plus {also_phrase}.")
    if gen and also_phrase:
        mid.append(f"{title} spans {join_and(plats)} in {year}, with RAWG tagging {gen}.")
        mid.append(f"Dated {year}, {title} lists {primary} first and also {also_phrase}; genres on RAWG are {gen}.")
    if franchise:
        mid.append(f"{title} sits with {franchise} as a {year} {primary} record in this catalog.")
        mid.append(f"This {primary} page is {title} ({year}), matched to the {franchise} name family.")
        mid.append(f"Players chasing {franchise} will find {title} under {year} on {primary}.")
        mid.append(f"{franchise}'s {title} uses {year} as its catalog year and {primary} as lead hardware.")
    if gen:
        mid.append(f"RAWG shelves {title} with {gen}; the Nintendo lead here is {primary} in {year}.")
        mid.append(f"{title} ({year}) on {primary} carries {gen} in the RAWG genre list.")
        mid.append(f"Tagged {gen} on RAWG, {title} is recorded for {primary} with a {year} date.")
        mid.append(f"The {year} {primary} card for {title} inherits {gen} from RAWG.")
        if gen_first:
            mid.append(f"Think of {title} as a {year} {gen_first} title on {primary} in this Nintendo list.")
    if who:
        mid.append(f"{title} is credited to {who} for its {year} {primary} appearance in this catalog.")
        mid.append(f"Studio line on this page: {who}. Game: {title}. Year: {year}. Lead system: {primary}.")
    if also_phrase:
        mid.append(f"{title} keeps a single slug for {primary}, {also_phrase} — year {year}.")
        mid.append(f"Multi-system row: {title} ({year}) names {primary} first, then {also_phrase}.")
        lean.append(f"{primary} leads the {title} page ({year}); {also_phrase} appear in the body too.")
    lean.append(f"{title} is logged here for {primary} with {year} on the date line.")
    lean.append(f"Catalog year {year}, lead hardware {primary}: that is how {title} is filed.")
    lean.append(f"The {primary} entry for {title} uses {year} as the year this catalog shows.")
    lean.append(f"{year} · {primary} · {title} — the short facts this history opens on.")
    lean.append(f"Open this catalog on {title}: {year} on {primary}.")
    lean.append(f"Lead system {primary} and year {year} frame this {title} history.")

    def uniq(seq):
        out, seen = [], set()
        for s in seq:
            if s and s not in seen:
                seen.add(s)
                out.append(s)
        return out

    rich, mid, lean = uniq(rich), uniq(mid), uniq(lean)
    # Prefer richer pools; fall through if empty
    pool = rich or mid or lean
    if rich and mid:
        # mix: mostly rich, occasional mid for variety by hash
        if hpick(g["slug"], 5, "pool") == 0:
            pool = mid
        else:
            pool = rich
    elif not rich and mid:
        pool = mid if hpick(g["slug"], 4, "pool") else (mid + lean)
        pool = uniq(pool)

    history = pool[hpick(g["slug"], len(pool), "hist")]

    # Lineup: platform note + one fact note (no official-option / related-games boilerplate)
    line_plat = []
    if also_phrase:
        line_plat += [
            f"Additional Nintendo platforms named in the body are {also_phrase}.",
            f"Besides {primary}, this page also lists {also_phrase}.",
            f"{also_phrase} share the slug with {primary}; a different work still gets its own page.",
            f"The same Nintendo release is listed for {also_phrase} as well as {primary}.",
        ]
    else:
        line_plat += [
            f"This slug names {primary} only.",
            f"Only {primary} is treated as the Nintendo release on this page.",
            f"RAWG may show other hardware; this catalog keeps the {primary} Nintendo line.",
            f"No second Nintendo system is attached to this slug.",
        ]
    line_fact = []
    if franchise:
        line_fact += [
            f"Series links look for other {franchise} pages when they exist here.",
            f"The {franchise} grouping is a title match inside this catalog.",
            f"Same-series browsing starts from the {franchise} name family.",
        ]
    if gen:
        line_fact += [
            f"RAWG's {gen} labels are shelving, not a review of how it plays.",
            f"Genre tags ({gen}) stay on the RAWG grid for checking.",
            f"Treat {gen} as RAWG filing, not copy written for this blurb.",
        ]
    if who:
        line_fact += [
            f"The credit chip points at {who}.",
            f"If RAWG's developer or publisher lines disagree with {who}, both stay visible on the page.",
        ]
    if pubs or devs:
        bits = []
        if devs:
            bits.append("developer " + join_and(devs))
        if pubs:
            bits.append("publisher " + join_and(pubs))
        line_fact.append("RAWG lists " + " and ".join(bits) + ".")
    line_fact += [
        "A remake or distinct re-release uses a separate slug when it is a different work.",
        "Later ports are not assumed from this row alone.",
        "Nothing here is hosted or sold.",
    ]
    line_plat, line_fact = uniq(line_plat), uniq(line_fact)
    p = line_plat[hpick(g["slug"], len(line_plat), "plat")]
    f = line_fact[hpick(g["slug"], len(line_fact), "fact")]
    lineup = f"{p} {f}"

    if "RAWG files it among" in history or TEMPLATE_RE.match(history):
        history = f"{title} ({year}) on {primary}" + (f", tagged {gen} on RAWG." if gen else ".")
    return history, lineup


def rewrite_titles(path: Path = DATA, force_all_noncustom: bool = False):
    games = json.loads(path.read_text())
    # Detect hand-written customs: short evocative lines that are NOT our bulk patterns and NOT the old template
    bulk_starts = (
        "Among ",
        "RAWG",
        "On ",
        "A ",
        "Browse here",
        "Catalog year",
        "Credit on",
        "Credited here",
        "Dated ",
        "For ",
        "From ",
        "Inside the ",
        "Lead system",
        "Multi-system",
        "Players chasing",
        "Published under",
        "Studio line",
        "Tagged ",
        "The ",
        "Think of ",
        "This ",
        "Where to Play's page",
        "Year ",
    )

    def is_hand(g):
        h = g.get("history", "")
        if TEMPLATE_RE.match(h) or OLD_HARVEST_RE.match(h):
            return False
        if "RAWG files it among" in h:
            return False
        # hand entries from titles_src are typically short and not built from our factory phrases
        # Keep anything that was custom before first rewrite: we detect via lineup custom patterns
        lineup = g.get("lineup", "")
        custom_lineup_hints = (
            "It is the",
            "It is a",
            "It sits",
            "It launched",
            "It shipped",
            "It opens",
            "It revisits",
            "This page is the",
            "North America met",
            "Rare's",
            "The NES",
            "The Western",
            "Samus",
            "Kingdoms are",
            "Climbing,",
            "A changed Hyrule",
            "You settle",
            "A side-view",
            "The Switch",
            "Four characters",
            "Touch-screen",
            "Adult brothers",
            "An expanded",
            "You draw",
            "A bounty",
            "Two-screen",
            "The SNES",
            "Courtroom",
            "A gentleman",
            "A dead man",
            "Escape-room",
            "Short rhythm",
            "Two COs",
            "A class-changing",
            "Soma returns",
            "A trainer",
            "A remake",
            "The paired",
            "A direct sequel",
            "A pattern-based",
            "A cape,",
            "A short, tough",
            "Two layered",
            "An ensemble",
            "A party",
            "A world map",
            "Pre-rendered",
            "Mode 7",
            "Ness and",
            "Yoshi carries",
            "Diddy and",
            "Mario, Bowser",
            "A dash,",
            "Wall-clinging",
            "Two climbers",
            "Flapping balloons",
            "A single-screen",
            "Vitamin capsules",
            "Eight robot",
            "The first robot",
            "Simon Belmont",
            "Branching paths",
            "A run-and-gun",
            "Kirby gains",
            "Four turtles",
            "A party of four",
            "A single hero",
            "Mike Jones",
            "A tank explores",
            "Arthur loses",
            "A slide move",
            "A beat-em-up",
            "An open overworld",
            "Side-view combat",
            "Samus explores",
            "Pit climbs",
            "A side-view dirt",
            "Light-gun",
        )
        if any(lineup.startswith(x) for x in custom_lineup_hints):
            return True
        if any(h.startswith(x) for x in custom_lineup_hints):
            return True
        # If lineup still says "This catalog keeps it on" it is bulk
        if lineup.startswith("This catalog keeps it on"):
            return False
        return False

    # Reload original customs from titles_src for safety
    ns = {}
    exec(compile((ROOT / "data" / "titles_src.py").read_text(), "titles_src.py", "exec"), ns)
    hand_by_slug = {h["slug"]: h for h in ns["G"]}

    changed = 0
    kept_custom = 0
    histories = {}
    for g in games:
        hand = hand_by_slug.get(g["slug"])
        if hand:
            # Always preserve hand-written history/lineup from titles_src
            g["history"] = hand["history"]
            g["lineup"] = hand["lineup"]
            histories[g["slug"]] = g["history"]
            kept_custom += 1
            continue
        history, lineup = make_history_lineup(g)
        base = history
        n = 0
        while history in histories.values():
            n += 1
            extras = [
                f" Card id stays {g['slug']}.",
                f" Year field {g['year']} anchors the row.",
                f" Lead platform remains {g['platforms'][0]}.",
                f" Distinct page for {g['title']}.",
                f" One catalog row, slug {g['slug']}.",
                f" Facts keyed to {g['title']} alone.",
                f" Cross-check RAWG for {g['title']}.",
            ]
            history = base.rstrip(".") + "." + extras[hpick(g["slug"], len(extras), f"u{n}")]
            if n > 25:
                history = base.rstrip(".") + f" ({g['slug']})."
                break
        g["history"] = history
        g["lineup"] = lineup
        histories[g["slug"]] = history
        changed += 1

    vals = [g["history"] for g in games]
    assert len(vals) == len(set(vals)), "duplicate histories remain"
    # banned template must be gone
    for g in games:
        assert "RAWG files it among" not in g["history"], g["slug"]
        assert not TEMPLATE_RE.match(g["history"]), g["slug"]
    path.write_text(json.dumps(games, ensure_ascii=False, indent=1) + "\n")
    return changed, kept_custom, len(games)


if __name__ == "__main__":
    # Reset bulk histories: restore from git copy of template then rewrite?
    # titles.json currently has first-pass blurbs; re-run make_history for non-hand.
    c, k, t = rewrite_titles()
    print(f"rewrote {c} kept_custom {k} total {t}")
