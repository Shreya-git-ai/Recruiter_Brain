import json

INPUT = "data/candidates.jsonl"
OUTPUT = "data/demo_candidates.jsonl"

LIMIT = 500

with open(INPUT, "r", encoding="utf-8") as fin, open(OUTPUT, "w", encoding="utf-8") as fout:
    for i, line in enumerate(fin):
        if i >= LIMIT:
            break
        fout.write(line)

print(f"Saved {LIMIT} candidates to {OUTPUT}")