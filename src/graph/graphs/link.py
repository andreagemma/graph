from __future__ import annotations

from collections.abc import Hashable
from copy import deepcopy
from typing import Any


class Link(dict[Any, Any]):
    """Directed graph link from node ``i`` to node ``j``."""

    def __init__(self, idx: Hashable, i: Hashable, j: Hashable, **kwargs: Any) -> None:
        """Create a link with an identifier, start node, and end node."""
        super().__init__(**kwargs)
        self["idx"] = idx
        self["i"] = i
        self["j"] = j

    @property
    def idx(self) -> Hashable:
        """Link identifier."""
        return self["idx"]

    @property
    def i(self) -> Hashable:
        """Start node identifier."""
        return self["i"]

    @property
    def j(self) -> Hashable:
        """End node identifier."""
        return self["j"]

    def copy(self) -> Link:
        """Return a deep copy of the link."""
        return deepcopy(self)


__all__ = ["Link"]
