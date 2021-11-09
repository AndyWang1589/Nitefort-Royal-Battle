###########################################################
#Author: Andy Wang
#Description: Main launcher for Nitefort: Royal Battle
#File name: _nitefort.py
#Date written: 29/5/18
###########################################################
from bulletClass import *
from contestantClasses import *
from wallClass import *
from weaponClass import *
from medkitClass import *

import pygame
from random import randint, choice
from math import *
import time

pygame.init()

#FUNCTIONS===============================================================
#function to draw text
def drawText(window, text, font, x, y, size, colour = (0, 0, 0), antiAlias = True):
    window.blit(pygame.font.SysFont(font, size).render(text, antiAlias, colour), (x, y))

#function to find distance between 2 points
def dist(x, y, x2, y2):
    return sqrt(((x2 - x) ** 2) + ((y2 - y) ** 2))

#function to find angle between two points (returns radians)
def findAngle (x, y, x2, y2):
    dx = x2 - x
    dy = y2 - y

    rads = atan2(-dy, dx)
    rads %= 2 * pi
    return rads + radians(90) #add 90 degrees so that it works with how python calculates trig stuff

#function to see if mouse is inside a button
def inButton (buttonRect): 
    bX = buttonRect[0]
    bY = buttonRect[1]
    bW = buttonRect[2]
    bH = buttonRect[3]
    if mouseX >= bX and mouseX <= bX + bW and mouseY >= bY and mouseY <= bY + bH:
        return True
    return False

#function to find the closest body or pickup to the npc (uses the centre of sprites instead of top left corners)
def closest(npc):
    closest = player #player by default
    for body in contestants:
        if npc != body:
            if dist(npc.cX, npc.cY, body.cX, body.cY) < dist(npc.cX, npc.cY, closest.cX, closest.cY):
                closest = body

    for pickup in pickups:
        if dist(npc.cX, npc.cY, pickup.cX, pickup.cY) < dist(npc.cX, npc.cY, closest.cX, closest.cY):
            closest = pickup

    if dist (npc.cX, npc.cY, closest.cX, closest.cY) <= npc.shootRange:
        return closest
    else:
        return None

#function to draw buttons (w/o text)
def drawButton(baseColour, hoverColour, outlineColour, buttonRect):
    if inButton (buttonRect):
        pygame.draw.rect(screen, hoverColour, buttonRect, FILL_STROKE)
    else:
        pygame.draw.rect(screen, baseColour, buttonRect, FILL_STROKE)

    pygame.draw.rect(screen, outlineColour, buttonRect, THICK_STROKE_2)    

#function to draw the menu screen
def drawMenu():
    screen.blit(menuScreen, ORIGIN)

    #PLAY BUTTON
    drawButton (MENU_BUTTON_CLR, MENU_BUTTON_HOVER_CLR, MENU_BUTTON_OUTLINE_CLR, playButtonRect)
    drawText(screen, "PLAY", "comicsansms", playButtonRect[0] + 25, playButtonRect[1] + 2, 20, MENU_BUTTON_OUTLINE_CLR)

    #INSTRUCTIONS BUTTON
    drawButton (MENU_BUTTON_CLR, MENU_BUTTON_HOVER_CLR, MENU_BUTTON_OUTLINE_CLR, instructionsButtonRect)
    #text
    drawText(screen, "HOW 2 PLAY", "comicsansms", instructionsButtonRect[0] + 5, instructionsButtonRect[1] + 5, 15, MENU_BUTTON_OUTLINE_CLR)

#function to draw instructions
def drawInstructions():
    screen.blit(menuScreen, ORIGIN)

    #THE INSTRUCTIONS
    screen.blit(instructionsImage, (instructionsX, instructionsY))

    #BACK BUTTON
    drawButton (MENU_BUTTON_CLR, MENU_BUTTON_HOVER_CLR, MENU_BUTTON_OUTLINE_CLR, backButtonRect)
    #text
    drawText(screen, "BACK", "comicsansms", backButtonRect[0] + 25, backButtonRect[1] + 2, 20, MENU_BUTTON_OUTLINE_CLR)

