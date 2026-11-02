#!/usr/bin/env python3
"""Turn raw downloads into the small, render-ready layers the map module uses.

Inputs (already downloaded):
  data/<city>/land.geojson, water.geojson, roads-major.geojson   (Overture, fetch_overture.py)
  data/<area>/buildings.geojson, roads.geojson                    (Overture, fetch_overture.py)
  Natural Earth 10m GeoJSON folder (public domain)                 (--ne)
Outputs (in data/<area>/render/):
  region-countries.geojson, region-emirates.geojson, region-land.geojson  (Natural Earth, Gulf only)
  city-land.geojson, city-water.geojson, city-roads.geojson               (Overture, slimmed)
  area-buildings.geojson, area-roads.geojson                               (Overture, slimmed)
  island.geojson                                                           (the island outline that contains --point)
  sources.json                                                             (every dataset + licence used → on-screen credit)

Usage:
  python3 prepare_area.py --city data/abu-dhabi --area data/al-maryah --point 54.389,24.4984 --ne /path/to/natural-earth
"""
import argparse, json, os
from shapely.geometry import shape, mapping, box, Point
from shapely import set_precision

REGION = box(44.0, 15.0, 63.0, 32.5)  # Gulf + neighbours, enough for the UAE fly-in


def load(p):
    return json.load(open(p))


def save(p, feats, sources=None):
    json.dump({"type": "FeatureCollection", "features": feats}, open(p, "w"), separators=(",", ":"))
    print(f"  {os.path.basename(p)}: {len(feats)} features, {os.path.getsize(p) // 1024} KB")


def slim(g, tol=0.0):
    if tol:
        g = g.simplify(tol, preserve_topology=True)
    return set_precision(g, 1e-6)


def feat(g, props):
    return {"type": "Feature", "geometry": mapping(g), "properties": props}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", required=True)
    ap.add_argument("--area", required=True)
    ap.add_argument("--point", required=True, help="lon,lat inside the island")
    ap.add_argument("--ne", required=True, help="folder with Natural Earth 10m geojson files")
    a = ap.parse_args()
    out = os.path.join(a.area, "render")
    os.makedirs(out, exist_ok=True)
    srcs = {}

    def note(lst):
        for s in lst or []:
            ds, lic = (s.split("|") + [""])[:2]
            srcs.setdefault(ds, set()).add(lic)

    # Natural Earth (public domain)
    print("Natural Earth")
    feats = []
    for f in load(os.path.join(a.ne, "ne_10m_admin_0_countries.geojson"))["features"]:
        g = shape(f["geometry"])
        if g.intersects(REGION):
            p = f["properties"]
            feats.append(feat(slim(g.intersection(REGION), 0.005), {"name": p.get("NAME_EN") or p.get("NAME"), "iso": p.get("ISO_A3") or p.get("ADM0_A3")}))
    save(os.path.join(out, "region-countries.geojson"), feats)
    feats = []
    for f in load(os.path.join(a.ne, "ne_10m_admin_1_states_provinces.geojson"))["features"]:
        p = f["properties"]
        if p.get("adm0_a3") == "ARE":
            feats.append(feat(slim(shape(f["geometry"]), 0.003), {"name": p.get("name_en") or p.get("name")}))
    save(os.path.join(out, "region-emirates.geojson"), feats)
    feats = [feat(slim(shape(f["geometry"]).intersection(REGION), 0.005), {}) for f in load(os.path.join(a.ne, "ne_10m_land.geojson"))["features"] if shape(f["geometry"]).intersects(REGION)]
    save(os.path.join(out, "region-land.geojson"), feats)
    srcs["Natural Earth"] = {"public domain"}

    # Overture city layers
    print("Overture city layers")
    feats = []
    island = None
    pt = Point(*[float(v) for v in a.point.split(",")])
    for f in load(os.path.join(a.city, "land.geojson"))["features"]:
        p = f["properties"]
        g = shape(f["geometry"])
        if g.geom_type not in ("Polygon", "MultiPolygon"):
            continue
        if p.get("subtype") == "land":
            feats.append(feat(slim(g, 0.00002), {"class": p.get("class")}))
            note(p.get("sources"))
            if p.get("class") == "island" and g.contains(pt) and (island is None or g.area < island[0].area):
                island = (g, p)
    save(os.path.join(out, "city-land.geojson"), feats)
    feats = []
    for f in load(os.path.join(a.city, "water.geojson"))["features"]:
        p = f["properties"]
        g = shape(f["geometry"])
        if g.geom_type in ("Polygon", "MultiPolygon") and p.get("subtype") not in ("human_made",):
            feats.append(feat(slim(g, 0.00002), {"subtype": p.get("subtype")}))
            note(p.get("sources"))
    save(os.path.join(out, "city-water.geojson"), feats)
    feats = []
    for f in load(os.path.join(a.city, "roads-major.geojson"))["features"]:
        p = f["properties"]
        if p.get("subtype") != "road":
            continue
        feats.append(feat(slim(shape(f["geometry"]), 0.00001), {"class": p.get("class")}))
        note(p.get("sources"))
    save(os.path.join(out, "city-roads.geojson"), feats)

    # Overture area layers (street level)
    print("Overture area layers")
    feats = []
    for f in load(os.path.join(a.area, "buildings.geojson"))["features"]:
        p = f["properties"]
        g = shape(f["geometry"])
        if g.geom_type not in ("Polygon", "MultiPolygon"):
            continue
        h = p.get("height") or (p.get("num_floors") or 0) * 3.5 or 8
        feats.append(feat(slim(g), {"h": round(float(h), 1), "name": p.get("name"),
                                     "on_island": bool(island and island[0].buffer(0.0003).contains(g.centroid))}))
        note(p.get("sources"))
    save(os.path.join(out, "area-buildings.geojson"), feats)
    feats = []
    for f in load(os.path.join(a.area, "roads.geojson"))["features"]:
        p = f["properties"]
        if p.get("subtype") != "road":
            continue
        feats.append(feat(slim(shape(f["geometry"])), {"class": p.get("class")}))
        note(p.get("sources"))
    save(os.path.join(out, "area-roads.geojson"), feats)

    if island:
        g, p = island
        save(os.path.join(out, "island.geojson"), [feat(slim(g), {"name": p.get("name"), "id": p.get("id")})])
        c = g.centroid
        print(f"  island centroid: {c.x:.5f},{c.y:.5f}  bounds: {[round(v, 5) for v in g.bounds]}")
    else:
        print("  WARNING: no island polygon contains --point")
    json.dump({k: sorted(v) for k, v in srcs.items()}, open(os.path.join(out, "sources.json"), "w"), indent=1)
    print("  sources:", {k: sorted(v) for k, v in srcs.items()})


if __name__ == "__main__":
    main()
