from __future__ import annotations

from typing import Hashable, Any
from copy import deepcopy


class Link(dict[Any, Any]):
    """Directed graph link from node ``i`` to node ``j``."""

    def __init__(self, idx: Hashable, i: Hashable, j: Hashable, **kwargs: Any) -> None:
        """Create a link with an identifier, start node, and end node."""
        super().__init__(**kwargs)
        dict.__setitem__(self, "idx", idx) # pyright: ignore[reportUnknownMemberType]
        dict.__setitem__(self, "i", i) # pyright: ignore[reportUnknownMemberType]
        dict.__setitem__(self, "j", j) # pyright: ignore[reportUnknownMemberType]

    @property
    def idx(self) -> Hashable:
        """Link identifier."""
        return dict.__getitem__(self, "idx") # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

    @property
    def i(self) -> Hashable:
        """Start node identifier."""
        return dict.__getitem__(self, "i") # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

    @property
    def j(self) -> Hashable:
        """End node identifier."""
        return dict.__getitem__(self, "j") # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

    def copy(self) -> Link:
        """Return a deep copy of the link."""
        return deepcopy(self)


__all__ = ["Link"]
