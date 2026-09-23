from __future__ import annotations

from collections.abc import Hashable
from copy import deepcopy
from pathlib import Path as FilePath
from typing import Any

import dill

Numeric = int | float


class Path(dict):
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
        dict.__setitem__(self, "source", source)
        dict.__setitem__(self, "target", target)
        dict.__setitem__(self, "t_start", t_start)
        dict.__setitem__(self, "t_base", t_base)
        dict.__setitem__(self, "t", t_base + t_start)
        dict.__setitem__(self, "mode", mode)
        dict.__setitem__(self, "tot_cost", tot_cost if not cost_values else cost_values[-1])
        dict.__setitem__(self, "links", tuple() if links is None else tuple(links))
        dict.__setitem__(self, "costs", cost_values)

    def key(self) -> tuple[Hashable, Hashable, Numeric, str | None]:
        """Return the lookup key used by path containers."""
        return (
            dict.__getitem__(self, "source"),
            dict.__getitem__(self, "target"),
            dict.__getitem__(self, "t_start"),
            dict.__getitem__(self, "mode"),
        )

    def copy(self) -> Path:
        """Return a deep copy of the path."""
        return deepcopy(self)

    def get_links(self) -> tuple[Hashable, ...]:
        """Return the link identifiers in this path."""
        return dict.get(self, "links", tuple())

    def get_costs(self) -> tuple[Numeric, ...]:
        """Return the cumulative costs stored for this path."""
        return dict.get(self, "costs", tuple())

    def has_link(self, id_link: Hashable) -> bool:
        """Return ``True`` when ``id_link`` appears in the path."""
        return id_link in self.get_links()

    def counts_link(self, id_link: Hashable) -> int:
        """Count how many times ``id_link`` appears in the path."""
        return self.get_links().count(id_link)

    def save(self, filename: str | FilePath) -> None:
        """Serialize the path to ``filename`` using dill."""
        with open(filename, "wb") as file:
            dill.dump(self, file, dill.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename: str | FilePath) -> Path:
        """Load a serialized path from ``filename``."""
        with open(filename, "rb") as file:
            return dill.load(file)


__all__ = ["Path"]
