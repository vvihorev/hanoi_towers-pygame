from objects import *


Board = GameBoard()
Board.init_game(4)

for tower in Board.towers:
    print(tower.blocks)