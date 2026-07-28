"""Project ZERO — Cognitive Knowledge Graph Subsystem (Phase 4 Capability #15)."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class GraphEdge(BaseModel):
    """Relationship link between two knowledge nodes."""

    source: str
    relation: str
    target: str


class KnowledgeGraphNode(BaseModel):
    """Knowledge Graph entity node."""

    name: str
    type: str = "entity"
    properties: Dict[str, Any] = Field(default_factory=dict)


class CognitiveKnowledgeGraph:
    """Cognitive Knowledge Graph linking memories and project entities into relational networks."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = (storage_file or (Path.cwd() / "data" / "knowledge_graph.json")).resolve()
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.nodes: Dict[str, KnowledgeGraphNode] = {}
        self.edges: List[GraphEdge] = []
        self._load()

    def _load(self):
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.nodes = {k: KnowledgeGraphNode(**v) for k, v in data.get("nodes", {}).items()}
                    self.edges = [GraphEdge(**e) for e in data.get("edges", [])]
            except Exception:
                pass

    def _save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump({
                    "nodes": {k: v.model_dump() for k, v in self.nodes.items()},
                    "edges": [e.model_dump() for e in self.edges]
                }, f, indent=2)
        except Exception:
            pass

    def add_relation(self, source: str, relation: str, target: str) -> GraphEdge:
        """Create connected relationship link between two entities."""
        if source not in self.nodes:
            self.nodes[source] = KnowledgeGraphNode(name=source)
        if target not in self.nodes:
            self.nodes[target] = KnowledgeGraphNode(name=target)

        edge = GraphEdge(source=source, relation=relation, target=target)
        if not any(e.source == source and e.relation == relation and e.target == target for e in self.edges):
            self.edges.append(edge)
            self._save()
        return edge

    def query_entity(self, entity_name: str) -> Dict[str, Any]:
        """Query linked relationships for a target entity."""
        name_lower = entity_name.lower()
        related_edges = [
            e for e in self.edges
            if e.source.lower() == name_lower or e.target.lower() == name_lower
        ]

        return {
            "entity": entity_name,
            "relationships": [f"{e.source} --[{e.relation}]--> {e.target}" for e in related_edges]
        }
