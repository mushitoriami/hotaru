import random


class Board:
    def __init__(self) -> None:
        self.board = [[i for i in range(4)] for _ in range(4)]

    def is_start(self, turn: int) -> bool:
        return set(self.board[turn]) == {0, 1, 2, 3}

    def is_end(self, turn: int) -> bool:
        return set(self.board[turn]) == {44, 45, 46, 47}

    def get_movables(self, turn: int, dice: int) -> list[int]:
        moves = []
        for i in range(4):
            move_from = self.board[turn][i]
            if move_from >= 4:
                move_to = move_from + dice
            elif dice == 6:
                move_to = 4
            else:
                continue
            if move_to <= 47 and move_to not in self.board[turn]:
                moves.append(i)
        return moves

    def move(self, piece: int, turn: int, dice: int) -> "Board":
        move_to = self.board[turn][piece] + dice if self.board[turn][piece] >= 4 else 4
        board_new = Board()
        board_new.board = [
            [
                p
                if is_same_pos(move_to, turn, self.board[t][p], t)
                else self.board[t][p]
                for p in range(4)
            ]
            for t in range(4)
        ]
        board_new.board[turn][piece] = move_to
        return board_new

    def visualize(self) -> str:
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
                table[x][y] = mapping_color[t] + str(p + 1)
        visualized = ""
        for x in range(11):
            for c in table[x]:
                visualized += "[" + c + "]" if c is not None else "    "
            visualized += "\n"
        return visualized


def get_absolute_pos(pos: int, turn: int) -> int:
    return (pos - 4 + turn * 10) % 40


def is_same_pos(pos1: int, turn1: int, pos2: int, turn2: int) -> bool:
    if not (4 <= pos1 <= 43 and 4 <= pos2 <= 43):
        return False
    return get_absolute_pos(pos1, turn1) == get_absolute_pos(pos2, turn2)


def game() -> None:
    board = Board()
    turn = 0
    count_six, count_start = 0, 0
    while True:
        dice = random.randint(1, 6)
        movables = board.get_movables(turn, dice)
        print(board.visualize())
        print()
        print("Turn: " + ("R", "G", "B", "Y")[turn] + ", Dice: " + str(dice))
        while True:
            piece_str = input("> ").strip()
            if piece_str == "":
                if len(movables) == 0:
                    break
                else:
                    print("Cannot pass")
            else:
                piece = int(piece_str) - 1
                if piece in movables:
                    board = board.move(piece, turn, dice)
                    count_six = (count_six + 1) % 3 if dice == 6 else 0
                    break
                else:
                    print("Cannot move")
        count_start = (count_start + 1) % 3 if board.is_start(turn) else 0
        if board.is_end(turn):
            break
        if count_six == 0 and count_start == 0:
            turn = (turn + 1) % 4
