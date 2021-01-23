import pyglet
from pyglet.window import key

from Player import Player


class Repair(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Repair, self).__init__(*args, **kwargs)

        self.label = pyglet.text.Label('Testing...')

        self.player = Player("player.json")
        self.player.set_scale(2)

        self.speed = 150

        # keyboard handling
        self.key_handler = key.KeyStateHandler()
        self.push_handlers(self.key_handler)

        # joystick  handling
        self.joysticks = pyglet.input.get_joysticks()
        assert self.joysticks, "No joystick detected."
        if self.joysticks:
            self.joy1 = self.joysticks[0]
        self.joy1.open()

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.label.draw()

    def update(self, dt):
        if self.key_handler[key.LEFT] or self.joy1.x < -0.5:
            self.player.x -= self.speed * dt
            self.player.action = "left"
        if self.key_handler[key.RIGHT] or self.joy1.x > 0.5:
            self.player.x += self.speed * dt
            self.player.action = "right"
        if self.key_handler[key.UP] or self.joy1.y < -0.5:
            self.player.y += self.speed * dt
            self.player.action = "up"
        if self.key_handler[key.DOWN] or self.joy1.y > 0.5:
            self.player.y -= self.speed * dt
            self.player.action = "down"


def update(dt):
    repair.update(dt)


if __name__ == "__main__":
    main_batch = pyglet.graphics.Batch()

    pyglet.resource.path = ['./graphics']
    pyglet.resource.reindex()

    repair = Repair(width=1920, height=1080)

    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
