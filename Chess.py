__author__ = 'Petrov'

import Chessboard
import Figures
import Player
import chessGUI


class Game():
    turn = "white"
    board = None
    hit_cells = []

    def __init__(self):
        self.board = Chessboard.ChessBoard()
        self.turn = "white"

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
            self.find_hit_cells()

    def find_hit_cells(self):
        # тут я понял, что наверное было бы лучше возвращать списки возможных ходов в check_for_...(),
        # но т.к. почти всю структуру проверки придется переделывать... то так:
        self.hit_cells = []
        for x_from in range(8):
            for y_from in range(8):
                for x_to in range(8):
                    for y_to in range(8):
                        if self.board.board[y_from][x_from] is not None:
                            if self.is_under_strike(x_from, y_from, x_to, y_to) and \
                               (self.board.board[y_from][x_from].color != self.turn):
                                self.hit_cells.append((x_to, y_to))

    def is_in_check(self, x, y):
        if (x, y) in self.hit_cells:
            return True
        else:
            return False

    def check(self, start, end):
        x_from, y_from = start
        x_to, y_to = end
        if self.board.board[y_to][x_to] is None:
            end_figure = Figures.Figure("none")  # у NoneType нет атрибута color, поэтому создаем виртуальный
        else:
            end_figure = self.board.board[y_to][x_to]
        if self.board.board[y_from][x_from] is not None:
            if (self.board.board[y_from][x_from].color == self.turn) and \
               (end_figure.color != self.board.board[y_from][x_from].color):
                can_go = self.is_able_to_go(x_from, y_from, x_to, y_to)
                if can_go:
                    self.change_turn()
                return can_go

    def is_able_to_go(self, x_from, y_from, x_to, y_to):
        return self.check_for_bishop(x_from, y_from, x_to, y_to) or \
               self.check_for_king(x_from, y_from, x_to, y_to) or \
               self.check_for_queen(x_from, y_from, x_to, y_to) or \
               self.check_for_horse(x_from, y_from, x_to, y_to) or \
               self.check_for_tower(x_from, y_from, x_to, y_to) or \
               self.check_for_pawn(x_from, y_from, x_to, y_to)

    def is_under_strike(self, x_from, y_from, x_to, y_to):
        return self.check_for_bishop(x_from, y_from, x_to, y_to) or \
               self.check_for_king(x_from, y_from, x_to, y_to) or \
               self.check_for_queen(x_from, y_from, x_to, y_to) or \
               self.check_for_horse(x_from, y_from, x_to, y_to) or \
               self.check_for_tower(x_from, y_from, x_to, y_to) or \
               self.check_for_pawn_strike(x_from, y_from, x_to, y_to)

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
            return allow
        else:
            return False

    def check_for_lines(self, x_from, y_from, x_to, y_to):
        if x_from == x_to:
            allow = True
            for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                if self.board.board[i][x_from] is not None:
                    allow = False
            return allow

        elif y_from == y_to:
            allow = True
            for i in range(min(x_from, x_to) + 1, max(x_from, x_to)):
                if self.board.board[y_from][i] is not None:
                    allow = False
            return allow
        else:
            return False

    def check_for_queen(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Queen):
            return self.check_for_lines(x_from, y_from, x_to, y_to) or \
                   self.check_for_diags(x_from, y_from, x_to, y_to)
        else:
            return False

    def check_for_king(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.King):
            if (abs(x_from - x_to) < 2) and (abs(y_from - y_to) < 2):
                return not self.is_in_check(x_to, y_to)
            else:
                return False
        else:
            return False

    def check_for_tower(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Tower):
            if (x_from == x_to) or (y_from == y_to):
                return self.check_for_lines(x_from, y_from, x_to, y_to)
            else:
                return False
        else:
            return False

    def check_for_horse(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Knight):
            if (abs(x_from - x_to) == 2) and (abs(y_from - y_to) == 1) or \
               (abs(x_from - x_to) == 1) and (abs(y_from - y_to) == 2):
                return True
            else:
                return False
        else:
            return False

    def check_for_bishop(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Bishop):
            return self.check_for_diags(x_from, y_from, x_to, y_to)
        else:
            return False

    def check_for_pawn(self, x_from, y_from, x_to, y_to):
        if self.board.board[y_to][x_to] is None:
            end_figure = Figures.Figure("none") #?
        else:
            end_figure = self.board.board[y_to][x_to]

        if isinstance(self.board.board[y_from][x_from], Figures.Pawn):
            if self.board.board[y_from][x_from].color == "white":
                if (x_to == x_from) & (y_from - y_to < 3) and (y_from - y_to > 0) and (end_figure.color == "none") and (y_from == 6):
                    allow = True
                    for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                        if self.board.board[i][x_from] is not None:
                            allow = False
                    return allow
                else:
                    if (x_to == x_from) and (y_from - y_to < 2) and (y_from - y_to > 0) and (end_figure.color == "none"):
                        return True
                    else:
                        if (abs(x_to - x_from) == 1) and (y_from - y_to == 1) and (end_figure.color == "black"):
                            return True
                        else:
                            return False
            else:
                if self.board.board[y_from][x_from].color == "black":
                    if (x_to == x_from) and (y_to - y_from < 3) and (y_to - y_from > 0) and (end_figure.color == "none") and (y_from == 1):
                        allow = True
                        for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                            if self.board.board[i][x_from] is not None:
                                allow = False
                        return allow
                    else:
                        if (x_to == x_from) and (y_to - y_from < 2) and (y_to - y_from > 0) and (end_figure.color == "none"):
                            return True
                        else:
                            if (abs(x_to - x_from) == 1) and (y_from - y_to == -1) and (end_figure.color == "white"):
                                return True
                            else:
                                return False
                else:
                    return False
        else:
            return False

    def check_for_pawn_strike(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.Pawn):
            if self.board.board[y_from][x_from].color == "white":
                if (abs(x_to - x_from) == 1) and (y_from - y_to == 1):
                    return True
                else:
                    return False
            else:
                if self.board.board[y_from][x_from].color == "black":
                    if (abs(x_to - x_from) == 1) and (y_from - y_to == -1):
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False









