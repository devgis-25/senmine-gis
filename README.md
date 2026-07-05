# ⛏ SenMine GIS

**WebGIS platform for geospatial analysis of Senegal's mining sector.**

Built with real data from USGS Africa GIS Database, OpenStreetMap and WorldPop 2020, SenMine GIS provides decision-support tools for mining governance in Senegal.

---

## 🔍 Key Features

- 🗺 Interactive map — exploitation sites, exploration zones, mineral deposits
- ⚠ Land-use conflict analysis — proximity scoring to protected areas & waterways
- 🌿 Environmental impact — WorldPop 2020 population exposure per mining site
- 🎯 Predictive analysis — regional mining potential scoring (0–100)
- 📊 Full statistics dashboard with charts and detailed tables

---

## 📊 Data Coverage

| Layer | Source | Count |
|-------|--------|-------|
| Mining exploitation sites | USGS NMIC 2021 | 16 |
| Exploration sites | USGS NMIC 2021 | 14 |
| Mineral deposits | USGS NMIC 2021 | 6 |
| Protected areas | OpenStreetMap | 12 |
| Waterways | OpenStreetMap | 1,895 |
| Localities | OpenStreetMap | 255 |
| Power lines | USGS NMIC 2021 | 89 |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Spatial database | PostgreSQL 17 + PostGIS 3.5 (Supabase) |
| Backend | Django 6 + GeoDjango |
| Geospatial API | Django REST Framework + djangorestframework-gis |
| Spatial analysis | GeoPandas, Shapely, pyproj, rasterio |
| Frontend | MapLibre GL JS, Chart.js, Turf.js |
| CI/CD | GitHub Actions → Railway |
| Data sources | USGS NMIC, OpenStreetMap, WorldPop 2020 |
| Projection | EPSG:32628 UTM Zone 28N |

---

## 🚀 Getting Started

```bash
git clone https://github.com/devgis-25/senmine-gis.git
cd senmine-gis/backend

python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env with your DB credentials

python manage.py migrate
python manage.py runserver
```

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/sites-miniers/` | Mining sites (GeoJSON) |
| `GET /api/explorations/` | Exploration sites (GeoJSON) |
| `GET /api/gisements/` | Mineral deposits (GeoJSON) |
| `GET /api/conflits-usage/` | Land-use conflict scores |
| `GET /api/impact-environnemental/` | Population exposure analysis |
| `GET /api/predictions/` | Regional mining potential |
| `GET /api/stats/` | National statistics |

---

## 👤 Author

**Oumar THIOMBANE** — Fullstack & WebGIS Engineer, Dakar, Senegal

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/oumar-thiombane-a0a51721b/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/vibedarkness)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/devgis-25)

---

## 📄 Data Sources

- USGS National Minerals Information Center (2021) — Public domain
- OpenStreetMap contributors — ODbL License
- WorldPop 2020, University of Southampton — CC BY 4.0

## 📄 License

MIT License