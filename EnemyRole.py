# -*- coding: UTF-8 -*-
import pygame
import math
import random
from BulletRole import *
from util import *
from GlobalParameter import *




enemy_filename='resources/image/enemy.png'
enemy_img=pygame.image.load(enemy_filename)
enemy_down_filename='resources/image/enemy2.png'
enemy_down_img=pygame.image.load(enemy_down_filename)
enemy_filename3='resources/image/enemy3.png'
enemy_img2=pygame.image.load(enemy_filename3)
boss_filename='resources/image/boss.png'
boss_img=pygame.image.load(boss_filename)

#敌机的素材图片，包括机体以及机体爆炸后的图片

enemy1_imgs=[]
for i in range(5):
    enemy1_imgs.append(transformScale(enemy_img.subsurface(pygame.Rect(32*i,322,32,25)),1.5))

enemy1_down_imgs = []
for i in range(8):
    enemy1_down_imgs.append(transformScale(enemy_down_img.subsurface(pygame.Rect(32*i,32*2,32,32)),1.5))

enemy2_imgs=[]
for i in range(5):
    enemy2_imgs.append(transformScale(enemy_img.subsurface(pygame.Rect(32*i,354,32,25)),1.5))

enemy2_down_imgs = []
for i in range(8):
    enemy2_down_imgs.append(transformScale(enemy_down_img.subsurface(pygame.Rect(32*i,0,32,32)),1.5))

enemy3_imgs=[]
for i in range(4):
    enemy3_imgs.append(transformScale(enemy_img.subsurface(pygame.Rect(320+i*48,6,48,45)),1.5))

enemy4_imgs=[]
for i in range(4):
    enemy4_imgs.append(transformScale(enemy_img.subsurface(pygame.Rect(5+i*48,0,38,30)),1.5))

enemy5_imgs=[]
for i in range(4):
    enemy5_imgs.append(transformScale(enemy_img.subsurface(pygame.Rect(5+i*48,32,38,30)),1.5))

enemy6_imgs=[]
for i in range(4):
    enemy6_imgs.append(transformScale(enemy_img2.subsurface(pygame.Rect(14+64*i,7,36,53)),1.5))

enemy3_down_imgs = []
for i in range(4):
    enemy3_down_imgs.append(transformScale(enemy_img2.subsurface(pygame.Rect(32*i,223,32,32)),1.5))
for i in range(4):
    enemy3_down_imgs.append(transformScale(enemy_img2.subsurface(pygame.Rect(32 * (3-i), 223, 32, 32)), 1.5))


boss_imgs=[]
for i in range(4):
    boss_imgs.append(transformScale(boss_img.subsurface(pygame.Rect(8+96*i,10,80,113)),1.5))

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
    def __init__(self, imgs, down_imgs, init_pos, enemy_bul_grp,bul_spd, a=0,b=0,delay=10,_fq=20):
        pygame.sprite.Sprite.__init__(self)
#实体属性
        self.rect = imgs[0].get_rect()
        self.rect.center = init_pos
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
        self._freqShoot= _fq
        self.shoot_frequency = self._freqShoot/2 #用于对每一个敌机发出子弹进行计数 #OK
        self.dict_speed=bul_spd
        self.hp = 1



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

    def tryshot(self,player,mode=0): #抽象？ OK
        if mode==0:
            if self.shoot_frequency == self._freqShoot: #_freqShoot 是可以因机而异得
                self.shoot_frequency += 1
                self.shoot(self.dict_speed,player)
            else:
                if self.shoot_frequency > self._freqShoot:
                    self.shoot_frequency = 0
                self.shoot_frequency += 1
        if mode==1:
            if self.shoot_frequency == self._freqShoot1: #_freqShoot 是可以因机而异得
                self.shoot_frequency += 1
                self.shoot1(self.dict_speed,player)
            else:
                if self.shoot_frequency > self._freqShoot1:
                    self.shoot_frequency = 0
                self.shoot_frequency += 1

        if mode==2:
            if self.shoot_frequency == self._freqShoot2: #_freqShoot 是可以因机而异得
                self.shoot_frequency += 1
                self.shoot2(self.dict_speed,player)
            else:
                if self.shoot_frequency > self._freqShoot2:
                    self.shoot_frequency = 0
                self.shoot_frequency += 1

        if mode==3:
            if self.shoot_frequency == self._freqShoot3: #_freqShoot 是可以因机而异得
                self.shoot_frequency += 1
                self.shoot3(self.dict_speed,player)
            else:
                if self.shoot_frequency > self._freqShoot3:
                    self.shoot_frequency = 0
                self.shoot_frequency += 1


    def shoot(self,speed,player): #抽象
        #bullet = EnemyBul2( self.rect.midbottom, speed,player)
        #self.bul_grp.add(bullet)
        raise NotImplementedError

