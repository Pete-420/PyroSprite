import random
import math
from .particle import Particle
from .config import FIRE_COLORS
import numpy as np 
import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GLU import *    
import pygame

class Emitter:
    def __init__(self, x, y, emit_rate=10):
        self.x = x
        self.y = y
        self.emit_rate = emit_rate
        self.particles = []
        self.emit_accum = 0  # accumulated time for emission
    def emit(self):
        # simple particle emission logic, random vector and speed and life
        angle = random.uniform(0, 2 * 3.14159)  # Random angle in radians
        speed = random.uniform(0.5, 2.0)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        life = random.uniform(1.0, 3.0)
        particle = Particle(
            self.x, 
            self.y, 
            vx, 
            vy, 
            life, 
            size=random.uniform(0.5, 2.0),  # Random size
            color = FIRE_COLORS[random.randint(0, len(FIRE_COLORS) - 1)]  # Random color from FIRE_COLORS
        )
        self.particles.append(particle)
    def update(self, dt):
        self.emit_accum += dt *self.emit_rate
        while self.emit_accum >= 1.0:
            self.emit()
            self.emit_accum -= 1.0
        for particle in self.particles:
            particle.update(dt)
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]

width = 1920
height = 1080

emitter = Emitter(width // 2, height // 2, emit_rate=15)

def particle_overlay(dt, width, height):
    
    # --- Zapisz stan macierzy ---
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # --- Zapisz i ustaw tryby rysowania ---
    depth = glIsEnabled(GL_DEPTH_TEST)
    lighting = glIsEnabled(GL_LIGHTING)
    blend = glIsEnabled(GL_BLEND)

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    emitter.x = width // 2
    emitter.y = height // 2
    emitter.update(dt)
    for particle in emitter.particles:
        color = [int(c * 255) for c in particle.color[:3]]
        alpha = int(particle.color[3] * 255)
        size = int(particle.size * 10)
        x = int(particle.x)
        y = int(particle.y)

        glColor4ub(color[0], color[1], color[2], alpha)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for angle in range(0, 361, 30):
            rad = np.radians(angle)
            glVertex2f(x + np.cos(rad) * size, y + np.sin(rad) * size)
        glEnd()

    # --- Przywróć tryby rysowania ---
    if not blend:
        glDisable(GL_BLEND)
    if lighting:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)
    if depth:
        glEnable(GL_DEPTH_TEST)
    else:
        glDisable(GL_DEPTH_TEST)

    # --- Przywróć macierze ---
    glPopMatrix()  # MODELVIEW
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)