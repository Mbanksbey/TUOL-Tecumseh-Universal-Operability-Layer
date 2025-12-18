"""
Python Loader: Dynamically instantiate Python factories.
"""

from importlib import import_module
from .base import BaseLoader


class PythonLoader(BaseLoader):
    """
    Dynamically instantiates Python objects via factory functions.
    
    Expected config:
        - factory: Dotted path to factory function (e.g., 'module.submodule.factory_func')
        - args: Dict of arguments to pass to factory (optional)
        - kwargs: Dict of keyword arguments to pass to factory (optional)
    """
    
    def build(self):
        """
        Instantiate Python object via factory function.
        
        Returns:
            Result of factory function call, or error dict if fails
        """
        factory_path = self.component.conf.get("factory", "")
        args = self.component.conf.get("args", {})
        kwargs = self.component.conf.get("kwargs", {})
        
        if not factory_path:
            return {
                "error": "No factory path specified",
                "component": self.component.uid,
                "kind": "python"
            }
        
        try:
            # Split module path and function name
            modpath, funcname = factory_path.rsplit(".", 1)
            
            # Import module and get factory function
            mod = import_module(modpath)
            factory = getattr(mod, funcname)
            
            # Call factory with arguments
            if isinstance(args, dict):
                # If args is a dict, pass as kwargs
                result = factory(**args)
            elif isinstance(args, (list, tuple)):
                # If args is a list/tuple, pass as positional args
                result = factory(*args, **kwargs)
            else:
                # Single argument
                result = factory(args, **kwargs)
            
            return {
                "component": self.component.uid,
                "kind": "python",
                "factory": factory_path,
                "result": result
            }
            
        except (ImportError, AttributeError, TypeError) as e:
            return {
                "error": f"Python factory error: {e}",
                "component": self.component.uid,
                "kind": "python",
                "factory": factory_path
            }
