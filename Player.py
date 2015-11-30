import pygame
import Config
import Action
import random

class human():
    def __init__(self,ui,name,icon1,icon2,pos,board):
        self.ui = ui
        self.name = name
        self.icon1 = icon1
        self.icon2 = icon2
        self.pos = pos
        self.board = board
        self.chooseMethod = Action.manual()
        self.pickMethod = Action.playerOnePick(self.ui,self.icon2) if self.name == "player1" else Action.playerTwoPick(self.ui,self.icon2)

    def play(self):
        self.choose()
        self.pick()

    #Press space to select
    #if it's not a empty plate,pick them
    def choose(self):
        self.ui.draw(self.icon1,self.pos)
        while True:
            rt = self.chooseMethod.choose(self.pos)
            if rt == True:
                return
            else:
                self.ui.draw(self.icon1,self.pos)

    #if you get a bonus play chance or select a empty plate, continue
    def pick(self):
        while True:
            rt = self.pickMethod.pick(self.pos[:],self.board)
            if rt == "Play Again" or rt == "Invalid Plate":
                self.choose()
            else:
                return
        return True

class computer():
    def __init__(self,ui,name,icon1,icon2,pos,board,level):
        self.ui = ui
        self.name = name
        self.icon1 = icon1
        self.icon2 = icon2
        self.pos = pos
        self.board = board
        self.level = level
        if level == 1:
            self.chooseMethod = Action.random()
        self.pickMethod = Action.playerOnePick(self.ui,self.icon2) if self.name == "player1" else Action.playerTwoPick(self.ui,self.icon2)
        self.plate_index = 0 if self.name == "player1" else 7
        self.bowl_index = 6 if self.name == "player1" else 13

    def play(self):
        if self.level == 1:
            self.choose()
            self.pick()
        else:
            self.calculate()
            print(self.max_record)
            for i in range(len(self.max_record)):
                self.ui.draw(self.icon1,self.pos)
                pygame.time.delay(300)
                self.move(self.max_record[i])
                self.pickMethod.pick(self.pos[:],self.board)

    #Todo
    def choose(self):
        self.ui.draw(self.icon1,self.pos)
        pygame.time.delay(300)
        startPos = self.ui.getPlateIndex(self.pos)
        validIndex = list(filter(lambda x:self.board[x] > 0,range(self.plate_index,self.bowl_index)))
        endPos = validIndex[random.randint(0,len(validIndex)-1)]
        if startPos != endPos:
            if startPos > endPos:
                if self.name == "player1":
                    self.ui.slideLeft(self.icon1,self.pos,(startPos-endPos)*100)
                else:
                    self.ui.slideRight(self.icon1,self.pos,(startPos-endPos)*100)
            elif startPos < endPos:
                if self.name == "player1":
                    self.ui.slideRight(self.icon1,self.pos,(endPos-startPos)*100)
                else:
                    self.ui.slideLeft(self.icon1,self.pos,(endPos-startPos)*100)
            else:
                pass
        self.ui.draw(self.icon1,self.pos)

    def pick(self):
        while True:
            rt = self.pickMethod.pick(self.pos[:],self.board)
            if rt == "Play Again" or rt == "Invalid Plate":
                self.choose()
            else:
                return
        return True

    def move(self,endPos):
        self.ui.draw(self.icon1,self.pos)
        startPos = self.ui.getPlateIndex(self.pos)
        if startPos != endPos:
            if startPos > endPos:
                self.ui.slideRight(self.icon1,self.pos,(startPos-endPos)*100)
            elif startPos < endPos:
                self.ui.slideLeft(self.icon1,self.pos,(endPos-startPos)*100)
            else:
                pass
        self.ui.draw(self.icon1,self.pos)

    def calculate(self):
        self.record = []
        self.max_score = self.board[self.bowl_index]
        self.max_record = []
        self.dfs(self.board[:],1)

    def dfs(self,board,depth):
        temp_score = board[self.bowl_index]
        temp_board = board[:]
        temp_record = self.record[:]

        for i in range(self.plate_index,self.bowl_index):
            if board[i] == 0:
                continue
            else:
                #When it has a bonus play chance, the score obviously is greater than current max_score
                if self.update_board(board,i) == True:
                    self.record.append(i)
                    if board[self.bowl_index] > self.max_score:
                        self.max_score = board[self.bowl_index]
                        self.max_record = self.record[:]
                    self.dfs(board,depth+1)
                    self.record = temp_record[:]
                else:
                    if board[self.bowl_index] > self.max_score:
                        self.max_score = board[self.bowl_index]
                        self.max_record = self.record[:] + [i]
                board = temp_board[:]
        if temp_score == self.max_score and len(self.max_record) == depth - 1:
            validIndex = list(filter(lambda x:board[x] > 0,range(self.plate_index,self.bowl_index)))
            self.max_record.append(validIndex[random.randint(0,len(validIndex)-1)])

    #return True if it has a bonus play chance
    def update_board(self,board,index):
        beans = board[index]
        board[index] = 0
        while beans > 0:
            index += 1
            if(index == 14):
                index = 0
            beans -= 1
            board[index] += 1
        if board[index] == 1 and index in range(self.plate_index,self.bowl_index):
            board[index] = 0
            board[self.bowl_index] += board[12-index]
            board[12-index] = 0
            return False
        if index == self.bowl_index:
            return True
        else:
            return False
