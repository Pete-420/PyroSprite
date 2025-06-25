import pygame
import sys
from src.background import Background
from src.emitter import Emitter
from src.config import BACKGROUND_CONFIG, SCREEN_CONFIG, PARTICLE_CONFIG, BACKGROUND_ATLAS_CONFIG, EMMITTER_CONFIG
from src.particleAtlas import ParticleAtlas
from src.spriteCache import SpriteCache

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_CONFIG['width'], SCREEN_CONFIG['height']))
    pygame.display.set_caption(SCREEN_CONFIG['title'])
    clock = pygame.time.Clock()
    
    background = Background(
        atlas_config=BACKGROUND_ATLAS_CONFIG,
        scale_to_screen=BACKGROUND_CONFIG['scale_to_screen'],
        maintain_aspect=BACKGROUND_CONFIG['maintain_aspect'],
        animation_speed=0.2
    )
    
    fireplace_x = SCREEN_CONFIG['width'] // 2
    fireplace_y = (SCREEN_CONFIG['height'] - 115)  
    emitter = Emitter(fireplace_x, fireplace_y, emit_rate=EMMITTER_CONFIG['emmit_rate'], max_particles=EMMITTER_CONFIG['limit'])  # Zwiększ limit
    
    atlas = ParticleAtlas(
        texture_path=PARTICLE_CONFIG['atlas_path'],
        frame_width=PARTICLE_CONFIG['frame_width'],
        frame_height=PARTICLE_CONFIG['frame_height'],
        cols=PARTICLE_CONFIG['atlas_cols'],
        rows=PARTICLE_CONFIG['atlas_rows']
    )
    
    sprite_cache = SpriteCache(atlas)
    sprite_cache.preload_common_sprites()
    
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
        dt = clock.tick(60) / 1000.0
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
                    emitter.emit_rate = min(emitter.emit_rate + EMMITTER_CONFIG['emmit_++'], EMMITTER_CONFIG['limit'])
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
                emitter.x, emitter.y = event.pos
        
        if not paused:
            background.update(dt)
            emitter.update(dt)
        
        screen.fill((0, 0, 0))
        background.render(screen)
        
        if atlas.is_loaded:
            for particle in emitter.particles:
                if particle.is_alive():
                    life_ratio = particle.life / particle.max_life
                    scale_w = max(8, int(particle.size * 24))
                    if particle.is_ember:
                        frame_idx = 5 if life_ratio > 0.5 else 6
                        scale_h = scale_w
                    else:
                        frame_idx = min(4, int((1.0 - life_ratio) * 5))
                        scale_h = scale_w * 3
                    
                    sprite = sprite_cache.get_sprite(frame_idx, scale_w, scale_h)
                    if sprite:
                        sprite.set_alpha(int(particle.color[3] * 255))
                        screen.blit(sprite, (particle.x - scale_w // 2, particle.y - scale_h // 2))
        
        if show_debug:
            font = pygame.font.Font(None, 24)
            
            # Pool statistics
            stats = emitter.get_particle_stats()
            particle_count = stats['active']
            text1 = font.render(f"Particles: {particle_count}/{stats['total']}", True, (255, 255, 255))
            screen.blit(text1, (10, 10))
            
            # Pool usage
            usage = (stats['active'] / stats['total']) * 100 if stats['total'] > 0 else 0
            text_pool = font.render(f"Pool Usage: {usage:.1f}%", True, (255, 255, 255))
            screen.blit(text_pool, (10, 35))
            
            # Emit rate
            text2 = font.render(f"Emit Rate: {emitter.emit_rate}/s", True, (255, 255, 255))
            screen.blit(text2, (10, 60))
            
            # FPS
            fps = clock.get_fps()
            text3 = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
            screen.blit(text3, (10, 85))
            
            # Emitter position
            text4 = font.render(f"Emitter: ({emitter.x:.0f}, {emitter.y:.0f})", True, (255, 255, 255))
            screen.blit(text4, (10, 110))
            
            # Cache stats
            text_cache = font.render(f"Cached Sprites: {len(sprite_cache.cache)}", True, (255, 255, 255))
            screen.blit(text_cache, (10, 135))
            
            if paused:
                text5 = font.render("PAUSED", True, (255, 255, 0))
                screen.blit(text5, (SCREEN_CONFIG['width'] - 80, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()