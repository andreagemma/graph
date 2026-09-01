from __future__ import annotations

from collections.abc import Generator, Hashable
from typing import Any

from .path import Path
from .path_container import PathContainer

Numeric = int | float


class PathList(PathContainer):
    """Dictionary-backed collection with at most one path per path key."""

    def __init__(self, **kwargs: Any) -> None:
        """Create an empty path list."""
        super().__init__()
        self.update(kwargs)
        dict.__setitem__(self, "class_name", self.__class__.__name__)
        dict.__setitem__(self, "paths", {})

    def add_path(self, to_add: Path, **kwargs: Any) -> None:
        """Add or replace a path by its canonical key."""
        del kwargs
        self["paths"][to_add.key()] = to_add

    def get_sources(
        self,
        target: Hashable | None = None,
        t_start: Numeric | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        """Return source labels matching the optional filters."""
        del kwargs
        return tuple(
            dict.fromkeys(
                source
                for source, candidate_target, candidate_time, candidate_mode in self["paths"]
                if (target is None or candidate_target == target)
                and (t_start is None or candidate_time == t_start)
                and (mode is None or candidate_mode == mode)
            )
        )

    def get_targets(
        self,
        source: Hashable | None = None,
        t_start: Numeric | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        """Return target labels matching the optional filters."""
        del kwargs
        return tuple(
            dict.fromkeys(
                target
                for candidate_source, target, candidate_time, candidate_mode in self["paths"]
                if (source is None or candidate_source == source)
                and (t_start is None or candidate_time == t_start)
                and (mode is None or candidate_mode == mode)
            )
        )

    def get_t_starts(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Numeric, ...]:
        """Return departure times matching the optional filters."""
        del kwargs
        return tuple(
            dict.fromkeys(
                t_start
                for candidate_source, candidate_target, t_start, candidate_mode in self["paths"]
                if (source is None or candidate_source == source)
                and (target is None or candidate_target == target)
                and (mode is None or candidate_mode == mode)
            )
        )

    def get_modes(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        t_start: Numeric | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        """Return mode labels matching the optional filters."""
        del kwargs
        return tuple(
            dict.fromkeys(
                mode
                for candidate_source, candidate_target, candidate_time, mode in self["paths"]
                if (source is None or candidate_source == source)
                and (target is None or candidate_target == target)
                and (t_start is None or candidate_time == t_start)
            )
        )

    def path(
        self,
        source: Hashable,
        target: Hashable | None = None,
        t_start: Numeric | None = 0,
        mode: str | None = None,
        **kwargs: Any,
    ) -> Path | None:
        """Return one path by key, or ``None`` when missing."""
        del kwargs
        return self["paths"].get((source, target, t_start, mode))

    def all_paths(self, **kwargs: Any) -> Generator[Path, None, None]:
        """Yield all paths in insertion order."""
        del kwargs
        yield from self["paths"].values()

    def n_paths(self, **kwargs: Any) -> int:
        """Count paths in the list."""
        del kwargs
        return len(self["paths"])


__all__ = ["PathList"]
