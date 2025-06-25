import pygame
import sys
from src.background import Background
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
    
    print("Controls:")
    print("  ESC - Exit")
    print("  S - Toggle scaling")
    print("  A - Toggle aspect ratio")
    
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
                elif event.key == pygame.K_s:
                    background.scale_to_screen = not background.scale_to_screen
                    background.scaled_texture = None  # Force rescale
                    print(f"Scaling: {'ON' if background.scale_to_screen else 'OFF'}")
                elif event.key == pygame.K_a:
                    background.maintain_aspect = not background.maintain_aspect
                    background.scaled_texture = None  # Force rescale
                    print(f"Maintain aspect: {'ON' if background.maintain_aspect else 'OFF'}")
        
        # Render
        screen.fill((0, 0, 0))  # Clear screen
        background.render(screen)
        
        # Debug info
        info = background.get_texture_info()
        font = pygame.font.Font(None, 36)
        debug_text = font.render(
            f"Original: {info['original_size']} | "
            f"Scaled: {info['scaled_size']} | "
            f"Screen: {info['screen_size']}", 
            True, (255, 255, 255)
        )
        screen.blit(debug_text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
