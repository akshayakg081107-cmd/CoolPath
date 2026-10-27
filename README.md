# CoolPath — AI-powered heat-safe route comparison (prototype)

**Team:** Dwishakti · **Theme:** AI, GIS & Emerging Technologies  
CoolPath compares walking routes using illustrative street-segment heat-risk, shade and cooling-stop attributes. This repository implements a small, runnable proof of concept based on the submitted concept deck.

> **Important:** This is a demo, not a live navigation or heat-health service. Included data are synthetic examples, not verified Chennai streets, live weather, measured shade, or official cooling points. The score is a relative decision-support indicator and does not guarantee a safe route.

## Features
- Browser-based mobile-friendly route comparison page.
- JSON API endpoint (`/api/routes`) and transparent route scoring.
- Shortest-distance and lower-estimated-heat route objectives using Dijkstra's algorithm.
- Per-route distance, illustrative heat score, shade estimate and mapped cooling-stop count.
- Sample dataset, automated unit tests, and MIT license.

## Tech stack
- Python 3.10+ (standard library only; no third-party runtime dependencies)
- HTML, CSS, vanilla JavaScript
- JSON sample network; algorithm is deliberately lightweight for the first prototype.

## Setup
Install Python 3.10 or newer. No package installation is needed. From this folder run:
```bash
python app.py
```
Open `http://127.0.0.1:8000` in a browser. Stop the server with Ctrl+C.

## API
`GET /api/routes?start=A&end=D`

Returns a JSON object with candidate route summaries. Known sample node IDs: `A`, `B`, `C`, `D`. Unknown node IDs return HTTP 400 with an error message.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Repository structure
```text
CoolPath_OpenSource/
├── app.py
├── app/
│   ├── __init__.py
│   └── routing.py
├── data/
│   └── sample_network.json
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_routing.py
├── docs/
│   └── TECHNICAL_DESIGN.md
├── requirements.txt
├── LICENSE
└── README.md
```

## How the route score works
Each edge has distance in metres, heat-risk estimate from 0 to 1, shade percentage from 0 to 100, and an optional cooling-stop flag. The heat-aware route cost for each edge is:

`distance_m × (0.35 + heat_risk + (1 - shade_pct / 100) × 0.45)`

Dijkstra's algorithm selects the path with the lowest summed cost. Route summaries then calculate distance-weighted average heat-risk and shade. The factors and weights are starter assumptions for a prototype; they must be calibrated and validated against reliable local observations before real use.

## Data and future integration
For a real pilot:
1. Replace synthetic links with a verified OpenStreetMap pedestrian network and comply with its attribution/ODbL requirements.
2. Add weather/forecast data (for example, Open-Meteo subject to its current terms) and suitable land-surface-temperature data (NASA Earthdata products require careful interpretation).
3. Collect shade and cooling-point information with source and last-verified timestamp.
4. Validate on a small campus/neighbourhood with local users and public-health/civic partners.
5. Add time-of-day effects, accessibility, route geometry on a map, and clear uncertainty reporting.

Do not present land-surface temperature as the same thing as pedestrian-level air temperature. Do not call this a medical device or a guarantee of safety.

## Known limitations
- Sample network has only four synthetic nodes.
- No live weather, GIS processing, geocoding, authentication, database, or production map tiles.
- “Cooling stops” are sample flags, not verified facilities.
- Risk weights are illustrative and are not validated by health experts.
- No machine-learning model is trained; the first prototype uses transparent rule-based scoring. AI/ML analysis is a future phase.

## License
MIT. See `LICENSE`.
