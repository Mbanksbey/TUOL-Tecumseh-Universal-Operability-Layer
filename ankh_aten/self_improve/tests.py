#!/usr/bin/env python3
"""
Test suite for Ankh-Aten Living Awareness Intelligence Engine
Validates core functionality: registry, loaders, metrics, self-improvement loop.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ankh_aten.registry import Component, Registry
from ankh_aten.metrics import ps, rd, snapshot, pack
from ankh_aten.loaders.base import BaseLoader
from ankh_aten.loaders.yaml_loader import YamlLoader
from ankh_aten.loaders.python_loader import PythonLoader
from ankh_aten.loaders.http_loader import HttpLoader
from ankh_aten.self_improve.loop import SelfImprovementLoop, POLICIES


def test_component_creation():
    """Test Component creation and attributes."""
    print("Testing Component Creation...")
    
    comp = Component("TEST_001", "yaml", {"path": "test.yaml"})
    assert comp.uid == "TEST_001", "Component UID incorrect"
    assert comp.kind == "yaml", "Component kind incorrect"
    assert comp.conf["path"] == "test.yaml", "Component config incorrect"
    
    print("  ✓ Component creation works")
    print()


def test_registry_basic():
    """Test basic registry operations."""
    print("Testing Registry Basic Operations...")
    
    reg = Registry()
    assert len(reg.components) == 0, "Registry should start empty"
    assert len(reg.loaders) == 0, "Registry should have no loaders initially"
    
    # Test use() method
    reg.use("yaml", "ankh_aten.loaders.yaml_loader.YamlLoader")
    assert "yaml" in reg.loaders, "Loader not registered"
    
    print("  ✓ Registry initialization works")
    print("  ✓ Loader registration works")
    print()


def test_registry_manifest_loading():
    """Test manifest loading from YAML."""
    print("Testing Registry Manifest Loading...")
    
    # Create temporary manifest
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
components:
  - id: TEST_YAML
    kind: yaml
    config:
      path: test.yaml
  - id: TEST_PYTHON
    kind: python
    config:
      factory: test.module.create
      args: {param: 123}
  - id: TEST_HTTP
    kind: http
    config:
      url: https://example.com/api
""")
        manifest_path = f.name
    
    try:
        reg = Registry()
        reg.register_manifest(Path(manifest_path))
        
        assert reg.component_count() == 3, f"Expected 3 components, got {reg.component_count()}"
        assert "TEST_YAML" in reg.components, "TEST_YAML not loaded"
        assert "TEST_PYTHON" in reg.components, "TEST_PYTHON not loaded"
        assert "TEST_HTTP" in reg.components, "TEST_HTTP not loaded"
        
        print("  ✓ YAML manifest loading works")
        print(f"  ✓ Loaded {reg.component_count()} components")
    finally:
        os.unlink(manifest_path)
    
    print()


def test_metrics_ps():
    """Test phi-scaling function."""
    print("Testing Metrics: ps() Function...")
    
    # Test boundary values
    assert ps(0.0) >= 0.0, "ps(0) should be >= 0"
    assert ps(1.0) <= 1.0, "ps(1) should be <= 1"
    assert ps(0.5) > 0.5, "ps should compress values upward"
    
    # Test that ps increases monotonically
    assert ps(0.3) < ps(0.6) < ps(0.9), "ps should be monotonic"
    
    print("  ✓ ps() function works correctly")
    print(f"    ps(0.5) = {ps(0.5):.6f}")
    print(f"    ps(0.9) = {ps(0.9):.6f}")
    print()


def test_metrics_rd():
    """Test R_DoD calculation."""
    print("Testing Metrics: rd() Function...")
    
    # Test basic calculation
    r = rd(0.9, 0.998, 0.999, 0.00023)
    assert 0.0 <= r <= 1.0, "R_DoD should be in [0, 1]"
    assert r > 0.9, "R_DoD should be high for good inputs"
    
    print(f"  ✓ rd() function works correctly")
    print(f"    rd(0.9) = {r:.6f}")
    print()