'''
总结，想要继承Enemy类，我们需要得公共的成员为：images,downimages (自下而上传入),rect,down_index,bul_grp,shoot_frequency
并且，如果要继承的话，子类独有的是:spd,images,downimages,spd,_freqshoot, move(), shoot().

'''

class smallEnemy(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy1_imgs,enemy1_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=4,delay=5)

       self.speed = 10 #要修改 #X
#自击狙，从上到下
    def move(self): #抽象
        self.rect.top += self.speed
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul1( self.rect.center, speed,player)
        self.bul_grp.add(bullet)


class smallEnemy2(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy2_imgs,enemy2_down_imgs,init_pos,enemy_bul_grp,bul_spd,a=0,b=4,delay=5)

       self.speed = 2+random.randint(0,10)


    def move(self): #抽象
        self.rect.top += self.speed
        self.imagechange()


    def shoot(self,speed,player): #抽象
        bullet = EnemyBul2( self.rect.center, speed,player)
        self.bul_grp.add(bullet)

class smallEnemy3(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy1_imgs,enemy1_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=4,delay=5)

       self.speed = 10 #要修改 #X
#自击狙，从左向右
    def move(self): #抽象
        self.rect.left += self.speed
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul1( self.rect.center, speed,player)
        self.bul_grp.add(bullet)

class smallEnemy4(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy1_imgs,enemy1_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=4,delay=5)

       self.speed = 10 #要修改 #X
#自机狙，从右向左
    def move(self): #抽象
        self.rect.left -= self.speed
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul1( self.rect.center, speed,player)
        self.bul_grp.add(bullet)

class smallEnemy5(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy3_imgs,enemy2_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=60-random.randint(0,45))

       self.speed = 3 #要修改 #X
#三个角度弹1
    def move(self): #抽象
        self.rect.top += self.speed
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul3( self.rect.center, speed,player,2,0)
        self.bul_grp.add(bullet)
        bullet2 = EnemyBul3( self.rect.center, speed,player,2,2)
        self.bul_grp.add(bullet2)
        bullet3 = EnemyBul3( self.rect.center, speed,player,2,1)
        self.bul_grp.add(bullet3)

class smallEnemy6(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy3_imgs,enemy2_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=60-random.randint(0,45))

       self.speed = 3 #要修改 #X
#三个角度弹2
    def move(self): #抽象
        self.rect.top += self.speed
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul3( self.rect.center, speed,player,-2,0)
        self.bul_grp.add(bullet)
        bullet2 = EnemyBul3( self.rect.center, speed,player,-2,2)
        self.bul_grp.add(bullet2)
        bullet3 = EnemyBul3( self.rect.center, speed,player,-2,1)
        self.bul_grp.add(bullet3)


class smallEnemy7(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy3_imgs,enemy2_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=100-random.randint(0,50))

       self.speed = 3 #要修改 #X
#从左向右，两个角度弹
    def move(self): #抽象
        self.rect.left += self.speed
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul3( self.rect.center, speed,player,1,-1)
        self.bul_grp.add(bullet)
        bullet2 = EnemyBul3( self.rect.center, speed,player,1,1)
        self.bul_grp.add(bullet2)


