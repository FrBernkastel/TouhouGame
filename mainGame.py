# -*- coding: utf-8 -*-
"""
Created By Pan Yancen.
2017/4/20
Jilin University.
"""

import pygame
from sys import exit
from pygame.locals import *
from EnemyRole import *
from BulletRole import *
from GlobalParameter import *
from PlayerRole import Player
from SoundRes import *
from util import transformScale
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



'''
*********************
游戏系统级别参数
*********************
'''
x = 200
y = 25
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)


'''
*********************
游戏资源定义区
*********************
'''
# 初始化游戏 (screen)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TouHou Project2')



# 载入背景图 (background,game_over)
background = transformScale(pygame.image.load('resources/image/background.jpg').convert(),ContractRate)
game_over = transformScale(pygame.image.load('resources/image/gameover.png'),ContractRate)
start_page = transformScale(pygame.image.load('resources/image/start_page.png').convert(),0.85)
win_game = pygame.image.load('resources/image/win_game.png').convert()
'''
****************************
全局的对象
****************************
'''
player_pos = [SCREEN_WIDTH/2, SCREEN_HEIGHT*7/8]
player=Player(player_pos)

enemies1 = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()
enemy_bul_grp = pygame.sprite.Group()

clock = pygame.time.Clock()

score=0
running = False
is_win = False
enemy_frequency = 0
clock_cnt=0

'''
****************************
游戏流程参数：
****************************
'''
'''
游戏难度控制：
敌人的密集程度
敌人的射击频率
敌人的射击速度
敌人本身移动的速度
'''


_freqEnemy=15
_freqEnemy2=50
_freqEnemy3=40
_freqEnemy4=80



'''
***************************
游戏流程
***************************
'''
def StartGame():
    clock_count=0
    clock = pygame.time.Clock()
    player_filename = 'resources/image/player.png'
    player_img = pygame.image.load(player_filename)
    sprites = []
    for i in range(8):
        sprites.append(player_img.subsurface(pygame.Rect(32*i, 0, 32, 48)).convert_alpha())
    position = [player.rect.centerx,player.rect.centery]
    heading = []
    dly = 5
    decdly = dly
    img_ind = 0
    starting = 0   #0为开始游戏，1为BOSS战，2为退出游戏
    while True:
        clock.tick(50)
        clock_count+=1
        screen.fill(0)
        screen.blit(start_page, (0, 0))
        decdly -= 1
        if decdly == 0:
            img_ind += 1
            decdly = dly
        if img_ind > 7:
            img_ind = 0
        # 魔法少女会趋向于鼠标所指位置移动
        sprite = sprites[img_ind]
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 100.0

        tmp1=pygame.mouse.get_pos()
        tmp2=sprite.get_size()
        tmp2=[tmp2[0]/2,tmp2[1]/2]

        destination = [tmp1[0]-tmp2[0],tmp1[1]-tmp2[1]]
        vector_to_mouse = [position[0]-destination[0],position[1]-destination[1]]

        vector_to_mouse=regulateNum(vector_to_mouse[0],vector_to_mouse[1])
        heading = heading + ([vector_to_mouse[0] * .5,vector_to_mouse[1] * .5])
        position[0] += heading[0] * time_passed_seconds
        position[1] += heading[1] * time_passed_seconds
        if position[0] < 0:
            position[0] = 0
        if position[1] < 0:
            position[1] = 0
        if position[0] > SCREEN_WIDTH - sprite.get_size()[0]:
            position[0] = SCREEN_WIDTH - sprite.get_size()[0]
        if position[1] > SCREEN_HEIGHT - sprite.get_size()[1]:
            position[1] = SCREEN_HEIGHT - sprite.get_size()[1]
        screen.blit(sprite, position)
        # 开始与退出
        font1 = pygame.font.SysFont('微软雅黑', 48)
        font2 = pygame.font.SysFont('微软雅黑', 36)
        rect = [SCREEN_WIDTH/7,SCREEN_HEIGHT*0.6]
        if starting==0:
            start_text = font1.render(u'开始', True, (255, 0, 0))
            rect[0] += 50
        else:
            start_text = font2.render(u'开始', True, (255, 255, 255))
            rect[0] += 60
        rect[1] += 36
        screen.blit(start_text, rect)
        if starting==1:
            boss_text = font1.render(u'Boss战', True, (255, 0, 0))
            rect[0] -= 20
        else:
            boss_text = font2.render(u'Boss战', True, (255, 255, 255))
            rect[0] += 20
        rect[1] += 72
        screen.blit(boss_text, rect)
        if starting==2:
            quit_text = font1.render(u'退出', True, (255, 0, 0))
            rect[0] -= 20
        elif starting==1:
            quit_text = font2.render(u'退出', True, (255, 255, 255))
            rect[0] += 50
        else:
            quit_text = font2.render(u'退出', True, (255, 255, 255))
            rect[0] += 20
        rect[1] += 72
        screen.blit(quit_text, rect)
        key_press = pygame.key.get_pressed()
        if starting==0 and key_press[K_RETURN]:
            return 0
        if starting==1 and key_press[K_RETURN]:
            return 1
        if starting==2 and key_press[K_RETURN]:
            pygame.quit()
            exit()
        if  clock_count%4==0 and key_press[K_DOWN]:
            starting =(starting+1)%3
        if  clock_count%4==0 and key_press[K_UP]:
            starting =(starting-1)%3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()

