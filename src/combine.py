def compute_final_score(semantic_score, keyword_score, red_flag_deduction, signal_score):
    technical_fit = 0.55 * semantic_score + 0.45 * keyword_score
    
    # Additive penalty - subtract, don't multiply, so one red flag 
    # doesn't collapse an otherwise strong candidate
    adjusted_fit = max(0.0, technical_fit - red_flag_deduction)
    
    # Multiplicative availability with floor - soft down-weight, never zero
    availability_multiplier = 0.5 + 0.5 * signal_score
    
    final = adjusted_fit * availability_multiplier
    return round(final, 4)