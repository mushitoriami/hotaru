Board = list[list[int]]


def init_board() -> Board:
    return [[i for i in range(4)] for _ in range(4)]


def is_end_board(board: Board, turn: int) -> bool:
    return set(board[turn]) == {44, 45, 46, 47}


def get_movables_board(board: Board, turn: int, dice: int) -> list[int]:
    moves = []
    for i in range(4):
        move_from = board[turn][i]
        if move_from >= 4:
            move_to = move_from + dice
        elif dice == 6:
            move_to = 4
        else:
            continue
        if move_to <= 47 and move_to not in board[turn]:
            moves.append(i)
    return moves


def get_absolute_pos(pos: int, turn: int) -> int:
    return (pos - 4 + turn * 10) % 40


def is_same_pos(pos1: int, turn1: int, pos2: int, turn2: int) -> bool:
    if not (4 <= pos1 <= 43 and 4 <= pos2 <= 43):
        return False
    return get_absolute_pos(pos1, turn1) == get_absolute_pos(pos2, turn2)


def move_board(board: Board, piece: int, turn: int, dice: int) -> Board:
    move_to = board[turn][piece] + dice if board[turn][piece] >= 4 else 4
    board_new = [
        [
            p if is_same_pos(move_to, turn, board[t][p], t) else board[t][p]
            for p in range(4)
        ]
        for t in range(4)
    ]
    board_new[turn][piece] = move_to
    return board_new
