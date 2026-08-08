from __future__ import annotations

import argparse
import mmap
import random
import struct
from collections.abc import Callable
from dataclasses import dataclass, replace
from math import comb
from pathlib import Path
from typing import IO

from shizuku import Agent, Cli, Game
from shizuku import play_auto as engine_play_auto


@dataclass(frozen=True)
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


def apply_move(state: State, piece: int | None) -> set[State]:
    board = state.board
    if state.turn is not None and piece is not None:
        move_to = (
            board[state.turn][piece - 1] + state.dice
            if board[state.turn][piece - 1] >= 4
            else 4
        )
        board_rows = [list(row) for row in board]
        for t in range(4):
            for p in range(4):
                if is_same_pos(move_to, state.turn, board_rows[t][p], t):
                    board_rows[t][p] = p
        board_rows[state.turn][piece - 1] = move_to
        board = tuple(tuple(row) for row in board_rows)

    count_six = (
        (state.count_six + 1) % 3 if piece is not None and state.dice == 6 else 0
    )
    count_start = (
        (state.count_start + 1) % 3 if is_start(replace(state, board=board)) else 0
    )

    turn = state.turn
    winner = state.winner
    reroll = False
    if turn is not None:
        if set(board[turn]) == {44, 45, 46, 47}:
            winner = turn
            turn = None
        else:
            if count_six == 0 and count_start == 0:
                turn = next_turn(state, turn)
            reroll = True

    base = replace(
        state,
        board=board,
        turn=turn,
        winner=winner,
        count_six=count_six,
        count_start=count_start,
    )
    if reroll:
        return {replace(base, dice=dice) for dice in range(1, 7)}
    return {base}


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


_COLOR_BG = ["\033[97;41m", "\033[97;42m", "\033[97;44m", "\033[30;43m"]
_COLOR_RESET = "\033[0m"
_PLAYER_LABELS = ["R", "G", "B", "Y"]


def _render_player_label(t: int, colored: bool) -> str:
    label = _PLAYER_LABELS[t]
    return _COLOR_BG[t] + label + _COLOR_RESET if colored else label


def _render_cell(x: int, y: int, pieces: dict[tuple[int, int], str]) -> str:
    if (x, y) in pieces:
        return "[" + pieces[(x, y)] + "]"
    if (x, y) in _USABLE_CELLS:
        return "[  ]"
    return "    "


def _render_board(state: State, colored: bool) -> str:
    pieces = {
        _MAPPING[t][state.board[t][p]]: _render_player_label(t, colored) + str(p + 1)
        for t in range(4)
        for p in range(4)
    }
    rows = (
        "".join(_render_cell(x, y, pieces) for y in range(_BOARD_SIZE))
        for x in range(_BOARD_SIZE)
    )
    return "\n".join(rows)


def _render_status(state: State, colored: bool) -> str:
    if state.turn is not None:
        return f"Turn: {_render_player_label(state.turn, colored)}, Dice: {state.dice}"
    if state.winner is not None:
        return f"Winner: {_render_player_label(state.winner, colored)}"
    assert False, "unreachable"


def visualize(state: State, colored: bool = True) -> str:
    return _render_board(state, colored) + "\n\n" + _render_status(state, colored) + "\n"


