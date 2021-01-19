import pyglet


class Player:
    def __init__(self, sprite_sheet):
        self.x, self.y = 0, 0

        self.sprites = {}

        self.active_anim = "down"

        for action, sprite in sprite_sheet.items():
            sheet = pyglet.resource.image(sprite)
            grid = pyglet.image.ImageGrid(sheet, rows=1, columns=4)
            anim = pyglet.image.Animation.from_image_sequence(grid, duration=0.25)
            self.sprites[action] = pyglet.sprite.Sprite(anim)

    def draw(self):
        self.sprites[self.active_anim].x = self.x
        self.sprites[self.active_anim].y = self.y
        return self.sprites[self.active_anim].draw()

    @property
    def action(self):
        return self.active_anim

    @action.setter
    def action(self, act):
        self.active_anim = act
        self.sprites[self.active_anim].x = self.x
        self.sprites[self.active_anim].y = self.y



if __name__ == "__main__":
    from pyglet.window import key

    pyglet.resource.path = ['./graphics']
    pyglet.resource.reindex()

    window = pyglet.window.Window()

    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    player = Player({
        "right": "dude-right.png",
        "left": "dude-left.png",
        "up": "dude-up.png",
        "down": "dude-down.png",
    })

    testing = pyglet.text.Label("Testing....")
    player.x = window.width // 2
    player.y = window.height // 2

    @window.event
    def on_draw():
        window.clear()
        player.draw()
        testing.draw()


    counter = 0


    def update(dt):
        global counter

        if 0 <= counter < 180:
            player.x += 30 * dt
            player.action = "right"
        elif 180 <= counter < 360:
            player.y += 30 * dt
            player.action = "up"
        elif 360 <= counter < 520:
            player.x -= 30 * dt
            player.action = "left"
        elif 520 <= counter < 720:
            player.y -= 30 * dt
            player.action = "down"
        else:
            counter = 0

        counter += 1
        # print("counter: {} - delta time: {}".format(counter, dt))
        # print(player.sprites[player.active_anim].x, player.sprites[player.active_anim].y)


    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
