from hotaru.hotaru import State


def test_init_board() -> None:
    assert State().board == [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]


def test_end_board() -> None:
    state = State()
    state.board = [[45, 44, 47, 46], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = 0
    assert state.is_end()
    state.turn = 2
    assert not state.is_end()


def test_board_0() -> None:
    state = State()
    state.dice = 1
    assert state.is_start() is True
    assert (
        state.visualize(colored=False)
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
        + "\n"
        + "Turn: R, Dice: 1"
    )
    assert state.eval() == {None: 0}


def test_board_1() -> None:
    state = State()
    state.board = [[46, 1, 8, 10], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.dice, state.turn = 2, 0
    assert state.get_movables() == [4]
    state.move(4)
    assert state.board == [
        [46, 1, 8, 12],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    state.dice = 5
    assert state.is_start() is True
    assert (
        state.visualize(colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G1][G2]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[R4][  ][  ][  ][R3][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][R1][  ]                \n"
        + "    [  ][R2]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [  ][  ][  ]                \n"
        + "\n"
        + "Turn: G, Dice: 5"
    )
    assert state.eval() == {None: 0}


def test_board_2() -> None:
    state = State()
    state.board = [[10, 4, 2, 43], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.dice, state.turn = 6, 0
    assert state.get_movables() == [1]
    state.move(1)
    assert state.board == [
        [16, 4, 2, 43],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    state.dice = 5
    assert state.is_start() is False
    assert (
        state.visualize(colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G1][G2]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][R1][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [R3][  ]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [R2][R4][  ]                \n"
        + "\n"
        + "Turn: R, Dice: 5"
    )
    assert state.eval() == {1: 0, 2: 0}


def test_board_3() -> None:
    state = State()
    state.board = [[0, 7, 46, 15], [0, 34, 2, 3], [0, 1, 2, 3], [0, 1, 2, 19]]
    state.dice, state.turn = 2, 0
    assert state.get_movables() == [2, 4]
    state.move(2)
    assert state.board == [
        [0, 9, 46, 15],
        [0, 34, 2, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    state.dice = 5
    assert state.is_start() is False
    assert (
        state.visualize(colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G1][  ]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][R4][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][R2][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][R3][  ]                \n"
        + "    [R1][  ]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [G2][  ][  ]                \n"
        + "\n"
        + "Turn: G, Dice: 5"
    )
    assert state.eval() == {2: 0}


def test_board_4() -> None:
    state = State()
    state.board = [[13, 43, 2, 3], [0, 1, 34, 3], [0, 1, 2, 3], [0, 29, 2, 3]]
    state.dice, state.turn = 6, 0
    assert state.get_movables() == [1, 3, 4]
    state.move(3)
    assert state.board == [
        [13, 43, 4, 3],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
        [0, 29, 2, 3],
    ]
    state.dice = 3
    assert state.is_start() is False
    assert (
        state.visualize(colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G1][G2]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][G4]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [Y2][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[R1][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y1][  ]    \n"
        + "    [  ][R4]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [R3][R2][  ]                \n"
        + "\n"
        + "Turn: R, Dice: 3"
    )
    assert state.eval() == {1: 0, 2: 0, 3: 0}


def test_board_5() -> None:
    state = State()
    state.board = [[0, 29, 2, 3], [13, 43, 2, 3], [0, 1, 34, 3], [0, 1, 2, 3]]
    state.dice, state.turn = 6, 1
    assert state.get_movables() == [1, 3, 4]
    state.move(4)
    assert state.board == [
        [0, 29, 2, 3],
        [13, 43, 2, 4],
        [0, 1, 2, 3],
        [0, 1, 2, 3],
    ]
    state.dice = 4
    assert state.is_start() is False
    assert (
        state.visualize(colored=False)
        == "                [  ][G1][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [B1][B2]    \n"
        + "    [G3][  ]    [  ][  ][  ]    [B3][B4]    \n"
        + "                [  ][  ][  ]                \n"
        + "[G4][  ][  ][  ][  ][  ][  ][R2][  ][  ][  ]\n"
        + "[G2][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [R1][  ]    [  ][  ][  ]    [Y1][Y2]    \n"
        + "    [R3][R4]    [  ][  ][  ]    [Y3][Y4]    \n"
        + "                [  ][  ][  ]                \n"
        + "\n"
        + "Turn: G, Dice: 4"
    )
    assert state.eval() == {1: 0, 2: 0, 4: 0}
