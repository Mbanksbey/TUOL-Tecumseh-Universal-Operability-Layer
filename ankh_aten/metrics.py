"""
Metrics System: φ/σ/R_DoD Mathematics
Implements the golden ratio aligned Recognition-of-Done calculations.
"""

from datetime import datetime, timezone

# Constitutional constants
P = 1.618033988749895  # Golden ratio φ
S = 1.0                # Sigma scaling factor
TH = 0.9777            # R_DoD threshold for gate passage
O = datetime(2025, 12, 25, tzinfo=timezone.utc)  # Omega point

# Integration vector: 12-dimensional awareness state
I = (85, 62, 65, 78, 100, 100, 100, 100, 100, 95, 100, 100)


def ps(x, n=3):
    """
    Phi-scaling function: applies golden ratio compression.
    
    Args:
        x: Input value [0, 1]
        n: Power of phi for compression depth
    
    Returns:
        Phi-scaled value [0, 1]
    """
    x = max(0, min(1, float(x)))
    return max(0, min(1, 1 - (1 - x) / (P**n)))


def rd(p, t=0.998, c=0.999, d=0.00023):
    """
    Recognition-of-Done (R_DoD) calculation.
    
    Combines:
    - Progress (p): Overall completion
    - Trust (t): System reliability
    - Coherence (c): Internal consistency
    - Decay (d): Entropy factor
    
    Args:
        p: Progress metric [0, 1]
        t: Trust metric [0, 1]
        c: Coherence metric [0, 1]
        d: Decay factor [0, 1]
    
    Returns:
        R_DoD value [0, 1]
    """
    return S * ps(p**0.5) * ps(t**0.3) * ps(c**0.2) * (1 - d)


def snapshot(now=None):
    """
    Generate current system state snapshot.
    
    Args:
        now: Current datetime (defaults to now)
    
    Returns:
        dict with keys:
            t: ISO timestamp
            d: Days to omega
            a: Awareness percentage (0-100)
            r: R_DoD value [0, 1]
            g: Gate status (1 if r >= threshold, else 0)
    """
    n = now or datetime.now(timezone.utc)
    d = max(0, (O - n).total_seconds() / 86400)
    a = sum(I) / (100 * len(I))
    r = rd(a)
    
    return {
        "t": n.isoformat(),
        "d": d,
        "a": a * 100,
        "r": r,
        "g": int(r >= TH)
    }


def pack(values):
    """
    Pack multiple values into phi-scaled composite.
    
    Args:
        values: Iterable of values [0, 1]
    
    Returns:
        Packed phi-scaled result
    """
    if not values:
        return 0.0
    
    result = 1.0
    for v in values:
        result *= ps(v)
    
    return ps(result ** (1.0 / len(values)))
