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
pygame.display.set_caption("Hanoi Towers")

# set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set up adaptivity
# BODY_HEIGHT = DISPLAY_HEIGHT // 12
BODY_HEIGHT = 30
BASE_WIDTH = (DISPLAY_WIDTH - BODY_HEIGHT * 6) // 3
BASE_Y = DISPLAY_HEIGHT - BODY_HEIGHT * 2
COLUMN_X = (DISPLAY_HEIGHT - BODY_HEIGHT) // 2
COLUMN_Y = 2 * BODY_HEIGHT
COLUMN_HEIGHT = DISPLAY_HEIGHT // 3 * 2

# Sprites
POLE_IMG = pygame.image.load("sprites/pole.png")


class Stretchable:
    def __init__(self, display, images, pos, size):
        self.display = display

        l_img, m_img, r_img = images
        left, top = pos
        width, height = size

        self.left_image = pygame.image.load(l_img)
        self.right_image = pygame.image.load(r_img)
        self.mid_image = pygame.image.load(m_img)

        self.left_rect = self.left_image.get_rect()
        self.right_rect = self.right_image.get_rect()

        self.mid_image = pygame.transform.scale(
            self.mid_image, (width - self.left_rect.width * 2, height)
        )
        self.mid_rect = self.mid_image.get_rect()

        self.set_left(left)
        self.set_top(top)

    def set_centerx(self, value):
        self.mid_rect.centerx = value
        self.left_rect.right = self.mid_rect.left
        self.right_rect.left = self.mid_rect.right

    def get_centerx(self):
        return self.mid_rect.centerx

    def set_left(self, value):
        self.left_rect.left = value
        self.mid_rect.left = self.left_rect.right
        self.right_rect.left = self.right_rect.right

    def set_top(self, value):
        self.left_rect.top = value
        self.mid_rect.top = value
        self.right_rect.top = value

    def set_bottom(self, value):
        self.left_rect.bottom = value
        self.mid_rect.bottom = value
        self.right_rect.bottom = value

    def draw(self):
        self.display.blit(self.left_image, self.left_rect)
        self.display.blit(self.mid_image, self.mid_rect)
        self.display.blit(self.right_image, self.right_rect)


class StretchableRotated(Stretchable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_image = pygame.transform.rotate(self.left_image, 90)
        self.mid_image = pygame.transform.rotate(self.mid_image, 90)
        self.right_image = pygame.transform.rotate(self.right_image, 90)
        self.left_rect = self.left_image.get_rect()
        self.mid_rect = self.mid_image.get_rect()
        self.right_rect = self.right_image.get_rect()

    def set_centerx(self, value):
        self.mid_rect.centerx = value
        self.left_rect.centerx = value
        self.right_rect.centerx = value

    def get_centerx(self):
        return self.mid_rect.centerx

    def set_left(self, value):
        self.left_rect.left = value
        self.mid_rect.left = value
        self.right_rect.left = value

    def set_top(self, value):
        self.right_rect.top = value
        self.mid_rect.top = self.right_rect.bottom
        self.left_rect.top = self.mid_rect.bottom

    def set_bottom(self, value):
        self.left_rect.bottom = value
        self.mid_rect.bottom = self.left_rect.top
        self.right_rect.bottom = self.mid_rect.top


class Tower:
    def __init__(self, board, base_center_x):
        self.board = board
        self.blocks = []

        self.base = Stretchable(
            DISPLAYSURF,
            images=(
                "sprites/base_left.png",
                "sprites/base_mid.png",
                "sprites/base_right.png",
            ),
            pos=(0, BASE_Y),
            size=(BASE_WIDTH, BODY_HEIGHT),
        )
        self.column = StretchableRotated(
            DISPLAYSURF,
            images=(
                "sprites/base_left.png",
                "sprites/base_mid.png",
                "sprites/base_right.png",
            ),
            pos=(0, BASE_Y),
            size=(COLUMN_HEIGHT, BODY_HEIGHT),
        )

        self.column.set_top(COLUMN_Y)

        self.base.set_centerx(base_center_x)
        self.column.set_centerx(base_center_x)

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
        self.column.draw()
        self.base.draw()


class Block:
    def __init__(self, width, body_width, tower):
        self.tower = tower
        self.width = width
        self.position = self.tower.board.blocks_number - self.width

        self.body = Stretchable(
            DISPLAYSURF,
            images=(
                "sprites/ring_left.png",
                "sprites/ring_mid.png",
                "sprites/ring_right.png",
            ),
            pos=(0, BASE_Y),
            size=(body_width, BODY_HEIGHT),
        )

        self.body.set_centerx(self.tower.base.get_centerx())
        self.body.set_bottom(BASE_Y - self.position * BODY_HEIGHT)

    def draw(self):
        self.body.set_centerx(self.tower.base.get_centerx())
        self.body.set_bottom(BASE_Y - self.position * BODY_HEIGHT)
        self.body.draw()


class GameBoard:
    def __init__(self):
        self.towers = []
        self.blocks_number = 0

    def init_game(self, n):
        self.blocks_number = n
        self.towers = [Tower(self, DISPLAY_HEIGHT // 2 * (2 * i + 1)) for i in range(3)]
        body_width = (BASE_WIDTH - BODY_HEIGHT) // self.blocks_number
        self.towers[0].blocks = [
            Block(i, body_width * i, self.towers[0])
            for i in range(self.blocks_number, 0, -1)
        ]

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
