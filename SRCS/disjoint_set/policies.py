from .types_def import T, K
from enum import Enum
#union policies by data-types
#flag makes control flow to 1. NO_RANK 2. RANKED 3.SIZED

class FindPolicy(Enum):
    DEFAULT = 1
    PATH_COMPRESSION = 2
class UnionPolicy(Enum):
    DEFAULT=1
    RANK=2
    SIZE=3

def list_parent_get_index_util(identity, storage:list[tuple[T, T]], x:T) -> int:
    for idx, data in enumerate(storage):
        if identity(data[0], x):
            return idx
    raise KeyError(x)
def list_parent_set_parent_util(identity, storage:list[tuple[T,T]], x:T, parent:T) -> None:
    idx = list_parent_get_index_util(identity, storage, x)
    storage[idx] = (storage[idx][0], parent)
#union policies by data-types
def list_parent_union_util(identity, meta:list[int], storage:list[tuple[T,T]], a:T, b:T, flag)->None:
    idx_a = list_parent_get_index_util(identity, storage, a)
    idx_b = list_parent_get_index_util(identity, storage, b)
    if flag in (UnionPolicy.SIZE, UnionPolicy.RANK):
        if meta[idx_a] < meta[idx_b]:
            idx_a, idx_b = idx_b, idx_a
        storage[idx_b] = (storage[idx_b][0], storage[idx_a][0])
        if flag is UnionPolicy.SIZE:
            meta[idx_a] = meta[idx_a] + meta[idx_b]
        elif meta[idx_a] == meta[idx_b]:
            meta[idx_a] = meta[idx_a] + 1
        meta.pop(idx_b)
    else:
        storage[idx_b] = (storage[idx_b][0], storage[idx_a][0])
#find policies by data-types
def list_parent_find_util(identity, storage:list[tuple[T,T]], a:T, flag)->T:
    idx = list_parent_get_index_util(identity, storage, a)
    value, parent = storage[idx]
    if identity(value, parent):
        return value
    root = list_parent_find_util(identity, storage, parent, flag)
    if flag is FindPolicy.PATH_COMPRESSION:
        storage[idx] = (value, root)
    return root