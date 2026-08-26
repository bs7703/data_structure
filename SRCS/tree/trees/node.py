from __future__ import annotations
from typing import Generic, TypeVar

T = TypeVar("T")

RED = 0
BLACK = 1
FIND_MIN_NODE = 0
FIND_MAX_NODE = 1
BROTHER_FULL_BLACK = 0
BROTHER_INNER_RED = 1
BROTHER_OUTER_RED = 2

__all__ =[
"RED",
"BLACK",
"FIND_MIN_NODE",
"FIND_MAX_NODE",
"BROTHER_FULL_BLACK",
"BROTHER_INNER_RED",
"BROTHER_OUTER_RED",
]
class Node(Generic[T]):
    def __init__(self, data:T,left:Node[T] | None=None, right:Node[T] | None=None, parent:Node[T] | None=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent =parent
    def is_leaf(self)->bool:
        return True if self.left is None and self.right is None else False
    def is_full(self)->bool:
        return True if self.left is not None and self.right is not None else False
    def next(self, is_left)->Node[T]:
        return self.left if is_left else self.right
    def set_next(self, node:Node[T], is_left):
        if is_left:
            self.left = node
        else:
            self.right = node
    #FIND_MIN_NODE = 최소 FIND_MAX_NODE= 최대
    def brother_state(self) -> int:
        is_left = self.is_left_child()
        if is_left is None:
            return BROTHER_FULL_BLACK
        parent = self.parent
        brother = parent.right if is_left else parent.left
        if brother is None:
            return BROTHER_FULL_BLACK
        inner = brother.left if is_left else brother.right
        outer = brother.right if is_left else brother.left
        if outer is not None and outer.color == RED:
            return BROTHER_OUTER_RED
        if inner is not None and inner.color == RED:
            return BROTHER_INNER_RED
        return BROTHER_FULL_BLACK
    def is_left_child(self) -> bool | None:
        if self.parent is None:
            return None
        return self.parent.left is self
    @staticmethod
    def find_node(current:Node[T] | None, mode:int = FIND_MAX_NODE)->Node[T]:
        if (mode == FIND_MIN_NODE):
            if (current.left is None):
                return current
        elif (current.right is None):
                return current
        return Node.find_node(current.left, mode) if mode == FIND_MIN_NODE else Node.find_node(current.right, mode)
    @staticmethod
    def set_child(parent:RBNode[T], child:RBNode[T], is_left:bool):
        if is_left:
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent
    @staticmethod
    def detach_parent(child:RBNode[T])->RBNode[T] | None:
        is_left = child.is_left_child()
        if is_left is None:
            return None
        p = child.parent
        if is_left:
            p.left = None
        else:
            p.right = None
        child.parent = None
        return p
class AVLNode(Node[T]):
    def __init__(self, data:T, left:AVLNode[T] | None=None, right:AVLNode[T] | None=None, h:int = 1):
        super().__init__(data, left, right)
        self.h = h

class RBNode(Node[T]):
    def __init__(self, data:T, left:RBNode[T] | None = None, right:RBNode[T] | None = None, parent:RBNode[T] | None = None, color:int = RED):
        super().__init__(data, left, right, parent)
        self.color = color
