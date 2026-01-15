import arcade
class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()

        self.player = arcade.SpriteList()

        self.win_or_not = False
        self.background_color = arcade.color.BLACK