class smallEnemy8(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
       Enemy.__init__(self,enemy3_imgs,enemy2_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=80-random.randint(0,30))

       self.speed = 3 #要修改 #X
#从右向左，两个角度弹
    def move(self): #抽象
        self.rect.left -= self.speed
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul3( self.rect.center, speed,player,-1,-1)
        self.bul_grp.add(bullet)
        bullet2 = EnemyBul3( self.rect.center, speed,player,-1,1)
        self.bul_grp.add(bullet2)

class smallEnemy9(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
        Enemy.__init__(self,enemy4_imgs,enemy1_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=25)
        self.speed = random.randint(3,8)
    #每次都向远离的对角线行进
        if init_pos[0] < SCREEN_WIDTH/2:
            self.ratex=SCREEN_WIDTH-init_pos[0]
        else:
            self.ratex=-init_pos[0]

        if init_pos[1] < SCREEN_HEIGHT / 2:
            self.ratey = SCREEN_HEIGHT - init_pos[1]
        else:
            self.ratey = -init_pos[1]
        dis=math.sqrt(self.ratex*self.ratex+self.ratey*self.ratey)
        self.ratex,self.ratey=float(self.ratex)/dis,float(self.ratey)/dis

    def move(self): #抽象

        self.rect.left +=self.speed*self.ratex
        self.rect.top +=self.speed*self.ratey
        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul4( self.rect.center, speed,player)
        self.bul_grp.add(bullet)

class smallEnemy10(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
        Enemy.__init__(self,enemy5_imgs,enemy2_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=25)
        self.speed = 15
    #每次都绕着圆心移动
        self.rorn=random.randint(0,1)

    def move(self): #抽象
        cx,cy=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        nx,ny=self.rect.centerx,self.rect.centery
        vec1=(cx-nx,cy-ny)
        if self.rorn == 0:
            vec2=(vec1[1],-vec1[0])
        else:
            vec2=(-vec1[1],vec1[0])
        rx,ry=regulateNum(*vec2)

        self.rect.left +=self.speed*rx
        self.rect.top +=self.speed*ry
        self.imagechange()

    def shoot(self,speed,player): #抽象
        vec1=(SCREEN_WIDTH/2-self.rect.centerx,SCREEN_HEIGHT/2-self.rect.centery)
        dis=math.sqrt(vec1[0]*vec1[0]+vec1[1]*vec1[1])
        rx=vec1[0]/dis
        ry=vec1[1]/dis
        bullet = EnemyBul5( self.rect.center, speed,player,rx,ry,fdis=150)
        self.bul_grp.add(bullet)

class smallEnemy11(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
        Enemy.__init__(self,enemy6_imgs,enemy3_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=120)
        self.speed = 5
    #不定向移动
        self.constmovedist=600
        self.movedist=self.constmovedist
        self.ratex=random.randint(-10,10)
        self.ratey=random.randint(1,10)
        self.ratex,self.ratey=regulateNum(self.ratex,self.ratey)

    def move(self): #抽象
        if self.movedist > self.constmovedist/4:
            self.movedist-=self.speed
            self.rect.left += self.speed * self.ratex
            self.rect.top += self.speed * self.ratey
        elif self.movedist>0 and self.movedist<=self.constmovedist/4:
            self.movedist-=self.speed
        else:
            self.movedist=self.constmovedist
            self.ratex=random.randint(-100,100)
            self.ratey=random.randint(-100,100)
            self.ratex,self.ratey=regulateNum(self.ratex,self.ratey)
            self.rect.left += self.speed * self.ratex
            self.rect.top += self.speed * self.ratey

        self.imagechange()

    def shoot(self,speed,player): #抽象
        bullet = EnemyBul6( self.rect.center, speed,player,self.bul_grp,mdis=600)
        #bullet = EnemyBul7(self.rect.center, speed, player, 2,2,self.bul_grp)
        self.bul_grp.add(bullet)



class bossEnemy(Enemy):
    def __init__(self, init_pos, enemy_bul_grp,bul_spd):
        Enemy.__init__(self,boss_imgs,enemy2_down_imgs, init_pos,enemy_bul_grp,bul_spd,a=0,b=3,delay=4,_fq=15) #要修改,协调多个shoot
        self.ratex,self.ratey=0,0
    #phase1
        self.speed1 = 10 #要修改 #X
        self.constdist1=1500
        self.dist1=self.constdist1
        self._freqShoot1= 120
    #phase2
        self.speed2 = 4
        self.constdist2=300
        self.dist2=self.constdist2
        self._freqShoot2= 15
    #phase3
        self.speed3 = 4
        self.constdist3=500
        self.dist3=self.constdist3
        self.ph3start=False
        self._freqShoot3= 20


        self.hp = 1000
    
    #phase1
    def move1(self): #抽象
         '''
         移动方式：移动一段，然后停下来很长时间；移动的方向根据当前位置决定，如果在SCREEN.width/8 - SCREEN.width*7/8，随机左或者右方向。
         如果小于SCREEN.width/8或者大于SCREEN.width*7/8，则一定朝着反方向移动
         关于y轴移动方向，每次向上或者向下移动是完全随机的，但是如果y在SCREEN.width/8-SCREEN.width/2以外，则朝着反方向移动
         '''
         if self.dist1>self.constdist1*7/8:
             self.dist1-=self.speed1
             self.rect.left+=self.ratex*self.speed1
             self.rect.top+=self.ratey*self.speed1
         elif self.dist1>0 and self.dist1<=self.constdist1*7/8:
             self.dist1-=self.speed1*2
         else:
             cur_x,cur_y=self.rect.centerx,self.rect.centery
             if cur_x<=SCREEN_WIDTH/4:
                 self.ratex=2
             elif cur_x>=SCREEN_WIDTH*3/4:
                 self.ratex=-2
             else:
                 self.ratex=random.choice([-2,-1,1,2])

             if cur_y<=SCREEN_HEIGHT/8:
                 self.ratey=1
             elif cur_y>=SCREEN_HEIGHT*5/8:
                 self.ratey=-1
             else:
                 self.ratey=random.randint(-1,1)

             self.ratex,self.ratey=regulateNum(self.ratex,self.ratey)
             self.dist1=self.constdist1


    def shoot1(self,speed,player): #抽象
        rx,ry=player.rect.centerx-self.rect.centerx,player.rect.centery-self.rect.centery
        rx,ry=regulateNum(rx,ry)
        bullet = EnemyBul7( self.rect.center, speed,player,rx,ry,self.bul_grp)
        self.bul_grp.add(bullet)


    #phase2
    def move2(self): #抽象
         '''
         移动方式：连续缓慢移动一段距离后，会改变方向，但是不会停留
         '''
         if self.dist2>0:
             self.dist2-=self.speed2
             self.rect.left+=self.ratex*self.speed2
             self.rect.top+=self.ratey*self.speed2
         else:
             cur_x,cur_y=self.rect.centerx,self.rect.centery
             if cur_x<=SCREEN_WIDTH/4:
                 self.ratex=2
             elif cur_x>=SCREEN_WIDTH*3/4:
                 self.ratex=-2
             else:
                 self.ratex=random.choice([-2,-1,1,2])

             if cur_y<=SCREEN_HEIGHT/6:
                 self.ratey=1
             elif cur_y>=SCREEN_HEIGHT*5/8:
                 self.ratey=-1
             else:
                 self.ratey=random.randint(-1,1)

             self.ratex,self.ratey=regulateNum(self.ratex,self.ratey)
             self.dist2=self.constdist2


    def shoot2(self,speed,player): #抽象
        rx,ry=player.rect.centerx-self.rect.centerx,player.rect.centery-self.rect.centery
        rx1,ry1=regulateNum(rx,ry)
        rx2,ry2=regulateNum(rx,ry,30)
        rx3,ry3=regulateNum(rx,ry,-30)
        bullet = EnemyBul5( self.rect.center, speed,player,rx1,ry1,fdis=600)
        bullet2 =EnemyBul5( self.rect.center, speed,player,rx2,ry2,fdis=600)
        bullet3 =EnemyBul5( self.rect.center, speed,player,rx3,ry3,fdis=600)
        self.bul_grp.add(bullet)
        self.bul_grp.add(bullet2)
        self.bul_grp.add(bullet3)

    #phase2
    def move3(self): #抽象
         '''
         移动方式：连续缓慢移动一段距离后，会改变方向，但是不会停留
         '''
         if self.dist3>0:
             self.dist3-=self.speed3
             self.rect.left+=self.ratex*self.speed3
             self.rect.top+=self.ratey*self.speed3
         else:
             cur_x,cur_y=self.rect.centerx,self.rect.centery
             if cur_x<=SCREEN_WIDTH/4:
                 self.ratex=3
             elif cur_x>=SCREEN_WIDTH*3/4:
                 self.ratex=-3
             else:
                 self.ratex=random.choice([-2,-1,1,2])

             if cur_y<=SCREEN_HEIGHT/6:
                 self.ratey=1
             elif cur_y>=SCREEN_HEIGHT*6/8:
                 self.ratey=-1
             else:
                 self.ratey=random.randint(-1,1)

             self.ratex,self.ratey=regulateNum(self.ratex,self.ratey)
             self.dist3=self.constdist3


    def shoot3(self,speed,player): #抽象

        if not self.ph3start:
            bul_pos=(self.rect.centerx+100,self.rect.centery+100)
            bullet = EnemyBul8(bul_pos,8,player,self.bul_grp,self,0,sdis=100)
            self.bul_grp.add(bullet)
            bul_pos2=(self.rect.centerx-100,self.rect.centery-100)
            bullet2 = EnemyBul8(bul_pos2,8,player,self.bul_grp,self,1,sdis=100)
            self.bul_grp.add(bullet2)
            self.ph3start=True
        '''
               else:
            rx,ry=player.rect.centerx-self.rect.centerx,player.rect.centery-self.rect.centery
            rx1,ry1=regulateNum(rx,ry)
            rx2,ry2=regulateNum(rx,ry,30)
            rx3,ry3=regulateNum(rx,ry,-30)
            bullet = EnemyBul5( self.rect.center, speed,player,rx1,ry1,fdis=300)
            bullet2 =EnemyBul5( self.rect.center, speed,player,rx2,ry2,fdis=300)
            bullet3 =EnemyBul5( self.rect.center, speed,player,rx3,ry3,fdis=300)
            self.bul_grp.add(bullet)
            self.bul_grp.add(bullet2)
            self.bul_grp.add(bullet3)
        '''


