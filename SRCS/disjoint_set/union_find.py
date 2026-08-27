from .types_def import T,K
from .abstracts import AbstractDisjointSet

class UnionFind(AbstractDisjointSet[T, K]):
    def find(self, x: T) -> K:
        return self.store.get_group(x)
    def union(self, x: T, y: T) -> bool:
        gx = self.find(x)
        gy = self.find(y)
        if self.store.identityofk(gx, gy):
            return False
        self.store.merge_group(gx, gy)
        return True