# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame
import math
import random


'''
参数区
'''
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900


TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3

_freqShoot=30
_pl_freqShoot=1




'''
对象图片素材区
'''




#自机图片 (plane_img)
filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)
bullet_filename='resources/image/bullet.png'
bullet_img0 = pygame.image.load(bullet_filename)
enemy_filename='resources/image/enemy.png'
enemy_img=pygame.image.load(enemy_filename)
enemy_down_filename='resources/image/enemy2.png'
enemy_down_img=pygame.image.load(enemy_down_filename)
player_filename='resources/image/player.png'
player_img=pygame.image.load(player_filename)

#敌机的素材图片，包括机体以及机体爆炸后的图片

enemy1_imgs=[]
for i in range(5):
    enemy1_imgs.append(enemy_img.subsurface(pygame.Rect(32*i,322,32,25)))

enemy1_down_imgs = []
for i in range(8):
    enemy1_down_imgs.append(enemy_down_img.subsurface(pygame.Rect(32*i,32*2,32,32)))

enemy2_imgs=[]
for i in range(5):
    enemy2_imgs.append(enemy_img.subsurface(pygame.Rect(32*i,354,32,25)))

enemy2_down_imgs = []
for i in range(8):
    enemy2_down_imgs.append(enemy_down_img.subsurface(pygame.Rect(32*i,0,32,32)))


# 自机的素材图片

player_imgs=[]
for i in range(8):
    player_imgs.append(player_img.subsurface(pygame.Rect(32*i,0,32,48)))

player_down_imgs=[]
for i in range(8):
    player_down_imgs.append(player_img.subsurface(pygame.Rect(32*i,224,32,32)))

# 子弹素材
bullet_rect = pygame.Rect(1004, 987, 9, 21)

bullet_img = plane_img.subsurface(bullet_rect)


ebullet1_imgs=[]
for i in range(16):
    ebullet1_imgs.append(bullet_img0.subsurface(pygame.Rect(16*i+4,96,8,16)))

ebullet2_imgs=[]
for i in range(16):
    ebullet2_imgs.append(bullet_img0.subsurface(pygame.Rect(16*i,160,16,16)))


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
    def __init__(self,imgs,init_pos,a=0,b=0,delay=2):
        pygame.sprite.Sprite.__init__(self)
    # 视图属性
        self.rect = imgs[0].get_rect()
        self.rect.midbottom = init_pos


        self.imgidxa=a
        self.imgidxb=b
        self.imgidx = a
        self.imagelist=imgs
        self.image = imgs[a]
        self.dly=delay
        self.dlyrt=self.dly

    def move(self):
        raise NotImplementedError

    def imagechange(self):
        if self.dlyrt == 0:
            self.imgidx+=1
            self.dlyrt=self.dly
        else:
            self.dlyrt-=1

        if self.imgidx > self.imgidxb:
            self.imgidx= self.imgidxa
        self.image=self.imagelist[self.imgidx]


class PlayerBul(Bullet):
    def __init__(self, init_pos): #
        Bullet.__init__(self, [bullet_img], init_pos)
        self.speed = 50


    def move(self):
        self.rect.top -= self.speed

#自机狙
class EnemyBul1(Bullet):
    def __init__(self,  init_pos, spd, player):
        Bullet.__init__(self,ebullet1_imgs, init_pos,a=1,b=2)

        self.speed = spd
        #引入成员函数self.ratex,self.ratey
        self.ratex,self.ratey=self.FollowPlayer(player.rect.center)



    def move(self):
        self.rect.left += self.speed*self.ratex
        self.rect.top += self.speed*self.ratey
        self.imagechange()


    def FollowPlayer(self,player_pos):
        Bul_pos=self.rect.center
        disx=player_pos[0]-Bul_pos[0]
        disy=player_pos[1]-Bul_pos[1]
        dis=math.sqrt(disx*disx+disy*disy)
        ratex=disx/dis
        ratey=disy/dis
        return ratex,ratey

#跟踪弹
class EnemyBul2(Bullet):
    def __init__(self, init_pos, spd, player):
        Bullet.__init__(self,ebullet2_imgs,  init_pos,a=1,b=10,delay=5)
        self.speed = spd
        self.ratex,self.ratey=self.FollowPlayer(player.rect.center)

        self.trackdis=300
        self.target=player



    def move(self):
        if self.trackdis>=0:
            self.ratex,self.ratey=self.FollowPlayer(self.target.rect.center)
            self.trackdis-=self.speed

        self.rect.left+=self.speed*self.ratex
        self.rect.top+=self.speed*self.ratey
        self.imagechange()


    def FollowPlayer(self,player_pos):
        Bul_pos=self.rect.center
        disx=player_pos[0]-Bul_pos[0]
        disy=player_pos[1]-Bul_pos[1]
        dis=math.sqrt(disx*disx+disy*disy)
        ratex=disx/dis
        ratey=disy/dis
        return ratex,ratey

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
        self.drawrect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.rect = pygame.Rect(self.drawrect.centerx-5,self.drawrect.centery-6,10,12)



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
    def tryshot(self): #抽象？ OK
        if self.shoot_frequency == _pl_freqShoot: #_freqShoot 是可以因机而异得
            self.shoot_frequency += 1
            return True
        else:
            if self.shoot_frequency > _pl_freqShoot:
                self.shoot_frequency = 0
            self.shoot_frequency += 1
            return False

    def shoot(self):
        bullet = PlayerBul( self.rect.midtop)
        bullet2 = PlayerBul( self.rect.topleft)
        bullet3 = PlayerBul( self.rect.topright)
        self.bullets.add(bullet)
        self.bullets.add(bullet2)
        self.bullets.add(bullet3)

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
    def __init__(self, imgs, down_imgs, init_pos, enemy_bul_grp, a=0,b=0,delay=10):
       pygame.sprite.Sprite.__init__(self)
