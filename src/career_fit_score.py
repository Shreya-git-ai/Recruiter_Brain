AI_ML_KEYWORDS = [
    "embedding", "vector database", "vector search", "retrieval",
    "rerank", "ranking model", "recommend", "recommendation",
    "search relevance", "semantic search", "pinecone", "weaviate",
    "qdrant", "milvus", "faiss", "opensearch", "elasticsearch",
    "llm", "language model", "transformer", "sentence-transformers",
    "model serving", "ml inference", "ndcg", "mrr", "evaluation framework",
    "feature engineering", "training pipeline", "machine learning model",
    "nlp", "natural language processing", "information retrieval"
]


def keyword_match_score(candidate):
    career_history = candidate.get("career_history", [])
    if not career_history:
        return 0.0

    all_text = " ".join((job.get("description") or "").lower() for job in career_history)
    hits = sum(1 for kw in AI_ML_KEYWORDS if kw in all_text)
    score = min(hits / 7, 1.0)  # changed from /4 to /7
    return score


def title_chaser_score(candidate):
    career_history = candidate.get("career_history", [])
    if len(career_history) < 3:
        return 1.0

    durations = [job.get("duration_months", 0) for job in career_history]
    avg_tenure = sum(durations) / len(durations)

    if avg_tenure < 18:
        return 0.6
    elif avg_tenure < 24:
        return 0.85
    return 1.0


def coding_recency_score(candidate):
    profile = candidate.get("profile", {})
    current_title = (profile.get("current_title") or "").lower()
    non_coding_titles = ["manager", "director", "vp", "head of", "architect"]
    is_non_coding_title = any(t in current_title for t in non_coding_titles)

    if not is_non_coding_title:
        return 1.0

    career_history = candidate.get("career_history", [])
    current_job = next((job for job in career_history if job.get("is_current")), None)

    if current_job and current_job.get("duration_months", 0) > 18:
        return 0.6
    return 1.0


def compute_red_flag_penalty(candidate):
    """
    Multiplicative penalty (0.36 to 1.0) from title-chasing and
    non-coding-recency red flags.
    """
    return title_chaser_score(candidate) * coding_recency_score(candidate)