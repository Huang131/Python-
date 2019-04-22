#coding=utf-8
import time
import random
import pygame
from pygame.locals import *

#玩家飞机
class HeroPlane(object):

    def __init__(self,screen):
        #设置飞机默认位置
        self.x=230
        self.y=600
        
        #设置要显示内容的窗口
        self.screen=screen
        #玩家飞机的图片路径
        self.imagePath="./feiji/hero.gif"
        #根据路径生成图片
        self.image=pygame.image.load(self.imagePath).convert()
        
        #用来保存玩家飞机发出的子弹
        self.bulletList = []

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))
        needDelItemList = []

        #保存需要删除的对象信息
        for bullet in self.bulletList:
            if bullet.judge():
                needDelItemList.append(bullet)
        #删除self.bulletList中需要删除的对象
        for item in needDelItemList:
            self.bulletList.remove(item)

        for bullet in self.bulletList:
            bullet.display()
            bullet.move()

    def moveLeft(self):
        self.x -=10

    def moveRight(self):
        self.x +=10

    def sheBullet(self):
        newBullet = Bullet(self.x,self.y,self.screen)
        self.bulletList.append(newBullet)


# 子弹类
class Bullet(object):
    def __init__(self,x,y,screen):
        self.x = x+40
        self.y = y-20
        self.screen=screen
        self.image=pygame.image.load("./feiji/bullet-3.gif").convert()

    def move(self):
        self.y -=2

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))

    def judge(self):
        if self.y<0:
            return True
        else:
            return False

# 敌人飞机
class Enemplane(object):
    def __init__(self,screen):
        #设置敌机默认位置
        self.x=0
        self.y=0

        #设置要显示内容的窗口
        self.screen=screen

        self.imagePath='./feiji/enemy-1.gif'
        self.image = pygame.image.load(self.imagePath).convert()

        #敌机子弹
        self.bulletList=[]

        self.direction = 'right'

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))
        needDelItemList = []

        #保存需要删除的对象信息
        for bullet in self.bulletList:
            if bullet.judge():
                needDelItemList.append(bullet)
        #删除self.bulletList中需要删除的对象
        for item in needDelItemList:
            self.bulletList.remove(item)

        for bullet in self.bulletList:
            bullet.display()
            bullet.move() 

    def move(self):   
        if self.direction == 'right':
            self.x +=2
        elif self.direction == 'left':
            self.x -=2
        
        if self.x>480-50:
            self.direction ='left'
        elif self.x<0:
            self.direction = 'right'

    def sheBullet(self):
        num = random.randint(1,100)
        if num ==88:
            newBullet = EnemyBullet(self.x,self.y,self.screen)
            self.bulletList.append(newBullet)

class EnemyBullet(object):
    def __init__(self,x,y,screen):
        self.x = x+30
        self.y = y+30
        self.screen = screen
        self.image=pygame.image.load("./feiji/bullet-1.gif").convert()
    def move(self):
        self.y +=2

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))
    
    def judge(self):
        if self.y>890:
            return True
        else:
            return False


if __name__ == "__main__":

    #1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480,890),0,32)

    #2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()

    #创建一个飞机对象
    heroPlane=HeroPlane(screen)
    
    #创建一个敌人飞机
    enemplane = Enemplane(screen)


    while True:
        screen.blit(background,(0,0))

        heroPlane.display()

        enemplane.move()
        enemplane.sheBullet()
        enemplane.display()

        #判断是否点击了退出按钮
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
                    heroPlane.sheBullet()

        #通过延时来降低速度
        time.sleep(0.01)
        pygame.display.update()
