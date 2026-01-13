from hotaru.hotaru import add, init_board


def test_init_board() -> None:
    assert init_board() == [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]


def test_add() -> None:
    assert add(2, 2) == 4
