#!/usr/bin/env python3
"""Semantic search over game-icons SVG names. usage: ./iconsearch.py explosion [N]"""
import sys, pathlib, pickle, numpy as np
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

q = model.encode([" ".join(sys.argv[1:2] or ["explosion"])])[0]
q /= np.linalg.norm(q)
for i in (vecs @ q).argsort()[::-1][: int(sys.argv[2]) if len(sys.argv) > 2 else 30]:
    print(f"{vecs[i] @ q:.3f}  {names[i]:28} {paths[i].relative_to(ROOT)}")
