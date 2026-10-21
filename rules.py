"""Layer 3: REASONING. Check limits, classify blooms, test a trend."""
import math
from itertools import combinations
from config import LIMITS, HAB_TIERS


def violations(sample, limits=LIMITS):
    """Return the names of the parameters that are outside their (low, high) range."""
    bad = []
    for name, value in sample.items():
        if name not in limits or value is None or value != value:  # value != value means NaN
            continue
        low, high = limits[name]
        if (low is not None and value < low) or (high is not None and value > high):
            bad.append(name)
    return bad


def hab_tier(cells_ml):
    """Walk down the tiers (highest first) and return the first one the count reaches."""
    for lower, name in HAB_TIERS:
        if cells_ml >= lower:
            return name
    return "Normal"


def mann_kendall(x):
    """Mann-Kendall trend test. Returns S, Var(S), Z and the two-tailed p-value."""
    n = len(x)
    s = sum((x[j] > x[k]) - (x[j] < x[k]) for k, j in combinations(range(n), 2))
    var = n * (n - 1) * (2 * n + 5) / 18.0
    z = 0.0 if s == 0 else (s - 1) / math.sqrt(var) if s > 0 else (s + 1) / math.sqrt(var)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return s, var, z, p


def sens_slope(t, x):
    """Sen's slope: the median of all pairwise slopes (x_j - x_k) / (t_j - t_k)."""
    slopes = sorted((x[j] - x[k]) / (t[j] - t[k]) for k, j in combinations(range(len(x)), 2))
    m = len(slopes)
    return slopes[m // 2] if m % 2 else (slopes[m // 2 - 1] + slopes[m // 2]) / 2.0
