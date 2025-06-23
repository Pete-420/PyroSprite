import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

from src.emitter import Emitter
from background import *

def main():
    pygame.init()

    height, width = 1920, 1080
    pygame.display.set_mode((height, width), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Particles on Panoramic Background')

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(120, (width/height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    texture_id = load_texture('pernice.jpg')

    emitter = Emitter(width // 2, height, emit_rate=15)

    yaw = 0.0
    cam_x, cam_y, cam_z = 0.0, 0.0, 1
    move_speed = 0.5

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

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

        # --- Render background (OpenGL 3D) ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)
        glRotatef(yaw, 0, 1, 0)
        glScalef(-1, 1, 1)
        draw_sphere_segment(texture_id, fov_deg=360)

        # --- Switch to 2D mode for particles ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

        # --- Update and draw particles (2D overlay, always at center) ---
        emitter.x = width // 2
        emitter.y = height // 2
        emitter.update(dt)
        for particle in emitter.particles:
            color = [int(c * 255) for c in particle.color[:3]]
            alpha = int(particle.color[3] * 255)
            size = int(particle.size * 5)
            x = int(width // 2 + (particle.x - width // 2))
            y = int(height // 2 + (particle.y - height // 2))

            glColor4ub(color[0], color[1], color[2], alpha)
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(x, y)
            for angle in range(0, 361, 30):
                rad = np.radians(angle)
                glVertex2f(x + np.cos(rad) * size, y + np.sin(rad) * size)
            glEnd()

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()