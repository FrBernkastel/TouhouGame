# -*- coding: utf-8 -*-
"""

"""

import pygame
import math
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800


TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3

_freqShoot=20

'''
子弹类的成员.
传入参数：bullet_img, init_pos

成员：
image = bullet_img #精灵的显示图片
rect =  #精灵的实体存在矩阵
rect.midbottom = init_pos #通过设置一个坐标点，可以重新定位实体存在矩阵的四个坐标点
speed = 10 #子弹的速度

def move(); #调用一次这个方法可以让子弹的实体存在矩阵四个坐标点向上移动10个像素点

'''

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos

    def move(self):
        raise NotImplementedError


class PlayerBul(Bullet):
    def __init__(self, bullet_img, init_pos):
        Bullet.__init__(self, bullet_img, init_pos)
        self.speed = 20

    def move(self):
        self.rect.top -= self.speed

#自机狙
class EnemyBul1(Bullet):
    def __init__(self, bullet_img, init_pos, spd, player_pos):
        Bullet.__init__(self, bullet_img, init_pos)
        
        self.speed = spd
        Bul_pos=self.rect.center
        disx=player_pos[0]-Bul_pos[0]
        disy=player_pos[1]-Bul_pos[1]
        dis=math.sqrt(disx*disx+disy*disy)
        ratex=disx/dis
        ratey=disy/dis
        self.spdx=ratex*spd
        self.spdy=ratey*spd

    def move(self):
        self.rect.left += self.spdx
        self.rect.top += self.spdy





'''

玩家类的成员：
传入参数：plane_img(未划分)、player_rect(一组)、init_pos

成员:
image = [] #用一个列表存储玩家类的各种飞机图片

#!根据player_rect中的每一个rect对象，对一整块plane_img进行划分，CtoA后存入image列表
for i in range(len(player_rect)): 
    self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())

rect = player_rect[0] #取第一个rect，定义了玩家类的实体存在矩阵
rect.topleft = init_pos #重新定义玩家类的实体存在矩阵位置
speed = 8 #玩家的速度

bullets = pygame.sprite.Group() #创建一个集合，存储玩家已经发射的子弹
img_index = 0 #玩家精灵图片索引(??????)

is_hit = False #被攻击判定变量，确定玩家是否被击中


def shoot(bullet_img); #根据给定的bullet_img，创建Bullet类对象，然后加入到自己已经发射的子弹集合中

def moveUp/Down/Left/Right(); #玩家移动，即实体存在矩阵的变化


'''

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家对象精灵图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.drawrect = player_rect[0]                      # 初始化图片所在的矩形
        self.drawrect.topleft = init_pos                    # 初始化矩形的左上角坐标

        self.rect = pygame.Rect(self.drawrect.centerx-5,self.drawrect.centery-6,10,12)

        self.speed = 10                                  # 初始化玩家速度，这里是一个确定的值
        self.slow_speed = 5                             # 玩家慢速状态
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家精灵图片索引
        self.is_hit = False                             # 玩家是否被击中

    def shoot(self, bullet_img):
        bullet = PlayerBul(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self,mod = 0):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            if mod == 0:
                spd = self.speed
            if mod == 1:
                spd = self.slow_speed
            self.rect.top -= spd    #!!Waring, insimultantous change.
            self.drawrect.top -=spd

    def moveDown(self,mod = 0):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            if mod == 0:
                spd = self.speed
            if mod == 1:
                spd = self.slow_speed
            self.rect.top += spd
            self.drawrect.top += spd

    def moveLeft(self,mod = 0):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            if mod == 0:
                spd = self.speed
            if mod == 1:
                spd = self.slow_speed
            self.rect.left -= spd
            self.drawrect.left -= spd

    def moveRight(self,mod = 0):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            if mod == 0:
                spd = self.speed
            if mod == 1:
                spd = self.slow_speed
            self.rect.left += spd
            self.drawrect.left += spd

'''

敌人类的成员：
传入参数： enemy_img, enemy_down_imgs, init_pos

image = enemy_img #设置正常状态下敌人类的图片
down_imgs = enemy_down_imgs #设置敌人被攻击时候的动画效果图片集合，是一组图片
rect = image.get_rect() #同子弹类，用于创建敌人的实体存在矩阵
rect.topleft = init_pos #通过一个基准点重新定位敌人的实体存在矩阵，同子弹类
speed = 2 #同子弹类
down_index = 0 #???


def move(); #每调用一次，敌人对象实体存在矩阵向下移动2个单位

'''

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos, enemy_bul_grp):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 2+random.randint(0,10) #要修改
       self.down_index = 0
       self.bul_grp=enemy_bul_grp
       self.shoot_frequency = 0 #用于对每一个敌机发出子弹进行计数

    def move(self):
        self.rect.top += self.speed


    def tryshot(self):
        if self.shoot_frequency == _freqShoot:
            self.shoot_frequency += 1
            return True
        else:
            if self.shoot_frequency > _freqShoot:
                self.shoot_frequency = 0           
            self.shoot_frequency += 1
            return False



    def shoot(self, bullet_img,speed,player_pos):
        bullet = EnemyBul1(bullet_img, self.rect.midbottom, speed,player_pos)
        self.bul_grp.add(bullet)