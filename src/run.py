import Game
import Menus

game = Game.GameLoop(640, 480, 30)
titlescreen = Menus.Title()

game.Start(titlescreen)
