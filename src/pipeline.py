import os
import time
import numpy as np
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


def run_pipeline(candidates_path, output_path, embeddings_path, ids_path, limit=None, top_n=100):
    t0 = time.time()
    print("Loading candidates...")
    candidates = load_candidates(candidates_path, limit=limit)
    print(f"Loaded {len(candidates)} candidates in {time.time()-t0:.1f}s")

    t1 = time.time()
    print("Loading precomputed embeddings...")
    all_embeddings = np.load(embeddings_path, allow_pickle=True)
    all_ids = np.load(ids_path, allow_pickle=True)
    id_to_embedding = {cid: emb for cid, emb in zip(all_ids, all_embeddings)}
    print(f"Loaded {len(id_to_embedding)} precomputed embeddings in {time.time()-t1:.1f}s")

    t2 = time.time()
    print("Loading embedding model (for JD encoding only)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    jd_embedding = model.encode(JD_FOCUS_TEXT)
    print(f"Model loaded in {time.time()-t2:.1f}s")

    t3 = time.time()
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

    print(f"Filtering done in {time.time()-t3:.1f}s. Excluded {excluded_count}, {len(valid_candidates)} remain")

    t4 = time.time()
    print("Looking up precomputed embeddings...")
    valid_embeddings = np.array([id_to_embedding[c["candidate_id"]] for c in valid_candidates])
    print(f"Lookup done in {time.time()-t4:.1f}s")

    t5 = time.time()
    print("Computing semantic scores...")
    semantic_scores = compute_semantic_scores(jd_embedding, valid_embeddings)
    print(f"Semantic scoring done in {time.time()-t5:.1f}s")

    t6 = time.time()
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
            "final_score": final,
        }

        reasoning = generate_reasoning(candidate, score_dict)

        results.append({
            "candidate_id": candidate["candidate_id"],
            "score": final,
            "reasoning": reasoning,
        })

    print(f"Scoring loop done in {time.time()-t6:.1f}s")

    t7 = time.time()
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by=["score", "candidate_id"], ascending=[False, True]).head(top_n)
    results_df = results_df.reset_index(drop=True)
    results_df.insert(1, "rank", results_df.index + 1)
    output_df = results_df[["candidate_id", "rank", "score", "reasoning"]]

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    output_df.to_csv(output_path, index=False)
    print(f"Saved top {len(output_df)} candidates to {output_path} in {time.time()-t7:.1f}s")
    print(f"TOTAL TIME: {time.time()-t0:.1f}s")

    return output_df