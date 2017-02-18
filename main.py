# !/user/bin/env python
# coding: utf-8

import pygame
from pygame.locals import*
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import random
import math
import datetime

from character import Character
# About Character class：
#   Design with 4*4 grid layout.
#   Rightmost column is for spacing.
from replay import Replay
from crosstest import cross_test

# Initialize modules
SCR_RECT = pygame.Rect(0, 0, 640, 480)
pygame.init()
screen = pygame.display.set_mode(SCR_RECT.size)
pygame.display.set_caption("KOBATO")
surface = pygame.Surface(SCR_RECT.size)
character = Character(screen)
replay = Replay()
# Constant
GRID = 50
CELL = 0
if SCR_RECT[3] <= SCR_RECT[2]:
    CELL = SCR_RECT[3] // 54
else:
    CELL = SCR_RECT[2] // 54
MARGIN_X = (SCR_RECT[2]-GRID*CELL) // 2
MARGIN_Y = (SCR_RECT[3]-GRID*CELL) // 2
GRID_FOR_CHAR = CELL // 2
LIGHT_GRAY = (110, 110, 110)
DARK_GRAY = (50, 50, 50)
GRID_COLOR = (30, 30, 30)
BG_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 0, 100)
GEM_COLOR = (0, 255, 255)
GEM_COLOR_DARK = (0, 80, 80)
ENEMY_COLOR_0 = (255, 255, 0)
DARK_EC0 = (128, 128, 50)
ENEMY_COLOR_1 = (GEM_COLOR)
# Game settings
ENEMIES_LEN = 10
V_LIM = 4
INITIAL_SPAWN_SPAN = 31
MINIMUM_SPAWN_SPAN = 5
INITIAL_LEVEL = 3
CLEAR_LEVEL = 10
GEM_TIME_GAIN = 5
# Sound Files
SE_CLASH = pygame.mixer.Sound(os.path.join("data\se_clash.wav"))
SE_GEM = pygame.mixer.Sound(os.path.join("data\se_gem.wav"))
SE_MOVE = pygame.mixer.Sound(os.path.join("data\se_move.wav"))
SE_INCUBATION = pygame.mixer.Sound(os.path.join("data\se_incubation.wav"))
SE_LEVEL_UP = pygame.mixer.Sound(os.path.join("data\se_level_up.wav"))
BGM = pygame.mixer.music.load(os.path.join("data\kobato.ogg"))
# FROM Grid TO Display
def dX(x):
    return MARGIN_X + x*CELL
def dY(y):
    return MARGIN_Y + y*CELL

# Generate the game
def main():
    game = Game()
    replay.__init__(game)
    game.set_up()

