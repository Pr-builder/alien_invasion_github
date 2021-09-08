import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen=screen
        self.ai_settings=ai_settings

        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        #自己为了实现飞船上下移动 添加的代码
        #self.rect.y = self.screen.screen_height
        #self.y=float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right: #标志位为真且未出界
            self.center += self.ai_settings.ship_speed_factor  #self.rect.centerx +=此种情况  飞船不动!!!
        if self.moving_left and self.rect.left > 0:       #因为左右方向是平等的所以用if
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:          #上下移动的时候center 应该如何变化
            self.rect.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.bottom += self.ai_settings.ship_speed_factor

        self.rect.centerx=self.center  #这句不是很明白  可能是稳住中心？？？


    def blitme(self):
        self.screen.blit(self.image,self.rect)


    def center_ship(self):
        self.center=self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom   #每次飞船销毁时  飞船可以在底部

