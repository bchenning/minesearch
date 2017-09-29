# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 22:06:35 2017

@author: Benny
"""

import random as rnd


def printField(field):
    '''printField printes the Minesweeperfield'''
    
    for row in range(len(field)):
        print()
        for col in range(len(field[0])):
            print(field[row][col], end = "")

class Field:
    '''Field is a class for gameboards specially for Minesweeper'''
    def __init__(self, height, width, p):
        self.height     = height
        self.width      = width
        self.p          = p
        self.emptyfield = self.generateField()
        self.solution   = self.mineplanting()
        self.generateSolution()
        
        
        
    def generateField(self):
        '''generateField generates an empty (with 0 filled) Field'''

        gamefield = [[0 for x in range(self.width)] for y in range(self.height)]
            
        return gamefield

    
    def mineplanting(self):
        """mineplanting platziert zufaellig Minen auf ein Feld"""

        minelist = []
        
        while len(minelist) < self.p:
            mine_x = rnd.randint(0, self.width-1)
            mine_y = rnd.randint(0, self.height-1)
            if not (mine_x, mine_y) in minelist:
                minelist.append( (mine_x, mine_y) )
    
        field = [["*" if (x,y) in minelist else 0 for x in range(self.width)] for y in range(self.height)]
            
        return field
        
        
    
    def generateSolution(self):
        """generateSolution generiert die Lösung zu einem Spielfeld"""

        for y in range(self.height):
            for x in range(self.width):
                if self.solution[y][x] != '*':
                    if y == 0:               h = (0, 1)
                    elif y == self.height-1: h = (0,-1)
                    else:                    h = (-1,0,1)

                    if x == 0:               b = (0, 1)
                    elif x == self.width-1:  b = (0,-1)
                    else:                    b = (-1,0,1)

                    for i in h:
                        for j in b:
                            if self.solution[y+i][x+j] == '*':
                                self.solution[y][x] += 1

                    if self.solution[y][x] == 0: self.solution[y][x] = '.'


if __name__ == "__main__":
    gameBoard = Field(5, 10, 5)
    printField(gameBoard.emptyfield)
    print("\n")
    printField(gameBoard.solution)
