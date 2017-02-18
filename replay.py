# !/user/bin/env python
# coding: utf-8

import pygame
from pygame.locals import*
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import math
import datetime

import glob

class Replay:
    '''Replay class'''
    def __init__(self, game=None):
        self.game = game
    
    def start(self):
        if not self.game.isRecording and self.game.waitForInitialInput:
            self.game.isRecording = True
            # Generate replay log file
            if not os.path.exists("replay"):
                os.mkdir("replay")
            self.fileName = datetime.datetime.today()
            self.fileName = self.fileName.strftime("replay/kobato_replay_%Y_%m_%d_%H_%M_%S")
            self.fileName = str(self.fileName)+".txt"
            self.f = open(self.fileName, 'w')
            self.f.write(str(self.game.SEED)+"\n")
            self.f.close()
            self.f = open(self.fileName, 'a')
            self.writeSpan = 20
            self.writeCount = 0
            print "Replay start"
            return True
        
    def write(self, x, y):
        if self.game.isRecording and not self.game.waitForInitialInput:
            self.f.write(str(x)+" "+str(y)+"\n")
            if self.writeCount >= self.writeSpan:
                self.f.close()
                self.f = open(self.fileName, 'a')
                print "Replay saved"
                self.writeCount = 0
            self.writeCount += 1
            
    def close(self):
        if self.game.isRecording and not self.game.waitForInitialInput:
            self.f.close()
            print "Replay saved"
    
    def play(self):
        if(glob.glob("replay/*.txt")):
            # TODO: Format check
            fName = glob.glob("replay/*.txt")[0]
            f = open(fName, 'r')
            inputList = []
            lines = f.readlines()
            seed = int(lines.pop(0))
            for line in lines:
                line = line.split()
                inputList.append((int(line[0]), int(line[1])))
            self.game.set_up(seed)
            for playerInput in inputList:
                self.game.update(playerInput[0], playerInput[1])
                pygame.time.wait(80)
                self.get_return_key()
            while True:
                pygame.mixer.music.fadeout(80)
                msg = self.game.common_msg("PRESS RETURN AND EXIT REPLAY")
                pygame.display.update()
                self.get_return_key()
                
    def get_return_key(self):
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_RETURN:
                self.game.set_up()
