PRODUCTION_KEYWORDS = [
    "deployed", "production", "shipped", "scaled", "users", "launched",
    "live", "ranking", "retrieval", "search", "recommendation", "embeddings",
    "vector", "latency", "throughput", "a/b test"
]

def production_signal_score(candidate):
    """
    Returns 0-1 score based on how much career_history descriptions
    mention production/deployment-related work.
    """
    career_history = candidate.get("career_history", [])
    if not career_history:
        return 0.0

    all_text = " ".join((job.get("description") or "").lower() for job in career_history)

    hits = sum(1 for kw in PRODUCTION_KEYWORDS if kw in all_text)

    # Cap at 5 hits = full score (1.0). More than 5 doesn't add extra value.
    score = min(hits / 5, 1.0)
    return score

def title_chaser_score(candidate):
    """
    Returns penalty multiplier (0-1). If 3+ jobs with average tenure
    < 18 months, candidate looks like a title-chaser, apply penalty.
    """
    career_history = candidate.get("career_history", [])

    if len(career_history) < 3:
        return 1.0  # not enough jobs to judge - no penalty

    durations = [job.get("duration_months", 0) for job in career_history]
    avg_tenure = sum(durations) / len(durations)

    if avg_tenure < 18:
        return 0.6  # significant penalty
    elif avg_tenure < 24:
        return 0.85  # mild penalty

    return 1.0  # no penalty

def coding_recency_score(candidate):
    """
    Returns penalty multiplier (0-1). If current role is purely
    managerial/architectural with 18+ months tenure, apply penalty.
    """
    profile = candidate.get("profile", {})
    current_title = (profile.get("current_title") or "").lower()

    non_coding_titles = ["manager", "director", "vp", "head of", "architect"]

    is_non_coding_title = any(t in current_title for t in non_coding_titles)

    if not is_non_coding_title:
        return 1.0  # current role sounds hands-on, no penalty

    # Find current job's duration
    career_history = candidate.get("career_history", [])
    current_job = next((job for job in career_history if job.get("is_current")), None)

    if current_job and current_job.get("duration_months", 0) > 18:
        return 0.6  # penalty

    return 1.0

def compute_career_fit_score(candidate):
    """
    Combine career-fit sub-scores into single 0-1 score.
    production_signal is the base; chaser/coding penalties multiply it down.
    """
    production = production_signal_score(candidate)
    chaser_penalty = title_chaser_score(candidate)
    coding_penalty = coding_recency_score(candidate)

    score = production * chaser_penalty * coding_penalty
    return round(score, 4)