def InitGame():
    player_pos = [SCREEN_WIDTH/2, SCREEN_HEIGHT*7/8]
    player.drawrect.center=player_pos
    player.ModiRect()
    player.down_imgidx = 0
    player.shoot_frequency=0
    player.is_hit=False

    enemies1.empty()
    enemies_down.empty()
    enemy_bul_grp.empty()

    global score
    global running
    global enemy_frequency
    global clock_cnt
    score=0
    running=True
    enemy_frequency = 0
    clock_cnt =0

def RunGame():
    global clock_cnt
    global score
    global running
    global is_win
    #用于boss控制
    mode=0
    while running:
        clock.tick(60)
        clock_cnt +=1
        time_cnt=getCurrentTime(clock_cnt)


        if(time_cnt<2):
            EnemyPattern1(SCREEN_WIDTH-20)
        if(2<time_cnt<4):
            EnemyPattern1(SCREEN_WIDTH/2)
        if(4<time_cnt<6):
            EnemyPattern1(20)
        if(6<time_cnt<8):
             EnemyPattern1(SCREEN_WIDTH/4)
        if(8<time_cnt<10):
            EnemyPattern1(SCREEN_WIDTH*3/4)
        if(12<time_cnt<15):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern2(heiht)
        if(15<time_cnt<18):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern3(heiht)
        if(18<time_cnt<21):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern2(heiht)
        if(21<time_cnt<24):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern3(heiht)
        if(24<time_cnt<27):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern2(heiht)
        if(27<time_cnt<30):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern3(heiht)
        if(30<time_cnt<33):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern2(heiht)
        if(33<time_cnt<36):
            heiht=random.randint(0,SCREEN_HEIGHT/2)
            EnemyPattern3(heiht)
        if(36<time_cnt<46):
            EnemyPattern4()
        if(48<time_cnt<60):
            EnemyPattern5()

        if (62 < time_cnt < 85):
            EnemyPattern6()
        if (90 < time_cnt <110):
            EnemyPattern7()
        if (113<time_cnt<135):
            EnemyPattern8()
        if (time_cnt == 140):
            BulClear()
            EnemyClear()

        if time_cnt == 150:
            mode = 1
            BossPhase1()
        # 不考虑优雅了，boss在这里单独处理吧，我先睡了
        if mode != 0:
            for enemy in enemies1:
                if isinstance(enemy, bossEnemy):
                    if enemy.hp == 600:
                        mode = 2
                    if enemy.hp == 400:
                        mode = 3
                    if enemy.hp == 0:
                        score = 99999999
                        running = False
                        is_win = True
        MoveAndCheck(mode)
        DrawEverything()
        KeyBoardControl()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def RunBossGame():
    global clock_cnt
    global score
    global running
    global is_win
    #用于boss控制
    mode=0
    while running:
        clock.tick(60)
        clock_cnt +=1
        time_cnt=getCurrentTime(clock_cnt)
        # if(time_cnt<2):
        #     EnemyPattern1(SCREEN_WIDTH-20)
        # if(2<time_cnt<4):
        #     EnemyPattern1(SCREEN_WIDTH/2)
        # if(4<time_cnt<6):
        #     EnemyPattern1(20)
        # if(6<time_cnt<8):
        #     EnemyPattern1(SCREEN_WIDTH/4)
        # if(8<time_cnt<10):
        #     EnemyPattern1(SCREEN_WIDTH*3/4)
        # if(12<time_cnt<15):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern2(heiht)
        # if(15<time_cnt<18):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern3(heiht)
        # if(18<time_cnt<21):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern2(heiht)
        # if(21<time_cnt<24):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern3(heiht)
        # if(24<time_cnt<27):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern2(heiht)
        # if(27<time_cnt<30):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern3(heiht)
        # if(30<time_cnt<33):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern2(heiht)
        # if(33<time_cnt<36):
        #     heiht=random.randint(0,SCREEN_HEIGHT/2)
        #     EnemyPattern3(heiht)
        # if(36<time_cnt<46):
        #     EnemyPattern4()
        # if(48<time_cnt<60):
        #     EnemyPattern5()

        # if (62 < time_cnt < 85):
        #     EnemyPattern6()
        # if (90 < time_cnt <110):
        #     EnemyPattern7()
        # if (113<time_cnt<135):
        #     EnemyPattern8()
        # if (time_cnt == 140):
        #     BulClear()
        #     EnemyClear()
        # 这是单独测试boss部分，你把前面的取消注释就行了
        # 把boss的血改成1直接可以看wingame的背景图
        if time_cnt == 2:
            mode = 1
            BossPhase1()
        # 不考虑优雅了，boss在这里单独处理吧，我先睡了
        if mode != 0:
            for enemy in enemies1:
                if isinstance(enemy, bossEnemy):
                    if enemy.hp == 600:
                        mode = 2
                    if enemy.hp == 400:
                        mode = 3
                    if enemy.hp == 0:
                        score = 99999999
                        running = False
                        is_win = True
        MoveAndCheck(mode)
        DrawEverything()
        KeyBoardControl()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def LoseGame():
    font = pygame.font.Font(None, 70)
    text = font.render('Score:      '+ str(score), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 100
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)

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

