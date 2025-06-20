import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import sys
import numpy as np

width = image_width = 1920
height = image_height = 1080

def load_texture(filename):
    img = Image.open(filename)
    img = img.rotate(0, expand=True)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGB").tobytes()
    width, height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id

def draw_sphere_segment(texture_id, fov_deg=10, slices=64, stacks=64):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    radius = 50
    fov_rad = np.radians(fov_deg)
    start_long = -fov_rad / 2
    end_long = fov_rad / 2

    for i in range(slices):
        long0 = start_long + (end_long - start_long) * i / slices
        long1 = start_long + (end_long - start_long) * (i + 1) / slices
        glBegin(GL_QUAD_STRIP)
        for j in range(stacks + 1):
            lat = np.pi * (j / stacks - 0.5)
            for longi in [long0, long1]:
                x = radius * np.cos(lat) * np.cos(longi)
                y = radius * np.sin(lat)
                z = radius * np.cos(lat) * np.sin(longi)
                u = (longi - start_long) / (end_long - start_long)
                v = (j / stacks)
                glTexCoord2f(u, v)
                glVertex3f(-x, y, z)  # -x to invert sphere
        glEnd()
    glDisable(GL_TEXTURE_2D)

def render():
    pygame.init()
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Panoramic Background')

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(120, (width/height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    texture_id = load_texture('pernice.jpg')

    yaw = 0.0
    cam_x, cam_y, cam_z = 0.0, 0.0, 1  # Camera position
    move_speed = 0.5

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            yaw += 0.5
        if keys[K_LEFT]:
            yaw -= 0.5
        if keys[K_a]:
            cam_x -= move_speed
        if keys[K_d]:
            
            cam_x += move_speed
        if keys[K_w]:
            cam_z -= move_speed
        if keys[K_s]:
            cam_z += move_speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)
        glRotatef(yaw, 0, 1, 0)
        glScalef(-1, 1, 1)
        draw_sphere_segment(texture_id, fov_deg=360)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "render":
    render()