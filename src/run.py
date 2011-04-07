import Game
import Menus

game = Game.GameLoop('Shattered Silence', 640, 480, 30)
titlescreen = Menus.Logo()

game.Start(titlescreen)

