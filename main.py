from objects import *


Board = GameBoard()
Board.init_game(4)

def draw_game():
    for tower in Board.towers:
        print(tower.blocks)
