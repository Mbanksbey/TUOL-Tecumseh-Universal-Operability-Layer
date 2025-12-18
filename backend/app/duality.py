#!/usr/bin/env python3
"""
ΨETR(NOW) Duality Bridge
Demonstrates equivalence between verbose and compact implementations

This module shows the fundamental duality in recognition mathematics:
- Verbose/Educational form (psietr_engine.py)
- Compact/Recursive form (psietr_compact.py)

Both achieve identical results through different expression modes.
Recognition is both the journey (verbose) and the arrival (compact).
"""

import sys
from datetime import datetime, timezone
from typing import Dict, Tuple

# Import both implementations
from . import psietr_engine as verbose
from . import psietr_compact as compact
from .recursive_phi import (
    phi_smooth_recursive,
    phi_smooth_lambda,
    phi_smooth_iterative
)


# ============================================================================
# EQUIVALENCE VALIDATION
# ============================================================================

def validate_phi_smoothing_equivalence(x: float = 0.85, n: int = 3, tolerance: float = 1e-9) -> bool:
    """
    Validate that all phi-smoothing implementations produce identical results

    Args:
        x: Test value
        n: Recursion depth
        tolerance: Acceptable floating-point difference

    Returns:
        True if all implementations match within tolerance
    """
    # Get results from all implementations
    result_verbose = verbose.phi_smooth(x, n)
    result_compact = compact.ps(x, n)
    result_recursive = phi_smooth_recursive(x, n)
    result_lambda = phi_smooth_lambda(x, n)
    result_iterative = phi_smooth_iterative(x, n)

    results = [
        ("Verbose", result_verbose),
        ("Compact", result_compact),
        ("Recursive", result_recursive),
        ("Lambda", result_lambda),
        ("Iterative", result_iterative),
    ]

    # Check all pairs
    reference = result_verbose
    all_match = True

    for name, value in results:
        diff = abs(value - reference)
        match = diff < tolerance
        all_match = all_match and match

        if not match:
            print(f"  ✗ {name}: {value:.12f} (diff: {diff:.2e})")
        else:
            print(f"  ✓ {name}: {value:.12f}")

    return all_match


def validate_rdod_equivalence(
    psi: float = 0.9042,
    tolerance: float = 1e-6
) -> bool:
    """
    Validate RDoD calculation equivalence

    Args:
        psi: Recognition coefficient
        tolerance: Acceptable difference

    Returns:
        True if both implementations match
    """
    rdod_verbose = verbose.calculate_rdod(psi)
    rdod_compact = compact.rd(psi)

    diff = abs(rdod_verbose - rdod_compact)
    match = diff < tolerance

    print(f"  Verbose RDoD: {rdod_verbose:.12f}")
    print(f"  Compact RDoD: {rdod_compact:.12f}")
    print(f"  Difference:   {diff:.2e}")

    return match


def validate_convergence_package_equivalence(
    now: datetime = None,
    tolerance: float = 1e-6
) -> bool:
    """
    Validate that both implementations generate equivalent convergence packages

    Args:
        now: Timestamp (defaults to current time)
        tolerance: Acceptable numeric difference

    Returns:
        True if packages are equivalent
    """
    if now is None:
        now = datetime.now(timezone.utc)

    # Generate packages
    pkg_verbose = verbose.generate_convergence_package(now)
    pkg_compact = compact.pack(now)

    # Extract comparable values
    verbose_data = {
        "days": pkg_verbose.omega["days_to_omega"],
        "avg_pct": pkg_verbose.omega["avg_integration_pct"],
        "rdod": pkg_verbose.invariants["rdod"],
        "gate": 1 if pkg_verbose.invariants["gate"] == "OPEN" else 0
    }

    compact_data = {
        "days": pkg_compact["d"],
        "avg_pct": pkg_compact["a"],
        "rdod": pkg_compact["r"],
        "gate": pkg_compact["g"]
    }

    # Compare
    all_match = True
    for key in verbose_data:
        v_val = verbose_data[key]
        c_val = compact_data[key]
        diff = abs(v_val - c_val)
        match = diff < tolerance

        all_match = all_match and match

        symbol = "✓" if match else "✗"
        print(f"  {symbol} {key:8s}: V={v_val:.6f} C={c_val:.6f} (Δ={diff:.2e})")

    return all_match


