#coding=utf-8
import pygame
from pygame.locals import *

'''
    1. 搭建界面，主要完成窗口和背景图的显示
'''

class HeroPlane(object):
    def __init__(self,screen):
        #设置飞机默认位置
        self.x=230
        self.y=600

        self.screen=screen

        self.imageName="./feiji/hero.gif"

        self.image=pygame.image.load(self.imageName).convert()
        
        self.bullet = []


    def display(self):
        self.screen.blit(self.image,(self.x,self.y))
    def moveLeft(self):
        self.x -=10
    def moveRight(self):
        self.x +=10
    def sheBullet(self):
        pass


if __name__ == "__main__":

    #1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480,890),0,32)

    #2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()

    #飞机一个飞机对象
    heroPlane=HeroPlane(screen)
    

    while True:
        screen.blit(background,(0,0))

        heroPlane.display()

        for event in pygame.event.get():
            if event.type == QUIT:
                print('exit')
                exit()
            elif event.type == KEYDOWN:
                if   event.key == K_a or event.key == K_LEFT:
                      print('left')
                      heroPlane.moveLeft()
                elif event.key == K_d or event.key == K_RIGHT:    
                      print('right')
                      heroPlane.moveRight()
                elif event.key == K_SPACE:
                    print('space')
        pygame.display.update()
