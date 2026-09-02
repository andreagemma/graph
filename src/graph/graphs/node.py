from __future__ import annotations

from typing import Hashable, Any
from copy import deepcopy


class Node(dict[Any, Any]):
    """Graph node keyed by a stable identifier and arbitrary attributes."""

    def __init__(self, idx: Hashable, **kwargs: Any) -> None:
        """Create a node with an identifier and optional extra attributes."""
        super().__init__(**kwargs)
        dict.__setitem__(self, "idx", idx) # pyright: ignore[reportUnknownMemberType]

    @property
    def idx(self) -> Hashable:
        """Node identifier."""
        return dict.__getitem__(self, "idx")  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

    def copy(self) -> Node:
        """Return a deep copy of the node."""
        return deepcopy(self)


__all__ = ["Node"]
