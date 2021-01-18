import pyglet


class Player:
    def __init__(self, sprites):
        self.anim = {}
        self.sheet = {}
        self.grid = {}
        self.anim = {}
        self.sprite = {}

        self.active_anim = "up"

        for action, sprite in sprites.items():
            sheet = pyglet.resource.image(sprite)
            grid = pyglet.image.ImageGrid(sheet, rows=1, columns=4)
            anim = pyglet.image.Animation.from_image_sequence(grid, duration=0.25)
            self.sprite[action] = pyglet.sprite.Sprite(anim)

            print("action: {}, sprite: {}".format(action, sprite))

        # self.sprite = pyglet.resource.image(sprite)
        # self.grid = pyglet.image.ImageGrid(self.sprite, rows=1, columns=4)
        # self.anim = pyglet.image.Animation.from_image_sequence(self.grid, duration=0.25)
        #
        # self.anim = pyglet.sprite.Sprite(self.anim)

    def draw(self):
        return self.sprite["right"]
