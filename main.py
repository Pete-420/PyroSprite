import pygame
import sys
from src.background import Background
from src.emitter import Emitter
from src.config import BACKGROUND_CONFIG, SCREEN_CONFIG
from src.particleAtlas import ParticleAtlas

def main():
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((SCREEN_CONFIG['width'], SCREEN_CONFIG['height']))
    pygame.display.set_caption(SCREEN_CONFIG['title'])
    clock = pygame.time.Clock()
    
    # Create background
    background = Background(
        texture_path=BACKGROUND_CONFIG['texture_path'],
        scale_to_screen=BACKGROUND_CONFIG['scale_to_screen'],
        maintain_aspect=BACKGROUND_CONFIG['maintain_aspect']
    )
    
    # Create emitter in center-bottom of screen
    emitter_x = SCREEN_CONFIG['width'] // 2
    emitter_y = SCREEN_CONFIG['height'] - 50  # Near bottom
    emitter = Emitter(emitter_x, emitter_y, emit_rate=50)
    
    # Inicjalizacja atlasu płomieni
    atlas = ParticleAtlas(
        texture_path="textures/j.png",
        frame_width=307,   # 1536 / 5
        frame_height=1024, # cały obraz
        cols=5,
        rows=1
    )
    
    print("Controls:")
    print("  ESC - Exit")
    print("  SPACE - Pause/Resume")
    print("  + - Increase emit rate")
    print("  - - Decrease emit rate")
    print("  Mouse - Move emitter")
    
    paused = False
    show_debug = True
    
    running = True
    while running:
        dt = clock.tick(60) / 500.0  # Convert to seconds
        
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
                    emitter.emit_rate = min(emitter.emit_rate + 5, 1000)
                    print(f"Emit rate: {emitter.emit_rate}")
                elif event.key == pygame.K_MINUS:
                    emitter.emit_rate = max(emitter.emit_rate - 5, 1)
                    print(f"Emit rate: {emitter.emit_rate}")
                elif event.key == pygame.K_d:
                    show_debug = not show_debug
                    print(f"Debug info: {'ON' if show_debug else 'OFF'}")
            elif event.type == pygame.MOUSEMOTION:
                # Move emitter to mouse position
                emitter.x, emitter.y = event.pos
        
        # Update simulation
        if not paused:
            emitter.update(dt)
        
        # Render everything
        screen.fill((0, 0, 0))  # Clear screen
        
        # 1. Render background
        background.render(screen)
        
        # 2. Render particles as flame sprites from atlas
        for i, particle in enumerate(emitter.particles):
            if particle.is_alive() and atlas.is_loaded:
                # Wybierz klatkę animacji (np. losowo lub na podstawie życia)
                # Tu: 0-4 płomienie, 5 dymek (opcjonalnie na końcu życia)
                if particle.life / particle.max_life < 0.5:
                    frame_idx = 5  # dymek
                else:
                    frame_idx = i % 5  # płomienie 0-4

                frame = atlas.get_frame(frame_idx)
                if frame:
                    # Dopasuj rozmiar sprite do particle.size, ale wysokość 2x większa niż szerokość
                    scale_w = max(8, int(particle.size * 24))
                    scale_h = scale_w * 4
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
            
            # Paused status
            if paused:
                text5 = font.render("PAUSED", True, (255, 255, 0))
                screen.blit(text5, (SCREEN_CONFIG['width'] - 80, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()