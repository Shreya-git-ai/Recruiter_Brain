import pandas as pd
from sentence_transformers import SentenceTransformer

from src.data_loader import load_candidates, build_candidate_text
from src.honeypot_detector import run_honeypot_checks
from src.hard_filters import run_hard_filters
from src.career_fit_score import keyword_match_score, compute_red_flag_penalty
from src.signal_score import compute_signal_score
from src.semantic_score import compute_semantic_scores, JD_FOCUS_TEXT
from src.combine import compute_final_score
from src.reasoning import generate_reasoning


def run_pipeline(candidates_path, output_path, limit=None, top_n=100):
    print("Loading candidates...")
    candidates = load_candidates(candidates_path, limit=limit)
    print(f"Loaded {len(candidates)} candidates")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    jd_embedding = model.encode(JD_FOCUS_TEXT)

    print("Running honeypot checks and hard filters...")
    valid_candidates = []
    excluded_count = 0

    for candidate in candidates:
        is_honeypot, _ = run_honeypot_checks(candidate)
        fails_filters, _ = run_hard_filters(candidate)

        if is_honeypot or fails_filters:
            excluded_count += 1
            continue

        valid_candidates.append(candidate)

    print(f"Excluded {excluded_count} candidates")
    print(f"{len(valid_candidates)} candidates remain")

    print("Building candidate texts and embeddings...")
    candidate_texts = [build_candidate_text(c) for c in valid_candidates]
    candidate_embeddings = model.encode(candidate_texts, batch_size=64, show_progress_bar=True)

    print("Computing semantic scores...")
    semantic_scores = compute_semantic_scores(jd_embedding, candidate_embeddings)

    print("Computing remaining scores, final score and reasoning...")
    results = []

    for candidate, sem_score in zip(valid_candidates, semantic_scores):
        kw_score = keyword_match_score(candidate)
        red_flag = compute_red_flag_penalty(candidate)
        signal = compute_signal_score(candidate)

        final = compute_final_score(sem_score, kw_score, red_flag, signal)

        score_dict = {
            "semantic_score": float(sem_score),
            "career_fit_score": kw_score,
            "signal_score": signal,
        }

        reasoning = generate_reasoning(candidate, score_dict)

        results.append({
            "candidate_id": candidate["candidate_id"],
            "final_score": final,
            "reasoning": reasoning,
        })

    print("Sorting and selecting top candidates...")
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("final_score", ascending=False).head(top_n)
    results_df = results_df.reset_index(drop=True)
    results_df["rank"] = results_df.index + 1

    output_df = results_df[["rank", "candidate_id", "final_score", "reasoning"]]
    output_df.to_csv(output_path, index=False)
    print(f"Saved top {top_n} candidates to {output_path}")

    return output_df