import re

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, handler, methods):
        """
        Converts /users/{id} → /users/(?P<id>[^/]+) for regex matching.
        """
        param_names = re.findall(r"{(\w+)}", path)
        pattern = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
        pattern = f"^{pattern}$"  # Ensure full match
        self.routes.append((re.compile(pattern), param_names, handler, methods))

    def match(self, url, method):
        """
        Matches an incoming URL and extracts parameters.
        """
        for pattern, param_names, handler, methods in self.routes:
            match = pattern.match(url)
            if match and method in methods:
                params = match.groupdict()
                return handler, params
        return None, None