__author__ = 'Petrov'

import Chessboard
import Figures
import Player
import chessGUI


class Game():
    turn = "white"
    board = None

    hit_cells = [
        [False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False],
        ]

    def find_hit_cells(self):
        # for i in range[]
        pass

    def __init__(self):
        self.board = Chessboard.ChessBoard()
        self.turn = "white"

    def change_turn(self):
        pass
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def is_under_strike(self, x_from, y_from, x_to, y_to, end_figure):
        return self.check_for_bishop(x_from, y_from, x_to, y_to) | \
               self.check_for_king(x_from, y_from, x_to, y_to) | \
               self.check_for_queen(x_from, y_from, x_to, y_to) | \
               self.check_for_horse(x_from, y_from, x_to, y_to) | \
               self.check_for_tower(x_from, y_from, x_to, y_to) | \
               self.check_for_pawn(x_from, y_from, x_to, y_to, end_figure)

    def check(self, start, end):
        x_from, y_from = start
        x_to, y_to = end

        if self.board.board[y_to][x_to] is None:
            end_figure = Figures.Figure("none") #?
        else:
            end_figure = self.board.board[y_to][x_to]

        if self.board.board[y_from][x_from] is not None:
            if (self.board.board[y_from][x_from].color == self.turn) & (end_figure.color != self.board.board[y_from][x_from].color):
                return self.is_under_strike(x_from, y_from, x_to, y_to, end_figure)

    def check_for_diags(self, x_from, y_from, x_to, y_to):
        if x_from + y_from == x_to + y_to:
            current_diag = x_from + y_from
            possible_cells = []
            for i in range(min(x_from, x_to) + 1, max(x_from, x_to)):
                for j in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                    if i + j == current_diag:
                        possible_cells.append((i, j))
            allow = True
            for i in range(len(possible_cells)):
                if self.board.board[possible_cells[i][1]][possible_cells[i][0]] is not None:
                    allow = False
            if allow:
                self.change_turn()
            return allow
        elif y_from - x_from == y_to - x_to:
            current_diag = y_from - x_from
            possible_cells = []
            for i in range(min(x_from, x_to) + 1, max(x_from, x_to)):
                for j in range(min(y_from, y_to)  + 1, max(y_from, y_to)):
                    if j - i == current_diag:
                        possible_cells.append((i, j))
            allow = True
            for i in range(len(possible_cells)):
                if self.board.board[possible_cells[i][1]][possible_cells[i][0]] is not None:
                    allow = False
            if allow:
                self.change_turn()
            return allow
        else:
            return False

    def check_for_lines(self, x_from, y_from, x_to, y_to):
        if x_from == x_to:
            allow = True
            for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                if self.board.board[i][x_from] is not None:
                    allow = False
            if allow:
                self.change_turn()
            return allow

        elif y_from == y_to:
            allow = True
            for i in range(min(x_from, x_to) + 1, max(x_from, x_to)):
                if self.board.board[y_from][i] is not None:
                    allow = False
            if allow:
                self.change_turn()
            return allow
        else:
            return False

    def check_for_queen(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Queen):
            if (x_from == x_to) | (y_from == y_to) | \
                    ((x_from + y_from == x_to + y_to) | (y_from - x_from == y_to - x_to)):
                return self.check_for_lines(x_from, y_from, x_to, y_to) | \
                       self.check_for_diags(x_from, y_from, x_to, y_to)

            else:
                return False
        else:
            return False

    def check_for_king(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.King):
            if (abs(x_from - x_to) < 2) & (abs(y_from - y_to) < 2):
                self.change_turn()
                return True
            else:
                return False
        else:
            return False

    def check_for_tower(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Tower):
            if (x_from == x_to) | (y_from == y_to):
                return self.check_for_lines(x_from, y_from, x_to, y_to)
            else:
                return False
        else:
            return False

    def check_for_horse(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Knight):
            if (abs(x_from - x_to) == 2) & (abs(y_from - y_to) == 1) | \
                            (abs(x_from - x_to) == 1) & (abs(y_from - y_to) == 2):
                self.change_turn()
                return True
            else:
                return False
        else: return False

    def check_for_bishop(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Bishop):
            if (x_from + y_from == x_to + y_to) | (y_from - x_from == y_to - x_to):
                return self.check_for_diags(x_from, y_from, x_to, y_to)
            else:
                return False
        else:
            return False

    def check_for_pawn(self, x_from, y_from, x_to, y_to, end_figure):
        if isinstance(self.board.board[y_from][x_from], Figures.Pawn):
            if self.board.board[y_from][x_from].color == "white":
                if (x_to == x_from) & (y_from - y_to < 3) & (y_from - y_to > 0) & (end_figure.color == "none") & (y_from == 6):
                    allow = True
                    for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                        if self.board.board[i][x_from] is not None:
                            allow = False
                    if allow:
                        self.change_turn()
                    return allow
                else:
                    if (x_to == x_from) & (y_from - y_to < 2) & (y_from - y_to > 0) & (end_figure.color == "none"):
                        self.change_turn()
                        return True
                    else:
                        if (abs(x_to - x_from) == 1) & (y_from - y_to == 1) & (end_figure.color == "black"):
                            self.change_turn()
                            return True
                        else:
                            return False
            else:
                if self.board.board[y_from][x_from].color == "black":
                    if (x_to == x_from) & (y_to - y_from < 3) & (y_to - y_from > 0) & (end_figure.color == "none") & (y_from == 1):
                        allow = True
                        for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                            if self.board.board[i][x_from] is not None:
                                allow = False
                        if allow:
                            self.change_turn()
                        return allow
                    else:
                        if (x_to == x_from) & (y_to - y_from < 2) & (y_to - y_from > 0) & (end_figure.color == "none"):
                            self.change_turn()
                            return True
                        else:
                            if (abs(x_to - x_from) == 1) & (y_from - y_to == -1) & (end_figure.color == "white"):
                                self.change_turn()
                                return True
                            else:
                                return False
                else:
                    return False
        else:
            return False