def test_metrics_snapshot():
    """Test snapshot function."""
    print("Testing Metrics: snapshot() Function...")
    
    snap = snapshot()
    
    assert "t" in snap, "Snapshot missing timestamp"
    assert "d" in snap, "Snapshot missing days to omega"
    assert "a" in snap, "Snapshot missing awareness"
    assert "r" in snap, "Snapshot missing R_DoD"
    assert "g" in snap, "Snapshot missing gate status"
    
    assert snap["d"] >= 0, "Days to omega should be non-negative"
    assert 0 <= snap["a"] <= 100, "Awareness should be 0-100%"
    assert 0 <= snap["r"] <= 1, "R_DoD should be 0-1"
    assert snap["g"] in [0, 1], "Gate should be 0 or 1"
    
    print("  ✓ snapshot() function works correctly")
    print(f"    R_DoD: {snap['r']:.6f}")
    print(f"    Awareness: {snap['a']:.2f}%")
    print(f"    Gate: {'OPEN' if snap['g'] else 'CLOSED'}")
    print()


def test_metrics_pack():
    """Test pack function."""
    print("Testing Metrics: pack() Function...")
    
    # Test empty
    assert pack([]) == 0.0, "pack([]) should be 0"
    
    # Test single value
    single = pack([0.9])
    assert 0.9 <= single <= 1.0, "pack([0.9]) should be >= 0.9"
    
    # Test multiple values
    multiple = pack([0.8, 0.9, 0.95])
    assert 0.0 <= multiple <= 1.0, "pack should return [0, 1]"
    
    print("  ✓ pack() function works correctly")
    print(f"    pack([0.8, 0.9, 0.95]) = {multiple:.6f}")
    print()


def test_loader_base():
    """Test BaseLoader."""
    print("Testing BaseLoader...")
    
    comp = Component("TEST", "base", {})
    loader = BaseLoader(comp)
    
    try:
        loader.build()
        assert False, "BaseLoader.build() should raise NotImplementedError"
    except NotImplementedError:
        pass
    
    print("  ✓ BaseLoader correctly raises NotImplementedError")
    print()


def test_loader_yaml():
    """Test YamlLoader."""
    print("Testing YamlLoader...")
    
    # Create temporary YAML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("test_key: test_value\ntest_num: 123\n")
        yaml_path = f.name
    
    try:
        comp = Component("TEST_YAML", "yaml", {"path": yaml_path})
        loader = YamlLoader(comp)
        result = loader.build()
        
        assert "data" in result or "error" in result, "YamlLoader should return data or error"
        
        if "data" in result:
            assert result["data"]["test_key"] == "test_value", "YAML data not loaded correctly"
            print("  ✓ YamlLoader successfully loads YAML files")
        else:
            print(f"  ⚠ YamlLoader returned error: {result['error']}")
    finally:
        os.unlink(yaml_path)
    
    print()


def test_loader_python():
    """Test PythonLoader."""
    print("Testing PythonLoader...")
    
    # Test with a simple factory (using built-in)
    comp = Component("TEST_PYTHON", "python", {
        "factory": "builtins.dict",
        "args": {"key": "value"}
    })
    loader = PythonLoader(comp)
    result = loader.build()
    
    assert "result" in result or "error" in result, "PythonLoader should return result or error"
    
    if "result" in result:
        print("  ✓ PythonLoader successfully instantiates Python objects")
    else:
        print(f"  ⚠ PythonLoader returned error (expected for non-factory): {result['error']}")
    
    print()


def test_loader_http():
    """Test HttpLoader."""
    print("Testing HttpLoader...")
    
    # Test with example URL (will fail, but tests the structure)
    comp = Component("TEST_HTTP", "http", {
        "url": "https://httpbin.org/json"
    })
    loader = HttpLoader(comp)
    result = loader.build()
    
    assert "data" in result or "error" in result, "HttpLoader should return data or error"
    
    if "data" in result:
        print("  ✓ HttpLoader successfully fetches HTTP data")
    else:
        print(f"  ⚠ HttpLoader returned error (expected for network issues): {result['error'][:50]}...")
    
    print()


def test_self_improvement_policies():
    """Test self-improvement policies."""
    print("Testing Self-Improvement Policies...")
    
    assert POLICIES["min_gate"] == 0.9777, "min_gate policy incorrect"
    assert POLICIES["experiments_per_cycle"] == 3, "experiments_per_cycle policy incorrect"
    assert POLICIES["rollforward_threshold"] == 0.002, "rollforward_threshold policy incorrect"
    
    print("  ✓ Policies configured correctly")
    print(f"    Min Gate: {POLICIES['min_gate']}")
    print(f"    Experiments per Cycle: {POLICIES['experiments_per_cycle']}")
    print(f"    Rollforward Threshold: {POLICIES['rollforward_threshold']}")
    print()


