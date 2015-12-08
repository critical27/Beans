#!/usr/bin/python
#-*- coding: utf-8 -*-
import pygame
import Config
import Action
import random

class player():
    pass

class human(player):
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
    #If it's not a empty plate,pick them
    def choose(self):
        self.ui.draw(self.icon1,self.pos)
        while True:
            rt = self.chooseMethod.choose(self.pos)
            if rt == True:
                return
            else:
                self.ui.draw(self.icon1,self.pos)

    #If you get a bonus play chance or select a empty plate, continue
    def pick(self):
        while True:
            rt = self.pickMethod.pick(self.pos[:],self.board)
            if rt == "Play Again" or rt == "Invalid Plate":
                if self.name == "player1":
                    if self.ui.isPlayerOneValid():
                        self.choose()
                    else:
                        return
                else:
                    if self.ui.isPlayerTwoValid():
                        self.choose()
                    else:
                        return
            else:
                return

class computer(player):
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
        self.own_plate_index = 0 if self.name == "player1" else 7
        self.own_bowl_index = 6 if self.name == "player1" else 13
        self.oppo_plate_index = 7 if self.name == "player1" else 0
        self.oppo_bowl_index = 13 if self.name == "player1" else 6

    def play(self):
        if self.level == 1:
            self.choose()
            self.pick()
        if self.level == 2:
            self.calculate()
            for i in range(len(self.max_record)):
                self.ui.draw(self.icon1,self.pos)
                pygame.time.delay(300)
                self.move(self.max_record[i])
                self.pickMethod.pick(self.pos[:],self.board)
        if self.level == 3:
            self.calculate()
            self.rethink()
            for i in range(len(self.max_record)):
                self.ui.draw(self.icon1,self.pos)
                pygame.time.delay(300)
                self.move(self.max_record[i])
                self.pickMethod.pick(self.pos[:],self.board)

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
                if self.name == "player1":
                    if self.ui.isPlayerOneValid():
                        self.choose()
                else:
                    if self.ui.isPlayerTwoValid():
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
        self.max_score = self.board[self.own_bowl_index]
        self.max_board = self.board[:]
        self.max_record = []
        self.dfs(self.board[:],1,self.own_plate_index,self.own_bowl_index)

    #Todo:
    #Consider how the opponent will play, and adjust the pick order
    def rethink(self):
        #Store current information
        tmp_cur_board = self.board[:]
        tmp_max_score = self.max_score
        tmp_max_board = self.max_board[:]
        tmp_max_record = self.max_record[:]

        #Only adjust the last pick
        #Firstly, replay the former pick
        for i in range(len(self.max_record) - 1):
            self.update_board(tmp_cur_board,self.max_record[i],self.own_plate_index,self.own_bowl_index)
        #store the difference between own score gap ane opponent's score gap
        diff = -100
        index = self.own_plate_index
        replay_board = tmp_cur_board[:]
        for i in range(self.own_plate_index,self.own_bowl_index):
            if tmp_cur_board[i] == 0:
                continue
            self.update_board(tmp_cur_board,i,self.own_plate_index,self.own_bowl_index)
            #Calculate the max score opponent can achieve
            self.max_score = tmp_max_score
            self.max_board = self.max_board[:]
            self.dfs(self.board[:],1,self.oppo_plate_index,self.oppo_bowl_index)

            #After calling dfs, self.max_board will store the board after opponent play
            #Then get the score gap
            print(self.max_board)
            gap = (self.max_board[self.own_bowl_index] - self.board[self.own_bowl_index]) - \
                  (self.max_board[self.oppo_bowl_index] - self.board[self.oppo_bowl_index])
            if gap > diff:
                diff = gap
                index = i
            #Restore the state
            tmp_cur_board = replay_board[:]
        #After the loop above, the index store the last pick, adjust the origin pick order
        self.max_record = tmp_max_record[:]
        self.max_record.pop()
        self.max_record.append(index)

    def dfs(self,board,depth,plate_index,bowl_index):
        temp_score = board[bowl_index]
        temp_board = board[:]
        temp_record = self.record[:]

        for i in range(plate_index,bowl_index):
            if board[i] == 0:
                continue
            else:
                #When it has a bonus play chance, the score obviously >= than current max_score
                if self.update_board(board,i,plate_index,bowl_index) == True:
                    self.record.append(i)
                    if board[bowl_index] > self.max_score:
                        self.max_score = board[bowl_index]
                        self.max_board = board[:]
                        self.max_record = self.record[:]
                    self.dfs(board,depth+1,plate_index,bowl_index)
                    self.record = temp_record[:]
                else:
                    if board[bowl_index] > self.max_score:
                        self.max_score = board[bowl_index]
                        self.max_board = board[:]
                        self.max_record = self.record[:] + [i]
                board = temp_board[:]
        if temp_score == self.max_score and len(self.max_record) == depth - 1:
            print("!!!")
            validIndex = list(filter(lambda x:board[x] > 0,range(plate_index,bowl_index)))
            if len(validIndex) != 0:
                index = random.randint(0,len(validIndex)-1)
                self.update_board(self.max_board,index,plate_index,bowl_index)
                self.max_record.append(validIndex[index])

    #Return True if it has a bonus play chance
    def update_board(self,board,index,plate_index,bowl_index):
        beans = board[index]
        board[index] = 0
        while beans > 0:
            index += 1
            if(index == 14):
                index = 0
            beans -= 1
            board[index] += 1
        if board[index] == 1 and index in range(plate_index,bowl_index):
            board[index] = 0
            board[bowl_index] += board[12-index]
            board[12-index] = 0
            return False
        if index == bowl_index:
            return True
        else:
            return False
