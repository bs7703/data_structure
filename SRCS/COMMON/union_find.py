from typing import Callable, Generic, Protocol, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

Identity = Callable[[T, T], bool]

class DisjointSet(Protocol[T]):
    def find(self, x: T) -> T:
        ...

    def union(self, x: T, y: T) -> bool:
        ...
class AbstractDisjointSet(ABC, Generic[T]):
    @abstractmethod
    def find(self, x: T) -> T:
        ...
    @abstractmethod
    def union(self, x: T, y: T) -> bool:
        ...
class ParentStore(Protocol[T]):
    def initialize(self, x: T) -> None:
        ...
    def get_parent(self, x: T) -> T:
        ...
    def set_parent(self, x: T, parent: T) -> None:
        ...
class RankStore(Protocol[T]):
    def initialize(self, x: T) -> None:
        ...
    def get_rank(self, x: T) -> int:
        ...
    def set_rank(self, x: T, rank: int) -> None:
        ...
class UnionStrategy(Protocol[T]):
    def initialize(self, x: T) -> None:
        ...
    def choose_roots(self, a: T, b: T) -> tuple[T, T]:
        ...
    def merge(self, parent: T, child: T) -> None:
        ...
class NoRank(Generic[T]):
    def initialize(self, x: T) -> None:
        pass
    def choose_roots(self, a: T, b: T) -> tuple[T, T]:
        return a, b
    def merge(self, parent: T, child: T) -> None:
        pass
class UnionByRank(Generic[T]):
    def __init__(self, rank_store: RankStore[T]):
        self._rank = rank_store
    def initialize(self, x: T) -> None:
        self._rank.initialize(x)
    def choose_roots(self, a: T, b: T) -> tuple[T, T]:
        if self._rank.get_rank(a) >= self._rank.get_rank(b):
            return a, b
        return b, a
    def merge(self, parent: T, child: T) -> None:
        parent_rank = self._rank.get_rank(parent)
        child_rank = self._rank.get_rank(child)

        if parent_rank == child_rank:
            self._rank.set_rank(parent, parent_rank + 1)
class UnionFind(AbstractDisjointSet[T]):
    def __init__(
        self,
        parent_store: ParentStore[T],
        union_strategy: UnionStrategy[T] | None = None,
        identity: Identity = lambda a, b: a == b,
    ):
        self._parent = parent_store
        self._strategy = (
            NoRank[T]() if union_strategy is None else union_strategy
        )
        self._identity = identity
    def find(self, x: T) -> T:
        ...
    def union(self, x: T, y: T) -> bool:
        ...