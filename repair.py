#!/usr/bin/env python3
from mapprocess import loadmap
from mapprocess import gettilemap
from settings import *

import os
import pygame
import sys

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 4,2048)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        self.title_font = None

    def draw_text(self,text, font_name, size, color, x, y, align="topleft"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        graphics_folder = os.path.join(game_folder, 'graphics')
        tiles_folder = os.path.join(graphics_folder, 'tiles')
        sound_folder = os.path.join(game_folder, 'sound')
        music_folder = os.path.join(game_folder, 'music')
        self.map_folder = os.path.join(game_folder, 'maps')
        
        tilemaplist = loadmap("test2.map")
        self.tilemap = gettilemap(tilemaplist)
        
        # Sound loading
        """
        pygame.mixer.music.load(os.path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pygame.mixer.Sound(os.path.join(sound_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for type in WEAPON_SOUNDS:
            self.weapon_sounds[type] = pygame.mixer.Sound(os.path.join(sound_folder, WEAPON_SOUNDS[type]))
        for type in ENEMY_HIT_SOUNDS:
            self.enemy_hit_sounds[type] = []
            for snd in ENEMY_HIT_SOUNDS[type]:
                s = pygame.mixer.Sound(os.path.join(sound_folder, snd))
                s.set_volume(0.2)
                self.enemy_hit_sounds[type].append(s)
        for type in ENEMY_ALERT_SOUNDS:
            self.enemy_alert_sounds[type] = pygame.mixer.Sound(os.path.join(sound_folder, ENEMY_ALERT_SOUNDS[type]))
            self.enemy_alert_sounds[type] = []
            for snd in ENEMY_ALERT_SOUNDS[type]:
                s = pygame.mixer.Sound(os.path.join(sound_folder, snd))
                s.set_volume(0.2)
                self.enemy_alert_sounds[type].append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder, snd)))
        """

    def new(self):
        # Initialize all variables and do all the setup for a new game.
    
        px = self.screen.get_width() / 2
        py = self.screen.get_height() / 2

        mapx = -(self.tilemap.get_width() / 2)
        mapy = -(self.tilemap.get_height() / 2)
    
    def run(self):
        # Game loop - set self.playing = false to end the game.
        pass

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        #Update portion of the game loop.
        pass

    def draw(self):
        pygame.display.set_caption('{:.2f}'.format(self.clock.get_fps()))
        screen.blit(tilemap, (int(mapx), int(mapy)))
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(px), int(py)),
            16
        )
        pygame.display.flip()

    def events(self):
        # Catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()        
            elif event.type == pygame.KEYDOWN:          # check for key presses          
                if event.key == pygame.K_LEFT:        # left arrow turns left
                    pressed_left = True
                elif event.key == pygame.K_RIGHT:     # right arrow turns right
                    pressed_right = True
                elif event.key == pygame.K_UP:        # up arrow goes up
                    pressed_up = True
                elif event.key == pygame.K_DOWN:     # down arrow goes down
                    pressed_down = True
            elif event.type == pygame.KEYUP:            # check for key releases
                if event.key == pygame.K_LEFT:        # left arrow turns left
                    pressed_left = False
                elif event.key == pygame.K_RIGHT:     # right arrow turns right
                    pressed_right = False
                elif event.key == pygame.K_UP:        # up arrow goes up
                    pressed_up = False
                elif event.key == pygame.K_DOWN:     # down arrow goes down
                    pressed_down = False

        # In your game loop, check for key states:
        if pressed_left:
            x -= PLAYER_SPEED 
        if pressed_right:
            x += PLAYER_SPEED
        if pressed_up:
            y -= PLAYER_SPEED
        if pressed_down:
            y += PLAYER_SPEED

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_text('GAME OVER', self.title_font, 100, (255, 0, 0),
                        WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Press a key to start', self.title_font, 75, (255, 255, 255),
                        WIDTH / 2, HEIGHT * 3 / 4, align='center')
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
