__author__ = 'user'

class Figure:
    color = None

    def __init__(self, color):
        self.color = color


class King(Figure):
    def __str__(self):
        return "\u2654" if self.color == "white" else "\u265A"



class Queen(Figure):
    def __str__(self):
        return "\u2655" if self.color == "white" else "\u265B"



class Tower(Figure):
    def __str__(self):
        return "\u2656" if self.color == "white" else "\u265C"



class Bishop(Figure):
    def __str__(self):
        return "\u2657" if self.color == "white" else "\u265D"


class Knight(Figure):
    def __str__(self):
        return "\u2658" if self.color == "white" else "\u265E"



class Pawn(Figure):
    def __str__(self):
        return "\u2659" if self.color == "white" else "\u265F"