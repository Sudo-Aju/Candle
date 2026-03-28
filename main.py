import pygame
import random
from config import ConfigManager
from audio_dsp import AudioProcessor
from particles import ParticleSystem
from ui import UIManager
from assets import AssetManager
from confetti import CelebrationManager
from utils import global_noise

def main():
    pygame.init()
    
    cfg = ConfigManager()
    WIDTH, HEIGHT = cfg.settings["SCREEN_WIDTH"], cfg.settings["SCREEN_HEIGHT"]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("hppy bday candle for u :)")
    clock = pygame.time.Clock()
    
    audio = AudioProcessor(cfg)
    psystem = ParticleSystem()
    ui = UIManager(WIDTH, HEIGHT)
    assets = AssetManager()
    party = CelebrationManager(WIDTH, HEIGHT)
    
    candle_x, candle_y = WIDTH // 2, HEIGHT - 200
    blow_limit = cfg.settings["BLOW_LIMIT"]
    
    cake_img = pygame.Surface((200, 100), pygame.SRCALPHA)
    pygame.draw.rect(cake_img, (255, 255, 255), cake_img.get_rect(), border_radius=10)

    candle_body = pygame.Surface((30, 105), pygame.SRCALPHA)
    pygame.draw.rect(candle_body, (230, 230, 240), (0, 0, 30, 105), border_radius=4) 
  
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
                    party.reset()

        t = pygame.time.get_ticks() * 0.005
        wick_noise = global_noise.get_noise(t) * 8
        wick_lean = wind * 25
        total_dx = wick_noise + wick_lean

        if current_state == STATE_MENU:
            ui.draw_text_center(screen, "Candle on a cake for bday buddy!", -50, "large")
            ui.draw_text_center(screen, "Press SPACE to light the candle", 20)

        elif current_state == STATE_PLAYING:
            screen.blit(cake_img, (candle_x - 100, candle_y + 100))
            screen.blit(candle_body, (candle_x - 15, candle_y)) 
            
            wick_top = (candle_x + total_dx, candle_y - 15)
            pygame.draw.line(screen, (255, 255, 255), (candle_x, candle_y), wick_top, 3)

            psystem.emit_fire(candle_x, candle_y - 15, count=6, dx=total_dx)
            psystem.update_and_draw(screen, wind)
            ui.draw_meter(screen, wind, blow_limit)
            
            if wind > blow_limit:
                current_state = STATE_OUT
                psystem.emit_smoke(candle_x, candle_y - 15, count=40, dx=total_dx)
                party.trigger(150)

        elif current_state == STATE_OUT:
            screen.blit(cake_img, (candle_x - 100, candle_y + 100))
            screen.blit(candle_body, (candle_x - 15, candle_y)) 
            
            wick_top = (candle_x + total_dx, candle_y - 15)
            pygame.draw.line(screen, (255, 255, 255), (candle_x, candle_y), wick_top, 3)

            if random.random() < 0.3:
                psystem.emit_smoke(candle_x, candle_y - 15, count=1, dx=total_dx)
                
            psystem.update_and_draw(screen, wind)
            party.update_and_draw(screen)
            
            ui.draw_text_center(screen, "make a wishh", -150, "large")
            ui.draw_text_center(screen, "Press 'R' to relight", -100)

        pygame.display.flip()
        clock.tick(cfg.settings["FPS"])

    pygame.quit()

if __name__ == "__main__":
    main()