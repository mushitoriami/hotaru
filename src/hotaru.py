from __future__ import annotations

import argparse
import mmap
import random
import readline  # noqa: F401
import struct
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, replace
from math import comb
from pathlib import Path


@dataclass
class State:
    players: frozenset[int]
    board: tuple[tuple[int, ...], ...]
    turn: int | None
    winner: int | None
    dice: int
    count_six: int
    count_start: int


def new_state(players: frozenset[int] | None = None) -> State:
    players = frozenset(range(4)) if players is None else players
    assert len(players) >= 2 and players <= frozenset(range(4))
    return State(
        players=players,
        board=tuple(tuple(range(4)) for _ in range(4)),
        turn=min(players),
        winner=None,
        dice=random.randint(1, 6),
        count_six=0,
        count_start=0,
    )


def next_turn(state: State, turn: int) -> int:
    t = turn
    while True:
        t = (t + 1) % 4
        if t in state.players:
            return t


def is_start(state: State) -> bool:
    return state.turn is not None and set(state.board[state.turn]) == {0, 1, 2, 3}


def get_movables(state: State) -> list[int | None]:
    if state.turn is None:
        return []
    moves: list[int | None] = []
    for i in range(4):
        move_from = state.board[state.turn][i]
        if move_from >= 4:
            move_to = move_from + state.dice
        elif state.dice == 6:
            move_to = 4
        else:
            continue
        if move_to <= 47 and move_to not in state.board[state.turn]:
            moves.append(i + 1)
    if len(moves) == 0:
        moves.append(None)
    return moves


def apply_move(state: State, piece: int | None) -> State:
    new = replace(state)
    if new.turn is not None and piece is not None:
        move_to = (
            new.board[new.turn][piece - 1] + new.dice
            if new.board[new.turn][piece - 1] >= 4
            else 4
        )
        board = [list(row) for row in new.board]
        for t in range(4):
            for p in range(4):
                if is_same_pos(move_to, new.turn, board[t][p], t):
                    board[t][p] = p
        board[new.turn][piece - 1] = move_to
        new.board = tuple(tuple(row) for row in board)
    if piece is not None:
        new.count_six = (new.count_six + 1) % 3 if new.dice == 6 else 0
    else:
        new.count_six = 0
    new.count_start = (new.count_start + 1) % 3 if is_start(new) else 0
    if new.turn is not None:
        if set(new.board[new.turn]) == {44, 45, 46, 47}:
            new.winner = new.turn
            new.turn = None
        else:
            if new.count_six == 0 and new.count_start == 0:
                new.turn = next_turn(new, new.turn)
            new.dice = random.randint(1, 6)
    return new


def _rotate_quarter(pos: tuple[int, int]) -> tuple[int, int]:
    x, y = pos
    return (y, 10 - x)


def _rotate_track(points: list[tuple[int, int]], n: int) -> list[tuple[int, int]]:
    for _ in range(n):
        points = [_rotate_quarter(p) for p in points]
    return points


_BOARD_SIZE = 11

_TRACK = [(10, 4), (9, 4), (8, 4), (7, 4), (6, 4)]
_TRACK += [(6, 3), (6, 2), (6, 1), (6, 0), (5, 0)]
_GOAL = [(9, 5), (8, 5), (7, 5), (6, 5)]
_HOME = [(8, 1), (8, 2), (9, 1), (9, 2)]
_TRACKS = [_rotate_track(_TRACK, t) for t in range(4)]
_GOALS = [_rotate_track(_GOAL, t) for t in range(4)]
_HOMES = [_rotate_track(_HOME, t) for t in range(4)]
_MAPPING = [
    _HOMES[t] + sum((_TRACKS[(t + i) % 4] for i in range(4)), []) + _GOALS[t]
    for t in range(4)
]

_USABLE_CELLS = frozenset(pos for player in _MAPPING for pos in player)
_BOARD_TEMPLATE: tuple[tuple[str | None, ...], ...] = tuple(
    tuple(
        "  " if (x, y) in _USABLE_CELLS else None for y in range(_BOARD_SIZE)
    )
    for x in range(_BOARD_SIZE)
)


def visualize(state: State, colored: bool = True) -> str:
    color_bg = ["\033[97;41m", "\033[97;42m", "\033[97;44m", "\033[30;43m"]
    color_reset = "\033[0m"
    mapping_color = ["R", "G", "B", "Y"]

    table: list[list[None | str]] = [list(row) for row in _BOARD_TEMPLATE]
    for t in range(4):
        for p in range(4):
            x, y = _MAPPING[t][state.board[t][p]]
            if colored:
                table[x][y] = color_bg[t] + mapping_color[t] + color_reset + str(p + 1)
            else:
                table[x][y] = mapping_color[t] + str(p + 1)
    visualized = ""
    for x in range(11):
        for c in table[x]:
            visualized += "[" + c + "]" if c is not None else "    "
        visualized += "\n"
    visualized += "\n"
    if state.turn is not None:
        turn_label = mapping_color[state.turn]
        if colored:
            turn_label = color_bg[state.turn] + turn_label + color_reset
        visualized += "Turn: " + turn_label + ", Dice: " + str(state.dice)
    elif state.winner is not None:
        winner_label = mapping_color[state.winner]
        if colored:
            winner_label = color_bg[state.winner] + winner_label + color_reset
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


