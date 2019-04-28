#coding=utf-8
import time
import random
import pygame
from pygame.locals import *


class Base(object):
    def __init__(self, name, screen):
        self.name = name
        self.screen = screen


#飞机子弹
class PublicBullet(Base):
    def __init__(self, x, y, planeName, screen):

        super().__init__(planeName, screen)
        if self.name == "hero":
            self.x = x + 40
            self.y = y - 20
            imagePath = "./feiji/bullet-3.gif"
        elif self.name == "enemy":
            self.x = x + 40
            self.y = y + 30
            imagePath = "./feiji/bullet-1.gif"

        self.image = pygame.image.load(imagePath).convert()

    def move(self):
        if self.name == "hero":
            self.y -= 2
        elif self.name == "enemy":
            self.y += 2

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def judge(self):
        if self.y > 890 or self.y < 0:
            return True
        else:
            return False


#飞机基类
class Plane(Base):
    def __init__(self, name, screen, imagePath):
        super().__init__(name, screen)
        self.imagePath = imagePath
        self.image = pygame.image.load(self.imagePath).convert()
        self.bulletList = []

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

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

    def sheBullet(self):
        newBullet = PublicBullet(self.x, self.y, self.name, self.screen)
        self.bulletList.append(newBullet)


#玩家飞机
class HeroPlane(Plane):
    def __init__(self, name, screen):
        #设置飞机默认位置
        self.x = 230
        self.y = 600

        #玩家飞机的图片路径
        self.imagePath = "./feiji/hero.gif"
        super().__init__(name, screen, self.imagePath)

    def moveLeft(self):
        self.x -= 10

    def moveRight(self):
        self.x += 10


#敌人飞机
class Enemplane(Plane):
    def __init__(self, name, screen):
        #设置敌机默认位置
        self.x = 0
        self.y = 0

        self.imagePath = './feiji/enemy-1.gif'
        super().__init__(name, screen, self.imagePath)
        self.direction = 'right'

    def move(self):
        if self.direction == 'right':
            self.x += 2
        elif self.direction == 'left':
            self.x -= 2

        if self.x > 480 - 50:
            self.direction = 'left'
        elif self.x < 0:
            self.direction = 'right'

    def sheBullet(self):
        num = random.randint(1, 100)
        if num == 88:
            super().sheBullet()


#键盘控制
def key_control(heroPlane):
    #获取事件
    for event in pygame.event.get():
        #是否退出
        if event.type == QUIT:
            print('exit')
            exit()
        #是否点击键盘
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                heroPlane.moveLeft()
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                heroPlane.moveRight()
            elif event.key == K_SPACE:
                print('space')
                heroPlane.sheBullet()


def main():
    #1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480, 890), 0, 32)

    #2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()

    #创建一个飞机对象
    heroPlane = HeroPlane("hero", screen)

    #创建一个敌人飞机
    enemplane = Enemplane("enemy", screen)

    while True:
        screen.blit(background, (0, 0))
        heroPlane.display()
        enemplane.display()
        enemplane.move()
        enemplane.sheBullet()
        pygame.display.update()
        key_control(heroPlane)
        #通过延时来降低速度
        time.sleep(0.01)


if __name__ == "__main__":
    main()
