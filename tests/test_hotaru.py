from collections.abc import Callable
from pathlib import Path

import pytest

from hotaru import (
    HotaruEvaluator,
    RandomEvaluator,
    apply_move,
    autoplay,
    cli,
    get_absolute_pos,
    get_movables,
    is_same_pos,
    is_start,
    new_state,
    visualize,
)


def test_init_board() -> None:
    assert new_state().board == ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))


def test_board_0() -> None:
    state = new_state()
    state.dice = 1
    assert is_start(state) is True
    assert (
        visualize(state, colored=False)
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
    assert RandomEvaluator().eval(state) == {None: 0}


def test_board_1() -> None:
    state = new_state()
    state.board = ((46, 1, 8, 10), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.dice, state.turn = 2, 0
    assert get_movables(state) == [4]
    state = apply_move(state, 4)
    assert state.board == ((46, 1, 8, 12), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.dice = 5
    assert is_start(state) is True
    assert (
        visualize(state, colored=False)
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
    assert RandomEvaluator().eval(state) == {None: 0}


def test_board_2() -> None:
    state = new_state()
    state.board = ((10, 4, 2, 43), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.dice, state.turn = 6, 0
    assert get_movables(state) == [1]
    state = apply_move(state, 1)
    assert state.board == ((16, 4, 2, 43), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.dice = 5
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
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
    assert RandomEvaluator().eval(state) == {1: 0, 2: 0}


def test_board_3() -> None:
    state = new_state()
    state.board = ((0, 7, 46, 15), (0, 34, 2, 3), (0, 1, 2, 3), (0, 1, 2, 19))
    state.dice, state.turn = 2, 0
    assert get_movables(state) == [2, 4]
    state = apply_move(state, 2)
    assert state.board == ((0, 9, 46, 15), (0, 34, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.dice = 5
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
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
    assert RandomEvaluator().eval(state) == {2: 0}


def test_board_4() -> None:
    state = new_state()
    state.board = ((13, 43, 2, 3), (0, 1, 34, 3), (0, 1, 2, 3), (0, 29, 2, 3))
    state.dice, state.turn = 6, 0
    assert get_movables(state) == [1, 3, 4]
    state = apply_move(state, 3)
    assert state.board == ((13, 43, 4, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 29, 2, 3))
    state.dice = 3
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
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
    assert RandomEvaluator().eval(state) == {1: 0, 2: 0, 3: 0}


def test_board_5() -> None:
    state = new_state()
    state.board = ((0, 29, 2, 3), (13, 43, 2, 3), (0, 1, 34, 3), (0, 1, 2, 3))
    state.dice, state.turn = 6, 1
    assert get_movables(state) == [1, 3, 4]
    state = apply_move(state, 4)
    assert state.board == ((0, 29, 2, 3), (13, 43, 2, 4), (0, 1, 2, 3), (0, 1, 2, 3))
    state.dice = 4
    assert is_start(state) is False
    assert (
        visualize(state, colored=False)
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
    assert RandomEvaluator().eval(state) == {1: 0, 2: 0, 4: 0}


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
    state = new_state()
    state.dice = 1

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
    state = new_state()
    state.board = ((44, 45, 46, 47), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.turn = None
    state.winner = 0

    red_bg = "\033[97;41m"
    reset = "\033[0m"

    colored_output = visualize(state, colored=True)
    assert f"Winner: {red_bg}R{reset}" in colored_output


def test_three_sixes_rule() -> None:
    state = new_state()
    state.board = ((4, 5, 6, 7), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.turn = 0
    state.count_six = 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.count_six == 1
    assert state.turn == 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.count_six == 2
    assert state.turn == 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.count_six == 0
    assert state.turn == 1


def test_three_sixes_rule_reset_on_non_six() -> None:
    state = new_state()
    state.board = ((4, 5, 6, 7), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.turn = 0
    state.count_six = 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.count_six == 1
    assert state.turn == 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.count_six == 2
    assert state.turn == 0

    state.dice = 3
    state = apply_move(state, 1)
    assert state.count_six == 0
    assert state.turn == 1


def test_three_starts_rule() -> None:
    state = new_state()
    state.board = ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.turn = 0
    state.count_start = 0

    state.dice = 3
    assert get_movables(state) == [None]
    state = apply_move(state, None)
    assert state.count_start == 1
    assert state.turn == 0

    state.dice = 2
    state = apply_move(state, None)
    assert state.count_start == 2
    assert state.turn == 0

    state.dice = 4
    state = apply_move(state, None)
    assert state.count_start == 0
    assert state.turn == 1


def test_three_starts_rule_reset_on_leaving_start() -> None:
    state = new_state()
    state.board = ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.turn = 0
    state.count_start = 0

    state.dice = 3
    state = apply_move(state, None)
    assert state.count_start == 1
    assert state.turn == 0

    state.dice = 2
    state = apply_move(state, None)
    assert state.count_start == 2
    assert state.turn == 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.board[0][0] == 4
    assert is_start(state) is False
    assert state.count_start == 0
    assert state.count_six == 1
    assert state.turn == 0


def test_three_starts_with_six_interaction() -> None:
    state = new_state()
    state.board = ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.turn = 0
    state.count_start = 2
    state.count_six = 0

    state.dice = 6
    state = apply_move(state, 1)
    assert is_start(state) is False
    assert state.count_start == 0
    assert state.count_six == 1
    assert state.turn == 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.count_six == 2
    assert state.turn == 0

    state.dice = 6
    state = apply_move(state, 1)
    assert state.count_six == 0
    assert state.turn == 1


def test_count_six_reset_on_pass() -> None:
    state = new_state()
    state.board = ((43, 45, 46, 47), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    state.turn = 0
    state.count_six = 1

    state.dice = 6
    assert get_movables(state) == [None]
    state = apply_move(state, None)

    assert state.count_six == 0
    assert state.turn == 1


@pytest.fixture
def run_cli() -> Callable[..., list[str]]:
    def _run(inputs: list[str], argv: list[str] | None = None) -> list[str]:
        input_iter = iter(inputs)
        outputs: list[str] = []

        def mock_input(prompt: str) -> str:
            return next(input_iter)

        def mock_print(*args: object) -> None:
            outputs.append(" ".join(str(arg) for arg in args))

        cli(
            argv=argv if argv is not None else [],
            input_fn=mock_input,
            print_fn=mock_print,
        )
        return outputs

    return _run


def test_cli_1(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["dice 6", "move 1", "quit"])
    assert any("Turn:" in output for output in outputs)
    assert not any("Cannot" in output for output in outputs)


def test_cli_2(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["dice 3", "move 1", "exit"])
    assert any("Cannot move: 1" in output for output in outputs)
    assert any("Turn:" in output for output in outputs)


def test_cli_3(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["dice 3", "pass", "quit"])
    assert not any("Cannot pass" in output for output in outputs)


def test_cli_4(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["dice 6", "pass", "quit"])
    assert any("Cannot pass" in output for output in outputs)


def test_cli_5(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["invalid", "quit"])
    assert any("Unknown command" in output for output in outputs)


def test_cli_6(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["undo", "quit"])
    assert any("Cannot undo" in output for output in outputs)


def test_cli_7(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["dice 6", "move 1", "undo", "quit"])
    assert not any("Cannot undo" in output for output in outputs)


def test_cli_8(run_cli: Callable[[list[str]], list[str]]) -> None:
    outputs = run_cli(["dice 6", "auto", "quit"])
    boards = [output for output in outputs if "Turn:" in output]
    assert len(boards) == 3
    assert boards[1] != boards[2]


def test_cli_players_option(run_cli: Callable[..., list[str]]) -> None:
    green_bg, reset = "\033[97;42m", "\033[0m"
    outputs = run_cli(["quit"], argv=["--players", "1,3"])
    assert any(f"Turn: {green_bg}G{reset}" in output for output in outputs)


def test_cli_players_option_invalid(run_cli: Callable[..., list[str]]) -> None:
    with pytest.raises(SystemExit):
        run_cli(["quit"], argv=["--players", "0"])


def test_autoplay_1(run_cli: Callable[[list[str]], list[str]]) -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                RandomEvaluator(),
                RandomEvaluator(),
                RandomEvaluator(),
                RandomEvaluator(),
            ]
        )
        wins[result] += 1
    assert all(400 < win < 600 for win in wins)


def test_autoplay_2(run_cli: Callable[[list[str]], list[str]]) -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                RandomEvaluator(),
                None,
                RandomEvaluator(),
                None,
            ]
        )
        wins[result] += 1
    assert wins[1] == wins[3] == 0 and 800 < wins[0] < 1200 and 800 < wins[2] < 1200


def test_hotaru_evaluator_endgame_only_outside_theo() -> None:
    state = new_state()
    state.dice = 1
    evaluator = HotaruEvaluator(enable_midgame=False, enable_endgame=True)
    assert evaluator.eval(state) == dict.fromkeys(get_movables(state), 0)


@pytest.mark.skipif(
    not Path("params_midgame.dat").exists(), reason="`params_midgame.dat` not found"
)
def test_autoplay_3(run_cli: Callable[[list[str]], list[str]]) -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                RandomEvaluator(),
                None,
                HotaruEvaluator(),
                None,
            ]
        )
        wins[result] += 1
    assert wins[1] == wins[3] == 0 and wins[0] < 600


@pytest.mark.skipif(
    not Path("params_midgame.dat").exists(), reason="`params_midgame.dat` not found"
)
@pytest.mark.skipif(
    not Path("params_endgame.dat").exists(), reason="`params_endgame.dat` not found"
)
def test_autoplay_4(run_cli: Callable[[list[str]], list[str]]) -> None:
    wins = [0, 0, 0, 0]
    for _ in range(2000):
        result = autoplay(
            [
                HotaruEvaluator(),
                None,
                HotaruEvaluator(enable_endgame=True),
                None,
            ]
        )
        wins[result] += 1
    assert wins[1] == wins[3] == 0 and 1000 < wins[2] < 1130
