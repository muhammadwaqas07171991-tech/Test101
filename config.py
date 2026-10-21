"""Layer 1: THE RULEBOOK. Limits, bloom tiers and folders. Change numbers here."""
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("docs")

# Korean Ministry of Environment, Living Environment Grade II.
# Each entry is (lowest allowed, highest allowed). None = no limit on that side.
LIMITS = {
    "pH":  (6.5, 8.5),
    "DO":  (5.0, None),   # dissolved oxygen must be AT LEAST 5.0 mg/L
    "BOD": (None, 3.0),   # at most 3.0 mg/L
    "COD": (None, 5.0),   # at most 5.0 mg/L
    "TN":  (None, 3.0),   # at most 3.0 mg/L
    "TP":  (None, 0.10),  # <-- EXPERIMENT: change 0.10 to 0.20, save, run with --again
}

# Cyanobacteria (algal bloom) alert tiers in cells/mL. Highest tier first!
HAB_TIERS = [
    (1_000_000, "Outbreak"),
    (10_000,    "Warning"),
    (1_000,     "Caution"),
    (0,         "Normal"),
]

HAB_ACTIONS = {
    "Outbreak": "Emergency: switch intake, notify public-health authority",
    "Warning":  "Lower intake depth, add PAC or ozone, daily sampling",
    "Caution":  "Sample twice a week, test geosmin and 2-MIB",
    "Normal":   "Routine weekly surveillance",
}
