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

    score = 1 - (days_since - 7) / (180 - 7)
    return score


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

    score = max(0.0, min(1.0, score))
    return round(score, 4)