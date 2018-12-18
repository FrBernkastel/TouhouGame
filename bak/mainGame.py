# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random
import os

'''
有哪些参数：
敌机出现频率
敌机射击频率
敌机移动速度

子弹不同的类型
子弹不同的速度
子弹相同类型不同的参数

自机的射击速度
自机的判定范围


'''



#SYSPARA
x = 200
y = 25
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#Game parameter
#Smaller, harder
_freqEnemy=30

_freqShoot2=2



'''
游戏资源定义区
'''
# 初始化游戏 (screen)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TouHou Project2')

# 载入游戏音乐(bullet_sound,enemy_down_sound,game_over_sound)
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 载入背景图 (background,game_over)
background = pygame.image.load('resources/image/background.jpg').convert()
game_over = pygame.image.load('resources/image/gameover.png')

player_pos = [200, 600]
player = Player( player_pos)

def InitGame():
    player_pos = [200, 600]
    player.drawrect.topleft=player_pos
    player.ModiRect()
    player.down_imgidx = 0
    player.shoot_frequency=0
    player.is_hit=False

def RunGame():
        #几个Groups集合
    enemies1 = pygame.sprite.Group()
    enemies_down = pygame.sprite.Group()
    enemy_bul_grp = pygame.sprite.Group()


    enemy_frequency = 0

    score = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        key_pressed = pygame.key.get_pressed()

        # 控制发射子弹频率,并发射子弹
        if not player.is_hit:
            if  key_pressed[K_z]:
                if player.tryshot():
                    bullet_sound.play()
                    player.shoot()

        # 生成敌机
        if enemy_frequency % _freqEnemy == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_imgs[0].get_rect().width), 0]
            enemy1 = smallEnemy2(enemy1_pos, enemy_bul_grp)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= _freqEnemy:
            enemy_frequency = 0

        # 所有敌机发出子弹
        for enm in enemies1:
            if enm.tryshot():
                enm.shoot(10, player)

        # 移动子弹，若超出窗口范围则删除,!!同时判定是否攻击到了自机
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)

        for bullet in enemy_bul_grp:
            bullet.move()
            if pygame.sprite.collide_circle(bullet, player):
                enemy_bul_grp.remove(bullet)
                player.is_hit = True
                game_over_sound.play()
                break
            if bullet.rect.bottom < 0 or bullet.rect.top > SCREEN_HEIGHT:
                enemy_bul_grp.remove(bullet)

        # 移动敌机，若超出窗口范围则删除
        for enemy in enemies1:
            enemy.move()
            # 判断玩家是否被击中
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy)

        # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)

        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))

        # 绘制玩家飞机
        if not player.is_hit:
            player.draw(screen)
        elif not player.draw(screen,1):
                 running = False

        # 绘制击毁动画
        for enemy_down in enemies_down:
            if not enemy_down.drawDown(screen):
                score+=1000
                enemy1_down_sound.play()
                enemies_down.remove(enemy_down)
                continue

        # 绘制子弹和敌机
        player.bullets.draw(screen)
        enemies1.draw(screen)
        enemy_bul_grp.draw(screen)

        # 绘制得分
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # !!!!更新屏幕
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # 监听键盘事件

        # 若玩家被击中，则无效
        if not player.is_hit:
            if not key_pressed[K_LSHIFT]:
                mod = 0
            else:
                mod = 1
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp(mod)
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown(mod)
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft(mod)
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight(mod)



    font = pygame.font.Font(None, 48)
    text = font.render('Score: '+ str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)


def LoseGame():
    over=True
    while over:
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_r]:
            over=False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


def main():
    while 1:
        InitGame()
        RunGame()
        LoseGame()

if __name__ == "__main__":
    main()
