import pygame
import sys
from src.background import Background
from src.emitter import Emitter
from src.config import BACKGROUND_CONFIG, SCREEN_CONFIG

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
    emitter = Emitter(emitter_x, emitter_y, emit_rate=20)
    
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
        
        # 2. Render particles as simple circles (temporary until we get textures)
        for particle in emitter.particles:
            if particle.is_alive():
                # Convert color from 0-1 range to 0-255
                color = (
                    int(particle.color[0] * 255),
                    int(particle.color[1] * 255), 
                    int(particle.color[2] * 255)
                )
                
                # Draw particle as circle with alpha blending
                alpha = int(particle.color[3] * 255)
                if alpha > 0:
                    # Create surface for alpha blending
                    particle_surface = pygame.Surface((particle.size * 4, particle.size * 4))
                    particle_surface.set_alpha(alpha)
                    particle_surface.fill(color)
                    
                    # Draw circle on the surface
                    pygame.draw.circle(
                        particle_surface, 
                        color, 
                        (particle.size * 2, particle.size * 2), 
                        int(particle.size)
                    )
                    
                    # Blit to screen
                    screen.blit(
                        particle_surface, 
                        (particle.x - particle.size * 2, particle.y - particle.size * 2)
                    )
        
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