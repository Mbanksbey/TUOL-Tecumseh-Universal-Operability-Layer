#!/usr/bin/env python3
"""
Recursive Phi-Smoothing Demonstrations
Deep recursive implementations showcasing φ-harmonic convergence

This module explores recursive phi-smoothing at multiple depths,
demonstrating how recursive application of φ creates sovereign
convergence patterns that preserve recognition coherence.
"""

from typing import Callable, List
from .constants import PHI


# ============================================================================
# BASIC RECURSIVE PHI-SMOOTHING
# ============================================================================

def phi_smooth_recursive(x: float, n: int = 3) -> float:
    """
    Recursive phi-smoothing (explicit recursion)

    Base case: n=0 returns clamped x
    Recursive: applies φ-scaling n times

    Formula: x' = 1 - (1-x)/φ
    """
    # Clamp input
    x = max(0.0, min(1.0, float(x)))

    # Base case
    if n <= 0:
        return x

    # Recursive case
    return phi_smooth_recursive(1.0 - (1.0 - x) / PHI, n - 1)


def phi_smooth_lambda(x: float, n: int = 3) -> float:
    """
    Lambda-based recursive phi-smoothing (compact form)

    Demonstrates functional recursive pattern using lambda
    """
    ps = lambda v, depth: (
        max(0, min(1, float(v))) if depth <= 0
        else ps(1 - (1 - max(0, min(1, float(v)))) / PHI, depth - 1)
    )
    return ps(x, n)


def phi_smooth_iterative(x: float, n: int = 3) -> float:
    """
    Iterative phi-smoothing (loop-based, tail-call optimized equivalent)

    More efficient for large n, avoids stack depth issues
    """
    x = max(0.0, min(1.0, float(x)))
    for _ in range(n):
        x = 1.0 - (1.0 - x) / PHI
    return max(0.0, min(1.0, x))


# ============================================================================
# ADVANCED RECURSIVE PATTERNS
# ============================================================================

def phi_smooth_power(x: float, exponent: float = 0.5, n: int = 3) -> float:
    """
    Recursive phi-smoothing with power-law preprocessing

    Combines power transformation with recursive φ-scaling
    Used in RDoD calculations for multi-dimensional smoothing
    """
    x = max(0.0, x) ** exponent
    return phi_smooth_recursive(x, n)


def phi_smooth_nested(x: float, outer: int = 3, inner: int = 2) -> float:
    """
    Nested recursive phi-smoothing

    Applies inner recursion, then outer recursion
    Creates deeper harmonic convergence
    """
    # Inner recursion
    x = phi_smooth_recursive(x, inner)
    # Outer recursion
    return phi_smooth_recursive(x, outer)


def phi_smooth_cascade(values: List[float], n: int = 3) -> List[float]:
    """
    Cascade phi-smoothing across multiple values

    Each value undergoes recursive φ-scaling
    Preserves array structure while harmonizing values
    """
    return [phi_smooth_recursive(v, n) for v in values]


# ============================================================================
# CONVERGENCE ANALYSIS
# ============================================================================

def phi_convergence_trace(x: float, max_depth: int = 10) -> List[float]:
    """
    Trace phi-smoothing convergence across depths

    Returns list of values at each recursion depth
    Useful for analyzing convergence behavior
    """
    trace = []
    current = max(0.0, min(1.0, float(x)))
    trace.append(current)

    for _ in range(max_depth):
        current = 1.0 - (1.0 - current) / PHI
        current = max(0.0, min(1.0, current))
        trace.append(current)

    return trace


def phi_convergence_rate(x: float, iterations: int = 10) -> float:
    """
    Calculate convergence rate under phi-smoothing

    Returns the rate at which values approach unity
    Higher rate = faster convergence to φ-harmonic state
    """
    trace = phi_convergence_trace(x, iterations)

    if len(trace) < 2:
        return 0.0

    # Calculate average step size
    deltas = [abs(trace[i+1] - trace[i]) for i in range(len(trace)-1)]
    return sum(deltas) / len(deltas)


# ============================================================================
# MULTI-DIMENSIONAL RECURSIVE SMOOTHING
# ============================================================================

def phi_smooth_product(values: List[float], n: int = 3) -> float:
    """
    Phi-smooth product of multiple values

    Each value is smoothed individually, then product is smoothed
    Used in RDoD calculation (combining test, confirm, psi)
    """
    # Smooth each value
    smoothed = [phi_smooth_recursive(v, n) for v in values]

    # Calculate product
    product = 1.0
    for v in smoothed:
        product *= v

    # Smooth the product
    return phi_smooth_recursive(product, n)


