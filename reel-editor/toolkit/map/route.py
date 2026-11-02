#!/usr/bin/env python3
"""Indicative route line between two points along OSM roads (Overture), for a map callout's "path".

  python3 route.py --roads data/al-maryah/render/area-roads.geojson data/al-maryah/render/city-roads.geojson \
                   --from 54.39026,24.50218 --to 54.39814,24.53370 [--scene scenes/x.json --callout 0]

Prints the road length and (with --scene) writes the simplified path into that callout.
IMPORTANT: this is the shortest path on the road geometry, ignoring one-way streets, turn bans and traffic.
Use it for the *shape* of a route only. Don't put its km on screen as a "driving distance", and never
turn it into a drive time. Drive times must be verified separately.
"""
import argparse, json, math
import networkx as nx
from shapely.geometry import LineString


def hav(a, b):
    r = math.pi / 180
    h = math.sin((b[1] - a[1]) * r / 2) ** 2 + math.cos(a[1] * r) * math.cos(b[1] * r) * math.sin((b[0] - a[0]) * r / 2) ** 2
    return 2 * 6371008.8 * math.asin(math.sqrt(h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roads", nargs="+", required=True)
    ap.add_argument("--from", dest="a", required=True)
    ap.add_argument("--to", dest="b", required=True)
    ap.add_argument("--scene")
    ap.add_argument("--callout", type=int, default=0)
    a = ap.parse_args()
    G = nx.Graph()
    key = lambda c: (round(c[0], 6), round(c[1], 6))
    for path in a.roads:
        for f in json.load(open(path))["features"]:
            g = f["geometry"]
            lines = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"] if g["type"] == "MultiLineString" else []
            for ln in lines:
                for p, q in zip(ln, ln[1:]):
                    G.add_edge(key(p), key(q), w=hav(p, q))
    # keep the largest connected piece so snapping can't land on an isolated stub
    G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    nodes = list(G.nodes)
    snap = lambda pt: min(nodes, key=lambda n: hav(n, pt))
    A, B = [float(v) for v in a.a.split(",")], [float(v) for v in a.b.split(",")]
    sa, sb = snap(A), snap(B)
    p = nx.shortest_path(G, sa, sb, weight="w")
    km = sum(hav(x, y) for x, y in zip(p, p[1:])) / 1000
    simp = list(LineString(p).simplify(0.00008).coords)
    print(f"snap: start {hav(sa, A):.0f} m, end {hav(sb, B):.0f} m from the points · road path {km:.2f} km · {len(simp)} vertices")
    print("(indicative shape only; not a verified driving distance)")
    if max(hav(sa, A), hav(sb, B)) > 150:
        print("WARNING: an end point snapped more than 150 m away. Fetch street-level roads around it "
              "(fetch_overture.py --theme transportation --type segment) and re-run, or don't use this path.")
    if a.scene:
        s = json.load(open(a.scene))
        s["callouts"][a.callout]["path"] = [[round(x, 6), round(y, 6)] for x, y in simp]
        json.dump(s, open(a.scene, "w"), indent=2, ensure_ascii=False)
        print(f"wrote path into {a.scene} callout {a.callout}")
    else:
        print(json.dumps([[round(x, 6), round(y, 6)] for x, y in simp]))


if __name__ == "__main__":
    main()
