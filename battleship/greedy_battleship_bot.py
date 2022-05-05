import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from BoardGenerator import SimulationBoard
from copy import deepcopy
import seaborn as sns
MISS, HIT, UNKNOWN = 0, 1, 2
DOWN, RIGHT = 0, 1 # indicating ship direction
EMPTY, PLACED = np.uint32(0), np.uint32(1)

def find_nearests(arr, v, eps=1e-6):
    """returns list of indexes in arr that has value closest to v (can be multiple)"""
    h, w = arr.shape
    nearests = []
    min_diff = np.abs(arr - v).min()
    #print(min_diff)
    for i in range(h):
        for j in range(w):
            if np.abs(arr[i][j] - v) <= min_diff + eps:
                nearests.append((i, j))
    return nearests


def gen_tex_code(board, tries):
    h, w = board.shape
    s = ""
    for i in range(h):
        for j in range(w):
            if board[i][j] == UNKNOWN:
                s += '|[w]|'
            if board[i][j] == MISS:
                s += '|[b]|'
            if board[i][j] == HIT:
                s += '|[r]|'
            if j < w - 1:
                s += '& '
        s += '\\\\\n'
    with open("tex_out.txt",'a') as f:
        f.write(f"{tries}\n")
        f.write(s)
        f.write("-"*50)

def visualize_board(board):
    h, w = board.shape
    for i in range(h):
        for j in range(w):
            if board[i][j] == UNKNOWN:
                print('⬜', end='')
            if board[i][j] == MISS:
                print('🌊', end='')
            if board[i][j] == HIT:
                print('💥', end='')
        print('')
        
    print("-"*50)
    

class Battleship_bot:
    def __init__(self, boards, debug=False, visualize=True) -> None:
        self.boards = boards
        self.debug = debug
        self.visualize = visualize
        self.logs = []
        self.reset()
        if debug:
            print("target board:\n", self.target)
            
    def logger(self, boards_left, hit_prob):
        self.logs.append((boards_left, hit_prob))
    
    def reset(self):
        self.logs = []
        self.valid_boards = deepcopy(self.boards) # initialize new boards space
        self.target = self.random_target_board()
            
    def random_target_board(self):
        """ Generate actual board to play against (random opponent's choice) """
        return random.choice(self.boards)
    
        
    def eliminate(self, cx, cy, hit) -> None:
        """Eliminate boards that mismatch bombing result"""
        def match_hit(board):
            return board[cx][cy] == hit
        
        self.valid_boards = list(filter(match_hit, self.valid_boards))

    def play_game(self, elimination_method):
        vis_board = np.full(self.target.shape, UNKNOWN)
        total_grids_to_hit = np.count_nonzero(self.target == PLACED)
        if self.visualize:
            print(f"{len(self.valid_boards)} possible boards.")
            print("Acutal target board is:")
            visualize_board(self.target)
        
        total_tries, total_hits = 0, 0
        #self.logger(len(self.valid_boards), 0)
        while len(self.valid_boards) > 1 and total_hits < total_grids_to_hit:
            cx, cy = elimination_method(total_tries)
            total_tries += 1
            hit = self.target[cx][cy] # see if bomb hit or not
            vis_board[cx][cy] = hit
            total_hits += hit
            if self.debug:
                print((cx, cy), "Hit!" if hit else "Miss!")
            if self.visualize:
                print("Try # ", total_tries)
                visualize_board(vis_board)
                gen_tex_code(vis_board, total_tries)
                  
            count_before = len(self.valid_boards)
            self.eliminate(cx, cy, hit)
            
            if self.debug:
                print(f"Eliminated {count_before - len(self.valid_boards)} boards. {len(self.valid_boards)} left.")
                
        
                
        hits_to_sink_all = total_grids_to_hit - total_hits
        print(f"Complete! Total tries = {total_tries}. {hits_to_sink_all} more hits required to sink all.")
        
        if self.visualize:
            print("Acutal target board is:")
            visualize_board(self.target)
            
        return total_tries, hits_to_sink_all, self.logs
        
        
class GreedyBot(Battleship_bot):
    
    def greedy_elimination(self, count):
        sum_board = np.array(sum(self.valid_boards))
        valid_count = len(self.valid_boards)
        
        normalized_board = sum_board / valid_count
        nearests = find_nearests(normalized_board, 0.5)
        greedy_choice_x, greedy_choice_y = random.choice(nearests)
        # Find grid w.p. closest to 0.5 to greedily maximize information gain. If multiple exists, randomly choose one.
        
        hit_prob = normalized_board[greedy_choice_x][greedy_choice_y]
        self.logger(len(self.valid_boards), hit_prob)
        if self.debug:
            #print(normalized_board, np.sum(normalized_board))
            sns.heatmap(data=normalized_board, annot=True, cmap="RdBu_r")
            plt.tight_layout()
            plt.savefig(f'fig/{count}.pdf')
            plt.close()
            #plt.show()
            print("Choose: ", greedy_choice_x, greedy_choice_y)
            print("Hit probability: ", hit_prob)
            #print(find_nearests(normalized_board, 0.5))

        return [greedy_choice_x, greedy_choice_y]



if __name__ == "__main__":
    np.set_printoptions(precision=3)
    
    all_boards = SimulationBoard(N=10, M=10, ship_dims=[5, 4, 3], debug=True, randseed=123456).gen_boards()
    Bot = GreedyBot(all_boards, debug=False, visualize=True)
    Bot.play_game(elimination_method=Bot.greedy_elimination)