import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

from src.emitter import *
from background import *

def main():
    pygame.init()
    render(particle_overlay_callback=particle_overlay)
    
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()