import pygame, random, sys

# ---- 設定 ----
CELL_SIZE = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
FPS = 60
DROP_INTERVAL = 500   # ms

# ---- テトリミノ形状 ----
SHAPES = [
    [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],      # I
    [[1,0,0],[1,1,1],[0,0,0]],                       # J
    [[0,0,1],[1,1,1],[0,0,0]],                       # L
    [[1,1],[1,1]],                                    # O
    [[0,1,1],[1,1,0],[0,0,0]],                       # S
    [[0,1,0],[1,1,1],[0,0,0]],                       # T
    [[1,1,0],[0,1,1],[0,0,0]]                        # Z
]

# ---- ボードクラス ----
class Board:
    def __init__(self):
        self.grid = [[(0,(0,0,0)) for _ in range(COLS)] for _ in range(ROWS)]

    def inside(self,x,y): return 0 <= x < COLS and 0 <= y < ROWS

    def empty_at(self,x,y):
        return self.inside(x,y) and self.grid[y][x][0] == 0

    def place_block(self,shape,offset,color):
        ox,oy = offset
        for y,row in enumerate(shape):
            for x,val in enumerate(row):
                if val:
                    self.grid[oy+y][ox+x] = (1,color)

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell[0]==0 for cell in row)]
        cleared = ROWS - len(new_grid)
        for _ in range(cleared):
            new_grid.insert(0,[(0,(0,0,0))]*COLS)
        self.grid = new_grid
        return cleared

# ---- テトリミノクラス ----
class Piece:
    def __init__(self,b):
        self.board=b
        self.shape=random.choice(SHAPES)
        self.color=tuple(random.randint(50,255) for _ in range(3))
        self.x=COLS//2 - len(self.shape[0])//2
        self.y=0

    def rotate(self):
        rotated=[list(row) for row in zip(*self.shape[::-1])]
        if self.valid_position(rotated,(self.x,self.y)):
            self.shape=rotated

    def valid_position(self,shape=None,offset=None):
        shape=shape or self.shape
        ox,oy=offset or (self.x,self.y)
        for y,row in enumerate(shape):
            for x,val in enumerate(row):
                if val:
                    nx,ny=ox+x,oy+y
                    if not self.board.inside(nx,ny) or not self.board.empty_at(nx,ny):
                        return False
        return True

    def move(self,dx,dy):
        new_x,new_y=self.x+dx,self.y+dy
        if self.valid_position(offset=(new_x,new_y)):
            self.x,self.y=new_x,new_y
            return True
        return False

    def hard_drop(self):
        while self.move(0,1): pass

# ---- メイン ----
def main():
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    clock=pygame.time.Clock()
    board=Board()
    piece=Piece(board)
    last_drop=pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT: piece.move(-1,0)
                elif event.key==pygame.K_RIGHT: piece.move(1,0)
                elif event.key==pygame.K_DOWN: piece.move(0,1)
                elif event.key==pygame.K_UP: piece.rotate()
                elif event.key==pygame.K_SPACE: piece.hard_drop()

        if pygame.time.get_ticks()-last_drop>DROP_INTERVAL:
            if not piece.move(0,1):
                board.place_block(piece.shape,(piece.x,piece.y),piece.color)
                board.clear_lines()
                piece=Piece(board)
            last_drop=pygame.time.get_ticks()

        screen.fill((30,30,30))
        for y,row in enumerate(board.grid):
            for x,(filled,color) in enumerate(row):
                if filled:
                    rect=pygame.Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                    pygame.draw.rect(screen,color,rect)
                    pygame.draw.rect(screen,(0,0,0),rect,1)

        for y,row in enumerate(piece.shape):
            for x,val in enumerate(row):
                if val:
                    rect=pygame.Rect((piece.x+x)*CELL_SIZE,
                                     (piece.y+y)*CELL_SIZE,
                                     CELL_SIZE,CELL_SIZE)
                    pygame.draw.rect(screen,piece.color,rect)
                    pygame.draw.rect(screen,(0,0,0),rect,1)

        pygame.display.flip()
        clock.tick(FPS)

if __name__=="__main__":
    main()
