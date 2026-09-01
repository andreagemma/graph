from __future__ import annotations

from graph import KPathList, Path, PathList


def test_path_list_adds_filters_and_counts_paths() -> None:
    paths = PathList()
    path = Path("A", "C", 0, links=["ab", "ab", "bc"], costs=[1, 2, 3], mode="car")
    paths.add_path(path)

    assert paths.path("A", "C", 0, "car") is path
    assert paths.n_paths() == 1
    assert paths.counts_tot_links() == 3
    assert paths.counts_link("ab") == 2
    assert paths.get_sources(target="C") == ("A",)
    assert paths.get_targets(source="A") == ("C",)
    assert paths.get_t_starts(source="A", target="C") == (0,)
    assert paths.get_modes(source="A", target="C") == ("car",)


def test_k_path_list_assigns_and_retrieves_k_paths() -> None:
    first = Path("A", "C", 0, links=["ab", "bc"], costs=[1, 2], mode="car")
    second = Path("A", "C", 0, links=["ac"], costs=[5], mode="car")
    paths = KPathList()

    paths.add_path(first)
    paths.add_path(second)

    assert first["k"] == 0
    assert second["k"] == 1
    assert list(paths.paths("A", "C", 0, "car")) == [first, second]
    assert paths.path("A", "C", 0, "car", k=1) is second
    assert paths.n_paths() == 2
    assert paths.k_paths() == 2


def test_k_path_merge_can_preserve_existing_k() -> None:
    path = Path("A", "C", 0, links=["ac"], costs=[5], mode="car")
    path["k"] = 2
    paths = KPathList()

    paths.merge(path, override_k=True)

    assert paths.path("A", "C", 0, "car", k=2) is path
    assert list(paths.paths("A", "C", 0, "car")) == [path]
    assert paths.n_paths() == 1
    assert paths.k_paths() == 3
