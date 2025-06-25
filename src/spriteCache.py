import pygame

class SpriteCache:
    def __init__(self, atlas):
        self.atlas = atlas
        self.cache = {}  # {(frame_idx, width, height): sprite}
        self.common_sizes = []
        self._generate_common_sizes()
        
    def _generate_common_sizes(self):
        for size in range(8, 120, 8):  # 8, 16, 24, 32...
            # Flame sizes (tall)
            self.common_sizes.append((size, size * 3))
            # Ember sizes (square)  
            self.common_sizes.append((size, size))
    
    def get_sprite(self, frame_idx, width, height):
        key = (frame_idx, width, height)
        
        if key not in self.cache:
            frame = self.atlas.get_frame(frame_idx)
            if frame:
                self.cache[key] = pygame.transform.smoothscale(frame, (width, height))
            else:
                return None
                
        return self.cache[key]
    
    def preload_common_sprites(self):
        print("Pre-loading sprite cache...")
        for frame_idx in range(self.atlas.get_frame_count()):
            for width, height in self.common_sizes:
                self.get_sprite(frame_idx, width, height)
        print(f"Cached {len(self.cache)} sprites")