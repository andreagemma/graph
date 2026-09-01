# API Reference

## `Graph`

```python
Graph(t0=0, total_time=60, delta_t=15, **kwargs)
```

Stores nodes, directed links, and turns. Nodes, links, and turns are dictionary
subclasses, so custom attributes can be attached directly.

Main methods:

- `add_node(idx, on_existing=ActionPolicy.RAISE, **kwargs)`
- `add_link(idx, i, j, on_existing=..., on_missing_node=..., **kwargs)`
- `add_turn(idx, in_link, out_link, on_existing=..., on_missing_link=..., **kwargs)`
- `get_node(idx)`, `get_link(idx)`, `get_turn(idx)`
- `get_all_nodes()`, `get_all_links()`, `get_all_turns()`
- `remove_node(idx, cascade=False)`, `remove_link(idx, cascade=False)`
- `remove_redundants()`
- `resize_attributes(new_total_time=None, new_delta_t=None)`

## `Path`, `PathList`, and `KPathList`

```python
Path(source, target, t_start, links=None, costs=None, tot_cost=0.0, mode=None)
PathList()
KPathList()
```

`Path` stores the labels and cumulative costs for a route. `PathList` keeps one
path per `(source, target, t_start, mode)` key. `KPathList` keeps multiple
k-ranked paths for the same key.

Main methods:

- `Path.key()`
- `Path.get_links()`
- `Path.get_costs()`
- `Path.has_link(id_link)`
- `Path.counts_link(id_link)`
- `PathList.add_path(path)`
- `PathList.path(source, target, t_start=0, mode=None)`
- `KPathList.add_path(path, k=None)`
- `KPathList.path(source, target, t_start=None, mode=None, k=0)`
- `KPathList.paths(source, target, t_start, mode=None)`

## `TurnType`

```python
TurnType.parse(value)
TurnType.classify_turn(in_edge_geometry, out_edge_geometry, angles=(30, 60, 120, 150))
```

Provides semantic labels for straight, left, right, sharp, and U-turn
movements. Geometries must expose a `.coords` sequence.

## `TimeDependentLinkBasedShortestPath`

```python
TimeDependentLinkBasedShortestPath.from_graph(graph, ...)
router.shortest_paths(source, targets=None, t_start=0)
```

Builds a dense link-based routing view from `Graph`. It supports scalar or
sequence cost fields on nodes, links, and turns, mode filters, and prohibited
turn fields.
