from __future__ import annotations

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
