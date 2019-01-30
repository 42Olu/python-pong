import pygame
import numpy as np
from random import randint
import math

white = (255,255,255)
black = (0,0,0)

display_w = 800
display_h = 600

rand_abstand = 7
balken_breite = 20
balken_hohe = 140
ball_radius = 15
beschleunigung = 1
balken_geschwindigkeit = 7

pygame.init()
canvas = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
text = pygame.font.SysFont('monospace' ,34)

def win():
    if(left.punkte == 9):
        ball.x = int(display_w/2)
        ball.y = int(display_h/2)
        ball.move_x = 0
        ball.move_y = 0
        canvas.blit(text.render('Links gewinnt!', 0, white), (ball.x - 130, ball.y - 70))
    elif(right.punkte == 9):
        ball.x = int(display_w/2)
        ball.y = int(display_h/2)
        ball.move_x = 0
        ball.move_y = 0
        canvas.blit(text.render('Rechts gewinnt!', 0, white), (ball.x - 130, ball.y - 70))

def ball_direc():
    x = randint(-5,5)
    y = randint(-3,3)
    if(x == 0 or y == 0):
        x,y = ball_direc()
    return x,y

class Balken:
    direction = 0
    punkte = 0
    
    def __init__(self, x, y, h, w, c):
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        self.color = c

    def draw(self):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, self.width, self.height), 0)
        if(self.punkte > 0):
            score = text.render(str(self.punkte), 0, black)
            for i in range(3):
                canvas.blit(score, (self.x + i, self.y + self.height/2 - 14))            

    def move(self, d):
        self.direction = d

    def update(self):
        self.y = self.y + self.direction* balken_geschwindigkeit

        if(self.y < 0):
            self.y = 0
        if(self.y > display_h - self.height):
            self.y = display_h - self.height

    def score(self):
        self.punkte += 1

class Ball:
    x = int(display_w/2)
    y = int(display_h/2)
    move_x, move_y = ball_direc()

    def __init__(self, rad, c, l, r):
        self.r = rad
        self.color = c
        self.right = r
        self.left = l

    def draw(self):
        pygame.draw.circle(canvas, self.color, (self.x, self.y), self.r, 0)

    def update(self):
        self.x += self.move_x
        self.y += self.move_y

        if(self.y < 0):
            self.y = 0
            self.move_y *= -1
        if(self.y > display_h):
            self.y = display_h
            self.move_y *= -1
        if(self.x < rand_abstand + balken_breite/2):
            self.x = int(display_w/2)
            self.y = int(display_h/2)
            
            self.right.score()
            self.move_x, self.move_y = ball_direc()
            if(self.move_x < 0):
                self.move_x *= -1
                
        if(self.x > display_w - rand_abstand - balken_breite/2):
            self.x = int(display_w/2)
            self.y = int(display_h/2)

            self.left.score()
            self.move_x, self.move_y = ball_direc()
            if(self.move_x > 0):
                self.move_x *= -1

    def check(self):
        if(self.x + self.r > self.right.x and self.y > self.right.y and self.y < self.right.y + self.right.height):
            self.x = self.right.x - self.r
            self.move_x += beschleunigung
            if(self.move_y > 0):
                self.move_y += beschleunigung
            else:
                self.move_y -= beschleunigung
            self.move_x *= -1            
            
        if(self.x - self.r < self.left.x + self.left.width and self.y > self.left.y and self.y < self.left.y + self.left.height):
            self.x = self.left.x + self.r + self.left.width
            self.move_x -= beschleunigung
            if(self.move_y > 0):
                self.move_y += beschleunigung
            else:
                self.move_y -= beschleunigung
            self.move_x *= -1
            

left = Balken( rand_abstand, display_h/2- balken_hohe/2, balken_hohe ,balken_breite, white)
right = Balken( display_w - rand_abstand - balken_breite, display_h/2 - balken_hohe/2, balken_hohe, balken_breite, white)
ball = Ball(ball_radius, white, left, right)

beendet = False

while not beendet:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            beendet = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                beendet = True
            if event.key == pygame.K_UP:
                right.move(-1)
            if event.key == pygame.K_DOWN:
                right.move(1)
            if event.key == pygame.K_w:
                left.move(-1)
            if event.key == pygame.K_s:
                left.move(1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                if(right.direction == -1):
                    right.move(0)
            if event.key == pygame.K_DOWN:
                if(right.direction == 1):
                    right.move(0)
            if event.key == pygame.K_w:
                if(left.direction == -1):
                    left.move(0)
            if event.key == pygame.K_s:
                if(left.direction == 1):
                    left.move(0)    
            

    left.update()
    right.update()
    ball.check()
    ball.update()
    canvas.fill(black)
    ball.draw()
    left.draw()
    right.draw()
    win()
    pygame.display.update()
    clock.tick(80)

   
pygame.quit()
