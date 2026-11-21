import sys
from collections import Counter

sys.path.insert(0, ".")
from attackgen.emitter import render
from attackgen.parser import parse, parse_file

original = parse_file(r"../CSV/Attack/PHMOD-MeteorMayhem.csv")
text = render(original)
again = parse(text, "roundtrip")

kinds = lambda s: [type(c).__name__ for c in s.commands if type(c).__name__ != "Raw"]
a, b = kinds(original), kinds(again)
print("original", len(a), Counter(a))
print("again   ", len(b), Counter(b))
for i, (x, y) in enumerate(zip(a, b)):
    if x != y:
        print("first diff at", i, x, y)
        break
print("---- rendered head ----")
print("\n".join(text.splitlines()[:12]))
