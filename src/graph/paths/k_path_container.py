from __future__ import annotations

from collections.abc import Generator, Hashable
from typing import Any

from .path import Path
from .path_container import PathContainer

Numeric = int | float


class KPathContainer(PathContainer):
    """Abstract base class for collections with multiple paths per key."""

    def __init__(self, **kwargs: Any) -> None:
        """Create an empty k-path container."""
        super().__init__(**kwargs)
        self["type"] = self.__class__.__name__

    def add_path(self, to_add: Path, k: int | None = None, **kwargs: Any) -> None:
        """Add one path at an optional k position."""
        raise NotImplementedError

    def merge(
        self,
        to_add: Path | PathContainer | KPathContainer,
        override_k: bool = False,
        **kwargs: Any,
    ) -> None:
        """Merge another path collection into this k-path container."""
        if isinstance(to_add, Path):
            self.add_path(to_add, k=to_add.get("k") if override_k else None, **kwargs)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
        elif isinstance(to_add, PathContainer):  # pyright: ignore[reportUnnecessaryIsInstance]
            for path in to_add.all_paths(**kwargs):
                self.add_path(path, k=path.get("k") if override_k else None)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
        else:
            msg = f"merge is not implemented for {type(to_add)!r}"
            raise NotImplementedError(msg)

    def paths(
        self,
        source: Hashable,
        target: Hashable,
        t_start: Numeric,
        mode: str | None = None,
        **kwargs: Any,
    ) -> Generator[Path, None, None]:
        """Yield paths for a specific source, target, departure time, and mode."""
        raise NotImplementedError

    def path(
        self,
        source: Hashable,
        target: Hashable,
        t_start: Numeric,
        mode: str | None = None,
        k: int = 0,
        **kwargs: Any,
    ) -> Path | None:
        """Return a single path by k position."""
        raise NotImplementedError

    def all_kpaths(
        self,
        **kwargs: Any,
    ) -> Generator[tuple[tuple[Hashable, Hashable, Numeric, str | None], list[Path]], None, None]:
        """Yield each canonical key with its path list."""
        raise NotImplementedError

    def k_paths(self, **kwargs: Any) -> int:
        """Return the largest stored k index, or ``-1`` when empty."""
        return max((int(path.get("k", 0)) for path in self.all_paths(**kwargs)), default=-1)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

    def counts_tot_links(self, **kwargs: Any) -> int:
        """Count the total number of link occurrences in all matching paths."""
        return sum(len(path.get_links()) for path in self.all_paths(**kwargs))

    def counts_link(self, id_link: Hashable, **kwargs: Any) -> int:
        """Count occurrences of ``id_link`` in all matching paths."""
        return sum(path.counts_link(id_link) for path in self.all_paths(**kwargs))


__all__ = ["KPathContainer"]
