import pyglet


class Player:
    def __init__(self, sprites):

        self.sprite = {}

        self.active_anim = "right"

        for action, sprite in sprites.items():
            sheet = pyglet.resource.image(sprite)
            grid = pyglet.image.ImageGrid(sheet, rows=1, columns=4)
            anim = pyglet.image.Animation.from_image_sequence(grid, duration=0.25)
            self.sprite[action] = pyglet.sprite.Sprite(anim)

            if action == "right":
                anim_left = anim.get_transform(flip_x=True)
                self.sprite["left"] = pyglet.sprite.Sprite(anim_left)

    def draw(self):
        # print(type(self.sprite["right"]))
        # return self.sprite["right"]
        return self.sprite[self.active_anim].draw()


if __name__ == "__main__":
    pyglet.resource.path = ['./graphics']
    pyglet.resource.reindex()
    window = pyglet.window.Window()

    player = Player({
        "right": "dude-right.png",
        "up": "dude-up.png",
        "down": "dude-down.png",
        "attack-right": "dude-right-attack.png"
    })
    testing = pyglet.text.Label("Testing....")


    @window.event
    def on_draw():
        window.clear()
        player.draw()
        testing.draw()


    pyglet.app.run()
