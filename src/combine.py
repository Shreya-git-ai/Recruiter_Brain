def compute_experience_penalty(candidate):
    """
    Penalty for candidates outside JD's 5-9 year range.
    Graduated penalty — closer to range = smaller penalty.
    """
    profile = candidate.get("profile", {})
    years_exp = profile.get("years_of_experience", 0)

    if 5 <= years_exp <= 9:
        return 1.0
    elif 4 <= years_exp < 5:
        return 0.88
    elif 9 < years_exp <= 12:
        return 0.88
    elif 3 <= years_exp < 4:
        return 0.75
    elif years_exp > 12:
        return 0.80
    else:
        return 0.65


def compute_final_score(semantic_score, keyword_score, red_flag_penalty, signal_score, location_penalty, exp_penalty):
    """
    Final score combines:
    - technical_fit: semantic (dominant) + keyword (confidence boost)
    - red_flag_penalty: title-chasing, non-coding recency
    - exp_penalty: JD experience range alignment
    - location_penalty: Pune/Noida preference
    - availability_multiplier: behavioral signals, floored at 0.5
    """
    technical_fit = 0.85 * semantic_score + 0.15 * keyword_score
    availability_multiplier = 0.5 + 0.5 * signal_score
    final = technical_fit * red_flag_penalty * exp_penalty * location_penalty * availability_multiplier
    return round(final, 4)