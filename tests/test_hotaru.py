from hotaru.hotaru import State, get_absolute_pos, is_same_pos


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


def test_get_absolute_pos() -> None:
    # turn=0: (pos - 4) % 40
    assert get_absolute_pos(4, 0) == 0
    assert get_absolute_pos(14, 0) == 10
    assert get_absolute_pos(43, 0) == 39

    # turn=1: (pos - 4 + 10) % 40
    assert get_absolute_pos(4, 1) == 10
    assert get_absolute_pos(14, 1) == 20
    assert get_absolute_pos(43, 1) == 9

    # turn=2: (pos - 4 + 20) % 40
    assert get_absolute_pos(4, 2) == 20
    assert get_absolute_pos(14, 2) == 30
    assert get_absolute_pos(43, 2) == 19

    # turn=3: (pos - 4 + 30) % 40
    assert get_absolute_pos(4, 3) == 30
    assert get_absolute_pos(14, 3) == 0
    assert get_absolute_pos(43, 3) == 29


def test_is_same_pos() -> None:
    # Same absolute position with different turns
    # pos=4, turn=0 has absolute 0; pos=14, turn=3 has absolute (14-4+30)%40=0
    assert is_same_pos(4, 0, 14, 3) is True
    assert is_same_pos(14, 3, 4, 0) is True

    # pos=14, turn=0 has absolute 10; pos=4, turn=1 has absolute 10
    assert is_same_pos(14, 0, 4, 1) is True
    assert is_same_pos(4, 1, 14, 0) is True

    # Same position and turn
    assert is_same_pos(10, 0, 10, 0) is True
    assert is_same_pos(20, 2, 20, 2) is True

    # Different absolute positions
    assert is_same_pos(4, 0, 5, 0) is False
    assert is_same_pos(10, 1, 20, 2) is False

    # Out of range positions (pos < 4 or pos > 43)
    assert is_same_pos(3, 0, 10, 0) is False
    assert is_same_pos(10, 0, 3, 0) is False
    assert is_same_pos(44, 0, 10, 0) is False
    assert is_same_pos(10, 0, 44, 0) is False
    assert is_same_pos(0, 0, 50, 0) is False


def test_visualize_colored() -> None:
    """Test that colored output contains ANSI escape codes."""
    state = State()
    state.dice = 1

    # ANSI color codes
    red_bg = "\033[97;41m"
    green_bg = "\033[97;42m"
    blue_bg = "\033[97;44m"
    yellow_bg = "\033[30;43m"
    reset = "\033[0m"

    colored_output = state.visualize(colored=True)

    # Check that colored pieces have ANSI codes (only color letter, not number)
    assert f"[{red_bg}R{reset}1]" in colored_output
    assert f"[{green_bg}G{reset}1]" in colored_output
    assert f"[{blue_bg}B{reset}1]" in colored_output
    assert f"[{yellow_bg}Y{reset}1]" in colored_output

    # Check that Turn label is colored
    assert f"Turn: {red_bg}R{reset}, Dice: 1" in colored_output


