import os
import pandas as pd

from app.ui import utils


def test_load_results_prefers_submission_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    output_dir = tmp_path / "output"
    outputs_dir = tmp_path / "outputs"
    output_dir.mkdir()
    outputs_dir.mkdir()

    pd.DataFrame([
        {"candidate_id": "CAND_001", "rank": 1, "score": 0.9, "reasoning": "old"}
    ]).to_csv(output_dir / "final_ranked_candidates.csv", index=False)

    pd.DataFrame([
        {"candidate_id": "CAND_002", "rank": 1, "score": 0.95, "reasoning": "correct"}
    ]).to_csv(outputs_dir / "submission.csv", index=False)

    monkeypatch.setattr(utils, "OUTPUT_CSV", str(output_dir / "final_ranked_candidates.csv"))
    monkeypatch.setattr(utils, "SUBMISSION_CSV", str(outputs_dir / "submission.csv"))

    df = utils.load_results()

    assert df is not None
    assert df.iloc[0]["candidate_id"] == "CAND_002"
    assert df.iloc[0]["score"] == 0.95
