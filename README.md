# Wiedeń - plan wycieczki

Planowanie krótkiego wypadu dla 2 osób do Wiednia: **3 dni**, tempo bez pośpiechu i bez żadnych sportów (dopasowane do osoby 60+). Pałace, muzea, kawiarnie z tradycją i wieczór z muzyką, wszystko w centrum na krótkich spacerach i dojazdach metrem.

**Interaktywna strona (oś czasu dzień po dniu):** https://lukrecjajestbe.github.io/wieden/ (deployuje się automatycznie po każdej zmianie na `main`)

## Struktura repo

- **`plan/`** - plan dzień po dniu w markdownie: [`wieden.md`](plan/wieden.md). Kończy się orientacyjną wyceną kosztów dla 2 osób. Zobacz [`plan/README.md`](plan/README.md) dla skrótu.
- **`scripts/build_data.py`** - skrypt Pythona (uruchamiany przez `uv run`) generujący dane dla interaktywnej strony z plików w `plan/`.
- **`web/`** - interaktywna prezentacja (React + Vite): mapa Leaflet z atrakcjami i restauracjami, kafelki (jeden na miejsce) z linkami do Google Maps, oś czasu dzień po dniu z miniaturami zdjęć i wyceną. Zobacz sekcję niżej.

## Zależności (uv)

Projekt używa [uv](https://docs.astral.sh/uv/) do zarządzania zależnościami Pythona. Instalacja:

```bash
uv sync
```

Skrypty w `scripts/` uruchamia się przez `uv run scripts/build_data.py`, nie bezpośrednio `python3`.

## Interaktywna prezentacja (`web/`)

Jednostronicowa aplikacja React pokazująca plan jako oś czasu dzień po dniu z wyceną.

Dane dla strony (`web/src/data/data.json`) są generowane z plików markdown w `plan/` - to nie jest osobne źródło prawdy, tylko odbicie tych plików.

```bash
# 1. Wygeneruj dane (za kazdym razem po zmianie plikow w plan/)
uv run scripts/build_data.py

# 2. Zainstaluj zaleznosci frontendu (jednorazowo)
cd web && npm install

# 3. Uruchom lokalnie
npm run dev
```

Otwórz `http://localhost:5173` (albo adres wypisany w terminalu).

## Deploy

Automatyczny - GitHub Actions (`.github/workflows/deploy.yml`) buduje i publikuje stronę na GitHub Pages po każdym pushu do `main`. Nie trzeba nic uruchamiać ręcznie. Szczegóły w sekcji "Deploy" w [`CLAUDE.md`](CLAUDE.md).
