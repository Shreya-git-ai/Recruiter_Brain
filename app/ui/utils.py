import pandas as pd
import os
 
 
def _find_project_root():
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(current, "output")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
 
 
_PROJECT_ROOT = _find_project_root()
 
# READ ONLY — sahi final results, kabhi overwrite nahi hogi
FINAL_RESULTS_CSV = os.path.join(_PROJECT_ROOT, "output", "final_ranked_candidates.csv")
 
# Pipeline ka output — alag file, UI se independent
STREAMLIT_OUTPUT_CSV = os.path.join(_PROJECT_ROOT, "outputs", "streamlit_output.csv")
 
 
def load_results():
    """
    Pehle FINAL_RESULTS_CSV padhne ki koshish karo (sahi 100-candidate data).
    Agar woh nahi mili toh STREAMLIT_OUTPUT_CSV se padho (pipeline ka fresh output).
    """
    # Priority 1: original final results
    for csv_path in [FINAL_RESULTS_CSV, STREAMLIT_OUTPUT_CSV]:
        if not os.path.exists(csv_path):
            continue
        try:
            df = pd.read_csv(csv_path)
            required = {"candidate_id", "rank", "score", "reasoning"}
            if not required.issubset(df.columns):
                continue
            if len(df) == 0:
                continue
            return df.sort_values("rank").reset_index(drop=True)
        except Exception:
            continue
    return None
 
 
def detect_dataset_paths():
    data_dir = os.path.join(_PROJECT_ROOT, "data")
 
    full = (
        os.path.join(data_dir, "candidates.jsonl"),
        os.path.join(data_dir, "candidate_embeddings.npy"),
        os.path.join(data_dir, "candidate_ids.npy"),
    )
    demo = (
        os.path.join(data_dir, "demo_candidates.jsonl"),
        os.path.join(data_dir, "demo_candidate_embeddings.npy"),
        os.path.join(data_dir, "demo_candidate_ids.npy"),
    )
 
    if all(os.path.exists(p) for p in full):
        return full[0], full[1], full[2], 2000, False
    return demo[0], demo[1], demo[2], 200, False
 
 
def format_score_color(score):
    if score >= 0.7:
        return "#10b981"
    elif score >= 0.5:
        return "#f59e0b"
    return "#ef4444"