# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

- Bumped package/build version from `0.1.4` to `0.1.5`.

## 0.1.4 - 2026-09-23

- Added link lookup by node pair with `get_link_by_nodes(i, j)` and `has_link_by_nodes(i, j)`.
- Added graph time helpers `get_intervals()` and `create_array_attribute(...)`.
- Extended `resize_attributes(...)` to resize/interpolate time-series attributes on nodes, links, and turns.
- Kept internal `(i, j)` link index consistent during link replacement and removal.
- Added test coverage for node-pair link lookup and time-series resize helpers.
- Added explicit `numpy` runtime dependency required by time-series operations.

## 0.1.3 - 2026-09-08

- Aligned GitHub Actions workflows with the configreader flow and analogous file names:
	- `all.yml`
	- `ci.yml`
	- `fast_ci.yml`
	- `quality.yml`
	- `create-release.yml`
	- `create-release-whl.yml`
	- `release.yml`
- Bumped package/build version from `0.1.2` to `0.1.3`.

## 0.1.0 - 2026-09-01

- Prepared the package for GitHub and PyPI publication as `ga-graph`.
- Added README, documentation, changelog, MIT license, gitignore, manifest, and typed package marker.
- Corrected packaging metadata, project URLs, coverage source, and GitHub Actions imports.
- Added a focused `pytest` suite for graph operations, path containers, turn helpers, routing, and version exports.
- Fixed graph neighbor filtering, cascade removals, redundant cleanup, filtered removals, k-path lookup, and time-dependent routing turn handling.
