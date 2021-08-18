class Tower:
    def __init__(self):
        self.blocks = []

    def put_block(self, block, old):
        top = self.take_block()
        if top != None:
            if top.width > block.width:
                self.blocks.append(top)
                self.blocks.append(block)
            else:
                self.blocks.append(top)
                old.blocks.append(block)
        
    def take_block(self):
        if len(self.blocks) > 0:
            return self.blocks.pop()
        return None


class Block:
    def __init__(self, width) -> None:
        self.width = width
        self.last = None


class GameBoard:
    def __init__(self):
        self.towers = []
        self.blocks_number = 0
    
    def init_game(self, n):
        self.blocks_number = n
        self.towers = [Tower() for i in range(3)]
        # TODO blocks have to be separate objects
        self.towers[0].blocks = [i for i in range(self.blocks_number, 0, -1)]

    def check_win(self):
        if self.towers[2] == self.blocks_number:
            return True
        return False
