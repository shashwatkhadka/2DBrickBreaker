import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Initialize Pygame
pygame.init()
width, height = 800, 600
display = (width, height)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

# Set up OpenGL perspective projection
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -10)

# Ball properties
ball_radius = 0.25
ball_pos = [0.0, 0.0, 0.0]
ball_speed = [0.07, 0.08]

# Slim block properties
block_width = 2.0
block_height = 0.2
block_pos = [0.0, -3.5, 0.0]  # Starting position for the slim block

# Blocks at the top
blocks = []
num_blocks = 10
block_spacing = 1.2
for i in range(num_blocks):
    blocks.append([-4.0 + i * block_spacing, 3.5, 0.0])

# Function to draw a sphere using triangles (for the ball)
def draw_sphere(radius):
    slices = 20
    stacks = 20

    for i in range(stacks):
        lat0 = math.pi * (-0.5 + (i / stacks))
        z0 = math.sin(lat0) * radius
        zr0 = math.cos(lat0) * radius

        lat1 = math.pi * (-0.5 + ((i + 1) / stacks))
        z1 = math.sin(lat1) * radius
        zr1 = math.cos(lat1) * radius

        glBegin(GL_QUAD_STRIP)

        for j in range(slices + 1):
            lng = 2 * math.pi * (j / slices)
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)

        glEnd()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()

    # Move the slim block
    if keys[pygame.K_a]:
        block_pos[0] -= 0.1
    if keys[pygame.K_d]:
        block_pos[0] += 0.1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw blocks at the top
    for block in blocks:
        glPushMatrix()
        glTranslatef(block[0], block[1], block[2])
        glColor3f(0.0, 0.0, 1.0)  # Set color for blocks
        glBegin(GL_QUADS)
        glVertex2f(-block_width / 2, -block_height / 2)
        glVertex2f(block_width / 2, -block_height / 2)
        glVertex2f(block_width / 2, block_height / 2)
        glVertex2f(-block_width / 2, block_height / 2)
        glEnd()
        glPopMatrix()

    # Draw slim block
    glPushMatrix()
    glTranslatef(block_pos[0], block_pos[1], block_pos[2])
    glColor3f(1.0, 1.0, 0.0)  # Set color for slim block
    glBegin(GL_QUADS)
    glVertex2f(-block_width / 2, -block_height / 2)
    glVertex2f(block_width / 2, -block_height / 2)
    glVertex2f(block_width / 2, block_height / 2)
    glVertex2f(-block_width / 2, block_height / 2)
    glEnd()
    glPopMatrix()

    # Draw ball
    glPushMatrix()
    glTranslatef(ball_pos[0], ball_pos[1], ball_pos[2])
    glColor3f(1.0, 0.0, 0.0)  # Set color for ball
    draw_sphere(ball_radius)
    glPopMatrix()

    # Update ball position
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce ball off walls
    if ball_pos[0] > 4.5 or ball_pos[0] < -4.5:
        ball_speed[0] *= -1
    if ball_pos[1] > 4.5:
        ball_speed[1] *= -1
    if (ball_pos[0] >= block_pos[0] - block_width / 2) and (ball_pos[0] <= block_pos[0] + block_width / 2) and (
            ball_pos[1] <= block_pos[1] + block_height / 2):
        ball_speed[1] *= -1
    elif ball_pos[1] < -4.5:  # If ball goes below the slim block, game over
        pygame.quit()
        quit()

    # Collision detection with blocks at the top
    collided_blocks = []
    for block in blocks:
        if (ball_pos[0] >= block[0] - block_width / 2) and (ball_pos[0] <= block[0] + block_width / 2) and (
                ball_pos[1] >= block[1] - block_height / 2) and (ball_pos[1] <= block[1] + block_height / 2):
            collided_blocks.append(block)

    for block in collided_blocks:
        blocks.remove(block)
        ball_speed[1] *= -1

    pygame.display.flip()
    pygame.time.wait(10)
