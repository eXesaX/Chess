__author__ = 'Petrov'

import Chessboard
import Figures
import History


class Game():
    turn = "white"
    board = None
    #list of cells under strike
    hit_cells = []
    #bools to show that figures never moved (for castle)
    w_king_state = True
    b_king_state = True
    w1_tower_state = True
    w2_tower_state = True
    b1_tower_state = True
    b2_tower_state = True
    #coordinates for pawn that reached last line of the board
    pawn_to_replace = None
    #en passant control
    black_pawns_state = [False, False, False, False, False, False, False, False]
    white_pawns_state = [False, False, False, False, False, False, False, False]

    history = History.History()

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
        self.hit_cells = []
        for x_from in range(8):
            for y_from in range(8):
                for x_to in range(8):
                    for y_to in range(8):
                        if self.board.board[y_from][x_from] is not None:
                            if self.is_under_strike(x_from, y_from, x_to, y_to) and \
                               (self.board.board[y_from][x_from].color != self.turn) and \
                               ((x_from, y_from) != (x_to, y_to)):
                                self.hit_cells.append((x_to, y_to))

    def is_in_check(self, x, y):
        if (x, y) in self.hit_cells:
            return True
        else:
            return False

    def is_current_king_in_check(self):
        is_in_check = False
        for x in range(8):
            for y in range(8):
                if self.board.board[y][x] is not None:
                    if (isinstance(self.board.board[y][x], Figures.King)) and \
                       (self.board.board[y][x].color == self.turn):
                        if self.is_in_check(x, y):
                            is_in_check = True
        return is_in_check

    def check_and_move(self, start, end):  # does rule checking and figure movement
        x_from, y_from = start
        x_to, y_to = end
        if self.board.board[y_to][x_to] is None:
            end_figure = Figures.Figure("none")  # у NoneType нет атрибута color, поэтому создаем виртуальный
        else:
            end_figure = self.board.board[y_to][x_to]
        if self.board.board[y_from][x_from] is not None:
            #figures color checking
            if (self.board.board[y_from][x_from].color == self.turn) and \
               (end_figure.color != self.board.board[y_from][x_from].color):
                #rules checking
                if self.is_able_to_go(x_from, y_from, x_to, y_to) or self.check_for_king(x_from, y_from, x_to, y_to):
                    #movement checking for castle
                    self.detect_first_move(x_from, y_from)
                    start_figure = self.board.board[y_from][x_from]
                    end_figure = self.board.board[y_to][x_to]
                    #actual moving
                    self.board.move_figure(self.board.convert_position_backwards(start),
                                           self.board.convert_position_backwards(end))
                    #acquiring new stricken cells
                    self.find_hit_cells()
                    #checking if king is in check, and if so, returning back to previous board state
                    if self.is_current_king_in_check():
                        self.board.move_figure(self.board.convert_position_backwards(end),
                                               self.board.convert_position_backwards(start))
                    else:  # check for pawns in last line and switch active player
                        self.find_pawn_for_replace()
                        if self.pawn_to_replace is not None:
                            self.ask_for_figure()
                        self.history.add_turn((x_from, y_from, x_to, y_to, start_figure, end_figure))
                        self.change_turn()

    def is_able_to_go(self, x_from, y_from, x_to, y_to):
        return self.check_for_bishop(x_from, y_from, x_to, y_to) or \
               self.check_for_king(x_from, y_from, x_to, y_to) or \
               self.check_for_queen(x_from, y_from, x_to, y_to) or \
               self.check_for_horse(x_from, y_from, x_to, y_to) or \
               self.check_for_tower(x_from, y_from, x_to, y_to) or \
               self.check_for_pawn(x_from, y_from, x_to, y_to)

    def is_under_strike(self, x_from, y_from, x_to, y_to):
        return self.check_for_bishop(x_from, y_from, x_to, y_to) or \
               self.check_for_king_strike(x_from, y_from, x_to, y_to) or \
               self.check_for_queen(x_from, y_from, x_to, y_to) or \
               self.check_for_horse(x_from, y_from, x_to, y_to) or \
               self.check_for_tower(x_from, y_from, x_to, y_to) or \
               self.check_for_pawn_strike(x_from, y_from, x_to, y_to)

    def detect_first_move(self, x_from, y_from):  # for castle control
        if isinstance(self.board.board[y_from][x_from], Figures.King):
            if self.board.board[y_from][x_from].color == "white":
                self.w_king_state = False
            else:
                self.b_king_state = False
        if isinstance(self.board.board[y_from][x_from], Figures.Tower):
            if self.board.board[y_from][x_from].color == "white":
                if x_from == 0:
                    self.w1_tower_state = False
                if x_from == 7:
                    self.w2_tower_state = False
            else:
                if x_from == 0:
                    self.b1_tower_state = False
                if x_from == 7:
                    self.b2_tower_state = False

    def find_pawn_for_replace(self):
        for i in range(0, 8):
            if isinstance(self.board.board[0][i], Figures.Pawn):
                if self.board.board[7][i].color == "white":
                    self.pawn_to_replace = (i, 0)
            if isinstance(self.board.board[7][i], Figures.Pawn):
                if self.board.board[0][i].color == "black":
                    self.pawn_to_replace = (i, 7)

    def replace_pawn_with(self, figure):
        if self.pawn_to_replace is not None:
            x, y = self.pawn_to_replace
            self.board.board[y][x] = figure
            self.pawn_to_replace = None

    def ask_for_figure(self):
        pass

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
                for j in range(min(y_from, y_to) + 1, max(y_from, y_to)):
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
            #usual king movement
            if (abs(x_from - x_to) < 2) and (abs(y_from - y_to) < 2):
                return not self.is_in_check(x_to, y_to)
            #castle
            elif (x_from - x_to == 2) and \
                 (y_from == y_to) and \
                 (self.board.board[y_from][x_from].color == "white") and \
                  self.w_king_state and \
                  self.w1_tower_state and \
                 (self.board.board[7][1] is None) and \
                 (self.board.board[7][3] is None) and \
                 (not self.is_in_check(3, 7)):
                self.board.move_figure(self.board.convert_position_backwards((0, 7)),
                                       self.board.convert_position_backwards((3, 7)))
                return True
            elif (x_to - x_from == 2) and \
                 (y_from == y_to) and \
                 (self.board.board[y_from][x_from].color == "white") and \
                  self.w_king_state and \
                  self.w2_tower_state and \
                 (self.board.board[7][5] is None) and \
                 (not self.is_in_check(5, 7)):
                self.board.move_figure(self.board.convert_position_backwards((7, 7)),
                                       self.board.convert_position_backwards((5, 7)))
                return True
            elif (x_to - x_from == 2) and \
                 (y_from == y_to) and \
                 (self.board.board[y_from][x_from].color == "black") and \
                  self.b_king_state and self.b2_tower_state and \
                 (self.board.board[0][5] is None) and \
                 (not self.is_in_check(0, 7)):
                self.board.move_figure(self.board.convert_position_backwards((7, 0)),
                                       self.board.convert_position_backwards((5, 0)))
                return True
            elif (x_from - x_to == 2) and \
                 (y_from == y_to) and \
                 (self.board.board[y_from][x_from].color == "black") and \
                  self.b_king_state and \
                  self.b1_tower_state and \
                 (self.board.board[0][1] is None) and \
                 (self.board.board[0][3] is None) and \
                 (not self.is_in_check(3, 0)):
                self.board.move_figure(self.board.convert_position_backwards((0, 0)),
                                       self.board.convert_position_backwards((3, 0)))
                return True
            else:
                return False

        else:
            return False

    def check_for_king_strike(self, x_from, y_from, x_to, y_to):
        if isinstance(self.board.board[y_from][x_from], Figures.King):
            if (abs(x_from - x_to) < 2) and (abs(y_from - y_to) < 2):
                return not self.is_in_check(x_to, y_to)
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

    # i am very sorry for this
    def check_for_pawn(self, x_from, y_from, x_to, y_to):
        if self.board.board[y_to][x_to] is None:
            end_figure = Figures.Figure("none")
        else:
            end_figure = self.board.board[y_to][x_to]

        if isinstance(self.board.board[y_from][x_from], Figures.Pawn):
            if self.board.board[y_from][x_from].color == "white":
                #first move, 1 and 2 step move
                if (x_to == x_from) and \
                   (y_from - y_to == 2) and \
                   (end_figure.color == "none") and \
                   (y_from == 6):
                        #obstacles detection
                        allow = True
                        for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                            if self.board.board[i][x_from] is not None:
                                allow = False
                        #en passant control
                        self.white_pawns_state[x_from] = True
                        return allow
                #1 step move
                elif (x_to == x_from) and (y_from - y_to == 1) and (end_figure.color == "none"):
                    self.white_pawns_state[x_from] = False
                    return True
                #en passant
                elif (y_from == 3) and (self.black_pawns_state[x_to]):
                    self.black_pawns_state[x_to] = False
                    self.board.board[y_from][x_to] = None
                    return True
                elif self.check_for_pawn_strike(x_from, y_from, x_to, y_to):
                    return True
                else:
                    return False
            elif self.board.board[y_from][x_from].color == "black":  # same as white
                if (x_to == x_from) and \
                   (y_to - y_from == 2) and \
                   (end_figure.color == "none") and \
                   (y_from == 1):
                        allow = True
                        for i in range(min(y_from, y_to) + 1, max(y_from, y_to)):
                            if self.board.board[i][x_from] is not None:
                                allow = False
                        self.black_pawns_state[x_from] = True
                        return allow
                elif (x_to == x_from) and (y_to - y_from == 1) and (end_figure.color == "none"):
                    self.black_pawns_state[x_from] = False
                    return True
                elif (y_from == 4) and (self.white_pawns_state[x_to]):
                    self.white_pawns_state[x_to] = False
                    self.board.board[y_from][x_to] = None
                    return True
                elif self.check_for_pawn_strike(x_from, y_from, x_to, y_to):
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









