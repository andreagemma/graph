from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator, Hashable
from pathlib import Path as FilePath
from typing import Any

import dill

from .path import Path

Numeric = int | float


class PathContainer(ABC, dict):
    """Abstract base class for path collections."""

    def __init__(self, **kwargs: Any) -> None:
        """Create an empty path container with optional metadata."""
        super().__init__()
        self.update(**kwargs)
        self["type"] = self.__class__.__name__

    def add_path(self, to_add: Path, **kwargs: Any) -> None:
        """Add one path to the container."""
        raise NotImplementedError

    def merge(self, to_add: Path | PathContainer, **kwargs: Any) -> None:
        """Merge one path or another container into this container."""
        if isinstance(to_add, Path):
            self.add_path(to_add, **kwargs)
        elif isinstance(to_add, PathContainer):
            for path in to_add.all_paths(**kwargs):
                self.add_path(path)

    @abstractmethod
    def get_sources(
        self,
        target: Hashable | None = None,
        t_start: Numeric | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        """Return source labels matching the optional filters."""
        raise NotImplementedError

    @abstractmethod
    def get_targets(
        self,
        source: Hashable | None = None,
        t_start: Numeric | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        """Return target labels matching the optional filters."""
        raise NotImplementedError

    @abstractmethod
    def get_t_starts(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Numeric, ...]:
        """Return departure times matching the optional filters."""
        raise NotImplementedError

    @abstractmethod
    def get_modes(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        t_start: Numeric | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        """Return mode labels matching the optional filters."""
        raise NotImplementedError

    @abstractmethod
    def all_paths(self, **kwargs: Any) -> Generator[Path, None, None]:
        """Yield all paths in the container."""
        raise NotImplementedError

    def counts_tot_links(self, **kwargs: Any) -> int:
        """Count the total number of link occurrences in all matching paths."""
        return sum(len(path.get_links()) for path in self.all_paths(**kwargs))

    def counts_link(self, id_link: Hashable, **kwargs: Any) -> int:
        """Count occurrences of ``id_link`` in all matching paths."""
        return sum(path.counts_link(id_link) for path in self.all_paths(**kwargs))

    def n_paths(self, **kwargs: Any) -> int:
        """Count all matching paths."""
        return sum(1 for _ in self.all_paths(**kwargs))

    def save(self, filename: str | FilePath) -> None:
        """Serialize the container to ``filename`` using dill."""
        with open(filename, "wb") as file:
            dill.dump(self, file, dill.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename: str | FilePath) -> PathContainer:
        """Load a serialized path container from ``filename``."""
        with open(filename, "rb") as file:
            return dill.load(file)


__all__ = ["PathContainer"]
