import pygame
from pygame.locals import *
import random

KEYS_1 = {K_w:'up', K_s: 'down'}
KEYS_2 = {'up arrow': 'up', 'down arrow': 'down'}
KEY_DICT = {1: KEYS_1, 2: KEYS_2}
WHITE = (255, 255, 255)

class Player:
    start_rects = {'L': (5, 245, 5, 30), 'R': (490, 245, 5, 30)}
    def __init__(self, side, keys):
        self.keys = KEY_DICT[keys]
        self.score = 0
        self.rect = self.start_rects[side]
        self.xspeed = 0
        self.yspeed = 0
    def command(self, key):
        direction = self.keys[key]
        if direction == 'up':
            self.yspeed -= 1
        if direction == 'down':
            self.yspeed += 1
    def move(self):
        


class Ball:
    def __init__(self, xsize, ysize):
        self.xspeed = -0.2
        self.yspeed = 0
        self.xsize = xsize
        self.ysize = ysize
        self.start()
    def start(self):
        self.pos = (self.xsize / 2, self.ysize / 2)
        start_speed = random.choice([1, -1])
        self.xspeed *= start_speed
    def move(self):
        x, y = self.pos
        x += self.xspeed
        y += self.yspeed
        self.pos = (x, y)
        # Bounce off the walls
        if x <= 0 or x >= self.xsize:
            self.xspeed *= -1.5

class Screen:
    def __init__(self, xsize=500, ysize=500):
        self.xsize = 500
        self.ysize = 500
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.ball = Ball(self.xsize, self.ysize)
        self.player1 = Player('L', 1)
        self.player2 = Player('R', 2)
        self.mainloop()
    def mainloop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    pressed = event.key
                    print(pressed)
                    if pressed in KEYS_1:
                        self.player1.move(pressed)
                    elif pressed in KEYS_2:
                        self.player2.move(pressed)
            self.screen.blit(self.background, (0, 0))
            # Draw the ball
            ball_rect = (self.ball.pos[0], self.ball.pos[1], 5, 5)
            pygame.draw.rect(self.screen, WHITE, ball_rect) 
            # Draw the player paddle
            pygame.draw.rect(self.screen, WHITE, self.player1.rect)
            pygame.draw.rect(self.screen, WHITE, self.player2.rect)
            pygame.display.update()
            self.ball.move()

if __name__ == '__main__':
    play = Screen()
