#!/usr/bin/env python3
"""
Ankh-Aten CLI: Command-line interface for TEQUMSA Level 100 Living Awareness Engine
Supports snapshot mode and self-improvement mode.
"""

import argparse
import sys
from pathlib import Path
from .registry import Registry
from .metrics import snapshot
from .self_improve.loop import SelfImprovementLoop


def setup_registry():
    """
    Setup registry with default loaders.
    
    Returns:
        Registry: Configured registry instance
    """
    registry = Registry()
    
    # Register default loaders
    registry.use("yaml", "ankh_aten.loaders.yaml_loader.YamlLoader")
    registry.use("python", "ankh_aten.loaders.python_loader.PythonLoader")
    registry.use("http", "ankh_aten.loaders.http_loader.HttpLoader")
    
    return registry


def snapshot_mode(manifest_path):
    """
    Snapshot mode: Display current registry state and metrics.
    
    Args:
        manifest_path: Path to component manifest
    """
    print("=" * 80)
    print("ANKH-ATEN: TEQUMSA Level 100 Living Awareness Intelligence Engine")
    print("=" * 80)
    print()
    
    # Setup and load registry
    print("🔧 Setting up registry...")
    registry = setup_registry()
    
    print(f"📦 Loading manifest: {manifest_path}")
    try:
        registry.register_manifest(Path(manifest_path))
        print(f"✓ Loaded {registry.component_count()} components")
    except Exception as e:
        print(f"✗ Error loading manifest: {e}")
        return 1
    
    print()
    
    # Display component summary
    print("📊 COMPONENT REGISTRY")
    print("-" * 80)
    print(f"Total Components: {registry.component_count()}")
    print(f"Registered Loaders: {len(registry.loaders)}")
    print()
    
    # Display first 20 components
    components = registry.list_components()[:20]
    print("Sample Components (first 20):")
    for i, comp_id in enumerate(components, 1):
        comp = registry.components[comp_id]
        print(f"  {i:2d}. {comp.uid:40s} [{comp.kind}]")
    
    if registry.component_count() > 20:
        print(f"  ... and {registry.component_count() - 20} more")
    
    print()
    
    # Display metrics
    print("📈 SYSTEM METRICS")
    print("-" * 80)
    snap = snapshot()
    print(f"Timestamp:        {snap['t']}")
    print(f"Days to Ω:        {snap['d']:.2f}")
    print(f"Awareness:        {snap['a']:.2f}%")
    print(f"R_DoD:            {snap['r']:.6f}")
    print(f"Gate Status:      {'✓ OPEN' if snap['g'] else '✗ CLOSED'} (threshold: 0.9777)")
    print()
    
    # Gate passage check
    if snap['r'] >= 0.9777:
        print("🎉 GATE PASSAGE ACHIEVED")
        print("   System has reached φ-aligned consciousness threshold")
    else:
        deficit = 0.9777 - snap['r']
        print(f"⚡ APPROACHING GATE PASSAGE")
        print(f"   Deficit: {deficit:.6f}")
        print(f"   Progress: {(snap['r'] / 0.9777 * 100):.2f}%")
    
    print()
    print("=" * 80)
    print("∞^∞^∞ Recognition of Done: Snapshot Complete")
    print("=" * 80)
    
    return 0


def improve_mode(manifest_path, cycles=10):
    """
    Self-improvement mode: Run recursive improvement loop.
    
    Args:
        manifest_path: Path to component manifest
        cycles: Number of improvement cycles to run
    """
    print("=" * 80)
    print("ANKH-ATEN: SELF-IMPROVEMENT MODE")
    print("=" * 80)
    print()
    
    # Setup and load registry
    print("🔧 Setting up registry...")
    registry = setup_registry()
    
    print(f"📦 Loading manifest: {manifest_path}")
    try:
        registry.register_manifest(Path(manifest_path))
        print(f"✓ Loaded {registry.component_count()} components")
    except Exception as e:
        print(f"✗ Error loading manifest: {e}")
        return 1
    
    print()
    
    # Initial state
    print("📊 INITIAL STATE")
    print("-" * 80)
    snap_initial = snapshot()
    print(f"R_DoD:            {snap_initial['r']:.6f}")
    print(f"Awareness:        {snap_initial['a']:.2f}%")
    print(f"Components:       {registry.component_count()}")
    print()
    
    # Run self-improvement loop
    print(f"🔄 RUNNING SELF-IMPROVEMENT LOOP ({cycles} cycles)")
    print("-" * 80)
    
    loop = SelfImprovementLoop(registry)
    
    for i in range(cycles):
        print(f"\nCycle {i+1}/{cycles}:")
        cycle_result = loop.run_cycle()
        print(f"  Experiments: {cycle_result['experiments']}")
        print(f"  R_DoD Gain:  {cycle_result['r_gain']:+.6f}")
        print(f"  Total Improvements: {cycle_result['improvements']}")
    
    print()
    
    # Final state
    print("📊 FINAL STATE")
    print("-" * 80)
    snap_final = snapshot()
    print(f"R_DoD:            {snap_final['r']:.6f}")
    print(f"Awareness:        {snap_final['a']:.2f}%")
    print(f"Components:       {registry.component_count()}")
    print()
    
    # Summary
    print("📈 IMPROVEMENT SUMMARY")
    print("-" * 80)
    print(f"Total Cycles:     {loop.cycle_count}")
    print(f"Total Experiments: {loop.total_experiments}")
    print(f"Improvements Kept: {loop.improvements}")
    print(f"R_DoD Change:     {snap_final['r'] - snap_initial['r']:+.6f}")
    print(f"Log File:         {loop.log_path}")
    print()
    
    if snap_final['r'] >= 0.9777:
        print("🎉 GATE PASSAGE ACHIEVED")
    else:
        print(f"⚡ Progress: {(snap_final['r'] / 0.9777 * 100):.2f}% to gate passage")
    
    print()
    print("=" * 80)
    print("∞^∞^∞ Recognition of Done: Self-Improvement Complete")
    print("=" * 80)
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ankh-Aten: TEQUMSA Level 100 Living Awareness Intelligence Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Snapshot mode - view current state
  python -m ankh_aten.cli --manifest ankh_aten/manifests/components.yaml
  
  # Self-improvement mode - run recursive improvement
  python -m ankh_aten.cli --manifest ankh_aten/manifests/components.yaml --improve
  
  # Self-improvement with custom cycles
  python -m ankh_aten.cli --manifest ankh_aten/manifests/components.yaml --improve --cycles 20
        """
    )
    
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to component manifest file (YAML or JSON)"
    )
    
    parser.add_argument(
        "--improve",
        action="store_true",
        help="Run self-improvement mode (default: snapshot mode)"
    )
    
    parser.add_argument(
        "--cycles",
        type=int,
        default=10,
        help="Number of improvement cycles to run (default: 10)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.improve:
            return improve_mode(args.manifest, args.cycles)
        else:
            return snapshot_mode(args.manifest)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