class Game:
    def __init__(self):
        pass
        
    def set_up(self, seed=None):
        '''Initialize game'''
        # Random seed
        if seed == None:
            self.SEED = random.randint(0, 9999)
        else:
            self.SEED = seed
        random.seed(self.SEED)
        # Initialize game settings
        self.waitForInitialInput = True
        self.isRecording = False
        self.enemies = []
        self.gem = Gem()
        self.spawnSpan = INITIAL_SPAWN_SPAN
        self.timeToSpawn = self.spawnSpan
        self.level = INITIAL_LEVEL
        self.player = Player()
        Player.vector = [0, 0]
        Player.pos[0] = GRID // 2
        Player.pos[1] = GRID // 2
        for i in range(ENEMIES_LEN):
            self.enemies.append(None)
        # Initial display
        screen.fill(BG_COLOR)
        self.draw_grid()
        self.update_clock()
        self.player.draw_spawn_point()
        self.update_info_display()
        self.update_gem()
        msg = character.write(
            "KOBATO",PLAYER_COLOR,
            (MARGIN_X + 40, SCR_RECT[3]//2 - CELL),
            GRID_FOR_CHAR, 2)
        attrMsg = (
            "INPUT",
            "R/P  RECORD/PLAYBACK REPLAY",
            "SPACE  CAPTURE SCREEN",
            "ENTER RESET GAME",
            "ESC  EXIT GAME")
        msg = self.attr_msg(attrMsg)
        msg = self.common_msg("PRESS ARROW KEY")
        pygame.display.update()
        ## BGM start
        pygame.mixer.music.play(-1, 0.0)
        # Into the loop
        if seed == None:
            self.phase = "Live"
            self.loop()
    
    def loop(self):
        '''Wait for input.'''
        while True:
            
            if self.phase == "Dead":
                pygame.mixer.music.fadeout(80)
                self.darken()
                msg = self.common_msg("PRESS RETURN TO CONTINUE")
                pygame.display.update()
                pygame.time.wait(80)

            if self.phase == "GameClear":
                for i in range(100):
                    pygame.mixer.music.fadeout(80)
                    self.draw_dia(DARK_GRAY, (dX(Player.pos[0]), dY(Player.pos[1])), i * 30, 1)
                    self.lighten()
                    msg = self.special_msg("CLEAR")
                    pygame.display.update()
                    pygame.time.wait(40)
                replay.close()
                sys.exit()
                
            # input check
            key = pygame.key.get_pressed()
            if self.phase == "Live":
                pygame.time.wait(80)
                if key[K_RIGHT] or key[K_LEFT] or key[K_DOWN] or key[K_UP]:
                    h = key[K_RIGHT] - key[K_LEFT]
                    v = key[K_DOWN] - key[K_UP]
                    # Record replay
                    replay.write(h, v)
                    # Game progress
                    self.update(h, v)
                
            for e in pygame.event.get():
                keyPressed = (e.type == KEYDOWN)
                if e.type == QUIT or (keyPressed and e.key == K_ESCAPE):
                    replay.close()
                    sys.exit()
                if keyPressed and self.waitForInitialInput:
                    # Replay
                    if e.key == K_r:
                        if replay.start():
                            pygame.draw.circle(screen, (255, 0, 0), (10, 10), 5, 0)
                            pygame.display.update()
                    elif e.key == K_p:
                        replay.play()
                    self.waitForInitialInput = False
                if keyPressed and e.key == K_SPACE:
                    name = datetime.datetime.today()
                    name = name.strftime("kobato_%Y_%m_%d_%H_%M_%S")
                    name = str(name)+".png"
                    print(name)
                    img = pygame.image.save(screen, name)
                if keyPressed and e.key == K_RETURN:
                    replay.close()
                    self.set_up()
                    
    def update(self, x, y):
        '''Turn-based process'''
        # SE
        SE_MOVE.play()
        
        # Enemy spawn
        self.enemy_spawn()
        
        # Preprocess
        self.player_stat_check()
        self.player_extend_check()
        
        # Move
        self.update_enemy_vector()
        self.player.move((x, y))
        
        # Cross check
        self.check_cross()
        self.player.bound()
        self.check_cross()
        
        self.update_player_stats()
        
        # Display
        self.update_clock()
        self.darken()
        self.player.update_line()
        self.update_enemy_line()
        self.update_info_display()
        self.update_gem()
        pygame.display.update()
        
        # Clean up
        self.update_position()
        self.reset_player_flags()
        self.clean_enemies()
        self.reset_gems()
        
    def player_stat_check(self):
        if Player.life <= 0:
            self.phase = "Dead"
        if self.level == CLEAR_LEVEL:
            self.phase = "GameClear"
    
    def enemy_spawn(self):
        if self.timeToSpawn < 0:
            # Generate Tobi
            self.spawn_tobi()
            if self.spawnSpan < 0:
                self.spawnSpan = MINIMUM_SPAWN_SPAN
            else:
                self.spawnSpan -= 5
            self.timeToSpawn = self.spawnSpan
            # SE
            SE_INCUBATION.play()
        for enemy in self.enemies:
            if enemy != None and enemy.spawnCount:
                enemy.update_spawn()
        self.timeToSpawn -= 1
    
    def player_extend_check(self):
        if Player.objective <= Player.point:
            Player.life += 1
            Player.objective += 1
            Player.extended = True
            Player.point = 0
            self.level += 1
            # Generate Taka
            self.spawn_taka()
            # SE
            SE_LEVEL_UP.play()
    
    def update_enemy_vector(self):
        for enemy in self.enemies:
            if enemy != None and not enemy.spawnCount:
                enemy.move()
                
    def update_enemy_line(self):
        for enemy in self.enemies:
            if enemy != None and not enemy.spawnCount:
                enemy.update_line()
                
    def update_player_stats(self):
        if Player.crossed:
            Player.life -= 1
        if self.gem.got:
            Player.point += 1
    
    def update_position(self):
        Player.pos[0] += Player.vector[0]
        Player.pos[1] += Player.vector[1]
        for e, enemy in enumerate(self.enemies):
            if enemy != None:
                self.enemies[e].pos[0] += enemy.vector[0]
                self.enemies[e].pos[1] += enemy.vector[1]
                
    def reset_player_flags(self):
        Player.crossed = False
        Player.extended = False
        
    def clean_enemies(self):
        for e, enemy in enumerate(self.enemies):
            if enemy != None and not enemy.alive:
                self.enemies[e] = None
    
    def reset_gems(self):
        if self.gem.got:
            self.timeToSpawn += GEM_TIME_GAIN
            self.gem.__init__()
    
    # Cross test functions
    
    def check_cross(self):
        for e, enemy in enumerate(self.enemies):
            if enemy != None and enemy.vector != [0,0]:
                # Player and enemy
                if self.cross_test_vec(Player.pos, Player.vector, enemy.pos, enemy.vector):
                    Player.crossed = True
                    # SE
                    SE_CLASH.play()
                for ee, exEnemy in enumerate(self.enemies):
                    # Enemy and enemy
                    if ee > e and exEnemy != None and exEnemy.vector != [0, 0]:
                        if self.cross_test_vec(enemy.pos, enemy.vector, exEnemy.pos, exEnemy.vector):
                            if not enemy.shield:
                                enemy.crossed = True
                                self.enemies[e].alive = False
                                # SE
                                SE_CLASH.play()
                            if not exEnemy.shield:
                                exEnemy.crossed = True
                                self.enemies[ee].alive = False
                                # SE
                                SE_CLASH.play()
        # Player and gem
        a = (Player.pos[0]+Player.vector[0], Player.pos[1]+Player.vector[1])
        for p, point in enumerate(self.gem.points):
            # Each edge in gem
            b = (self.gem.points[p - 1][0], self.gem.points[p - 1][1])
            c = (point[0], point[1])
            if cross_test(Player.pos, a, b, c):
                self.gem.got = True
                # SE
                SE_GEM.play()
                        
    def cross_test_vec(self, p1, v1, p2, v2):
        '''Test for cross among vector from p1 toward v1, and p2 toward v2'''
        return cross_test(p1, (p1[0] + v1[0], p1[1] + v1[1]), p2, (p2[0] + v2[0], p2[1] + v2[1]))
    
    # Spawn functions    

    def spawn_tobi(self):
        if None in self.enemies:
            self.enemies[self.enemies.index(None)] = Tobi(self, (GRID // 2, GRID // 2))
            
    def spawn_taka(self):
        if None in self.enemies:
            self.enemies[self.enemies.index(None)] = Taka(self, (GRID // 2, GRID // 2))

    # Draw functions
    
    def draw_grid(self):
        for x in range(GRID):
            pygame.draw.line(
                screen,GRID_COLOR,
                (dX(x), MARGIN_Y),
                (dX(x), SCR_RECT[3] - MARGIN_Y), 1)
        for y in range(GRID):
            pygame.draw.line(
                screen,GRID_COLOR,
                (MARGIN_X, dY(y)),
                (SCR_RECT[2] - MARGIN_X, dY(y)), 1)

    def update_info_display(self):
        # Player life
        r = CELL // 2
        for i in range(Player.life):
            center = (MARGIN_X + r + r*3*i, MARGIN_Y // 2)
            if Player.crossed == True:
                pygame.draw.circle(screen, (255, 255, 255), center, r, 0)
            else:
                pygame.draw.circle(screen, Player.color, center, r, 0)
            if Player.extended == True:
                pygame.draw.circle(screen, (255, 255, 255), center, r*2, 1)            
        # Player point
        center = (SCR_RECT[2] - MARGIN_X - r, MARGIN_Y // 2)
        for i in range(Player.objective):
            self.draw_dia(Gem.colorDark, (center[0] - r*3*i, center[1]), CELL // 2, 0)
        for i in range(Player.point):
            self.draw_dia(Gem.color, (center[0] - r*3*i, center[1]), CELL // 2, 0)
        if Player.extended:
            for i in range(Player.objective):
                self.draw_dia((255, 255, 255), (center[0] - r*3*i, center[1]), CELL, 1)
        # frame
        pygame.draw.rect(screen, GRID_COLOR, ((MARGIN_X, MARGIN_Y), (CELL * GRID, CELL * GRID)), 3)    
        
        # Level information
        gridR = SCR_RECT[2] - MARGIN_X
        gridT = MARGIN_Y
        color = LIGHT_GRAY
        # Line header height
        y = 0
        # Line spacing
        spacing = CELL*2
        # level
        msg = " LEVEL"    
        s = GRID_FOR_CHAR*3 // 4
        x = gridR
        y = gridT-s * 4
        w = 1
        label = character.write(msg, color, (x, y), s, w)
        y += s*4 + spacing
        # level value
        msg = str(self.level)
        s = GRID_FOR_CHAR * 2
        x = gridR + (MARGIN_X - len(msg)*s*4)//2
        w = 3
        label = character.write(msg, color, (x, y), s, w)
        y += s*4 + spacing
        # level objective
        msg = "/ " + str(CLEAR_LEVEL) + " "
        s = GRID_FOR_CHAR*3 // 4
        x = SCR_RECT[2] - len(msg)*s*4
        w = 1
        label = character.write(msg, color, (x, y), s, w)
        
    def draw_dia(self, col, center, size, width):
        pygame.draw.polygon(
            screen, col,
            ((center[0], center[1] - size),
            (center[0] + size, center[1]),
            (center[0], center[1] + size),
            (center[0] - size, center[1])),
            width)
    
    def update_gem(self):
        self.gem.draw()
    
    def update_clock(self):
        self.draw_clock(120, DARK_GRAY)
        self.draw_clock(self.timeToSpawn, DARK_EC0)
    
    def draw_clock(self, deg, col):
        for i in range(deg):
            pygame.draw.line(
                screen, col,
                (math.sin(math.radians(180 + i*-3))*CELL*10 + SCR_RECT[2]//2,
                 math.cos(math.radians(180 + i*-3))*CELL*10 + SCR_RECT[3]//2),
                (math.sin(math.radians(180 + i*-3))*CELL*12 + SCR_RECT[2]//2,
                 math.cos(math.radians(180 + i*-3))*CELL*12 + SCR_RECT[3]//2),
                 1)
    
    def darken(self):
        surface.fill(BG_COLOR)
        surface.set_alpha(80)
        screen.blit(surface,(0, 0))

    def lighten(self):
        surface.fill((255, 255, 255))
        surface.set_alpha(80)
        screen.blit(surface,(0, 0))
    
    def attr_msg(self, msgArray):
        '''Attributes message'''
        size = GRID_FOR_CHAR // 2
        for l, msg in enumerate(msgArray):
            character.write(
                msg, (255, 255, 255),
                (MARGIN_X + 10, MARGIN_Y + 10 + (size+20)*l),
                size, 1)
        
    def common_msg(self, msg):
        '''Common message'''
        size = GRID_FOR_CHAR//4 * 3
        character.write(
            msg, (255, 255, 255),
            ((SCR_RECT[2]-len(msg)*size*4) // 2, SCR_RECT[3]//4 * 3),
            size, 1)

    def special_msg(self, msg):
        '''Special message'''
        size = GRID_FOR_CHAR
        character.write(
            msg, DARK_GRAY,
            ((SCR_RECT[2]-len(msg)*size*4) // 2, SCR_RECT[3]//4 * 1),
            size, 2)

class Anima(object):
    '''Movethings class'''
    def __init__(self):
        self.crossed = False
        self.pos = [0, 0]
        self.vector = [0, 0]
        self.color = (0, 0, 0)
        
    def update_line(self):
        color = self.__class__.color
        if self.crossed == True:
            color = (255, 255, 255)
        self.drawLine(color)
        
    def drawLine(self, color):
        pygame.draw.line(screen, color,
            (dX(self.pos[0]), dY(self.pos[1])),
            (dX(self.pos[0] + self.vector[0]), dY(self.pos[1] + self.vector[1])),
            2)

class Player(Anima):
    '''Player class'''
    def __init__(self):
        # No inherit member vars of Anima class
        Player.color = PLAYER_COLOR
        Player.pos = [0, 0]
        Player.vector = [0, 0]
        Player.point = 0
        # Initial objective
        Player.objective = INITIAL_LEVEL
        # Life limit equals to initial level
        Player.life = INITIAL_LEVEL
        Player.crossed = False
        Player.extended = False
    
    def update_line(self):
        color = self.__class__.color
        if Player.crossed == True:
            color = (255, 255, 255)
        self.drawLine(color)
        
    def draw_spawn_point(self):
        size = CELL // 4
        pygame.draw.rect(
            screen, Player.color,
            (dX(Player.pos[0]) - size, dY(Player.pos[1]) - size,
            size * 2, size * 2), 0)
        pygame.draw.rect(
            screen, Player.color,
            (dX(Player.pos[0]) - size*2, dY(Player.pos[1]) - size*2,
            size * 4, size * 4), 1)
        
    def move(self, vec):
        for i in range(2):
            if V_LIM >= Player.vector[i] + vec[i] >= V_LIM * -1:
                    Player.vector[i] += vec[i]
        
    def bound(self):
        self.update_line()
        for i in range(2):
            if not(GRID >= Player.pos[i] + Player.vector[i] >= 1):
                Player.pos[0] += Player.vector[0]
                Player.pos[1] += Player.vector[1]
                if Player.pos[i] + Player.vector[i] < 1:
                    Player.vector[i] *= -1
                if Player.pos[i] + Player.vector[i] > GRID:
                    Player.vector[i] *= -1
                self.update_line()
                return True
        return False

class Enemy(Anima):
    '''Enemy class'''
    color = (0, 0, 0)
    shield = False
    speedOffset = 0
    def __init__(self, game, spawnPos):
        super(Enemy, self).__init__()
        self.game = game
        self.speed = V_LIM - 1 + self.__class__.speedOffset*2
        self.__class__.speedOffset += 1
        if self.__class__.speedOffset > 2:
            self.__class__.speedOffset = 0
        self.pos = [spawnPos[0], spawnPos[1]]
        self.vector = [0, 0]
        self.alive = True
        # Spawn duration
        self.spawnCountMax = 5
        self.spawnCount = self.spawnCountMax
        # 
        self.update_spawn()
    
    def update_spawn(self):
        SE_INCUBATION.play()
        r = (CELL*self.spawnCount)*2//2 + 2
        pygame.draw.circle(screen, self.__class__.color, (dX(self.pos[0]), dY(self.pos[1])), r, 1)
        self.spawnCount -= 1
        
    def move_to_player(self):
        target = Player.pos + Player.vector
        self.update_pos(target)
    
    def move_to_gem(self):
        target = self.game.gem.pos
        self.update_pos(target)

    def update_pos(self, target):
        for i in range(2):
            if self.pos[i] < target[i]:
                self.vector[i] += 1
            if self.pos[i] > target[i]:
                self.vector[i] -= 1
            if self.vector[i] >= self.speed:
                self.vector[i] -= 1
            if self.vector[i] <= -1 * (self.speed):
                self.vector[i] += 1
    
class Tobi(Enemy):
    '''Tobi class'''
    color = ENEMY_COLOR_0
    shield = False
    def __init__(self, game, spawnPos):
        super(Tobi, self).__init__(game, spawnPos)
    
    def move(self):
        self.move_to_player()
            
class Taka(Enemy):
    '''Taka class'''
    color = ENEMY_COLOR_1
    shield = True
    speedOffset = 0
    def __init__(self, game, spawnPos):
        super(Taka, self).__init__(game, spawnPos)
        
    def move(self):
        self.move_to_gem()
        
class Gem:
    '''Gem class'''
    color = GEM_COLOR
    colorDark = GEM_COLOR_DARK

    def __init__(self):
        self.pos = [0, 0]
        self.got = False
        # shape
        self.vers = ((-2, 0), (0, -2), (2, 0), (0, 2))
        # Shape with grid position
        self.points = []
        self.spawn()

    def spawn(self):
        self.pos[0] = random.randint(1, GRID - 1)
        self.pos[1] = random.randint(1, GRID - 1)
        for ver in self.vers:
            self.points.append([self.pos[0] + ver[0], self.pos[1] + ver[1]])
        self.got = False
        self.draw()
        
    def draw(self):
        c = self.__class__.color
        if self.got == True:
            c = (255, 255, 255)
        pointsDisp = []
        for p, point in enumerate(self.points):
            pointsDisp.append((dX(point[0]), dY(point[1])))
        pygame.draw.circle(screen, c, (dX(self.pos[0]), dY(self.pos[1])), CELL // 3, 1)
        pygame.draw.polygon(screen, c, pointsDisp, 1)


if __name__ == "__main__":
    main()
