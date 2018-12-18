# -*- coding: utf-8 -*-
import pygame

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')

enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
bullet_sound.set_volume(0.3)

pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)