import pygame
import sys
from src.background import Background
from src.emitter import Emitter
from src.config import BACKGROUND_CONFIG, SCREEN_CONFIG, PARTICLE_CONFIG, BACKGROUND_ATLAS_CONFIG
from src.particleAtlas import ParticleAtlas

def main():
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((SCREEN_CONFIG['width'], SCREEN_CONFIG['height']))
    pygame.display.set_caption(SCREEN_CONFIG['title'])
    clock = pygame.time.Clock()
    
    # Create animated background
    background = Background(
        atlas_config=BACKGROUND_ATLAS_CONFIG,
        scale_to_screen=BACKGROUND_CONFIG['scale_to_screen'],
        maintain_aspect=BACKGROUND_CONFIG['maintain_aspect'],
        animation_speed=0.2  # Adjust speed as needed (seconds per frame)
    )
    

    fireplace_x = SCREEN_CONFIG['width'] // 2
    fireplace_y = (SCREEN_CONFIG['height'] - 115)  
    emitter = Emitter(fireplace_x, fireplace_y, emit_rate=50)
#    # Inicjalizacja atlasu płomieni
#    atlas = ParticleAtlas(
#        texture_path="textures/j.png",
#        frame_width=307,   # 1536 / 5
#        frame_height=1024, # cały obraz
#        cols=7,
#        rows=1
#    )
    atlas = ParticleAtlas(
        texture_path=PARTICLE_CONFIG['atlas_path'],
        frame_width=PARTICLE_CONFIG['frame_width'],
        frame_height=PARTICLE_CONFIG['frame_height'],
        cols=PARTICLE_CONFIG['atlas_cols'],
        rows=PARTICLE_CONFIG['atlas_rows']
    )  
    
    print("Controls:")
    print("  ESC - Exit")
    print("  SPACE - Pause/Resume")
    print("  + - Increase emit rate")
    print("  - - Decrease emit rate")
    print("  Mouse - Move emitter")
    print("  G - mouse grab mode")
    
    paused = False
    show_debug = True
    mouse_grabbed = False
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Convert to seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    print(f"Simulation {'PAUSED' if paused else 'RESUMED'}")
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    emitter.emit_rate = min(emitter.emit_rate + 10, 1000)
                    print(f"Emit rate: {emitter.emit_rate}")
                elif event.key == pygame.K_MINUS:
                    emitter.emit_rate = max(emitter.emit_rate - 5, 1)
                    print(f"Emit rate: {emitter.emit_rate}")
                elif event.key == pygame.K_d:
                    show_debug = not show_debug
                    print(f"Debug info: {'ON' if show_debug else 'OFF'}")
                elif event.key == pygame.K_g:
                    mouse_grabbed = not mouse_grabbed
                    if(not mouse_grabbed):
                        emitter.x = fireplace_x
                        emitter.y = fireplace_y
                        print("fire locked to foreplace")
                    else:
                        print("fire stick to mouse! be careful!")
            elif event.type == pygame.MOUSEMOTION and mouse_grabbed:
                # Move emitter to mouse position
                emitter.x, emitter.y = event.pos
        if not paused:
            background.update(dt)  # Update background animation
            emitter.update(dt)
        
        screen.fill((0, 0, 0))  # Clear screen
        background.render(screen)
        
        # 2. Render particles as flame sprites from atlas
        for i, particle in enumerate(emitter.particles):
            if particle.is_alive() and atlas.is_loaded:
                life_ratio = particle.life / particle.max_life
                scale_w = max(8, int(particle.size * 24))
                
                # Różne renderowanie dla iskierek i płomieni
                if hasattr(particle, 'is_ember') and particle.is_ember:
                    # Iskry: używaj klatek dymu (5-6) i kwadratowy kształt
                    frame_idx = 5 if life_ratio > 0.5 else 6
                    scale_h = scale_w  # 1:1 ratio dla iskier (kwadrat)
                else:
                    # Normalne płomienie: klatki 0-4 z progresją życia
                    if life_ratio > 0.8:
                        frame_idx = 0
                    elif life_ratio > 0.6:
                        frame_idx = 1
                    elif life_ratio > 0.4:
                        frame_idx = 2
                    elif life_ratio > 0.2:
                        frame_idx = 3
                    else:
                        frame_idx = 4
                    scale_h = scale_w * 3  # 1:3 ratio dla płomieni (wysoki)
                
                frame = atlas.get_frame(frame_idx)
                if frame:
                    sprite = pygame.transform.smoothscale(frame, (scale_w, scale_h))
                    # Ustaw alpha zgodnie z particle.color[3]
                    sprite.set_alpha(int(particle.color[3] * 255))
                    # Wyśrodkuj sprite na pozycji cząstki
                    screen.blit(sprite, (particle.x - scale_w // 2, particle.y - scale_h // 2))
        
        # 3. Render debug info
        if show_debug:
            font = pygame.font.Font(None, 24)
            
            # Particle count
            particle_count = len(emitter.particles)
            text1 = font.render(f"Particles: {particle_count}", True, (255, 255, 255))
            screen.blit(text1, (10, 10))
            
            # Emit rate
            text2 = font.render(f"Emit Rate: {emitter.emit_rate}/s", True, (255, 255, 255))
            screen.blit(text2, (10, 35))
            
            # FPS
            fps = clock.get_fps()
            text3 = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
            screen.blit(text3, (10, 60))
            
            # Emitter position
            text4 = font.render(f"Emitter: ({emitter.x:.0f}, {emitter.y:.0f})", True, (255, 255, 255))
            screen.blit(text4, (10, 85))
                        # W debug info
            ember_count = sum(1 for p in emitter.particles if hasattr(p, 'is_ember') and p.is_ember)
            text6 = font.render(f"Embers: {ember_count}", True, (255, 255, 255))
            screen.blit(text6, (10, 110))
            if paused:
                text5 = font.render("PAUSED", True, (255, 255, 0))
                screen.blit(text5, (SCREEN_CONFIG['width'] - 80, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()