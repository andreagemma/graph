# Third-Party Notices

GA Graph uses the dependencies listed below. License texts are archived in
[`licenses/third_party/packages`](licenses/third_party/packages/); the complete
machine-readable inventory is
[`licenses/third_party/summary.tsv`](licenses/third_party/summary.tsv).

| Package | Archived version | License | Source |
|---|---:|---|---|
| ga-serializer | 0.1.3 | MIT | [andreagemma/serializer](https://github.com/andreagemma/serializer) |
| dill | 0.4.1 | BSD 3-Clause | [PyPI](https://pypi.org/project/dill/) |
| NumPy | 2.5.4 | BSD 3-Clause | [numpy/numpy](https://github.com/numpy/numpy) |
| Shapely | 2.2.0 | BSD 3-Clause | [shapely/shapely](https://github.com/shapely/shapely) |
| pytest | 9.1.1 | MIT | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| pytest-cov | 7.1.0 | MIT | [pytest-dev/pytest-cov](https://github.com/pytest-dev/pytest-cov) |
| build | 1.6.1 | MIT | [pypa/build](https://github.com/pypa/build) |
| mypy | 2.4.0 | MIT | [python/mypy](https://github.com/python/mypy) |
| Ruff | 0.17.0 | MIT | [astral-sh/ruff](https://github.com/astral-sh/ruff) |
| twine | 7.0.0 | Apache-2.0 | [pypa/twine](https://github.com/pypa/twine) |

These are the versions installed in the development environment when the
inventory was generated; project requirements may allow other versions.

Shapely's binary distribution also bundles GEOS under LGPL-2.1; its license is
archived as `licenses/third_party/packages/shapely/LICENSE_GEOS`. On Windows,
the Shapely distribution may bundle Microsoft Visual C++ runtime files; the
associated notice is archived as `licenses/third_party/packages/shapely/LICENSE_win32`.
