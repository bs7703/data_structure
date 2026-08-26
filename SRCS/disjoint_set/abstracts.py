from .types import T,K,Identity
from typing import Generic
from abc import ABC,abstractmethod
from .protocols import GroupStore

class AbstractDisjointSet(ABC, Generic[T, K]):
    def __init__(self, store: GroupStore[T, K], identity:Identity | None):
        self.store = store
        self.identity = Identity
        if self.identity is None:
            identity = lambda a,b: a==b
    @abstractmethod
    def find(self, x: T) -> K:
        ...
    @abstractmethod
    def union(self, x: T, y: T) -> bool:
        ...