import pygame
from pygame.locals import *

import Config
import Player
import Interface

class app(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Doodle")
        self.screen = pygame.display.set_mode((800,600))
        self.font = pygame.font.Font("Resource/simkai.ttf",32)
        self.menu = menu(self.screen,self.font)
        self.menuEvent(*self.menu.draw())

    def menuEvent(self,rect1,rect2,rect3,rect4):
        #Menu event
        self.game = game(self.screen,self.font)
        while True:
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                if(event.pos[0] in range(rect1.left,rect1.right+1) and event.pos[1] in range(rect1.top,rect1.bottom+1)):
                    self.game = game(self.screen,self.font)
                elif(event.pos[0] in range(rect2.left,rect2.right+1) and event.pos[1] in range(rect2.top,rect2.bottom+1)):
                    self.demo = demo(self.screen)
                elif(event.pos[0] in range(rect3.left,rect3.right+1) and event.pos[1] in range(rect3.top,rect3.bottom+1)):
                    self.option = option(self.screen)
                elif(event.pos[0] in range(rect4.left,rect4.right+1) and event.pos[1] in range(rect4.top,rect4.bottom+1)):
                    sys.exit()

class menu():
    def __init__(self,screen,font):
        self.screen = screen
        self.font = font
        self.screen.fill((127,127,127))

    def draw(self):
        #menu initialize
        text_new_game = self.font.render("New Game",True,(255,255,255))
        rect_new_game = self.screen.blit(text_new_game,(400 - text_new_game.get_width() / 2, 150 - text_new_game.get_height() / 2))
        text_how_to_play = self.font.render("How to Play",True,(255,255,255))
        rect_how_to_play = self.screen.blit(text_how_to_play,(400 - text_how_to_play.get_width() / 2, 250 - text_how_to_play.get_height() / 2))
        text_option = self.font.render("Option",True,(255,255,255))
        rect_option = self.screen.blit(text_option,(400 - text_option.get_width() / 2, 350 - text_option.get_height() / 2))
        text_quit_game = self.font.render("Quit Game",True,(255,255,255))
        rect_quit_game = self.screen.blit(text_quit_game,(400 - text_quit_game.get_width() / 2, 450 - text_quit_game.get_height() / 2))
        pygame.display.update()
        return rect_new_game,rect_how_to_play,rect_option,rect_quit_game

class game():
    def __init__(self,screen,font):
        self.ui = Interface.interface(screen,font)
        self.player_init()
        self.run()

    def player_init(self):
        #Create two players
        if Config.players_num == 1:
            self.player1 = Player.human(self.ui,"player1","Resource/cursor1.png","Resource/pick1.png",[110,440],self.ui.board)
            self.player2 = Player.computer(self.ui,"player2","Resource/cursor2.png","Resource/pick2.png",[110,80],self.ui.board,0)
        else:
            self.player1 = Player.human(self.ui,"player1","Resource/cursor1.png","Resource/pick1.png",[110,440],self.ui.board)
            self.player2 = Player.human(self.ui,"player2","Resource/cursor2.png","Resource/pick2.png",[110,80],self.ui.board)

    def run(self):
        #Draw thw interface
        #Two players play in turn
        self.ui.draw(self.player1.icon1, self.player1.pos)
        while self.ui.isPlayerOneValid() or self.ui.isPlayerTwoValid():
            if self.ui.isPlayerOneValid():
                self.player1.play()
            if self.ui.isPlayerTwoValid():
                self.player2.play()
        print("Game Over")

class demo():
    def __init__(self,screen,font):
        pass

class option():
    pass

if __name__ == "__main__":
    beans = app()
