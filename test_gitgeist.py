import unittest
from gitgeist.forecaster import HauntingForecaster
from gitgeist.scanner import PRESET_HAUNTED_ARTIFACTS
from gitgeist.seance_llm import generate_seance_whisper, generate_ofrenda_tribute


class TestGitGeist(unittest.TestCase):
    def setUp(self):
        self.forecaster = HauntingForecaster()

    def test_witching_hour_increases_haunting_risk(self):
        daytime = dict(PRESET_HAUNTED_ARTIFACTS[2]["telemetry"])
        midnight = dict(PRESET_HAUNTED_ARTIFACTS[0]["telemetry"])
        r_day = self.forecaster.predict_risk(daytime)
        r_night = self.forecaster.predict_risk(midnight)
        self.assertGreater(r_night["haunting_risk_pct"], r_day["haunting_risk_pct"])
        self.assertEqual(len(r_night["range_10_90_pct"]), 2)

    def test_seance_whisper_cites_exact_commit_and_risk(self):
        item = PRESET_HAUNTED_ARTIFACTS[0]
        forecast = self.forecaster.predict_risk(item["telemetry"])
        seance = generate_seance_whisper(item, forecast)
        self.assertIn(item["commit_hash"], seance["whisper"])
        self.assertIn(str(forecast["haunting_risk_pct"]), seance["whisper"])

    def test_ofrenda_tribute_honors_author(self):
        item = PRESET_HAUNTED_ARTIFACTS[1]
        forecast = self.forecaster.predict_risk(item["telemetry"])
        ofrenda = generate_ofrenda_tribute(item, forecast)
        self.assertIn(item["commit_hash"], ofrenda["tribute"])


if __name__ == "__main__":
    unittest.main()