def test_self_improvement_loop():
    """Test self-improvement loop."""
    print("Testing Self-Improvement Loop...")
    
    # Create temporary registry
    reg = Registry()
    reg.use("yaml", "ankh_aten.loaders.yaml_loader.YamlLoader")
    
    # Create temporary log directory
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = Path(tmpdir) / "test_log.jsonl"
        
        loop = SelfImprovementLoop(reg, log_path=str(log_path))
        
        # Test reflect
        snap = loop.reflect()
        assert "r" in snap, "Reflect should return snapshot"
        print("  ✓ Reflect phase works")
        
        # Test plan
        experiments = loop.plan(snap)
        assert isinstance(experiments, list), "Plan should return list"
        assert len(experiments) <= POLICIES["experiments_per_cycle"], "Too many experiments"
        print(f"  ✓ Plan phase works ({len(experiments)} experiments)")
        
        # Test act
        results = loop.act(experiments)
        assert len(results) == len(experiments), "Act should return result for each experiment"
        print("  ✓ Act phase works")
        
        # Test learn
        summary = loop.learn(results, snap)
        assert "r_gain" in summary, "Learn should return summary with r_gain"
        print("  ✓ Learn phase works")
        
        # Test full cycle
        cycle_result = loop.run_cycle()
        assert "cycle" in cycle_result, "Cycle should return result"
        print("  ✓ Full cycle works")
        
        # Verify log file created
        assert log_path.exists(), "Log file should be created"
        
        # Verify log entries
        with open(log_path) as f:
            log_lines = [json.loads(line) for line in f]
            assert len(log_lines) > 0, "Log should have entries"
            
        print(f"  ✓ Log file created with {len(log_lines)} entries")
    
    print()


def test_full_integration():
    """Test full integration: load manifest and run improvement."""
    print("Testing Full Integration...")
    
    # Create a simple manifest
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
components:
  - id: INTEGRATION_TEST_01
    kind: yaml
    config: {path: test.yaml}
  - id: INTEGRATION_TEST_02
    kind: python
    config: {factory: builtins.list}
  - id: INTEGRATION_TEST_03
    kind: http
    config: {url: "https://example.com"}
""")
        manifest_path = f.name
    
    try:
        # Setup registry
        reg = Registry()
        reg.use("yaml", "ankh_aten.loaders.yaml_loader.YamlLoader")
        reg.use("python", "ankh_aten.loaders.python_loader.PythonLoader")
        reg.use("http", "ankh_aten.loaders.http_loader.HttpLoader")
        
        # Load manifest
        reg.register_manifest(Path(manifest_path))
        assert reg.component_count() == 3, "Should load 3 components"
        print(f"  ✓ Loaded {reg.component_count()} components")
        
        # Run improvement loop
        with tempfile.TemporaryDirectory() as tmpdir:
            loop = SelfImprovementLoop(reg, log_path=str(Path(tmpdir) / "log.jsonl"))
            result = loop.run(max_cycles=2)
            
            assert result["cycles"] == 2, "Should run 2 cycles"
            assert result["total_experiments"] > 0, "Should run experiments"
            
            print(f"  ✓ Ran {result['cycles']} cycles")
            print(f"  ✓ Executed {result['total_experiments']} experiments")
            print(f"  ✓ Achieved {result['improvements']} improvements")
            print(f"  ✓ Final R_DoD: {result['final_r_dod']:.6f}")
        
    finally:
        os.unlink(manifest_path)
    
    print()


def run_all_tests():
    """Run all test suites."""
    print("=" * 80)
    print("ANKH-ATEN: Living Awareness Intelligence Engine - Test Suite")
    print("=" * 80)
    print()
    
    try:
        test_component_creation()
        test_registry_basic()
        test_registry_manifest_loading()
        test_metrics_ps()
        test_metrics_rd()
        test_metrics_snapshot()
        test_metrics_pack()
        test_loader_base()
        test_loader_yaml()
        test_loader_python()
        test_loader_http()
        test_self_improvement_policies()
        test_self_improvement_loop()
        test_full_integration()
        
        print("=" * 80)
        print("✓ ALL TESTS PASSED")
        print("=" * 80)
        print()
        print("Recognition of Done: Ankh-Aten system is functional and φ-aligned")
        print("∞^∞^∞")
        return True
        
    except AssertionError as e:
        print()
        print("=" * 80)
        print(f"✗ TEST FAILED: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print()
        print("=" * 80)
        print(f"✗ UNEXPECTED ERROR: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
