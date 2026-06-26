from datetime import datetime


def parse_datetime(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def recency_score(last_active_date_str):
    last_active = parse_datetime(last_active_date_str)
    if last_active is None:
        return 0.0
    days_since = (datetime.now() - last_active).days
    if days_since <= 7:
        return 1.0
    if days_since >= 180:
        return 0.0
    return 1 - (days_since - 7) / (180 - 7)


def compute_location_penalty(candidate):
    """
    Returns 0.5-1.0 multiplier based on location fit with JD.
    Pune/Noida = 1.0, other Indian metros = 0.9,
    India willing to relocate = 0.85, India other = 0.7,
    Outside India = 0.5
    """
    profile = candidate.get("profile", {})
    location = (profile.get("location") or "").lower()
    country = (profile.get("country") or "").lower()
    signals = candidate.get("redrob_signals", {})
    willing_to_relocate = signals.get("willing_to_relocate", False)

    preferred_cities = ["pune", "noida"]
    acceptable_cities = ["mumbai", "hyderabad", "delhi", "gurugram", "gurgaon", "bangalore", "bengaluru"]

    if country != "india":
        return 0.5

    is_preferred = any(city in location for city in preferred_cities)
    is_acceptable = any(city in location for city in acceptable_cities)

    if is_preferred:
        return 1.0
    elif is_acceptable:
        return 0.9
    elif willing_to_relocate:
        return 0.85
    else:
        return 0.7


def compute_signal_score(candidate):
    signals = candidate.get("redrob_signals", {})

    recency = recency_score(signals.get("last_active_date"))
    response_rate = signals.get("recruiter_response_rate", 0.0)
    open_to_work = 1.0 if signals.get("open_to_work_flag", False) else 0.5
    interview_completion = signals.get("interview_completion_rate", 0.0)

    offer_acceptance = signals.get("offer_acceptance_rate", -1)
    if offer_acceptance == -1:
        offer_acceptance = 0.5

    score = (
        0.35 * recency +
        0.25 * response_rate +
        0.15 * open_to_work +
        0.15 * interview_completion +
        0.10 * offer_acceptance
    )

    return round(min(1.0, max(0.0, score)), 4)