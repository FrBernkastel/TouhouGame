# -*- coding: UTF-8 -*-
import pygame
import math
import random
from util import *
from GlobalParameter import *


filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)
bullet_filename='resources/image/bullet.png'
bullet_img0 = pygame.image.load(bullet_filename)
bullet_filename2='resources/image/bullet2.png'
bullet_img1 = pygame.image.load(bullet_filename2)
bullet_filename3='resources/image/bullet3.png'
bullet_img2 = pygame.image.load(bullet_filename3)
bullet_filename2 = 'resources/image/bullet/bulletf.png'
bullet_imgf = pygame.image.load(bullet_filename2)
# 子弹素材
bullet_rect = pygame.Rect(1004, 987, 9, 21)

bullet_img = plane_img.subsurface(bullet_rect)
# player快速子弹素材
bullet_imgfs = []
for i in range(8):
    bullet_imgfs.append(bullet_imgf.subsurface(pygame.Rect(32*i+11, 96, 10, 32)))

ebullet1_imgs=[]
for i in range(16):
    ebullet1_imgs.append(transformScale(bullet_img0.subsurface(pygame.Rect(16*i+4,96,8,16)),1.5))

ebullet2_imgs=[]
itrlist=[[15,0],[1,2],[3,4],[5,6],[7,8],[9,10],[11,12],[13,14]]
for i in range(8):
    temp=[]
    temp.append(transformScale(bullet_img0.subsurface(pygame.Rect(16*itrlist[i][0],160,16,16)),1.5))
    temp.append(transformScale(bullet_img0.subsurface(pygame.Rect(16*itrlist[i][1],160,16,16)),1.5))
    ebullet2_imgs.append(temp)

ebullet3_imgs=[]
for i in range(8):
    ebullet3_imgs.append(pygame.transform.rotate(transformScale(bullet_img0.subsurface(pygame.Rect(32*i,208,32,32)),1.5),360/8*i))

ebullet4_imgs=[]
for i in range(8):
    temp=[]
    temp.append(transformScale(bullet_img0.subsurface(pygame.Rect(16*itrlist[i][0],32,16,16)),1.5))
    temp.append(transformScale(bullet_img0.subsurface(pygame.Rect(16*itrlist[i][1],32,16,16)),1.5))
    ebullet4_imgs.append(temp)

ebullet5_imgs=[]
for i in range(8):
    temp=[]
    temp.append(transformScale(bullet_img0.subsurface(pygame.Rect(16*itrlist[i][0],16*7,16,16)),1.5))
    temp.append(transformScale(bullet_img0.subsurface(pygame.Rect(16*itrlist[i][1],16*7,16,16)),1.5))
    ebullet5_imgs.append(temp)

ebullet6_imgs=[]
for i in range(9):
    ebullet6_imgs.append(transformScale(bullet_img1.subsurface(pygame.Rect(128*i,0,128,128)),1.2))

ebullet7_imgs=[]
for i in range(9):
    ebullet7_imgs.append(transformScale(bullet_img2.subsurface(pygame.Rect(128*i,0,128,128)),1.5))

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
        self.rect.center = init_pos

        self.dg=0

        self.imgidxa=a
        self.imgidxb=b
        self.imgidx = a
        self.imagelist=imgs
        self.image = imgs[a]
        self.dly=delay
        self.dlyrt=self.dly
    #冗余属性
        self.death=False

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

    def FollowPlayer(self,player_pos):
        Bul_pos=self.rect.center
        disx=player_pos[0]-Bul_pos[0]
        disy=player_pos[1]-Bul_pos[1]
        dis=math.sqrt(disx*disx+disy*disy)
        ratex=disx/dis
        ratey=disy/dis
        return ratex,ratey


class PlayerBul(Bullet):
    def __init__(self, init_pos): #
        Bullet.__init__(self, [bullet_img], init_pos)
        self.speed = 50
    def move(self):
        self.rect.top -= self.speed

class PlayerBulF(Bullet):
    left_offsets = [-.2, 0, 0, .2]
    def __init__(self, init_pos, img_ind):
        Bullet.__init__(self, [bullet_imgfs[img_ind]], init_pos)
        self.speed = 50
        self.img_ind = img_ind
    def move(self):
        self.rect.top -= self.speed
        self.rect.left += (self.left_offsets[self.img_ind-1])*self.speed

