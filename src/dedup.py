def build_career_signature(candidate):
    """
    Builds a signature string representing the candidate's career
    trajectory - used to detect near-duplicate "behavioral twin" profiles.
    """
    career_history = candidate.get("career_history", [])

    job_signatures = sorted(
        f"{job.get('title', '')}|{job.get('duration_months', 0)}"
        for job in career_history
    )

    return "::".join(job_signatures)


def deduplicate_results(results_with_signatures):
    """
    results_with_signatures: list of dicts, each containing at least
    'signature' and already sorted by final_score descending.

    Removes lower-scoring duplicates that share the same career signature,
    keeping only the highest-scoring one from each duplicate group.
    """
    seen_signatures = set()
    deduped = []

    for result in results_with_signatures:
        signature = result["signature"]

        if signature in seen_signatures:
            continue

        seen_signatures.add(signature)
        deduped.append(result)

    return deduped