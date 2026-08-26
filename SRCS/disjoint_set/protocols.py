from .types import T,K,Identity
from typing import Protocol

#abstract_class_protocols
class DisjointSet(Protocol[T, K]):
    def find(self, x: T) -> K:
        ...
    def union(self, x: T, y: T) -> bool:
        ...

#store_type_protocols
class GroupStore(Protocol[T, K]):
    def get_group(self, x: T) -> K:
        ...
    def merge_group(self, a: K, b: K) -> None:
        ...
class ParentStore(Protocol[T]):
    def initialize(self, x: T) -> None:
        ...
    def get_parent(self, x: T) -> T:
        ...
    def set_parent(self, x: T, parent: T) -> None:
        ...
    def merge(self, parent: T, child: T) -> None:
        parent_rank = self._rank.get_rank(parent)
        child_rank = self._rank.get_rank(child)
        if parent_rank == child_rank:
            self._rank.set_rank(parent, parent_rank + 1)