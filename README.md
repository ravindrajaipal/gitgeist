# 👻 GitGeist: The Ghost in Your Git History & Digital Code Ofrenda

> **Built for the [Hacktoberfest 2026 Open-Source AI Challenge — Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)** (`#devchallenge` `#hf26challenge`)

**GitGeist** is an offline-first haunted terminal, Git blame séance engine, and Día de los Muertos *Code Ofrenda* built on two open-weight AI models running locally on your machine:

1. **Prior Labs' TabPFN (`tabpfn-v2`)**: Predicts the **Haunting Risk Score** (incident/regression probability + calibrated 10–90% range) of any commit or sensor log from tabular telemetry (`data/haunted_commits_telemetry.csv`) in a single CPU pass—with a zero-dependency calibrated NumPy fallback so it works instantly on any laptop.
2. **Google's Gemma 3 (`gemma3:1b` / `gemma3:4b` via Ollama)**: Channels the spirit of suspicious 3:00 AM commits to whisper why a cursed line of code exists (citing the exact commit hash and TabPFN risk without hallucinating numbers), and writes a candlelit **Día de los Muertos Code Ofrenda** honoring retired functions and the developers who built them.

---

## 🚀 Quick Start (100% Offline on Your Laptop)

```bash
# 1. Install core dependencies
pip install fastapi uvicorn pandas numpy requests
# (Optional) Install open-weight TabPFN and pull local Gemma 3 via Ollama:
# pip install tabpfn
# ollama pull gemma3:1b

# 2. Launch the Haunted Web UI & API on http://localhost:8080
python3 run.py

# 3. Or summon the Haunted Terminal CLI directly in your shell
python3 cli.py --preset 0

# 4. Reproduce the empirical feature-sensitivity sweep table
python3 scripts/analyze.py

# 5. Run unit tests
python3 -m unittest discover tests
```

---

## 🏆 Hacktoberfest Prize Categories Supported

- **Overall Winner ($250)**: Combines both halves of Week 4's *Ghost in the Machine* theme—a spooky Git commit séance that accuses you of your own 3:00 AM hotfixes *and* a heartfelt Día de los Muertos digital *Ofrenda* honoring retired code.
- **Best Use of Gemma ($200)**: Uses Google's open-weight **Gemma 3** locally via Ollama (with Google AI Studio API & deterministic offline fallback) as the voice of the Haunted Séance and the Keeper of the Code Ofrenda.
- **Best Use of TabPFN ($200)**: Uses **TabPFN** on historical commit & thermal telemetry data (`data/haunted_commits_telemetry.csv`) to output calibrated incident probabilities and feature-sensitivity sweeps.
- **Best Use of Render ($200)** / **Best Use of DigitalOcean ($200)**: Includes `render.yaml` and `Dockerfile` for one-click cloud deployment.
