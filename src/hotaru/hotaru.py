Board = list[int]


def init_board() -> Board:
    return [i // 4 for i in range(16)]


def get_movables_board(board: Board, turn: int, dice: int) -> list[int]:
    raise NotImplementedError


def move_board(board: Board, piece: int, dice: int) -> Board:
    raise NotImplementedError


def pass_board(board: Board) -> Board:
    raise NotImplementedError


def add(x: int, y: int) -> int:
    return x + y
