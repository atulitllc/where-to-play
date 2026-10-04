# Notes

Working title: **Where to Play**. Browse catalog of Nintendo games. 1971 games: NES 208, SNES 217, Nintendo 64 209, Game Boy 211, Game Boy Color 201, Game Boy Advance 225, GameCube 218, Wii 209, Wii U 209, Nintendo DS 250, Nintendo 3DS 234, Nintendo Switch 208.

## Product constraints

- Browse only. Detail pages name the year, Nintendo platforms, developer and publisher, genres, series context, a RAWG record, and related games in this catalog (same series, same franchise, same platform).
- Official option notes are soft. They name Nintendo Switch Online or a Nintendo Switch listing and tell the reader to confirm the title is still offered. A link is included only for a public Nintendo page we actually know (the Switch Online overview or Nintendo's website), not a guessed product URL.
- No ROMs, no emulator, no in-browser player, no file links.
- Nothing is for sale. No prices, cart, or checkout.
- Game names are trademarks of their owners. The site is not affiliated with Nintendo.
- One page per game slug. A game that launched on two Nintendo systems is one page that names both. Remakes use their own slug, with the year in the name when needed to tell them apart.
- System pages are real HTML at `platforms/{slug}/` only. There is no `?platform=` or `?q=` URL. Home search is client-side and does not change the URL.
- Every HTML page has `noindex` and a relative canonical (`./`). Canonicals do not point at a custom domain or at the GitHub path. No robots.txt and no sitemap. The header wordmark is permanently NES Classics, with the subtitle NINTENDO CATALOG. Do not change it back to Where to Play. Page titles still say Where to Play, and the catalog still spans NES through Switch. The home title is `Legal ways to play Nintendo games | Where to Play`.
- Cover images and RAWG grids are RAWG's, attributed on every page that shows them. Blurbs are original. See CREDITS.md.
- No company mark and no company footer beyond the trademark and non-affiliation line.

## Local preview

Open `index.html` in a browser, or serve the folder so directory URLs resolve. Paths are relative, so the folder also fits a static host such as GitHub Pages.
