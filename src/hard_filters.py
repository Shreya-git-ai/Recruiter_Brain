def fails_location_filter(candidate):
    """
    we will check eligibilty based on lacation as per JD
    if in india candidate is nit in eligible cities and doesnt agree to relocate exclude them
    also if not indian we will not consider
    """
    profile = candidate.get("profile", {})
    location = profile.get("location", "").lower()
    country = profile.get("country", "").lower()

    signals = candidate.get("redrob_signals", {})
    willing_to_relocate = signals.get("willing_to_relocate", False)

    eligible_cities = ["noida", "pune", "mumbai", "hyderabad", "delhi", "gurugram", "gurgaon", "ghaziabad", "faridabad"]

    if country != "india":
        return False  # outside India - not hard-excluded, case-by-case

    is_eligible_city = any(city in location for city in eligible_cities)

    if not is_eligible_city and not willing_to_relocate:
        return True  # exclude

    return False


def fails_pure_consulting_filter(candidate):
    """
    Returns True if jobs in career_history are all consulating firms
    (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini, etc.) 
    without any product company experience.
    """
    career_history = candidate.get("career_history", [])
    if not career_history:
        return False

    consulting_firms = {"tcs", "infosys", "wipro", "hcl", "l&t infotech", "accenture", "cognizant", "capgemini"}

    all_consulting = all(
        any(firm in (job.get("company", "")).lower() for firm in consulting_firms)
        for job in career_history
    )

    return all_consulting


def fails_pure_research_filter(candidate):
    """
    Returns True agar career_history ki SAARI jobs research/academic
    institutions me hain (no product-company experience).
    """
    career_history = candidate.get("career_history", [])
    if not career_history:
        return False

    research_keywords = {"research", "institute", "university", "iit", "iisc", "lab", "academia"}

    all_research = all(
        any(kw in (job.get("company", "") + " " + job.get("industry", "")).lower() for kw in research_keywords)
        for job in career_history
    )

    return all_research

def run_hard_filters(candidate):
    """
    runs all hard filter definitions we have coded till now.
    """
    reasons = []

    if fails_location_filter(candidate):
        reasons.append("location not eligible and not willing to relocate")

    if fails_pure_consulting_filter(candidate):
        reasons.append("entire career history is at consulting firms only")

    if fails_pure_research_filter(candidate):
        reasons.append("entire career history is research/academic only")

    fails = len(reasons) > 0
    return fails, reasons

def fails_ai_domain_filter(candidate):
    """
    FINAL SUBMISSION-GRADE AI FILTER
    Strictly enforces AI/ML relevance before scoring.
    """

    profile = candidate.get("profile", {})
    career_history = candidate.get("career_history", [])

    current_title = (profile.get("current_title") or "").lower()
    current_industry = (profile.get("current_industry") or "").lower()

    ai_core_keywords = [
        "machine learning", "ml engineer", "ai engineer", "data scientist",
        "nlp", "recommendation", "ranking", "search", "retrieval",
        "embedding", "vector", "deep learning", "llm"
    ]

   