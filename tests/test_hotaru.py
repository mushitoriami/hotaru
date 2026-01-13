from hotaru.hotaru import add, init_board, get_movables_board, move_board


def test_init_board() -> None:
    assert init_board() == [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]


def test_board_1() -> None:
    board = [[46, 1, 8, 10], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    dice, turn = 2, 0
    assert get_movables_board(board, turn, dice) == [3]
    assert move_board(board, 3, turn, dice) == [
        [46, 1, 8, 12],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]


def test_board_2() -> None:
    board = [[10, 4, 2, 43], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    dice, turn = 6, 0
    assert get_movables_board(board, turn, dice) == [0]
    assert move_board(board, 0, turn, dice) == [
        [16, 4, 2, 43],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]


def test_board_3() -> None:
    board = [[0, 7, 46, 15], [0, 34, 2, 3], [0, 1, 2, 3], [0, 1, 2, 19]]
    dice, turn = 2, 0
    assert get_movables_board(board, turn, dice) == [1, 3]
    assert move_board(board, 1, turn, dice) == [
        [0, 9, 46, 15],
        [0, 34, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert move_board(board, 3, turn, dice) == [
        [0, 7, 46, 17],
        [0, 34, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 19],
    ]


def test_board_4() -> None:
    board = [[13, 43, 2, 3], [0, 1, 34, 3], [0, 1, 2, 3], [0, 29, 2, 3]]
    dice, turn = 6, 0
    assert get_movables_board(board, turn, dice) == [0, 2, 3]
    assert move_board(board, 0, turn, dice) == [
        [19, 43, 2, 3],
        [0, 1, 34, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert move_board(board, 2, turn, dice) == [
        [13, 43, 4, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 29, 2, 3],
    ]
    assert move_board(board, 3, turn, dice) == [
        [13, 43, 2, 4],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 29, 2, 3],
    ]


def test_add() -> None:
    assert add(2, 2) == 4
