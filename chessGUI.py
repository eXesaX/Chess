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


    def __init__(self, *args):
        super().__init__()
        pygame.init()
        if args:
            self.size = self.width, self.height = args
        else:
            self.size = self.width, self.height = 800, 600
        screen = pygame.display.set_mode(self.size)
        white = 255, 255, 255
        screen.fill(white)

        self.g_chessboard = GChessboard(screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_from, y_from = pygame.mouse.get_pos()
                    x_from, y_from = int(x_from / self.g_chessboard.cell_size), int(y_from / self.g_chessboard.cell_size)
                    start = self.g_chessboard.convert_position_backwards((x_from, y_from))
                if event.type == pygame.MOUSEBUTTONUP:
                    x_to, y_to = pygame.mouse.get_pos()
                    x_to, y_to = int(x_to / self.g_chessboard.cell_size), int(y_to / self.g_chessboard.cell_size)
                    end = self.g_chessboard.convert_position_backwards((x_to, y_to))
                    if (self.check((x_from, y_from), (x_to, y_to))):
                        self.g_chessboard.move_figure(start, end)
            #drawing code here
            self.g_chessboard.draw()

            pygame.display.flip()


class GChessboard(Chessboard.ChessBoard):
    cell_size = 0
    context = None

    def __init__(self, context):
        super().__init__()
        self.update_board()
        self.context = context
        self.cell_size = int(min(context.get_width(), context.get_height()) / 8)

    def draw(self):
        # self.update_board()
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




