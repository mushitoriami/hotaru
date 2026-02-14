from __future__ import annotations

import random
import readline
from abc import ABC, abstractmethod
from collections.abc import Callable

import numpy as np
import numpy.typing as npt


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


class Evaluator(ABC):
    @abstractmethod
    def eval(self, state: State) -> dict[int | None, float]:
        pass


class HotaruEvaluator(Evaluator):
    def __init__(self) -> None:
        self.params: npt.NDArray[np.float64] = np.load("params_midgame.npy")

    def eval(self, state: State) -> dict[int | None, float]:
        assert state.turn == 0 or state.turn == 2
        result = {}
        for move in state.get_movables():
            state_next = state.move(move)
            p = [piece * 2 for piece in state_next.board[state.turn]] + [
                piece * 2 + 1 for piece in state_next.board[(state.turn + 2) % 4]
            ]
            features = [p1 * 96 * 96 + p2 * 96 + p3 for p1 in p for p2 in p for p3 in p]
            result[move] = sum(self.params[i] for i in features)
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
    evaluator: Evaluator | None = None,
) -> None:
    evaluator = evaluator or RandomEvaluator()
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
                state.move(move)
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
            elif query[0] in ("undo"):
                if state.previous is not None:
                    state = state.previous
                else:
                    print_fn("Cannot undo")
                break
            elif query[0] in ("quit", "exit"):
                return
            else:
                print_fn("Unknown command")
