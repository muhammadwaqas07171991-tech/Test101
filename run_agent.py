"""The conductor. Perceive -> Reason -> Act. You run it now; GitHub runs it every morning."""
from datetime import date
from config import DATA_DIR, OUT_DIR
from collector import load_csv
from rules import violations, hab_tier, mann_kendall, sens_slope
from report import publish

PARAMS = ["pH", "DO", "BOD", "COD", "TN", "TP"]


def main():
    # 1. PERCEIVE: read the three data files and clean them
    sample = load_csv(DATA_DIR / "sample.csv", PARAMS).iloc[0]
    intakes = load_csv(DATA_DIR / "intakes.csv", ["cells_per_ml"])
    annual = load_csv(DATA_DIR / "tp_annual.csv", ["TP"])

    # 2. REASON: apply the rules from rules.py and config.py
    bad = violations({p: float(sample[p]) for p in PARAMS})
    tiers = {row.intake: hab_tier(row.cells_per_ml) for row in intakes.itertuples()}
    years = [int(y) for y in annual["year"]]
    tp = [float(v) for v in annual["TP"]]
    s, var, z, p = mann_kendall(tp)
    slope = sens_slope(years, tp)

    # 3. ACT: publish the results
    summary = {
        "run_date": date.today().isoformat(),
        "sample": "12 Aug 2026 (classroom lab sample)",
        "parameters_checked": len(PARAMS),
        "limits_broken": bad,
        "bloom_tiers": tiers,
        "tp_trend": {
            "S": int(s),
            "Z": round(z, 2),
            "p_two_tailed": round(p, 3),
            "slope_mg_per_L_per_year": round(slope, 4),
            "n_years": len(tp),
            "verdict": "Not significant at 0.05 (only 5 years of data)" if p >= 0.05 else "Significant at 0.05",
        },
    }
    publish(years, tp, slope, summary, out=OUT_DIR)

    print(f"Limits broken ({len(bad)} of {len(PARAMS)}): {', '.join(bad) if bad else 'none'}")
    print("Bloom tiers: " + ", ".join(f"{k}={v}" for k, v in tiers.items()))
    print(f"TP trend: S={s}, Z={z:.2f}, p={p:.3f}, slope={slope:+.4f} mg/L per year")
    print(f"Wrote {OUT_DIR}/index.html, status.json, tp_trend.png")


if __name__ == "__main__":
    main()
