import pygame
import os
from config import PARTICLE_ATLAS_CONFIG
class ParticleAtlas:
    def __init__(self, texture_path, frame_width, frame_height, cols=1, rows=1):
        self.texture_path = texture_path
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cols = cols
        self.rows = rows
        
        self.atlas_texture = None
        self.frames = []
        self.is_loaded = False
        
        # TODO: Implementacja ładowania atlasu
        # TODO: Wycinanie klatek z atlasu
        # TODO: Placeholder gdy brak tekstury
    
    def get_frame(self, frame_index):
        # TODO: Zwróć określoną klatkę
        pass
    
    def get_frame_count(self):
        # TODO: Zwróć liczbę dostępnych klatek
        return 0