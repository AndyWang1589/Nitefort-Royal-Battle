######################################
#Author: Andy Wang
#Description: Class for the walls
#File name: wallClass.py
#Date written: 29/5/18
######################################
class Wall (object):
    def __init__(self, npcCX, npcCY, degree, health):
        self.npcCX, self.npcCY = npcCX, npcCY #centre coordinates of the body that placed the wall
        self.direction = int(degree / 90) % 4 #0 = 0 degrees, 1 = 90, 2 = 180, 3 = 270
        self.health = health

        if self.direction == 0:
            self.x = self.npcCX + WALL_DISTANCE_FROM_BODY
            self.y = self.npcCY - (WALL_LENGTH / 2)
            self.width = WALL_WIDTH
            self.height = WALL_LENGTH
            
        elif self.direction == 1:
            self.x = self.npcCX - (WALL_LENGTH / 2)
            self.y = self.npcCY - WALL_DISTANCE_FROM_BODY - WALL_WIDTH
            self.width = WALL_LENGTH
            self.height = WALL_WIDTH
            
        elif self.direction == 2:
            self.x = self.npcCX - WALL_DISTANCE_FROM_BODY - WALL_WIDTH
            self.y = self.npcCY - (WALL_LENGTH / 2)
            self.width = WALL_WIDTH
            self.height = WALL_LENGTH
            
        else:
            self.x = self.npcCX - (WALL_LENGTH / 2)
            self.y = self.npcCY + WALL_DISTANCE_FROM_BODY
            self.width = WALL_LENGTH
            self.height = WALL_WIDTH

        self.cX = self.x + self.width / 2
        self.cY = self.y + self.height / 2

WALL_DISTANCE_FROM_BODY = 45
WALL_WIDTH = 10 #short side
WALL_LENGTH = 2 * WALL_DISTANCE_FROM_BODY# long side
WALL_HEALTH = 200

walls = []
