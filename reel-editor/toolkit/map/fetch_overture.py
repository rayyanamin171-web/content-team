#!/usr/bin/env python3
"""Download Overture Maps features for a bounding box and save them as GeoJSON.

Overture Maps is free open data on AWS S3 (no account, no API key).
Licences: base/transportation/buildings are mostly ODbL (from OpenStreetMap),
places are CDLA-Permissive-2.0. Every output keeps each feature's source dataset
so attribution can be generated automatically (see attribution.py).

Usage:
  python3 fetch_overture.py --bbox 54.25,24.38,54.62,24.60 --theme transportation --type segment --out data/abu-dhabi/roads.geojson
  python3 fetch_overture.py --bbox ... --theme buildings --type building --out data/al-maryah/buildings.geojson

Works through the session's HTTPS proxy if HTTPS_PROXY is set (cloud), or directly (Rayan's Mac).
"""
import argparse, json, os, sys, urllib.parse as up
from concurrent.futures import ThreadPoolExecutor

import pyarrow.dataset as ds
import pyarrow.fs as pafs
import pyarrow.compute as pc
from shapely import wkb
from shapely.geometry import mapping, box

RELEASE = os.environ.get("OVERTURE_RELEASE", "2026-10-21.0")
BUCKET = "overturemaps-us-west-2"

# Only the columns we need per type (keeps downloads small)
COLUMNS = {
    "segment": ["id", "geometry", "bbox", "subtype", "class", "names", "sources"],
    "connector": ["id", "geometry", "bbox"],
    "building": ["id", "geometry", "bbox", "names", "height", "num_floors", "class", "sources"],
    "place": ["id", "geometry", "bbox", "names", "basic_category", "taxonomy", "confidence", "sources"],
    "land": ["id", "geometry", "bbox", "subtype", "class", "names", "sources"],
    "water": ["id", "geometry", "bbox", "subtype", "class", "names", "sources"],
    "land_use": ["id", "geometry", "bbox", "subtype", "class", "names", "sources"],
    "infrastructure": ["id", "geometry", "bbox", "subtype", "class", "names", "sources"],
    "division_area": ["id", "geometry", "bbox", "subtype", "class", "names", "country", "region", "sources"],
}


def s3fs():
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    kw = dict(anonymous=True, region="us-west-2")
    if proxy:
        p = up.urlparse(proxy)
        po = {"scheme": p.scheme, "host": p.hostname, "port": p.port}
        if p.username:
            po.update(username=up.unquote(p.username), password=up.unquote(p.password or ""))
        kw["proxy_options"] = po
    return pafs.S3FileSystem(**kw)


def simplify_sources(srcs):
    return sorted({f"{s.get('dataset')}|{s.get('license') or ''}" for s in (srcs or []) if s})


def to_props(row, ftype):
    names = row.get("names") or {}
    props = {"id": row["id"], "name": names.get("primary") if isinstance(names, dict) else None}
    for k in ("subtype", "class", "height", "num_floors", "basic_category", "confidence", "country", "region"):
        if k in row and row[k] is not None:
            props[k] = row[k]
    if ftype == "place" and row.get("taxonomy"):
        props["category"] = (row["taxonomy"] or {}).get("primary")
    props["sources"] = simplify_sources(row.get("sources"))
    return props


def fetch(theme, ftype, bbox, out, clip=True, name_filter=None, classes=None):
    xmin, ymin, xmax, ymax = bbox
    fs = s3fs()
    path = f"{BUCKET}/release/{RELEASE}/theme={theme}/type={ftype}/"
    files = [f.path for f in fs.get_file_info(pafs.FileSelector(path)) if f.path.endswith(".parquet")]
    cols = COLUMNS.get(ftype, ["id", "geometry", "bbox", "names", "sources"])
    flt = (
        (pc.field("bbox", "xmin") <= xmax) & (pc.field("bbox", "xmax") >= xmin)
        & (pc.field("bbox", "ymin") <= ymax) & (pc.field("bbox", "ymax") >= ymin)
    )
    clipbox = box(xmin, ymin, xmax, ymax)

    def one(fp):
        d = ds.dataset(fp, filesystem=fs, format="parquet")
        names = d.schema.names
        t = d.to_table(columns=[c for c in cols if c in names], filter=flt)
        return t.to_pylist()

    rows = []
    with ThreadPoolExecutor(16) as ex:
        for i, part in enumerate(ex.map(one, files)):
            rows.extend(part)
            print(f"\r{theme}/{ftype}: {i + 1}/{len(files)} files, {len(rows)} features", end="", file=sys.stderr)
    print(file=sys.stderr)

    feats = []
    for r in rows:
        g = wkb.loads(r["geometry"])
        props = to_props(r, ftype)
        if classes and props.get("class") not in classes:
            continue
        if name_filter and not (props.get("name") and any(n.lower() in props["name"].lower() for n in name_filter)):
            continue
        if clip and g.geom_type not in ("Point", "MultiPoint"):
            g = g.intersection(clipbox)
            if g.is_empty:
                continue
        feats.append({"type": "Feature", "geometry": mapping(g), "properties": props})
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"type": "FeatureCollection", "features": feats,
                   "meta": {"source": f"Overture Maps {RELEASE} {theme}/{ftype}", "bbox": bbox}}, f)
    print(f"wrote {out}: {len(feats)} features", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bbox", required=True, help="xmin,ymin,xmax,ymax (lon/lat)")
    ap.add_argument("--theme", required=True)
    ap.add_argument("--type", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-clip", action="store_true")
    ap.add_argument("--name", action="append", help="keep only features whose name contains this (repeatable)")
    ap.add_argument("--class", dest="classes", help="comma list, e.g. motorway,trunk,primary")
    a = ap.parse_args()
    fetch(a.theme, a.type, [float(v) for v in a.bbox.split(",")], a.out, not a.no_clip, a.name, a.classes.split(",") if a.classes else None)
