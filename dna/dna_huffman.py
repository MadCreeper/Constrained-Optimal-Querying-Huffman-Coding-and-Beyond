from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Generator, List, Optional, Tuple
import pickle


@dataclass
class TreeNode:
    left: Optional[TreeNode]
    right: Optional[TreeNode]
    question: Optional[List[int]]  # 询问的问题
    prob: float  # 概率之和
    remain: List[int]
    remain_max: int  # 辅助用
    remain_min: int  # 辅助用
    continuous: bool  # 辅助用
    expected_length: float


def by_sum_order(nodes: List[TreeNode]) -> Generator[Tuple[int, int]]:
    n = len(nodes)
    sums = [((i, j), nodes[i].prob + nodes[j].prob)
            for i in range(n) for j in range(i + 1, n)]
    sums.sort(key=lambda x: x[1])
    return (x[0] for x in sums)


def ok(left: TreeNode, right: TreeNode) -> bool:
    a = left.remain_max < right.remain_max and left.remain_max > right.remain_min
    b = left.remain_min < right.remain_max and left.remain_min > right.remain_max
    overlapped = a or b
    return left.continuous or right.continuous or not overlapped


def merge(left: TreeNode, right: TreeNode) -> TreeNode:
    question = [left.remain_min, left.remain_max]
    prob = left.prob + right.prob
    remain = left.remain + right.remain
    remain_max = max(left.remain_max, right.remain_max)
    remain_min = min(left.remain_min, right.remain_min)
    p = left.prob / (left.prob + right.prob)
    excepted_length = p * left.expected_length + (1-p) * right.expected_length + 1
    continuous = left.continuous and right.continuous and (
        left.remain_max == right.remain_min - 1 or left.remain_min == right.remain_max + 1)
    return TreeNode(left=left, right=right, question=question, prob=prob, remain=remain, remain_min=remain_min,
                    remain_max=remain_max, expected_length=excepted_length, continuous=continuous)


def greedy_huffman(prob: List[float]) -> Optional[TreeNode]:
    '''
    贪心法
    '''
    nodes = [TreeNode(left=None, right=None, question=None, prob=v, remain=[i],
                      remain_max=i, remain_min=i, expected_length=0, continuous=True) for i, v in enumerate(prob)]
    return _huffman(nodes)


def _huffman(nodes: List[TreeNode]) -> Optional[TreeNode]:
    if len(nodes) == 1:
        return nodes[0]
    for i, j in by_sum_order(nodes):
        left = nodes[i]
        right = nodes[j]
        if not ok(left, right):
            continue
        new_nodes = [v for k, v in enumerate(nodes) if k not in (i, j)]
        new_nodes.append(merge(left, right))
        x = _huffman(new_nodes)
        if x:
            return x
    return None


class Enumeration:
    '''
    枚举法
    '''

    def __init__(self):
        self.best_expected_length = 99999999
        self.best_tree = None

    def solve(self, prob: List[float]) -> Optional[TreeNode]:
        nodes = [TreeNode(left=None, right=None, question=None, prob=v, remain=[i],
                          remain_max=i, remain_min=i, expected_length=0, continuous=True) for i, v in enumerate(prob)]
        self._huffman(nodes)
        return self.best_tree

    def _huffman(self, nodes: List[TreeNode]):
        if len(nodes) == 1:
            tree = nodes[0]
            if tree.expected_length < self.best_expected_length:
                self.best_expected_length = tree.expected_length
                self.best_tree = tree
        for i, j in self.pairs(nodes):
            left = nodes[i]
            right = nodes[j]
            if not ok(left, right):
                continue
            new_nodes = [v for k, v in enumerate(nodes) if k not in (i, j)]
            new_nodes.append(merge(left, right))
            self._huffman(new_nodes)

    def pairs(self, nodes: List[TreeNode]):
        n = len(nodes)
        for i in range(n):
            for j in range(i+1, n):
                yield (i, j)


def random_prob(n: int) -> List[float]:
    prob = [random.random() for i in range(n)]
    s = sum(prob)
    prob = [i / s for i in prob]
    return prob


def brute_force(prob: List[float]) -> Optional[TreeNode]:
    return Enumeration().solve(prob)


