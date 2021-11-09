######################################
#Author: Andy Wang
#Description: Class for weapon pickups
#File name: weaponClass.py
#Date written: 29/5/18
######################################
import pygame
import random
pygame.init()
class Weapon(object):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name 

        if self.name == "Handgun":
            self.data = [10, 3, 1, 10, 15, 30, 450] 
            #handgun has no sprite because it's not a weapon drop, it's the default weapon

        elif self.name == "Shotgun":
            self.data = [15, 25, 15, 6, 50, 25, 375]
            self.sprite = weaponSprites[0]

        elif self.name == "Sniper":
            self.data = [20, 0, 1, 42, 90, 60, 600]
            self.sprite = weaponSprites[1]

        elif self.name == "Faster shotgun":
            self.data = [15, 18, 8, 4, 12, 20, 300]
            self.sprite = weaponSprites[2]

        elif self.name == "Pulse gun":
            self.data = [15, 180, 30, 3, 8, 15, 250]
            self.sprite = weaponSprites[3]

        self.bulletSpeed = self.data[0]
        self.bulletOffset = self.data[1]
        self.bulletNum = self.data[2]
        self.bulletDamage = self.data[3]
        self.fireCooldown = self.data[4]
        self.bulletMaxFrames = self.data[5]
        self.shootRange = self.data[6]

        #cX and cY are only made for non-handguns
        if self.name != "Handgun":
            self.cX = self.x + (self.sprite.get_width() / 2)
            self.cY = self.y + (self.sprite.get_height() / 2)

weaponSprites = [pygame.image.load("images/sprites/weapon_shotgun.png"), pygame.image.load("images/sprites/weapon_sniper.png"), pygame.image.load("images/sprites/weapon_faster_shotgun.png"), pygame.image.load("images/sprites/weapon_pulse_gun.png")]
