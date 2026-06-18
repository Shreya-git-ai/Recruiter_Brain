import time

def run_pipeline(candidates_path, output_path, limit=None, top_n=100):
    t0 = time.time()
    print("Loading candidates...")
    candidates = load_candidates(candidates_path, limit=limit)
    print(f"Loaded {len(candidates)} candidates in {time.time()-t0:.1f}s")

    t1 = time.time()
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    jd_embedding = model.encode(JD_FOCUS_TEXT)
    print(f"Model loaded in {time.time()-t1:.1f}s")

    t2 = time.time()
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
    print(f"Filtering done in {time.time()-t2:.1f}s. Excluded {excluded_count}, {len(valid_candidates)} remain")

    t3 = time.time()
    print("Building candidate texts and embeddings...")
    candidate_texts = [build_candidate_text(c) for c in valid_candidates]
    candidate_embeddings = model.encode(candidate_texts, batch_size=64, show_progress_bar=True)
    print(f"Embedding done in {time.time()-t3:.1f}s")

    t4 = time.time()
    print("Computing semantic scores...")
    semantic_scores = compute_semantic_scores(jd_embedding, candidate_embeddings)
    print(f"Semantic scoring done in {time.time()-t4:.1f}s")

    t5 = time.time()
    print("Computing remaining scores...")
    results = []
    for candidate, sem_score in zip(valid_candidates, semantic_scores):
        kw_score = keyword_match_score(candidate)
        red_flag = compute_red_flag_penalty(candidate)
        signal = compute_signal_score(candidate)
        final = compute_final_score(sem_score, kw_score, red_flag, signal)
        score_dict = {"semantic_score": float(sem_score), "career_fit_score": kw_score, "signal_score": signal}
        reasoning = generate_reasoning(candidate, score_dict)
        results.append({"candidate_id": candidate["candidate_id"], "score": final, "reasoning": reasoning})
    print(f"Scoring loop done in {time.time()-t5:.1f}s")

    # ... rest same as before (sort, save)
    
    print(f"TOTAL TIME: {time.time()-t0:.1f}s")