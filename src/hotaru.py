from __future__ import annotations

import random
import readline  # noqa: F401
import struct
from abc import ABC, abstractmethod
from collections.abc import Callable
from math import comb
from pathlib import Path


class State:
    def __init__(self, base: State | None = None) -> None:
        if base is None:
            self.board = [list(range(4)) for _ in range(4)]
            self.turn: int | None = 0
            self.winner: int | None = None
            self.dice = random.randint(1, 6)
            self.count_six, self.count_start = 0, 0
            self.previous: State | None = None
        else:
            self.board = [list(base.board[i]) for i in range(4)]
            self.turn = base.turn
            self.winner = base.winner
            self.dice = base.dice
            self.count_six, self.count_start = base.count_six, base.count_start
            self.previous = base

    def is_start(self) -> bool:
        return self.turn is not None and set(self.board[self.turn]) == {0, 1, 2, 3}

    def get_movables(self) -> list[int | None]:
        if self.turn is None:
            return []
        moves: list[int | None] = []
        for i in range(4):
            move_from = self.board[self.turn][i]
            if move_from >= 4:
                move_to = move_from + self.dice
            elif self.dice == 6:
                move_to = 4
            else:
                continue
            if move_to <= 47 and move_to not in self.board[self.turn]:
                moves.append(i + 1)
        if len(moves) == 0:
            moves.append(None)
        return moves

    def move(self, piece: int | None) -> State:
        state = State(self)
        if state.turn is not None and piece is not None:
            move_to = (
                state.board[state.turn][piece - 1] + state.dice
                if state.board[state.turn][piece - 1] >= 4
                else 4
            )
            for t in range(4):
                for p in range(4):
                    if is_same_pos(move_to, state.turn, state.board[t][p], t):
                        state.board[t][p] = p
            state.board[state.turn][piece - 1] = move_to
        if piece is not None:
            state.count_six = (state.count_six + 1) % 3 if state.dice == 6 else 0
        else:
            state.count_six = 0
        state.count_start = (state.count_start + 1) % 3 if state.is_start() else 0
        if state.turn is not None:
            if set(state.board[state.turn]) == {44, 45, 46, 47}:
                state.winner = state.turn
                state.turn = None
            else:
                if state.count_six == 0 and state.count_start == 0:
                    state.turn = (state.turn + 1) % 4
                state.dice = random.randint(1, 6)
        return state

    def visualize(self, colored: bool = True) -> str:
        color_bg = ["\033[97;41m", "\033[97;42m", "\033[97;44m", "\033[30;43m"]
        color_reset = "\033[0m"

        table: list[list[None | str]] = [
            [None, None, None, None, "  ", "  ", "  ", None, None, None, None],
            [None, "  ", "  ", None, "  ", "  ", "  ", None, "  ", "  ", None],
            [None, "  ", "  ", None, "  ", "  ", "  ", None, "  ", "  ", None],
            [None, None, None, None, "  ", "  ", "  ", None, None, None, None],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", None, "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            [None, None, None, None, "  ", "  ", "  ", None, None, None, None],
            [None, "  ", "  ", None, "  ", "  ", "  ", None, "  ", "  ", None],
            [None, "  ", "  ", None, "  ", "  ", "  ", None, "  ", "  ", None],
            [None, None, None, None, "  ", "  ", "  ", None, None, None, None],
        ]
        mapping_r = [
            (10, 4),
            (9, 4),
            (8, 4),
            (7, 4),
            (6, 4),
            (6, 3),
            (6, 2),
            (6, 1),
            (6, 0),
            (5, 0),
        ]
        mapping_g = [
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (3, 4),
            (2, 4),
            (1, 4),
            (0, 4),
            (0, 5),
        ]
        mapping_b = [
            (0, 6),
            (1, 6),
            (2, 6),
            (3, 6),
            (4, 6),
            (4, 7),
            (4, 8),
            (4, 9),
            (4, 10),
            (5, 10),
        ]
        mapping_y = [
            (6, 10),
            (6, 9),
            (6, 8),
            (6, 7),
            (6, 6),
            (7, 6),
            (8, 6),
            (9, 6),
            (10, 6),
            (10, 5),
        ]
        mapping = [
            (
                [(8, 1), (8, 2), (9, 1), (9, 2)]
                + (mapping_r + mapping_g + mapping_b + mapping_y)
                + [(9, 5), (8, 5), (7, 5), (6, 5)]
            ),
            (
                [(1, 1), (1, 2), (2, 1), (2, 2)]
                + (mapping_g + mapping_b + mapping_y + mapping_r)
                + [(5, 1), (5, 2), (5, 3), (5, 4)]
            ),
            (
                [(1, 8), (1, 9), (2, 8), (2, 9)]
                + (mapping_b + mapping_y + mapping_r + mapping_g)
                + [(1, 5), (2, 5), (3, 5), (4, 5)]
            ),
            (
                [(8, 8), (8, 9), (9, 8), (9, 9)]
                + (mapping_y + mapping_r + mapping_g + mapping_b)
                + [(5, 9), (5, 8), (5, 7), (5, 6)]
            ),
        ]
        mapping_color = ["R", "G", "B", "Y"]
        for t in range(4):
            for p in range(4):
                x, y = mapping[t][self.board[t][p]]
                if colored:
                    table[x][y] = (
                        color_bg[t] + mapping_color[t] + color_reset + str(p + 1)
                    )
                else:
                    table[x][y] = mapping_color[t] + str(p + 1)
        visualized = ""
        for x in range(11):
            for c in table[x]:
                visualized += "[" + c + "]" if c is not None else "    "
            visualized += "\n"
        visualized += "\n"
        if self.turn is not None:
            turn_label = mapping_color[self.turn]
            if colored:
                turn_label = color_bg[self.turn] + turn_label + color_reset
            visualized += "Turn: " + turn_label + ", Dice: " + str(self.dice)
        elif self.winner is not None:
            winner_label = mapping_color[self.winner]
            if colored:
                winner_label = color_bg[self.winner] + winner_label + color_reset
            visualized += "Winner: " + winner_label
        else:
            assert False, "unreachable"
        return visualized


