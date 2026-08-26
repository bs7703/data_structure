from typing import Callable, TypeVar
T = TypeVar("T")
K = TypeVar("K")
Identity = Callable[[K, K], bool]