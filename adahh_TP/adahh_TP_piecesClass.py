from cmu_graphics import *

class Piece:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top 
        self.height = height
        self.width = width
    
    def shift(self, dx):
        self.left -= dx
    