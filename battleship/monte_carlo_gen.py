from audioop import avg
from locale import normalize
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time

DOWN, RIGHT = 0, 1 # indicating ship direction
EMPTY, PLACED = False, True

class avgBoard:
    
    
    
    def __init__(self, N, board_count, ship_dims, randseed=0, debug=False) -> None:
        self.grid_size = N
        self.ship_dims = ship_dims
        self.sim_count = board_count
        random.seed(randseed)
        self.debug = debug
        
        

    
    def random_legal_pos(self, facing, ship_dim): # generate legal sx, sy given facing such that ship is in bounds
        if facing == DOWN:
            return random.randrange(self.grid_size - ship_dim + 1), random.randrange(self.grid_size)
        if facing == RIGHT:
            return random.randrange(self.grid_size), random.randrange(self.grid_size - ship_dim + 1)
            
    
    def test_legal(self, board, sx, sy, facing, ship_dim) -> bool:
        if facing == DOWN:
            for x in range(sx, sx + ship_dim):
                if board[x][sy] == PLACED: # already placed in that place
                    return False           

        if facing == RIGHT:
            for y in range(sy, sy + ship_dim):
                if board[sx][y] == PLACED: # already placed in that place
                    return False
        
        return True
        
    def place_boat(self, board, sx, sy, facing, ship_dim):
        if facing == DOWN:
            for x in range(sx, sx + ship_dim):
                board[x][sy] = PLACED

        if facing == RIGHT:
            for y in range(sy, sy + ship_dim):
                board[sx][y] = PLACED
    
    def gen_board(self):
        board = np.zeros((self.grid_size, self.grid_size))
        for ship_dim in self.ship_dims:
            while True:
                facing = random.randrange(2) 
                sx, sy = self.random_legal_pos(facing, ship_dim)
                #print(sx, sy, facing)
                if self.test_legal(board, sx, sy, facing, ship_dim):
                   self.place_boat(board, sx, sy, facing, ship_dim)
                   break 
        return board     
                            
    def randomboard(self):
        boards = []
        for i in range(self.sim_count):
            board = self.gen_board()
            if self.debug:
                print(board)
            boards.append(board)
        
        sum_boards = np.array(sum(boards))
        #print(sum_boards)
        normalized_boards = sum_boards / self.sim_count
        print(normalized_boards)
        print("Done calculating board")
        return normalized_boards
        #print(np.sum(normalized_boards))
        
        
        
            
if __name__ == "__main__":
    
    MONTE_CARLO_CNT = 100000
    
    start = time.time()
    A = avgBoard(N=6, board_count=MONTE_CARLO_CNT, ship_dims=[5, 4, 3, 3, 2], randseed=114514, debug=False)
    sns.set(font_scale=1.5)
    ax = sns.heatmap(data=A.randomboard(), annot=True,cmap="RdBu_r")
    
    print(f"Done, took {time.time() - start} secs")
    plt.title(f"MonteCarlo-{MONTE_CARLO_CNT}")
    plt.show()
    