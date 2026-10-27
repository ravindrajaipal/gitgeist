#!/usr/bin/env python3
"""
GitGeist Haunted Terminal CLI.
Run `python cli.py` to summon the Ghost in the Machine directly inside your terminal!
"""
import argparse
from pathlib import Path
from gitgeist.forecaster import HauntingForecaster
from gitgeist.scanner import PRESET_HAUNTED_ARTIFACTS, scan_local_git_repo
from gitgeist.seance_llm import generate_seance_whisper, generate_ofrenda_tribute


def main():
    parser = argparse.ArgumentParser(description="👻 GitGeist: Haunted Git Séance & Code Ofrenda CLI")
    parser.add_argument("--repo", type=str, default=None, help="Path to a local Git repo to scan")
    parser.add_argument("--preset", type=int, default=0, help="Preset index (0, 1, or 2)")
    args = parser.parse_args()

    forecaster = HauntingForecaster()
    if args.repo:
        artifacts = scan_local_git_repo(Path(args.repo))
    else:
        artifacts = PRESET_HAUNTED_ARTIFACTS

    idx = max(0, min(args.preset, len(artifacts) - 1))
    item = artifacts[idx]
    forecast = forecaster.predict_risk(item["telemetry"])
    seance = generate_seance_whisper(item, forecast)
    ofrenda = generate_ofrenda_tribute(item, forecast)

    print("=" * 76)
    print("👻 GITGEIST — THE GHOST IN THE MACHINE (HACKTOBERFEST 2026 WEEK 4)")
    print("=" * 76)
    print(f"Commit       : {item['commit_hash']} | Author: {item['author']}")
    print(f"Date         : {item['date']}")
    print(f"File         : {item['file_path']}")
    print(f"Cursed Line  : {item['suspicious_line']}")
    print("-" * 76)
    print(f"🔮 TabPFN Haunting Risk : {forecast['haunting_risk_pct']}% "
          f"(10–90% Range: {forecast['range_10_90_pct'][0]}% – {forecast['range_10_90_pct'][1]}%)")
    print(f"⚠️  Severity Classification: {forecast['severity']}")
    print(f"🧭 Risk Drivers          : {', '.join(forecast['top_drivers'])}")
    print("-" * 76)
    print(f"🕯️  HAUNTED SÉANCE WHISPER ({seance['source']}):")
    print(f"   {seance['whisper']}")
    print("-" * 76)
    print(f"🌼 DÍA DE LOS MUERTOS CODE OFRENDA ({ofrenda['source']}):")
    print(f"   {ofrenda['tribute']}")
    print("=" * 76)


if __name__ == "__main__":
    main()
