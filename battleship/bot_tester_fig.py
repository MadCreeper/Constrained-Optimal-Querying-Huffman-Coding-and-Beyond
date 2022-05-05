from cProfile import label
from greedy_battleship_bot import GreedyBot, visualize_board
from BoardGenerator import SimulationBoard
from matplotlib import pyplot as plt
import numpy as np
import time

def test(Bot, rounds):
    sum_tries, sum_tries_sink = 0, 0
    board_counts_log = []
    tries_log = []
    for rd in range(rounds):
        Bot.reset()
        tries = []
        board_counts = []
        hit_probs = []
        tries, remaining_hits, logs = Bot.play_game(elimination_method=Bot.greedy_elimination)
        sum_tries += tries
        sum_tries_sink += tries + remaining_hits
        
        #print(logs)
        tries = len(logs)
        for num_boards, hit_prob in logs:
            board_counts.append(num_boards)
            hit_probs.append(hit_prob)
        
        max_board_cnt = board_counts[0]
        board_counts_log.append(board_counts)
        tries_log.append(list(range(tries)))
        
        
        print("round: ", rd, "time: ", time.time() - st, )
    
    
    num_tries = []
    for idx in range(rounds):
        plt.plot(tries_log[idx], np.log2(board_counts_log[idx]), label=f'Board {idx+1}')
        num_tries.append(len(board_counts_log[idx]))
        #print(board_counts_log[idx])
    
    B = np.log2(max_board_cnt)
    x = np.arange(0, 21, 0.1)
    y = B - x
    plt.plot(x, y, 'r--', label='theoretical best',  linewidth=3 )
    # print(num_tries)
    # plt.xlabel("Number of queries (t)")
    # plt.ylabel("Frequency")
    # plt.hist(num_tries, density=True)
    # plt.show()
    
    plt.xlabel("Number of queries (t)")
    plt.ylabel("Entropy (bits)")
    plt.legend()
    plt.show()

      
    return sum_tries / rounds, sum_tries_sink / rounds
  
def main():
    all_boards = SimulationBoard(N=10, M=10, ship_dims=[5, 4, 3], debug=True, randseed=114514).gen_boards()
    Bot = GreedyBot(all_boards, debug=False, visualize=False)
    
    rounds = 10
    avg_tries, avg_tries_to_sink = test(Bot, rounds)
    
    print(f"{rounds} rounds avg: {avg_tries} tries to determine board, {avg_tries_to_sink} to sink all ships")

if __name__ == "__main__":
    st = time.time()
    main()
    print(f"ALL done, took {time.time() - st} secs")