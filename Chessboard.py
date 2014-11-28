__author__ = 'user'

import Figures


class ChessBoard:
    board = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]

    def __init__(self, *args):
        if args == ():
            self['a2'] = Figures.Pawn("white")
            self['b2'] = Figures.Pawn("white")
            self['c2'] = Figures.Pawn("white")
            self['d2'] = Figures.Pawn("white")
            self['e2'] = Figures.Pawn("white")
            self['f2'] = Figures.Pawn("white")
            self['g2'] = Figures.Pawn("white")
            self['h2'] = Figures.Pawn("white")

            self['a1'] = Figures.Tower("white")
            self['b1'] = Figures.Knight("white")
            self['c1'] = Figures.Bishop("white")
            self['d1'] = Figures.Queen("white")
            self['e1'] = Figures.King("white")
            self['f1'] = Figures.Bishop("white")
            self['g1'] = Figures.Knight("white")
            self['h1'] = Figures.Tower("white")

            self['a8'] = Figures.Tower("black")
            self['b8'] = Figures.Knight("black")
            self['c8'] = Figures.Bishop("black")
            self['d8'] = Figures.Queen("black")
            self['e8'] = Figures.King("black")
            self['f8'] = Figures.Bishop("black")
            self['g8'] = Figures.Knight("black")
            self['h8'] = Figures.Tower("black")

            self['a7'] = Figures.Pawn("black")
            self['b7'] = Figures.Pawn("black")
            self['c7'] = Figures.Pawn("black")
            self['d7'] = Figures.Pawn("black")
            self['e7'] = Figures.Pawn("black")
            self['f7'] = Figures.Pawn("black")
            self['g7'] = Figures.Pawn("black")
            self['h7'] = Figures.Pawn("black")

    def __getitem__(self, position):
        x, y = self.convert_position(position)
        return self.board[x][y]

    def __setitem__(self, position, figure):
        x, y = self.convert_position(position)
        self.board[x][y] = figure

    def __str__(self):
        b = ''
        for line in self.board:
            for figure in line:
                if figure is None:
                    b += '░ '  # 20DE
                else:
                    b += str(figure) + ' '
            b += '\n'
        return b

    def move_figure(self, start_position, finish_position):
        if start_position[0] == '0':
            if start_position == '00':
                if finish_position == '00':
                    self.move_figure('e1', 'c1')
                    self.move_figure('a1', 'd1')
                else:
                    self.move_figure('e1', 'g1')
                    self.move_figure('h1', 'f1')
            if start_position == '01':
                if finish_position == '00':
                    self.move_figure('e8', 'c8')
                    self.move_figure('a8', 'd8')
                else:
                    self.move_figure('e8', 'g8')
                    self.move_figure('h8', 'f8')
        else:
            self[finish_position] = self[start_position]
            self[start_position] = None

    def convert_position(self, position):
        letters = "abcdefgh"
        x, y = position
        x, y = letters.index(x), int(y) - 1
        y, x = x, 7 - y
        return x, y

    def convert_position_backwards(self, position):
        letters = "abcdefgh"
        y, x = position
        x, y = 8 - x, letters[y]
        return y, x
