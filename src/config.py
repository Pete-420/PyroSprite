# Fire particle system configuration
FIRE_COLORS = [
    (1.0, 0.3, 0.1, 1.0),  # Red-orange
    (1.0, 0.6, 0.1, 1.0),  # Orange  
    (1.0, 0.8, 0.2, 1.0),  # Yellow-orange
    (0.9, 0.1, 0.1, 1.0),  # Deep red
]

EMMITTER_CONFIG = {
    'limit' : 2500,  # Maximum number of particles
    'emmit_rate': 50,  # Particles emitted per second
    'emmit_++': 25, # Additional particles emitted per second
}

# Background configuration
BACKGROUND_CONFIG = {
    'texture_path': 'textures/fire_background.png',  # Path to static background (relative to project root)
    'scale_to_screen': True,  # Scale background to fit screen
    'maintain_aspect': True   # Keep original aspect ratio when scaling
}

# Screen configuration  
SCREEN_CONFIG = {
    'width': 773,
    'height': 765,
    'title': 'PyroSprites - Fire Particle System',
}    

PARTICLE_CONFIG = {
    'atlas_path': 'textures/j.png',
    'frame_width': 219,
    'frame_height': 1024,
    'atlas_cols': 7,
    'atlas_rows': 1,
}

BACKGROUND_ATLAS_CONFIG = {
    'atlas_background_path': 'textures/background_atlas.png',
    'frame_width':773,
    'frame_height': 765,
    'atlas_cols': 4,
    'atlas_rows': 2,
}