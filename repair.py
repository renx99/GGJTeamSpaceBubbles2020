#!/usr/bin/env python3
import pygame as pg
import  mapprocess

from settings import *
from sprites import *

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
        text_rect = text_surface.get_rect(**{align: (int(x), int(y))})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        graphics_folder = os.path.join(game_folder, 'graphics')
        tiles_folder = os.path.join(graphics_folder, 'tiles')
        sound_folder = os.path.join(game_folder, 'sound')
        music_folder = os.path.join(game_folder, 'music')
        self.map_folder = os.path.join(game_folder, 'maps')
        self.player_img = pygame.image.load(os.path.join(graphics_folder, PLAYER['image']))

        game_map = mapprocess.Map(os.path.join(self.map_folder, "test2.map"), tiles_folder)
        self.tilemap = game_map.gettilemap()

        # Sound loading

        pygame.mixer.music.load(os.path.join(music_folder, BG_MUSIC))
        self.effect_sounds = []
        for snd in EFFECT_SOUNDS:
            self.effect_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder, snd)))
        self.weapon_sounds = []
        for snd in WEAPON_SOUNDS:
            self.weapon_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder, snd)))

        self.enemy_hit_sounds = {}
        for type in ENEMY_HIT_SOUNDS:
            self.enemy_hit_sounds[type] = []
            for snd in ENEMY_HIT_SOUNDS[type]:
                s = pygame.mixer.Sound(os.path.join(sound_folder, snd))
                s.set_volume(0.2)
                self.enemy_hit_sounds[type].append(s)

        self.enemy_alert_sounds = {}
        for type in ENEMY_ALERT_SOUNDS:
            self.enemy_alert_sounds[type] = []
            for snd in ENEMY_ALERT_SOUNDS[type]:
                s = pygame.mixer.Sound(os.path.join(sound_folder, snd))
                s.set_volume(0.2)
                self.enemy_alert_sounds[type].append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder, snd)))


    def new(self):
        # Initialize all variables and do all the setup for a new game.
        self.all_sprites = pg.sprite.LayeredUpdates()

        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        self.camera = mapprocess.Camera(self.tilemap.get_width(), self.tilemap.get_height())

        self.draw_debug = False
        self.paused = False
        self.night = False

        self.px = self.screen.get_width() / 2
        self.py = self.screen.get_height() / 2

        self.mapx = -(self.tilemap.get_width() / 2)
        self.mapy = -(self.tilemap.get_height() / 2)
        self.player = Player(self, self.px, self.py)

    def run(self):
        # Game loop - set self.playing = false to end the game.
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        #Update portion of the game loop.
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        pygame.display.set_caption('{:.2f}'.format(self.clock.get_fps()))
        self.screen.blit(self.tilemap, (int(self.mapx), int(self.mapy)))
        """
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (int(self.px), int(self.py)),
            16
        )
        """
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def events(self):
        # Catch all events here
        pressed_left = False
        pressed_right = False 
        pressed_down = False 
        pressed_up = False
        
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
            self.px -= PLAYER['speed']
        if pressed_right:
            self.px += PLAYER['speed']
        if pressed_up:
            self.py -= PLAYER['speed']
        if pressed_down:
            self.py += PLAYER['speed']

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        # self.screen.fill((0, 0, 0))
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
