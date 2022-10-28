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
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Clock
clock = pygame.time.Clock()
FPS = 120

# Game vars
dia = 36

# Colours
BG = (50, 50, 50)

# Load images
cue_image = pygame.image.load("assets/images/cue.png").convert_alpha()
table_image = pygame.image.load("assets/images/table.png").convert_alpha()
ball_images = []
for i in range(1, 17):
    ball_image = pygame.image.load(f"assets/images/ball_{i}.png").convert_alpha()
    ball_images.append(ball_image)


# Ball function
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    # Use pivot to add friction
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 1000
    space.add(body, shape, pivot)
    return shape


# Setup Game Balls
balls = []
rows = 5
# Potting Balls
for col in range(5):
    for row in range(rows):
        pos = (250 + (col * dia + 1), 267 + (row * (dia + 1)) + (col * dia / 2))
        new_ball = create_ball(dia / 2, pos)
        balls.append(new_ball)
    rows -= 1

# Cue ball
pos = (888, SCREEN_HEIGHT / 2)
cue_ball = create_ball(dia / 2, pos)
balls.append(cue_ball)

# Create six pockets on table
pockets = [
  (55, 63),
  (592, 48),
  (1134, 64),
  (55, 616),
  (592, 629),
  (1134, 616)
]

# Cushion coordinates
cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]


# Create cushions
def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8
    space.add(body, shape)


# Generate cushions
for c in cushions:
    create_cushion(c)


# Create pool cue
class Cue:
    def __init__(self, pos):
        self.original_image = cue_image
        self.angle = 0
        self.image = cue_image
        self.rect = self.image.get_rect()
        self.rect.center = pos


# Game loop
run = True
while run:

    clock.tick(FPS)
    space.step(1 / FPS)

    # Fill background
    screen.fill(BG)

    # Pool Table
    screen.blit(table_image, (0, 0))

    # Draw pool balls
    for i, ball in enumerate(balls):
        screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    # Event listener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cue_ball.body.apply_impulse_at_local_point((-500, 0), (0, 0))

    # space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
