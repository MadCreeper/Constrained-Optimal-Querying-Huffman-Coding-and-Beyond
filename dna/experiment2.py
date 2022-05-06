from dna_gbsc import *
from dna_huffman import *

random.seed(114514)
n = 36
slow = [55, 113]
fast = [3, 12]
slowest = 55
for i in range(300):
    # try:
    prob = random_prob(n)
    if i in slow:
        print(prob)
        with open('slow'+str(i)+'.pickle', 'wb') as f:
            pickle.dump(prob, f)
    if i in fast:
        print(prob)
        with open('fast'+str(i)+'.pickle', 'wb') as f:
            pickle.dump(prob, f)
    t = time.time()
    print(i, greedy_huffman(prob).expected_length, time.time() - t)
    # except Exception as e:
    #     print(e)