#draw graphics of the game
def drawGame():
    screen.fill(BLACK)

    #draw the battlefield
    screen.blit(ground, (groundX, groundY))

    #draw the lake
    screen.blit(lake, (lakeX, lakeY))

    #draw the pickups
    for p in pickups:
        screen.blit(p.sprite, (p.x, p.y))

    #draw the walls
    WALL_HB_LENGTH = 30
    for wall in walls:
        pygame.draw.rect(screen, WALL_CLR, (wall.x, wall.y, wall.width, wall.height), FILL_STROKE)

        #health bar
        pygame.draw.rect(screen, BLACK, (wall.x + (wall.width / 2) - (WALL_HB_LENGTH / 2), wall.y + wall.height + 10, WALL_HB_LENGTH, 3), FILL_STROKE)
        pygame.draw.rect(screen, L_GREEN, (wall.x + (wall.width / 2) - (WALL_HB_LENGTH / 2), wall.y + wall.height + 10, int((float(wall.health) / WALL_HEALTH) * WALL_HB_LENGTH), 3), FILL_STROKE)

    #draw the contestants (player and NPC)
    for contestant in contestants:
        screen.blit(contestant.sprite, (contestant.x, contestant.y))

        if not contestant.isDead:
            #sparkle
            if contestant.spriteIDX == 0:
                screen.blit(contestant.sparkleSprite, (contestant.x - 10, contestant.y + 5))
            elif contestant.spriteIDX == 1:
                screen.blit(contestant.sparkleSprite, (contestant.x - 10, contestant.y - 2))
            else:
                screen.blit(contestant.sparkleSprite, (contestant.x - 10, contestant.y - 10))

            #health bar
            pygame.draw.rect(screen, BLACK, (contestant.x, contestant.y + 50, spriteW, 3), FILL_STROKE)
            pygame.draw.rect(screen, L_GREEN, (contestant.x, contestant.y + 50, int((float(contestant.health) / STARTING_HEALTH) * spriteW), 3), FILL_STROKE)

    #draw all bullets
    for b in bullets:
        bulletCLR = PINK
        if b.npcIndex == playerIndex:
            bulletCLR = CYAN
        pygame.draw.circle(screen, bulletCLR, (b.x, b.y), BULLET_RADIUS, FILL_STROKE)

    #draw the circle
    pygame.draw.circle(screen, WHITE, (circleX, circleY), circleRadius, THICK_STROKE_2)

    #tell which weapon you're holding
    drawText(screen, "Weapon: " + player.weaponHeld.name, "comicsansms", 15, 13, 20, WHITE)

    #display score
    drawText(screen, "Kills: " + str(kills), "comicsansms", 15, 46, 20, WHITE)

    #how many NPCs are left
    drawText(screen, "Enemies left: " + str(NPCsLeft), "comicsansms", 15, 79, 20, WHITE)

    #how many walls are available to build
    drawText(screen, "Walls allowed: " + str(wallsAvailable), "comicsansms", 15, 112, 20, WHITE)

    #display the actual fps
    fpsColour = GREEN

    if realFPS >= 10 and realFPS < 20:
        fpsColour = YELLOW
    elif realFPS < 10:
        fpsColour = RED

    drawText(screen, str(realFPS) + " fps", "consolas", WIDTH - 45, 10, 10, fpsColour)

    #cursor
    CURSOR_RADIUS = 6
    framesPassed = frame - (player.nextWeaponShoot - player.coolDown)
    pygame.draw.arc(screen, L_GREEN, (mouseX - CURSOR_RADIUS, mouseY - CURSOR_RADIUS, CURSOR_RADIUS * 2, CURSOR_RADIUS * 2), 0, radians(360 * (float(framesPassed) / player.coolDown)), THICK_STROKE_2)

