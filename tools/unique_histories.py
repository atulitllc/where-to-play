#!/usr/bin/env python3
"""Real one-off histories for generated games.

Handwritten blurbs in data/titles_src.py are copied through, except where
a lineup opener is edited in that file. Generated blurbs come from
data/histories.json. They are prose about that game, not a filled skeleton,
they do not credit RAWG, and they never grow a slug or card id to dodge a
collision.

history_gate_errors() strips the title, genre, platform, era, date, ESRB
label, and title-token clauses ("the word that sticks", "doing the
identifying", and the same family). If two pages still share a sentence,
or a history still uses those clauses, the site build fails.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "titles.json"
HAND = ROOT / "data" / "titles_src.py"
BLURBS = ROOT / "data" / "histories.json"

# Longest first so "Game Boy Advance" is not eaten as "Game Boy".
PLATFORM_NAMES = [
    "Nintendo 3DS",
    "Nintendo DS",
    "Nintendo 64",
    "Nintendo Switch",
    "Game Boy Advance",
    "Game Boy Color",
    "Game Boy",
    "GameCube",
    "Wii U",
    "SNES",
    "NES",
    "Wii",
]

GENRE_WORDS = [
    "massively multiplayer",
    "board games",
    "platformer",
    "adventure",
    "simulation",
    "strategy",
    "shooter",
    "fighting",
    "educational",
    "family",
    "arcade",
    "puzzle",
    "racing",
    "sports",
    "action",
    "casual",
    "indie",
    "card",
    "rpg",
]

ESRB_WORDS = [
    "adults only",
    "rating pending",
    "everyone 10+",
    "everyone",
    "teen",
    "mature",
    "early childhood",
]

# Compose() slot clauses. The title word inside the clause is consumed so
# "built so Dug is the word that sticks" cannot pass as a unique sentence.
CLAUSE_RES = [
    r"built so [a-z0-9']+ is the word that sticks",
    r"[a-z0-9']+ doing the identifying(?: in the name)?",
    r"the word that sticks",
    r"doing the identifying",
    r"(?:with )?the name turning on [a-z0-9']+",
    r"with [a-z0-9']+ as the word the title turns on",
    r"anchored by the word [a-z0-9']+",
    r"the title holding onto [a-z0-9']+",
    r"identified by the word [a-z0-9']+",
    r"the memorable piece of the name being [a-z0-9']+",
    r"the name pairing [a-z0-9']+ with [a-z0-9']+",
    r"with [a-z0-9']+ and [a-z0-9']+ both at work in the title",
    r"[a-z0-9']+ set beside [a-z0-9']+ in the title",
    r"the year already printed in the name",
    r"without repeating the year(?: the title shows)?",
    r"the name already carrying its year",
    r"a roman numeral marking a later entry",
    r"the roman numeral saying this is not the first",
    r"a roman numeral doing the sequel work",
    r"the 64 in the name pointing at that console",
    r"gbc in the name marking the color handheld",
    r"gba in the name marking the advance handheld",
    r"ds in the name marking the dual screen",
    r"the name joining its halves with an ampersand",
    r"(?:its |with |a |the )?release day [a-z0-9 ,]+",
    r"released [a-z]+ \d{1,2}(?:, \d{4})?",
    r"with [a-z]+ \d{1,2}(?:, \d{4})? as its release day",
    r"out on [a-z]+ \d{1,2}(?:, \d{4})?",
    r"dated [a-z]+ \d{1,2}(?:, \d{4})?",
    r"the calendar pointing at [a-z0-9 ,]+",
    r"first dated [a-z]+ \d{1,2}(?:, \d{4})?",
    r"a [a-z]+ \d{1,2}(?:, \d{4})? release",
    r"the catalog year \d{4}",
    r"rated [a-z0-9+ ]{3,24}",
    r"\d+ player ratings recorded against it",
    r"a name of \d+ characters",
    r"a single-word title of \d+ characters",
    r"the whole name being one word, \d+ characters long",
    r"nothing but a \d+-character name",
    r"a one-word title running \d+ characters",
    r"the subtitle [a-z0-9' ]+",
    r"[a-z0-9' ]+ sitting after the colon",
    r"the colon leading into [a-z0-9' ]+",
    r"part of the [a-z0-9' ]+ line",
    r"sitting with the other [a-z0-9' ]+ names",
    r"one of the [a-z0-9' ]+ entries here",
    r"with [a-z0-9' ]+ named on the same page",
    r"sharing this page with [a-z0-9' ]+",
    r"[a-z0-9' ]+ listed beside [a-z0-9' ]+",
    r"the \d+ in the name counting the entry",
    r"a \d+ in the title marking which one this is",
]

TEMPLATE_PHRASES = (
    "the word that sticks",
    "doing the identifying",
    "the name turning on",
    "word the title turns on",
    "anchored by the word",
    "the title holding onto",
    "identified by the word",
    "memorable piece of the name",
    "both at work in the title",
    "the year already printed",
    "without repeating the year",
    "the name already carrying its year",
    "catalog note for",
    "playable context for",
    "the year in the name marks",
)

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

PLACE = {
    "NES": ("third generation", "8-bit home console"),
    "SNES": ("fourth generation", "16-bit home console"),
    "Nintendo 64": ("fifth generation", "3D home console"),
    "Game Boy": ("fourth generation", "8-bit handheld"),
    "Game Boy Color": ("fifth generation", "color handheld"),
    "Game Boy Advance": ("sixth generation", "32-bit handheld"),
    "GameCube": ("sixth generation", "disc home console"),
    "Wii": ("seventh generation", "motion home console"),
    "Wii U": ("eighth generation", "HD home console"),
    "Nintendo DS": ("seventh generation", "dual-screen handheld"),
    "Nintendo 3DS": ("eighth generation", "glasses-free 3D handheld"),
    "Nintendo Switch": ("ninth generation", "hybrid console"),
}

STOP = {
    "a", "an", "the", "of", "and", "or", "for", "to", "in", "on", "with",
    "from", "vs", "vol", "volume", "part", "episode", "ed", "edition",
    "game", "games", "collection", "classic", "classics", "featuring",
    "ii", "iii", "iv", "vi", "vii", "viii", "ix", "xi", "xii", "xiii",
}

ABBREV = {
    "mr", "mrs", "ms", "dr", "jr", "sr", "vs", "st", "vol", "etc",
    "inc", "co", "bros", "no", "ed", "mt", "capt", "gen", "sgt",
}

FRANCHISES = [
    ("Paper Mario", ("paper mario",)),
    ("Mario Kart", ("mario kart",)),
    ("Mario Party", ("mario party",)),
    ("Mario Golf", ("mario golf",)),
    ("Mario Tennis", ("mario tennis",)),
    ("Dr. Mario", ("dr mario",)),
    ("WarioWare", ("warioware", "wario ware")),
    ("Wario", ("wario",)),
    ("Yoshi", ("yoshi",)),
    ("Super Smash Bros.", ("smash bros", "super smash")),
    ("Donkey Kong", ("donkey kong", "diddy kong")),
    ("The Legend of Zelda", ("zelda",)),
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
    ("Mother", ("earthbound", "mother 3")),
    ("Castlevania", ("castlevania",)),
    ("Mega Man", ("mega man", "megaman")),
    ("Final Fantasy", ("final fantasy",)),
    ("Dragon Quest", ("dragon quest", "dragon warrior")),
    ("Harvest Moon", ("harvest moon", "story of seasons", "rune factory")),
    ("Sonic", ("sonic",)),
    ("Tetris", ("tetris",)),
    ("Bomberman", ("bomberman",)),
    ("Contra", ("contra",)),
    ("Street Fighter", ("street fighter",)),
    ("Resident Evil", ("resident evil",)),
    ("Metal Gear", ("metal gear",)),
    ("Star Wars", ("star wars",)),
    ("LEGO", ("lego",)),
    ("Pac-Man", ("pac-man", "pac man")),
    ("Monster Hunter", ("monster hunter",)),
    ("Ace Attorney", ("ace attorney", "phoenix wright")),
    ("Kingdom Hearts", ("kingdom hearts",)),
    ("Mario", ("mario",)),
]

STOCK_PHRASES = (
    "nothing here is hosted or sold",
    "distinct re-release uses a separate slug",
    "rawg shelves",
    "rawg files it among",
    "inherits from rawg",
    "hosted or sold",
    "card id stays",
    "this slug names",
    "rawg may show other hardware",
    "later ports are not assumed",
)


def hpick(slug: str, n: int, salt: str = "") -> int:
    digest = hashlib.sha256(f"{slug}|{salt}".encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % n


def words_of(title: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+", title or "")


def flexible_title_pattern(title: str) -> str | None:
    words = words_of(title)
    if not words:
        return None
    # Keep the gap between title words short so a later echo is not eaten.
    gap = r"[^A-Za-z0-9]{1,12}"
    return r"\b" + gap.join(re.escape(w) for w in words) + r"\b"


def remove_title(text: str, title: str) -> str:
    seen = set()
    forms = [title or ""]
    bare = re.sub(r"\s*\(\d{4}\)\s*$", "", title or "").strip()
    if bare and bare != title:
        forms.append(bare)
    out = text or ""
    for form in forms:
        pat = flexible_title_pattern(form)
        if not pat or pat in seen:
            continue
        seen.add(pat)
        out = re.sub(pat, " ", out, flags=re.I)
    return out


def normalize_sentence(sentence: str, title: str) -> str:
    t = remove_title(sentence, title).lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _era_phrases() -> list[str]:
    out = []
    for era, kind in PLACE.values():
        out.append(era)
        out.append(kind)
    return out


def residue(sentence: str, game: dict) -> str:
    """What is left after the slots a Mad Libs history uses to look unique.

    Strips the title, genre labels, platform names, generation phrases,
    calendar dates, ESRB labels, and title-token clauses. Two compose()
    lines that differed only in those slots land on the same string.
    """
    t = remove_title(sentence, game.get("title") or "").lower()
    for rx in CLAUSE_RES:
        t = re.sub(rx, " ", t)
    for name in PLATFORM_NAMES:
        t = re.sub(rf"\b{re.escape(name.lower())}\b", " ", t)
    for phrase in sorted(set(_era_phrases()), key=len, reverse=True):
        t = re.sub(rf"\b{re.escape(phrase.lower())}\b", " ", t)
    genres = [x.lower() for x in ((game.get("meta") or {}).get("genres") or [])]
    for gname in sorted(set(GENRE_WORDS) | set(genres), key=len, reverse=True):
        if len(gname) < 3:
            continue
        t = re.sub(rf"\b{re.escape(gname)}\b", " ", t)
    for label in ESRB_WORDS:
        t = re.sub(rf"\b{re.escape(label)}\b", " ", t)
    for month in MONTHS:
        t = re.sub(rf"\b{month.lower()}\b", " ", t)
    t = re.sub(r"\b(?:19|20)\d{2}\b", " ", t)
    t = re.sub(r"\b\d{1,2}(?:st|nd|rd|th)?\b", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def split_sentences(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        buf.append(c)
        if c in ".!?":
            prev = "".join(buf).rstrip(".!?")
            toks = re.findall(r"[A-Za-z0-9]+", prev)
            last = toks[-1].lower() if toks else ""
            nxt = text[i + 1] if i + 1 < n else ""
            hold = len(last) == 1 or last.isdigit() or last in ABBREV
            if i + 1 == n or (nxt.isspace() and not hold):
                s = "".join(buf).strip()
                if s:
                    parts.append(s)
                buf = []
                while i + 1 < n and text[i + 1].isspace():
                    i += 1
        i += 1
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def article_for(word: str) -> str:
    if word.upper() in {"RPG", "NES", "SNES"}:
        return "an"
    return "an" if word[:1].lower() in "aeiou" else "a"


def cap(s: str) -> str:
    return s[0].upper() + s[1:] if s else s


def join_and(items: list[str]) -> str:
    items = [x for x in items if x]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + ", and " + items[-1]


def gloss_genre(g: str) -> str:
    if g.upper() == "RPG":
        return "RPG"
    if g.isupper() and len(g) <= 4:
        return g
    return g[0].lower() + g[1:] if g else g


def franchise_of(title: str) -> str | None:
    n = unicodedata.normalize("NFKD", title or "")
    n = "".join(c for c in n if not unicodedata.combining(c)).lower()
    n = re.sub(r"[^a-z0-9]+", " ", n)
    for name, keys in FRANCHISES:
        if any(k in n for k in keys):
            return name
    return None


def year_in_title(title: str, year) -> bool:
    return str(year) in (title or "")


def doubles_year(title: str, year, text: str) -> bool:
    y = str(year)
    if y not in (title or ""):
        return text.count(y) > 1
    return y in remove_title(text, title)


def load_hand() -> dict:
    ns: dict = {}
    exec(compile(HAND.read_text(), "titles_src.py", "exec"), ns)
    return {h["slug"]: h for h in ns["G"]}


def token_freq(games: list[dict]) -> dict[str, int]:
    freq: dict[str, int] = {}
    for g in games:
        seen = set()
        for w in words_of(g["title"]):
            wl = w.lower()
            if wl in seen:
                continue
            seen.add(wl)
            freq[wl] = freq.get(wl, 0) + 1
    return freq


def pick_tokens(title: str, freq: dict[str, int]) -> list[str]:
    cands = []
    for w in words_of(title):
        wl = w.lower()
        if wl in STOP or w.isdigit() or len(w) < 3:
            continue
        cands.append(w)
    if not cands:
        cands = [w for w in words_of(title) if not w.isdigit() and len(w) >= 2]
    cands.sort(key=lambda w: (freq.get(w.lower(), 1), -len(w), w.lower()))
    out, seen = [], set()
    for w in cands:
        if w.lower() in seen:
            continue
        seen.add(w.lower())
        out.append(w)
    return out


def clean_fragment(text: str) -> str:
    text = text.replace("...", " ").replace("…", " ")
    text = re.sub(r"[.!?]+", "", text)
    return re.sub(r"\s+", " ", text).strip(" ,;:-")


class Info:
    def __init__(self, g: dict, freq: dict[str, int]):
        self.title = g["title"]
        self.year = str(g["year"])
        self.slug = g["slug"]
        self.primary = g["platforms"][0]
        self.also = list(g["platforms"][1:])
        self.year_in_name = year_in_title(self.title, self.year)
        self.era, self.kind = PLACE.get(self.primary, ("its generation", "Nintendo system"))
        meta = g.get("meta") or {}
        self.genres = [x for x in (meta.get("genres") or []) if x][:3]
        self.esrb = meta.get("esrb") or ""
        self.ratings = int(meta.get("ratings_count") or 0)
        released = meta.get("released") or ""
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", released)
        self.date_raw = ""
        if m:
            month = MONTHS[int(m.group(2)) - 1]
            day = int(m.group(3))
            # Never restate a year the title already contains.
            self.date_raw = f"{month} {day}" if self.year_in_name else f"{month} {day}, {self.year}"
        self.tokens = pick_tokens(self.title, freq)
        self.token = self.tokens[0] if self.tokens else ""
        self.token2 = self.tokens[1] if len(self.tokens) > 1 else ""
        title_words = words_of(self.title)
        self.single_word = len(title_words) == 1
        self.token_survives = bool(self.token) and not (
            self.single_word and title_words and title_words[0].lower() == self.token.lower()
        )
        self.letters = len(re.sub(r"\s+", "", self.title))
        self.franchise = franchise_of(self.title)
        self.feats = self._feats()

    def _feats(self) -> list:
        feats = []
        if self.year_in_name:
            feats.append("year_in_name")
        if ":" in self.title:
            sub = clean_fragment(re.sub(r"\s*\(\d{4}\)\s*$", "", self.title.split(":", 1)[1]))
            if len(sub) > 2:
                feats.append(("subtitle", sub))
        if re.search(r"\b(?:II|III|IV|VI|VII|VIII|IX|XI|XII|XIII)\b", self.title):
            feats.append("roman")
        nums = [n for n in re.findall(r"\b\d+\b", self.title) if n != self.year]
        if self.primary == "Nintendo 64":
            nums = [n for n in nums if n != "64"]
        if nums:
            feats.append(("num", nums[0]))
        if "&" in self.title:
            feats.append("amp")
        if self.primary == "Nintendo 64" and re.search(r"\b64\b", self.title):
            feats.append("sixtyfour")
        if re.search(r"\bGBC\b", self.title):
            feats.append("gbc")
        if re.search(r"\bGBA\b", self.title):
            feats.append("gba")
        if re.search(r"\bDS\b", self.title):
            feats.append("ds")
        if self.franchise:
            feats.append(("franchise", self.franchise))
        if self.also:
            feats.append(("also", join_and(self.also)))
        return feats


def genre_verb(info: Info, v: int) -> str:
    gs = [gloss_genre(g) for g in info.genres]
    if not gs:
        return [
            "does not carry a genre label",
            "has genre left blank",
            "comes without a genre label",
            "is not tagged with a genre",
        ][v % 4]
    if len(gs) == 1:
        art = article_for(gs[0])
        return [
            f"is {art} {gs[0]}",
            f"plays as {art} {gs[0]}",
            f"reads as {art} {gs[0]}",
            f"stands as {art} {gs[0]}",
            f"lands as {art} {gs[0]}",
            f"arrives as {art} {gs[0]}",
            f"counts as {art} {gs[0]}",
            f"shows up as {art} {gs[0]}",
        ][v % 8]
    if len(gs) == 2:
        pair = f"{gs[0]} and {gs[1]}"
        return [
            f"mixes {pair}",
            f"spans {pair}",
            f"covers {pair}",
            f"brings together {pair}",
            f"pairs {pair}",
            f"crosses {pair}",
        ][v % 6]
    triple = f"{gs[0]}, {gs[1]}, and {gs[2]}"
    return [
        f"mixes {triple}",
        f"spans {triple}",
        f"covers {triple}",
        f"brings together {triple}",
    ][v % 4]


def place_clause(info: Info, v: int) -> str:
    p, era, kind = info.primary, info.era, info.kind
    art = article_for(p.split()[0])
    return [
        f"on {p}",
        f"on {p}, {art} {era} {kind}",
        f"for {p} in the {era}",
        f"on the {kind} {p}",
        f"during the {era} on {p}",
        f"as {art} {p} release from the {era}",
        f"in the {era}, on {p}",
        f"on {p} hardware from the {era}",
        f"for the {kind} years of {p}",
        f"among {era} games on {p}",
    ][v % 10]


def token_clause(info: Info, v: int) -> str:
    w, w2 = info.token, info.token2
    opts = [
        f"the name turning on {w}",
        f"with {w} as the word the title turns on",
        f"anchored by the word {w}",
        f"the title holding onto {w}",
        f"identified by the word {w}",
        f"{w} doing the identifying in the name",
        f"the memorable piece of the name being {w}",
        f"built so {w} is the word that sticks",
    ]
    if w2:
        opts.extend([
            f"the name pairing {w} with {w2}",
            f"with {w} and {w2} both at work in the title",
            f"{w} set beside {w2} in the title",
        ])
    return opts[v % len(opts)]


def single_clause(info: Info, v: int) -> str:
    n = info.letters
    return [
        f"a single-word title of {n} characters",
        f"the whole name being one word, {n} characters long",
        f"nothing but a {n}-character name",
        f"a one-word title running {n} characters",
    ][v % 4]


def feat_clause(info: Info, v: int) -> str:
    if not info.feats:
        return ""
    feat = info.feats[v % len(info.feats)]
    if feat == "year_in_name":
        return [
            "the year already printed in the name",
            "without repeating the year the title shows",
            "the name already carrying its year",
        ][v % 3]
    if feat == "roman":
        return [
            "a Roman numeral marking a later entry",
            "the Roman numeral saying this is not the first",
            "a Roman numeral doing the sequel work",
        ][v % 3]
    if feat == "single":
        return ["the title kept to one word", "no subtitle hanging off the name"][v % 2]
    if feat == "amp":
        return "the name joining its halves with an ampersand"
    if feat == "sixtyfour":
        return "the 64 in the name pointing at that console"
    if feat == "gbc":
        return "GBC in the name marking the color handheld"
    if feat == "gba":
        return "GBA in the name marking the Advance handheld"
    if feat == "ds":
        return "DS in the name marking the dual screen"
    if isinstance(feat, tuple) and feat[0] == "subtitle":
        sub = feat[1]
        return [f"the subtitle {sub}", f"{sub} sitting after the colon", f"the colon leading into {sub}"][v % 3]
    if isinstance(feat, tuple) and feat[0] == "num":
        n = feat[1]
        return [f"the {n} in the name counting the entry", f"a {n} in the title marking which one this is"][v % 2]
    if isinstance(feat, tuple) and feat[0] == "franchise":
        fr = feat[1]
        return [f"part of the {fr} line", f"sitting with the other {fr} names", f"one of the {fr} entries here"][v % 3]
    if isinstance(feat, tuple) and feat[0] == "also":
        also = feat[1]
        return [f"with {also} named on the same page", f"sharing this page with {also}", f"{also} listed beside {info.primary}"][v % 3]
    return ""


def extra_clause(info: Info, v: int) -> str:
    # Character counts and rating totals are last-resort differentiators only.
    bits = []
    if info.esrb and v % 3 != 1:
        bits.append(f"rated {info.esrb}")
    if info.also and v % 4 == 3:
        bits.append(f"also on {join_and(info.also)}")
    if v >= 320 and not info.single_word:
        bits.append(f"a name of {info.letters} characters")
    if v >= 360 and info.ratings:
        bits.append(f"{info.ratings} player ratings recorded against it")
    if v >= 400 and info.token2 and info.token_survives:
        bits.append(f"alongside {info.token2}")
    out = []
    for b in bits:
        if b not in out:
            out.append(b)
    return ", ".join(out)


def date_tail(info: Info, v: int) -> str:
    d = info.date_raw
    if not d:
        if info.year_in_name:
            return ""
        return f"the catalog year {info.year}"
    return [
        f"released {d}",
        f"with {d} as its release day",
        f"its release day {d}",
        f"out on {d}",
        f"dated {d}",
        f"the calendar pointing at {d}",
        f"first dated {d}",
        f"a {d} release",
    ][v % 8]


def _tail(parts, datebit, include_date: bool) -> str:
    bits = list(parts)
    if include_date and datebit:
        bits.append(datebit)
    return ", ".join(b for b in bits if b)


def compose(info: Info, v: int) -> str:
    gv = genre_verb(info, v)
    place = place_clause(info, v // 3)
    fam = v % 12
    feat = feat_clause(info, v // 5)
    token_bit = token_clause(info, v // 2) if info.token_survives else single_clause(info, v)
    # One concrete hook. Prefer a fact about the name over a second echo of the same word.
    if feat and info.token and info.token.lower() in feat.lower() and "word" in token_bit:
        hook = [feat]
    elif feat:
        hook = [feat]
        if info.token_survives and info.token.lower() not in feat.lower():
            hook.append(token_bit)
    else:
        hook = [token_bit]
    extra = extra_clause(info, v)
    if extra:
        hook.append(extra)
    # Drop exact duplicate clauses.
    deduped = []
    for bit in hook:
        if bit and bit not in deduped:
            deduped.append(bit)
    title = info.title
    datebit = date_tail(info, v // 7)
    tail = _tail(deduped, datebit, True)
    tail_nodate = _tail(deduped, "", False)
    era = info.era
    kind = info.kind
    primary = info.primary
    when = info.date_raw or ("the year already in the name" if info.year_in_name else str(info.year))

    styles = [
        f"{title} {gv} {place}, {tail}.",
        f"{cap(place)}, {title} {gv}, {tail}.",
        f"{when} is the release day for {title}, which {gv} {place}, {tail_nodate}.",
        f"In the {era}, {title} {gv} {place}, {tail}.",
        f"The {era} {kind} is where {title} {gv}, {tail}.",
        f"Set on {primary}, {title} {gv} {place}, {tail}.",
        f"For {primary} in the {era}, {title} {gv}, {tail}.",
        f"A {era} {kind} entry: {title} {gv}, {tail}.",
        f"Looking up {title} turns up {gv.replace('is ', '', 1) if gv.startswith('is ') else gv} {place}, {tail}.",
        f"{primary} leads for {title}, which {gv} {place}, {tail}.",
        f"This {era} page is {title}. It {gv} {place}, {tail}.",
        f"From the {kind} years, {title} {gv} {place}, {tail}.",
    ]
    # A few more wordings so the common families do not share a first line.
    styles.extend([
        f"What belongs on the {primary} line is {title}, which {gv} {place}, {tail}.",
        f"Catalog note for {title}: it {gv} {place}, {tail}.",
        f"The {kind} frame for {title} is the {era}. It {gv}, {tail}.",
        f"Playable context for {title} is {place}: it {gv}, {tail}.",
    ])
    s = styles[fam % len(styles)] if v < 320 else styles[v % len(styles)]
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r",\s*,", ", ", s)
    s = re.sub(r",\s*\.", ".", s)
    s = re.sub(r"\s+\.", ".", s)
    if not s.endswith("."):
        s += "."
    return s



def _title_present(text: str, title: str) -> bool:
    if title and title in text:
        return True
    pat = flexible_title_pattern(title)
    return bool(pat and re.search(pat, text, flags=re.I))


def slug_appended(text: str, g: dict) -> bool:
    slug = g["slug"].lower()
    low = remove_title(text, g["title"]).lower()
    if f"({slug})" in low or f"slug {slug}" in low:
        return True
    # A hyphenated id pasted into the sentence is the old collision dodge.
    if "-" in slug and re.search(rf"(?<![a-z0-9]){re.escape(slug)}(?![a-z0-9])", low):
        return True
    return False


def banned(text: str, g: dict) -> str:
    low = text.lower()
    if "rawg" in low:
        return "rawg"
    for phrase in STOCK_PHRASES:
        if phrase in low:
            return phrase
    if slug_appended(text, g):
        return "slug"
    if doubles_year(g["title"], g["year"], text):
        return "year"
    if not _title_present(text, g["title"]):
        return "title-missing"
    return ""


def history_gate_errors(games: list[dict], hand_slugs: set[str] | None = None) -> list[str]:
    """Sentences that still match after template slots are removed.

    Compared text is history and lineup. Slots removed: title, genre,
    platform, era, date, ESRB, and title-token clauses.
    """
    errors = []
    seen: dict[str, str] = {}
    for g in games:
        history = (g.get("history") or "").strip()
        lineup = (g.get("lineup") or "").strip()
        if not history:
            errors.append(f"empty history {g['slug']}")
            continue
        blob = f"{history} {lineup}".lower()
        for phrase in TEMPLATE_PHRASES:
            if phrase in blob:
                errors.append(f"template clause {g['slug']}: {phrase}")
                break
        for field, text in (("history", history), ("lineup", lineup)):
            if not text:
                continue
            for sent in split_sentences(text):
                key = residue(sent, g)
                if len(key) < 12:
                    continue
                prev = seen.get(key)
                if prev and prev != g["slug"]:
                    errors.append(
                        f"shared sentence after slot strip: {g['slug']} {field} vs {prev}: {key[:180]}"
                    )
                else:
                    seen.setdefault(key, g["slug"])
        if slug_appended(history, g):
            errors.append(f"slug appended in history {g['slug']}")
        auto = hand_slugs is not None and g["slug"] not in hand_slugs
        if auto and doubles_year(g["title"], g["year"], history):
            errors.append(f"year doubled {g['slug']}: {history[:180]}")
        if auto:
            if lineup:
                errors.append(f"generated page still has a second paragraph {g['slug']}")
            low = history.lower()
            if "rawg" in low or "inherits from rawg" in low or "rawg shelves" in low:
                errors.append(f"RAWG attribution in history {g['slug']}")
    blob_counts: dict[str, int] = {}
    for g in games:
        blob = f"{g.get('history') or ''} {g.get('lineup') or ''}"
        for marker in (
            "Nothing here is hosted or sold",
            "A remake or distinct re-release uses a separate slug",
            "Later ports are not assumed from this row alone",
            "This slug names",
            "RAWG may show other hardware",
            "No second Nintendo system is attached",
            "RAWG shelves",
            "inherits from RAWG",
        ):
            if marker in blob:
                blob_counts[marker] = blob_counts.get(marker, 0) + 1
    for marker, n in blob_counts.items():
        if n:
            errors.append(f"stock boilerplate x{n}: {marker}")
    return errors


def load_blurbs(path: Path = BLURBS) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    if isinstance(data, list):
        return {row["slug"]: row["history"] for row in data}
    return {slug: text for slug, text in data.items()}


def rewrite_titles(path: Path = DATA) -> tuple[int, int, int]:
    games = json.loads(path.read_text())
    hand = load_hand()
    blurbs = load_blurbs()
    kept = changed = 0
    missing = []
    for g in games:
        src = hand.get(g["slug"])
        if src:
            g["history"] = src["history"]
            g["lineup"] = src["lineup"]
            kept += 1
            continue
        text = (blurbs.get(g["slug"]) or "").strip()
        if not text:
            missing.append(g["slug"])
            continue
        why = banned(text, g)
        if why:
            raise SystemExit(f"banned history {g['slug']}: {why}\n{text}")
        g["history"] = text
        g["lineup"] = ""
        changed += 1
    if missing:
        raise SystemExit(f"missing real history for {len(missing)} games, first: {missing[:12]}")
    errors = history_gate_errors(games, set(hand))
    if errors:
        raise SystemExit(f"gate failed after rewrite ({len(errors)}):\n" + "\n".join(errors[:25]))
    path.write_text(json.dumps(games, ensure_ascii=False, indent=1) + "\n")
    return changed, kept, len(games)


def compose_would_fail() -> None:
    """The old generator collides once slot words are stripped."""
    games = json.loads(DATA.read_text())
    hand = set(load_hand())
    freq = token_freq(games)
    sample = [g for g in games if g["slug"] not in hand][:40]
    for g in sample:
        g["history"] = compose(Info(g, freq), hpick(g["slug"], 16, "gate"))
        g["lineup"] = ""
    errors = history_gate_errors(sample, hand)
    shared = [e for e in errors if e.startswith("shared sentence") or e.startswith("template clause")]
    if not shared:
        raise SystemExit("gate did not reject compose() output")
    print(f"compose() rejected ({len(shared)} signals on {len(sample)} samples)")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--prove-compose-fails":
        compose_would_fail()
    else:
        c, k, t = rewrite_titles()
        print(f"rewrote {c} kept_handwritten {k} total {t}")
