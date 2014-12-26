__author__ = 'user'

import Figures

class History():
    turns = []
    current_turn = 0

    def __init__(self):
        self.current_turn = 0
        self.turns = []

    def add_turn(self, coords):
        if self.current_turn == len(self.turns):
            self.turns.append(coords)
            self.current_turn = len(self.turns)
        else:
            for i in range(len(self.turns) - self.current_turn):
                self.turns.pop()
            self.turns.append(coords)
            self.current_turn = len(self.turns)

    def get_prev_turn(self):
        if self.current_turn > 0:
            self.current_turn -= 1
            return self.turns[self.current_turn]
        else:
            return None

    def get_next_turn(self):
        if self.current_turn < len(self.turns):
            self.current_turn += 1
            return self.turns[self.current_turn]
        else:
            return None

    def get_last_10_as_notation(self):
        if len(self.turns) > 0:
            notation = []
            for turn in self.turns[-10:]:
                castle = False
                x_from, y_from, x_to, y_to, start_figure, end_figure = turn
                a, b = self._convert_position_backwards((x_from, y_from))
                c, d = self._convert_position_backwards((x_to, y_to))
                pos1 = str(a) + str(b)
                pos2 = str(c) + str(d)
                figure = ''
                if isinstance(start_figure, Figures.King):
                    if (x_from - x_to) < 0 and (abs(x_from - x_to) != 1):
                        castle = True
                        figure = '0-0'
                    elif (x_from - x_to > 0) and (abs(x_from - x_to) != 1):
                        castle = True
                        figure = '0-0-0'
                    else:
                        figure = 'K'
                if isinstance(start_figure, Figures.Queen):
                    figure = 'Q'
                if isinstance(start_figure, Figures.Tower):
                    figure = 'R'
                if isinstance(start_figure, Figures.Knight):
                    figure = 'N'
                if isinstance(start_figure, Figures.Bishop):
                    figure = 'B'
                if isinstance(start_figure, Figures.Pawn):
                    figure = 'p'
                if not castle:
                    if end_figure is None:
                        dot = '-'
                    else:
                        dot = 'x'
                    notation.append(figure + pos1 + dot + pos2)
                else:
                    notation.append(figure)
                # print(notation)
            return notation
        else:
            return ['..']

    def _convert_position_backwards(self, position):
        letters = "abcdefgh"
        y, x = position
        x, y = 8 - x, letters[y]
        return y, x