def in_theo(s: State) -> bool:
    return (
        s.board[0][0] == 47
        or s.board[0][1] == 47
        or s.board[0][2] == 47
        or s.board[0][3] == 47
    ) and (
        s.board[2][0] == 47
        or s.board[2][1] == 47
        or s.board[2][2] == 47
        or s.board[2][3] == 47
    )


def eval_state_theo(filename: str, state: State, turn: int) -> float:
    return read_bin(filename, index_state(state, turn))


def read_bin(filename: str, index: int) -> float:
    with open(filename, "rb") as f:
        f.seek(index * 4)
        r = struct.unpack("f", f.read(4))[0]
        assert isinstance(r, float)
        return r


def rank_pieces(positions: list[int]) -> tuple[int, int, int]:
    d = sorted(positions, reverse=True)
    assert d[0] == 47
    for i, floor in ((3, 0), (2, 1), (1, 2)):
        if d[i] <= 3:
            d[i] = floor
    return 46 - d[1], d[1] - d[2] - 1, d[2] - d[3] - 1


def combination_rank(x1: int, x2: int, x3: int) -> int:
    a = 44
    return (
        comb(a + 3, 3)
        - comb(a - x1 + 3, 3)
        + comb(a - x1 + 2, 2)
        - comb(a - x1 - x2 + 2, 2)
        + x3
    )


def index_state(state: State, turn: int) -> int:
    p = combination_rank(*rank_pieces(state.board[0]))
    o = combination_rank(*rank_pieces(state.board[2]))
    span = comb(47, 3)
    return span * p + o if turn == 0 else span * o + p


class Evaluator(ABC):
    @abstractmethod
    def eval(self, state: State) -> dict[int | None, float]:
        pass