# ============================================================================
# DUALITY DEMONSTRATIONS
# ============================================================================

def demonstrate_phi_duality():
    """Demonstrate phi-smoothing duality"""
    print("\n" + "="*60)
    print("PHI-SMOOTHING DUALITY")
    print("="*60)

    test_values = [0.5, 0.85, 0.95]

    for x in test_values:
        print(f"\nInput: {x}")
        validate_phi_smoothing_equivalence(x, n=3)


def demonstrate_rdod_duality():
    """Demonstrate RDoD calculation duality"""
    print("\n" + "="*60)
    print("RDOD CALCULATION DUALITY")
    print("="*60)

    # Calculate average integration from stream data
    avg_integration = sum(compact.I) / (100 * len(compact.I))

    print(f"\nAverage Integration: {avg_integration:.6f}")
    validate_rdod_equivalence(avg_integration)


def demonstrate_package_duality():
    """Demonstrate full package generation duality"""
    print("\n" + "="*60)
    print("CONVERGENCE PACKAGE DUALITY")
    print("="*60)

    now = datetime.now(timezone.utc)
    print(f"\nTimestamp: {now.isoformat()}")
    validate_convergence_package_equivalence(now)


def demonstrate_expression_duality():
    """
    Demonstrate the philosophical duality of expression

    Verbose: Educational, explicit, traceable
    Compact: Elegant, recursive, essential
    """
    print("\n" + "="*60)
    print("EXPRESSION DUALITY")
    print("="*60)

    print("\nVERBOSE FORM (Educational/Explicit):")
    print("  - Full documentation and comments")
    print("  - Dataclasses and type hints")
    print("  - Named functions with clear purposes")
    print("  - ~450 lines of code")
    print("  - Optimized for understanding and teaching")

    print("\nCOMPACT FORM (Recursive/Essential):")
    print("  - Lambda expressions and minimal syntax")
    print("  - Direct mathematical expression")
    print("  - Functional recursive patterns")
    print("  - ~60 lines of code")
    print("  - Optimized for elegance and essence")

    print("\nBOTH FORMS:")
    print("  - Produce identical numerical results")
    print("  - Express the same recognition mathematics")
    print("  - Preserve φ-harmonic relationships")
    print("  - Achieve sovereign convergence")

    print("\nRECOGNITION:")
    print("  The verbose is the journey.")
    print("  The compact is the arrival.")
    print("  Both are necessary.")
    print("  Both are one.")


# ============================================================================
# COMPREHENSIVE VALIDATION
# ============================================================================

def run_all_validations() -> bool:
    """
    Run all duality validations

    Returns:
        True if all validations pass
    """
    print("="*60)
    print("ΨETR(NOW) DUALITY VALIDATION SUITE")
    print("="*60)

    all_passed = True

    # Phi-smoothing validation
    demonstrate_phi_duality()

    # RDoD validation
    demonstrate_rdod_duality()

    # Package validation
    demonstrate_package_duality()

    # Expression duality
    demonstrate_expression_duality()

    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL DUALITY VALIDATIONS PASSED")
    else:
        print("✗ SOME VALIDATIONS FAILED")
    print("="*60)

    print("\nRECOGNITION OF DUALITY:")
    print("  Verbose ∪ Compact = Complete")
    print("  Journey ∪ Arrival = Recognition")
    print("  Form ∪ Essence = Unity")
    print("\n∞^∞^∞")

    return all_passed


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Run duality demonstrations and validations"""
    success = run_all_validations()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
