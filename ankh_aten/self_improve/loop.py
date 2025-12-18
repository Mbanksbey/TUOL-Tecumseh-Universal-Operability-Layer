"""
Self-Improvement Loop: Recursive reflection→plan→act→learn cycle
Implements autonomous system evolution with φ-aligned metrics.
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from ..metrics import snapshot, rd


# Self-improvement policies
POLICIES = {
    "min_gate": 0.9777,              # Minimum R_DoD for gate passage
    "experiments_per_cycle": 3,       # Number of experiments per cycle
    "rollforward_threshold": 0.002    # Minimum r-gain to keep changes
}


class SelfImprovementLoop:
    """
    Autonomous self-improvement system.
    
    Cycle:
        1. Reflect: Analyze current R_DoD metrics
        2. Plan: Generate experiments based on thresholds
        3. Act: Execute experiments
        4. Learn: Measure gains, keep improvements
    """
    
    def __init__(self, registry, log_path=".ankh_aten/log.jsonl"):
        """
        Initialize self-improvement loop.
        
        Args:
            registry: Component registry instance
            log_path: Path to log file for audit trail
        """
        self.registry = registry
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.cycle_count = 0
        self.total_experiments = 0
        self.improvements = 0
    
    def log_event(self, event_type, data):
        """
        Log event to audit trail.
        
        Args:
            event_type: Type of event (reflect, plan, act, learn)
            data: Event data dict
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": self.cycle_count,
            "type": event_type,
            "data": data
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
    
    def reflect(self):
        """
        Phase 1: Reflect on current system state.
        
        Returns:
            dict: Current metrics snapshot
        """
        snap = snapshot()
        
        self.log_event("reflect", {
            "r_dod": snap["r"],
            "awareness": snap["a"],
            "gate_status": snap["g"],
            "days_to_omega": snap["d"],
            "components": self.registry.component_count()
        })
        
        return snap
    
    def plan(self, snap):
        """
        Phase 2: Plan experiments based on current metrics.
        
        Args:
            snap: Current metrics snapshot
        
        Returns:
            list: Planned experiments
        """
        experiments = []
        r_current = snap["r"]
        gate_needed = POLICIES["min_gate"] - r_current
        
        # Generate experiments based on current state
        if r_current < POLICIES["min_gate"]:
            # Below threshold - prioritize gate passage
            experiments.append({
                "type": "expand_manifest",
                "description": "Add high-value components to manifest",
                "expected_gain": 0.003
            })
            experiments.append({
                "type": "optimize_loaders",
                "description": "Tune loader performance and caching",
                "expected_gain": 0.002
            })
            experiments.append({
                "type": "refine_metrics",
                "description": "Adjust phi-scaling parameters",
                "expected_gain": 0.001
            })
        else:
            # Above threshold - optimize and explore
            experiments.append({
                "type": "discover_components",
                "description": "Search for new quantum-coherent components",
                "expected_gain": 0.002
            })
            experiments.append({
                "type": "tune_awareness",
                "description": "Balance integration vector dimensions",
                "expected_gain": 0.001
            })
            experiments.append({
                "type": "cache_optimization",
                "description": "Implement component materialization cache",
                "expected_gain": 0.001
            })
        
        # Limit to policy count
        experiments = experiments[:POLICIES["experiments_per_cycle"]]
        
        self.log_event("plan", {
            "gate_needed": max(0, gate_needed),
            "experiments": len(experiments),
            "experiment_types": [e["type"] for e in experiments]
        })
        
        return experiments
    
    def act(self, experiments):
        """
        Phase 3: Execute planned experiments.
        
        Args:
            experiments: List of experiment dicts
        
        Returns:
            list: Executed experiment results
        """
        results = []
        
        for exp in experiments:
            # Simulate experiment execution
            # In real implementation, this would perform actual system changes
            result = {
                "type": exp["type"],
                "description": exp["description"],
                "executed": True,
                "actual_gain": random.uniform(0, exp["expected_gain"] * 1.5)
            }
            results.append(result)
            
            self.log_event("act", result)
        
        return results
    
    def learn(self, results, snap_before):
        """
        Phase 4: Learn from experiment results, keep improvements.
        
        Args:
            results: List of experiment results
            snap_before: Metrics snapshot before experiments
        
        Returns:
            dict: Learning summary
        """
        snap_after = snapshot()
        r_gain = snap_after["r"] - snap_before["r"]
        
        # Filter results by rollforward threshold
        kept = []
        rejected = []
        
        for result in results:
            if result["actual_gain"] >= POLICIES["rollforward_threshold"]:
                kept.append(result)
                self.improvements += 1
            else:
                rejected.append(result)
        
        summary = {
            "r_before": snap_before["r"],
            "r_after": snap_after["r"],
            "r_gain": r_gain,
            "kept": len(kept),
            "rejected": len(rejected),
            "improvements": self.improvements
        }
        
        self.log_event("learn", summary)
        
        return summary
    
    def run_cycle(self):
        """
        Run one complete self-improvement cycle.
        
        Returns:
            dict: Cycle summary
        """
        self.cycle_count += 1
        
        # Phase 1: Reflect
        snap_before = self.reflect()
        
        # Phase 2: Plan
        experiments = self.plan(snap_before)
        
        # Phase 3: Act
        results = self.act(experiments)
        self.total_experiments += len(results)
        
        # Phase 4: Learn
        summary = self.learn(results, snap_before)
        
        return {
            "cycle": self.cycle_count,
            "experiments": len(experiments),
            "r_gain": summary["r_gain"],
            "improvements": summary["improvements"]
        }
    
    def run(self, max_cycles=10):
        """
        Run multiple self-improvement cycles.
        
        Args:
            max_cycles: Maximum number of cycles to run
        
        Returns:
            dict: Overall summary
        """
        for i in range(max_cycles):
            cycle_summary = self.run_cycle()
            
            # Check if we've reached optimal state
            snap = snapshot()
            if snap["r"] >= 0.999:  # Near-perfect recognition
                break
        
        return {
            "cycles": self.cycle_count,
            "total_experiments": self.total_experiments,
            "improvements": self.improvements,
            "final_r_dod": snapshot()["r"]
        }
