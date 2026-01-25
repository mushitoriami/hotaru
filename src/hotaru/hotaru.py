import random


class State:
    def __init__(self) -> None:
        self.board = [[i for i in range(4)] for _ in range(4)]
        self.turn: int | None = 0
        self.winner: int | None = None
        self.dice = random.randint(1, 6)
        self.count_six, self.count_start = 0, 0

    def is_start(self) -> bool:
        return self.turn is not None and set(self.board[self.turn]) == {0, 1, 2, 3}

    def is_end(self) -> bool:
        return self.turn is not None and set(self.board[self.turn]) == {44, 45, 46, 47}

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
                moves.append(i)
        if len(moves) == 0:
            moves.append(None)
        return moves

    def move(self, piece: int | None) -> None:
        if self.turn is not None and piece is not None:
            move_to = (
                self.board[self.turn][piece] + self.dice
                if self.board[self.turn][piece] >= 4
                else 4
            )
            for t in range(4):
                for p in range(4):
                    if is_same_pos(move_to, self.turn, self.board[t][p], t):
                        self.board[t][p] = p
            self.board[self.turn][piece] = move_to
        if piece is not None:
            self.count_six = (self.count_six + 1) % 3 if self.dice == 6 else 0
        self.count_start = (self.count_start + 1) % 3 if self.is_start() else 0
        if self.turn is not None:
            if self.is_end():
                self.winner = self.turn
                self.turn = None
            else:
                if self.count_six == 0 and self.count_start == 0:
                    self.turn = (self.turn + 1) % 4
                self.dice = random.randint(1, 6)

    def eval(self) -> dict[int | None, float]:
        return {move: 0 for move in self.get_movables()}

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
        visualized += "\n"
        if self.turn is not None:
            visualized += (
                "Turn: " + ("R", "G", "B", "Y")[self.turn] + ", Dice: " + str(self.dice)
            )
        elif self.winner is not None:
            visualized += "Winner: " + ("R", "G", "B", "Y")[self.winner]
        else:
            assert False, "unreachable"
        return visualized


def get_absolute_pos(pos: int, turn: int) -> int:
    return (pos - 4 + turn * 10) % 40


def is_same_pos(pos1: int, turn1: int, pos2: int, turn2: int) -> bool:
    if not (4 <= pos1 <= 43 and 4 <= pos2 <= 43):
        return False
    return get_absolute_pos(pos1, turn1) == get_absolute_pos(pos2, turn2)


def cli() -> None:
    state = State()
    while True:
        movables = state.get_movables()
        print(state.visualize())
        while True:
            query = input("> ").split()
            if query[0] in ("move", "pass"):
                piece = int(query[1]) - 1 if query[0] == "move" else None
                if piece in movables:
                    state.move(piece)
                    break
                print("Invalid move")
            else:
                print("Unknown command")
