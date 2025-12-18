"""
Component Registry System for Ankh-Aten
Manages 318+ components with unique IDs, kinds, and configurations.
Supports pluggable loaders (YAML, Python factory, HTTP, etc.).
"""

from importlib import import_module
from pathlib import Path
import yaml
import json


class Component:
    """Represents a component with unique ID, kind, and configuration."""
    
    def __init__(self, uid, kind, conf):
        self.uid = uid
        self.kind = kind
        self.conf = conf
    
    def __repr__(self):
        return f"Component(uid={self.uid!r}, kind={self.kind!r})"


class Registry:
    """
    Programmable registry for managing components and their loaders.
    
    Supports:
    - Dynamic loader registration via use()
    - Manifest loading from YAML/JSON files
    - Component materialization through registered loaders
    """
    
    def __init__(self):
        self.components = {}
        self.loaders = {}
    
    def use(self, kind: str, loader: str):
        """
        Register a loader for a specific component kind.
        
        Args:
            kind: Component kind (e.g., 'yaml', 'python', 'http')
            loader: Dotted path to loader class (e.g., 'ankh_aten.loaders.yaml_loader.YamlLoader')
        
        Returns:
            self for chaining
        """
        self.loaders[kind] = loader
        return self
    
    def register_manifest(self, path: Path):
        """
        Load components from a manifest file (YAML or JSON).
        
        Args:
            path: Path to manifest file (.yaml, .yml, or .json)
        """
        path = Path(path)
        
        # Load data based on file extension
        if str(path).endswith((".yml", ".yaml")):
            data = yaml.safe_load(path.read_text())
        else:
            data = json.loads(path.read_text())
        
        # Register each component
        for row in data.get("components", []):
            c = Component(
                row["id"],
                row["kind"],
                row.get("config", {})
            )
            self.components[c.uid] = c
    
    def materialize(self, uid: str):
        """
        Materialize a component by its unique ID using its registered loader.
        
        Args:
            uid: Unique component ID
        
        Returns:
            Materialized component instance
        
        Raises:
            KeyError: If component or loader not found
        """
        c = self.components[uid]
        Lpath = self.loaders[c.kind]
        
        # Dynamically import loader class
        modpath, clsname = Lpath.rsplit(".", 1)
        L = getattr(import_module(modpath), clsname)
        
        # Build and return component
        return L(c).build()
    
    def list_components(self):
        """Return list of all registered component IDs."""
        return list(self.components.keys())
    
    def component_count(self):
        """Return total count of registered components."""
        return len(self.components)
    
    def __repr__(self):
        return f"Registry(components={len(self.components)}, loaders={len(self.loaders)})"
