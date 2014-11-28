__author__ = 'Petrov'

import Chessboard
import Figures
import Player
import chessGUI


class Game():
    turn = "white"
    board = None
    # player_1 =
    # player_2 =

    def __init__(self):
        self.board = Chessboard.ChessBoard()
        self.turn = "white"

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def check(self, start, end):
        x_from, y_from = start
        x_to, y_to = end
        if self.board.board[y_to][x_to] is None:
            end_figure = Figures.Figure("none") #?
        else:
            end_figure = self.board.board[y_to][x_to]
        if self.board.board[y_from][x_from] is not None:
            if (self.board.board[y_from][x_from].color == self.turn) & (end_figure.color != self.board.board[y_from][x_from].color):
                if isinstance(self.board.board[y_from][x_from], Figures.King):
                    if (abs(x_from - x_to) < 2) & (abs(y_from - y_to) < 2):
                        self.change_turn()
                        return True
                    else:
                        return False

                if isinstance(self.board.board[y_from][x_from], Figures.Queen):
                    if (x_from == x_to) | (y_from == y_to) | ((x_from + y_from == x_to + y_to) | (y_from - x_from == y_to - x_to)):
                        self.change_turn()
                        return True
                    else:
                        return False

                if isinstance(self.board.board[y_from][x_from], Figures.Tower):
                    if (x_from == x_to) | (y_from == y_to):
                        self.change_turn()
                        return True
                    else:
                        return False

                if isinstance(self.board.board[y_from][x_from], Figures.Knight):
                    if (abs(x_from - x_to) == 2) & (abs(y_from - y_to) == 1) | \
                       (abs(x_from - x_to) == 1) & (abs(y_from - y_to) == 2):
                        self.change_turn()
                        return True
                    else:
                        return False

                if isinstance(self.board.board[y_from][x_from], Figures.Pawn):
                    if self.board.board[y_from][x_from].color == "white":
                        if (x_to == x_from) & (y_from - y_to < 3) & (y_from - y_to > 0) & (end_figure.color == "none") & (y_from == 6):
                            self.change_turn()
                            return True
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
                                self.change_turn()
                                return True
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


                if isinstance(self.board.board[y_from][x_from], Figures.Bishop):
                    if (x_from + y_from == x_to + y_to) | (y_from - x_from == y_to - x_to):
                        self.change_turn()
                        return True
                    else:
                        return False