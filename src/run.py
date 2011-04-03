import Game
import Menus

game = Game.GameLoop(640, 480, 30)
titlescreen = Menus.Logo()

game.Start(titlescreen)

