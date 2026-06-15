import gzip
import json


def load_candidates(filepath, limit=None):
    """
    Load candidates from a JSONL file (gzipped or plain).
    limit: if set, only loads first N candidates (useful for testing).
    """
    candidates = []

    if filepath.endswith(".gz"):
        opener = gzip.open(filepath, "rt", encoding="utf-8")
    else:
        opener = open(filepath, "r", encoding="utf-8")

    with opener as f:
        for line in f:
            if limit is not None and len(candidates) >= limit:
                break
            candidate = json.loads(line)
            candidates.append(candidate)
            

    return candidates


def build_candidate_text(candidate):
    """
    Combine relevant text fields into one string for embedding.
    We avoid using raw 'skills' list to prevent keyword-stuffing bias.
    """
    profile = candidate.get("profile", {})
    summary = profile.get("summary", "")
    headline = profile.get("headline", "")
    current_title = profile.get("current_title", "")

    career_descriptions = " ".join(
        job.get("description", "") for job in candidate.get("career_history", [])
    )

    combined = f"{headline}. {current_title}. {summary} {career_descriptions}"
    return combined.strip()