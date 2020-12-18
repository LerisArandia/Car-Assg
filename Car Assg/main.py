import pygame
import sys
from enum import Enum
import math
import random
import time

pygame.init()

# Game Screen
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("GOTTA GO FAST")
clock = pygame.time.Clock()

# Time Variables
timer_started = False
starttime = time.time()
lapsed_time = 0.0

# Game Sounds
pygame.mixer.music.load("./media/background_music.wav")
pygame.mixer.music.play(-1)

car_crash = pygame.mixer.Sound("./media/car_crash.wav")
police_siren = pygame.mixer.Sound("./media/police_siren.wav")

# Text and Fonts
font = pygame.font.Font("./font/Orbitron-VariableFont_wght.ttf", 45)
small_font = pygame.font.Font("./font/Orbitron-VariableFont_wght.ttf", 25)

# Overall Game Speed
game_speed = 1.3
game_speed_change = 0.02

# Background
menu_color = pygame.Color('grey12')
background = pygame.image.load("./media/road.png").convert()
background = pygame.transform.scale(background, (500,600))
background_y_pos = 0

# Road Blocks
coneImg = pygame.image.load("./media/traffic-cone.png")
coneImg = pygame.transform.scale(coneImg, (40,45))
cone = coneImg.get_rect(topleft=(-10,-10))

blocksImg = []
blockX = []
blockY = []
crash_number = 0

for i in range(6):
    blocksImg.append(coneImg)
    blockX.append(random.randint(100,350))
    blockY.append(random.randrange(-1050, -100))

# Police
policeImg = pygame.image.load("./media/police.png")
policeImg = pygame.transform.scale(policeImg, (50, 95))
policeX = 225
policeY = 480

# Player
playerImg = pygame.image.load("./media/car.png")
player_i = playerImg.get_rect(topleft=(350,380))
playerX = 225
playerY = 380
playerX_change = 0
playerY_change = 0

# Functions 
def draw_road():
    screen.blit(background, (0, background_y_pos))
    screen.blit(background, (0, background_y_pos - 600))

def player(x, y):
    player_i.topleft = (x,y)
    screen.blit(playerImg, player_i)

def police(x, y):
    police_i = policeImg.get_rect(topleft=(x,y))
    screen.blit(policeImg, police_i)

def road_block(i, x, y):
    cone.topleft = (x,y)
    screen.blit(blocksImg[i], cone)    

def is_crash(bX, bY):
    global cone, player_i
    
    if cone.colliderect(player_i):
        return True
    else:
        return False

# road block logic
def create_road_block():
    global blockY, crash_number, game_speed, game_speed_change, playerY

    for i in range(len(blocksImg)):
        blockY[i] += game_speed

        if blockY[i] > 600:
            blockY[i] = random.randrange(-1050, -100)
            blockX[i] = random.randint(100, 350)
            game_speed += game_speed_change

        road_block(i, blockX[i], blockY[i])

        crashed = is_crash(blockX[i], blockY[i])
        if crashed:
            car_crash.play()    
            crash_number += 1
            game_speed += 0.3 # increases speed extra
            playerY = 380 # resets player back to infront of police
            blockX[i] = random.randint(100, 350)
            blockY[i] = random.randrange(-1050, -100)

def display_level_text():
    global lapsed_time

    if state is State.menu:
        title_text = font.render(f'GOTTA GO FAST', False, (255,255,255))

        ins_text = pygame.image.load("./media/ins_text.png")
        ins_text_2 = pygame.image.load("./media/ins_text_2.png")

        instructions_text = small_font.render("se" , True, (255,255,255))

        screen.blit(ins_text, (20, 175))
        screen.blit(ins_text_2, (70, 275))
        screen.blit(title_text, (50,75))

    elif state is State.play:

        lapsed_time = (pygame.time.get_ticks() - game_start_time)/1000
        text = small_font.render("Timer: " + str(lapsed_time), True, (255,255,255))

        speed_text = "Speed: {:.1F}".format(game_speed)
        speed_text = small_font.render(speed_text, True, (255,255,255))

        crash_count = "Crash Count: " + str(crash_number)
        crash_count = small_font.render(crash_count, True, (255,255,255))
        
        screen.blit(text, (10,10))
        screen.blit(speed_text, (350,10))
        screen.blit(crash_count, (10,35))

    elif state is State.end:

        final_time = font.render(str(lapsed_time) + "s", False, (255,255,255))
        game_over_text = small_font.render(f"You've been caught!", False, (255,255,255))
        continue_text = small_font.render("Press Enter to Try Again!", False, (255,255,255))

        screen.blit(final_time, (150,75))
        screen.blit(game_over_text, (110, 175))
        screen.blit(continue_text, (75, 200)) 

class State(Enum):
    menu = 1
    play = 2
    end = 3

# Game Loop
state = State.menu
running = True
while running:
    clock.tick(120)

    # Surfaces
    screen.blit(background, (0,0))
    screen.fill((0,0,0))
    background_y_pos += game_speed
    draw_road()

    if background_y_pos >= 600:
        background_y_pos = 0
    
    # Game Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # --------- ALL EVENTS / INPUTS ARE IN HERE -------------
        if event.type == pygame.KEYDOWN:

            if state is not State.menu and state is not State.end:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2.5

                if event.key == pygame.K_RIGHT:
                    playerX_change = 2.5

                if event.key == pygame.K_UP:
                    playerY_change = -2.5

                if event.key == pygame.K_DOWN:
                    playerY_change = 2.5

            elif state is State.menu or state is State.end:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # Check for any user input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        state = State.play
                        timer_started = True
                        game_start_time = pygame.time.get_ticks()
                            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0


    # ----------- STATE CONTROL -----------

    if state is State.play:

        if crash_number == 3:
            police_siren.play()
            state = State.end

        create_road_block()

    elif state is State.end:

        # Reset game vars for new game
        playerX = 225
        playerY = 380
        crash_number = 0
        game_speed = 1.3

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        state = State.play
                        

    # --------- Blit Characters -----------

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 100:
        playerX = 100
    elif playerX >= 350:
        playerX = 350
    elif playerY <= 0:
        playerY = 0
    elif playerY >= 405:
        police_siren.play()
        state = State.end

    player(playerX, playerY)
    police(playerX, policeY) # keeps the police car in line with the player
    display_level_text()

    pygame.display.update()