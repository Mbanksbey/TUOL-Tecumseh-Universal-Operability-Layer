"""
HTTP Loader: Fetch JSON data from HTTP endpoints.
"""

import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from .base import BaseLoader


class HttpLoader(BaseLoader):
    """
    Fetches component data from HTTP endpoints.
    
    Expected config:
        - url: HTTP(S) URL to fetch
        - method: HTTP method (default: GET)
        - headers: Dict of HTTP headers (optional)
        - timeout: Request timeout in seconds (default: 30)
    """
    
    def build(self):
        """
        Fetch JSON data from HTTP endpoint.
        
        Returns:
            dict: Parsed JSON response or error dict
        """
        url = self.component.conf.get("url", "")
        method = self.component.conf.get("method", "GET")
        headers = self.component.conf.get("headers", {})
        timeout = self.component.conf.get("timeout", 30)
        
        if not url:
            return {
                "error": "No URL specified",
                "component": self.component.uid,
                "kind": "http"
            }
        
        try:
            # Create request with headers
            req = Request(url, method=method)
            for key, value in headers.items():
                req.add_header(key, value)
            
            # Fetch data
            with urlopen(req, timeout=timeout) as response:
                data = response.read().decode('utf-8')
                
                # Try to parse as JSON
                try:
                    json_data = json.loads(data)
                except json.JSONDecodeError:
                    # Return raw data if not JSON
                    json_data = data
                
                return {
                    "component": self.component.uid,
                    "kind": "http",
                    "url": url,
                    "status": response.status,
                    "data": json_data
                }
                
        except (URLError, HTTPError, TimeoutError) as e:
            return {
                "error": f"HTTP request failed: {e}",
                "component": self.component.uid,
                "kind": "http",
                "url": url
            }