class HotaruEvaluator(Evaluator):
    def __init__(
        self, enable_midgame: bool = True, enable_endgame: bool = False
    ) -> None:
        self.params_midgame: bytes | None = None
        if enable_midgame:
            with open("params_midgame.dat", "rb") as f:
                self.params_midgame = f.read()
        self.enable_endgame: bool = enable_endgame

    def score_theo(self, s: State, turn: int) -> float:
        return 1 - 2 * eval_state_theo("params_endgame.dat", s, 1 if turn == 0 else 0)

    def score(self, state: State, turn: int) -> float:
        assert self.params_midgame is not None
        p = [piece * 2 for piece in state.board[turn]] + [
            piece * 2 + 1 for piece in state.board[(turn + 2) % 4]
        ]
        features = [p1 * 96 * 96 + p2 * 96 + p3 for p1 in p for p2 in p for p3 in p]
        r = sum(
            struct.unpack("d", self.params_midgame[i * 8 : i * 8 + 8])[0]
            for i in features
        )
        assert isinstance(r, float)
        return 2 * r - 1

    def eval(self, state: State) -> dict[int | None, float]:
        assert state.turn == 0 or state.turn == 2
        result = {}
        for move in state.get_movables():
            state_next = state.move(move)
            if in_theo(state_next) and self.enable_endgame:
                result[move] = self.score_theo(state_next, state.turn)
            elif self.params_midgame is not None:
                result[move] = self.score(state_next, state.turn)
            else:
                result[move] = 0
        return result


class RandomEvaluator(Evaluator):
    def eval(self, state: State) -> dict[int | None, float]:
        return dict.fromkeys(state.get_movables(), 0)


def get_absolute_pos(pos: int, turn: int) -> int:
    return (pos - 4 + turn * 10) % 40


def is_same_pos(pos1: int, turn1: int, pos2: int, turn2: int) -> bool:
    if not (4 <= pos1 <= 43 and 4 <= pos2 <= 43):
        return False
    return get_absolute_pos(pos1, turn1) == get_absolute_pos(pos2, turn2)


def autoplay(evaluators: list[Evaluator | None]) -> int:
    state = State()
    while state.turn is not None:
        evaluator = evaluators[state.turn]
        if evaluator is None:
            state = state.move(None)
        else:
            scores = evaluator.eval(state)
            move = random.choice(
                [
                    move
                    for move, score in scores.items()
                    if score == max(scores.values())
                ]
            )
            state = state.move(move)
    assert state.winner is not None
    return state.winner


def cli(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[..., None] = print,
) -> None:
    enable_midgame = Path("params_midgame.dat").exists()
    enable_endgame = Path("params_endgame.dat").exists()
    evaluator: Evaluator = (
        HotaruEvaluator(enable_midgame, enable_endgame)
        if enable_midgame or enable_endgame
        else RandomEvaluator()
    )
    state = State()
    query_previous = [""]
    while True:
        movables = state.get_movables()
        print_fn(state.visualize())
        while True:
            query = input_fn("> ").split()
            if len(query) == 0:
                query = query_previous
            else:
                query_previous = query
            if query[0] == "move":
                piece = int(query[1])
                if piece in movables:
                    state = state.move(piece)
                    break
                print_fn("Cannot move: " + query[1])
            elif query[0] == "pass":
                if None in movables:
                    state = state.move(None)
                    break
                print_fn("Cannot pass")
            elif query[0] == "eval":
                scores = evaluator.eval(state)
                print_fn(
                    "Scores | "
                    + ", ".join(
                        [
                            (str(move) if move is not None else "Pass")
                            + ": "
                            + str(score)
                            for move, score in scores.items()
                        ]
                    )
                )
            elif query[0] == "auto":
                scores = evaluator.eval(state)
                move = random.choice(
                    [
                        move
                        for move, score in scores.items()
                        if score == max(scores.values())
                    ]
                )
                state = state.move(move)
                break
            elif query[0] == "dice":
                dice = int(query[1])
                if 1 <= dice <= 6:
                    state.dice = dice
                    break
                print_fn("Invalid dice roll: " + query[1])
            elif query[0] == "new":
                state = State()
                break
            elif query[0] in ("undo",):
                if state.previous is not None:
                    state = state.previous
                else:
                    print_fn("Cannot undo")
                break
            elif query[0] in ("quit", "exit"):
                return
            else:
                print_fn("Unknown command")