def WinGame():
    font = pygame.font.Font(None, 70)
    text = font.render('Score:      '+ str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx+70
    text_rect.centery = screen.get_rect().centery+20
    screen.blit(win_game, (0, 0))
    screen.blit(text, text_rect)
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

'''
*****************************
RunGame子流程
*****************************
'''
def getCurrentTime(clock_cnt):
    return float(clock_cnt)/60
#Core Code: 敌人进攻的模式

def EnemyPattern1(x_pos):
    global enemy_frequency
# 生成敌机
    if enemy_frequency % _freqEnemy == 0:
        enemy_pos = [x_pos,0]
        enemy1 = smallEnemy(enemy_pos, enemy_bul_grp,6)
        enemies1.add(enemy1)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy:
        enemy_frequency = 0

def EnemyPattern2(y_pos):
    global enemy_frequency
# 生成敌机
    if enemy_frequency % _freqEnemy == 0:
        enemy_pos = [0,y_pos]
        enemy1 = smallEnemy3(enemy_pos, enemy_bul_grp,6)
        enemies1.add(enemy1)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy:
        enemy_frequency = 0

def EnemyPattern3(y_pos):
    global enemy_frequency
# 生成敌机
    if enemy_frequency % _freqEnemy == 0:
        enemy_pos = [SCREEN_WIDTH,y_pos]
        enemy1 = smallEnemy4(enemy_pos, enemy_bul_grp,6)
        enemies1.add(enemy1)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy:
        enemy_frequency = 0

def EnemyPattern4():
    global enemy_frequency
# 生成敌机
    if enemy_frequency % _freqEnemy2 == 0:
        enemy_pos = [[SCREEN_WIDTH/4,0],[SCREEN_WIDTH*3/4,0]]
        enemy1 = smallEnemy5(enemy_pos[0], enemy_bul_grp,3)
        enemies1.add(enemy1)
        enemy2 = smallEnemy6(enemy_pos[1], enemy_bul_grp,3)
        enemies1.add(enemy2)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy2:
        enemy_frequency = 0

def EnemyPattern5():
    global enemy_frequency
# 生成敌机
    if enemy_frequency % _freqEnemy2 == 0:
        enemy_pos = [[0,SCREEN_HEIGHT/2],[SCREEN_WIDTH,SCREEN_HEIGHT/2]]
        enemy1 = smallEnemy7(enemy_pos[0], enemy_bul_grp,6)
        enemy2 = smallEnemy8(enemy_pos[1], enemy_bul_grp,6)
        enemies1.add(enemy1)
        enemies1.add(enemy2)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy2:
        enemy_frequency = 0

def EnemyPattern6():
    global enemy_frequency
# 生成敌机
    if enemy_frequency % _freqEnemy3 == 0:
        enemy_pos = [SCREEN_WIDTH/5+random.randint(0,SCREEN_WIDTH*3/5),SCREEN_HEIGHT/5+random.randint(0,SCREEN_HEIGHT*3/5)]
        enemy1 = smallEnemy9(enemy_pos, enemy_bul_grp,10)
        enemies1.add(enemy1)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy3:
        enemy_frequency = 0

def EnemyPattern7():
    global enemy_frequency
# 生成敌机,特殊：
    #固定一个半径值，随机化一个角度后，再求出生成的位置
    rad=SCREEN_HEIGHT/2-20
    if enemy_frequency % _freqEnemy3 == 0:
        theta=random.randint(0,360)
        theta2=theta*math.pi/180
        enemy_pos=(SCREEN_WIDTH/2+rad*math.cos(theta2),SCREEN_HEIGHT/2+rad*math.sin(theta2))
        enemy1 = smallEnemy10(enemy_pos, enemy_bul_grp,15)
        enemies1.add(enemy1)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy3:
        enemy_frequency = 0

def EnemyPattern8():
    global enemy_frequency
# 生成敌机,特殊：
    #随机出现在窗口的上半部分
    if enemy_frequency % _freqEnemy4 == 0:

        enemy_pos=(random.randint(SCREEN_WIDTH/4,SCREEN_WIDTH/4*3),random.randint(SCREEN_HEIGHT/8,SCREEN_HEIGHT/2))
        enemy1 = smallEnemy11(enemy_pos, enemy_bul_grp,4)
        enemies1.add(enemy1)

    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy4:
        enemy_frequency = 0

def BossPhase1():
    enemy_pos=(SCREEN_WIDTH/2,SCREEN_HEIGHT/4)
    boss = bossEnemy(enemy_pos,enemy_bul_grp,6)
    enemies1.add(boss)

def BossPhase2():
    enemy_pos=(SCREEN_WIDTH/2,SCREEN_HEIGHT/4)
    boss = bossEnemy(enemy_pos,enemy_bul_grp,10)
    enemies1.add(boss)

def BossPhase3():
    enemy_pos=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    boss = bossEnemy(enemy_pos,enemy_bul_grp,14)
    enemies1.add(boss)

#具有death属性的子弹
def BulClear():
    for bul in enemy_bul_grp:
        bul.death=True

#杀死全部敌人
def EnemyClear():
    for ene in enemies1:
        enemies_down.add(ene)
        enemies1.remove(ene)


def MoveAndCheck(mode=0):
    # 所有敌机发出子弹
    for enm in enemies1:
        enm.tryshot(player,mode=mode)
    # 移动子弹，若超出窗口范围则删除,!!同时判定是否攻击到了自机
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    for bullet in enemy_bul_grp:
        bullet.move()
        if pygame.sprite.collide_circle(bullet, player):
            player.is_hit = True
            game_over_sound.play()
        if bullet.rect.bottom < -300 or bullet.rect.top > SCREEN_HEIGHT+300 or bullet.rect.right <-300 or bullet.rect.left>SCREEN_WIDTH+300:
            enemy_bul_grp.remove(bullet)

    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies1:
        if mode ==0:
            enemy.move()
        if mode ==1:
            enemy.move1()
        if mode ==2:
            enemy.move2()
        if mode ==3:
            enemy.move3()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT+30 or enemy.rect.bottom<-30 or enemy.rect.right<-30 or enemy.rect.left>SCREEN_WIDTH+30:
            enemies1.remove(enemy)


    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画 !!!可以给所有对象加HP

    if mode == 0:
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)

    else:
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 0, 1)
        for enemy_down in enemies1_down:
            enemy_down.hp -= 1
            if enemy_down.hp == 0:
                enemies_down.add(enemy_down)

def DrawEverything():
    global score
    global running
#绘图部分
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
    for enemy in enemies1:
        if isinstance(enemy, bossEnemy):
            rect = Rect(enemy.rect.left, enemy.rect.top+10, enemy.rect.width*(enemy.hp)/1000.0, 10)
            pygame.draw.rect(screen, (255,0,0), rect)
    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # !!!!更新屏幕
    pygame.display.update()

def KeyBoardControl():
    # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
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

            # 控制发射子弹频率,并发射子弹
            if key_pressed[K_z]:
                player.tryshot(mod)

def main():
    while 1:
        mode=StartGame()
        InitGame()
        if mode == 0:
            RunGame()
        if mode == 1:
            RunBossGame()
        if not is_win:
            LoseGame()
        else:
            WinGame()





if __name__ == "__main__":
    main()



'''
def EnemyPattern1():
    global enemy_frequency
# 生成敌机
    if enemy_frequency % _freqEnemy == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_imgs[0].get_rect().width), 0]
        enemy1 = smallEnemy(enemy1_pos, enemy_bul_grp)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= _freqEnemy:
        enemy_frequency = 0
# 所有敌机发出子弹
    for enm in enemies1:
        enm.tryshot(10,player)
'''