#实体属性
       self.rect = imgs[0].get_rect()
       self.rect.topleft = init_pos #OK
#图片属性
       self.imgidxa = a
       self.imgidxb = b
       self.imgidx = a
       self.imagelist = imgs
       self.image = imgs[a]
       self.dly = delay
       self.dlyrt = self.dly
#！爆炸属性
       self.down_imgidx = 0
       self.down_imagelist=down_imgs
       self.down_image=down_imgs[0]

#控制信息
       self.bul_grp=enemy_bul_grp #OK from downer
       self.shoot_frequency = 0 #用于对每一个敌机发出子弹进行计数 #OK

    def drawDown(self,screen):
        screen.blit(self.down_image, self.rect)
        self.imagechange2()
        if self.down_imgidx > 7:
            return False
        else:
            return True

    def move(self): #抽象
        #self.rect.top += self.speed
        raise NotImplementedError

    def imagechange(self):
        if self.dlyrt == 0:
            self.imgidx+=1
            self.dlyrt=self.dly
        else:
            self.dlyrt-=1

        if self.imgidx > self.imgidxb:
            self.imgidx= self.imgidxa
        self.image=self.imagelist[self.imgidx]

    def imagechange2(self):
        if self.down_imgidx <=7:
            self.down_image=self.down_imagelist[self.down_imgidx]
            if self.dlyrt == 0:
                self.down_imgidx+=1
                self.dlyrt=self.dly
            else:
                self.dlyrt-=1

    def tryshot(self): #抽象？ OK
        if self.shoot_frequency == _freqShoot: #_freqShoot 是可以因机而异得
            self.shoot_frequency += 1
            return True
        else:
            if self.shoot_frequency > _freqShoot:
                self.shoot_frequency = 0           
            self.shoot_frequency += 1
            return False


    def shoot(self,speed,player): #抽象
        #bullet = EnemyBul2( self.rect.midbottom, speed,player)
        #self.bul_grp.add(bullet)
        raise NotImplementedError

'''
总结，想要继承Enemy类，我们需要得公共的成员为：images,downimages (自下而上传入),rect,down_index,bul_grp,shoot_frequency
并且，如果要继承的话，子类独有的是:spd,images,downimages,spd,_freqshoot, move(), shoot().

'''

class smallEnemy(Enemy):
    def __init__(self, init_pos, enemy_bul_grp):
       Enemy.__init__(self,enemy1_imgs,enemy1_down_imgs, init_pos,enemy_bul_grp,a=0,b=4,delay=5)

       self.speed = 2+random.randint(0,10) #要修改 #X

    def move(self): #抽象
        self.rect.top += self.speed
        self.imagechange()


    def tryshot(self): #抽象？ OK
        if self.shoot_frequency == _freqShoot: #_freqShoot 是可以因机而异得
            self.shoot_frequency += 1
            return True
        else:
            if self.shoot_frequency > _freqShoot:
                self.shoot_frequency = 0
            self.shoot_frequency += 1
            return False


    def shoot(self,speed,player): #抽象
        bullet = EnemyBul1( self.rect.midbottom, speed,player)
        self.bul_grp.add(bullet)


class smallEnemy2(Enemy):
    def __init__(self, init_pos, enemy_bul_grp):
       Enemy.__init__(self,enemy2_imgs,enemy2_down_imgs,init_pos,enemy_bul_grp,a=0,b=4,delay=5)

       self.speed = 2+random.randint(0,10)


    def move(self): #抽象
        self.rect.top += self.speed
        self.imagechange()


    def tryshot(self): #抽象？ OK
        if self.shoot_frequency == _freqShoot: #_freqShoot 是可以因机而异得
            self.shoot_frequency += 1
            return True
        else:
            if self.shoot_frequency > _freqShoot:
                self.shoot_frequency = 0
            self.shoot_frequency += 1
            return False


    def shoot(self,speed,player): #抽象
        bullet = EnemyBul2( self.rect.midbottom, speed,player)
        self.bul_grp.add(bullet)