#game over screen
def drawGameEnd():
    if isDead:
        screen.blit(gameEndBG, ORIGIN)
    else:
        screen.blit(victoryBG, ORIGIN)

    drawText(screen, "You placed: #" + str(playerRank) + "!", "comicsansms", CENTRE_X - 55, CENTRE_Y - 18, 20, WHITE)

#========================================================================

#VARIABLES AND STUFF================================================================================================================================
WIDTH, HEIGHT = 800, 600
ORIGIN = (0, 0)
CENTRE_X, CENTRE_Y = WIDTH / 2, HEIGHT / 2        

screen = pygame.display.set_mode((800, 600))

mouseX, mouseY = 0, 0

#images, music, and sounds
menuScreen = pygame.image.load("images/nitefort.png")
instructionsImage = pygame.image.load("images/instructions.png")
ground = pygame.image.load("images/ground.png")

gameEndBG = pygame.image.load("images/game_end_bg.png")
victoryBG = pygame.image.load("images/victory_bg.png")

lake = pygame.image.load("images/lake.png")

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.load("audio/the_fortnite_song.mp3")

shootSound = pygame.mixer.Sound("audio/pew_pew.ogg")
shootSound.set_volume(0.2)

buildSound = pygame.mixer.Sound("audio/build.ogg")
buildSound.set_volume(1)

reloadSound = pygame.mixer.Sound("audio/reload.ogg")
reloadSound.set_volume(1)

healSound = pygame.mixer.Sound("audio/heal.ogg")
healSound.set_volume(0.8)

oofSound = pygame.mixer.Sound("audio/oof.ogg")
oofSound.set_volume(0.4)

deathSound = pygame.mixer.Sound("audio/dead.ogg")
deathSound.set_volume(1)

#button and graphics-related coordinates
playButtonRect = (75, (HEIGHT / 2) + 25, 100, 35)
instructionsButtonRect = (75, (HEIGHT / 2) + 85, 100, 35)
backButtonRect = (75, HEIGHT - 110, 100, 35)

instructionsX = 200
instructionsY = 150

groundW = ground.get_width()
groundH = ground.get_height()

groundLeastX = (-groundW + (WIDTH / 2)) + (spriteW / 2)
groundLeastY = -groundH + (HEIGHT / 2) + (spriteH / 2)

groundX = randint(groundLeastX, (WIDTH / 2) - (spriteW / 2))
groundY = randint(groundLeastY, (HEIGHT / 2) - (spriteH / 2))

lakeW = lake.get_width()
lakeH = lake.get_height()
lakeX = randint(groundX, groundX + groundW - lakeW)
lakeY = randint(groundY, groundY + groundH - lakeH)

#objects and object-related variables
NPC_NUM = 49 #number of NPCs you have to fight
HEARING_RANGE = WIDTH / 2 #how far awar you can hear bullet shots

WALK_SPEED = 5
STARTING_HEALTH = 50
LEADING_FACTOR = 8
xSpeed, ySpeed = 0, 0
BULLET_RADIUS = 2

CHOICE_LOWER, CHOICE_UPPER = 10, 60
choiceDelay = randint(CHOICE_LOWER, CHOICE_UPPER)

IDLE_LOWER, IDLE_UPPER = 20, 60
idleLength = randint(IDLE_LOWER, IDLE_UPPER)

NPC_WALK_ANGLE_OFFSET = 120

weaponTypes = ["Shotgun", "Sniper", "Faster shotgun", "Pulse gun"] #types of weapon drops 

STARTING_WEAPON_NUM = 30 #number of weapons scattered at start
STARTING_MEDKIT_NUM = 25 #number of medkits scattered at start
pickups = [Medkit (randint(groundX, groundX + groundW - medkitSprite.get_width()), randint(groundY, groundY + groundH - medkitSprite.get_height())) for counter in range (STARTING_MEDKIT_NUM)] + [Weapon (randint(groundX, groundX + groundW - weaponSprites[0].get_width()), randint(groundY, groundY + groundH - weaponSprites[0].get_height()), choice(weaponTypes)) for counter in range (STARTING_WEAPON_NUM)] #all pickups (weapons, medkits)

