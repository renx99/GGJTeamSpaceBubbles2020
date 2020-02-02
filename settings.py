import pygame as pg
vec = pg.math.Vector2

# Game Settings
WIDTH = 1920
HEIGHT = 1080
FPS = 60
TITLE = 'Rust Busters <working title>'


TILESIZE = 32
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

BOB_RANGE = 10
BOB_SPEED = 2

DIRECTIONS = {
        'north': 180,
        'east': 270,
        'south': 0,
        'west': 90,
    }

# Player Settings
PLAYER = {
        'health': 100,
        'regen': 10,
        'speed': 5,
        'hit_rect': pg.Rect(0, 0, 128, 128),
        'image': 'dude.png'
    }

WEAPON_OFFSET = vec(30,10)

# Weapon Settings
WEAPONS = {
        'wrench': {
                'range': 2,
                'damage': 50
            },
        'bite': {
                'damage': 50,
                'range': 1,
            },
        'gun': {
                'range': 5,
                'damage': 100,
            }
    }

# Enemy Settings
ENEMIES = {
        'dog': {
            'speed': 3,
            'weapon': 'bite',
            'img': 'temp-dog.png',
            'hit_rect': pg.Rect(0, 0, 64, 64),
            'health': 100
        },
        'guard': {
            'speed': 1,
            'weapon': 'gun',
            'img': 'temp-guard.png',
            'hit_rect': pg.Rect(0, 0, 128, 128),
            'health': 200
        }
    }

# Layers
LAYERS = {
        'wall': 1,
        'player': 2,
        'enemy': 2,
        'bullet': 3,
        'item': 4,
        'effects': 5
    }

# Sounds
BG_MUSIC = 'combat_loop_fixed.ogg'
COMBAT_MUSIC = 'imperial_march.wav'
PLAYER_HIT_SOUNDS = ['WilhelmScream.wav']
ENEMY_HIT_SOUNDS = {'dog':['Chewie-chatting.wav'],
                    'guard':['WilhelmScream.wav']}
ENEMY_ALERT_SOUNDS = {'dog':['chewy_roar.wav'],
                        'guard':['yodalaughing.wav']}
WEAPON_SOUNDS = ['light-saber-on.wav']
EFFECT_SOUNDS = ['blaster-firing.wav']
