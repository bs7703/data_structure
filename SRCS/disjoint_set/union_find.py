from typing import Callable, Generic, Protocol, TypeVar
from .types import T,K,Identity
from .abstracts import AbstractDisjointSet
from protocols import GroupStore
from abc import ABC, abstractmethod


#핵심아이디어 유니온셋은 최초로 원소,컨테이너 그리고 원소를담은 하위컨테이너와 그것의 그륩id가 필요할것이다.
#이떄 그륩아이디어를비교해 같은아이디면 합치지않고
class UnionFind(AbstractDisjointSet[T,K]):
    def find(self, x: T) -> K:
        return self.store.get_group(x)
    def union(self, x: T, y: T) -> bool:
        gx = self.find(x)
        gy = self.find(y)
        if gx == gy:
            return False
        self.store.merge_group(gx, gy)
        return True 