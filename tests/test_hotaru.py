from hotaru.hotaru import add, init_board, get_movables_board, move_board


def test_init_board() -> None:
    assert init_board() == [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]


def test_board_1() -> None:
    board = [46, 0, 0, 0, 1, 1, 1, 1, 8, 2, 2, 2, 10, 3, 3, 3]
    dice, turn = 2, 0
    assert get_movables_board(board, turn, dice) == [3]
    assert move_board(board, 3, turn, dice) == [
        46,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        11,
        2,
        2,
        2,
        10,
        3,
        3,
        3,
    ]


def test_board_2() -> None:
    board = [10, 0, 0, 0, 4, 1, 1, 1, 2, 2, 2, 2, 43, 3, 3, 3]
    dice, turn = 6, 0
    assert get_movables_board(board, turn, dice) == [0]
    assert move_board(board, 0, turn, dice) == [
        16,
        0,
        0,
        0,
        4,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        43,
        3,
        3,
        3,
    ]


def test_board_3() -> None:
    board = [0, 0, 0, 0, 7, 34, 1, 1, 46, 2, 2, 2, 15, 3, 3, 19]
    dice, turn = 2, 0
    assert get_movables_board(board, turn, dice) == [1, 3]
    assert move_board(board, 1, turn, dice) == [
        0,
        0,
        0,
        0,
        9,
        34,
        1,
        1,
        46,
        2,
        2,
        2,
        15,
        3,
        3,
        3,
    ]
    assert move_board(board, 3, turn, dice) == [
        0,
        0,
        0,
        0,
        7,
        34,
        1,
        1,
        46,
        2,
        2,
        2,
        17,
        3,
        3,
        19,
    ]


def test_board_4() -> None:
    board = [13, 0, 0, 0, 43, 1, 1, 29, 2, 24, 2, 2, 3, 3, 3, 3]
    dice, turn = 6, 0
    assert get_movables_board(board, turn, dice) == [0, 2, 3]
    assert move_board(board, 0, turn, dice) == [
        19,
        0,
        0,
        0,
        43,
        1,
        1,
        2,
        2,
        24,
        2,
        2,
        3,
        3,
        3,
        3,
    ]
    assert move_board(board, 2, turn, dice) == [
        13,
        0,
        0,
        0,
        43,
        1,
        1,
        29,
        4,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
    ]
    assert move_board(board, 3, turn, dice) == [
        13,
        0,
        0,
        0,
        43,
        1,
        1,
        29,
        2,
        2,
        2,
        2,
        4,
        3,
        3,
        3,
    ]


def test_add() -> None:
    assert add(2, 2) == 4
