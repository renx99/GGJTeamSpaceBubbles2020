from abc import ABC

import pyglet

from Player import Player


class Repair(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Repair, self).__init__()

        self.label = pyglet.text.Label('Testing...')

        # self.player = Player("dude-right.png")
        self.player = Player({
            "right": "dude-right.png",
            "left": "dude-left.png",
            "up": "dude-up.png",
            "down": "dude-down.png",
        })

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.label.draw()



if __name__ == "__main__":

    main_batch = pyglet.graphics.Batch()

    pyglet.resource.path = ['./graphics']
    pyglet.resource.reindex()

    repair = Repair()
    pyglet.app.run()
