import pandas as pd
from sentence_transformers import SentenceTransformer

from src.data_loader import load_candidates, build_candidate_text
from src.honeypot_detector import run_honeypot_checks
from src.hard_filters import run_hard_filters
from src.career_fit_score import compute_career_fit_score
from src.signal_score import compute_signal_score
from src.semantic_score import compute_semantic_scores, JD_FOCUS_TEXT
from src.combine import compute_final_score
from src.reasoning import generate_reasoning


def run_pipeline(candidates_path, output_path, limit=None, top_n=100):
    # Step 1: Load candidates
    print("Loading candidates...")
    candidates = load_candidates(candidates_path, limit=limit)
    print(f"Loaded {len(candidates)} candidates")

    # Step 2: Load model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    jd_embedding = model.encode(JD_FOCUS_TEXT)
    print("Running honeypot checks and hard filters...")    
    valid_candidates = []
    excluded_count = 0

    for candidate in candidates:
        # Honeypot checks
        is_honeypot, honeypot_reasons = run_honeypot_checks(candidate)
        if is_honeypot:
            excluded_count += 1
            continue

        # Hard filters
        fails_filters, filter_reasons = run_hard_filters(candidate)
        if fails_filters:
            excluded_count += 1
            continue

        valid_candidates.append(candidate)
        print(f"Excluded {excluded_count} candidates")
        print(f"{len(valid_candidates)} candidates remain")

        #build text and embed in batch after loop for efficiency
        print("Building candidate texts and embeddings...")
        candidate_texts = [build_candidate_text(c) for c in valid_candidates]
        candidate_embeddings = model.encode(candidate_texts,batch_size=64, show_progress_bar=True)

        #compute semantic scores
        print("Computing semantic scores...")
        semantic_scores = compute_semantic_scores(jd_embedding, candidate_embeddings)

        #compute remaining scores, combine and generate reasoning
        print("Computing remaining scores, final score and reasoning...")
        output_rows = []
        for c, sem_score in zip(valid_candidates, semantic_scores):
            career_fit = compute_career_fit_score(c)
            signal_score = compute_signal_score(c)
            final_score = compute_final_score(sem_score, career_fit, signal_score)
            reasoning = generate_reasoning(c, {
                "semantic_score": sem_score,
                "career_fit_score": career_fit,
                "signal_score": signal_score
            })

            output_rows.append({
                "candidate_id": c.get("candidate_id"),
                "final_score": final_score,
                "reasoning": reasoning
            })
        # Save to CSV
        print(f"Saving top {top_n} candidates to {output_path}...")
        output_df = pd.DataFrame(output_rows)
        output_df = output_df.sort_values(by="final_score", ascending=False).head(top_n
        )        
        output_df.to_csv(output_path, index=False)
        print("Pipeline completed successfully.")   

