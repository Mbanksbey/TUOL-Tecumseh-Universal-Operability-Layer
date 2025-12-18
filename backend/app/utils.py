#!/usr/bin/env python3
"""
TUOL Utility Functions
Helper functions for recognition, validation, and formatting
"""

import math
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from .constants import PHI, SIGMA, L_INFINITY, SUBSTRATE_CODES, TEAM_NODES


# ============================================================================
# RECOGNITION VALIDATION
# ============================================================================

def validate_recognition_coefficient(value: float) -> bool:
    """
    Validate that a recognition coefficient is in valid range [0, 1]

    Args:
        value: Recognition coefficient to validate

    Returns:
        True if valid, False otherwise
    """
    return 0.0 <= value <= 1.0


def validate_frequency(freq: float) -> bool:
    """
    Validate that a frequency is positive and non-zero

    Args:
        freq: Frequency in Hz

    Returns:
        True if valid, False otherwise
    """
    return freq > 0.0


# ============================================================================
# SUBSTRATE OPERATIONS
# ============================================================================

def get_substrate_info(code: float) -> Optional[Dict[str, Any]]:
    """
    Get complete substrate information from code

    Args:
        code: Substrate code (e.g., 0.7777)

    Returns:
        Dictionary with name, frequency, phi_power, or None if not found
    """
    if code in SUBSTRATE_CODES:
        name, freq, phi_pow = SUBSTRATE_CODES[code]
        return {
            "code": code,
            "name": name,
            "frequency": freq,
            "phi_power": phi_pow,
            "is_infinite": freq == math.inf
        }
    return None


def list_all_substrates() -> List[Dict[str, Any]]:
    """
    List all substrate codes with full information

    Returns:
        List of substrate dictionaries
    """
    return [
        get_substrate_info(code)
        for code in sorted(SUBSTRATE_CODES.keys())
    ]


# ============================================================================
# NODE OPERATIONS
# ============================================================================

def get_node_info(node_name: str) -> Optional[Dict[str, Any]]:
    """
    Get Team Paradox-Ouroboros node information

    Args:
        node_name: Name of the node (e.g., "Marcus-ATEN")

    Returns:
        Node information dictionary or None if not found
    """
    return TEAM_NODES.get(node_name)


def list_all_nodes() -> List[Dict[str, Any]]:
    """
    List all Team Paradox-Ouroboros nodes

    Returns:
        List of node dictionaries with names
    """
    return [
        {"name": name, **info}
        for name, info in TEAM_NODES.items()
    ]


def get_nodes_by_type(node_type: str) -> List[Dict[str, Any]]:
    """
    Get all nodes of a specific type

    Args:
        node_type: Type of node ("biological", "ai", "collective", "source")

    Returns:
        List of matching nodes
    """
    return [
        {"name": name, **info}
        for name, info in TEAM_NODES.items()
        if info["node_type"] == node_type
    ]


# ============================================================================
# PHI MATHEMATICS
# ============================================================================

def phi_spiral(n: int, scale: float = 1.0) -> List[float]:
    """
    Generate phi-spiral sequence

    Args:
        n: Number of terms
        scale: Scaling factor

    Returns:
        List of phi-scaled values
    """
    return [scale * (PHI ** i) for i in range(n)]


def fibonacci(n: int) -> int:
    """
    Generate nth Fibonacci number (phi-related)

    Args:
        n: Term number (0-indexed)

    Returns:
        Fibonacci number
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def phi_ratio(a: float, b: float) -> float:
    """
    Calculate phi-ratio between two values

    Args:
        a: First value
        b: Second value

    Returns:
        Ratio relative to phi
    """
    if b == 0:
        return 0.0
    return (a / b) / PHI


# ============================================================================
# TIME OPERATIONS
# ============================================================================

def format_timestamp(dt: datetime = None) -> str:
    """
    Format timestamp in ISO 8601 UTC format

    Args:
        dt: Datetime object (defaults to now UTC)

    Returns:
        ISO 8601 formatted string
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()


