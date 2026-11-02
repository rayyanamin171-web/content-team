#!/usr/bin/env python3
"""Cut a true-colour satellite image out of a free Sentinel-2 scene (AWS Open Data).

Licence: Copernicus Sentinel data is free and open. Required credit on screen:
  "Contains modified Copernicus Sentinel data <year>"
Resolution is 10 m per pixel: great from city to district scale, soft at street scale
(the map module switches to vector buildings when zoomed into an island).

Usage:
  python3 fetch_sentinel.py --scene S2C_40RBN_20261024_0_L2A --bbox 54.28,24.40,54.50,24.56 --out data/abu-dhabi/sentinel.webp
Writes <out> (Web-Mercator .jpg, or .webp with feathered transparent edges) and <out>.json (corner coordinates for MapLibre + credit line).
"""
import argparse, json, os
import numpy as np
import rasterio
from rasterio.warp import transform_bounds, calculate_default_transform, reproject, Resampling
from rasterio.windows import from_bounds
from PIL import Image

BASE = "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs"


def scene_url(scene):
    # S2C_40RBN_20261024_0_L2A -> 40/R/BN/2026/10/<scene>/TCI.tif
    tile, date = scene.split("_")[1], scene.split("_")[2]
    zone, band, sq = tile[:2], tile[2], tile[3:]
    return f"{BASE}/{zone}/{band}/{sq}/{date[:4]}/{int(date[4:6])}/{scene}/TCI.tif"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True)
    ap.add_argument("--bbox", required=True, help="xmin,ymin,xmax,ymax lon/lat")
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=float, default=1.0, help="output pixels per source pixel (1 = 10 m)")
    ap.add_argument("--feather", type=float, default=0.12, help=".webp only: edge fade as a share of the image size")
    a = ap.parse_args()
    bbox = [float(v) for v in a.bbox.split(",")]
    url = scene_url(a.scene)
    env = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
    if os.path.exists("/root/.ccr/ca-bundle.crt"):
        env["CURL_CA_BUNDLE"] = "/root/.ccr/ca-bundle.crt"
    with rasterio.Env(**env):
        with rasterio.open("/vsicurl/" + url) as src:
            l, b, r, t = transform_bounds("EPSG:4326", src.crs, *bbox)
            win = from_bounds(l, b, r, t, src.transform).round_offsets().round_lengths()
            data = src.read(window=win)
            wt = src.window_transform(win)
            # Reproject to Web Mercator so it drops straight into MapLibre as an image source
            dst_crs = "EPSG:3857"
            tr, w, h = calculate_default_transform(src.crs, dst_crs, data.shape[2], data.shape[1],
                                                   *rasterio.transform.array_bounds(data.shape[1], data.shape[2], wt))
            w, h = int(w * a.scale), int(h * a.scale)
            tr = tr * tr.scale(1 / a.scale)
            out = np.zeros((3, h, w), dtype=np.uint8)
            for i in range(3):
                reproject(data[i], out[i], src_transform=wt, src_crs=src.crs, dst_transform=tr, dst_crs=dst_crs,
                          resampling=Resampling.lanczos)
    img = np.transpose(out, (1, 2, 0))
    # Gentle auto-levels (Sentinel TCI is dark); clip at 0.2 / 99.95 percentiles
    lo, hi = np.percentile(img[img.sum(2) > 0], [0.2, 99.95])
    img = np.clip((img.astype(np.float32) - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if a.out.endswith(".webp"):
        # Feathered edges (alpha) so the photo melts into the vector base map while zooming
        valid = (out.sum(0) > 0).astype(np.float32)
        hh, ww = valid.shape
        fe = int(min(hh, ww) * a.feather)
        ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / max(1, fe), 0, 1)
        alpha = np.outer(ramp(hh), ramp(ww)) * valid
        alpha = (alpha * alpha * (3 - 2 * alpha) * 255).astype(np.uint8)
        Image.fromarray(np.dstack([img, alpha]), "RGBA").save(a.out, quality=88, method=4)
    else:
        Image.fromarray(img).save(a.out, quality=90)
    # Corner coordinates in lon/lat (top-left, top-right, bottom-right, bottom-left) for MapLibre
    L, B, R, T = rasterio.transform.array_bounds(h, w, tr)
    from pyproj import Transformer
    f = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True).transform
    corners = [list(f(L, T)), list(f(R, T)), list(f(R, B)), list(f(L, B))]
    year = a.scene.split("_")[2][:4]
    json.dump({"image": os.path.basename(a.out), "coordinates": corners, "scene": a.scene, "source": url,
               "credit": f"Contains modified Copernicus Sentinel data {year}"}, open(a.out + ".json", "w"), indent=1)
    print(f"wrote {a.out} {w}x{h}")


if __name__ == "__main__":
    main()
