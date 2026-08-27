from .types_def import T,K,IdentityOfT, IdentityOfK,UnionPolicy
from .abstracts import AbstractGroupStore, AbstractParentStore
from functools import partial
from .policies import list_parent_union_util, list_parent_find_util,list_parent_set_parent_util, FindPolicy, UnionPolicy as UP

### implemented_storages

##-- 1.Groupstore - not -parent -based

#고찰1. 임의사이즈병합, 리스트에서 큰사이즈 작은사이즈를 구분해서 다시 병합작업을하는것은 비용이크다
#따라서 merge시 그륩id가 a,b인것의 크기를구분하지않고 병합시도
#즉 전체리스트순회후 a인것을 강제로b로변환

#고찰2. 초기에 데이터가 생성되거나 추가되는경우 불변조건의책임이 외부에있으나,
#데이터추가가 명시되는경우 불변조건을 검사하는것이 필요하다.

#기본적으로 현재list_based_store는 인자를 왼쪽의 그륩id를 오른쪽의 그륩id로 고정시키는 정책이다
class listbasedstore(AbstractGroupStore[T,K]):
    def __init__(self, store:list[tuple[T,K]], identityoft:IdentityOfT|None = None, identityofk:IdentityOfK|None = None):
        super().__init__(store, identityoft, identityofk)
    def get_group(self, x: T) -> K:
        for value, group_id in self.store:
            if (self.identityoft(value, T)):
                return group_id
        raise KeyError(x)
    def merge_group(self, a: K, b: K) -> None:
        for i, (value, group_id) in enumerate(self.store):
            if self.identityofk(group_id, a):
                self.store[i] = (value, b)

##-- 2.ParentStore
class listbasedparentstore(AbstractParentStore[T]):
    def __init__(self, storage: list[tuple[T, T]], meta: list[int] | None = None, union_policy: UnionPolicy = UP.DEFAULT,identity_of_t: IdentityOfT | None = None, find_policy: FindPolicy = FindPolicy.PATH_COMPRESSION):
        identity = identity_of_t or (lambda a, b: a == b)
        if union_policy is not UP.DEFAULT and meta is None:
            raise ValueError("meta is required for RANK or SIZE")
        self.meta = meta
        get_group_policy = partial(list_parent_find_util, identity=identity, storage=storage, flag=find_policy)
        set_parent_policy = partial(list_parent_set_parent_util, identity=identity, storage=storage)
        union_policy_func = partial(list_parent_union_util, identity=identity, meta=meta, storage=storage, flag=union_policy)
        super().__init__(storage, get_group_policy, union_policy_func, set_parent_policy, identity)