WEAPON_DROP_LOWER, WEAPON_DROP_UPPER = 100, 200
weaponDropDelay = randint(WEAPON_DROP_LOWER, WEAPON_DROP_UPPER) #delay in frames between each new drop
nextWeaponDropFrame = weaponDropDelay #next frame on which a pickup is dropped

MEDKIT_DROP_LOWER, MEDKIT_DROP_UPPER = 125, 225
medkitDropDelay = randint(MEDKIT_DROP_LOWER, MEDKIT_DROP_UPPER)
nextMedkitDropFrame = medkitDropDelay

MAX_WALLS = 8 #max number of walls that can exist at the same time (keep it low to prevent lag)
BUILD_DELAY = 10
nextBuildFrame = 0
WALL_DECAY = 4
WALL_DECAY_DELAY = 1

NPC_BUILD_CHANCE = 1 #chance that an npc will build a wall if it detects a bullet coming its way (please set this very low, as to prevent lag :) )

#make all the bodies
handGun = Weapon (0, 0, "Handgun") #default handgun (this will not be drawn, as it is not a drop)
player = Player (CENTRE_X - (spriteW / 2), CENTRE_Y - (spriteH / 2), STARTING_HEALTH, 0, handGun, False)

contestants = [NPC (randint(groundX, groundX + groundW - spriteW), randint(groundY, groundY + groundH - spriteH), WALK_SPEED, randint(0, 360), STARTING_HEALTH, 0, handGun, 0, choiceDelay, idleLength, idleLength, False, 0, False) for c in range (NPC_NUM)] + [player]

#circle properties
CIRCLE_STARTING_RADIUS = int(((groundW * 1.8) / 2))
CIRCLE_MIN_RADIUS = 100
CIRCLE_DECAY_RATE = 2

circleRadius = CIRCLE_STARTING_RADIUS

circleX = randint(groundX + (CIRCLE_STARTING_RADIUS / 2), (groundX + groundH) - (CIRCLE_STARTING_RADIUS / 2))
circleY = randint(groundY + (CIRCLE_STARTING_RADIUS / 2), (groundY + groundH) - (CIRCLE_STARTING_RADIUS / 2))

#colours and line strokes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MENU_BUTTON_CLR = (247, 207, 49)
MENU_BUTTON_HOVER_CLR = (183, 150, 22)
MENU_BUTTON_OUTLINE_CLR = (86, 69, 5)
CYAN = (0, 255, 255)
PINK = (255, 189, 178)
L_GREEN = (196, 255, 170)
WALL_CLR = (214, 171, 53)

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

FILL_STROKE = 0
THICK_STROKE_1 = 1
THICK_STROKE_2 = 2

#player scores and relevant variables
kills = 0
NPCsLeft = NPC_NUM
playerRank = NPC_NUM + 1
wallsAvailable = MAX_WALLS
playerIndex = contestants.index(player)

#boolean about what to draw
menu = True
instructions = False
playGame = False
isDead = False
victory = False
deathMusicPlayed = False
victoryMusicPlayed = False

#variables for basic things needed to run the game
inPlay = True
FPS = 35
realFPS = 0 #actual frames per second
fpsTracker = 0
frame = 0

now = time.time()
timePassed = 0 
clock = pygame.time.Clock()

pygame.mixer.music.play(loops = -1)
#==============================================================================================================================

