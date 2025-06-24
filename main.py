import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

from src.emitter import *
from src.background import *

def main():
    pygame.init()

    render()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()