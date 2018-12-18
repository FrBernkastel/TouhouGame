# -*- coding: utf-8 -*-
import pygame
import math

def transformScale(img,scale):
    width,height=img.get_size()
    return pygame.transform.scale(img, (int(width * scale), int(height * scale)))

def regulateNum(x1,y1,theta=0):
    if theta!=0:
        costheta=math.cos(theta*math.pi/180.0)
        sintheta=math.sin(theta*math.pi/180.0)
        x,y=costheta*x1-sintheta*y1,sintheta*x1+costheta*y1
    else:
        x,y=x1,y1
    dis=math.sqrt(x*x+y*y)
    return float(x)/dis,float(y)/dis