#MAIN PROGRAM=====================================================================
while inPlay:
    clock.tick(FPS)

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        inPlay = False

    mouseX, mouseY = pygame.mouse.get_pos()

    lakeRect = pygame.Rect(lakeX, lakeY, lakeW, lakeH)

    if menu:
        drawMenu()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #press play button
                if inButton (playButtonRect):
                    menu = False
                    playGame = True
                    pygame.mixer.music.stop()

                #press back button
                elif inButton (instructionsButtonRect):
                    menu = False
                    instructions = True

    elif instructions:
        drawInstructions()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #press back button
                if inButton (backButtonRect):
                    instructions = False
                    menu = True

    elif playGame:
        drawGame()
        if not player.isDead:
            playerIndex = contestants.index(player)

        if not player.isDead:
            #key detection
            if key[pygame.K_w]:
                player.ySpeed = -WALK_SPEED
                
            if key[pygame.K_s]:
                player.ySpeed = WALK_SPEED
                
            if key[pygame.K_a]:
                player.xSpeed = -WALK_SPEED
            
            if key[pygame.K_d]:
                player.xSpeed = WALK_SPEED

            if key[pygame.K_b] and frame > nextBuildFrame and wallsAvailable > 0:
                    nextBuildFrame = frame + BUILD_DELAY
                    degreeToBuild = degrees(findAngle(CENTRE_X, player.y + 23, mouseX, mouseY))
                    player.build(degreeToBuild)
                    wallsAvailable -= 1

                    buildSound.play()

            '''UNCOMMENT THE REGION BELOW FOR A SUPER COOL HAX CHEAT!'''
