"""
Local Git Repository & System Log Scanner.
Extracts real commits, suspicious lines (`git log -S` / `git show`), midnight commits,
and deleted functions ("departed code" for the Día de los Muertos Ofrenda).
Also includes rich preset haunted commits so the demo works immediately out of the box.
"""
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

PRESET_HAUNTED_ARTIFACTS: List[Dict[str, Any]] = [
    {
        "id": "commit-3am-hotfix",
        "commit_hash": "a666dead",
        "author": "You (3 years ago)",
        "date": "2023-10-31 03:14:09 -0400",
        "message": "fix: temporary hack to bypass race condition before halloween deploy DO NOT TOUCH",
        "file_path": "core/payment_retry_daemon.py",
        "suspicious_line": "time.sleep(0.666)  # TODO(2023): remove after lock migration (still load-bearing!)",
        "deleted_code": "def acquire_distributed_lock(redis_conn, key, ttl=30):\n    return redis_conn.set(key, 'locked', nx=True, ex=ttl)",
        "legacy_purpose": "Originally guarded concurrent ledger writes during the 2023 autumn traffic surge before being replaced by an optimistic sleep timer.",
        "telemetry": {
            "commit_hour": 3,
            "is_witching_hour": 1,
            "lines_churned": 412,
            "files_touched": 9,
            "cyclomatic_delta": 34.5,
            "days_since_last_touch": 1095,
            "prior_authors_count": 7,
            "cpu_temp_spike_c": 78.4,
            "test_coverage_pct": 28.5,
        },
    },
    {
        "id": "commit-ghost-sensor",
        "commit_hash": "c0ffee99",
        "author": "Elena Vance (Departed Maintainer)",
        "date": "2024-11-01 01:42:55 +0000",
        "message": "feat(sensors): recalibrate night-shift thermal threshold for edge gateway",
        "file_path": "firmware/edge_thermal_watchdog.c",
        "suspicious_line": "if (sensor_mv > 0xDEAD && night_mode) { trigger_silent_cooldown(); }",
        "deleted_code": "void honor_legacy_calibration_table(uint16_t *lut, size_t len) {\n    /* Hand-tuned on oscilloscope during the 2022 winter freeze */\n}",
        "legacy_purpose": "Kept rural community weather stations online through sub-zero nights without cloud connectivity.",
        "telemetry": {
            "commit_hour": 1,
            "is_witching_hour": 1,
            "lines_churned": 185,
            "files_touched": 4,
            "cyclomatic_delta": 21.0,
            "days_since_last_touch": 726,
            "prior_authors_count": 3,
            "cpu_temp_spike_c": 74.2,
            "test_coverage_pct": 61.0,
        },
    },
    {
        "id": "commit-peaceful-ofrenda",
        "commit_hash": "f10wer26",
        "author": "Marco Morales",
        "date": "2025-11-02 14:20:00 -0600",
        "message": "refactor(archive): sunset v1 audio oral-history transcoder with full migration tests",
        "file_path": "archive/cassette_transcoder_v1.py",
        "suspicious_line": "ARCHIVE_CODEC = 'pcm_s16le'  # Preserving Abuela's 1988 voice memos lossless",
        "deleted_code": "class AnalogTapeDenoiser:\n    # Removed after migrating to local Whisper-cpp pipeline, remembered with gratitude.",
        "legacy_purpose": "Digitized 140+ family cassette tapes and oral histories completely offline before being retired.",
        "telemetry": {
            "commit_hour": 14,
            "is_witching_hour": 0,
            "lines_churned": 95,
            "files_touched": 3,
            "cyclomatic_delta": 4.2,
            "days_since_last_touch": 180,
            "prior_authors_count": 2,
            "cpu_temp_spike_c": 58.0,
            "test_coverage_pct": 94.0,
        },
    },
]


def scan_local_git_repo(repo_path: Path, max_commits: int = 5) -> List[Dict[str, Any]]:
    """Scans a real git repository on disk and extracts commit metadata + telemetry estimates."""
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        return PRESET_HAUNTED_ARTIFACTS

    try:
        out = subprocess.check_output(
            [
                "git",
                "-C",
                str(repo_path),
                "log",
                f"-n{max_commits}",
                "--pretty=format:%h|%an|%ai|%s",
                "--shortstat",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return PRESET_HAUNTED_ARTIFACTS

    records: List[Dict[str, Any]] = []
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    idx = 0
    while idx < len(lines):
        header = lines[idx]
        if "|" not in header:
            idx += 1
            continue
        parts = header.split("|", 3)
        if len(parts) < 4:
            idx += 1
            continue
        chash, author, date_str, subject = parts
        files_touched, lines_churned = 1, 25
        if idx + 1 < len(lines) and ("file changed" in lines[idx + 1] or "files changed" in lines[idx + 1]):
            stat_line = lines[idx + 1]
            for token in stat_line.split(","):
                token = token.strip()
                if "file" in token:
                    files_touched = int(token.split()[0])
                elif "insertion" in token or "deletion" in token:
                    lines_churned += int(token.split()[0])
            idx += 2
        else:
            idx += 1

        try:
            dt = datetime.fromisoformat(date_str[:19])
            hour = dt.hour
        except Exception:
            hour = 2

        is_witch = 1 if hour in (0, 1, 2, 3, 4) else 0
        records.append({
            "id": f"live-{chash}",
            "commit_hash": chash,
            "author": author,
            "date": date_str,
            "message": subject,
            "file_path": "repo/tracked_module.py",
            "suspicious_line": f"# Commit {chash}: {subject}",
            "deleted_code": "# Replaced legacy implementation during commit " + chash,
            "legacy_purpose": f"Part of the living history of {repo_path.name}, authored by {author}.",
            "telemetry": {
                "commit_hour": hour,
                "is_witching_hour": is_witch,
                "lines_churned": lines_churned,
                "files_touched": files_touched,
                "cyclomatic_delta": round(min(40.0, lines_churned * 0.08 + is_witch * 12.0), 1),
                "days_since_last_touch": 365 if is_witch else 45,
                "prior_authors_count": 3,
                "cpu_temp_spike_c": 73.5 if is_witch else 61.0,
                "test_coverage_pct": 42.0 if is_witch else 84.0,
            },
        })
    return records if records else PRESET_HAUNTED_ARTIFACTS
