from datetime import datetime


def parse_datetime(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def check_signup_lastactive_dates(candidate):
    signals = candidate.get("redrob_signals", {})
    signup_date = parse_datetime(signals.get("signup_date"))
    last_active_date = parse_datetime(signals.get("last_active_date"))

    if signup_date and last_active_date:
        if last_active_date < signup_date:
            reason = (
                f"Last active date {last_active_date.date()} is before "
                f"signup date {signup_date.date()}."
            )
            return True, reason

    return False, None


def check_experience(candidate):
    profile = candidate.get("profile", {})
    year_exp = profile.get("years_of_experience", 0)

    education = candidate.get("education", [])

    if education:
        earliest_start_year = min(e.get("start_year", 9999) for e in education)
        if earliest_start_year != 9999:
            current_year = datetime.now().year
            max_possible_exp = current_year - earliest_start_year

            if year_exp > max_possible_exp + 2:
                reason = (
                    f"years_of_experience ({year_exp}) exceeds max possible "
                    f"experience ({max_possible_exp}) based on education start year."
                )
                return True, reason

    return False, None


def check_overlapping_jobs(candidate):
    career_history = candidate.get("career_history", [])

    current_jobs = [job for job in career_history if job.get("is_current")]
    if len(current_jobs) > 1:
        reason = f"Multiple current jobs found: {[j.get('title') for j in current_jobs]}"
        return True, reason

    parsed_jobs = []
    for job in career_history:
        start_date = parse_datetime(job.get("start_date"))
        end_date_str = job.get("end_date")
        end_date = parse_datetime(end_date_str) if end_date_str else datetime.now()
        if start_date:
            parsed_jobs.append((start_date, end_date, job.get("title")))

    parsed_jobs.sort(key=lambda x: x[0])

    for i in range(len(parsed_jobs) - 1):
        current_end = parsed_jobs[i][1]
        start_next = parsed_jobs[i + 1][0]

        if current_end and start_next < current_end:
            overlap_days = (current_end - start_next).days
            if overlap_days > 60:
                reason = (
                    f"Job '{parsed_jobs[i][2]}' overlaps with next job "
                    f"'{parsed_jobs[i+1][2]}' by {overlap_days} days."
                )
                return True, reason

    return False, None


def check_skill_duration_mismatch(candidate):
    career_history = candidate.get("career_history", [])
    total_months = sum(job.get("duration_months", 0) for job in career_history)

    skills = candidate.get("skills", [])
    for skill in skills:
        skill_months = skill.get("duration_months", 0)
        if total_months > 0 and skill_months > total_months + 24:
            reason = (
                f"Skill '{skill.get('name')}' duration ({skill_months} mo) "
                f"exceeds total career duration ({total_months} mo)."
            )
            return True, reason

    return False, None


def run_honeypot_checks(candidate):
    checks = [
        check_signup_lastactive_dates,
        check_experience,
        check_overlapping_jobs,
        check_skill_duration_mismatch,
    ]

    reasons = []
    for check_function in checks:
        flagged, reason = check_function(candidate)
        if flagged:
            reasons.append(reason)

    is_honeypot = len(reasons) > 0
    return is_honeypot, reasons