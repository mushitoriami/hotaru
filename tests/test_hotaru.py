import io
import mmap
from dataclasses import replace

import pytest
from shizuku import Agent, Cli

from hotaru import (
    HOTARU_GAME,
    State,
    apply_move,
    autoplay,
    cli,
    get_absolute_pos,
    get_movables,
    hotaru_evaluator,
    is_same_pos,
    is_start,
    new_state,
    random_evaluator,
    visualize,
)


def apply_move_one(state: State, piece: int | None) -> State:
    return next(iter(apply_move(state, piece)))


def test_init_board() -> None:
    assert new_state().board == ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))


def test_board_0() -> None:
    state = replace(new_state(), dice=1)
    assert is_start(state) is True
    assert (
        visualize(state, colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G3][G1]    [  ][  ][  ]    [B4][B3]    \n"
        + "    [G4][G2]    [  ][  ][  ]    [B2][B1]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [R1][R2]    [  ][  ][  ]    [Y2][Y4]    \n"
        + "    [R3][R4]    [  ][  ][  ]    [Y1][Y3]    \n"
        + "                [  ][  ][  ]                \n"
        + "\n"
        + "Turn: R, Dice: 1\n"
    )
    assert get_movables(state) == [None]
    assert random_evaluator(state) == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}


def test_board_1() -> None:
    state = replace(
        new_state(),
        board=((46, 1, 8, 10), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        dice=2,
        turn=0,
    )
    assert get_movables(state) == [4]
    state = apply_move_one(state, 4)
    assert state.board == ((46, 1, 8, 12), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state = replace(state, dice=5)
    assert is_start(state) is True
    assert (
        visualize(state, colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G3][G1]    [  ][  ][  ]    [B4][B3]    \n"
        + "    [G4][G2]    [  ][  ][  ]    [B2][B1]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[R4][  ][  ][  ][R3][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][R1][  ]                \n"
        + "    [  ][R2]    [  ][  ][  ]    [Y2][Y4]    \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y1][Y3]    \n"
        + "                [  ][  ][  ]                \n"
        + "\n"
        + "Turn: G, Dice: 5\n"
    )
    assert get_movables(state) == [None]
    assert random_evaluator(state) == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}


def test_board_2() -> None:
    state = replace(
        new_state(),
        board=((10, 4, 2, 43), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        dice=6,
        turn=0,
    )
    assert get_movables(state) == [1]
    state = apply_move_one(state, 1)
    assert state.board == ((16, 4, 2, 43), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state = replace(state, dice=5)
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G3][G1]    [  ][  ][  ]    [B4][B3]    \n"
        + "    [G4][G2]    [  ][  ][  ]    [B2][B1]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][  ][R1][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y2][Y4]    \n"
        + "    [R3][  ]    [  ][  ][  ]    [Y1][Y3]    \n"
        + "                [R2][R4][  ]                \n"
        + "\n"
        + "Turn: R, Dice: 5\n"
    )
    assert get_movables(state) == [1, 2]
    assert random_evaluator(state) == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}


def test_board_3() -> None:
    state = replace(
        new_state(),
        board=((0, 7, 46, 15), (0, 34, 2, 3), (0, 1, 2, 3), (0, 1, 2, 19)),
        dice=2,
        turn=0,
    )
    assert get_movables(state) == [2, 4]
    state = apply_move_one(state, 2)
    assert state.board == ((0, 9, 46, 15), (0, 34, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state = replace(state, dice=5)
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G3][G1]    [  ][  ][  ]    [B4][B3]    \n"
        + "    [G4][  ]    [  ][  ][  ]    [B2][B1]    \n"
        + "                [  ][  ][  ]                \n"
        + "[  ][R4][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][R2][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][R3][  ]                \n"
        + "    [R1][  ]    [  ][  ][  ]    [Y2][Y4]    \n"
        + "    [  ][  ]    [  ][  ][  ]    [Y1][Y3]    \n"
        + "                [G2][  ][  ]                \n"
        + "\n"
        + "Turn: G, Dice: 5\n"
    )
    assert get_movables(state) == [2]
    assert random_evaluator(state) == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}


def test_board_4() -> None:
    state = replace(
        new_state(),
        board=((13, 43, 2, 3), (0, 1, 34, 3), (0, 1, 2, 3), (0, 29, 2, 3)),
        dice=6,
        turn=0,
    )
    assert get_movables(state) == [1, 3, 4]
    state = apply_move_one(state, 3)
    assert state.board == ((13, 43, 4, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 29, 2, 3))
    state = replace(state, dice=3)
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
        == "                [  ][  ][  ]                \n"
        + "    [G3][G1]    [  ][  ][  ]    [B4][B3]    \n"
        + "    [G4][G2]    [  ][  ][  ]    [B2][B1]    \n"
        + "                [Y2][  ][  ]                \n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "[R1][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [  ][  ]    [  ][  ][  ]    [  ][Y4]    \n"
        + "    [  ][R4]    [  ][  ][  ]    [Y1][Y3]    \n"
        + "                [R3][R2][  ]                \n"
        + "\n"
        + "Turn: R, Dice: 3\n"
    )
    assert get_movables(state) == [1, 2, 3]
    assert random_evaluator(state) == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}


