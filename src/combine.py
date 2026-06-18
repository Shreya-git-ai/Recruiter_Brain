def compute_final_score(semantic_score, keyword_score, red_flag_penalty, signal_score):
    """
    technical_fit blends meaning-based similarity (primary signal) with
    domain-specific keyword evidence (secondary confidence boost).

    red_flag_penalty (title-chasing, non-coding role) multiplies down.
    availability_multiplier (behavioral signals) multiplies down further
    with a floor of 0.5, so availability down-weights but never zeroes
    out an otherwise strong candidate.
    """
    technical_fit = 0.85 * semantic_score + 0.15 * keyword_score
    availability_multiplier = 0.5 + 0.5 * signal_score
    final = technical_fit * red_flag_penalty * availability_multiplier
    return round(final, 4)