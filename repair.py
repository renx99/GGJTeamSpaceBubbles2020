from mapprocess import loadmap
from mapprocess import gettilemap
from settings import *

import pygame
import sys

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4,2048)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def draw_text(self,text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        graphics_folder = path.join(game_folder, 'graphics')
        tiles_folder = path.join(graphics_folder, 'tiles')
        sound_folder = path.join(game_folder, 'sound')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        
        # Sound loading
        pygame.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pygame.mixer.Sound(path.join(sound_folder, EFFECTS_SOUNDS[type))
        self.weapon_sounds = {}
        for type in WEAPON_SOUNDS:
            self.weapon_sounds[type] = pygame.mixer.Sound(path.join(sound_folder, WEAPON_SOUNDS[type))
        for type in ENEMY_HIT_SOUNDS:
            self.enemy_hit_sounds[type] = []
            for snd in ENEMY_HIT_SOUNDS[type]:
                s = pygame.mixer.Sound(path.join(sound_folder, snd)
                s.set_volume(0.2)
                self.enemy_hit_sounds[type].append(s)
        for type in ENEMY_ALERT_SOUNDS:
            self.enemy_alert_sounds[type] = pygame.mixer.Sound(path.join(sound_folder, ENEMY_ALERT_SOUNDS[type))
            self.enemy_alert_sounds[type] = []
            for snd in ENEMY_ALERT_SOUNDS[type]:
                s = pygame.mixer.Sound(path.join(sound_folder, snd)
                s.set_volume(0.2)
                self.enemy_alert_sounds[type].append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pygame.mixer.Sound(path.join(sound_folder, snd)))

    def new(self):
        # Initialize all variables and do all the setup for a new game.

    def run(self):
        # Game loop - set self.playing = false to end the game.

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        #Update portion of the game loop.

    def draw(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

    def events(self):
        # Catch all events here
        for event in pygame.event.get():
            if event.type == pygame.quit:
                self.quit()

    def show_start_screen(self):
        pass


MAP_WIDTH_THRESH = 32
MAP_HEIGHT_THRESH = 32

if __name__ == "__main__":

    tilemaplist = loadmap("test2.map")
    tilemap = gettilemap(tilemaplist)

    pygame.key.set_repeat(500, 1)


    done = False

    px = screen.get_width() / 2
    py = screen.get_height() / 2

    mapx = -(tilemap.get_width() / 2)
    mapy = -(tilemap.get_height() / 2)

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_UP:
                    py -= 1
                elif event.key == pygame.K_RIGHT:
                    px += 1
                elif event.key == pygame.K_DOWN:
                    py += 1
                elif event.key == pygame.K_LEFT:
                    px -= 1

        if px < 0:
            px = 0
        elif px > tilemap.get_width():
            px = tilemap.get_width()

        if py < 0:
            py = 0
        elif py > tilemap.get_height():
            py = tilemap.get_height()

        # Does not stop in other direction
        if screen.get_width() > (tilemap.get_width() + mapx):
            mapx = tilemap.get_width() - screen.get_width()
            px = screen.get_width() - MAP_WIDTH_THRESH
        
        # Does not stop in other direction
        if screen.get_height() > (tilemap.get_height() + mapy):
            mapy = tilemap.get_height() - screen.get_height()
            py = screen.get_height() - MAP_HEIGHT_THRESH

        if px < MAP_WIDTH_THRESH:
            mapx += (MAP_WIDTH_THRESH - px)
            px = MAP_WIDTH_THRESH
        elif px > (screen.get_width() - MAP_WIDTH_THRESH):
            mapx -= ((MAP_WIDTH_THRESH + px) - screen.get_width())
            px = (screen.get_width() - MAP_WIDTH_THRESH)

        if py < MAP_HEIGHT_THRESH:
            mapy += (MAP_HEIGHT_THRESH - py)
            py = MAP_HEIGHT_THRESH
        elif py > (screen.get_height() - MAP_HEIGHT_THRESH):
            mapy -= ((MAP_HEIGHT_THRESH + py) - screen.get_height())
            py = (screen.get_height() - MAP_HEIGHT_THRESH)


        screen.blit(tilemap, (int(mapx), int(mapy)))
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(px), int(py)),
            16
        )

        pygame.display.flip()

    pygame.quit()
