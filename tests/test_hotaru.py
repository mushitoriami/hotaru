from hotaru.hotaru import (
    Board,
    get_movables_board,
    move_board,
    is_end_board,
    visualize_board,
)


def test_init_board() -> None:
    assert Board().board == [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]


def test_end_board() -> None:
    board = Board()
    board.board = [[45, 44, 47, 46], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    assert is_end_board(board, 0)
    assert not is_end_board(board, 2)


def test_board_0() -> None:
    board = Board()
    assert (
        visualize_board(board)
        == "                [  ][  ][  ]                \n"
        + "    [G1][G2]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [R1][R2]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [R3][R4]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [  ][  ][  ]                \n"
    )


def test_board_1() -> None:
    board = Board()
    board.board = [[46, 1, 8, 10], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    dice, turn = 2, 0
    assert get_movables_board(board, turn, dice) == [3]
    assert move_board(board, 3, turn, dice).board == [
        [46, 1, 8, 12],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert (
        visualize_board(board)
        == "                [  ][  ][  ]                \n"
        + "    [G1][G2]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][R4][  ][R3][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][R1][  ]                \n"
        + "    [  ][R2]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [  ][  ][  ]                \n"
    )


def test_board_2() -> None:
    board = Board()
    board.board = [[10, 4, 2, 43], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    dice, turn = 6, 0
    assert get_movables_board(board, turn, dice) == [0]
    assert move_board(board, 0, turn, dice).board == [
        [16, 4, 2, 43],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert (
        visualize_board(board)
        == "                [  ][  ][  ]                \n"
        + "    [G1][G2]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][R1][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [R3][  ]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [R2][R4][  ]                \n"
    )


def test_board_3() -> None:
    board = Board()
    board.board = [[0, 7, 46, 15], [0, 34, 2, 3], [0, 1, 2, 3], [0, 1, 2, 19]]
    dice, turn = 2, 0
    assert get_movables_board(board, turn, dice) == [1, 3]
    assert move_board(board, 1, turn, dice).board == [
        [0, 9, 46, 15],
        [0, 34, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert move_board(board, 3, turn, dice).board == [
        [0, 7, 46, 17],
        [0, 34, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 19],
    ]
    assert (
        visualize_board(board)
        == "                [  ][  ][  ]                \n"
        + "    [G1][  ]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][R4][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][Y4][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [R2][R3][  ]                \n"
        + "    [R1][  ]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y3][  ]    \n"
        + "                [G2][  ][  ]                \n"
    )


def test_board_4() -> None:
    board = Board()
    board.board = [[13, 43, 2, 3], [0, 1, 34, 3], [0, 1, 2, 3], [0, 29, 2, 3]]
    dice, turn = 6, 0
    assert get_movables_board(board, turn, dice) == [0, 2, 3]
    assert move_board(board, 0, turn, dice).board == [
        [19, 43, 2, 3],
        [0, 1, 34, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert move_board(board, 2, turn, dice).board == [
        [13, 43, 4, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 29, 2, 3],
    ]
    assert move_board(board, 3, turn, dice).board == [
        [13, 43, 2, 4],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 29, 2, 3],
    ]
    assert (
        visualize_board(board)
        == "                [  ][  ][  ]                \n"
        + "    [G1][G2]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [  ][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [Y2][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[R1][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y1][  ]    \n"
        + "    [R3][R4]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [G3][R2][  ]                \n"
    )


def test_board_5() -> None:
    board = Board()
    board.board = [[0, 29, 2, 3], [13, 43, 2, 3], [0, 1, 34, 3], [0, 1, 2, 3]]
    dice, turn = 6, 1
    assert get_movables_board(board, turn, dice) == [0, 2, 3]
    assert move_board(board, 0, turn, dice).board == [
        [0, 1, 2, 3],
        [19, 43, 2, 3],
        [0, 1, 34, 3],
        [0, 1, 2, 3],
    ]
    assert move_board(board, 2, turn, dice).board == [
        [0, 29, 2, 3],
        [13, 43, 4, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert move_board(board, 3, turn, dice).board == [
        [0, 29, 2, 3],
        [13, 43, 2, 4],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    assert (
        visualize_board(board)
        == "                [  ][G1][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [  ][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[B3][  ][  ][  ][  ][  ][  ][R2][  ][  ][  ]\n"
        + "[G2][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [R1][  ]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [R3][R4]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [  ][  ][  ]                \n"
    )
