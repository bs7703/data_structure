from typing import Generic, TypeVar, Callable
from abc import ABC, abstractmethod

T = TypeVar("T")
Comparator = Callable[[T, T], int]

class Heap(ABC, Generic[T]):
    def __init__(self, comp:Comparator[T]):
        self._data = []
        self.comp = comp
    def insert(self, value:T):
        self._data.append(value)
        self._sift_up(len(self._data) - 1)
    def _compare(self, a:T, b:T):
        return self.comp(a, b)
    def peek(self) -> T | None:
        return self._data[0] if self._data else None
    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from empty heap")
        result = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return result
    def _parent(self, index:int)->int:
        return (index - 1) // 2
    def _left(self, index: int) -> int | None:
        child = index * 2 + 1
        return child if child < len(self._data) else None
    def _right(self, index: int) -> int | None:
        child = index * 2 + 2
        return child if child < len(self._data) else None
    def _sift_up(self, index:int):
        while (index > 0):
            to_up = self._compare(self._data[index], self._data[self._parent(index)]) < 0
            if not (to_up):
                break
            self._swap(index, self._parent(index))
            index = self._parent(index)
    def _sift_down(self, index:int):
        while (True):
            to_left = self._left(index)
            to_right = self._right(index)
            to_swp = None
            if (to_right is not None and (self._compare(self._data[index], self._data[to_right]) > 0)):
                to_swp = to_right
            if (to_left is not None and (self._compare(self._data[index], self._data[to_left]) > 0)):
                if (to_swp is None or self._compare(self._data[to_left], self._data[to_swp]) < 0):
                    to_swp = to_left
            if to_swp is None:
                break
            self._swap(index, to_swp)
            index = to_swp
    def _swap(self, i:int, j:int):
        a = self._data[i]
        self._data[i] = self._data[j]
        self._data[j] = ad