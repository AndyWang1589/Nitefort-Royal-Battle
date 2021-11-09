######################################
#Author: Andy Wang
#Description: Class for medkit pickups
#File name: medkitClass.py
#Date written: 6/6/18
######################################
import pygame
pygame.init()

class Medkit (object):
    def __init__(self, x, y):
        self.sprite = medkitSprite
        
        self.x = x
        self.y = y

        self.cX = self.x + (self.sprite.get_width() / 2)
        self.cY = self.y + (self.sprite.get_height() / 2)

        self.healAmount = 10

medkitSprite = pygame.image.load("images/sprites/medkit.png")
        