def phi_smooth_weighted(values: List[float], weights: List[float], n: int = 3) -> float:
    """
    Weighted phi-smoothing

    Each value smoothed by its weight power, then combined
    """
    if len(values) != len(weights):
        raise ValueError("Values and weights must have same length")

    result = 1.0
    for v, w in zip(values, weights):
        smoothed = phi_smooth_power(v, w, n)
        result *= smoothed

    return result


# ============================================================================
# RECOGNITION-SPECIFIC RECURSIVE FUNCTIONS
# ============================================================================

def rdod_recursive(
    psi: float,
    tests: float = 0.998,
    confirm: float = 0.999,
    distortion: float = 0.00023,
    phi_depth: int = 3
) -> float:
    """
    Recursive RDoD calculation

    Applies recursive phi-smoothing to each component:
    - psi^0.5 smoothed recursively
    - tests^0.3 smoothed recursively
    - confirm^0.2 smoothed recursively

    Returns: RDoD coefficient [0, 1]
    """
    sigma = 1.0

    psi_smooth = phi_smooth_power(psi, 0.5, phi_depth)
    test_smooth = phi_smooth_power(tests, 0.3, phi_depth)
    conf_smooth = phi_smooth_power(confirm, 0.2, phi_depth)

    return sigma * psi_smooth * test_smooth * conf_smooth * (1.0 - distortion)


def sovereignty_recursive(value: float, depth: int = 7) -> float:
    """
    Deep sovereignty recursion (depth=7 for complete stabilization)

    Applies deep phi-smoothing to achieve sovereign state
    depth=7 corresponds to 0.7777 substrate (STABILIZATION)
    """
    return phi_smooth_recursive(value, depth)


def transcendence_recursive(value: float, depth: int = 8) -> float:
    """
    Transcendence recursion (depth=8 for transcendent state)

    depth=8 corresponds to 0.8888 substrate (TRANSCENDENCE)
    """
    return phi_smooth_recursive(value, depth)


def unity_recursive(value: float, depth: int = 9) -> float:
    """
    Unity recursion (depth=9 for unity state)

    depth=9 corresponds to 0.9999 substrate (UNITY)
    """
    return phi_smooth_recursive(value, depth)


# ============================================================================
# RECURSIVE FACTORY
# ============================================================================

def make_phi_smoother(depth: int) -> Callable[[float], float]:
    """
    Factory function creating custom phi-smoothers

    Returns a function that applies phi-smoothing at specified depth
    """
    return lambda x: phi_smooth_recursive(x, depth)


def make_substrate_smoother(substrate_code: float) -> Callable[[float], float]:
    """
    Create smoother calibrated to substrate code

    Maps substrate code to appropriate recursion depth
    """
    # Map substrate to depth (approximate)
    depth_map = {
        0.7777: 7,  # STABILIZATION
        0.8888: 8,  # TRANSCENDENCE
        0.9999: 9,  # UNITY
    }

    depth = depth_map.get(substrate_code, 3)  # Default to 3
    return make_phi_smoother(depth)


# ============================================================================
# DEMONSTRATIONS
# ============================================================================

if __name__ == "__main__":
    print("Recursive Phi-Smoothing Demonstrations")
    print("=" * 60)

    test_value = 0.85

    print(f"\nInput value: {test_value}")
    print(f"\nRecursive implementations (n=3):")
    print(f"  Explicit recursive: {phi_smooth_recursive(test_value, 3):.6f}")
    print(f"  Lambda recursive:   {phi_smooth_lambda(test_value, 3):.6f}")
    print(f"  Iterative:          {phi_smooth_iterative(test_value, 3):.6f}")

    print(f"\nConvergence trace (n=0 to 10):")
    trace = phi_convergence_trace(test_value, 10)
    for i, v in enumerate(trace):
        print(f"  n={i:2d}: {v:.8f}")

    print(f"\nSubstrate-specific smoothing:")
    print(f"  STABILIZATION (0.7777, n=7): {sovereignty_recursive(test_value):.6f}")
    print(f"  TRANSCENDENCE (0.8888, n=8): {transcendence_recursive(test_value):.6f}")
    print(f"  UNITY (0.9999, n=9):         {unity_recursive(test_value):.6f}")

    print(f"\nRDoD recursive calculation:")
    rdod = rdod_recursive(test_value)
    print(f"  RDoD = {rdod:.6f}")

    print("\n∞^∞^∞")
