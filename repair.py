#!/usr/bin/env python3
import pygame as pg
import mapprocess
from  random import randint, choice, randrange

from settings import *
from sprites import *

import os
import pygame
import sys

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 4,2048)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        self.title_font = None
        self.hud_font = 'arial'
        self.enumerated_mobs = {}
        self.golem_parts = 0
        self.golem_goal = 99


    def draw_text(self,text, font_name, size, color, x, y, align="topleft"):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (int(x), int(y))})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        graphics_folder = os.path.join(game_folder, 'graphics')
        self.tiles_folder = os.path.join(graphics_folder, 'tiles')
        sound_folder = os.path.join(game_folder, 'sound')
        self.music_folder = os.path.join(game_folder, 'music')
        self.map_folder = os.path.join(game_folder, 'maps')
        self.player_img = pygame.image.load(os.path.join(graphics_folder, PLAYER['image']))
        self.mob_img = {}
        for mob_type in ENEMIES.keys():
            img_path = os.path.join(graphics_folder, ENEMIES[mob_type]['image'])
            self.mob_img[mob_type] = pygame.image.load(img_path)

        # Sound loading
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

        map_name = "1.map"
        game_map = mapprocess.Map(os.path.join(self.map_folder, map_name), self.tiles_folder)
        self.tilemap = game_map.gettilemap()

        # Locate the player spawn or user the middle of the Map
        grid = game_map.maplist
        p_row = [l.index('S') if 'S' in l else 0 for l in grid]
        p_x = sum(p_row)
        if p_x > 0:
            p_y = p_row.index(p_x)
            p_x = TILESIZE * p_x
            p_y = TILESIZE * p_y
        else:
            p_x = self.screen.get_width() / 2
            p_y = self.screen.get_height() / 2
        self.player = Player(self, p_x, p_y)

        tilemap_w = self.tilemap.get_width()
        tilemap_h = self.tilemap.get_height()
        self.camera = mapprocess.Camera(tilemap_w, tilemap_h)
        self.mapx = -(tilemap_w / 2)
        self.mapy = -(tilemap_h / 2)

        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for wall in game_map.getwallmap():
            Obstacle(self, wall[0], wall[1], wall[2], wall[3])

        self.draw_debug = False
        self.paused = False
        self.night = False

        # Spawn dogs with random movemnt timers on 'm' tiles
        # TODO: Fix multple dogs in same ROW issues
        d_rows = [l.index('m') if 'm' in l else 0 for l in grid]
        d_spawns = [(x, y) for y, x in enumerate(d_rows) if x != 0]
        for i, (x, y) in enumerate(d_spawns):
            self.enumerated_mobs[i] = Mob(self, x * TILESIZE, y * TILESIZE, 'dog')
            seconds = randrange(500,3000)
            e = pygame.event.Event(pygame.USEREVENT + i)
            pygame.time.set_timer(e.type, seconds)

        # Spawn Guards with random movemnt timers on 'M' tiles
        # TODO: Fix multple dogs in same ROW issues
        j = len(self.enumerated_mobs)
        g_rows = [l.index('M') if 'M' in l else 0 for l in grid]
        g_spawns = [(x, y) for y, x in enumerate(g_rows) if x != 0]
        for i, (x, y) in enumerate(g_spawns):
            self.enumerated_mobs[i + j] = Mob(self, x * TILESIZE, y * TILESIZE, 'guard')
            seconds = randrange(300,2000)
            e = pygame.event.Event(pygame.USEREVENT + i + j)
            pygame.time.set_timer(e.type, seconds)

    def run(self):
        # Game loop - set self.playing = false to end the game.
        self.playing = True
        pygame.mixer.music.load(os.path.join(self.music_folder, BG_MUSIC))
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

        # In your game loop, check for key states:

    def draw(self):
        pygame.display.set_caption('{:.2f}'.format(self.clock.get_fps()))
        self.screen.blit(self.tilemap, self.camera.apply_rect(self.tilemap.get_rect()))
        for wall in self.walls:
            pygame.draw.rect(self.screen, (0, 255, 255), self.camera.apply_rect(wall.rect), 1)

        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        if PLAYER['health'] >= 90:  # if above 90 health text is green
            self.draw_text('Health: {}'.format(PLAYER['health']), self.hud_font, 20, (0, 255, 0),
                        75, 15, align='center')
        elif PLAYER['health'] <= 66 and PLAYER['health'] >= 51:  # if above 51 and bellow 66 health text is yellow
            self.draw_text('Health: {}'.format(PLAYER['health']), self.hud_font, 20, (255, 255, 0),
                           75, 15, align='center')
        elif PLAYER['health'] <= 50:  # if bellow 50 health text is red
            self.draw_text('Health: {}'.format(PLAYER['health']), self.hud_font, 20, (255, 0, 0),
                           75, 15, align='center')
        #golem_parts
        self.draw_text('Golem parts: {}/{}'.format(self.golem_parts, self.golem_goal), self.hud_font, 20, (255, 0, 0),
                           220, 15, align='center')

        pygame.display.flip()

    def events(self):
        # Catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:     # check for key presses
                if event.key == pygame.K_LEFT:     # left arrow turns left
                    self.player.pressed = 'left'
                elif event.key == pygame.K_RIGHT:  # right arrow turns right
                    self.player.pressed = 'right'
                elif event.key == pygame.K_UP:     # up arrow goes up
                    self.player.pressed = 'up'
                elif event.key == pygame.K_DOWN:   # down arrow goes down
                    self.player.pressed = 'down'
                elif event.key == pygame.K_p:      # down arrow goes down
                    self.paused
                elif event.key == pygame.K_ESCAPE:  # down arrow goes down
                    self.quit()
            elif event.type == pygame.KEYUP:        # check for key releases
                self.player.pressed = None
            elif event.type >= pygame.USEREVENT:
                pygame.time.set_timer(event.type, 0)
                mob = self.enumerated_mobs[event.type - pygame.USEREVENT]
                mob.facing = choice(list(DIRECTIONS.keys()))
                seconds = randrange(500,3000)
                pygame.time.set_timer(event.type, seconds)


    def show_start_screen(self):
        pygame.mixer.music.load(os.path.join(self.music_folder, MENU_MUSIC))
        pg.mixer.music.play(loops=-1)
        self.draw_text(TITLE, self.title_font, 100, (255, 0, 0),
                        WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Press a key to start', self.title_font, 75, (255, 255, 255),
                        WIDTH / 2, HEIGHT * 3 / 4, align='center')
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
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
