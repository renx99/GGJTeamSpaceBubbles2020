import pyglet


class Player:
    def __init__(self, sprites):
        # self.anim = {}
        # self.sheet = {}
        # self.grid = {}
        # self.anim = {}
        # self.sprite = {}

        # self.active_anim = "right"

        # for action, sprite in sprites.items():
        #     sheet = pyglet.resource.image(sprite)
        #     grid = pyglet.image.ImageGrid(sheet, rows=1, columns=4)
        #     anim = pyglet.image.Animation.from_image_sequence(grid, duration=0.25)
        #     self.sprite[action] = pyglet.sprite.Sprite(anim)
        #
        #     print("action: {}, sprite: {}".format(action, sprite))

        sheet = pyglet.resource.image(sprites)
        grid = pyglet.image.ImageGrid(sheet, rows=1, columns=4)
        anim = pyglet.image.Animation.from_image_sequence(grid, duration=0.25)

        self.sprite = pyglet.sprite.Sprite(anim)

    def draw(self):
        # print(type(self.sprite["right"]))
        # return self.sprite["right"]
        return self.sprite.draw()


if __name__ == "__main__":
    pyglet.resource.path = ['./graphics']
    pyglet.resource.reindex()
    window = pyglet.window.Window()

    player = Player("dude-right.png")
    testing = pyglet.text.Label("Testing....")

    @window.event
    def on_draw():
        window.clear()
        player.draw()
        testing.draw()

    pyglet.app.run()