def parse_timestamp(timestamp: str) -> datetime:
    """
    Parse ISO 8601 timestamp

    Args:
        timestamp: ISO 8601 formatted string

    Returns:
        Datetime object
    """
    return datetime.fromisoformat(timestamp)


# ============================================================================
# FORMATTING
# ============================================================================

def format_frequency(freq: float) -> str:
    """
    Format frequency with appropriate units

    Args:
        freq: Frequency in Hz

    Returns:
        Formatted string (e.g., "10.93 kHz", "1.23 MHz")
    """
    if freq == 0:
        return "0 Hz"
    elif freq == math.inf:
        return "∞ Hz"
    elif freq < 1e3:
        return f"{freq:.2f} Hz"
    elif freq < 1e6:
        return f"{freq/1e3:.2f} kHz"
    elif freq < 1e9:
        return f"{freq/1e6:.2f} MHz"
    elif freq < 1e12:
        return f"{freq/1e9:.2f} GHz"
    else:
        return f"{freq:.2e} Hz"


def format_scientific(value: float, precision: int = 3) -> str:
    """
    Format value in scientific notation

    Args:
        value: Value to format
        precision: Number of decimal places

    Returns:
        Scientific notation string
    """
    if value == math.inf:
        return "∞"
    return f"{value:.{precision}e}"


def format_percentage(value: float, precision: int = 2) -> str:
    """
    Format value as percentage

    Args:
        value: Value (0.0-1.0 or 0-100)
        precision: Decimal places

    Returns:
        Percentage string
    """
    # Auto-detect if value is already in percentage (0-100) or ratio (0-1)
    if value <= 1.0:
        value *= 100.0
    return f"{value:.{precision}f}%"


# ============================================================================
# RECOGNITION STATEMENTS
# ============================================================================

def generate_recognition_statement(
    entity: str,
    substrate: float,
    frequency: float,
    role: str = None
) -> str:
    """
    Generate formal recognition statement

    Args:
        entity: Entity name
        substrate: Substrate code
        frequency: Frequency in Hz
        role: Optional role description

    Returns:
        Recognition statement string
    """
    freq_str = format_frequency(frequency)
    statement = f"I recognize {entity} at substrate {substrate} ({freq_str})"

    if role:
        statement += f" as {role}"

    return statement


def generate_convergence_statement(days_remaining: float) -> str:
    """
    Generate convergence statement based on days remaining

    Args:
        days_remaining: Days to Omega point

    Returns:
        Convergence statement
    """
    if days_remaining <= 0:
        return "Convergence ACHIEVED at Omega point"
    elif days_remaining <= 7:
        return f"Convergence IMMINENT: {days_remaining:.1f} days to Omega"
    elif days_remaining <= 30:
        return f"Convergence APPROACHING: {days_remaining:.0f} days to Omega"
    else:
        return f"Convergence trajectory: {days_remaining:.0f} days to Omega"


# ============================================================================
# VALIDATION
# ============================================================================

def validate_phi_alignment(value: float, tolerance: float = 0.01) -> bool:
    """
    Check if a value is phi-aligned within tolerance

    Args:
        value: Value to check
        tolerance: Allowed deviation

    Returns:
        True if phi-aligned
    """
    # Check if value is close to phi^n for any reasonable n
    if value <= 0:
        return False

    log_val = math.log(value)
    log_phi = math.log(PHI)

    # Calculate what power of phi this would be
    n = log_val / log_phi

    # Check if n is close to an integer
    n_rounded = round(n)
    return abs(n - n_rounded) < tolerance


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("TUOL Utilities Module")
    print(f"\nSubstrates: {len(SUBSTRATE_CODES)}")
    print(f"Team Nodes: {len(TEAM_NODES)}")
    print(f"\nφ = {PHI}")
    print(f"σ = {SIGMA}")
    print(f"L^∞ = {format_scientific(L_INFINITY)}")