#自机狙
class EnemyBul1(Bullet):
    def __init__(self,  init_pos, spd, player):
        Bullet.__init__(self,ebullet2_imgs[random.randint(0,7)], init_pos,a=0,b=1,delay=5)

        self.speed = spd
        #引入成员函数self.ratex,self.ratey
        self.ratex,self.ratey=self.FollowPlayer(player.rect.center)


    def move(self):
        self.rect.left += self.speed*self.ratex
        self.rect.top += self.speed*self.ratey
        self.imagechange()


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




#方向弹
class EnemyBul3(Bullet):
    def __init__(self, init_pos, spd, player,rx,ry):
        Bullet.__init__(self,[ebullet3_imgs[random.randint(0,7)]],  init_pos,a=0,b=0,delay=30)
        self.speed = spd
        self.ratex,self.ratey=rx,ry

        self.target=player


    def move(self):
        self.rect.left+=self.speed*self.ratex
        self.rect.top+=self.speed*self.ratey
        self.imagechange()

#高速自机狙击
class EnemyBul4(Bullet):
    def __init__(self,  init_pos, spd, player,fdis=250):
        Bullet.__init__(self,ebullet4_imgs[random.randint(0,7)], init_pos,a=0,b=1,delay=5)

        self.speed = spd
        self.slowspeed = 4
        #引入成员函数self.ratex,self.ratey
        self.ratex,self.ratey=self.FollowPlayer(player.rect.center)
        self.fastdis=fdis


    def move(self):
        tempspeed=self.slowspeed
        if self.fastdis>0:
            tempspeed = self.speed
            self.fastdis-=tempspeed

        self.rect.left += tempspeed*self.ratex
        self.rect.top += tempspeed*self.ratey
        self.imagechange()

#高速方向弹
class EnemyBul5(Bullet):
    def __init__(self,  init_pos, spd, player,rx,ry,fdis=250):
        Bullet.__init__(self,ebullet5_imgs[random.randint(0,7)], init_pos,a=0,b=1,delay=2)

        self.speed = spd
        self.slowspeed = 4
        #引入成员函数self.ratex,self.ratey
        self.ratex,self.ratey=rx,ry
        self.fastdis=fdis


    def move(self):
        tempspeed=self.slowspeed
        if self.fastdis>0:
            tempspeed = self.speed
            self.fastdis-=tempspeed

        self.rect.left += tempspeed*self.ratex
        self.rect.top += tempspeed*self.ratey
        self.imagechange()

#巨型魔法阵, 定向变速，生成子弹
class EnemyBul6(Bullet):
    def __init__(self,  init_pos, spd, player,bul_grp,mdis=50):
        Bullet.__init__(self,ebullet6_imgs, init_pos,a=0,b=8,delay=1)
        self.speed = spd
        #引入成员函数self.ratex,self.ratey
        self.ratex,self.ratey=regulateNum(*self.FollowPlayer(player.rect.center))
        self.constdist=mdis
        self.dist=self.constdist
        self.bul_grp=bul_grp
    #防止子弹始终存在
        self.death = False

    def move(self):
        if not self.death:
            if self.dist > self.constdist/3:
                self.dist-=self.speed
                self.rect.left += self.speed * self.ratex
                self.rect.top += self.speed * self.ratey
            elif self.dist <=self.constdist/3 and self.dist > 0:
                self.dist-=self.speed
            else:
                div_bul_num=4
                for i in range(div_bul_num):
                    dg=360.0/div_bul_num*i/180*math.pi
                    ratex,ratey=math.cos(dg),math.sin(dg)
                    tmp_bul=EnemyBul5(self.rect.center,6,0,ratex,ratey,fdis=150)
                    self.bul_grp.add(tmp_bul)
                self.ratex+=random.randint(-1,1)
                self.ratey+=random.randint(-1,1)
                self.ratex,self.ratey=regulateNum(self.ratex,self.ratey)
                self.dist=self.constdist
                self.rect.left += self.speed * self.ratex
                self.rect.top += self.speed * self.ratey
        else:
            self.rect.left+=self.speed*self.ratex
            self.rect.top+=self.speed*self.ratey
        self.imagechange()


