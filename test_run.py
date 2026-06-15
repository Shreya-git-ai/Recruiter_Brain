from src.data_loader import load_candidates, build_candidate_text
from src.honeypot_detector import check_signup_lastactive_dates

# Step 1: Load candidates
candidates = load_candidates("data/candidates.jsonl", limit=5)
print(f"Loaded {len(candidates)} candidates")
print()
print("First candidate ID:", candidates[0]["candidate_id"])
print()
print("Sample text for embedding:")
print(build_candidate_text(candidates[0])[:300])

# Step 2: Honeypot check test on a larger sample
print()
print("--- Honeypot Check Test (2000 candidates) ---")

test_candidates = load_candidates("data/candidates.jsonl", limit=2000)

flagged_count = 0
for c in test_candidates:
    is_honeypot, reasons = check_signup_lastactive_dates(c)
    if is_honeypot:
        flagged_count += 1
        if flagged_count <= 5:
            print(f"{c['candidate_id']}: {reasons}")

print()
print(f"Total flagged out of {len(test_candidates)}: {flagged_count}")


from src.honeypot_detector import run_honeypot_checks

print()
print("--- Honeypot Check Test (2000 candidates) ---")

test_candidates = load_candidates("data/candidates.jsonl", limit=2000)

flagged_count = 0
for c in test_candidates:
    is_honeypot, reasons = run_honeypot_checks(c)
    if is_honeypot:
        flagged_count += 1
        if flagged_count <= 5:  # sirf pehle 5 flagged candidates print karo
            print(f"{c['candidate_id']}: {reasons}")

print()
print(f"Total flagged out of {len(test_candidates)}: {flagged_count}")

from src.hard_filters import run_hard_filters

print()
print("--- Hard Filter Test (2000 candidates) ---")

filtered_count = 0
for c in test_candidates:
    fails, reasons = run_hard_filters(c)
    if fails:
        filtered_count += 1
        if filtered_count <= 5:
            print(f"{c['candidate_id']}: {reasons}")

print()
print(f"Total filtered out of {len(test_candidates)}: {filtered_count}")