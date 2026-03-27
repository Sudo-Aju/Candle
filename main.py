import pygame
import random
from config import ConfigManager
from audio_dsp import AudioProcessor
from particles import ParticleSystem
from ui import UIManager

def main():
    pygame.init()
    cfg = ConfigManager()
    WIDTH, HEIGHT = cfg.settings["SCREEN_WIDTH"], cfg.settings["SCREEN_HEIGHT"]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Birthday Simulator")
    clock = pygame.time.Clock()
    
    audio = AudioProcessor(cfg)
    psystem = ParticleSystem()
    ui = UIManager(WIDTH, HEIGHT)
    
    candle_x, candle_y = WIDTH // 2, HEIGHT - 200
    blow_limit = cfg.settings["BLOW_LIMIT"]
    
    STATE_MENU = 0
    STATE_PLAYING = 1
    STATE_OUT = 2
    current_state = STATE_MENU

    running = True
    while running:
        screen.fill((15, 15, 25))
        wind = audio.get_blow_intensity()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_state == STATE_MENU:
                    current_state = STATE_PLAYING
                if event.key == pygame.K_r and current_state == STATE_OUT:
                    current_state = STATE_PLAYING
                    psystem.clear()

        
        pygame.draw.rect(screen, (255, 255, 255), (candle_x - 100, candle_y + 100, 200, 100), border_radius=10)
        pygame.draw.rect(screen, (230, 230, 240), (candle_x - 15, candle_y - 15, 30, 120), border_radius=4)
        pygame.draw.rect(screen, (40, 40, 40), (candle_x - 3, candle_y - 30, 6, 15))

        
        if current_state == STATE_MENU:
            ui.draw_text_center(screen, "BIRTHDAY SIMULATOR", -50, "large")
            ui.draw_text_center(screen, "Press SPACE to light the candle", 20)

        elif current_state == STATE_PLAYING:
            psystem.emit_fire(candle_x, candle_y - 30, count=6)
            psystem.update_and_draw(screen, wind)
            ui.draw_meter(screen, wind, blow_limit)
            
            if wind > blow_limit:
                current_state = STATE_OUT
                psystem.emit_smoke(candle_x, candle_y - 30, count=40)

        elif current_state == STATE_OUT:
            if random.random() < 0.3:
                psystem.emit_smoke(candle_x, candle_y - 30, count=1)
                
            psystem.update_and_draw(screen, wind)
            ui.draw_text_center(screen, "Make a wish!", -150, "large")
            ui.draw_text_center(screen, "Press 'R' to relight", -100)

        pygame.display.flip()
        clock.tick(cfg.settings["FPS"])

    pygame.quit()

if __name__ == "__main__":
    main()
