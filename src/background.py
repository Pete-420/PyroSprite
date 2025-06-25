import pygame
import os

class Background:
    def __init__(self, texture_path, scale_to_screen=True, maintain_aspect=True):
        self.texture_path = texture_path
        self.scale_to_screen = scale_to_screen
        self.maintain_aspect = maintain_aspect
        
        # Texture properties
        self.texture = None
        self.texture_width = 0
        self.texture_height = 0
        self.scaled_texture = None
        self.screen_size = None
        
        # Load texture
        self._load_texture()
        
    def _load_texture(self):
        if not os.path.exists(self.texture_path):
            print(f"Warning: Texture file not found: {self.texture_path}")
            # Create a placeholder texture for testing
            self.texture = pygame.Surface((800, 600))
            # Create a simple gradient background
            for y in range(600):
                intensity = int(64 + (y / 600) * 128)  # Gradient from dark to lighter
                color = (intensity // 4, intensity // 8, intensity // 16)  # Dark red gradient
                pygame.draw.line(self.texture, color, (0, y), (800, y))
            self.texture_width = 800
            self.texture_height = 600
            print("Created placeholder gradient background")
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
            'screen_size': self.screen_size
        }
