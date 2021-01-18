import pyglet

class Player:
    def __init__(self, sprite):

        self.sprite = pyglet.resource.image(sprite)
        self.grid = pyglet.image.ImageGrid(self.sprite, rows=1, columns=4)
        self.anim = pyglet.image.Animation.from_image_sequence(self.grid, duration=0.25)

        self.anim = pyglet.sprite.Sprite(self.anim)

    def draw(self):
        return self.anim.draw()