import pygame as pg
from random import uniform, choice, randint, random
from settings import *
import mapprocess
#import pytweening as tween
from itertools import chain
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, mapprocess.collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, mapprocess.collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYERS['player']
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.stallkludge = 0
        self.pingpong = 1
        self.imageindex = 0
        self.imagemap = game.player_img
        self.image = self.imagemap.subsurface(PLAYER['hit_rect'])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER['hit_rect']
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.facing = 'south'
        self.last_shot = 0
        self.health = PLAYER['health']
        self.weapon = 'wrench'
        self.damaged = False
        self.pressed = None

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.facing = 'west'
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.facing = 'east'
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.facing = 'north'
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.facing = 'south'
        if keys[pg.K_SPACE]:
            self.attack()

    def attack(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def update(self):
        self.get_keys()

        # In your game loop, check for key states:
        if self.pressed == 'left':
            self.pos.x -= PLAYER['speed']
        if self.pressed == 'right':
            self.pos.x += PLAYER['speed']
        if self.pressed == 'up':
            self.pos.y -= PLAYER['speed']
        if self.pressed == 'down':
            self.pos.y += PLAYER['speed']

        self.pos = vec(self.pos.x, self.pos.y)

        # slows down the animation rate
        self.stallkludge += 1
        if self.stallkludge > 15:
            self.stallkludge = 0
            if self.imageindex <= 0:
                self.pingpong = 1
            elif self.imageindex >= 2:
                self.pingpong = -1
            self.imageindex += self.pingpong
            if self.facing == 'south':
                self.image = self.imagemap.subsurface(self.imageindex*32, 0*64, 32, 64)
            elif self.facing == 'east':
                self.image = self.imagemap.subsurface(self.imageindex*32, 1*64, 32, 64)
            elif self.facing == 'north':
                self.image = self.imagemap.subsurface(self.imageindex*32, 2*64, 32, 64)
            elif self.facing == 'west':
                self.image = self.imagemap.subsurface(self.imageindex*32, 3*64, 32, 64)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER['health']:
            self.health = PLAYER['health']


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        mob_type = 'dog'  # TODO: add gaurds
        self._layer = LAYERS['enemy']
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.stallkludge = 0
        self.imageindex = 0
        self.facing = 'south'
        self.game = game
        self.imagemap = game.mob_img.copy()
        self.image = self.imagemap.subsurface(ENEMIES[mob_type]['hit_rect'])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = ENEMIES[mob_type]['hit_rect'].copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        self.health = ENEMIES[mob_type]['health']
        self.radius = ENEMIES[mob_type]['radius']
        self.speed = choice([ENEMIES[mob_type]['speed']])
        self.target = game.player

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def get_facing(self):
        self.facing = 'west'
        self.facing = 'east'
        self.facing = 'north'
        self.facing = 'south'

    def update(self):
        #print('dog update')

        self.pos.x += ENEMIES['dog']['speed']
        self.pos.y += ENEMIES['dog']['speed']

        self.pos = vec(self.pos.x, self.pos.y)

        target_dist = self.target.pos - self.pos
        mob_type = 'dog'

        if random() < 0.002:
            print('bark')
            #choice(self.game.zombie_moan_sounds).play()

        self.stallkludge += 1
        if self.stallkludge > 15:
            self.stallkludge = 0
            self.imageindex = (self.imageindex + 1) % 4

            if self.facing == 'south':
                self.image = self.imagemap.subsurface(self.imageindex*32, 3*32, 32, 32)
            elif self.facing == 'east':
                self.image = self.imagemap.subsurface(self.imageindex*32, 1*32, 32, 32)
            elif self.facing == 'north':
                self.image = self.imagemap.subsurface(self.imageindex*32, 2*32, 32, 32)
            elif self.facing == 'west':
                self.image = self.imagemap.subsurface(self.imageindex*32, 0*32, 32, 32)

        if target_dist.length_squared() < ENEMIES[mob_type]['radius']**2:
            # Chase mode
            # TODO: make chase
            pass
        else:
            # Patrol Mode
            pass

            #self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        #self.avoid_mobs()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))

    def draw_health(self):
        enemy = 'dog'  # TODO: add guards
        if self.health > 60:
            col = (0, 255, 0)  # GREEN
        elif self.health > 30:
            col = (255, 255, 0)  # YELLOW
        else:
            col = (0, 0, 255)  # RED
        width = int(self.rect.width * self.health / ENEMIES[enemy]['health'])
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < ENEMIES[enemy]['health']:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = LAYER['bullet']
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = LAYER['effects']
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = LAYER['items']
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        #self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = 0  # BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
