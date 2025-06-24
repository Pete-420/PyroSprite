import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import sys
import numpy as np
from .emitter import *
from .config import *

def load_texture(filename):
    img = Image.open(filename)
    img = img.rotate(0, expand=True)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGB").tobytes()
    w, h = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id

def draw_sphere_segment(texture_id, fov_deg=10, slices=64, stacks=64):
    glColor4f(1.0, 1.0, 1.0, 1.0)
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

    texture_id = load_texture('src/pernice.jpg')

    yaw = 0.0
    cam_x, cam_y, cam_z = 0.0, 0.0, 10.0  # Fixed distance from center

    # --- Utwórz emitter w centrum ekranu ---
    emitter = Emitter(width // 2, height // 2, emit_rate=15)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            yaw += 1.0
        if keys[pygame.K_LEFT]:
            yaw -= 1.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)
        glRotatef(yaw, 0, 1, 0)
        glScalef(-1, 1, 1)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        draw_sphere_segment(texture_id, fov_deg=360)

        # --- Rysowanie particle point sprites ---
        # Przełącz na tryb 2D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        emitter.x = width // 2
        emitter.y = height // 2
        emitter.update(dt)

        glPointSize(12)
        glBegin(GL_POINTS)
        for particle in emitter.particles:
            color = [int(c * 255) for c in particle.color[:3]]
            alpha = int(particle.color[3] * 255)
            glColor4ub(color[0], color[1], color[2], alpha)
            glVertex2f(particle.x, particle.y)
        glEnd()

        # Przywróć stan OpenGL
        glDisable(GL_POINT_SMOOTH)
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    render()