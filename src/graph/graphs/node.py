from __future__ import annotations

from collections.abc import Hashable
from copy import deepcopy
from typing import Any


class Node(dict[Any, Any]):
    """Graph node keyed by a stable identifier and arbitrary attributes."""

    def __init__(self, idx: Hashable, **kwargs: Any) -> None:
        """Create a node with an identifier and optional extra attributes."""
        super().__init__(**kwargs)
        self["idx"] = idx

    @property
    def idx(self) -> Hashable:
        """Node identifier."""
        return self["idx"]

    def copy(self) -> Node:
        """Return a deep copy of the node."""
        return deepcopy(self)


__all__ = ["Node"]
