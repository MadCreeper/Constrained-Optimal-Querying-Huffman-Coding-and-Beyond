import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
from random import sample
from collections import deque
from copy import deepcopy

DOWN, RIGHT = 0, 1 # indicating ship direction
EMPTY, PLACED = np.uint32(0), np.uint32(1)

    

class Board:
    
    def __init__(self, N, M, ship_dims, board_count=1,randseed=0, debug=False) -> None:
        self.HEIGHT, self.WIDTH = N, M
        self.ship_dims = ship_dims
        self.sim_count = board_count
        random.seed(randseed)
        self.debug = debug
        
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
    
    def place_boat_copy(self, cur_board, sx, sy, facing, ship_dim): # Place boat at (sx, sy). Returns placed board if legal, otherwise returns None.
        board = deepcopy(cur_board)
        if facing == DOWN:
            for x in range(sx, sx + ship_dim):
                if board[x][sy] == PLACED: # already placed, illegal pos
                    return None
                board[x][sy] = PLACED
        if facing == RIGHT:
            for y in range(sy, sy + ship_dim):
                if board[sx][y] == PLACED: # already placed, illegal pos
                    return None
                board[sx][y] = PLACED
                
        return board
       
class MonteCarloBoard(Board):
    def random_legal_pos(self, facing, ship_dim): # generate legal sx, sy given facing such that ship is in bounds
        if facing == DOWN:
            return random.randrange(self.HEIGHT - ship_dim + 1), random.randrange(self.WIDTH)
        if facing == RIGHT:
            return random.randrange(self.HEIGHT), random.randrange(self.WIDTH - ship_dim + 1)
    
    def gen_board(self):
        board = np.zeros((self.HEIGHT, self.WIDTH))
        for ship_dim in self.ship_dims:
            while True:
         
                facing = random.randrange(2) 
                if facing == DOWN and ship_dim > self.HEIGHT:
                    facing = RIGHT
                if facing == RIGHT and ship_dim > self.WIDTH:
                    facing = DOWN
                
                sx, sy = self.random_legal_pos(facing, ship_dim)
                #print(sx, sy, facing)
                if self.test_legal(board, sx, sy, facing, ship_dim):
                   self.place_boat(board, sx, sy, facing, ship_dim)
                   break 
        return board     
                            
    def randomboard(self, constr=None):
        boards = []
        for i in range(self.sim_count):
            board = self.gen_board()
            if constr is not None:
                and_board = np.logical_and(board, constr)
                if not np.array_equal(and_board, constr): # board and constraint mismatch
                    continue
            if self.debug:
                print(board)
            boards.append(board)
        
        sum_boards = np.array(sum(boards))
        valid_count = len(boards)
        #print(sum_boards)
        normalized_boards = sum_boards / valid_count
        print(normalized_boards)
        print("Done calculating board")
        #print(np.sum(normalized_boards)) 
        return normalized_boards

class SimulationBoard(Board): # N*M Battleship board, full simulation
    

    def gen_boards(self):
        Q = deque()
        Q.append((0, np.full((self.HEIGHT, self.WIDTH), EMPTY, dtype=np.uint32)))
        for idx, ship_dim in enumerate(self.ship_dims): # loop all the ships
            
            while(Q[0][0] != idx + 1):
                if(len(Q) % 1000000 == 0):
                    print(len(Q)) 
                cur = Q[0]
                cur_board = cur[1]
                Q.popleft()
                
                facing = DOWN
                for sx in range(self.HEIGHT - ship_dim + 1):
                    for sy in range(self.WIDTH):
                        new_board = self.place_boat_copy(cur_board, sx, sy, facing, ship_dim)
                        if new_board is not None:
                            Q.append((cur[0] + 1, new_board))
                        
                facing = RIGHT
                for sx in range(self.HEIGHT):
                    for sy in range(self.WIDTH - ship_dim + 1):
                        new_board = self.place_boat_copy(cur_board, sx, sy, facing, ship_dim)
                        if new_board is not None:
                            Q.append((cur[0] + 1, new_board))

            if self.debug: # print some random boards to visualize
                for _, board in sample(Q, 1):
                    print(board)
            print("Done round", idx + 1, "total count: ", len(Q))
        
        
        all_boards = [board for _, board in Q]
        return all_boards
    
    
    
def test_monte_carlo():
    MONTE_CARLO_CNT = 10000
    N, M = 10, 10
    
    start = time.time()
    A = MonteCarloBoard(N=N, M=M, board_count=MONTE_CARLO_CNT, ship_dims=[5, 4, 3, 3, 2], randseed=114514, debug=False)
    sns.set(font_scale=1.5)
    
    constr = np.full((N,M), False, dtype=bool)
    constr[4][4] = True
    constr[7][9] = True
    
    randomboard = A.randomboard(constr=constr)
    ax = sns.heatmap(data=randomboard, annot=True,cmap="RdBu_r")
    
    print(f"Done, took {time.time() - start} secs")
    plt.title(f"MonteCarlo-{MONTE_CARLO_CNT}")
    plt.show()


            
if __name__ == "__main__":
    
    sim = SimulationBoard(N=10, M=10, ship_dims=[5, 4, 3], debug=True)
    boards = sim.gen_boards()
    