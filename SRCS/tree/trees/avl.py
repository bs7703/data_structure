from .tree import Tree, Comparator
from .node import *
from .node import AVLNode,Node
from typing import TypeVar, Callable

T = TypeVar("T")
ROTATE_RIGHT=0
ROTATE_LEFT=1


class AVL(Tree[T]):
    def __init__(self, comparator:Comparator[T]):
        super().__init__(comparator)
    def _insert(self, current:AVLNode[T], key:T)->tuple[AVLNode[T], bool]:
        if current is None:
            return AVLNode(key), True
        comp = self.compare(current.data, key)
        if (comp == 0):
            return current, False
        node, res = self._insert(current.next(comp > 0), key)
        current.set_next(node, (comp > 0))
        current = self._rebalance(current)
        return current, res
    def _delete(self, current:AVLNode[T], key:T)->tuple[AVLNode[T], bool]:
        if current is None:
            return None, False
        comp = self.compare(current.data, key)
        if (comp == 0):
            if current.right is None:
                return current.left, True
            if current.left is None:
                return current.right, True
            my_node = Node.find_node(current.left, FIND_MAX_NODE)
            current.data = my_node.data
            node,res = self._delete(current.left, my_node.data)
        else:
            node, res = self._delete(current.next(comp > 0), key)
        current.set_next(node, (comp >= 0))
        current = self._rebalance(current)
        return current, res
    #다음 메인노드가될것을 받아서 재귀적으로 할당.
    def _rotate_mode(self, node:AVLNode[T], mode:int=ROTATE_RIGHT)->AVLNode[T] | None:
        if (mode == ROTATE_RIGHT):
            B = node.left
            node.left = B.right
            B.right = node
        else:
            B = node.right
            node.right = B.left
            B.left = node
        node.h = max(self._get_height(node.left), self._get_height(node.right)) + 1
        B.h = max(self._get_height(B.left), self._get_height(B.right)) + 1
        return B
    def _get_height(self, node:AVLNode[T] | None)->int:
        if node is None:
            return 0
        return node.h
    def _cal_bf(self, node:AVLNode[T])->int:
        return self._get_height(node.left) - self._get_height(node.right)
    def _rebalance(self, node:AVLNode[T])-> AVLNode[T] | None:
        node.h = 1 + max(self._get_height(node.left), self._get_height(node.right))
        bf = self._cal_bf(node)
        left_heavy =  bf > 1 
        right_heavy = bf < -1
        if (left_heavy or right_heavy):
            val1 = node.left if left_heavy else node.right 
            inner_rotation = bf * self._cal_bf(val1) < 0
            if (inner_rotation):
                node.set_next(self._rotate_mode(val1, ROTATE_LEFT if left_heavy else ROTATE_RIGHT), left_heavy)
            return self._rotate_mode(node, ROTATE_RIGHT if left_heavy else ROTATE_LEFT)
        return node