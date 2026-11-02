# Map data & software: sources and licences

Every map frame shows a credit line built from `data/<area>/render/sources.json`, e.g.
"Map data © OpenStreetMap contributors (ODbL), via Overture Maps Foundation · Natural Earth · Contains modified Copernicus Sentinel data 2026".
**Never crop it out.** Keep it in the Reel's IG caption too if a credit gets cut in an edit.

| Layer | Source | Licence | Credit required |
|---|---|---|---|
| Coastline, water, roads, buildings (incl. heights), island outline | [Overture Maps](https://overturemaps.org) release `2026-10-21.0` (data from OpenStreetMap, plus TomTom / Microsoft ML Buildings contributed under ODbL) | ODbL 1.0 | "© OpenStreetMap contributors", Overture Maps Foundation |
| Landmark points (place names) | Overture Maps places | CDLA-Permissive-2.0 | Overture Maps Foundation |
| Country / emirate outlines | [Natural Earth](https://www.naturalearthdata.com) 10m | Public domain | Not required (credited anyway) |
| Satellite image | Copernicus **Sentinel-2 L2A**, scene `S2C_40RBN_20261017_0_L2A` (17 Oct 2026, cloud-free), via [AWS Open Data](https://registry.opendata.aws/sentinel-2-l2a-cogs/) | Copernicus free & open licence | "Contains modified Copernicus Sentinel data 2026" |

| Software | Licence |
|---|---|
| MapLibre GL JS 5.24.0 (`../vendor/maplibre-gl.js`) | BSD-3-Clause (`../vendor/LICENSE-maplibre.txt`) |
| GSAP 3.15.0 (`../vendor/gsap.min.js`) | GSAP standard "no charge" licence |
| Playfair Display, Inter (`../fonts/`) | SIL Open Font License 1.1 |
| HyperFrames, Playwright, FFmpeg, pyarrow, rasterio, shapely | Open source (Apache-2.0 / MIT / LGPL / BSD) |

ODbL note: we display the data as a rendered image (a "Produced Work"), which only needs the attribution above. If we ever share the modified GeoJSON itself publicly, it must stay under ODbL.

## Verified on-screen facts in the Al Maryah demo
- ADGM Square towers (Al Maqam, Al Sila, Al Sarab, Al Khatem), The Galleria and Cleveland Clinic Abu Dhabi **are located on Al Maryah Island**: positions from OSM/Overture (place confidence ≥ 0.98 for Galleria and Cleveland Clinic).
- **≈ 3.6 km straight line** from the island's centroid (54.39026, 24.50218) to Louvre Abu Dhabi (54.39814, 24.53370): haversine distance computed from those coordinates. It is **not** a driving distance.
