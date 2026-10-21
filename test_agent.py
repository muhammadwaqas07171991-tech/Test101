"""Six tests = six questions with known answers. All six must pass.
The tests keep their OWN copy of the limits, so your experiment in config.py cannot break them."""
import math
from collector import clean
from rules import violations, hab_tier, mann_kendall, sens_slope
import pandas as pd

GRADE_II = {"pH": (6.5, 8.5), "DO": (5.0, None), "BOD": (None, 3.0),
            "COD": (None, 5.0), "TN": (None, 3.0), "TP": (None, 0.10)}
LAB = {"pH": 8.9, "DO": 4.2, "BOD": 4.8, "COD": 7.9, "TN": 4.3, "TP": 0.165}
YEARS = [2020, 2021, 2022, 2023, 2024]
TP = [0.088, 0.095, 0.101, 0.116, 0.114]


def test_lab_sample_breaks_all_six_limits():
    assert sorted(violations(LAB, GRADE_II)) == sorted(LAB)


def test_good_water_and_missing_values_are_not_violations():
    good = {"pH": 7.2, "DO": 8.0, "BOD": 1.0, "COD": 2.0, "TN": 1.0, "TP": 0.02}
    assert violations(good, GRADE_II) == []
    assert violations({"pH": float("nan"), "TP": None}, GRADE_II) == []


def test_bloom_tiers():
    assert hab_tier(999) == "Normal"
    assert hab_tier(1_000) == "Caution"
    assert hab_tier(38_500) == "Warning"
    assert hab_tier(1_250_000) == "Outbreak"


def test_clean_turns_bad_text_into_nan_and_drops_empty_rows():
    df = pd.DataFrame({"name": ["a", "b"], "x": ["12", "N/A"]})
    out = clean(df, ["x"])
    assert len(out) == 1 and out["x"].iloc[0] == 12


def test_mann_kendall_matches_the_lecture():
    s, var, z, p = mann_kendall(TP)
    assert s == 8
    assert math.isclose(z, 1.71, abs_tol=0.01)
    assert math.isclose(p, 0.086, abs_tol=0.001)


def test_sens_slope_matches_the_lecture():
    assert math.isclose(sens_slope(YEARS, TP), 0.0065, abs_tol=1e-9)
