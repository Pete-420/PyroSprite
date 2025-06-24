# Fire particle system configuration
FIRE_COLORS = [
    (1.0, 0.3, 0.1, 1.0),  # Red-orange
    (1.0, 0.6, 0.1, 1.0),  # Orange  
    (1.0, 0.8, 0.2, 1.0),  # Yellow-orange
    (0.9, 0.1, 0.1, 1.0),  # Deep red
]

PARTICLE_CONFIG = {
  ## toDo
}

# Background configuration
BACKGROUND_CONFIG = {
    'texture_path': 'textures/fire_background.png',  # Path to static background (relative to project root)
    'scale_to_screen': True,  # Scale background to fit screen
    'maintain_aspect': True   # Keep original aspect ratio when scaling
}

# Screen configuration  
SCREEN_CONFIG = {
    'width': 800,
    'height': 600,
    'title': 'PyroSprite Fire Simulation'
}    