def test_board_5() -> None:
    state = replace(
        new_state(),
        board=((0, 29, 2, 3), (13, 43, 2, 3), (0, 1, 34, 3), (0, 1, 2, 3)),
        dice=6,
        turn=1,
    )
    assert get_movables(state) == [1, 3, 4]
    state = apply_move_one(state, 4)
    assert state.board == ((0, 29, 2, 3), (13, 43, 2, 4), (0, 1, 2, 3), (0, 1, 2, 3))
    state = replace(state, dice=4)
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
        == "                [  ][G1][  ]                \n"
        + "    [G3][  ]    [  ][  ][  ]    [B4][B3]    \n"
        + "    [  ][  ]    [  ][  ][  ]    [B2][B1]    \n"
        + "                [  ][  ][  ]                \n"
        + "[G4][  ][  ][  ][  ][  ][  ][R2][  ][  ][  ]\n"
        + "[G2][  ][  ][  ][  ]    [  ][  ][  ][  ][  ]\n"
        + "[  ][  ][  ][  ][  ][  ][  ][  ][  ][  ][  ]\n"
        + "                [  ][  ][  ]                \n"
        + "    [R1][  ]    [  ][  ][  ]    [Y2][Y4]    \n"
        + "    [R3][R4]    [  ][  ][  ]    [Y1][Y3]    \n"
        + "                [  ][  ][  ]                \n"
        + "\n"
        + "Turn: G, Dice: 4\n"
    )
    assert get_movables(state) == [1, 2, 4]
    assert random_evaluator(state) == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}


def test_get_absolute_pos() -> None:
    assert get_absolute_pos(4, 0) == 0
    assert get_absolute_pos(14, 0) == 10
    assert get_absolute_pos(43, 0) == 39

    assert get_absolute_pos(4, 1) == 10
    assert get_absolute_pos(14, 1) == 20
    assert get_absolute_pos(43, 1) == 9

    assert get_absolute_pos(4, 2) == 20
    assert get_absolute_pos(14, 2) == 30
    assert get_absolute_pos(43, 2) == 19

    assert get_absolute_pos(4, 3) == 30
    assert get_absolute_pos(14, 3) == 0
    assert get_absolute_pos(43, 3) == 29


def test_is_same_pos() -> None:
    assert is_same_pos(4, 0, 14, 3) is True
    assert is_same_pos(14, 3, 4, 0) is True

    assert is_same_pos(14, 0, 4, 1) is True
    assert is_same_pos(4, 1, 14, 0) is True

    assert is_same_pos(10, 0, 10, 0) is True
    assert is_same_pos(20, 2, 20, 2) is True

    assert is_same_pos(4, 0, 5, 0) is False
    assert is_same_pos(10, 1, 20, 2) is False

    assert is_same_pos(3, 0, 10, 0) is False
    assert is_same_pos(10, 0, 3, 0) is False
    assert is_same_pos(44, 0, 10, 0) is False
    assert is_same_pos(10, 0, 44, 0) is False
    assert is_same_pos(0, 0, 50, 0) is False


def test_visualize_colored() -> None:
    state = replace(new_state(), dice=1)

    red_bg = "\033[97;41m"
    green_bg = "\033[97;42m"
    blue_bg = "\033[97;44m"
    yellow_bg = "\033[30;43m"
    reset = "\033[0m"

    colored_output = visualize(state, colored=True)

    assert f"[{red_bg}R{reset}1]" in colored_output
    assert f"[{green_bg}G{reset}1]" in colored_output
    assert f"[{blue_bg}B{reset}1]" in colored_output
    assert f"[{yellow_bg}Y{reset}1]" in colored_output

    assert f"Turn: {red_bg}R{reset}, Dice: 1" in colored_output


