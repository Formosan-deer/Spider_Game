import pygame
import sys
import random
from time import sleep

from pygame.time import Clock

#배경 크기지정
padWidth = 800
padHeight = 600
spiderImage = ['spider01.png','spider02.png','spider03.png','spider04.png','spider05.png',
                    'spider06.png','spider07.png','spider08.png','spider09.png','spider10.png',
                    'spider11.png','spider12.png','spider13.png','spider14.png','spider15.png']

def drawObject(obj, x, y): #게임에 등장하는 객체 드로잉
    global gamePad
    gamePad.blit(obj, (x,y)) #blit(복사할 이미지.img/복사할 대상.rect)

def initGame():
    global gamePad, clock , background, fighter, missile, explosion
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('Spider_Game') #게임이름
    background = pygame.image.load('background.png') #배경
    fighter = pygame.image.load('fighter.png') #전투기
    missile = pygame.image.load('missile.png') #레이저
    explosion = pygame.image.load('explosion.png') #폭발
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosion

    #전투기크기
    fighterSize = fighter.get_rect().size
    fighterWidth =fighterSize[0]
    fighterHeight = fighterSize[1]
    #전투기 초기 위치(x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    #무기좌표 리스트
    missileXY = []

    #거미 랜덤 생성
    spider = pygame.image.load(random.choice(spiderImage))
    spiderSize = spider.get_rect().size #거미 크기
    spiderWidth = spiderSize[0]
    spiderHeight = spiderSize[1]
    
    #거미 초기 위치
    spiderX = random.randrange(0, padWidth - spiderWidth)
    spiderY = 0
    spiderSpeed = 2

    #레이저에 거미 맞은경우 True
    inShot = False
    shotCount = 0
    spiderPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: #게임 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_SPACE:
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
            
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0 #방향키 떼면 전투기 멈춤

        drawObject(background, 0, 0) #배경그리기

        #전투기 위치 재조정
        x += fighterX
        if x < 0: #전투기가 왼쪽끝으로 가는경우 멈춤
            x = 0
        elif x > padWidth - fighterWidth: #전투기가가 오른쪽 끝으로 가는 경우 멈춤
            x = padWidth - fighterWidth

        drawObject(fighter, x, y) #전투기그리기

        #레이저 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): #레이저 요소에 대해 반복함
                bxy[1] -= 10 #레이저의 y좌표 -10(위로 이동)
                missileXY[i][1] =bxy[1]

                #레이저가 거미를 맞춘경우
                if bxy[1] < spiderY:
                    if bxy[0] > spiderX and bxy[0] < spiderX + spiderWidth:
                        missileXY.remove(bxy)
                        inShot = True
                        shotCount += 1

                if bxy[1] <=0: #레이저가 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy) #레이저 제거
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        spiderY += spiderSpeed #거미 아래로 움직임

        #거미가 끝으로 떨어진 경우
        if spiderY > padHeight :
            #새로운 거미 (랜덤)
            spider = pygame.image.load(random.choice(spiderImage))
            spiderSize = spider.get_rect().size
            spiderWidth = spiderSize[0]
            spiderHeight = spiderSize[1]
            spiderX = random.randrange(0, padWidth - spiderHeight)
            spiderY = 0

        #거미를 맞춘 경우
        if inShot:
            #거미 사망
            drawObject(explosion, spiderX, spiderY) #폭발그림

            #새로운 거미 (랜덤)
            spider = pygame.image.load(random.choice(spiderImage))
            spiderSize = spider.get_rect().size
            spiderWidth = spiderSize[0]
            spiderHeight = spiderSize[1]
            spiderX = random.randrange(0, padWidth - spiderWidth)
            spiderY = 0
            inShot = False

        drawObject(spider, spiderX, spiderY) #거미그림

        pygame.display.update() #게임화면을 다시그림

        clock.tick(60) #게임 초당 프레임 수 60

    pygame.quit() #pygame종료

initGame()
runGame()