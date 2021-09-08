import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
    def __init__(self,ai_settings,screen,ship):
        super().__init__()
        self.screen=screen
        self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_width)
        self.rect.centerx=ship.rect.centerx
        self.rect.top=ship.rect.top

        self.y=float(self.rect.y)
        self.color=ai_settings.bullet_color
        self.speed_factor=ai_settings.bullet_speed_factor

    def update(self):
        self.y -=self.speed_factor
        self.rect.y=self.y  #可能是保持子弹本身与子弹矩形的相同高度

    def draw_bullet(self):  #因为子弹没有加载对应的图片 采取绘制
        pygame.draw.rect(self.screen,self.color,self.rect)
