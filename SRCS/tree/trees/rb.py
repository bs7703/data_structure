from .tree import Tree, Comparator
from .node import *
from .node import RBNode
from typing import TypeVar

T = TypeVar("T")

ROTATE_RIGHT=0
ROTATE_LEFT=1
PARENT_LEFT = 0x10
CHILD_LEFT = 0x01

__all__ = [
    "ROTATE_RIGHT",
    "ROTATE_LEFT",
    "PARENT_LEFT",
    "CHILD_LEFT"
]
class RB(Tree[T]):
    def __init__(self, comparator:Comparator[T]):
        super().__init__(comparator)
    def insert(self, key:T) -> bool:
        node, inserted = self._insert(self.root, key)
        if node is not None and node.parent is None:
            self.root = node
            self.root.color = BLACK
        if inserted:
            self._size += 1
        return inserted
    def _insert(self, current:RBNode[T], key:T)->tuple[RBNode[T], bool]:
        tmp = current
        if tmp is None:
            return RBNode(key), True
        while True:
            comp = self.compare(tmp.data, key)
            if comp == 0:
                return None, False
            if tmp.next(comp > 0) is None:
                RBNode.set_child(tmp, RBNode(key), comp > 0)
                tmp = tmp.next(comp > 0)
                break
            else:
                tmp = tmp.next(comp > 0)
        while tmp is not None:
            parent = tmp.parent
            if parent is None:
                break
            DOUBLE_RED = (tmp.color + parent.color) == RED
            if not DOUBLE_RED:
                break
            tmp = self._remodel(parent, tmp)
        return tmp, True
    #1개만남아서 삭제시 root를 None으로만드는것과, None을받았을떄도 정상적으로 기능하도록처리
    def delete(self, key: T) -> bool:
        node, deleted = self._delete(self.root, key)
        #1개인케이스
        if deleted:
            self._size -= 1
            if (node is None) or (self._size == 0):
                self.root = None
        #node를 거슬러 조상을비교후 재할당
            else:
                while (node.parent):
                    node = node.parent
                if (node is not self.root):
                    self.root = node
                    node.color = BLACK
        return deleted
    def _delete(self, current:RBNode[T], key:T)->tuple[RBNode[T], bool]:
            tmp = current
            if tmp is None:
                return None, False
            while True:
                comp = self.compare(tmp.data, key)
                if comp == 0:
                    if tmp.is_full():
                        res = RBNode.find_node(tmp.left, FIND_MAX_NODE)
                        tmp.data = res.data
                        tmp = res
                    break
                if tmp.next(comp > 0) is None:
                    return None, False
                else:
                    tmp = tmp.next(comp > 0)
            if (tmp.color == RED):
                RBNode.detach_parent(tmp)
                return current, True
            if not (tmp.is_leaf()):
                is_left = tmp.is_left_child()
                c = tmp.next(True) or tmp.next(False)
                c.color = BLACK
                p = RBNode.detach_parent(tmp)
                tmp.left = None
                tmp.right = None
                if is_left is not None:
                    RBNode.set_child(p, c, is_left)
                else:
                    c.parent = None
                return c, True
            #더블블랙 재귀의 시작인 경우에만.
            slf = tmp
            tmp = self._delete_fix_up(tmp)
            RBNode.detach_parent(slf)
            return tmp, True

    def _delete_fix_up(self, node:RBNode[T]|None)->RBNode[T] | None:
        is_left = node.is_left_child()
        if is_left is None:
            return node
        parent = node.parent
        brother = parent.right if is_left else parent.left
        #형제가 블랙인경우
        if (not (brother.color == BLACK)):
            parent.color = RED
            brother.color = BLACK
            self._rotate_mode(parent, ROTATE_LEFT if is_left else ROTATE_RIGHT)
            return self._delete_fix_up(node)
        #형제가 레드인경우
        else:
            brother_state = node.brother_state()
            if (brother_state is BROTHER_FULL_BLACK):
                brother.color = RED
                if (parent.color is RED):
                    parent.color = BLACK
                    return parent
                return self._delete_fix_up(parent)
            if (brother_state is BROTHER_INNER_RED or brother_state is BROTHER_OUTER_RED):
                fil = (PARENT_LEFT if not is_left else 0) | (CHILD_LEFT if (not is_left) ^ (brother_state == BROTHER_INNER_RED) else 0)
                new_root = self._rebalance(parent, fil)
                new_root.color = parent.color
                parent.color = BLACK
                far_child = new_root.right if parent.is_left_child() else new_root.left
                far_child.color = BLACK
                return new_root
    def _remodel(self, p:RBNode[T] | None, c:RBNode[T] | None)->RBNode[T]:
        g = p.parent
        u = g.left if (g.right == p) else g.right
        if u is not None and u.color == RED:
            u.color = BLACK
            p.color = BLACK
            g.color = RED
            res = g
        else:
            fil = ((PARENT_LEFT if p.is_left_child() else 0) | (CHILD_LEFT if c.is_left_child() else 0))
            res = self._rebalance(g, fil)
            res.color = BLACK
            (res.right if fil & PARENT_LEFT else res.left).color = RED
        return res
    def _rotate_mode(self, node:RBNode[T], mode:int=ROTATE_RIGHT)->RBNode[T] | None:
        tmp = node.parent
        is_left = tmp is not None and tmp.left is node
        if (mode == ROTATE_RIGHT):
            B = node.left
            RBNode.set_child(node, B.right, True)
            RBNode.set_child(B, node, False)
        else:
            B = node.right
            RBNode.set_child(node, B.left, False)
            RBNode.set_child(B, node, True)
        if tmp is not None:
            RBNode.set_child(tmp, B, is_left)
        else:
            B.parent = None
        return B
    def _rebalance(self, node: RBNode[T], filter: int) -> RBNode[T] | None:
        get_parent_left = bool(filter & PARENT_LEFT)
        child_left = bool(filter & CHILD_LEFT)
        inner = get_parent_left != child_left
        if inner:
            mode = ROTATE_LEFT if get_parent_left else ROTATE_RIGHT
            child = node.left if get_parent_left else node.right
            self._rotate_mode(child, mode)
        mode = ROTATE_RIGHT if get_parent_left else ROTATE_LEFT
        node = self._rotate_mode(node, mode)
        return node
