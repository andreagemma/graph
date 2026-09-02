from __future__ import annotations

import warnings
from collections.abc import Callable, Generator, Hashable, Iterable
from copy import deepcopy
from pathlib import Path as FilePath
from typing import Any

from .action_policy import ActionPolicy
from .exceptions import (
    ExistingLinkError,
    ExistingNodeError,
    ExistingTurnError,
    MissingLinkError,
    MissingNodeError,
)
from .link import Link
from .node import Node
from .turn import Turn

Numeric = int | float

class Graph(dict[Any, Any]):
    """Graph structure used to manage nodes, directed links, and turns."""

    def __init__(
        self,
        t0: float | int = 0,
        total_time: float | int = 60,
        delta_t: float | int = 15,
        **kwargs: Any,
    ) -> None:
        """Create an empty graph with a time discretization."""
        super().__init__()
        self.update(**kwargs)
        self["links"] = {}
        self["nodes"] = {}
        self["turns"] = {}
        self["t0"] = t0 
        self["total_time"] = total_time 
        self["delta_t"] = delta_t 
        self["num_intervals"] = int(total_time // delta_t) 

    @property
    def delta_t(self) -> float | int:
        """Duration of each time interval."""
        return self["delta_t"]

    @property
    def t0(self) -> float | int:
        """Base time used by time-dependent attributes."""
        return self["t0"]

    @property
    def total_time(self) -> float | int:
        """Total modelled time horizon."""
        return self["total_time"]

    @property
    def num_intervals(self) -> int:
        """Number of time intervals in the graph horizon."""
        return self["num_intervals"]

    def save(self, filename: str | FilePath) -> None: 
        """Serialize the graph to ``filename`` using dill."""
        try:

            import dill  # pyright: ignore[reportMissingTypeStubs]

            with open(filename, "wb") as file:
                dill.dump(self, file, dill.HIGHEST_PROTOCOL)  # pyright: ignore[reportUnknownMemberType]
        except ImportError as e:
            raise ImportError("dill is required for saving the graph.") from e

    @staticmethod
    def load(filename: str | FilePath) -> Graph:
        """Load a serialized graph from ``filename``."""
        try:

            import dill  # pyright: ignore[reportMissingTypeStubs]

            with open(filename, "rb") as file:
                return dill.load(file)  # pyright: ignore[reportUnknownMemberType]
        except ImportError as e:
            raise ImportError("dill is required for loading the graph.") from e

    def copy(self) -> Graph:
        """Return a deep copy of the graph."""
        return deepcopy(self)

    def add_link(
        self,
        idx: Hashable,
        i: Hashable,
        j: Hashable,
        on_existing: ActionPolicy = ActionPolicy.RAISE,
        on_missing_node: ActionPolicy = ActionPolicy.RAISE,
        **kwargs: Any,
    ) -> Link | None:
        """Add a directed link to the graph."""
        kwargs["delta_t"] = self.delta_t
        kwargs["total_time"] = self.total_time

        if not self._handle_missing_node(i, "Start", on_missing_node):
            return None
        if not self._handle_missing_node(j, "End", on_missing_node):
            return None

        links = self["links"]
        if idx in links:
            if on_existing == ActionPolicy.RAISE:
                raise ExistingLinkError(f"Link with id {idx} already exists.")
            if on_existing == ActionPolicy.WARN:
                warnings.warn(f"Link with id {idx} already exists.", stacklevel=2)
            if on_existing in {ActionPolicy.IGNORE, ActionPolicy.SKIP}:
                return links[idx]

        link = Link(idx=idx, i=i, j=j, **kwargs)
        links[idx] = link
        return link

    def _handle_missing_node(
        self,
        idx: Hashable,
        role: str,
        policy: ActionPolicy,
    ) -> bool:
        nodes = self["nodes"]
        if idx in nodes:
            return True
        if policy == ActionPolicy.RAISE:
            raise MissingNodeError(f"{role} node with id {idx} does not exist.")
        if policy == ActionPolicy.WARN:
            warnings.warn(f"{role} node with id {idx} does not exist.", stacklevel=3)
        elif policy == ActionPolicy.SKIP:
            return False
        elif policy == ActionPolicy.REPLACE:
            self.add_node(idx, on_existing=ActionPolicy.SKIP)
        return True

    def add_node(
        self,
        idx: Hashable,
        on_existing: ActionPolicy = ActionPolicy.RAISE,
        **kwargs: Any,
    ) -> Node:
        """Add a node to the graph."""
        nodes = self["nodes"]
        if idx in nodes:
            if on_existing == ActionPolicy.RAISE:
                raise ExistingNodeError(f"Node with id {idx} already exists.")
            if on_existing == ActionPolicy.WARN:
                warnings.warn(f"Node with id {idx} already exists.", stacklevel=2)
            if on_existing in {ActionPolicy.IGNORE, ActionPolicy.SKIP}:
                return nodes[idx]

        node = Node(idx=idx, **kwargs)
        nodes[idx] = node
        return node

    def add_turn(
        self,
        idx: Hashable,
        in_link: Hashable,
        out_link: Hashable,
        on_existing: ActionPolicy = ActionPolicy.RAISE,
        on_missing_link: ActionPolicy = ActionPolicy.RAISE,
        **kwargs: Any,
    ) -> Turn | None:
        """Add a turn between two directed links."""
        kwargs["delta_t"] = self.delta_t
        kwargs["total_time"] = self.total_time

        if not self._handle_missing_link(in_link, "Incoming", on_missing_link):
            return None
        if not self._handle_missing_link(out_link, "Outgoing", on_missing_link):
            return None

        turns = self["turns"]
        if idx in turns:
            if on_existing == ActionPolicy.RAISE:
                raise ExistingTurnError(f"Turn with id {idx} already exists.")
            if on_existing == ActionPolicy.WARN:
                warnings.warn(f"Turn with id {idx} already exists.", stacklevel=2)
            if on_existing in {ActionPolicy.IGNORE, ActionPolicy.SKIP}:
                return turns[idx]

        turn = Turn(idx=idx, in_link=in_link, out_link=out_link, **kwargs)
        turns[idx] = turn
        return turn

    def _handle_missing_link(
        self,
        idx: Hashable,
        role: str,
        policy: ActionPolicy,
    ) -> bool:
        links = self["links"]
        if idx in links:
            return True
        if policy == ActionPolicy.RAISE:
            raise MissingLinkError(f"{role} link with id {idx} does not exist.")
        if policy == ActionPolicy.WARN:
            warnings.warn(f"{role} link with id {idx} does not exist.", stacklevel=3)
        elif policy == ActionPolicy.SKIP:
            return False
        return True

    def get_all_links(self) -> Generator[Link]:
        """Yield all links in insertion order."""
        yield from self["links"].values()

    def get_all_nodes(self) -> Generator[Node]:
        """Yield all nodes in insertion order."""
        yield from self["nodes"].values()

    def get_all_turns(self) -> Generator[Turn]:
        """Yield all turns in insertion order."""
        yield from self["turns"].values()

    def apply_links(self, fn: Callable[[Link], Any] | None = None) -> None:
        """Apply ``fn`` to every link."""
        if fn is None:
            msg = "fn must be callable"
            raise TypeError(msg)
        for link in self.get_all_links():
            fn(link)

    def apply_nodes(self, fn: Callable[[Node], Any] | None = None) -> None:
        """Apply ``fn`` to every node."""
        if fn is None:
            msg = "fn must be callable"
            raise TypeError(msg)
        for node in self.get_all_nodes():
            fn(node)

    def apply_turns(self, fn: Callable[[Turn], Any] | None = None) -> None:
        """Apply ``fn`` to every turn."""
        if fn is None:
            msg = "fn must be callable"
            raise TypeError(msg)
        for turn in self.get_all_turns():
            fn(turn)

    def resize_attributes(
        self,
        new_total_time: Numeric | None = None,
        new_delta_t: Numeric | None = None,
    ) -> None:
        """Resize the graph time horizon metadata."""
        total_time = self.total_time if new_total_time is None else new_total_time
        delta_t = self.delta_t if new_delta_t is None else new_delta_t

        self["total_time"] = total_time
        self["delta_t"] = delta_t
        self["num_intervals"] = int(total_time // delta_t)

        for element in (*self.get_all_links(), *self.get_all_turns()):
            element["total_time"] = total_time
            element["delta_t"] = delta_t

    def get_link(self, idx: Hashable) -> Link | None:
        """Return a link by identifier, or ``None`` when missing."""
        return self["links"].get(idx)

    def get_node(self, idx: Hashable) -> Node | None:
        """Return a node by identifier, or ``None`` when missing."""
        return self["nodes"].get(idx)

    def get_turn(self, idx: Hashable) -> Turn | None:
        """Return a turn by identifier, or ``None`` when missing."""
        return self["turns"].get(idx)

    def remove_link(self, idx: Hashable, cascade: bool = False) -> None:
        """Remove a link by identifier."""
        if cascade:
            turns_to_remove = [
                turn.idx
                for turn in self.get_all_turns()
                if turn.in_link == idx or turn.out_link == idx
            ]
            self.remove_turns(turns_to_remove)
        self["links"].pop(idx, None)

    def remove_links(self, idx: Iterable[Hashable], cascade: bool = False) -> None:
        """Remove multiple links by identifier."""
        link_ids = set(idx)
        if cascade:
            turns_to_remove = [
                turn.idx
                for turn in self.get_all_turns()
                if turn.in_link in link_ids or turn.out_link in link_ids
            ]
            self.remove_turns(turns_to_remove)
        for link_idx in link_ids:
            self["links"].pop(link_idx, None)

    def remove_node(self, idx: Hashable, cascade: bool = False) -> None:
        """Remove a node by identifier."""
        if cascade:
            links_to_remove = [
                link.idx for link in self.get_all_links() if link.i == idx or link.j == idx
            ]
            self.remove_links(links_to_remove, cascade=True)
        self["nodes"].pop(idx, None)

    def remove_nodes(self, idx: Iterable[Hashable], cascade: bool = False) -> None:
        """Remove multiple nodes by identifier."""
        node_ids = set(idx)
        if cascade:
            links_to_remove = [
                link.idx
                for link in self.get_all_links()
                if link.i in node_ids or link.j in node_ids
            ]
            self.remove_links(links_to_remove, cascade=True)

        for node_idx in node_ids:
            self["nodes"].pop(node_idx, None)

    def remove_turn(self, idx: Hashable) -> None:
        """Remove a turn by identifier."""
        self["turns"].pop(idx, None)

    def remove_turns(self, idx: Iterable[Hashable]) -> None:
        """Remove multiple turns by identifier."""
        for turn_idx in set(idx):
            self["turns"].pop(turn_idx, None)

    def get_node_neighbors(
        self,
        idx: Hashable,
        include_in_links: bool = True,
        include_out_links: bool = True,
    ) -> list[Link]:
        """Return links connected to ``idx`` using incoming/outgoing switches."""
        return [
            link
            for link in self.get_all_links()
            if (include_in_links and link.j == idx) or (include_out_links and link.i == idx)
        ]

    def get_nodes_neighbors(
        self,
        include_in_links: bool = True,
        include_out_links: bool = True,
    ) -> dict[Hashable, list[Link]]:
        """Return connected links for every node."""
        return {
            node.idx: self.get_node_neighbors(
                node.idx,
                include_in_links=include_in_links,
                include_out_links=include_out_links,
            )
            for node in self.get_all_nodes()
        }

    def get_node_degree(
        self,
        idx: Hashable,
        include_in_links: bool = True,
        include_out_links: bool = True,
    ) -> int:
        """Return the number of connected links for a node."""
        return len(
            self.get_node_neighbors(
                idx,
                include_in_links=include_in_links,
                include_out_links=include_out_links,
            )
        )

    def remove_isolated_nodes(self) -> None:
        """Remove nodes with no connected links."""
        neighbors = self.get_nodes_neighbors(include_in_links=True, include_out_links=True)
        isolated_nodes = [
            node.idx for node in self.get_all_nodes() if len(neighbors[node.idx]) == 0
        ]
        self.remove_nodes(isolated_nodes, cascade=False)

    def remove_links_without_nodes(self, cascade: bool = False) -> None:
        """Remove links whose start or end node is missing."""
        all_node_ids = {node.idx for node in self.get_all_nodes()}
        links_to_remove = [
            link.idx
            for link in self.get_all_links()
            if link.i not in all_node_ids or link.j not in all_node_ids
        ]
        self.remove_links(links_to_remove, cascade=cascade)

    def remove_turns_without_links(self) -> None:
        """Remove turns whose incoming or outgoing link is missing."""
        all_link_ids = {link.idx for link in self.get_all_links()}
        turns_to_remove = [
            turn.idx
            for turn in self.get_all_turns()
            if turn.in_link not in all_link_ids or turn.out_link not in all_link_ids
        ]
        self.remove_turns(turns_to_remove)

    def remove_redundants(self) -> None:
        """Remove links without nodes, isolated nodes, and turns without links."""
        self.remove_links_without_nodes()
        self.remove_isolated_nodes()
        self.remove_turns_without_links()

    def nodes_by_filter(self, filter_func: Callable[[Node], bool]) -> Generator[Node, None, None]:
        """Yield nodes that satisfy ``filter_func``."""
        for node in self.get_all_nodes():
            if filter_func(node):
                yield node

    def remove_nodes_by_filter(
        self,
        filter_func: Callable[[Node], bool],
        cascade: bool = False,
    ) -> None:
        """Remove nodes that satisfy ``filter_func``."""
        self.remove_nodes((node.idx for node in self.nodes_by_filter(filter_func)), cascade=cascade)

    def links_by_filter(self, filter_func: Callable[[Link], bool]) -> Generator[Link, None, None]:
        """Yield links that satisfy ``filter_func``."""
        for link in self.get_all_links():
            if filter_func(link):
                yield link

    def remove_links_by_filter(
        self,
        filter_func: Callable[[Link], bool],
        cascade: bool = False,
    ) -> None:
        """Remove links that satisfy ``filter_func``."""
        self.remove_links((link.idx for link in self.links_by_filter(filter_func)), cascade=cascade)

    def turns_by_filter(self, filter_func: Callable[[Turn], bool]) -> Generator[Turn, None, None]:
        """Yield turns that satisfy ``filter_func``."""
        for turn in self.get_all_turns():
            if filter_func(turn):
                yield turn

    def remove_turns_by_filter(
        self,
        filter_func: Callable[[Turn], bool],
        cascade: bool = False,
    ) -> None:
        """Remove turns that satisfy ``filter_func``.

        The ``cascade`` parameter is accepted for API symmetry and currently has
        no effect because turns have no dependent entities.
        """
        del cascade
        self.remove_turns(turn.idx for turn in self.turns_by_filter(filter_func))


__all__ = ["Graph"]
