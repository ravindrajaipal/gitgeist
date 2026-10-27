import numpy as np
import pandas as pd
from pathlib import Path

def generate_dataset(out_path: Path, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = 400
    
    # Features driving software & smart-lab "midnight hauntings" (incidents/regressions)
    commit_hour = rng.integers(0, 24, size=n)
    # 0 to 5 AM commits have high fatigue
    is_witching_hour = ((commit_hour >= 0) & (commit_hour <= 4)).astype(float)
    
    lines_churned = rng.integers(5, 1200, size=n)
    files_touched = rng.integers(1, 28, size=n)
    cyclomatic_delta = np.round(rng.uniform(0.5, 45.0, size=n), 2)
    days_since_last_touch = rng.integers(1, 1460, size=n)  # up to 4 years old ("ancient code")
    prior_authors_count = rng.integers(1, 15, size=n)
    cpu_temp_spike_c = np.round(rng.normal(62.0, 9.5, size=n) + is_witching_hour * 6.5, 1)
    test_coverage_pct = np.round(np.clip(rng.normal(74.0, 18.0, size=n) - is_witching_hour * 14.0, 5.0, 99.0), 1)
    
    # True underlying haunting risk score (0 to 100): probability that a commit/log triggers a post-deploy incident
    # Strongest drivers: witching hour / commit timing, cyclomatic delta, days_since_last_touch (ancient untouched code), low test coverage
    raw_score = (
        18.0
        + 24.5 * is_witching_hour
        + 0.58 * cyclomatic_delta
        + 0.014 * days_since_last_touch
        + 0.012 * lines_churned
        + 0.45 * files_touched
        + 0.28 * np.maximum(0, cpu_temp_spike_c - 65.0)
        - 0.26 * test_coverage_pct
        + rng.normal(0, 3.2, size=n)
    )
    haunting_risk_pct = np.round(np.clip(raw_score, 2.0, 98.5), 1)
    incident_within_48h = (haunting_risk_pct > 55.0).astype(int)
    
    df = pd.DataFrame({
        "commit_hour": commit_hour,
        "is_witching_hour": is_witching_hour.astype(int),
        "lines_churned": lines_churned,
        "files_touched": files_touched,
        "cyclomatic_delta": cyclomatic_delta,
        "days_since_last_touch": days_since_last_touch,
        "prior_authors_count": prior_authors_count,
        "cpu_temp_spike_c": cpu_temp_spike_c,
        "test_coverage_pct": test_coverage_pct,
        "haunting_risk_pct": haunting_risk_pct,
        "incident_within_48h": incident_within_48h,
    })
    df.to_csv(out_path, index=False)
    return df

if __name__ == "__main__":
    generate_dataset(Path(__file__).resolve().parent.parent / "data/haunted_commits_telemetry.csv")
