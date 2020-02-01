import pygame as pg
vec = pg.math.Vector2

# Game Settings
WIDTH = 1920
HEIGHT = 1080
FPS = 60

TILESIZE = 64
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

# Player Settings
PLAYER_HEALTH = 100
PLAY_REGEN = 10
PLAYER_SPEED = 5
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
WEAPON_OFFSET = vec(30,10)

# Weapon Settings
WEAPONS = {}
WEAPONS['wrench'] = {'damage': 50}

# Enemy Settings
ENEMIES = {}
ENEMIES['dog'] = {
                    'damage':20,
                    'range':1,
                    'speed':3
                    }
ENEMIES['guard'] = {
                    'damage':34,
                    'range':5,
                    'speed':1
                    }

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
ENEMY_LAYER = 2

# Sounds
BG_MUSIC = ''
COMBAT_MUSIC = ''
WEAPON_SOUNDS = {}
EFFECT_SOUNDS = {}