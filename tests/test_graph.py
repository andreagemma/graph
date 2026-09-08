from __future__ import annotations

import pytest

from graph import ActionPolicy, ExistingNodeError, Graph, MissingNodeError


def make_graph() -> Graph:
    graph = Graph(total_time=60, delta_t=15)
    for node in ("A", "B", "C"):
        graph.add_node(node)
    graph.add_link("ab", "A", "B")
    graph.add_link("bc", "B", "C")
    graph.add_link("ca", "C", "A")
    graph.add_turn("ab_bc", "ab", "bc")
    return graph


def link_ids(links) -> set[str]:  # type: ignore
    return {link.idx for link in links}  # type: ignore


def test_add_node_and_link_policies() -> None:
    graph = Graph()
    graph.add_node("A")

    with pytest.raises(ExistingNodeError):
        graph.add_node("A")

    assert graph.add_node("A", on_existing=ActionPolicy.IGNORE) is graph.get_node("A")

    with pytest.raises(MissingNodeError):
        graph.add_link("ab", "A", "B")

    link = graph.add_link("ab", "A", "B", on_missing_node=ActionPolicy.REPLACE)

    assert link is graph.get_link("ab")
    assert graph.get_node("B") is not None


def test_neighbors_honor_incoming_and_outgoing_switches() -> None:
    graph = make_graph()

    assert link_ids(graph.get_node_neighbors("A")) == {"ab", "ca"}
    assert link_ids(
        graph.get_node_neighbors("A", include_in_links=True, include_out_links=False)
    ) == {"ca"}
    assert link_ids(
        graph.get_node_neighbors("A", include_in_links=False, include_out_links=True)
    ) == {"ab"}
    assert graph.get_node_neighbors("A", include_in_links=False, include_out_links=False) == []


def test_cascade_remove_node_removes_dependent_links_and_turns() -> None:
    graph = make_graph()

    graph.remove_node("B", cascade=True)

    assert graph.get_node("B") is None
    assert graph.get_link("ab") is None
    assert graph.get_link("bc") is None
    assert graph.get_turn("ab_bc") is None
    assert graph.get_link("ca") is not None


def test_cleanup_removes_links_and_turns_with_missing_dependencies() -> None:
    graph = make_graph()
    graph.add_link("orphan", "missing", "A", on_missing_node=ActionPolicy.IGNORE)
    graph.add_turn("broken", "orphan", "missing-link", on_missing_link=ActionPolicy.IGNORE)

    graph.remove_redundants()

    assert graph.get_link("orphan") is None
    assert graph.get_turn("broken") is None


def test_filter_removals_use_entity_identifiers() -> None:
    graph = make_graph()
    graph.get_node("C")["drop"] = True  # type: ignore

    graph.remove_nodes_by_filter(lambda node: bool(node.get("drop")), cascade=True)

    assert graph.get_node("C") is None
    assert graph.get_link("bc") is None
    assert graph.get_link("ca") is None
    assert graph.get_turn("ab_bc") is None


def test_resize_updates_graph_and_link_turn_metadata() -> None:
    graph = make_graph()

    graph.resize_attributes(new_total_time=120, new_delta_t=30)

    assert graph.num_intervals == 4
    assert graph.get_link("ab")["delta_t"] == 30  # type: ignore
    assert graph.get_turn("ab_bc")["total_time"] == 120  # type: ignore
