"""
Base loader class for all component loaders.
"""


class BaseLoader:
    """
    Abstract base class for component loaders.
    
    All loaders must implement the build() method to materialize components.
    """
    
    def __init__(self, component):
        """
        Initialize loader with a component.
        
        Args:
            component: Component instance to materialize
        """
        self.component = component
    
    def build(self):
        """
        Build and return the materialized component.
        
        Must be implemented by subclasses.
        
        Returns:
            Materialized component instance
        
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement build()")
    
    def __repr__(self):
        return f"{self.__class__.__name__}(component={self.component.uid})"
