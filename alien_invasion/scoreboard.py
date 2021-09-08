import pygame.font
from ship import Ship
from pygame.sprite import Group  # ??？ 以前是否导入过  第一次导入？？？


class ScoreBoard():
    def __init__(self,ai_settings,screen,stats):
        self.screen=screen
        self.screen_rect=self.screen.get_rect()
        self.ai_settings=ai_settings
        self.stats=stats

        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,30)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = int(round(self.stats.score,-1))  #圆整到10的倍数
        score_str="Score:{:,}".format(rounded_score)  #分数显示例如1,000
        self.score_image=self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20


    def prep_high_score(self):
        high_score = int(round(self.stats.score, -1))  # 圆整到10的倍数
        high_score_str = "High_Record:{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        self.level_image=self.font.render("Level:"+str(+self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        #self.level_rect.right = self.score_rect.right-40
        #self.level_rect.top = self.score_rect.bottom +10
        self.level_rect.right = self.high_score_rect.right + 250
        self.level_rect.top = self.score_rect.top

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship=Ship(self.ai_settings,self.screen)
            ship.rect.x=10+ship_number * ship.rect.width
            #ship.rect.y=10
            ship.rect.y = 10
            self.ships.add(ship)



    def show_score(self):  #什么地方调用了show   好像多出是调用prep_x
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)   #不同以上三种形式