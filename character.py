# !/user/bin/env python
# coding: utf-8

import pygame
from pygame.locals import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os

class Character:
    """Character class"""
    def __init__(self, screen):
        self._charset = {}
        self.load()
        self.screen = screen
        
    def load(self):
        file = os.path.join("data/char.data")
        fp = open(file)
        lines = fp.readlines()
        for line in lines:
            line = line.split()
            self._charset[line[0]] = line[1 : len(line)]
            self._charset[line[0]] = self._charset[line[0]]
            
    def write(self, line, color, pos, size, width):
        for i, char in enumerate(line):
            if char != " ":
                self.render(str(char), color, (size*4*i + pos[0], pos[1]), size, width)
            
    def render(self, char, color, pos, size, width):
        for i, c in enumerate(self._charset[char]):
            if  i < len(self._charset[char]) - 1:
                if self._charset[char][i] != "/" and self._charset[char][i + 1] != "/":
                    p1 = self._charset[char][i].split(",")
                    p2 = self._charset[char][i + 1].split(",")
                    p1 = [int(p1[0])*size + pos[0], int(p1[1])*size + pos[1]]
                    p2 = [int(p2[0])*size + pos[0], int(p2[1])*size + pos[1]]
                    pygame.draw.line(self.screen, color, p1, p2, width)

