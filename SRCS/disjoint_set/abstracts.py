from .types_def import T,K,IdentityOfK, IdentityOfT,GetGroupPolicy,UnionPolicy,SetParentPolicy
from typing import Generic
from abc import ABC,abstractmethod
from .protocols import GroupStore

# Union-Find Invariants

# 1. Union-Find의 연산 대상은 Storage에 등록된 원소로 제한한다. (기본전제)
# 2. Find 및 Union에 전달되는 원소는 반드시 Storage에 존재한다고 가정한다. (1에따른 당연한귀결)
#    따라서 Storage 조회 결과가 존재하지 않는 경우는 정상적인 연산 범위에 포함하지 않는다. 
# 3. Store가 비어 있는 경우 등록된 원소가 존재하지 않으므로(1에따른 당연한귀결)
#    유효한 Find 및 Union 연산의 대상이 존재하지 않는다.
class AbstractDisjointSet(ABC, Generic[T, K]):
    def __init__(self, store: GroupStore[T, K]):
        self.store = store
    @abstractmethod
    def find(self, x: T) -> K:
        ...
    @abstractmethod
    def union(self, x: T, y: T) -> bool:
        ...
class AbstractGroupStore(ABC,Generic[T, K]):
    def __init__(self, store:GroupStore[T, K], identityoft:IdentityOfT|None = None, identityofk:IdentityOfK|None = None):
        self.store = store
        self.identityoft = identityoft
        self.identityofk = identityofk
        if self.identityoft is None:
            self.identityoft = lambda a,b: a==b
        if self.identityofk is None:
            self.identityofk = lambda a,b: a==b
    @abstractmethod
    def get_group(self, x: T) -> K:
        ...
    @abstractmethod
    def merge_group(self, a: K, b: K) -> None:
        ...
# P-Store같은경우 추상화계층의 최상단에서 각함수 즉 get_group(=get_parent)와 merge_group(상위단게의 union)
# 을 최적화 할지,말지의 선택들이 가능하고, 이것을 외부함수로 주입하는방법으로 추상화단계에서는
# 실제 구현을 알 필요는없지만, 가능한 조합들을 만들고
# 가능한 정책들의 제한과 구현의공통을뽑아 재사용하기쉽게 만들어둔다.

class AbstractParentStore(Generic[T]):
    def __init__(self, storage, get_group_policy: GetGroupPolicy[T], union_policy: UnionPolicy[T], set_parent_policy: SetParentPolicy[T], identity_of_t: IdentityOfT | None = None):
        self.storage = storage
        self.get_group_policy = get_group_policy
        self.union_policy = union_policy
        self.set_parent_policy = set_parent_policy
        self.identity = identity_of_t or (lambda a, b: a == b)
    def set_parent(self, x: T, parent: T) -> None:
        self.set_parent_policy(x, parent)
    def get_group(self, x: T) -> T:
        return self.get_group_policy(x)
    def merge_group(self, a: T, b: T) -> None:
        self.union_policy(a, b)