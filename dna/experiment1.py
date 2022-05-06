from dna_huffman import *

random.seed(114514)

result = []
for i in range(10000):
    prob = random_prob(6)
    a = brute_force(prob)
    b = greedy_huffman(prob)
    result.append((a.expected_length, b.expected_length))


with open('experiment1.pickle', 'wb') as f:
    pickle.dump(result, f)