def eval_state_theo(mm: mmap.mmap, state: State, turn: int) -> float:
    return read_bin(mm, index_state(state, turn))


def read_bin(mm: mmap.mmap, index: int) -> float:
    r = struct.unpack_from("f", mm, index * 4)[0]
    assert isinstance(r, float)
    return r


def rank_pieces(positions: tuple[int, ...]) -> tuple[int, int, int]:
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
        self.params_endgame: mmap.mmap | None = None
        if enable_endgame:
            with open("params_endgame.dat", "rb") as f:
                self.params_endgame = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        self.enable_endgame: bool = enable_endgame

    def score_theo(self, s: State, turn: int) -> float:
        assert self.params_endgame is not None
        return 1 - 2 * eval_state_theo(self.params_endgame, s, 1 if turn == 0 else 0)

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
        for move in get_movables(state):
            state_next = apply_move(state, move)
            if in_theo(state_next) and self.enable_endgame:
                result[move] = self.score_theo(state_next, state.turn)
            elif self.params_midgame is not None:
                result[move] = self.score(state_next, state.turn)
            else:
                result[move] = 0
        return result


class RandomEvaluator(Evaluator):
    def eval(self, state: State) -> dict[int | None, float]:
        return dict.fromkeys(get_movables(state), 0)


def get_absolute_pos(pos: int, turn: int) -> int:
    return (pos - 4 + turn * 10) % 40


def is_same_pos(pos1: int, turn1: int, pos2: int, turn2: int) -> bool:
    if not (4 <= pos1 <= 43 and 4 <= pos2 <= 43):
        return False
    return get_absolute_pos(pos1, turn1) == get_absolute_pos(pos2, turn2)


def autoplay(evaluators: list[Evaluator | None]) -> int:
    state = new_state()
    while state.turn is not None:
        evaluator = evaluators[state.turn]
        if evaluator is None:
            state = apply_move(state, None)
        else:
            scores = evaluator.eval(state)
            move = random.choice(
                [
                    move
                    for move, score in scores.items()
                    if score == max(scores.values())
                ]
            )
            state = apply_move(state, move)
    assert state.winner is not None
    return state.winner


def parse_players(value: str) -> frozenset[int]:
    try:
        players = frozenset(int(seat) for seat in value.split(","))
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid players: {value}") from None
    if not (players <= frozenset(range(4)) and len(players) >= 2):
        raise argparse.ArgumentTypeError(f"invalid players: {value}")
    return players


def cli(
    argv: list[str] | None = None,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[..., None] = print,
) -> None:
    parser = argparse.ArgumentParser(prog="hotaru")
    parser.add_argument(
        "--players",
        type=parse_players,
        default=frozenset(range(4)),
        help="comma-separated seat indices (0-3, at least 2) that participate,"
        " e.g. 0,2 (default: 0,1,2,3)",
    )
    args = parser.parse_args(argv)

    enable_midgame = Path("params_midgame.dat").exists()
    enable_endgame = Path("params_endgame.dat").exists()
    evaluator: Evaluator = (
        HotaruEvaluator(enable_midgame, enable_endgame)
        if enable_midgame or enable_endgame
        else RandomEvaluator()
    )
    state = new_state(players=args.players)
    history: list[State] = []
    query_previous = [""]
    while True:
        movables = get_movables(state)
        print_fn(visualize(state))
        while True:
            query = input_fn("> ").split()
            if len(query) == 0:
                query = query_previous
            else:
                query_previous = query
            if query[0] == "move":
                piece = int(query[1])
                if piece in movables:
                    history.append(state)
                    state = apply_move(state, piece)
                    break
                print_fn("Cannot move: " + query[1])
            elif query[0] == "pass":
                if None in movables:
                    history.append(state)
                    state = apply_move(state, None)
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
                history.append(state)
                state = apply_move(state, move)
                break
            elif query[0] == "dice":
                dice = int(query[1])
                if 1 <= dice <= 6:
                    state.dice = dice
                    break
                print_fn("Invalid dice roll: " + query[1])
            elif query[0] == "new":
                state = new_state(players=args.players)
                history = []
                break
            elif query[0] in ("undo",):
                if history:
                    state = history.pop()
                else:
                    print_fn("Cannot undo")
                break
            elif query[0] in ("quit", "exit"):
                return
            else:
                print_fn("Unknown command")
