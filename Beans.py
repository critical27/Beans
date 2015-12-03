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
        self.menu_event()

    def menu_event(self):
        #Menu event
        while True:
            self.menu = menu(self.screen,self.font)
            rect1,rect2,rect3,rect4 = self.menu.draw()
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                if(event.pos[0] in range(rect1.left,rect1.right+1) and event.pos[1] in range(rect1.top,rect1.bottom+1)):
                    game(self.screen,self.font)
                elif(event.pos[0] in range(rect2.left,rect2.right+1) and event.pos[1] in range(rect2.top,rect2.bottom+1)):
                    demo(self.screen,self.font)
                elif(event.pos[0] in range(rect3.left,rect3.right+1) and event.pos[1] in range(rect3.top,rect3.bottom+1)):
                    option(self.screen)
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
        self.screen = screen
        self.font = font
        self.player_init()
        self.run()
        self.over()

    def player_init(self):
        #Create two players
        if Config.players_num == 0:
            self.player1 = Player.computer(self.ui,"player1","Resource/cursor1.png","Resource/pick1.png",[110,440],self.ui.board,1)
            self.player2 = Player.computer(self.ui,"player2","Resource/cursor2.png","Resource/pick2.png",[110,80],self.ui.board,2)
        elif Config.players_num == 1:
            self.player1 = Player.human(self.ui,"player1","Resource/cursor1.png","Resource/pick1.png",[110,440],self.ui.board)
            self.player2 = Player.computer(self.ui,"player2","Resource/cursor2.png","Resource/pick2.png",[110,80],self.ui.board,Config.level)
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

    def over(self):
        self.screen.fill((127,127,127))
        text_game_over = "Player{0} win".format(1 if self.ui.score1 > self.ui.score2 else 2)
        text_continue = "Press any key to continue"
        surface_game_over = self.font.render(text_game_over,True,(255,255,255))
        surface_continue = self.font.render(text_continue,True,(255,255,255))
        self.screen.blit(surface_game_over,(400 - surface_game_over.get_width(),250 - surface_game_over.get_height()))
        self.screen.blit(surface_continue,(400 - surface_continue.get_width(),350 - surface_continue.get_height()))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                break
        print("Game Over")

#Todo
class Demo():
    def __init__(self,screen,font):
        self.screen = screen
        self.font = font
        self.run()

    def run(self):
        pass

class option():
    def __init__(self,screen):
        self.screen = screen
        self.font = pygame.font.Font("Resource/simkai.ttf",72)
        self.draw()
        self.option_event()

    def draw(self):
        self.screen.fill((253,246,227))
        minus = pygame.image.load("Resource/minus.png")
        self.rect_beans_minus = self.screen.blit(minus,(250 - minus.get_width() / 2,150 - minus.get_height() / 2))
        self.rect_players_minus = self.screen.blit(minus,(250 - minus.get_width() / 2,300- minus.get_height() / 2))
        self.rect_difficulty_minus = self.screen.blit(minus,(250 - minus.get_width() / 2,450 - minus.get_height() / 2))

        plus = pygame.image.load("Resource/plus.png")
        self.rect_beans_plus = self.screen.blit(plus,(550 - plus.get_width() / 2,150 - minus.get_height() / 2))
        self.rect_players_plus = self.screen.blit(plus,(550 - plus.get_width() / 2,300 - minus.get_height() / 2))
        self.rect_difficulty_plus = self.screen.blit(plus,(550 - plus.get_width() / 2,450 - minus.get_height() / 2))

        beans_num = self.font.render(str(Config.beans_num),True,(0,0,0))
        self.screen.blit(beans_num,(400 - beans_num.get_width() / 2, 150 - beans_num.get_height() / 2))
        players_num = self.font.render(str(Config.players_num),True,(0,0,0))
        self.screen.blit(players_num,(400 - players_num.get_width() / 2, 300 - players_num.get_height() / 2))
        level = "Easy" if Config.level == 1 else "Hard"
        difficulty = self.font.render(level,True,(0,0,0))
        self.screen.blit(difficulty,(400 - difficulty.get_width() / 2, 450 - difficulty.get_height() / 2))

        self.text_font = pygame.font.Font("Resource/simkai.ttf",48)
        text_beans_num = self.text_font.render("Beans in Each Plate",True,(0,0,0))
        self.screen.blit(text_beans_num,(400 - text_beans_num.get_width() / 2, 80 - text_beans_num.get_height() / 2))
        text_players_num = self.text_font.render("Human Players",True,(0,0,0))
        self.screen.blit(text_players_num,(400 - text_players_num.get_width() / 2, 230 - text_players_num.get_height() / 2))
        text_difficulty = self.text_font.render("Difficulty",True,(0,0,0))
        self.screen.blit(text_difficulty,(400 - text_difficulty.get_width() / 2, 380 - text_difficulty.get_height() / 2))
        text_ok = self.text_font.render("ok",True,(0,0,0))
        self.button_ok = self.screen.blit(text_ok,(400 - text_ok.get_width() / 2, 550 - text_ok.get_height() / 2))
        pygame.display.update()

    def option_event(self):
        #Option event
        while True:
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                if(event.pos[0] in range(self.rect_beans_minus.left,self.rect_beans_minus.right+1) and event.pos[1] in range(self.rect_beans_minus.top,self.rect_beans_minus.bottom+1)):
                    if Config.beans_num > 3:
                        Config.beans_num -= 1
                        self.draw()
                elif(event.pos[0] in range(self.rect_beans_plus.left,self.rect_beans_plus.right+1) and event.pos[1] in range(self.rect_beans_plus.top,self.rect_beans_plus.bottom+1)):
                    if Config.beans_num < 6:
                        Config.beans_num += 1
                        self.draw()
                elif(event.pos[0] in range(self.rect_players_minus.left,self.rect_players_minus.right+1) and event.pos[1] in range(self.rect_players_minus.top,self.rect_players_minus.bottom+1)):
                    if Config.players_num > 0:
                        Config.players_num -= 1
                        self.draw()
                elif(event.pos[0] in range(self.rect_players_plus.left,self.rect_players_plus.right+1) and event.pos[1] in range(self.rect_players_plus.top,self.rect_players_plus.bottom+1)):
                    if Config.players_num < 2:
                        Config.players_num += 1
                        self.draw()
                elif(event.pos[0] in range(self.rect_difficulty_minus.left,self.rect_difficulty_minus.right+1) and event.pos[1] in range(self.rect_difficulty_minus.top,self.rect_difficulty_minus.bottom+1)):
                    if Config.level > 1:
                        Config.level -= 1
                        self.draw()
                elif(event.pos[0] in range(self.rect_difficulty_plus.left,self.rect_difficulty_plus.right+1) and event.pos[1] in range(self.rect_difficulty_plus.top,self.rect_difficulty_plus.bottom+1)):
                    if Config.level < 2:
                        Config.level += 1
                        self.draw()
                elif(event.pos[0] in range(self.button_ok.left,self.button_ok.right+1) and event.pos[1] in range(self.button_ok.top,self.button_ok.bottom+1)):
                    break

if __name__ == "__main__":
    beans = app()
