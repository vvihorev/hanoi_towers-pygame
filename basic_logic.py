import getch
from os import system


def cls():
    try:
        system('clear')
    except:
        system('cls')


def get_input(for_init=False):
    #TODO prevent bad input (alphabet) and over 3
    input = getch.getch()
    return int(input)


def init_game():
    print("Enter number of blocks to play with: ")
    n = get_input()

    first = [i for i in range(n,0,-1)]
    second = []
    third = []
    return first, second, third


def check_win(towers):
    if len(towers[1]) + len(towers[2]) == 0:
        return True
    return False


def draw_game(towers, active='', tower=0):
    cls()
    for i in range(1,4):
        print(i, ': ', towers[i], ' ', (active if tower == i else ''))


def move_block(towers):
    i = get_input()
    if len(towers[i]) > 0:
        active = towers[i].pop()
        draw_game(towers, active, i)

        j = get_input()
        if len(towers[j]) > 0:
            top = towers[j].pop()
            if top <= active:
                towers[i].append(active)
                towers[j].append(top)
                return None
            towers[j].append(top)
        towers[j].append(active)
    return None
        

cls()
first, second, third = init_game()
playing = True
towers = {1:first, 2:second, 3:third}
draw_game(towers)


while playing:
    if check_win(towers):
        playing = False
        draw_game(towers)
        print('You Won!')
        continue

    move_block(towers)
    draw_game(towers)
