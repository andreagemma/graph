from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from collections.abc import Generator, Hashable
from pathlib import Path as FilePath
from typing import Any

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString

from ..graphs.graph import Graph
from ..utils import multiline_to_line
from .path import Path

Numeric = int | float


class PathContainer(ABC, dict[str, Any]):
    """Abstract base class for path collections."""

    def __init__(self, **kwargs: Any) -> None:
        """Create an empty path container with optional metadata."""
        super().__init__()
        self.update(**kwargs)  # type: ignore
        self["type"] = self.__class__.__name__

    def add_path(self, to_add: Path, **kwargs: Any) -> None:
        """Add one path to the container."""
        raise NotImplementedError

    def merge(self, to_add: Path | PathContainer, **kwargs: Any) -> None:
        """Merge one path or another container into this container."""
        if isinstance(to_add, Path):
            self.add_path(to_add, **kwargs)
        elif isinstance(to_add, PathContainer):  # type: ignore
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
        import dill  # type: ignore

        with open(filename, "wb") as file:
            dill.dump(self, file, dill.HIGHEST_PROTOCOL)  # type: ignore

    @staticmethod
    def load(filename: str | FilePath) -> PathContainer:
        """Load a serialized path container from ``filename``."""
        import dill  # type: ignore

        with open(filename, "rb") as file:
            return dill.load(file)  # type: ignore

    def to_pandas(self, G: Graph, crs_link: str = "EPSG:4326", t: Numeric | None = None) -> pd.DataFrame | gpd.GeoDataFrame:
        df_paths: pd.DataFrame = pd.DataFrame(path for path in self.all_paths() if t is None or path["t"] == t)
        if df_paths.empty:
            df_paths = gpd.GeoDataFrame(df_paths, geometry=[], crs=crs_link)
            return df_paths
        _link: dict[str, Any] = next(G.get_all_links())
        for geom in ("geom", "geometry"):
            if geom in _link:
                df_paths[geom] = [  # type: ignore
                    MultiLineString(
                        [multiline_to_line(link.get(geom)) for l_idx in links if (link := G.get_link(l_idx)) is not None]  # type: ignore
                    )
                    for links in df_paths["links"]
                ]
                df_paths = gpd.GeoDataFrame(df_paths, geometry=geom, crs=crs_link)
                return df_paths
        return df_paths

    def copy(self) -> PathContainer:
        """Return a shallow copy of the path container."""
        return copy.deepcopy(self)


__all__ = ["PathContainer"]
