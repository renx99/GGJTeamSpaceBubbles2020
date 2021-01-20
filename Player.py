import pyglet
import json
import itertools


class Player:
    def __init__(self, sprite_config):
        # Sprite location
        self.x, self.y = 0, 0
        self.anchor_x, self.anchor_y = 0, 0
        self.offset_x, self.offset_y = 0, 0

        # Sprite name, provided by config file
        self.sprite_name = ""

        # Collection of sprite animations
        self.sprites = {}

        # Specifies which sprite is shown when draw is called
        self.active_anim = "down"

        # load data from json and assemble sprites
        with open(sprite_config, "r") as f:
            config_json = f.read()
            config = json.loads(config_json)
            for k, v in config.items():
                if k == "name":
                    self.sprite_name = v
                elif k == "actions":
                    for action, act_data in v.items():
                        sheet = pyglet.resource.image(act_data["file"])
                        grid = pyglet.image.ImageGrid(sheet, rows=1, columns=4)
                        anim = pyglet.image.Animation.from_image_sequence(grid, duration=act_data["timing"])
                        self.sprites[action] = pyglet.sprite.Sprite(anim)

    # Updates the animations to be show with the current position and returns sprite
    def draw(self):
        self.sprites[self.active_anim].x = self.x - self.offset_x
        self.sprites[self.active_anim].y = self.y - self.offset_y
        return self.sprites[self.active_anim].draw()

    # action is used to fetch and set which animation to show
    @property
    def action(self):
        return self.active_anim

    @action.setter
    def action(self, act):
        self.active_anim = act
        self.sprites[self.active_anim].x = self.x
        self.sprites[self.active_anim].y = self.y

    # Return a list of currently available actions used to set which animation to show
    def get_actions(self):
        return list(self.sprites)

    # Set scale for all sprites
    def set_scale(self, size):
        for act, sprite in self.sprites.items():
            sprite.scale = size

    # # Set anchor for all sprites
    # def set_anchor(self, x, y):
    #     for act, sprite in self.sprites.items():
    #         sprite.

if __name__ == "__main__":
    from pyglet.window import key

    pyglet.resource.path = ['./graphics']
    pyglet.resource.reindex()

    window = pyglet.window.Window()

    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    player = Player("player.json")

    testing = pyglet.text.Label("Testing....")
    testing.x, testing.y = 10, 10

    player.x = window.width // 2
    player.y = window.height // 2
    player.offset_x = player.sprites["right"].width // 2
    player.offset_y = player.sprites["right"].height // 2

    player.set_scale(2)

    @window.event
    def on_draw():
        window.clear()
        player.draw()
        testing.draw()


    counter = 0

    demo = itertools.cycle(player.get_actions())


    def change_action(dt):
        player.action = next(demo)


    def update(dt):
        testing.text = "Action: {}".format(player.active_anim)


    # def update(dt):
    #     global counter
    #
    #     if 0 <= counter < 180:
    #         player.action = "right"
    #     elif 180 <= counter < 360:
    #         player.action = "up"
    #     elif 360 <= counter < 520:
    #         player.action = "left"
    #     elif 520 <= counter < 720:
    #         player.action = "down"
    #     else:
    #         counter = 0
    #
    #
    #     counter += 1
        # print("counter: {} - delta time: {}".format(counter, dt))
        # print(player.sprites[player.active_anim].x, player.sprites[player.active_anim].y)


    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.clock.schedule_interval(change_action, 3)
    pyglet.app.run()
