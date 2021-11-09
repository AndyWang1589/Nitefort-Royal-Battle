######################################
#Author: Andy Wang
#Description: File for NPC and Player classes
#File name: contestantClasses.py
#Date written: 29/5/18
######################################
import pygame
from math import *
from bulletClass import *
from wallClass import *
from random import randint
pygame.init()

class NPC (object):
    def __init__(self, x, y, walkSpeed, walkDegree, health, walkIDX, weaponHeld, nextWalkFrame, walkChoiceDelay, nextIdleFrame, idleLength, isIdle, nextBuildFrame, isDead):
        self.x = x
        self.y = y
        
        self.cX = self.x + (spriteW / 2)
        self.cY = self.y + (spriteH / 2)
        
        self.walkSpeed = walkSpeed
        self.walkDegree = walkDegree
        self.health = health

        self.walkIDX = walkIDX
        self.deathSpriteIDX = 0
        self.spriteIDX = walkIndeces[self.walkIDX]
        
        self.sprite = enemyOrbSprites[self.spriteIDX]
        self.sparkleSprite = enemySparkles[self.spriteIDX]

        self.weaponHeld = weaponHeld
        self.coolDown = self.weaponHeld.fireCooldown
        self.nextWeaponShoot = self.coolDown

        self.shootRange = self.weaponHeld.shootRange
        
        self.nextWalkFrame = nextWalkFrame
        self.walkChoiceDelay = walkChoiceDelay
        
        self.nextIdleFrame = nextIdleFrame
        self.idleLength = idleLength
        self.isIdle = isIdle

        self.isDead = isDead

        self.nextBuildFrame = nextBuildFrame

        self.xSpeed = sin(radians(self.walkDegree)) * self.walkSpeed
        self.ySpeed = cos(radians(self.walkDegree)) * self.walkSpeed

        self.indexOfShooter = 0 #arbitrary value, only used to increase player's kill count

    def update(self):
        if not self.isDead:
            if not self.isIdle:
                self.x += self.xSpeed
                self.y += self.ySpeed
                self.cX = self.x + (spriteW / 2)
                self.cY = self.y + (spriteH / 2)
            else:
                self.nextWalkFrame += 1

            #update the index of the sprite
            self.walkIDX += 1
            self.walkIDX %= len(walkIndeces)
            
            self.spriteIDX = walkIndeces[self.walkIDX]
            
            self.sprite = enemyOrbSprites[self.spriteIDX]
            self.sparkleSprite = enemySparkles[self.spriteIDX]

            #update weapon stats (in case they change)
            self.coolDown = self.weaponHeld.fireCooldown
            self.shootRange = self.weaponHeld.shootRange
            
        else:
            self.spriteIDX = deathIndeces[self.deathSpriteIDX]
            self.sprite = deathSprites[self.spriteIDX]
            self.deathSpriteIDX += 1

    def shoot(self, radian, index):
        for counter in range (self.weaponHeld.bulletNum):
            #add bullet spread
            radianToUse = radian + radians(randint(-self.weaponHeld.bulletOffset, self.weaponHeld.bulletOffset))
            bullets.append(Bullet(self.x + (spriteW / 2), self.y + (spriteH / 2), self.weaponHeld.bulletSpeed, self.weaponHeld.bulletDamage, radianToUse, 0, self.weaponHeld.bulletMaxFrames, index))

    def build(self, degree):
        walls.append(Wall (self.cX, self.cY, degree, WALL_HEALTH))

class Player (object):
    def __init__ (self, x, y, health, walkIDX, weaponHeld, isDead):
        self.x = x
        self.y = y
        self.health = health

        self.xSpeed = 0
        self.ySpeed = 0

        self.cX = self.x + (spriteW / 2)
        self.cY = self.y + (spriteH / 2)
        
        self.walkIDX = walkIDX
        self.deathSpriteIDX = 0
        self.spriteIDX = walkIndeces[walkIDX]
        
        self.sprite = playerOrbSprites[self.spriteIDX]
        self.sparkleSprite = playerSparkles[self.spriteIDX]

        self.weaponHeld = weaponHeld
        self.coolDown = self.weaponHeld.fireCooldown
        self.nextWeaponShoot = self.coolDown

        self.isDead = isDead

    def update(self):
        self.cX = self.x + (spriteW / 2)
        self.cY = self.y + (spriteH / 2)

        if not self.isDead:
            #update the index of the sprite
            self.walkIDX += 1
            self.walkIDX %= len(walkIndeces)

            self.spriteIDX = walkIndeces[self.walkIDX]
            
            self.sprite = playerOrbSprites[self.spriteIDX]
            self.sparkleSprite = playerSparkles[self.spriteIDX]

            #update weapon stats (in case they change)
            self.coolDown = self.weaponHeld.fireCooldown

        else:
            self.spriteIDX = deathIndeces[self.deathSpriteIDX]
            self.sprite = deathSprites[self.spriteIDX]
            self.deathSpriteIDX += 1
            
    def shoot(self, radian, index):
        for counter in range (self.weaponHeld.bulletNum):
            #add bullet spread
            radianToUse = radian + radians(randint(-self.weaponHeld.bulletOffset, self.weaponHeld.bulletOffset))
            bullets.append(Bullet(self.x + (spriteW / 2), self.y + (spriteH / 2), self.weaponHeld.bulletSpeed, self.weaponHeld.bulletDamage, radianToUse, 0, self.weaponHeld.bulletMaxFrames, index))

    def build(self, degree):
        walls.append(Wall (self.cX, self.cY, degree, WALL_HEALTH))
#SPRITES========================================================================================================
playerOrbSprites = [pygame.image.load("images/sprites/player" + str(i) + ".png") for i in range (3)]
playerSparkles = [pygame.image.load("images/sprites/player_sparkle" + str(i) + ".png") for i in range (3)]

enemyOrbSprites = [pygame.image.load("images/sprites/enemy" + str(i) + ".png") for i in range (3)]
enemySparkles = [pygame.image.load("images/sprites/enemy_sparkle" + str(i) + ".png") for i in range (3)]

walkIndeces = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]

spriteW = playerOrbSprites[0].get_width()
spriteH = playerOrbSprites[0].get_height()

#death sprites
deathIndeces = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
deathSprites = [pygame.image.load ("images/sprites/death_sprite" + str(i) + ".png") for i in range (3)]
#===============================================================================================================