#巨型子弹, 定向反弹，生成子弹
class EnemyBul7(Bullet):
    def __init__(self,  init_pos, spd, player,rx,ry,bul_grp):
        Bullet.__init__(self,ebullet7_imgs, init_pos,a=0,b=8,delay=1)
        self.speed = spd
        #引入成员函数self.ratex,self.ratey
        self.ratex,self.ratey=rx,ry

        self.bul_grp=bul_grp

        self.bonstimes=5
        self.firstbounce=False


    def move(self):
        '''
        if self.dist > self.constdist/3:
            self.dist-=self.speed
            self.rect.left += self.speed * self.ratex
            self.rect.top += self.speed * self.ratey
        elif self.dist <=self.constdist/3 and self.dist > 0:
            self.dist-=self.speed
        else:
            div_bul_num=4
            for i in range(div_bul_num):
                dg=360.0/div_bul_num*i/180*math.pi
                ratex,ratey=math.cos(dg),math.sin(dg)
                tmp_bul=EnemyBul5(self.rect.center,6,0,ratex,ratey,fdis=150)
                self.bul_grp.add(tmp_bul)
            self.ratex+=random.randint(-1,1)
            self.ratey+=random.randint(-1,1)
            self.ratex,self.ratey=regulateNum(self.ratex,self.ratey)
            self.dist=self.constdist
        '''

        if self.bonstimes>0:
            if self.rect.left < 0:
                self.ratex=-self.ratex
                self.bonstimes-=1
            if self.rect.right> SCREEN_WIDTH:
                self.ratex=-self.ratex
                self.bonstimes-=1
            if self.rect.bottom > SCREEN_HEIGHT:
                self.ratey=-self.ratey
                self.bonstimes-=1
            if self.rect.top < 0:
                self.ratey=-self.ratey
                self.bonstimes-=1


        self.rect.left += self.speed * self.ratex
        self.rect.top += self.speed * self.ratey

        self.imagechange()


#巨型魔法阵EX, 绕着Boss旋转，生成子弹
class EnemyBul8(Bullet):
    def __init__(self,  init_pos, spd, player,bul_grp,boss,dir,sdis=250): #传入了boss
        Bullet.__init__(self,ebullet6_imgs, init_pos,a=0,b=8,delay=1)
        self.speed = spd
        #引入成员函数self.ratex,self.ratey
        self.ratex,self.ratey=regulateNum(*self.FollowPlayer(player.rect.center))
        self.constdist=sdis
        self.dist=self.constdist
        self.bul_grp=bul_grp
    #防止子弹始终存在
        self.death = False

    #为了保持和boss同步，设立一个bosspos
        self.bossoldpos=boss.rect.center
        self.boss=boss
    #方向
        self.dir=dir

    def move(self):
        if not self.death:
            if self.dist > 0:
                self.dist-=self.speed
            else:
                div_bul_num=6
                for i in range(div_bul_num):
                    dg=360.0/div_bul_num*i/180*math.pi
                    ratex,ratey=math.cos(dg),math.sin(dg)
                    tmp_bul=EnemyBul5(self.rect.center,6,0,ratex,ratey,fdis=150)
                    self.bul_grp.add(tmp_bul)
                self.dist=self.constdist
            #每次绕着boss移动
            #首先根据上一次boss的移动情况，给这个魔法阵一个相同的偏移
            firstvec=(self.boss.rect.centerx-self.bossoldpos[0],self.boss.rect.centery-self.bossoldpos[1])
            self.rect.centerx+=firstvec[0]
            self.rect.centery+=firstvec[1]
            #接着，同原来的算法，计算应该旋转的角度，原来的方向向量伪self.ratex,self.ratey，经过计算.
            cx, cy = (self.boss.rect.centerx,self.boss.rect.centery)
            nx, ny = self.rect.centerx, self.rect.centery
            vec1 = (cx - nx, cy - ny)
            if self.dir==0:
                vec2 = (vec1[1], -vec1[0])
            else:
                vec2=(-vec1[1],vec1[0])
            rx,ry=regulateNum(*vec2)
            self.rect.left += self.speed * rx
            self.rect.top += self.speed * ry
            self.bossoldpos=self.boss.rect.center
        else:
            self.rect.left+=self.speed*self.ratex
            self.rect.top+=self.speed*self.ratey
        self.imagechange()