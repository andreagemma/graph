from __future__ import annotations

from collections.abc import Generator, Hashable
from typing import Any

from .k_path_container import KPathContainer
from .path import Path

Numeric = int | float


class KPathList(KPathContainer):
    """Dictionary-backed collection with multiple k-ranked paths per key."""

    def __init__(self, **kwargs: Any) -> None:
        """Create an empty k-path list."""
        super().__init__()
        self.update(kwargs)
        self["type"] = self.__class__.__name__
        self["paths"] = {}

    def add_path(self, to_add: Path, k: int | None = None, **kwargs: Any) -> None:
        """Add a path at the next or selected k position."""
        del kwargs
        key = to_add.key()
        paths = self["paths"].setdefault(key, [])
        if k is None:
            paths.append(to_add)
            to_add["k"] = len(paths) - 1
        else:
            if len(paths) < k + 1:
                paths.extend([None] * (k + 1 - len(paths)))
            paths[k] = to_add
            to_add["k"] = k

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
                for source, candidate_target, candidate_time, candidate_mode in (
                    path.key() for path in self.all_paths()
                )
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
                for candidate_source, target, candidate_time, candidate_mode in (
                    path.key() for path in self.all_paths()
                )
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
                for candidate_source, candidate_target, t_start, candidate_mode in (
                    path.key() for path in self.all_paths()
                )
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
                for candidate_source, candidate_target, candidate_time, mode in (
                    path.key() for path in self.all_paths()
                )
                if (source is None or candidate_source == source)
                and (target is None or candidate_target == target)
                and (t_start is None or candidate_time == t_start)
            )
        )

    def paths(
        self,
        source: Hashable,
        target: Hashable,
        t_start: Numeric,
        mode: str | None = None,
        **kwargs: Any,
    ) -> Generator[Path, None, None]:
        """Yield all k-ranked paths matching one canonical key."""
        del kwargs
        for path in self["paths"].get((source, target, t_start, mode), []):
            if path is not None:
                yield path

    def path(
        self,
        source: Hashable,
        target: Hashable,
        t_start: Numeric | None = None,
        mode: str | None = None,
        k: int = 0,
        **kwargs: Any,
    ) -> Path | None:
        """Return one path by canonical key and k position."""
        del kwargs
        paths = self["paths"].get((source, target, t_start, mode))
        if paths and len(paths) > k:
            return paths[k]
        return None

    def all_paths(self, **kwargs: Any) -> Generator[Path, None, None]:
        """Yield all non-empty stored paths in insertion order."""
        del kwargs
        for paths in self["paths"].values():
            for path in paths:
                if path is not None:
                    yield path

    def all_kpaths(
        self,
        **kwargs: Any,
    ) -> Generator[tuple[tuple[Hashable, Hashable, Numeric, str | None], list[Path]], None, None]:
        """Yield each canonical key with its non-empty path list."""
        del kwargs
        for key, paths in self["paths"].items():
            yield key, [path for path in paths if path is not None]

    def n_paths(self, **kwargs: Any) -> int:
        """Count all non-empty stored paths."""
        del kwargs
        return sum(1 for _ in self.all_paths())

    def k_paths(self, **kwargs: Any) -> int:
        """Return the maximum number of k slots stored for any key."""
        del kwargs
        return max((len(paths) for paths in self["paths"].values()), default=0)


__all__ = ["KPathList"]
