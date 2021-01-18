import pyglet


class Player:
    def __init__(self, sprites):
        self.sprite = {}

        self.active_anim = "left"

        for action, sprite in sprites.items():
            sheet = pyglet.resource.image(sprite)
            grid = pyglet.image.ImageGrid(sheet, rows=1, columns=4)
            anim = pyglet.image.Animation.from_image_sequence(grid, duration=0.25)
            self.sprite[action] = pyglet.sprite.Sprite(anim)

    def draw(self):
        return self.sprite[self.active_anim].draw()


if __name__ == "__main__":
    pyglet.resource.path = ['./graphics']
    pyglet.resource.reindex()
    window = pyglet.window.Window()

    player = Player({
        "right": "dude-right.png",
        "left": "dude-left.png",
        "up": "dude-up.png",
        "down": "dude-down.png",
    })

    player.sprite[player.active_anim].x = window.width // 2 - 16
    player.sprite[player.active_anim].y = window.height // 2 - 32

    testing = pyglet.text.Label("Testing....")


    @window.event
    def on_draw():
        window.clear()
        player.draw()
        testing.draw()


    pyglet.app.run()
