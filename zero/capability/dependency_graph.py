"""Project ZERO — Capability Dependency Graph.

Directed Acyclic Graph (DAG) for verifying compatibility, detecting circular dependencies,
preventing invalid upgrades, and protecting against breaking changes.
"""

from typing import Dict, List, Set, Tuple, Optional
from zero_logging import logger


class DependencyGraph:
    """DAG managing capability dependencies and version compatibility."""

    def __init__(self) -> None:
        # capability_name -> set of dependencies (capability names required by key)
        self._adj: Dict[str, Set[str]] = {}
        # capability_name -> version
        self._versions: Dict[str, str] = {}

    def add_capability(self, name: str, version: str = "1.0.0", dependencies: Optional[List[str]] = None) -> None:
        """Add or update node in dependency graph."""
        name_key = name.lower()
        deps = set(d.lower() for d in (dependencies or []))
        self._adj[name_key] = deps
        self._versions[name_key] = version
        logger.debug(f"[DependencyGraph] Added node '{name_key}' v{version} deps={list(deps)}")

    def remove_capability(self, name: str) -> None:
        """Remove capability node."""
        name_key = name.lower()
        if name_key in self._adj:
            del self._adj[name_key]
        if name_key in self._versions:
            del self._versions[name_key]

        # Clean up dependency references
        for key, deps in self._adj.items():
            deps.discard(name_key)

    def get_dependents(self, name: str) -> List[str]:
        """Find capabilities that directly or indirectly depend on `name`."""
        name_key = name.lower()
        dependents: List[str] = []
        for cap, deps in self._adj.items():
            if name_key in deps:
                dependents.append(cap)
        return dependents

    def can_install(self, name: str, dependencies: Optional[List[str]] = None) -> Tuple[bool, List[str]]:
        """Verify if a capability can be safely installed given current state."""
        deps = [d.lower() for d in (dependencies or [])]
        missing: List[str] = []
        for dep in deps:
            if dep not in self._adj and dep not in self._versions:
                missing.append(dep)

        if missing:
            return False, [f"Missing required dependency capabilities: {', '.join(missing)}"]

        # Check for potential cycle if installed
        temp_graph = {k: set(v) for k, v in self._adj.items()}
        temp_graph[name.lower()] = set(deps)

        has_cycle, cycle_path = self._detect_cycle(temp_graph)
        if has_cycle:
            return False, [f"Installing '{name}' creates circular dependency: {' -> '.join(cycle_path)}"]

        return True, []

    def can_remove(self, name: str) -> Tuple[bool, List[str]]:
        """Check if capability can be removed without breaking dependents."""
        dependents = self.get_dependents(name)
        if dependents:
            return False, [f"Cannot remove '{name}'; relied upon by active capabilities: {', '.join(dependents)}"]
        return True, []

    def validate_graph(self) -> Tuple[bool, List[str]]:
        """Validate entire graph for missing dependencies or cycles."""
        errors: List[str] = []
        # Check missing deps
        for cap, deps in self._adj.items():
            for dep in deps:
                if dep not in self._adj:
                    errors.append(f"Capability '{cap}' references non-existent dependency '{dep}'")

        # Check cycles
        has_cycle, cycle_path = self._detect_cycle(self._adj)
        if has_cycle:
            errors.append(f"Circular dependency detected in graph: {' -> '.join(cycle_path)}")

        return (len(errors) == 0), errors

    def _detect_cycle(self, graph: Dict[str, Set[str]]) -> Tuple[bool, List[str]]:
        """DFS cycle detector."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        path: List[str] = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    path.append(neighbor)
                    return True

            path.pop()
            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True, path

        return False, []
