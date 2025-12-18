"""
YAML Loader: Load component configuration from YAML files.
"""

from pathlib import Path
import yaml
from .base import BaseLoader


class YamlLoader(BaseLoader):
    """
    Loads component configuration from YAML files.
    
    Expected config:
        - path: Path to YAML file (relative or absolute)
    """
    
    def build(self):
        """
        Load and return YAML configuration.
        
        Returns:
            dict: Loaded YAML data
        
        Raises:
            FileNotFoundError: If YAML file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        yaml_path = Path(self.component.conf.get("path", ""))
        
        if not yaml_path.exists():
            # Try relative to project root
            yaml_path = Path.cwd() / yaml_path
        
        if not yaml_path.exists():
            return {
                "error": f"YAML file not found: {yaml_path}",
                "component": self.component.uid,
                "kind": "yaml",
                "config": self.component.conf
            }
        
        try:
            data = yaml.safe_load(yaml_path.read_text())
            return {
                "component": self.component.uid,
                "kind": "yaml",
                "data": data,
                "source": str(yaml_path)
            }
        except yaml.YAMLError as e:
            return {
                "error": f"YAML parsing error: {e}",
                "component": self.component.uid,
                "kind": "yaml",
                "source": str(yaml_path)
            }
