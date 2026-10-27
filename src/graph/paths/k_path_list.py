from __future__ import annotations

from collections.abc import Generator, Hashable
from typing import Any

from .k_path_container import KPathContainer
from .path import Path

Numeric = int | float


class KPathList(KPathContainer):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.update(**kwargs)
        self["type"] = self.__class__.__name__
        if "paths" not in self:
            self["paths"] = {}
        if "ull" not in self:
            self["ull"] = {}

    @property
    def _paths(self) -> dict[tuple[Hashable, Hashable, Numeric, str | None], list[Path]]:
        return self["paths"]  # type: ignore

    def add_path(self, to_add: Path, k: int | None = None, **kwargs: Any):
        to_add["links"] = self["ull"].setdefault(to_add["links"], to_add["links"])  # type: ignore
        key = to_add.key()
        links: list[Path | None] = self._paths.setdefault(key, [])  # type: ignore
        if k is None:
            links.append(to_add)  # type: ignore
            to_add["k"] = len(links) - 1
        else:
            links.extend([None] * (k + 1 - len(links))) if len(links) < k + 1 else links  # type: ignore
            links[k] = to_add
            to_add["k"] = k

    def get_sources(
        self,
        target: Hashable | None = None,
        t_start: Numeric | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        return tuple(
            set(
                [
                    s
                    for (s, t, ts, m) in map(lambda x: x.key(), self.all_paths())
                    if (t_start is None or ts == t_start) and (target is None or t == target) and (mode is None or m == mode)
                ]
            )
        )

    def get_targets(
        self,
        source: Hashable | None = None,
        t_start: Numeric | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        return tuple(
            set(
                [
                    t
                    for (s, t, ts, m) in map(lambda x: x.key(), self.all_paths())
                    if (source is None or s == source) and (t_start is None or ts == t_start) and (mode is None or m == mode)
                ]
            )
        )

    def get_t_starts(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Numeric, ...]:
        return tuple(
            set(
                [
                    ts
                    for (s, t, ts, m) in map(lambda x: x.key(), self.all_paths())
                    if (source is None or s == source) and (target is None or t == target) and (mode is None or m == mode)
                ]
            )
        )

    def get_ts(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> tuple[Numeric, ...]:
        return tuple(
            set(
                [
                    p["t"]
                    for p in self.all_paths()
                    if (source is None or p["source"] == source) and
                      (target is None or p["target"] == target) and 
                      (mode is None or p["mode"] == mode)
                ]
            )
        )
    
    def get_modes(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        t_start: Numeric | None = None,
        **kwargs: Any,
    ) -> tuple[Hashable, ...]:
        return tuple(
            set(
                [
                    m
                    for (s, t, ts, m) in map(lambda x: x.key(), self.all_paths())
                    if (source is None or s == source) and (t_start is None or ts == t_start) and (target is None or t == target)
                ]
            )
        )

    def paths(
        self,
        source: Hashable | None = None,
        target: Hashable | None = None,
        t_start: Numeric | None = None,
        mode: str | None = None,
        **kwargs: Any,
    ) -> Generator[Path, None, None]:
        if mode is None or source is None or target is None or t_start is None:
            for p in self.all_paths():
                if source is not None and p.source != source:
                    continue
                if target is not None and p.target != target:
                    continue
                if t_start is not None and p.t_start != t_start:
                    continue
                if mode is not None and p.mode != mode:
                    continue
                yield p
        else:
            yield from self._paths.get((source, target, t_start, mode), [])

    def path(
        self,
        source: Hashable,
        target: Hashable,
        t_start: Numeric | None = None,
        mode: str | None = None,
        k: int = 0,
        **kwargs: Any,
    ) -> Path | None:
        assert t_start is not None, "t_start must be specified"
        paths = self._paths.get((source, target, t_start, mode))
        if paths and len(paths) > k:
            return paths[k]
        else:
            return None

    def all_paths(self, **kwargs: Any) -> Generator[Path]:
        for paths in self["paths"].values():  # type: ignore
            yield from paths

    def all_kpaths(self, **kwargs: Any) -> Generator[tuple[tuple[Hashable, Hashable, Numeric, str | None], list[Path]]]:
        yield from self["paths"].items()  # type: ignore


    @property
    def empty(self) -> bool:
        if len(self._paths) == 0:
            return True
        return all(len(paths) == 0 for paths in self._paths.values())
    
    def n_paths(self, **kwargs: Any) -> int:
        n = 0
        for paths in self._paths.values():
            n += len(paths)
        return n

    def n_unique_paths(self, **kwargs: Any) -> int:
        return len(self["ull"])  # type: ignore

    def k_paths(self, **kwargs: Any) -> int:
        k = 0
        for paths in self._paths.values():
            k = max(k, len(paths))
        return k

    def is_empty(self) -> bool:
        return len(self._paths) == 0


__all__ = ["KPathList"]
