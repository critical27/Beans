import pygame
from pygame.locals import *

class chooseMethod():
    def __init__(self):
        self.vecLeft = [-100,0]
        self.vecRight = [100,0]
        self.vecUp = [-80,0]
        self.vecDown = [80,0]

#Human
class manual(chooseMethod):
    def choose(self,coordinate):
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                return True
            elif event.key == K_LEFT:
                if coordinate[0] > 110:
                    coordinate[0] += self.vecLeft[0]
            elif event.key == K_RIGHT:
                if coordinate[0] < 610:
                    coordinate[0] += self.vecRight[0]
        return False

#Random AI
class random(chooseMethod):
    def choose(self):
        pass

class pickMethod():
    def __init__(self,ui,icon):
        self.ui = ui
        self.icon = icon

    def pick(self):
        pass

class playerOnePick(pickMethod):
    def pick(self,pos,board):
        index = self.ui.getPlateIndex(pos)
        beans = board[index]
        if beans == 0:
            return "Invalid Plate"

        self.ui.slideUp(self.icon,pos,80)
        self.ui.boardUpdate(index,0)
        self.ui.slideDown(self.icon,pos,80)
        self.ui.slideRight(self.icon,pos,100)
        index = self.ui.getPlateIndex(pos)

        #If there are beans in hand
        while beans > 0:
            beans -= 1
            index = self.ui.getPlateIndex(pos)
            if index in range(0,6):
                #If last bean is put into own empty plate, it can score directly
                #Also, if there are beans in the opponent's responding plate, take them to score
                if beans == 0 and board[index] == 0:
                    self.pickLastOneAndOpponent(pos[:],board,index)
                else:
                    self.ui.slideUp(self.icon,pos,80)
                    self.ui.boardUpdate(index,board[index]+1)
                    self.ui.slideDown(self.icon,pos,80)
                    if beans > 0:
                        self.ui.slideRight(self.icon,pos,100)
            elif index == 6:
                self.ui.slideUp(self.icon,pos,180)
                self.ui.boardUpdate(index,board[index]+1)
                if beans > 0:
                    self.ui.slideUp(self.icon,pos,20)
                    self.ui.slideLeft(self.icon,pos,100)
            elif index in range(7,13):
                self.ui.slideUp(self.icon,pos,80)
                self.ui.boardUpdate(index,board[index]+1)
                self.ui.slideDown(self.icon,pos,80)
                if beans > 0:
                    self.ui.slideLeft(self.icon,pos,100)
            elif index == 13:
                self.ui.slideDown(self.icon,pos,20)
                self.ui.boardUpdate(index,board[index]+1)
                if beans > 0:
                    self.ui.slideDown(self.icon,pos,180)
                    self.ui.slideRight(self.icon,pos,100)
                    index = 0
            else:
                assert()
        #If last bean is put into own bowl, get a bonus play chance
        if index == 6:
            return "Play Again"
        return "Your Turn"

    def pickLastOneAndOpponent(self,pos,board,index):
        temp = pos[:]
        self.ui.slideUp(self.icon,pos,80)
        self.ui.boardUpdate(index,0)
        self.ui.slideUp(self.icon,pos,100)
        self.ui.slideRight(self.icon,pos,710-pos[0])
        self.ui.boardUpdate(6,board[6]+1)
        if board[12-index] != 0:
            self.ui.slideLeft(self.icon,pos,710-temp[0])
            self.ui.slideUp(self.icon,pos,100)
            beans = board[12-index]
            self.ui.boardUpdate(12-index,0)
            self.ui.slideDown(self.icon,pos,100)
            self.ui.slideRight(self.icon,pos,710-temp[0])
            self.ui.boardUpdate(6,board[6]+beans)

class playerTwoPick(pickMethod):
    def pick(self,pos,board):
        index = self.ui.getPlateIndex(pos)
        beans = board[index]
        if beans == 0:
            return "Invalid Plate"

        self.ui.slideDown(self.icon,pos,80)
        self.ui.boardUpdate(index,0)
        self.ui.slideUp(self.icon,pos,80)
        self.ui.slideLeft(self.icon,pos,100)
        index = self.ui.getPlateIndex(pos)

        #If there are beans in hand
        while beans > 0:
            beans -= 1
            index = self.ui.getPlateIndex(pos)
            if index in range(0,6):
                self.ui.slideDown(self.icon,pos,80)
                self.ui.boardUpdate(index,board[index]+1)
                self.ui.slideUp(self.icon,pos,80)
                if beans > 0:
                    self.ui.slideRight(self.icon,pos,100)
            elif index == 6:
                self.ui.slideUp(self.icon,pos,20)
                self.ui.boardUpdate(index,board[index]+1)
                if beans > 0:
                    self.ui.slideUp(self.icon,pos,180)
                    self.ui.slideLeft(self.icon,pos,100)
            elif index in range(7,13):
                #If last bean is put into own empty plate, it can score directly
                #Also, if there are beans in the opponent's responding plate, take them to score
                if beans == 0 and board[index] == 0:
                    self.pickLastOneAndOpponent(pos[:],board,index)
                else:
                    self.ui.slideDown(self.icon,pos,80)
                    self.ui.boardUpdate(index,board[index]+1)
                    self.ui.slideUp(self.icon,pos,80)
                    if beans > 0:
                        self.ui.slideLeft(self.icon,pos,100)
            elif index == 13:
                self.ui.slideDown(self.icon,pos,180)
                self.ui.boardUpdate(index,board[index]+1)
                if beans > 0:
                    self.ui.slideDown(self.icon,pos,20)
                    self.ui.slideRight(self.icon,pos,100)
                    index = 0
            else:
                assert()
        #If last bean is put into own bowl, get a bonus play chance
        if index == 13:
            return "Play Again"
        return "Your Turn"

    def pickLastOneAndOpponent(self,pos,board,index):
        temp = pos[:]
        self.ui.slideDown(self.icon,pos,80)
        self.ui.boardUpdate(index,0)
        self.ui.slideDown(self.icon,pos,100)
        self.ui.slideLeft(self.icon,pos,pos[0]-0)
        self.ui.boardUpdate(13,board[13]+1)
        if board[12-index] != 0:
            self.ui.slideRight(self.icon,pos,temp[0]-0)
            self.ui.slideDown(self.icon,pos,100)
            beans = board[12-index]
            self.ui.boardUpdate(12-index,0)
            self.ui.slideUp(self.icon,pos,100)
            self.ui.slideLeft(self.icon,pos,temp[0]-0)
            self.ui.boardUpdate(13,board[13]+beans)