def test_visualize_colored_winner() -> None:
    """Test that winner output is colored."""
    state = State()
    state.board = [[44, 45, 46, 47], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = None
    state.winner = 0

    red_bg = "\033[97;41m"
    reset = "\033[0m"

    colored_output = state.visualize(colored=True)
    assert f"Winner: {red_bg}R{reset}" in colored_output


def test_three_sixes_rule() -> None:
    """After rolling three consecutive 6s and moving, turn should advance."""
    state = State()
    # Set up board so Red has pieces that can move
    state.board = [[4, 5, 6, 7], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = 0
    state.count_six = 0

    # First 6: move piece, count_six becomes 1, turn stays with Red
    state.dice = 6
    state.move(1)  # Move piece 1
    assert state.count_six == 1
    assert state.turn == 0  # Still Red's turn

    # Second 6: move piece, count_six becomes 2, turn stays with Red
    state.dice = 6
    state.move(1)
    assert state.count_six == 2
    assert state.turn == 0  # Still Red's turn

    # Third 6: move piece, count_six wraps to 0, turn advances to Green
    state.dice = 6
    state.move(1)
    assert state.count_six == 0
    assert state.turn == 1  # Now Green's turn


def test_three_sixes_rule_reset_on_non_six() -> None:
    """Rolling a non-6 should reset count_six to 0."""
    state = State()
    state.board = [[4, 5, 6, 7], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = 0
    state.count_six = 0

    # Roll a 6, count_six becomes 1
    state.dice = 6
    state.move(1)
    assert state.count_six == 1
    assert state.turn == 0

    # Roll another 6, count_six becomes 2
    state.dice = 6
    state.move(1)
    assert state.count_six == 2
    assert state.turn == 0

    # Roll a non-6, count_six resets to 0, turn advances
    state.dice = 3
    state.move(1)
    assert state.count_six == 0
    assert state.turn == 1  # Turn advances to Green


def test_three_starts_rule() -> None:
    """After being stuck at start three times, turn should advance."""
    state = State()
    # All players at start
    state.board = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = 0
    state.count_start = 0

    # First start: pass, count_start becomes 1, turn stays
    state.dice = 3  # Can't move without a 6
    assert state.get_movables() == [None]
    state.move(None)
    assert state.count_start == 1
    assert state.turn == 0  # Still Red's turn

    # Second start: pass, count_start becomes 2, turn stays
    state.dice = 2
    state.move(None)
    assert state.count_start == 2
    assert state.turn == 0  # Still Red's turn

    # Third start: pass, count_start wraps to 0, turn advances
    state.dice = 4
    state.move(None)
    assert state.count_start == 0
    assert state.turn == 1  # Now Green's turn


def test_three_starts_rule_reset_on_leaving_start() -> None:
    """Moving a piece out of start should reset count_start to 0."""
    state = State()
    state.board = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = 0
    state.count_start = 0

    # First start: pass, count_start becomes 1
    state.dice = 3
    state.move(None)
    assert state.count_start == 1
    assert state.turn == 0

    # Second start: pass, count_start becomes 2
    state.dice = 2
    state.move(None)
    assert state.count_start == 2
    assert state.turn == 0

    # Roll a 6 and move out of start - is_start becomes False, count_start resets
    state.dice = 6
    state.move(1)  # Move piece 1 out of start
    assert state.board[0][0] == 4  # Piece moved to position 4
    assert state.is_start() is False
    assert state.count_start == 0
    # count_six is 1 (rolled a 6), so turn stays
    assert state.count_six == 1
    assert state.turn == 0


def test_three_starts_with_six_interaction() -> None:
    """Test interaction between count_start and count_six when rolling 6 at start."""
    state = State()
    state.board = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = 0
    state.count_start = 2  # Simulate having been stuck at start twice
    state.count_six = 0

    # Roll a 6 at start and move piece out
    state.dice = 6
    state.move(1)
    # After move: not at start anymore, rolled a 6
    assert state.is_start() is False
    assert state.count_start == 0  # Reset because no longer at start
    assert state.count_six == 1  # Incremented because rolled 6
    assert state.turn == 0  # Still Red's turn (count_six > 0)

    # Second 6: move piece 1 again (only movable piece since others can't exit to pos 4)
    state.dice = 6
    state.move(1)
    assert state.count_six == 2
    assert state.turn == 0

    # Third 6 - count_six wraps to 0, turn advances
    state.dice = 6
    state.move(1)
    assert state.count_six == 0
    assert state.turn == 1  # Green's turn


def test_count_six_reset_on_pass() -> None:
    state = State()
    state.board = [[43, 45, 46, 47], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
    state.turn = 0
    state.count_six = 1

    state.dice = 6
    state.get_movables() == [None]
    state.move(None)

    assert state.count_six == 0
    assert state.turn == 1
