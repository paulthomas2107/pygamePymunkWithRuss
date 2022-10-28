import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678

# Screen window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool")

# Pymunk space
space = pymunk.Space()
draw_options = pymunk.pygame_util.DrawOptions(screen)


# Ball function
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    space.add(body, shape)
    return shape


new_ball = create_ball(25, (300, 100))


# Game loop
run = True
while run:

    # Event listener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
