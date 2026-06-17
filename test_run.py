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
from src.signal_score import compute_signal_score

print()
print("--- Signal Score Test (first 5 candidates) ---")
for c in candidates:
    score = compute_signal_score(c)
    last_active = c.get("redrob_signals", {}).get("last_active_date")
    response_rate = c.get("redrob_signals", {}).get("recruiter_response_rate")
    print(f"{c['candidate_id']}: signal_score={score}, last_active={last_active}, response_rate={response_rate}")

from src.career_fit_score import compute_career_fit_score

print()
print("--- Career Fit Score Test (first 5 candidates) ---")
for c in candidates:
    score = compute_career_fit_score(c)
    title = c.get("profile", {}).get("current_title")
    n_jobs = len(c.get("career_history", []))
    print(f"{c['candidate_id']}: career_fit_score={score}, current_title='{title}', num_jobs={n_jobs}")

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from src.data_loader import build_candidate_text
from src.semantic_score import compute_semantic_scores, JD_FOCUS_TEXT

print()
print("--- Semantic Score Test (first 5 candidates) ---")

if SentenceTransformer is None:
    print("Skipping semantic tests: 'sentence-transformers' not installed. Install with `pip install sentence-transformers` to enable.")
    # provide a neutral score list so downstream logic can continue
    scores = [0.0 for _ in candidates]
else:
    model = SentenceTransformer("all-MiniLM-L6-v2")

    jd_embedding = model.encode(JD_FOCUS_TEXT)

    candidate_texts = [build_candidate_text(c) for c in candidates]
    candidate_embeddings = model.encode(candidate_texts)

    scores = compute_semantic_scores(jd_embedding, candidate_embeddings)

    for c, score in zip(candidates, scores):
        title = c.get("profile", {}).get("current_title")
        print(f"{c['candidate_id']}: semantic_score={score:.4f}, current_title='{title}'")

from src.combine import compute_final_score
from src.reasoning import generate_reasoning
from src.signal_score import compute_signal_score
from src.career_fit_score import compute_career_fit_score

print()
print("--- Full Pipeline Test (first 5 candidates) ---")

for c, sem_score in zip(candidates, scores):  # 'scores' from semantic test above
    career_fit = compute_career_fit_score(c)
    signal = compute_signal_score(c)
    final = compute_final_score(sem_score, career_fit, signal)

    score_dict = {
        "semantic_score": float(sem_score),
        "career_fit_score": career_fit,
        "signal_score": signal,
    }

    reasoning = generate_reasoning(c, score_dict)

    print(f"\n{c['candidate_id']} | final_score={final}")
    print(f"  semantic={sem_score:.3f}, career_fit={career_fit:.3f}, signal={signal:.3f}")
    print(f"  Reasoning: {reasoning}")

import argparse
from src.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Redrob Hackathon - Candidate Ranking Pipeline")
    parser.add_argument("--candidates", default="data/candidates.jsonl", help="Path to candidates file")
    parser.add_argument("--output", default="output/ranked_candidates.csv", help="Output CSV path")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of candidates loaded (for testing)")
    parser.add_argument("--top_n", type=int, default=100, help="Number of top candidates to output")

    args = parser.parse_args()

    run_pipeline(
        candidates_path=args.candidates,
        output_path=args.output,
        limit=args.limit,
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()