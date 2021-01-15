# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 22:03:49 2017

@author: Benny Christian Henning

"""

from minesearch import field
from os.path import dirname, abspath
import pygame


def main():
    """Start the MineSearch game."""
    # interpretieren der Map zur Darstellung der richtigen Tiles
    tile_dir_path = dirname(abspath(__file__)) + "/Tiles/"
    tile_dic = {
        '*': pygame.image.load(tile_dir_path + "MINESWEEPER_M.png"),
        '.': pygame.image.load(tile_dir_path + "MINESWEEPER_X.png"),
        0: pygame.image.load(tile_dir_path + "MINESWEEPER_0.png"),
        1: pygame.image.load(tile_dir_path + "MINESWEEPER_1.png"),
        2: pygame.image.load(tile_dir_path + "MINESWEEPER_2.png"),
        3: pygame.image.load(tile_dir_path + "MINESWEEPER_3.png"),
        4: pygame.image.load(tile_dir_path + "MINESWEEPER_4.png"),
        5: pygame.image.load(tile_dir_path + "MINESWEEPER_5.png"),
        6: pygame.image.load(tile_dir_path + "MINESWEEPER_6.png"),
        7: pygame.image.load(tile_dir_path + "MINESWEEPER_7.png"),
        8: pygame.image.load(tile_dir_path + "MINESWEEPER_8.png"),
        'f': pygame.image.load(tile_dir_path + "MINESWEEPER_F.png")
    }

    # Initialisierungsphase
    pygame.font.init()
    pygame.init()
    myfont = pygame.font.Font(pygame.font.get_default_font(), 35)
    myfont.set_bold(True)

    print("Bitte geben Sie die gewuenschte Feldgroesse ein")
    height = int(input("Hoehe:    "))
    width = int(input("Breite:   "))
    p = input("""Bitte geben Sie die gewuenschte Anzahl an Minen ein:
             (Fuer default: Enter druecken).\n""")
    try:
        p = int(p)
    except ValueError:
        p = (height*width)//7
        print(p)

    gameBoard = field.Field(height, width, p)
    tilesize = 72
    mapheight = gameBoard.height
    mapwidth = gameBoard.width

    gameDisplay = pygame.display.set_mode(
        (mapwidth * tilesize, mapheight * tilesize)
    )

    pygame.display.set_caption("Minesweeper")

    clock = pygame.time.Clock()

    timer = 0
    dt = 0

    solution = gameBoard.solution
    gamefield = gameBoard.emptyfield

    laeuft = True
    # Ende der Initialisierungsphase

    # Funktionenbereich
    def check(x, y):
        """Checks what """
        if x == 0:
            b = (0, 1)
        elif x == gameBoard.width-1:
            b = (0, -1)
        else:
            b = (-1, 0, 1)
        if y == 0:
            h = (0, 1)
        elif y == gameBoard.height-1:
            h = (0, -1)
        else:
            h = (-1, 0, 1)

        gameBoard.emptyfield[y][x] = gameBoard.solution[y][x]

        for i in h:
            for j in b:
                if gameBoard.solution[y+i][x+j] != '.':
                    gameBoard.emptyfield[y+i][x+j] = gameBoard.solution[y+i][x+j]
                elif (gameBoard.solution[y+i][x+j] == '.' and
                        not (
                            gameBoard.emptyfield[y+i][x+j] ==
                            gameBoard.solution[y+i][x+j])):
                    gameBoard.emptyfield[y+i][x+j] = gameBoard.solution[y+i][x+j]
                    check(x+j, y+i)

    def leftClick(x, y):
        """React to an click of the left mouse button."""
        if gameBoard.emptyfield[y][x] == 'f':
            return True
        elif gameBoard.solution[y][x] == "*":
            gameBoard.emptyfield = gameBoard.solution
            return False
        elif gameBoard.solution[y][x] == '.':
            check(x, y)
            return True
        else:
            gameBoard.emptyfield[y][x] = gameBoard.solution[y][x]
            return True

    def doubleclick(x, y):
        """React to a double click of the left mouse button."""
        if x == 0:
            b = (0, 1)
        elif x == gameBoard.width-1:
            b = (0, -1)
        else:
            b = (-1, 0, 1)
        if y == 0:
            h = (0, 1)
        elif y == gameBoard.height-1:
            h = (0, -1)
        else:
            h = (-1, 0, 1)

        anzahl = 0

        for i in h:
            for j in b:
                if gameBoard.emptyfield[y+i][x+j] == 'f':
                    anzahl += 1

        if anzahl == gameBoard.emptyfield[y][x]:
            for i in h:
                for j in b:
                    if gameBoard.emptyfield[y+i][x+j] != 'f':
                        gameBoard.emptyfield[y+i][x+j] = gameBoard.solution[y+i][x+j]
                        if gameBoard.solution[y+i][x+j] == '.':
                            check(x+j, y+i)
                        if gameBoard.solution[y+i][x+j] == '*':
                            return False

        return True

    def rightClick(x, y):
        """React to a click of the right mouse button."""
        if gameBoard.emptyfield[y][x] != gameBoard.solution[y][x]:
            if gameBoard.emptyfield[y][x] != 'f':
                gameBoard.emptyfield[y][x] = 'f'
            else:
                gameBoard.emptyfield[y][x] = 0

    def endcheck():
        """Return, if the has won the game."""
        win = [
            [False for i in range(gameBoard.width)]
            for j in range(gameBoard.height)]

        for i in range(gameBoard.height):
            for j in range(gameBoard.width):
                if gameBoard.emptyfield[i][j] == gameBoard.solution[i][j]:
                    win[i][j] = True
                elif (gameBoard.emptyfield[i][j] == 'f'
                      and gameBoard.solution[i][j] == '*'):
                    win[i][j] = True

        alltrue = [
            all(win[i][j] for j in range(gameBoard.width))
            for i in range(gameBoard.height)]
        if all(alltrue[i] for i in range(gameBoard.height)):
            return True
    # Ende Funktionsbereich

    # Spielschleife
    while laeuft:
        for row in range(mapheight):
            for col in range(mapwidth):
                image = tile_dic[gamefield[row][col]].convert()
                gameDisplay.blit(image, (col * tilesize, row * tilesize))
        pygame.display.update()

        # Schleife fuer Eventmanagement
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = x//tilesize
                y = y//tilesize
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    if timer == 0:
                        # Anfang fuer Doppelklickverarbeitung
                        timer = 0.001
                    elif timer < 0.5:
                        laeuft = doubleclick(x, y)
                        timer = 0
                        # Ende fuer Doppelklickverarbeitung

                    if laeuft:
                        laeuft = leftClick(x, y)
                    if not laeuft:
                        text = 'Du hast verloren.'
                        print(text)
                elif pygame.mouse.get_pressed() == (0, 0, 1):
                    rightClick(x, y)
            if event.type == pygame.QUIT:
                laeuft = False
                text = 'Du hast aufgegeben.'
                print(text)
        if endcheck() and laeuft:
            text = 'Du hast gewonnen.'
            print(text)
            laeuft = False
        if timer != 0:
            timer += dt
            if timer >= 0.5:
                timer = 0
        dt = clock.tick(30) / 1000
    # Bei beenden des Spieles
    gamefield = solution
    for row in range(mapheight):
        for col in range(mapwidth):
            image = tile_dic[gamefield[row][col]].convert()
            gameDisplay.blit(image, (col * tilesize, row * tilesize))

    textsurface = myfont.render(text, False, (0, 0, 0), (255, 255, 255))
    gameDisplay.blit(
        textsurface,
        ((mapwidth-4.5) * tilesize/2, (mapheight-1) * tilesize/2 - 10))

    pygame.display.update()
    pygame.time.delay(5000)
    pygame.font.quit()
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
