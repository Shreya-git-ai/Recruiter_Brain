def generate_reasoning(candidate, scores):
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    career_history = candidate.get("career_history", [])
    skills = candidate.get("skills", [])

    years_exp = profile.get("years_of_experience", 0)
    current_title = profile.get("current_title", "N/A")
    current_company = profile.get("current_company", "N/A")
    current_industry = profile.get("current_industry", "N/A")
    location = (profile.get("location") or "")
    country = (profile.get("country") or "").lower()

    semantic = scores.get("semantic_score", 0)
    career_fit = scores.get("career_fit_score", 0)
    signal = scores.get("signal_score", 0)
    final = scores.get("final_score", 0)

    response_rate = signals.get("recruiter_response_rate", 0)
    notice_period = signals.get("notice_period_days", None)
    willing_to_relocate = signals.get("willing_to_relocate", False)
    last_active = signals.get("last_active_date", "unknown")

    # Top skills
    strong_skills = [
        s["name"] for s in skills
        if s.get("proficiency") in ["advanced", "expert"]
    ][:3]

    # Previous company
    prev_jobs = [j for j in career_history if not j.get("is_current") and j.get("company")]
    prev_company = f", previously at {prev_jobs[0]['company']}" if prev_jobs else ""

    # Core strength — varies by career_fit + semantic
    if career_fit >= 0.7 and semantic >= 0.65:
        if strong_skills:
            strength = (
                f"{years_exp:.1f} yrs as {current_title} at {current_company} "
                f"({current_industry}){prev_company}; strong proficiency in "
                f"{', '.join(strong_skills)}"
            )
        else:
            strength = (
                f"{years_exp:.1f} yrs as {current_title} at {current_company} "
                f"({current_industry}){prev_company}"
            )
    elif career_fit >= 0.7 and semantic < 0.65:
        strength = (
            f"{years_exp:.1f} yrs as {current_title} at {current_company}; "
            f"career shows ML/AI production work but JD semantic overlap "
            f"is moderate{prev_company}"
        )
    elif career_fit >= 0.4:
        strength = (
            f"{years_exp:.1f} yrs as {current_title} at {current_company} "
            f"({current_industry}); some AI/ML-adjacent experience evident"
            f"{prev_company}"
        )
    else:
        strength = (
            f"{years_exp:.1f} yrs as {current_title} at {current_company}; "
            f"limited direct evidence of production ML/AI systems"
        )

    # JD semantic alignment — specific, not generic
    if semantic >= 0.72:
        jd_note = "very strong fit with JD's retrieval/ranking/embeddings core"
    elif semantic >= 0.65:
        jd_note = "good fit with JD's production ML emphasis"
    elif semantic >= 0.55:
        jd_note = "moderate alignment with JD's retrieval/search focus"
    else:
        jd_note = "partial overlap with JD requirements"

    # Concerns — specific and varied
    concerns = []

    if years_exp < 5:
        concerns.append(f"at {years_exp:.1f} yrs, below JD's 5-9yr preferred range")
    elif years_exp > 9:
        concerns.append(f"at {years_exp:.1f} yrs, above JD's 5-9yr range")

    if country != "india":
        city = location.split(",")[0] if location else "outside India"
        concerns.append(
            f"based {city} — outside India, JD preference is Pune/Noida"
            if not willing_to_relocate
            else f"based {city}, willing to relocate"
        )

    if notice_period and notice_period > 60:
        concerns.append(f"{notice_period}-day notice period is a concern")
    elif notice_period and 30 < notice_period <= 60:
        concerns.append(f"notice period {notice_period} days, JD prefers sub-30")

    if response_rate < 0.25:
        concerns.append(f"low recruiter response rate ({response_rate:.0%})")

    if response_rate >= 0.85:
        concerns.append(f"highly responsive ({response_rate:.0%} response rate)")

    concern_text = ""
    if concerns:
        concern_text = " Note: " + "; ".join(concerns[:2]) + "."

    reasoning = f"{strength}; {jd_note}.{concern_text}"
    return reasoning