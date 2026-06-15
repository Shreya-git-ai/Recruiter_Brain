def compute_final_score(semantic_score, career_fit_score, signal_score):
    """
    Combines the three component scores into a final ranking score.

    - semantic_score and career_fit_score are weighted equally (50/50) -
      "does the actual experience match" and "is the career trajectory
      a good fit" matter equally.

    - signal_score (availability) acts as a MULTIPLIER, not an additive
      component. Range 0.5-1.0 means a highly unavailable candidate gets
      at most 50% of their base score - down-weighted, not zeroed out.
    """
    base_score = 0.5 * semantic_score + 0.5 * career_fit_score
    availability_multiplier = 0.5 + 0.5 * signal_score
    final = base_score * availability_multiplier
    return round(final, 4)