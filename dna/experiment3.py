from dna_gbsc import *
from dna_huffman import *


random.seed(114514)
times = 100
tme = []
length = []
xAxis = [i for i in range(5, 20)]
for n in xAxis:
    l = 0
    startTime = time.time()
    for _ in range(times):
        x = RandomGener(n)
        # print(x)
        y = [i for i in range(len(x))]
        root = TreeNode(left=None, right=None, question=None, prob=1, remain=y, excepted_length=0)
        root = gbsc(x, root)
        # print(root.excepted_length)
        endTime = time.time()
        l += root.excepted_length
    length.append(l / times)
    tme.append((endTime - startTime)/times)
# print(tme)
with open('data.txt', 'a') as f:
    f.write(' '.join([str(i) for i in tme]))
    f.write('\n')
    f.write(' '.join([str(i) for i in length]))
    f.write('\n')
