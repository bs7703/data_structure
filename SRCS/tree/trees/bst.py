from .tree import Tree, Comparator
from typing import TypeVar, Generic, Callable
from .node import Node,FIND_MAX_NODE,FIND_MIN_NODE

T = TypeVar("T")

class BST(Tree[T]):
    def __init__(self, comparator:Comparator[T]):
        super().__init__(comparator)
    def _insert(self, current:Node[T] | None, key:T)->tuple[Node[T]|None, bool]:
        if current is None:
            return Node(data=key), True
        comp = self.compare(current.data, key)
        if comp == 0:
            return current, False
        node, inserted = self._insert(current.next(comp > 0), key)
        current.set_next(node, (comp > 0))
        return current, inserted
    def _delete(self, current:Node[T] | None, key:T)->tuple[Node[T] | None, bool]:
        if current is None:
            return None, False
        comp = self.compare(current.data, key)
        #여기서 연결을끊고 재할당시 가비지컬렉션이 작동해 메모리가사라지는지? 고찰
        if comp == 0:
            if current.right is None:
                return current.left, True
            if current.left is None:
                return current.right, True
            my_node = Node.find_node(current.left, FIND_MAX_NODE)
            current.data = my_node.data
            current.left, _ = self._delete(current.left, my_node.data)
            return current, True
        node, inserted = self._delete(current.next(comp > 0), key)
        current.set_next(node, (comp > 0))
        return current, inserted

