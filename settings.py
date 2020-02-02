import pygame as pg
vec = pg.math.Vector2


# Game Settings
WIDTH = int(abs(1280 ))
HEIGHT = int(abs(720 ))
FPS = 60
TITLE = 'I Am Lonely at the End of the World, What is This New Friend That I Have to Repair!? '

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
        'hit_rect': pg.Rect(32, 0, 32, 64),
        'image': 'dude.png',
        'weapon': 'wrench'
    }

WEAPON_OFFSET = vec(30,10)
BODY_OFFSET = vec(30,10)

# Weapon Settings
WEAPONS = {
        'wrench': {
                'range': 2,
                'damage': 50,
                'rate': 2
            },
        'bite': {
                'damage': 34,
                'range': 1,
                'rate': 1
            },
        'gun': {
                'range': 5,
                'damage': 60,
                'rate': 1
            }
    }

# Enemy Settings
ENEMIES = {
        'dog': {
            'speed': 3,
            'weapon': 'bite',
            'image': 'dog.png',
            'hit_rect': pg.Rect(0, 0, 32, 32),
            'health': 100,
            'radius': 10
        },
        'guard': {
            'speed': 1,
            'weapon': 'gun',
            'image': 'guard.png',
            'hit_rect': pg.Rect(0, 0, 32, 64),
            'health': 200,
            'radius': 10
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
MENU_MUSIC = 'menu_loop.ogg'
BG_MUSIC = 'combat_area_loop.ogg'
COMBAT_MUSIC = 'ambient_loop.ogg'
COMBAT_AREA_MUSIC = 'combat_area_loop.ogg'
PLAYER_HIT_SOUNDS = ['WilhelmScream.wav']
ENEMY_HIT_SOUNDS = {'dog':['Chewie-chatting.wav'],
                    'guard':['WilhelmScream.wav']}
ENEMY_ALERT_SOUNDS = {'dog':['chewy_roar.wav'],
                        'guard':['yodalaughing.wav']}
WEAPON_SOUNDS = ['light-saber-on.wav']
EFFECT_SOUNDS = ['blaster-firing.wav']
