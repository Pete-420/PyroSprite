import pygame
import os
from .particleAtlas import ParticleAtlas

class Background:
    def __init__(self, texture_path=None, atlas_config=None, scale_to_screen=True, maintain_aspect=True, animation_speed=0.2):
        self.texture_path = texture_path
        self.atlas_config = atlas_config
        self.scale_to_screen = scale_to_screen
        self.maintain_aspect = maintain_aspect
        self.animation_speed = animation_speed
        
        # Animation properties
        self.current_frame = 0
        self.animation_timer = 0.0
        self.atlas = None
        
        # Texture properties
        self.texture = None
        self.texture_width = 0
        self.texture_height = 0
        self.scaled_texture = None
        self.screen_size = None
        
        # Load texture or atlas
        if atlas_config:
            self._load_atlas()
        else:
            self._load_texture()
        
    def _load_atlas(self):
        self.atlas = ParticleAtlas(
            texture_path=self.atlas_config['atlas_background_path'],
            frame_width=self.atlas_config['frame_width'],
            frame_height=self.atlas_config['frame_height'],
            cols=self.atlas_config['atlas_cols'],
            rows=self.atlas_config['atlas_rows']
        )
        if self.atlas.is_loaded:
            self.texture_width = self.atlas_config['frame_width']
            self.texture_height = self.atlas_config['frame_height']
            # Get first frame as initial texture
            self.texture = self.atlas.get_frame(0)
            print(f"Background atlas loaded: {self.atlas.get_frame_count()} frames, {self.texture_width}x{self.texture_height}")
        else:
            self._create_placeholder()
    
    def _create_placeholder(self):
        self.texture = pygame.Surface((800, 600))
        # Create a simple gradient background
        for y in range(600):
            intensity = int(64 + (y / 600) * 128)
            color = (intensity // 4, intensity // 8, intensity // 16)
            pygame.draw.line(self.texture, color, (0, y), (800, y))
        self.texture_width = 800
        self.texture_height = 600
        print("Created placeholder gradient background")
    
    def update(self, dt):
        if self.atlas and self.atlas.is_loaded:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % self.atlas.get_frame_count()
                self.texture = self.atlas.get_frame(self.current_frame)
                self.animation_timer = 0.0
                # Clear scaled texture to force rescaling with new frame
                self.scaled_texture = None
        
    def _load_texture(self):
        if not self.texture_path:
            self._create_placeholder()
            return
            
        if not os.path.exists(self.texture_path):
            print(f"Warning: Texture file not found: {self.texture_path}")
            self._create_placeholder()
        else:
            self.texture = pygame.image.load(self.texture_path).convert()
            self.texture_width = self.texture.get_width()
            self.texture_height = self.texture.get_height()
            print(f"Background loaded: {self.texture_width}x{self.texture_height}")
    
    def _scale_texture(self, screen_width, screen_height):
        if not self.scale_to_screen:
            self.scaled_texture = self.texture
            return
        
        if self.maintain_aspect:
            # Calculate scale to fit screen while maintaining aspect ratio
            scale_x = screen_width / self.texture_width
            scale_y = screen_height / self.texture_height
            scale = min(scale_x, scale_y)  # Use smaller scale to fit entirely
            
            new_width = int(self.texture_width * scale)
            new_height = int(self.texture_height * scale)
        else:
            # Stretch to fill screen exactly
            new_width = screen_width
            new_height = screen_height
        
        self.scaled_texture = pygame.transform.scale(self.texture, (new_width, new_height))
        print(f"Background scaled to: {new_width}x{new_height}")
    
    def render(self, surface):
        screen_width, screen_height = surface.get_size()
        
        # Scale texture if screen size changed or first render
        if (self.scaled_texture is None or 
            self.screen_size != (screen_width, screen_height)):
            self.screen_size = (screen_width, screen_height)
            self._scale_texture(screen_width, screen_height)
        
        if self.scaled_texture:
            # Center the background on screen
            bg_width, bg_height = self.scaled_texture.get_size()
            x = (screen_width - bg_width) // 2
            y = (screen_height - bg_height) // 2
            surface.blit(self.scaled_texture, (x, y))
    
    def get_texture_info(self):
        return {
            'original_size': (self.texture_width, self.texture_height),
            'scaled_size': self.scaled_texture.get_size() if self.scaled_texture else None,
            'screen_size': self.screen_size,
            'is_animated': self.atlas is not None,
            'current_frame': self.current_frame if self.atlas else None,
            'total_frames': self.atlas.get_frame_count() if self.atlas else None
        }
