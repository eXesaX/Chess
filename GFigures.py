__author__ = 'user'

import Figures
import pygame
import os


class GFigure(Figures.Figure):
    pict = None
    rect = None

    def __init__(self, color):
        super().__init__(color)
        self.load_image()
        self.pict.convert()
        self.pict.set_colorkey((255, 0, 255))
        self.rect = self.pict.get_rect()

    def load_image(self):
        pass

    def draw(self, context):
        context.blit(self.pict, self.rect)

    def set_size(self, width, height):
        self.pict = pygame.transform.scale(self.pict, (width, height))
        self.rect = self.pict.get_rect()

    def move(self, x_to, y_to):
        self.rect.move_ip(x_to, y_to)


class GKing(Figures.King, GFigure):

    def load_image(self):
        if self.color == "white":
            self.pict = pygame.image.load(os.path.join('resources', 'king_w.bmp'))
        else:
            self.pict = pygame.image.load(os.path.join('resources', 'king.bmp'))


class GQueen(Figures.Queen, GFigure):
    def load_image(self):
        if self.color == "white":
            self.pict = pygame.image.load(os.path.join('resources', 'queen_w.bmp'))
        else:
            self.pict = pygame.image.load(os.path.join('resources', 'queen.bmp'))


class GTower(Figures.Tower, GFigure):
    def load_image(self):

        if self.color == "white":
            self.pict = pygame.image.load(os.path.join('resources', 'rook_w.bmp'))
        else:
            self.pict = pygame.image.load(os.path.join('resources', 'rook.png'))


class GBishop(Figures.Bishop, GFigure):
    def load_image(self):
        if self.color == "white":
            self.pict = pygame.image.load(os.path.join('resources', 'bishop_w.bmp'))
        else:
            self.pict = pygame.image.load(os.path.join('resources', 'knight.png'))


class GKnight(Figures.Knight, GFigure):
    def load_image(self):
        if self.color == "white":
            self.pict = pygame.image.load(os.path.join('resources', 'horse_w.bmp'))
        else:
            self.pict = pygame.image.load(os.path.join('resources', 'horse.bmp'))


class GPawn(Figures.Pawn, GFigure):
    def load_image(self):
        if self.color == "white":
            self.pict = pygame.image.load(os.path.join('resources', 'pawn_w.bmp'))
        else:
            self.pict = pygame.image.load(os.path.join('resources', 'pawn.bmp'))
