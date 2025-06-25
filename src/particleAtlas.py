import pygame
import os

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

        self._load_atlas()

    def _load_atlas(self):
        if not os.path.exists(self.texture_path):
            print(f"Atlas not found: {self.texture_path}")
            return
        self.atlas_texture = pygame.image.load(self.texture_path).convert_alpha()
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.frame_width,
                    row * self.frame_height,
                    self.frame_width,
                    self.frame_height
                )
                frame = self.atlas_texture.subsurface(rect).copy()
                self.frames.append(frame)
        self.is_loaded = True

    def get_frame(self, frame_index):
        if not self.frames:
            return None
        return self.frames[frame_index % len(self.frames)]

    def get_frame_count(self):
        return len(self.frames)