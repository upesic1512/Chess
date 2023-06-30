import pygame
from const import *


class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.inital_row = 0
        self.inital_col = 0

    def update_blit(self,surface):
        self.piece.set_texture(size = 128)
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center)

        surface.blit(img,self.piece.texture_rect)

    def update_mouse(self,pos):
        self.mouseX , self.mouseY = pos
    
    def save_inital(self,pos):
        self.inital_row = pos[1] // SQSIZE
        self.inital_col = pos[0] // SQSIZE

    def dragg_piece(self,piece):
        self.piece = piece
        self.dragging = True

    def undragg_piece(self):
        self.piece = None
        self.dragging = False