def in_theo(s: State, turn: int) -> bool:
    return any(p == 47 for p in s.board[turn]) and any(
        p == 47 for p in s.board[(turn + 2) % 4]
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
    p = combination_rank(*rank_pieces(state.board[turn]))
    o = combination_rank(*rank_pieces(state.board[(turn + 2) % 4]))
    span = comb(47, 3)
    return span * p + o


Evaluator = Callable[[State], dict[int, float]]


def score_midgame(
    params_midgame: bytes | None, state: State, turn: int
) -> float | None:
    if params_midgame is None:
        return None
    p = [piece * 2 for piece in state.board[turn]] + [
        piece * 2 + 1 for piece in state.board[(turn + 2) % 4]
    ]
    features = [p1 * 96 * 96 + p2 * 96 + p3 for p1 in p for p2 in p for p3 in p]
    r = sum(struct.unpack("d", params_midgame[i * 8 : i * 8 + 8])[0] for i in features)
    assert isinstance(r, float)
    return 2 * r - 1


def score_endgame(
    params_endgame: mmap.mmap | None, s: State, turn: int
) -> float | None:
    if params_endgame is None or not in_theo(s, turn):
        return None
    return 1 - 2 * eval_state_theo(params_endgame, s, (turn + 2) % 4)


def score_player(
    state: State,
    turn: int,
    params_midgame: bytes | None,
    params_endgame: mmap.mmap | None,
) -> float:
    score = score_endgame(params_endgame, state, turn)
    if score is None:
        score = score_midgame(params_midgame, state, turn)
    return score if score is not None else 0


def hotaru_evaluator(
    state: State,
    params_midgame: bytes | None,
    params_endgame: mmap.mmap | None,
) -> dict[int, float]:
    def score(turn: int) -> float:
        if turn not in state.players:
            return 0.0
        return score_player(state, turn, params_midgame, params_endgame)

    return {turn: score(turn) for turn in range(4)}


def random_evaluator(state: State) -> dict[int, float]:
    return {turn: 0.0 for turn in range(4)}


def get_absolute_pos(pos: int, turn: int) -> int:
    return (pos - 4 + turn * 10) % 40


def is_same_pos(pos1: int, turn1: int, pos2: int, turn2: int) -> bool:
    if not (4 <= pos1 <= 43 and 4 <= pos2 <= 43):
        return False
    return get_absolute_pos(pos1, turn1) == get_absolute_pos(pos2, turn2)


def _current_player(state: State) -> int:
    assert state.turn is not None
    return state.turn + 1


HOTARU_GAME: Game[State, int] = Game(
    get_moves=lambda state: frozenset(get_movables(state)),
    apply_move=lambda move, state: apply_move(state, move),
    is_end=lambda state: state.turn is None,
    current_player=_current_player,
    player_count=lambda state: 4,
    parse_move=int,
    format_move=str,
    render=visualize,
)


def _adapt_evaluator(evaluator: Evaluator) -> Callable[[State], dict[int, float]]:
    def adapted(state: State) -> dict[int, float]:
        return {seat + 1: score for seat, score in evaluator(state).items()}

    return adapted


def choose_move(state: State, evaluator: Evaluator) -> int | None:
    assert state.turn is not None
    return engine_play_auto(HOTARU_GAME, Agent(_adapt_evaluator(evaluator), 0), state)


def autoplay(evaluators: list[Evaluator | None]) -> int:
    state = new_state()
    while state.turn is not None:
        evaluator = evaluators[state.turn]
        move = None if evaluator is None else choose_move(state, evaluator)
        state = random.choice(list(apply_move(state, move)))
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
    stdin: IO[str] | None = None,
    stdout: IO[str] | None = None,
) -> None:
    parser = argparse.ArgumentParser(prog="hotaru")
    parser.add_argument(
        "--players",
        type=parse_players,
        default=frozenset(range(4)),
        help="comma-separated seat indices (0-3, at least 2) that participate,"
        " e.g. 0,2 (default: 0,1,2,3)",
    )
    parser.add_argument(
        "--midgame-params",
        type=Path,
        default=None,
        help="path to the midgame parameters file (enables midgame scoring if given)",
    )
    parser.add_argument(
        "--endgame-params",
        type=Path,
        default=None,
        help="path to the endgame parameters file (enables endgame lookups if given)",
    )
    args = parser.parse_args(argv)

    params_midgame: bytes | None = None
    if args.midgame_params is not None:
        with open(args.midgame_params, "rb") as f:
            params_midgame = f.read()
    params_endgame: mmap.mmap | None = None
    if args.endgame_params is not None:
        with open(args.endgame_params, "rb") as f:
            params_endgame = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    evaluator: Evaluator = (
        (lambda state: hotaru_evaluator(state, params_midgame, params_endgame))
        if params_midgame is not None or params_endgame is not None
        else random_evaluator
    )
    Cli(
        HOTARU_GAME,
        Agent(_adapt_evaluator(evaluator), 0),
        new_state(players=args.players),
        stdin=stdin,
        stdout=stdout,
    ).cmdloop()
