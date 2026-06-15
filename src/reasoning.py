def generate_reasoning(candidate, scores):
    """
    Generate a 1-2 sentence reasoning string using actual candidate data
    and computed scores.
    """
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    years_exp = profile.get("years_of_experience", "N/A")
    current_title = profile.get("current_title", "N/A")
    current_company = profile.get("current_company", "N/A")
    current_industry = profile.get("current_industry", "N/A")

    semantic = scores.get("semantic_score", 0)
    career_fit = scores.get("career_fit_score", 0)

    last_active = signals.get("last_active_date", "unknown")
    response_rate = signals.get("recruiter_response_rate", 0)

    reasoning = (
        f"{years_exp} yrs experience, currently {current_title} at {current_company} "
        f"({current_industry}). Profile-JD semantic fit: {semantic:.2f}, "
        f"career relevance: {career_fit:.2f}. "
        f"Last active {last_active}, recruiter response rate {response_rate:.0%}."
    )

    return reasoning