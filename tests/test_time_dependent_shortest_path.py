from __future__ import annotations

from graph import Graph, TimeDependentLinkBasedShortestPath


def make_routing_graph() -> Graph:
    graph = Graph(total_time=60, delta_t=15)
    for node in ("A", "B", "C"):
        graph.add_node(node, cost=0)
    graph.add_link("ab", "A", "B", cost=1, modes={"car"})
    graph.add_link("bc", "B", "C", cost=1, modes={"car"})
    graph.add_link("ac", "A", "C", cost=10, modes={"car", "bike"})
    return graph


def test_shortest_paths_accepts_single_string_target() -> None:
    graph = make_routing_graph()
    router = TimeDependentLinkBasedShortestPath.from_graph(graph, link_cost_field="cost")

    paths = router.shortest_paths("A", "C")
    path = paths.path("A", "C", 0, None)  # type: ignore

    assert path is not None
    assert path.get_links() == ("ab", "bc")  # type: ignore
    assert path.get_costs() == (1, 2)  # type: ignore
    assert path["tot_cost"] == 2


def test_turn_costs_affect_route_choice() -> None:
    graph = make_routing_graph()
    graph.add_turn("ab_bc", "ab", "bc", cost=20)
    router = TimeDependentLinkBasedShortestPath.from_graph(
        graph,
        link_cost_field="cost",
        turn_cost_field="cost",
    )

    path = router.shortest_paths("A", "C").path("A", "C", 0, None)  # type: ignore

    assert path is not None
    assert path.get_links() == ("ac",)  # type: ignore
    assert path["tot_cost"] == 10


def test_prohibited_turns_are_removed_from_link_successors() -> None:
    graph = make_routing_graph()
    graph.add_turn("ab_bc", "ab", "bc", prohibited=True)
    router = TimeDependentLinkBasedShortestPath.from_graph(
        graph,
        link_cost_field="cost",
        turn_prohibited_field="prohibited",
    )

    path = router.shortest_paths("A", "C").path("A", "C", 0, None)  # type: ignore

    assert path is not None
    assert path.get_links() == ("ac",)  # type: ignore


def test_mode_filter_uses_the_configured_mode_field() -> None:
    graph = make_routing_graph()
    graph.get_link("ac")["modes"] = {"bike"}  # type: ignore
    router = TimeDependentLinkBasedShortestPath.from_graph(
        graph,
        mode="car",
        link_mode_field="modes",
        link_cost_field="cost",
    )

    path = router.shortest_paths("A", "C").path("A", "C", 0, "car")  # type: ignore

    assert path is not None
    assert path.get_links() == ("ab", "bc")  # type: ignore
