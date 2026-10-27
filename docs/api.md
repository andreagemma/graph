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
- `get_link_by_nodes(i, j)`, `has_link_by_nodes(i, j)`
- `get_turn_by_links(in_link, out_link)`, `get_turn_by_links_or_error(...)`
- `get_all_nodes()`, `get_all_links()`, `get_all_turns()`
- `get_sample_node(...)`, `get_sample_link(...)`, `get_sample_turn(...)`
- `remove_node(idx, cascade=False)`, `remove_link(idx, cascade=False)`
- `remove_redundants()`
- `merge(other, copy=False, inplace=True)`
- `cut_time_slice(time_start=None, time_end=None, rebase=None, inplace=True)`
- `time_index(time_value)`
- `resize_attributes(new_total_time=None, new_delta_t=None)`
- `get_intervals()`
- `create_array_attribute(value, value_total_time=None, value_delta_t=None)`

Sampling helpers accept an optional predicate and can either return the first
match or choose a reproducible random match with `random=True` and a
`random_state`. Turn lookups are indexed by `(in_link, out_link)` and remain
consistent as turns are replaced or removed.

`merge` appends a compatible time horizon, and `cut_time_slice` selects a
portion of one. Graph time origins and durations may be integers or floats.

## `Path`, `PathList`, and `KPathList`

```python
Path(source, target, t_start, links=None, costs=None, tot_cost=0.0, mode=None)
PathList()
KPathList()
```

`Path` stores the labels and cumulative costs for a route. `PathList` keeps one
path per `(source, target, t_start, mode)` key. `KPathList` keeps multiple
k-ranked paths for the same key.

`KPathContainer.from_pandas(...)` creates a container from a pandas dataframe.
`PathContainer.to_pandas(...)` returns a pandas dataframe or, when link
geometries are available, a GeoPandas `GeoDataFrame`.

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
movements. Geometries must expose a `.coords` sequence. Graph path geometry
helpers accept Shapely `LineString` and `MultiLineString` geometries.

## `TimeDependentLinkBasedShortestPath`

```python
TimeDependentLinkBasedShortestPath.from_graph(graph, ...)
router.shortest_paths(source, targets=None, t_start=0)
```

Builds a dense link-based routing view from `Graph`. It supports scalar or
sequence cost fields on nodes, links, and turns, mode filters, and prohibited
turn fields.
