#! /usr/bin/env python3
import pygame
from pygame.locals import *
import random

KEYS_1 = {K_w:'up', K_s: 'down'}
KEYS_2 = {K_UP: 'up', K_DOWN: 'down'}
KEY_DICT = {1: KEYS_1, 2: KEYS_2}
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Player:
    """Controls the player paddle. Arguments to __init__() are
    side: either 'L' or 'R', corresponding to left and right
    keys: a dictionary mapping from two pygame key objects to 'up' and 'down'
    """
    # Height of the paddle is the last element of these tuples
    start_rects = {'L': (5, 245, 5, 50), 'R': (490, 245, 5, 50)}
    move_dict = {'up': -0.5, 'down': 0.5}
    def __init__(self, side, keys):
        self.keys = KEY_DICT[keys]
        self.score = 0
        self.rect = self.start_rects[side]
        self.xspeed = 0
        self.yspeed = 0
        self.maxspeed = 2
        self.moving = False
    def start_move(self, direction):
        self.moving=True
        self.yspeed = self.move_dict[direction]
    def stop(self):
        self.moving = False
    def command(self, key):
        direction = self.keys[key]
        if direction == 'up':
            self.yspeed -= 1
        if direction == 'down':
            self.yspeed += 1
    def move(self):
        x, y, width, height = self.rect
        y += self.yspeed
        #if y < -2 or y > 480:
        #    self.moving = False
        self.rect = (x, y, width, height)
        if self.moving and self.yspeed < self.maxspeed:
            self.yspeed *= 1.01
        else:
            # Gradually slow down
            self.yspeed *= 0.99
        


class Ball:
    """
    Updates the ball position and restarts it from the center when a
    point is scored.
    Takes the screen width and height as arguments, in order to know
    how to start from the center.
    """
    def __init__(self, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.start()
    def start(self):
        self.rect = (self.xsize / 2, self.ysize / 2, 5, 5)
        start_speed = random.choice([1, -1])
        self.xspeed = 0.4 * start_speed
        self.yspeed = 0
    def move(self):
        x, y, width, height = self.rect
        x += self.xspeed
        y += self.yspeed
        self.rect = (x, y, width, height)

class Screen:
    """
    Controls all the game logic and the display.
    """
    def __init__(self, xsize=500, ysize=500):
        self.xsize = 500
        self.ysize = 500
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.font = pygame.font.Font(None, 30)
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
                    if pressed in KEYS_1:
                        self.player1.start_move(KEYS_1[pressed])
                    elif pressed in KEYS_2:
                        self.player2.start_move(KEYS_2[pressed])
                if event.type == KEYUP:
                    pressed = event.key
                    if pressed in KEYS_1:
                        self.player1.stop()
                    if pressed in KEYS_2:
                        self.player2.stop()
            self.draw_all()
            self.ball.move()
            self.player1.move()
            self.player2.move()
            self.collision_check()
    def draw_all(self):
        self.screen.blit(self.background, (0, 0))
        # Draw the ball
        pygame.draw.rect(self.screen, WHITE, self.ball.rect) 
        # Draw the player paddle
        pygame.draw.rect(self.screen, WHITE, self.player1.rect)
        pygame.draw.rect(self.screen, WHITE, self.player2.rect)
        # Player scores
        score1_text = self.font.render(str(self.player1.score), True, WHITE)
        score2_text = self.font.render(str(self.player2.score), True, WHITE)
        self.screen.blit(score1_text, (self.xsize * 0.25, 10))
        self.screen.blit(score2_text, (self.xsize * 0.75, 10))
        pygame.display.update()
    def collision_check(self):
        ballx, bally, ballw, ballh = self.ball.rect
        onex, oney, onew, oneh = self.player1.rect
        twox, twoy, twow, twoh = self.player2.rect
        onediff = abs(ballx - onex)
        twodiff = abs(ballx - twox)
        if onediff < 0.5:
            if oney < bally < (oney + oneh):
                # Multiply by 1.1 so the game speeds up a bit
                self.ball.xspeed *= -1.2
                self.angle(self.player1)
        elif twodiff < 0.5:
            if twoy < bally < (twoy + twoh):
                self.ball.xspeed *= -1
                self.angle(self.player2)
        elif ballx <= 0:
            self.player2.score += 1
            self.ball.start()
        elif ballx >= self.xsize:
            self.player1.score += 1
            self.ball.start()
        elif bally <= 0 or bally >= self.ysize:
            self.ball.yspeed *= -1
    def angle(self, player):
        """Cause the ball to bounce off at an angle determined by how
        far it is from the center of the paddle when it collides.
        Further from the center = crazier angle
        """
        ballx, bally, ballw, ballh = self.ball.rect
        px, py, pw, ph = player.rect
        #pends = (py, py + ph)
        pcenter = (py + py + ph) / 2
        # This should scale the distance according to the paddle height
        d_from_center = abs(bally - pcenter)/(ph / 2)
        self.ball.yspeed += d_from_center * 0.2


if __name__ == '__main__':
    play = Screen()