def test_visualize_colored_winner() -> None:
    state = replace(
        new_state(),
        board=((44, 45, 46, 47), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        turn=None,
        winner=0,
    )

    red_bg = "\033[97;41m"
    reset = "\033[0m"

    colored_output = visualize(state, colored=True)
    assert f"Winner: {red_bg}R{reset}" in colored_output


def test_three_sixes_rule() -> None:
    state = replace(
        new_state(),
        board=((4, 5, 6, 7), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        turn=0,
        count_six=0,
    )

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.count_six == 1
    assert state.turn == 0

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.count_six == 2
    assert state.turn == 0

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.count_six == 0
    assert state.turn == 1


def test_three_sixes_rule_reset_on_non_six() -> None:
    state = replace(
        new_state(),
        board=((4, 5, 6, 7), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        turn=0,
        count_six=0,
    )

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.count_six == 1
    assert state.turn == 0

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.count_six == 2
    assert state.turn == 0

    state = replace(state, dice=3)
    state = apply_move_one(state, 1)
    assert state.count_six == 0
    assert state.turn == 1


def test_three_starts_rule() -> None:
    state = replace(
        new_state(),
        board=((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        turn=0,
        count_start=0,
    )

    state = replace(state, dice=3)
    assert get_movables(state) == [None]
    state = apply_move_one(state, None)
    assert state.count_start == 1
    assert state.turn == 0

    state = replace(state, dice=2)
    state = apply_move_one(state, None)
    assert state.count_start == 2
    assert state.turn == 0

    state = replace(state, dice=4)
    state = apply_move_one(state, None)
    assert state.count_start == 0
    assert state.turn == 1


def test_three_starts_rule_reset_on_leaving_start() -> None:
    state = replace(
        new_state(),
        board=((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        turn=0,
        count_start=0,
    )

    state = replace(state, dice=3)
    state = apply_move_one(state, None)
    assert state.count_start == 1
    assert state.turn == 0

    state = replace(state, dice=2)
    state = apply_move_one(state, None)
    assert state.count_start == 2
    assert state.turn == 0

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.board[0][0] == 4
    assert is_start(state) is False
    assert state.count_start == 0
    assert state.count_six == 1
    assert state.turn == 0


def test_three_starts_with_six_interaction() -> None:
    state = replace(
        new_state(),
        board=((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        turn=0,
        count_start=2,
        count_six=0,
    )

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert is_start(state) is False
    assert state.count_start == 0
    assert state.count_six == 1
    assert state.turn == 0

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.count_six == 2
    assert state.turn == 0

    state = replace(state, dice=6)
    state = apply_move_one(state, 1)
    assert state.count_six == 0
    assert state.turn == 1


def test_count_six_reset_on_pass() -> None:
    state = replace(
        new_state(),
        board=((43, 45, 46, 47), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        turn=0,
        count_six=1,
    )

    state = replace(state, dice=6)
    assert get_movables(state) == [None]
    state = apply_move_one(state, None)

    assert state.count_six == 0
    assert state.turn == 1


def run_cli(initial: State, input_text: str, depth: int = 0) -> str:
    stdout = io.StringIO()
    Cli(
        HOTARU_GAME,
        Agent(lambda state: dict.fromkeys(range(1, 5), 0.0), depth),
        initial,
        stdin=io.StringIO(input_text),
        stdout=stdout,
    ).cmdloop()
    return stdout.getvalue()


def test_cli_move() -> None:
    state = replace(
        new_state(),
        board=((10, 4, 2, 43), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        dice=6,
        turn=0,
    )
    output = run_cli(state, "move 1\n")
    assert "Cannot Move" not in output


def test_cli_move_illegal() -> None:
    state = replace(new_state(), dice=3, turn=0)
    output = run_cli(state, "move 1\n")
    assert "Cannot Move: 1" in output


def test_cli_pass() -> None:
    state = replace(new_state(), dice=3, turn=0)
    output = run_cli(state, "pass\n")
    assert "Cannot Pass" not in output


def test_cli_pass_illegal() -> None:
    state = replace(new_state(), dice=6, turn=0)
    output = run_cli(state, "pass\n")
    assert "Cannot Pass" in output


def test_cli_auto() -> None:
    state = replace(
        new_state(),
        board=((10, 4, 2, 43), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
        dice=6,
        turn=0,
    )
    output = run_cli(state, "auto\n")
    assert "Cannot" not in output
    assert output.count("Dice:") == 2


def test_cli_unknown_command() -> None:
    state = replace(new_state(), dice=3, turn=0)
    output = run_cli(state, "invalid\n")
    assert "Unknown syntax: invalid" in output


def test_cli_players_option() -> None:
    green_bg, reset = "\033[97;42m", "\033[0m"
    stdout = io.StringIO()
    cli(argv=["--players", "1,3"], stdin=io.StringIO(""), stdout=stdout)
    assert f"Turn: {green_bg}G{reset}" in stdout.getvalue()


def test_cli_players_option_invalid() -> None:
    with pytest.raises(SystemExit):
        cli(argv=["--players", "0"])


def test_autoplay_1() -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                random_evaluator,
                random_evaluator,
                random_evaluator,
                random_evaluator,
            ]
        )
        wins[result] += 1
    assert all(400 < win < 600 for win in wins)


def test_autoplay_2() -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                random_evaluator,
                None,
                random_evaluator,
                None,
            ]
        )
        wins[result] += 1
    assert wins[1] == wins[3] == 0 and 800 < wins[0] < 1200 and 800 < wins[2] < 1200


def test_hotaru_evaluator_endgame_only_outside_theo(
    endgame_params: mmap.mmap,
) -> None:
    state = replace(new_state(), dice=1)
    assert hotaru_evaluator(state, None, endgame_params) == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}


def test_autoplay_3(midgame_params: bytes) -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                random_evaluator,
                None,
                lambda state: hotaru_evaluator(state, midgame_params, None),
                None,
            ]
        )
        wins[result] += 1
    assert wins[1] == wins[3] == 0 and wins[0] < 600


def test_autoplay_4(
    midgame_params: bytes,
    endgame_params: mmap.mmap,
) -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                lambda state: hotaru_evaluator(state, midgame_params, None),
                None,
                lambda state: hotaru_evaluator(state, midgame_params, endgame_params),
                None,
            ]
        )
        wins[result] += 1
    assert wins[1] == wins[3] == 0 and 1000 < wins[2] < 1130
