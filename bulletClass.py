######################################
#Author: Andy Wang
#Description: Class for the bullets
#File name: bulletClass.py
#Date written: 29/5/18
######################################
from math import *
from random import randint
class Bullet(object):
    def __init__(self, x, y, speed, damage, radian, framesActive, maxFrames, npcIndex):
        self.x = int(x)
        self.y = int(y)
        self.speed = speed
        self.damage = damage
        self.radian = radian
        self.framesActive = framesActive
        self.maxFrames = maxFrames
        self.npcIndex = npcIndex

        self.xSpeed = int(sin(self.radian) * self.speed)
        self.ySpeed = int(cos(self.radian) * self.speed)

    def move(self):
        self.x += self.xSpeed
        self.y += self.ySpeed

        self.framesActive += 1

#list of all bullets
bullets = []
