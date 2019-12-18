import pygame
from math import cos, sin, pi, sqrt

FPS = 60
width = 600
height = 600
BACKGROUND = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('collision')
window = pygame.display.set_mode((width, height))
screen = pygame.Surface((width, height))


class Block:
    def __init__(self, x, w, v, m):
        self.x = x
        self.y = height/2 - w
        self.w = w
        self.v = v
        self.m = m

    def is_collide(self, other):
        return not (self.x + self.w < other.x or self.x > other.x + other.w)

    def hit_wall(self):
        if self.x <= 0 or self.x + self.w >= width:
            self.v *= -1

    def bounce(self, other):
        sum_m = self.m + other.m
        new_v = (self.m - other.m) / sum_m * self.v
        new_v += (2 * other.m / sum_m) * other.v
        return new_v

    def update(self):
        self.x += self.v

    def render(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.w, self.w))


def draw():
    if block1.is_collide(block2):
        v1 = block1.bounce(block2)
        v2 = block2.bounce(block1)
        block1.v = v1
        block2.v = v2

    block1.hit_wall()
    block2.hit_wall()
    block1.update()
    block2.update()
    block1.render()
    block2.render()

#
# def dist(x1, y1, x2, y2):
#     return sqrt((x1-x2)**2 +(y1-y2)**2)


block1 = Block(100, 100, 0, 50)
block2 = Block(500, 10, -10, 1)

run = True

while run:
    window.blit(screen, (0, 0))
    screen.fill(BACKGROUND)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
