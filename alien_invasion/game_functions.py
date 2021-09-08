import sys
import pygame
#from ship import Ship   用形参还是真正实际的类
from alien import Alien
from bullet import Bullet
from time import sleep

#检测事件
def check_keydown_events(event, ai_settings,screen,ship,bullets): #对应参数一步步的修改
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings,screen,stats,sb,button_play,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,button_play,ship,aliens,bullets,mouse_x,mouse_y)


def check_play_button(ai_settings,screen,stats,sb,button_play,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=button_play.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()        #初始游戏设置
        pygame.mouse.set_visible(False) #隐藏光标

        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,button_play):
    screen.fill(ai_settings.bg_color)
    #ship.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    #alien.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        button_play.draw_button()
    pygame.display.flip()


#子弹部分
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)


#检测外星人和子弹的碰撞
def check_high_score(stats,sb):   #曾经打出 中午的：
    if stats.score > stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,False,True)
    if collisions:
        # stats.score += ai_settings.alien_points                      #可能存在统计不完全
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens) == 0:                                              # False子弹有效 True 外星人消失
        bullets.empty()                                               #子弹清空
        ai_settings.increase_speed()                                  #外星人为空则晋级  加速度
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)


def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


 #创建外星人准备
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=ai_settings.screen_height-3*alien_height-ship_height
    number_rows=int(available_space_y/(2*alien_height))
    #number_rows = int(available_space_y / (3 * alien_height))
    return number_rows

def get_number_aliens(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 外星人的个数是整数
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien_width=alien.rect.width

    alien.x = alien_width + 2 * alien_width * alien_number
    '''
    # 自己添加的代码 
    if alien.x >= 20:
        alien.x -= 10
    else:
        alien.x += 5
    '''
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    #alien.rect.y = (alien.rect.height +20) + 2 * alien.rect.height * row_number  #因为缩小alien照片 所以需要调节高度
    aliens.add(alien)  # -》》aliens用处


def create_fleet(ai_settings,screen,ship,aliens):  # aliens用处？？？
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens(ai_settings,alien.rect.width)  #外星人的个数是整数
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):  #不加range()  会报错
            create_alien(ai_settings, screen, aliens, alien_number,row_number)
            #create_alien(ai_settings, screen, aliens, alien_number, number_rows)只会出现一行外星人


def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *=-1


#飞船和外星人碰撞
def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #collisions=pygame.sprite.groupcollide(bullets,aliens,False,True) 这是子弹和外星人的检测碰撞函数
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
        # print("Crush!!!")
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)


#飞船坠落
def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    if stats.ships_left > 0:
        stats.ships_left -=1
        sb.prep_ships()
        aliens.empty()
        bullets.empty() #如果是子弹碰撞到飞船 子弹可以不清空  但要是飞船和外星人碰撞   则子弹必须清零
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  #使得光标可见

    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()  #飞船重新归位

    sleep(0.5) #暂停 要玩家看到 碰撞情况


#外星人到达屏幕低端
def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break








