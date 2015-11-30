import pygame
import Config

class interface():
    #UI initialize
    def __init__(self,screen,font):
        self.screen = screen
        self.font = font
        self.vecUp = (0,-1)
        self.vecDown = (0,1)
        self.vecLeft = (-1,0)
        self.vecRight = (1,0)
        self.plate1 = [Config.beans_num for i in range(6)]
        self.plate2 = [Config.beans_num for i in range(6)]
        self.score1 = 0
        self.score2 = 0
        #Each player has 6 plates, and a bowl to score
        #they make up the board, the length is 14 = (6 plates + 1 bowl) * 2
        self.board = self.plate1 + [self.score1] + self.plate2 + [self.score2]

    #check if player has a non-empty plate
    def isPlayerOneValid(self):
        return self.plate1 != [0] * 6

    def isPlayerTwoValid(self):
        return self.plate2 != [0] * 6

    #Draw the UI, icon and pos default to None
    #display icon in coordinate pos
    def draw(self,icon = None,pos = None):
        self.screen.fill((127,127,127))
        self.plate_init()
        self.bowl_init()
        self.text_init(self.plate1,self.score1,self.plate2,self.score2)
        self.icon_init(icon,pos)
        pygame.display.update()

    #Draw the plates
    def plate_init(self):
        #plate surface
        plate_player_one = []
        plate_player_two = []
        for i in range(6):
            plate_player_one.append(pygame.surface.Surface((80,80)))
            plate_player_two.append(pygame.surface.Surface((80,80)))
        for i in range(6):
            plate_player_one[i].fill((0,127,127))
            plate_player_two[i].fill((0,127,127))
            self.screen.blit(plate_player_one[i],(110 + 100 * i, 160))
            self.screen.blit(plate_player_two[i],(610 - 100 * i, 360))

    #Draw the bowls
    def bowl_init(self):
        #bowl surface
        rect_player_one = pygame.Rect(710,160,80,280)
        rect_player_two = pygame.Rect(0,160,80,280)
        bowl_player_one = pygame.draw.ellipse(self.screen,(127,127,0),rect_player_one)
        bowl_player_two = pygame.draw.ellipse(self.screen,(127,127,0),rect_player_two)

    #Draw the text
    def text_init(self,plate1,score1,plate2,score2):
        score_player_one = self.font.render(str(score1),True,(0,0,0))
        score_player_two = self.font.render(str(score2),True,(0,0,0))
        self.screen.blit(score_player_one,(750 - score_player_one.get_width() / 2, 300 - score_player_one.get_height() / 2))
        self.screen.blit(score_player_two,(40 - score_player_two.get_width() / 2, 300 - score_player_two.get_height() / 2))
        #text surface
        num_player_one = []
        num_player_two = []
        for i in range(6):
            num_player_one.append(self.font.render(str(plate1[i]),True,(0,0,0)))
            num_player_two.append(self.font.render(str(plate2[i]),True,(0,0,0)))
        for i in range(6):
            self.screen.blit(num_player_one[i],(150 + 100 * i - num_player_one[i].get_width() / 2, 400 - num_player_one[i].get_height() / 2))
            self.screen.blit(num_player_two[i],(650 - 100 * i - num_player_two[i].get_width() / 2, 200 - num_player_two[i].get_height() / 2))

    def icon_init(self,icon,pos):
        if(icon != None and pos != None):
            self.screen.blit(pygame.image.load(icon),pos)

    def getVec(self,direction):
        if direction == "up":
            vec = self.vecUp
        elif direction == "down":
            vec = self.vecDown
        elif direction == "left":
            vec = self.vecLeft
        elif direction == "right":
            vec = self.vecRight
        else:
            assert()
        return vec

    #The animation of icon slide
    def slideAnimation(self,icon,pos,direction,rangeX,rangeY,animationSpeed):
        surface = pygame.image.load(icon)
        vec = self.getVec(direction)
        clock = pygame.time.Clock()
        self.draw()
        background = self.screen.copy()
        while True:
            self.screen.blit(background,(0,0))
            self.screen.blit(surface,pos)
            pygame.display.update()
            time_passed = clock.tick(60)
            pos[0] += animationSpeed * vec[0] * time_passed / 1000
            pos[1] += animationSpeed * vec[1] * time_passed / 1000
            if (not rangeX[0] <= pos[0] <= rangeX[1]) or (not rangeY[0] <= pos[1] <= rangeY[1]):
                return

    def boardUpdate(self,index,num):
        self.board[index] = num
        self.textUpdate(index,num)

    def textUpdate(self,index,num):
        if index in range(0,6):
            self.plate1[index] = num
        elif index == 6:
            self.score1 = num
        elif index in range(7,13):
            self.plate2[index - 7] = num
        elif index == 13:
            self.score2 = num
        else:
            assert()
        self.draw()

    def slideLeft(self,icon,pos,dis):
        rangeX = (pos[0] - dis, pos[0])
        rangeY = (pos[1], pos[1])
        self.slideAnimation(icon,pos[:],"left",rangeX,rangeY,Config.animation_speed)
        pos[0] -= dis

    def slideRight(self,icon,pos,dis):
        rangeX = (pos[0], pos[0] + dis)
        rangeY = (pos[1], pos[1])
        self.slideAnimation(icon,pos[:],"right",rangeX,rangeY,Config.animation_speed)
        pos[0] += dis

    def slideUp(self,icon,pos,dis):
        rangeX = (pos[0], pos[0])
        rangeY = (pos[1] - dis, pos[1])
        self.slideAnimation(icon,pos[:],"up",rangeX,rangeY,Config.animation_speed)
        pos[1] -= dis

    def slideDown(self,icon,pos,dis):
        rangeX = (pos[0], pos[0])
        rangeY = (pos[1], pos[1] + dis)
        self.slideAnimation(icon,pos[:],"down",rangeX,rangeY,Config.animation_speed)
        pos[1] += dis

    #Get responding index of board according to current icon coordinate
    def getPlateIndex(self,pos):
        if pos[1] == 440 or pos[1] == 280:
            return pos[0] // 100 - 1
        if pos[1] == 80 or pos[1] == 240:
            return 13 - pos[0] // 100
        assert()
