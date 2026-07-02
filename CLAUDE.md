# Projekt: Štítky se jmény (tisk na A4)

## Pravidla práce

- **Nikdy necommituj ani nepushuj do gitu bez výslovného příkazu uživatele.** Změny prováděj
  jen v pracovních souborech; `git commit`/`git push` až na explicitní pokyn.

Generátor štítků se jmény pro tisk na A4. Uživatel zadá jméno a aplikace vykreslí stránku
rozdělenou do tří sloupců a zvoleného počtu řádků, kde každá buňka obsahuje totéž jméno.
Stránka se tiskne (nebo ukládá jako PDF) a podle soutiskových křížků v rozích se rozstříhá
na jednotlivé štítky.

## Stav projektu

Funkční. Hlavní deliverable je samostatná HTML aplikace `Stitky_jmena.html` — žádný build,
žádné závislosti, otevírá se přímo v prohlížeči.

## Nasazení

- **Hosting: GitHub Pages** (ne Vercel). Publikováno z branch `main`, cesta `/`.
- **Repozitář:** https://github.com/polachp/mamka-stitky-jmen
- **Živá adresa:** https://polachp.github.io/mamka-stitky-jmen/ — `index.html` přesměruje na
  `Stitky_jmena.html`, což je vstupní bod aplikace pro uživatele.
- Aktualizace webu = `git push` na `main`; GitHub Pages nasadí automaticky.

## Soubory

- `Stitky_jmena.html` — kompletní aplikace (HTML + CSS + JS v jednom souboru).
- `Jmena_SK.md` — datový podklad: 30 nejčetnějších slovenských křestních jmen v celé
  populaci, společný žebříček obou pohlaví podle počtu nositelů. Zdroj forebears.io,
  pořadí ověřeno proti žebříčku Ministerstva vnitra SR. Slouží jako seznam jmen k tisku.
- `CLAUDE.md` — tento popis.

## Funkce aplikace

- **Vstupy v ovládacím panelu:** jméno, počet řádků (1–30), max. velikost písma (pt),
  výběr písma (combobox, 11 systémových fontů).
- **Pevné 3 sloupce.** Mřížka vždy vyplní celou výšku i šířku tiskové plochy A4.
- **Jméno vždy na jednom řádku.** Pokud se delší jméno nevejde do šířky buňky, písmo se
  automaticky zmenší (binární hledání největší velikosti ≤ max). „Max. velikost“ je horní
  hranice, na kterou písmo naroste u kratších jmen.
- **Soutiskové křížky** v každém průsečíku mřížky (v rozích buněk) místo plných čar —
  vykreslené jako SVG vrstva nad mřížkou. Označují řezy pro vodorovné i svislé stříhání.
- **Živý náhled** A4 (210 × 297 mm), aktualizace při každé změně.
- **Tisk / Uložit PDF** přes `window.print()`; tisková CSS skryje ovládací panel.
- **Ukládání nastavení** do `localStorage` (klíč `stitky_jmena_settings`) automaticky po
  každé změně; obnova při otevření.
- **Reset na výchozí** — vrátí výchozí hodnoty a smaže uložené nastavení.

## Technické detaily

- **Rozvržení tisku:** `@page { size: A4; margin: 0 }`, vnitřní okraj stránky `--margin: 10mm`.
  Mřížka `display: grid`, `grid-template-columns: repeat(var(--cols), 1fr)`, `grid-auto-rows: 1fr`.
- **CSS proměnné** na `:root`: `--cols` (3), `--rows`, `--font` (pt), `--family`, `--margin`.
- **Auto-fit písma** `fitFontPt(maxPt, family)`: měří šířku textu přes `canvas` `measureText`
  s odpovídajícím fontem a vahou 700, porovnává s šířkou buňky (mínus padding), binárně hledá
  největší velikost. Převod pt→px konstantou `96/72`.
- **Křížky** `renderCrops(rows)`: SVG s `viewBox = "0 0 W H"` (W, H = `grid.clientWidth/Height`),
  `preserveAspectRatio="none"`; pro každý průsečík `c=0..COLS`, `r=0..rows` dvě úsečky
  (vodorovná + svislá), rameno ~5,5 px. Přepočítává se i na `resize` a `beforeprint`.
- **Persistence:** `saveSettings()` / `loadSettings()` serializují `{name, rows, font, family}`
  do JSON v `localStorage`. `DEFAULTS` drží výchozí hodnoty pro reset.
- **Pořadí inicializace:** `loadSettings()` → `render()`. `render()` = přestavění buněk +
  auto-fit + křížky; `update()` = `render()` + `saveSettings()`.

## Omezení a poznámky

- `localStorage` je vázané na konkrétní soubor a prohlížeč — nastavení se nepřenáší na jiný
  počítač ani do jiného prohlížeče. U `file://` může být v některých prohlížečích omezené;
  Chrome/Edge/Firefox to běžně zvládají.
- Combobox nabízí jen systémové fonty (žádné načítání z webu), aby tisk fungoval offline.

## Možné další kroky

- Hromadný režim: vygenerovat všech 30 jmen najednou, každé jméno = jedna stránka.
- Volitelný počet sloupců (teď napevno 3).
- Nastavitelná velikost/tloušťka křížků a okrajů stránky v UI.
- Ukládání/načítání více pojmenovaných předvoleb.
- Volitelný rukopisný/ozdobný font (vyžadovalo by Google Fonts a online tisk).
