def generate_reasoning(candidate, scores):
    """
    Generates varied, JD-connected reasoning that acknowledges concerns
    when present, with tone calibrated to the candidate's overall fit.
    """
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    years_exp = profile.get("years_of_experience", 0)
    current_title = profile.get("current_title", "N/A")
    current_company = profile.get("current_company", "N/A")
    location = profile.get("location", "N/A")

    semantic = scores.get("semantic_score", 0)
    career_fit = scores.get("career_fit_score", 0)
    signal = scores.get("signal_score", 0)
    final = scores.get("final_score", 0)

    last_active = signals.get("last_active_date", "unknown")
    response_rate = signals.get("recruiter_response_rate", 0)
    notice_period = signals.get("notice_period_days", None)
    willing_to_relocate = signals.get("willing_to_relocate", False)

    # Build the core strength statement based on career_fit level
    if career_fit >= 0.7:
        strength = (
            f"{years_exp:.1f} years of experience with strong AI/ML production "
            f"signal in their career history (currently {current_title} at {current_company})"
        )
    elif career_fit >= 0.4:
        strength = (
            f"{years_exp:.1f} years of experience as {current_title} at {current_company}, "
            f"with some AI/ML-relevant work evident in their career history"
        )
    else:
        strength = (
            f"{years_exp:.1f} years of experience as {current_title} at {current_company}; "
            f"limited direct evidence of AI/ML production work in their described roles"
        )

    # JD connection - reference specific JD requirements based on semantic fit
    if semantic >= 0.65:
        jd_connection = (
            "their background closely aligns with the JD's emphasis on "
            "production embeddings/retrieval systems"
        )
    elif semantic >= 0.50:
        jd_connection = (
            "their experience shows partial alignment with the JD's "
            "retrieval/ranking focus, though not a precise match"
        )
    else:
        jd_connection = (
            "the overlap with the JD's core embeddings/retrieval "
            "requirements is weaker"
        )

    # Honest concerns - only included when actually relevant
    concerns = []

    if response_rate < 0.3:
        concerns.append(f"low recruiter response rate ({response_rate:.0%})")

    if notice_period and notice_period > 30:
        concerns.append(
            f"notice period of {notice_period} days exceeds the JD's "
            f"preferred sub-30-day window"
        )

    if not willing_to_relocate and "pune" not in location.lower() and "noida" not in location.lower():
        concerns.append(f"based in {location}, not directly in Pune/Noida")

    if years_exp < 5 or years_exp > 9:
        concerns.append(
            f"experience ({years_exp:.1f} yrs) falls outside the JD's "
            f"stated 5-9 year range"
        )

    concern_text = ""
    if concerns:
        concern_text = " Some concerns: " + "; ".join(concerns) + "."

    reasoning = f"{strength}; {jd_connection}.{concern_text}"

    return reasoning