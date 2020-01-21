import pygame
from math import sqrt
from random import randint as rnd


FPS = 60
width = 720
height = 480
BACKGROUND = (240, 255, 240)
RED = (220, 20, 20)
BLUE = (50, 50, 252)
RED_L = (255, 100, 100)

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Pool')
window = pygame.display.set_mode((width, height))
screen = pygame.Surface((width, height))


def dist(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Ball:
    def __init__(self, pos, vel, acc, rad, col):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.rad = rad
        self.col = col
        self.mass = self.rad * 10
        self.clicked_l = False
        self.clicked_r = False

    def collide(self, other):
        return dist(self.pos[0], self.pos[1], other.pos[0], other.pos[1]) <= self.rad + other.rad

    def overlap(self, other):
        if self.collide(other):
            d = dist(self.pos[0], self.pos[1], other.pos[0], other.pos[1])
            over = 0.5 * (d - self.rad - other.rad)

            self.pos[0] -= over * (self.pos[0] - other.pos[0]) / d
            self.pos[1] -= over * (self.pos[1] - other.pos[1]) / d
            other.pos[0] += over * (self.pos[0] - other.pos[0]) / d
            other.pos[1] += over * (self.pos[1] - other.pos[1]) / d

    def mom_trans(self, other):
        if self.collide(other):
            d = dist(self.pos[0], self.pos[1], other.pos[0], other.pos[1])

            nx = (other.pos[0] - self.pos[0]) / d
            ny = (other.pos[1] - self.pos[1]) / d

            tx = -ny
            ty = nx

            dpTan1 = self.vel[0] * tx + self.vel[1] * ty
            dpTan2 = other.vel[0] * tx + other.vel[1] * ty

            dpNorm1 = self.vel[0] * nx + self.vel[1] * ny
            dpNorm2 = other.vel[0] * nx + other.vel[1] * ny

            m1 = (dpNorm1 * (self.mass - other.mass) + 2 * other.mass * dpNorm2) / (self.mass + other.mass)
            m2 = (dpNorm2 * (other.mass - self.mass) + 2 * self.mass * dpNorm1) / (self.mass + other.mass)

            self.vel[0] = tx * dpTan1 + nx * m1
            self.vel[1] = ty * dpTan1 + ny * m1
            other.vel[0] = tx * dpTan2 + nx * m2
            other.vel[1] = ty * dpTan2 + ny * m2

    def render(self):
        pygame.draw.circle(screen, self.col, [int(self.pos[0]), int(self.pos[1])], self.rad)

    def update(self):
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99

        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def wall_wrap(self):
        if self.pos[0] < 0:
            self.pos[0] += width
        if self.pos[0] >= width:
            self.pos[0] -= width

        if self.pos[1] < 0:
            self.pos[1] += height
        if self.pos[1] >= height:
            self.pos[1] -= height


def draw():
    for ball1 in balls:
        ball1.render()
        ball1.update()
        for ball2 in balls:
            if ball2 != ball1:
                ball2.mom_trans(ball1)
                ball2.overlap(ball1)
                ball2.wall_wrap()


balls = []

for _ in range(10):
    balls.append(Ball([rnd(50, width - 50), rnd(50, height - 50)], [0, 0], [0, 0], rnd(5, 40), RED))


run = True

while run:
    window.blit(screen, (0, 0))
    screen.fill(BACKGROUND)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if dist(ball.pos[0], ball.pos[1], mx, my) < ball.rad:
                    if event.button == 1:
                        ball.col = RED_L
                        ball.clicked_l = True
                    elif event.button == 3:
                        ball.col = RED_L
                        ball.clicked_r = True
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            for ball in balls:
                ball.col = RED
                ball.clicked_l = False
                if ball.clicked_r:
                    ball.vel[0] = (ball.pos[0] - mx) / 5
                    ball.vel[1] = (ball.pos[1] - my) / 5
                    ball.clicked_r = False
        for ball in balls:
            if ball.clicked_l:
                ball.pos[0] = mx
                ball.pos[1] = my
            elif ball.clicked_r:
                pygame.draw.line(screen, BLUE, [ball.pos[0], ball.pos[1]], [mx, my], 2)
                break

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
