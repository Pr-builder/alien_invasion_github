import pygame
from settings import Settings
from ship import Ship #导入整体中的一部分
import game_functions as gf #导入整体
from pygame.sprite import Group   #并没有直接导入bullet
from alien import Alien #单个外星人需要  一群不需要
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

def run_game():
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ship = Ship(ai_settings,screen)
    bullets=Group()
    #alien = Alien(ai_settings, screen) #一个外星人
    aliens=Group()
    gf.create_fleet(ai_settings,screen,ship,aliens) #创建一群子弹时 好像没调用create_fleet
    stats=GameStats(ai_settings)
    sb=ScoreBoard(ai_settings,screen,stats)
    pygame.display.set_caption("Alien Invasion")

    button_play=Button(ai_settings,screen,"Play")

    while True:
        # 检测事件
         gf.check_events(ai_settings,screen,stats,sb,button_play,ship,aliens,bullets)
         #可能会改变 moving_right的标志 进而改变飞船的速度方向
         if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)

         # 重新绘制屏幕
         # gf.update_screen(ai_settings,screen,ship,alien,bullets)
         gf.update_screen(ai_settings, screen,stats,sb, ship, aliens, bullets,button_play)

         #使得屏幕可见
         pygame.display.flip()
         #pygame.dispaly.flip() 拼写错误
run_game()
