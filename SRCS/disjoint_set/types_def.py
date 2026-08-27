from typing import Callable, TypeVar, TypeAlias
T = TypeVar("T")
K = TypeVar("K")
IdentityOfT: TypeAlias  = Callable[[T, T], bool]
IdentityOfK: TypeAlias  = Callable[[K, K], bool]
SetParentPolicy: TypeAlias = Callable[[T, T], None]
GetGroupPolicy: TypeAlias = Callable[[T], T]
UnionPolicy: TypeAlias = Callable[[T, T], None]