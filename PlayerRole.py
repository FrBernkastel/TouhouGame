# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame
import math
import random
from BulletRole import *
from GlobalParameter import *
from SoundRes import *
from util import *

_pl_freqShoot=1

player_filename='resources/image/player.png'
player_img=pygame.image.load(player_filename)

# 自机的素材图片

player_imgs=[]
for i in range(8):
    player_imgs.append(transformScale(player_img.subsurface(pygame.Rect(32*i,0,32,48)),1.5))


player_down_imgs=[]
for i in range(8):
    player_down_imgs.append(transformScale(player_img.subsurface(pygame.Rect(32*i,224,32,32)),1.5))






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
    def __init__(self, init_pos):
        pygame.sprite.Sprite.__init__(self)

#视图属性
        self.image = player_imgs[0]                                 # 用来存储玩家对象精灵图片的列表
        self.imagelist=player_imgs
        self.imgidx=0
        self.dly=5
        self.dlyrt=self.dly

        self.down_image=player_down_imgs[0]
        self.down_imagelist=player_down_imgs
        self.down_imgidx=0

        self.drawrect = self.image.get_rect()                      # 初始化图片所在的矩形
        self.drawrect.center = init_pos                    # 初始化矩形的左上角坐标
        self.rect = pygame.Rect(self.drawrect.centerx-2,self.drawrect.centery-2,0,0)


#控制属性
        self.speed = 10                                  # 初始化玩家速度，这里是一个确定的值
        self.slow_speed = 5                             # 玩家慢速状态
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.is_hit = False                             # 玩家是否被击中
        self.shoot_frequency = 0                             # 玩家是否发射子弹

#视图方法
    def imagechange(self):
        if self.dlyrt == 0:
            self.imgidx+=1
            self.dlyrt=self.dly
        else:
            self.dlyrt-=1

        if self.imgidx > 7:
            self.imgidx = 0
        self.image=self.imagelist[self.imgidx]

    def imagechange2(self):
        if self.down_imgidx <=7:
            self.down_image=self.down_imagelist[self.down_imgidx]
            if self.dlyrt == 0:
                self.down_imgidx+=1
                self.dlyrt=self.dly
            else:
                self.dlyrt-=1


    def draw(self,screen,mode=0):    #写的非常非常巧妙，画图的时候进行改变图片，封装的很棒！！！
        if not mode:
            screen.blit(self.image, self.drawrect)
            self.imagechange()
        else:
            screen.blit(self.down_image,self.drawrect)
            self.imagechange2()
            if self.down_imgidx > 7:
                return False
            else:
                return True

#控制方法
    def tryshot(self, mode): #抽象？ OK
        if self.shoot_frequency == _pl_freqShoot: #_freqShoot 是可以因机而异得
            self.shoot_frequency += 1
            self.shoot(mode)
            bullet_sound.play()
        else:
            if self.shoot_frequency > _pl_freqShoot:
                self.shoot_frequency = 0
            self.shoot_frequency += 1


    def shoot(self, mode):
        rec = self.rect
        if mode == 1:
            poses = [rec.topleft,rec.topleft,rec.topright,rec.topright]
            for i in range(1, 5):
                self.bullets.add(PlayerBulF(poses[i-1], i))
        else:
            poses = [rec.topleft, rec.center, rec.topright]
            for i in range(3):
                self.bullets.add(PlayerBul(poses[i]))

    def ModiRect(self):
        self.rect.center=self.drawrect.center

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
        if self.rect.top >= SCREEN_HEIGHT - self.drawrect.height/2:
            self.rect.top = SCREEN_HEIGHT - self.drawrect.height/2
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


