class Tower:
    def __init__(self):
        self.blocks = []

    def put_block(self, block):
        top = self.take_block()
        if top != None:
            if top.width > block.width:
                self.blocks.append(top)
                self.blocks.append(block)
            else:
                self.blocks.append(top)
                block.last.blocks.append(block)
            return
        self.blocks.append(block)
        
    def take_block(self):
        if len(self.blocks) > 0:
            block = self.blocks.pop()
            block.last = self
            return block
        return None


class Block:
    def __init__(self, width):
        self.width = width
        self.last = None


class GameBoard:
    def __init__(self):
        self.towers = []
        self.blocks_number = 0
    
    def init_game(self, n):
        self.blocks_number = n
        self.towers = [Tower() for i in range(3)]
        self.towers[0].blocks = [Block(i) for i in range(self.blocks_number, 0, -1)]

    def check_win(self):
        if self.towers[2] == self.blocks_number:
            return True
        return False
