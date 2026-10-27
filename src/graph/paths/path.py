from __future__ import annotations

from collections.abc import Hashable
from copy import deepcopy
from pathlib import Path as FilePath
from typing import Any, cast

from serializer import dump, load

Numeric = int | float


class Path(dict[str, Any]):
    """A path between two nodes at a departure time."""

    def __init__(
        self,
        source: Hashable,
        target: Hashable,
        t_start: Numeric,
        links: list[Hashable] | None = None,
        costs: list[Numeric] | None = None,
        tot_cost: Numeric = 0.0,
        mode: str | None = None,
        t_base: Numeric = 0,
        **kwargs: Any,
    ) -> None:
        """Create a path and store its link sequence and cumulative costs."""
        super().__init__()
        self.update(**kwargs)
        cost_values = tuple() if costs is None else tuple(costs)
        self["source"] = source
        self["target"] = target
        self["t_start"] = t_start
        self["t_base"] = t_base
        self["t"] = t_base + t_start
        self["mode"] = mode
        self["tot_cost"] = tot_cost if not cost_values else cost_values[-1]
        self["links"] = tuple() if links is None else tuple(links)
        self["costs"] = cost_values

    def key(self) -> tuple[Hashable, Hashable, Numeric, str | None]:
        """Return the lookup key used by path containers."""
        return (
            cast(Hashable, self["source"]),
            cast(Hashable, self["target"]),
            cast(Numeric, self["t_start"]),
            cast(str | None, self["mode"]),
        )

    @property
    def source(self) -> Hashable:
        return self["source"]

    @property
    def target(self) -> Hashable:
        return self["target"]

    @property
    def t_start(self) -> Numeric:
        return self["t_start"]

    @property
    def t_base(self) -> Numeric:
        return self["t_base"]

    @property
    def t(self) -> Numeric:
        return self["t"]

    @property
    def mode(self) -> str | None:
        return self["mode"]

    @property
    def tot_cost(self) -> Numeric:
        return self["tot_cost"]

    @property
    def links(self) -> tuple[Hashable, ...]:
        return self["links"]

    @property
    def costs(self) -> tuple[Numeric, ...]:
        return self["costs"]

    def copy(self) -> Path:
        """Return a deep copy of the path."""
        return deepcopy(self)

    def get_links(self) -> tuple[Hashable, ...]:
        """Return the link identifiers in this path."""
        return self["links"]

    def get_costs(self) -> tuple[Numeric, ...]:
        """Return the cumulative costs stored for this path."""
        return self["costs"]

    def has_link(self, id_link: Hashable) -> bool:
        """Return ``True`` when ``id_link`` appears in the path."""
        return id_link in self.get_links()

    def counts_link(self, id_link: Hashable) -> int:
        """Count how many times ``id_link`` appears in the path."""
        return self.get_links().count(id_link)

    def save(self, filename: str | FilePath, compression: str | None = None, level: int = 5) -> None:
        """Serialize the path to ``filename`` using dill."""
        with open(filename, "wb") as file:
            dump(self, file, compression=compression, level=level)

    @staticmethod
    def load(filename: str | FilePath) -> Path:
        """Load a serialized path from ``filename``."""
        with open(filename, "rb") as file:
            return load(file)


__all__ = ["Path"]
