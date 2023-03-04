import pygame, sys
from pygame.locals import *

pygame.init()

# fps settings
FPS = 30
fpsClock = pygame.time.Clock()

# set up a window
DISPLAY_HEIGHT = 300
DISPLAY_WIDTH = DISPLAY_HEIGHT * 3
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0, 32)
pygame.display.set_caption('Hanoi Towers')

# set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set up adaptivity
BODY_HEIGHT = DISPLAY_HEIGHT // 12
BASE_WIDTH = (DISPLAY_WIDTH - BODY_HEIGHT * 6) // 3
BASE_Y = (DISPLAY_HEIGHT - BODY_HEIGHT * 2)
COLUMN_X = (DISPLAY_HEIGHT - BODY_HEIGHT) // 2
COLUMN_Y = 2 * BODY_HEIGHT
COLUMN_HEIGHT = DISPLAY_HEIGHT // 3 * 2


class Tower:
    def __init__(self, board, base_center_x):
        self.board = board
        self.blocks = []
        self.base = pygame.Rect(0, BASE_Y, BASE_WIDTH, BODY_HEIGHT)
        self.column = pygame.Rect(0, COLUMN_Y, BODY_HEIGHT, COLUMN_HEIGHT)
        self.base.centerx = base_center_x
        self.column.centerx = base_center_x

    def put_block(self, block):
        top = self.take_block()
        if top != None:
            if top.width > block.width:
                self.blocks.append(top)
                self.blocks.append(block)
                block.tower = self
                block.position = top.position + 1
            else:
                self.blocks.append(top)
                block.tower.blocks.append(block)
            return
        self.blocks.append(block)
        block.tower = self
        block.position = 0

    def take_block(self):
        if len(self.blocks) > 0:
            block = self.blocks.pop()
            block.tower = self
            return block
        return None

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, BLACK, self.base)
        pygame.draw.rect(DISPLAYSURF, BLACK, self.column)


class Block:
    def __init__(self, width, body_width, tower):
        self.tower = tower
        self.width = width
        self.position = (self.tower.board.blocks_number - self.width)
        self.body = pygame.Rect(0, 0, body_width, BODY_HEIGHT)
        self.body.centerx = self.tower.base.centerx
        self.body.bottom = BASE_Y - self.position * BODY_HEIGHT

    def draw(self):
        self.body.centerx = self.tower.base.centerx
        self.body.bottom = BASE_Y - self.position * BODY_HEIGHT
        pygame.draw.rect(DISPLAYSURF, BLACK, self.body)


class GameBoard:
    def __init__(self):
        self.towers = []
        self.blocks_number = 0

    def init_game(self, n):
        self.blocks_number = n
        self.towers = [Tower(self, DISPLAY_HEIGHT // 2 * (2*i + 1)) for i in range(3)]
        body_width = (BASE_WIDTH - BODY_HEIGHT) // self.blocks_number
        self.towers[0].blocks = [Block(i, body_width * i, self.towers[0]) for i in range(self.blocks_number, 0, -1)]

    def draw(self):
        for tower in self.towers:
            tower.draw()
            for block in tower.blocks:
                block.draw()


class InputHandler:
    def __init__(self, board):
        self.block = None
        self.board = board

    def handle(self, n):
        n -= 1
        if self.block != None:
            self.board.towers[n].put_block(self.block)
            self.block = None
        else:
            self.block = self.board.towers[n].take_block()


# create game objects
Board = GameBoard()
Handler = InputHandler(Board)
Board.init_game(4)


# main game loop
while True:
    DISPLAYSURF.fill(WHITE)

    Board.draw()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                Handler.handle(1)
            if event.key == pygame.K_2:
                Handler.handle(2)
            if event.key == pygame.K_3:
                Handler.handle(3)

    pygame.display.update()
    fpsClock.tick(FPS)
