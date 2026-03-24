import pygame
from config import ConfigManager
from audio_dsp import AudioProcessor
from particles import ParticleSystem

def main():
    pygame.init()
    cfg = ConfigManager()
    WIDTH, HEIGHT = cfg.settings["SCREEN_WIDTH"], cfg.settings["SCREEN_HEIGHT"]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Birthday Simulator")
    clock = pygame.time.Clock()
    
    audio = AudioProcessor(cfg)
    psystem = ParticleSystem()
    
    candle_x, candle_y = WIDTH // 2, HEIGHT - 200
    blow_limit = cfg.settings["BLOW_LIMIT"]
    is_lit = True 

    running = True
    while running:
        screen.fill((15, 15, 25))
        wind = audio.get_blow_intensity()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    is_lit = True
                    psystem.clear()

       
        pygame.draw.rect(screen, (255, 255, 255), (candle_x - 100, candle_y + 100, 200, 100), border_radius=10)
        
 
        pygame.draw.rect(screen, (230, 230, 240), (candle_x - 15, candle_y - 15, 30, 120), border_radius=4)
        pygame.draw.rect(screen, (40, 40, 40), (candle_x - 3, candle_y - 30, 6, 15))

      
        if is_lit:
            psystem.emit_fire(candle_x, candle_y - 30, count=5)
            if wind > blow_limit:
                is_lit = False

        psystem.update_and_draw(screen, wind)

        pygame.display.flip()
        clock.tick(cfg.settings["FPS"])

    pygame.quit()

if __name__ == "__main__":
    main()