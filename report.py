"""Layer 4: ACTION. Make a chart (for people), a JSON file (for programs), a web page (for everyone)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")                       # draw pictures without opening a window
import matplotlib.pyplot as plt
from config import LIMITS, HAB_ACTIONS

COLORS = {"Outbreak": "#B91C1C", "Warning": "#EA580C", "Caution": "#CA8A04", "Normal": "#15803D"}


def publish(years, tp, slope, summary, out="docs"):
    out = Path(out)
    out.mkdir(exist_ok=True)
    limit = LIMITS["TP"][1]                 # the chart follows config.py

    # 1. The chart
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(years, tp, color="#1E3A8A", s=60, zorder=5, label="Annual mean TP")
    line = [tp[0] + slope * (y - years[0]) for y in years]
    ax.plot(years, line, color="#EF4444", linewidth=2, label=f"Sen's slope ({slope:+.4f} mg/L per year)")
    ax.axhline(limit, color="#991B1B", linestyle=":", linewidth=1.5, label=f"Limit in config.py ({limit} mg/L)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total phosphorus (mg/L)")
    ax.set_title("Total phosphorus trend (Namgang, 5 years)")
    ax.set_xticks(years)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out / "tp_trend.png", dpi=150)
    plt.close(fig)

    # 2. The JSON file (a robot can read this)
    (out / "status.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # 3. The web page
    bad = summary["limits_broken"]
    pills = "".join(
        f"<li><span class='pill' style='background:{COLORS[t]}'>{t}</span> <b>{name}</b>: {HAB_ACTIONS[t]}</li>"
        for name, t in summary["bloom_tiers"].items()
    )
    tr = summary["tp_trend"]
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>K-WaterGuard Agent Status</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;max-width:820px;margin:30px auto;padding:0 20px;color:#0F172A;background:#F8FAFC;line-height:1.5}}
h1{{color:#1E3A8A;margin-bottom:0}} .sub{{color:#64748B;margin-top:4px}}
.card{{background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:14px 20px;margin:16px 0}}
.card h2{{margin:0 0 6px;font-size:1.05em;color:#1E3A8A}} ul{{padding-left:20px;margin:6px 0}}
.pill{{color:#fff;border-radius:12px;padding:1px 10px;font-size:.85em}} img{{max-width:100%;border-radius:10px;border:1px solid #CBD5E1}}
</style></head><body>
<h1>K-WaterGuard Agent Status</h1>
<p class="sub">Run date: {summary["run_date"]} &middot; Sample: {summary["sample"]}</p>
<div class="card"><h2>1. Limits broken: {len(bad)} of {summary["parameters_checked"]}</h2>
<p>{", ".join(bad) if bad else "None. All parameters are inside their limits."}</p></div>
<div class="card"><h2>2. Algal bloom tier at each intake</h2><ul>{pills}</ul></div>
<div class="card"><h2>3. Total phosphorus trend (Mann-Kendall)</h2>
<p>S = {tr["S"]}, Z = {tr["Z"]}, p = {tr["p_two_tailed"]}, Sen's slope = {tr["slope_mg_per_L_per_year"]:+.4f} mg/L per year<br>
<b>{tr["verdict"]}</b></p></div>
<img src="tp_trend.png" alt="Total phosphorus trend chart">
</body></html>"""
    (out / "index.html").write_text(page, encoding="utf-8")