##            if key[pygame.K_SPACE] and player.health < STARTING_HEALTH:
##                player.health += 1

            #check if player is going out of bounds
            if groundX - player.xSpeed > player.x or (groundX + groundW) - player.xSpeed < player.x + spriteW:
                player.xSpeed = 0
            if groundY - player.ySpeed > player.y or (groundY + groundH) - player.ySpeed < player.y + spriteH:
                player.ySpeed = 0

        #update all contestants
        for idx in range (len(contestants) - 1, -1, -1):
            con = contestants[idx]

            if not con.isDead:
                #body's collision rect
                bodyRect = pygame.Rect(con.x, con.y, spriteW, spriteH)
                
                #check if body picks up a weapon
                for pickupIDX in range (len(pickups) - 1, -1, -1):
                    pickup = pickups[pickupIDX]

                    #pickup's collision rect
                    pickupRect = pygame.Rect(pickup.x, pickup.y, pickup.sprite.get_width(), pickup.sprite.get_height())

                    #check collision between the two
                    if bodyRect.colliderect(pickupRect):
                        if type(pickup) is Weapon: #if the pickup is a weapon
                            if pickup.name != con.weaponHeld.name: #if the pickup is different than the body's weapon
                                con.weaponHeld = pickup
                                pickups.pop(pickupIDX)

                                #only play sound for the player
                                if con == player:
                                    reloadSound.play()
                                    
                        elif type(pickup) is Medkit and con.health < STARTING_HEALTH:
                            con.health += pickup.healAmount

                            #in case body overheals
                            if con.health > 50:
                                con.health = 50
                                
                            pickups.pop(pickupIDX)

                            #only play sound for the player
                            if con == player:
                                healSound.play()

                #check collision with other NPCs
                for other in  contestants:
                    if other != con:
                        otherRect = pygame.Rect(other.x, other.y, spriteW, spriteH / 2)
                        
                        #if moving sideways will collide
                        if otherRect.colliderect(pygame.Rect(con.x + con.xSpeed, con.y, spriteW, spriteH / 2)):
                            con.xSpeed = 0
                            other.xSpeed = 0
                        
                        #if moving up or down will collide
                        if otherRect.colliderect(pygame.Rect(con.x, con.y + con.ySpeed, spriteW, spriteH / 2)):
                            con.ySpeed = 0
                            other.ySpeed = 0

                #check collision with other walls
                if len(walls) > 0: #only do this if there are any walls
                    for wall in walls:
                        wallRect = pygame.Rect(wall.x, wall.y, wall.width, wall.height)
                        
                        #if moving sideways will collide
                        if wallRect.colliderect(pygame.Rect(con.x + con.xSpeed, con.y, spriteW, spriteH)):
                            con.xSpeed = 0
                        
                        #if moving up or down will collide
                        if wallRect.colliderect(pygame.Rect(con.x, con.y + con.ySpeed, spriteW, spriteH)):
                            con.ySpeed = 0
                                
                if con != player:
                    #detect collision with boundaries
                    if con.x + con.xSpeed < groundX or con.x + con.xSpeed > groundX + groundH - spriteW:
                        con.xSpeed = 0

                    if con.y + con.ySpeed < groundY or con.y + con.ySpeed > groundY + groundH - spriteH:
                        con.ySpeed = 0

                    #if they can shoot
                    if frame > con.nextWeaponShoot:
                        con.nextWeaponShoot = frame + con.coolDown
                        
                        bodyToShoot = closest(con)

                        #if bodyToShoot is indeed a body and not a pickup
                        if bodyToShoot in contestants:
                            #lead the target
                            con.shoot(findAngle(con.cX, con.cY, bodyToShoot.cX  + (LEADING_FACTOR * bodyToShoot.xSpeed), bodyToShoot.cY + (LEADING_FACTOR * bodyToShoot.ySpeed)), idx)

                            #if the NPC is within hearing range
                            if dist(CENTRE_X, CENTRE_Y, con.cX, con.cY) <= HEARING_RANGE:
                                shootSound.play()

                    #MOVEMENT RELATED THINGS
                    if frame > con.nextWalkFrame:
                        con.nextWalkFrame = frame + con.walkChoiceDelay
                        con.walkChoiceDelay = randint(CHOICE_LOWER, CHOICE_UPPER)

                        #if the closest thing is a pickup rather than a contestant, go to it
                        closestThing = closest(con)
                        if type(closestThing) is Weapon:
                            if closestThing.name != con.weaponHeld.name: #if it's a different weapon
                                con.walkDegree = degrees(findAngle(con.x, con.y, closestThing.cX, closestThing.cY))

                        elif type(closestThing) is Medkit and con.health < STARTING_HEALTH:
                            con.walkDegree = degrees(findAngle(con.x, con.y, closestThing.cX, closestThing.cY))
                        else:
                            #otherwise walk generally towards the centre of the circle
                            con.walkDegree = degrees(findAngle(con.x, con.y, circleX, circleY)) + randint(-NPC_WALK_ANGLE_OFFSET, NPC_WALK_ANGLE_OFFSET)

                        #update speeds based on degree
                        con.xSpeed = sin(radians(con.walkDegree)) * con.walkSpeed
                        con.ySpeed = cos(radians(con.walkDegree)) * con.walkSpeed

                        con.isIdle = True
                        con.idleLength = randint (IDLE_LOWER, IDLE_UPPER)
                        con.nextIdleFrame = frame + con.idleLength

                    if frame > con.nextIdleFrame and con.isIdle:
                        con.isIdle = False

                #check collision with bullets
                for bulletIDX in range (len(bullets) - 1, -1, -1):
                    bullet = bullets[bulletIDX]

                    bulletRect = pygame.Rect(bullet.x - BULLET_RADIUS, bullet.y - BULLET_RADIUS, BULLET_RADIUS * 2, BULLET_RADIUS * 2)
                    halfBodyRect = pygame.Rect(con.x, con.y, spriteW, spriteH / 2)

                    if bullet.npcIndex != idx: #the following only happens if the bullet was shot by someone else
                        
                        #build wall if bullet is coming (this only applies for NPCs, not player)
                        if wallsAvailable > 0 and con != player and dist(bullet.x + bullet.xSpeed, bullet.y + bullet.ySpeed, con.cX, con.cY) <= con.shootRange / 4 and frame > con.nextBuildFrame:
                            if randint(0, 100) <= NPC_BUILD_CHANCE:
                                degreeToBuild = degrees(findAngle(con.cX, con.cY, bullet.x + bullet.xSpeed, bullet.y + bullet.ySpeed))
                                con.build(degreeToBuild)
                                con.nextBuildFrame = frame + BUILD_DELAY
                                wallsAvailable -= 1

                                #if the NPC is within hearing range
                                if dist(CENTRE_X, CENTRE_Y, con.cX, con.cY) <= HEARING_RANGE:
                                    buildSound.play()
        
                        #if the bullet hits the body
                        if bulletRect.colliderect(halfBodyRect):
                            con.health -= bullet.damage
                            con.indexOfShooter = bullet.npcIndex
                                
                            bullets.pop(bulletIDX)

                            #if the NPC is within hearing range (this plays for the player as well)
                            if dist(CENTRE_X, CENTRE_Y, con.cX, con.cY) <= HEARING_RANGE:
                                oofSound.play()

                con.update() #move sprite

                #if the body runs out of health or is out of the circle
                if con.health <= 0 or dist(con.cX, con.cY, circleX, circleY) >= circleRadius:
                    #if the NPC is within hearing range (this plays for player too)
                    if dist(CENTRE_X, CENTRE_Y, con.cX, con.cY) <= HEARING_RANGE:
                        deathSound.play()

                    #check if player killed the npc
                    if con.indexOfShooter == playerIndex:
                        kills += 1
                        
                    con.isDead = True
            else:
                con.update() #update sprite (contestant's isDead varibale is now true, update() method is changed)
                con.spriteIDX += 1
                con.xSpeed = 0
                con.ySpeed = 0

                #remove contestant from list when death animation is finished
                if con.deathSpriteIDX == len(deathIndeces) - 1:
                    contestants.pop(idx)
                    NPCsLeft -= 1

                    #update each bullet's npcIndex
                    for bulletIDX in range (len(bullets) - 1, -1, -1):
                        bullet = bullets[bulletIDX]
                        if bullet.npcIndex > idx:
                            bullet.npcIndex -= 1

                        #if the npc is dead, remove its bullets
                        elif bullet.npcIndex == idx:
                            bullets.pop(bulletIDX)

                    if not player.isDead:
                        playerRank -= 1 #update player's rank
                        playerIndex = contestants.index(player) #re-find the player

            if idx < playerIndex and (player.xSpeed != 0 or player.ySpeed != 0):
                #move NPC relative to environment
                con.x -= player.xSpeed
                con.y -= player.ySpeed
                
        #shoot gun
        if not player.isDead:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and frame > player.nextWeaponShoot:
                    radian = findAngle(CENTRE_X, CENTRE_Y, mouseX, mouseY)
                    player.shoot(radian, playerIndex)
                    player.nextWeaponShoot = frame + player.coolDown
                    shootSound.play()
        
        #update all bullets
        for index in range (len(bullets) - 1, -1, -1):
            b = bullets[index]
            b.move()

            #move bullets relative to environment
            if player.xSpeed != 0 or player.ySpeed != 0:
                b.x -= player.xSpeed
                b.y -= player.ySpeed

            #remove bullet if it goes out of its range
            if b.framesActive == b.maxFrames:
                bullets.pop(index)

        #add pickups
        if frame > nextWeaponDropFrame:
            nextWeaponDropFrame = frame + weaponDropDelay
            weaponDropDelay = randint (WEAPON_DROP_LOWER, WEAPON_DROP_UPPER)

            pickups.append(Weapon (randint(circleX - circleRadius, circleX + circleRadius), randint(circleY - circleRadius, circleY + circleRadius), choice(weaponTypes)))

        if frame > nextMedkitDropFrame:
            nextMedkitDropFrame = frame + medkitDropDelay
            medkitDropDelay = randint (MEDKIT_DROP_LOWER, MEDKIT_DROP_UPPER)

            pickups.append(Medkit (randint(circleX - circleRadius, circleX + circleRadius), randint(circleY - circleRadius, circleY + circleRadius)))

        #update all pickups
        for idx in range (len(pickups) - 1, -1, -1):
            pickup = pickups[idx]
            
            #move pickups relative to the environment
            if player.xSpeed != 0 or player.ySpeed != 0:
                    pickup.x -= player.xSpeed
                    pickup.y -= player.ySpeed

                    pickup.cX -= player.xSpeed
                    pickup.cY -= player.ySpeed

            #if the pickup happens to be outside of the groun, move it back
            if pickup.x < groundX:
                pickup.x = groundX
            if pickup.x + pickup.sprite.get_width() > groundX + groundW:
                pickup.x = groundX + groundW - pickup.sprite.get_width()

            if pickup.y < groundY:
                pickup.y = groundY
            if pickup.y + pickup.sprite.get_height() > groundY + groundH:
                pickup.y = groundY + groundH - pickup.sprite.get_height()

            #remove pickup if it goes beyond the circle
            if dist(pickup.cX, pickup.cY, circleX, circleY) >= circleRadius:
                pickups.pop(idx)

        #move the walls relative to the player and check collision with bullets
        for wallIndex in range(len(walls) - 1, -1, -1):
            wall = walls[wallIndex]

            if player.xSpeed != 0 or player.ySpeed != 0:
                wall.x -= player.xSpeed
                wall.y -= player.ySpeed
            
            wallCollRect = pygame.Rect(wall.x, wall.y, wall.width, wall.height)

            #bullet collision
            for bulletIndex in range(len(bullets) - 1, -1, -1):
                bullet = bullets[bulletIndex]
                bulletCollRect = pygame.Rect(bullet.x - BULLET_RADIUS, bullet.y - BULLET_RADIUS, BULLET_RADIUS * 2, BULLET_RADIUS * 2)

                if wallCollRect.colliderect(bulletCollRect):
                    wall.health -= bullet.damage
                    bullets.pop(bulletIndex)

            #if wall decays
            if frame % WALL_DECAY_DELAY == 0:
                wall.health -= WALL_DECAY

            #remove wall is it is destroyed (out of health) or is in the lake
            if wall.health <= 0 or lakeRect.colliderect(wallCollRect):
                walls.pop(wallIndex)
                wallsAvailable += 1

        #move the ground relative to the environment
        if player.xSpeed != 0 or player.ySpeed != 0:
            groundX -= player.xSpeed
            groundY -= player.ySpeed

        #move lake relative to environment
        if player.xSpeed != 0 or player.ySpeed != 0:
            lakeX -= player.xSpeed
            lakeY -= player.ySpeed

        #decrease circle radius
        if circleRadius > CIRCLE_MIN_RADIUS:
            circleRadius -= CIRCLE_DECAY_RATE

        #move the circle relative to the environment
        if player.xSpeed != 0 or player.ySpeed != 0:
            circleX -= player.xSpeed
            circleY -= player.ySpeed

        #reset speeds
        player.xSpeed, player.ySpeed = 0, 0

        #check if the player dies (removed from contestants list)
        if not player in contestants:
            if not victory:
                isDead = True

                if not deathMusicPlayed:
                    pygame.mixer.music.load("audio/you_died_original.mp3") #i sped up the original music because pygame keeps playing it slower and at a lower pitch (at least on my laptop. if this isn't the case on yours use you_died_original instead)
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play()
                    deathMusicPlayed = True

        #if you won the game
        elif player in contestants and len(contestants) == 1:
            victory = True
            if not victoryMusicPlayed:
                    pygame.mixer.music.load("audio/victory_original.mp3") #i sped up the original music because pygame keeps playing it slower and at a lower pitch (at least on my laptop. if this isn't the case on yours use victory_original instead)
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play()
                    victoryMusicPlayed = True

    if isDead or victory:
        pygame.event.get()
        drawGameEnd()

    #track the real FPS
    if timePassed == 1.0:
        timePassed = 0
        realFPS = fpsTracker
        fpsTracker = 0
        now = time.time()
    else:
        fpsTracker += 1
        timePassed = round(time.time() - now)
        
    frame += 1
    pygame.display.update()
    
pygame.quit()
#=================================================================================
