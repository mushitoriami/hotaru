from __future__ import annotations

import mmap
from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--midgame-params-path",
        action="store",
        default=None,
        help="path to params_midgame.dat for tests that require it"
        " (such tests are skipped if omitted)",
    )
    parser.addoption(
        "--endgame-params-path",
        action="store",
        default=None,
        help="path to params_endgame.dat for tests that require it"
        " (such tests are skipped if omitted)",
    )


@pytest.fixture
def midgame_params_path(request: pytest.FixtureRequest) -> Path:
    path = request.config.getoption("--midgame-params-path")
    if path is None:
        pytest.skip("--midgame-params-path not given")
    return Path(path)


@pytest.fixture
def endgame_params_path(request: pytest.FixtureRequest) -> Path:
    path = request.config.getoption("--endgame-params-path")
    if path is None:
        pytest.skip("--endgame-params-path not given")
    return Path(path)


@pytest.fixture
def midgame_params(midgame_params_path: Path) -> bytes:
    with open(midgame_params_path, "rb") as f:
        return f.read()


@pytest.fixture
def endgame_params(endgame_params_path: Path) -> mmap.mmap:
    with open(endgame_params_path, "rb") as f:
        return mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
