from datetime import datetime

def parse_datetime(date_str):
    """
    we will Parse a date string in the format 'YYYY-MM-DD' and returns a datetime object.

    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def recency_score(candidate):
    """
    Calculate recency score from the candidate's redrob_signals.last_active_date.
    """

    signals = candidate.get("redrob_signals", {})
    last_active_date = parse_datetime(signals.get("last_active_date"))
    if not last_active_date:
        return 0.5

    current_date = datetime.now()
    days_since_last_active = (current_date - last_active_date).days
    if days_since_last_active <= 7:
        return 1.0
    if days_since_last_active >= 180:
        return 0.0

    return 1 - (days_since_last_active - 7) / (180 - 7)


def signal_score(candidate):
    signals = candidate.get("redrob_signals", {})
    recency = recency_score(candidate)
    response_rate = signals.get("recruiter_response_rate", 0)
    open_to_work = 1.0 if signals.get("open_to_work_flag", False) else 0.5
    interview_completion = signals.get("interview_completion_rate", 0)
    offer_acceptance = signals.get("offer_acceptance_rate", -1)
    if offer_acceptance == -1:
        offer_acceptance = 0.5  # neutral if no prior offer history
    score = (
        0.35 * recency +
        0.25 * response_rate +
        0.15 * open_to_work +
        0.15 * interview_completion +
        0.10 * offer_acceptance
    )

    # Clamp to 0-1 just in case of any edge cases
    score = max(0.0, min(1.0, score))

    return round(score, 4)


compute_signal_score = signal_score
