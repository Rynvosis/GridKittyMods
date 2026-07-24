#!/usr/bin/env python3
"""Semantic search over game-icons SVG names, with positive and negative concepts.

  ./iconsearch.py rocky barren                    positives only
  ./iconsearch.py rocky barren -n skull death     push away from skull/death
  ./iconsearch.py "dead planet" lifeless -n life bones -k 50 -w 1.5

Each positional arg is a positive concept; each -n arg a negative concept. Every
concept is encoded and unit-normalised on its own, then averaged, so multi-word
concepts ("dead planet") count once. The query vector is
mean(positives) - w*mean(negatives), and results rank by cosine to it.
  -k/--top   how many to print (default 30)
  -w/--neg-weight   strength of the negative subtraction (default 1.0)
"""
import pathlib, pickle, argparse, numpy as np
from model2vec import StaticModel

ROOT = pathlib.Path(__file__).parent
CACHE = ROOT / ".iconsearch.pkl"

model = StaticModel.from_pretrained("minishlab/potion-base-8M")
paths = sorted(ROOT.rglob("game-icons/**/*.svg"))
names = [p.stem.replace("-", " ") for p in paths]

if CACHE.exists() and (c := pickle.loads(CACHE.read_bytes()))["names"] == names:
    vecs = c["vecs"]
else:
    vecs = model.encode(names)
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    CACHE.write_bytes(pickle.dumps({"names": names, "vecs": vecs}))

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("pos", nargs="*", default=["explosion"], help="positive concept(s)")
ap.add_argument("-n", "--neg", nargs="*", default=[], help="negative concept(s) to push away from")
ap.add_argument("-k", "--top", type=int, default=30, help="number of results (default 30)")
ap.add_argument("-w", "--neg-weight", type=float, default=1.0, help="negative strength (default 1.0)")
a = ap.parse_args()

def centroid(terms):
    v = model.encode(terms)
    v = v / np.linalg.norm(v, axis=1, keepdims=True)
    return v.mean(0)

q = centroid(a.pos or ["explosion"])
if a.neg:
    q = q - a.neg_weight * centroid(a.neg)
q /= np.linalg.norm(q)

for i in (vecs @ q).argsort()[::-1][: a.top]:
    print(f"{vecs[i] @ q:.3f}  {names[i]:28} {paths[i].relative_to(ROOT)}")
