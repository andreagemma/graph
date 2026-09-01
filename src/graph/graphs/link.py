from __future__ import annotations

from collections.abc import Hashable
from copy import deepcopy
from pathlib import Path as FilePath
from typing import Any

import dill


class Link(dict):
    """Directed graph link from node ``i`` to node ``j``."""

    def __init__(self, idx: Hashable, i: Hashable, j: Hashable, **kwargs: Any) -> None:
        """Create a link with an identifier, start node, and end node."""
        super().__init__(**kwargs)
        dict.__setitem__(self, "idx", idx)
        dict.__setitem__(self, "i", i)
        dict.__setitem__(self, "j", j)

    @property
    def idx(self) -> Hashable:
        """Link identifier."""
        return dict.__getitem__(self, "idx")

    @property
    def i(self) -> Hashable:
        """Start node identifier."""
        return dict.__getitem__(self, "i")

    @property
    def j(self) -> Hashable:
        """End node identifier."""
        return dict.__getitem__(self, "j")

    def save(self, filename: str | FilePath) -> None:
        """Serialize the link to ``filename`` using dill."""
        with open(filename, "wb") as file:
            dill.dump(self, file, dill.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename: str | FilePath) -> Link:
        """Load a serialized link from ``filename``."""
        with open(filename, "rb") as file:
            return dill.load(file)

    def copy(self) -> Link:
        """Return a deep copy of the link."""
        return deepcopy(self)


__all__ = ["Link"]
