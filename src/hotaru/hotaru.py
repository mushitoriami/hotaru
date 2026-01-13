Board = list[list[int]]


def init_board() -> Board:
    return [[i for i in range(4)] for _ in range(4)]


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


def move_board(board: Board, piece: int, turn: int, dice: int) -> Board:
    raise NotImplementedError


def pass_board(board: Board) -> Board:
    raise NotImplementedError


def add(x: int, y: int) -> int:
    return x + y
