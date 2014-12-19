__author__ = 'user'

import pygame
import Chessboard
import Chess
import Figures
import GFigures
import Player
import sys

class GGame(Chess.Game):
    size = width, height = 0, 0
    board = None
    screen = None

    def __init__(self, *args):
        super().__init__()
        pygame.init()
        if args:
            self.size = self.width, self.height = args
        else:
            self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        white = 255, 255, 255
        self.screen.fill(white)

        self.g_chessboard = GChessboard(self.screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_from, y_from = pygame.mouse.get_pos()
                    x_from, y_from = int(x_from / self.g_chessboard.cell_size), \
                                     int(y_from / self.g_chessboard.cell_size)
                if event.type == pygame.MOUSEBUTTONUP:
                    x_to, y_to = pygame.mouse.get_pos()
                    x_to, y_to = int(x_to / self.g_chessboard.cell_size), \
                                 int(y_to / self.g_chessboard.cell_size)
                    if (x_from in range(8)) and (x_to in range(8)) and (y_from in range(8)) and (y_to in range(8)):
                        self.check_and_move((x_from, y_from), (x_to, y_to))
            self.g_chessboard.draw()
            pygame.display.flip()

    def ask_for_figure(self):
        chosen = False
        self.screen.fill((127, 127, 127), (8 * self.g_chessboard.cell_size,
                                           0,
                                           self.g_chessboard.cell_size,
                                           5 * self.g_chessboard.cell_size))
        choice = [GFigures.GPawn(self.turn),
                  GFigures.GTower(self.turn),
                  GFigures.GKnight(self.turn),
                  GFigures.GBishop(self.turn),
                  GFigures.GQueen(self.turn)]
        for i in range(5):
            choice[i].set_size(self.g_chessboard.cell_size, self.g_chessboard.cell_size)
            choice[i].move(8 * self.g_chessboard.cell_size, i * self.g_chessboard.cell_size)
            choice[i].draw(self.screen)
        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x_from, y_from = pygame.mouse.get_pos()
                    x_from, y_from = int(x_from / self.g_chessboard.cell_size), \
                                     int(y_from / self.g_chessboard.cell_size)
                    if (x_from == 8) and (y_from < 6):
                        self.replace_pawn_with(choice[y_from])
                        chosen = True
            pygame.display.flip()




class GChessboard(Chessboard.ChessBoard):
    cell_size = 0
    context = None

    def __init__(self, context):
        super().__init__()
        self.update_board()
        self.context = context
        self.cell_size = int(min(context.get_width() / 9, context.get_height() / 8))

    def draw(self):
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(self.context, (192, 192, 192),
                                     [x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size])
                else:
                    pygame.draw.rect(self.context, (100, 100, 100),
                                     [x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size])
                if self.board[y][x] is not None:
                    self.board[y][x].set_size(self.cell_size, self.cell_size)
                    self.board[y][x].move(x * self.cell_size, y * self.cell_size)
                    self.board[y][x].draw(self.context)

    def update_board(self):
        for i in range(8):
            for j in range(8):
                #ugly
                if isinstance(self.board[i][j], Figures.King):
                    self.board[i][j] = GFigures.GKing(self.board[i][j].color)
                if isinstance(self.board[i][j], Figures.Queen):
                    self.board[i][j] = GFigures.GQueen(self.board[i][j].color)
                if isinstance(self.board[i][j], Figures.Tower):
                    self.board[i][j] = GFigures.GTower(self.board[i][j].color)
                if isinstance(self.board[i][j], Figures.Knight):
                    self.board[i][j] = GFigures.GKnight(self.board[i][j].color)
                if isinstance(self.board[i][j], Figures.Bishop):
                    self.board[i][j] = GFigures.GBishop(self.board[i][j].color)
                if isinstance(self.board[i][j], Figures.Pawn):
                    self.board[i][j] = GFigures.GPawn(self.board[i][j].color)




