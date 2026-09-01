from __future__ import annotations

from collections.abc import Hashable
from copy import deepcopy
from pathlib import Path as FilePath
from typing import Any

import dill


class Node(dict):
    """Graph node keyed by a stable identifier and arbitrary attributes."""

    def __init__(self, idx: Hashable, **kwargs: Any) -> None:
        """Create a node with an identifier and optional extra attributes."""
        super().__init__(**kwargs)
        dict.__setitem__(self, "idx", idx)

    @property
    def idx(self) -> Hashable:
        """Node identifier."""
        return dict.__getitem__(self, "idx")

    def save(self, filename: str | FilePath) -> None:
        """Serialize the node to ``filename`` using dill."""
        with open(filename, "wb") as file:
            dill.dump(self, file, dill.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename: str | FilePath) -> Node:
        """Load a serialized node from ``filename``."""
        with open(filename, "rb") as file:
            return dill.load(file)

    def copy(self) -> Node:
        """Return a deep copy of the node."""
        return deepcopy(self)


__all__ = ["Node"]
