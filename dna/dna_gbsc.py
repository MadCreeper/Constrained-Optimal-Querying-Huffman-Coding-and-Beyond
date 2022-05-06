from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TreeNode:
    left: Optional[TreeNode]
    right: Optional[TreeNode]
    question: Optional[List[int]]  # 询问的问题
    prob: float  # 概率之和
    remain: List[int]
    excepted_length: float


def gbsc(x: List, node: TreeNode) -> TreeNode:
    # print(node.remain)
    if (le := len(node.remain)) == 1:
        return node
    tempn = [x[i] for i in node.remain]
    t = sum(tempn)
    tempn = [i/t for i in tempn]  # 归一化
    # print(tempn)
    r1, l1, r2, l2, su, temp, pr = 0, 0, 0, 0, 0, 1, 0
    while r1 < le:
        # 寻找概率和最接近0.5的一段
        while su < 0.5 and r1 < le:
            su += tempn[r1]
            r1 += 1
        t1, t2 = abs(su-0.5), abs(su-tempn[r1-1]-0.5)
        if t1 < t2 and t1 < temp:
            #print(t1, temp, l1, r1,'s')
            temp = t1
            l2, r2 = l1, r1
            pr = su
        elif t2 < temp:
            #print(t2, temp, l1, r1,'t')
            temp = t2
            l2, r2 = l1, r1-1
            pr = su - tempn[r1-1]
        su -= tempn[l1]
        l1 += 1
    # 查询节点为l2到r2之间的一段，包括l2，不包括r2
    node.question = [l2, r2]
    # 左子树是中间一段
    node.left = gbsc(x, TreeNode(left=None, right=None, question=None,
                     prob=pr, remain=node.remain[l2:r2], excepted_length=0))
    # 右子树为两端
    node.right = gbsc(x, TreeNode(left=None, right=None, question=None, prob=1-pr,
                      remain=node.remain[:l2]+node.remain[r2:], excepted_length=0))

    # 计算以节点为根的树的期望长度
    if node.left:
        node.excepted_length += (node.left.excepted_length + 1) * node.left.prob
    if node.right:
        node.excepted_length += (node.right.excepted_length + 1) * node.right.prob
    return node


def RandomGener(n: int):
    return [random.random() for i in range(n)]


if __name__ == '__main__':
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
    # plt.plot(xAxis, tme, 'ro-', label='Binery')
    # plt.title('The average time cost for different numbers of exons')
    # plt.xlabel("The number of exons")
    # plt.ylabel('The time cost')
    # plt.legend(loc='best')
    # plt.savefig('./binary.pdf')
    # plt.show()
    # print(cal(y))
    # print(f'The total time cost is {times}')
