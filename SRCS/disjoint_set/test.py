from .storages import listbasedstore,listbasedparentstore
from .union_find import UnionFind
from .policies import UnionPolicy

"""
test_data = [
    # Group 0
    ("A", 0),
    ("B", 0),
    ("C", 0),

    # Group 1
    ("D", 1),
    ("E", 1),
    ("F", 1),
    ("G", 1),
    ("H", 1),

    # Group 2
    ("I", 2),
    ("J", 2),

    # Group 3
    ("K", 3),
    ("L", 3),
    ("M", 3),
    ("N", 3),

    # Group 4
    ("O", 4),

    # Group 5
    ("P", 5),
    ("Q", 5),
    ("R", 5),
    ("S", 5),
    ("T", 5),
]
my_list = listbasedstore(test_data)
my_u = UnionFind(my_list)
my_u.union("A", "D")
my_u.union("I", "A")
my_u.union("K", "A")
my_u.union("P", "A")
my_u.union("A", "O")
print(test_data)
"""

test_data2 = [
    ("A", "A"),
    ("B", "A"),
    ("C", "B"),
    ("D", "C"),

    ("E", "E"),
    ("F", "E"),
    ("G", "F"),

    ("H", "H"),
    ("I", "H"),

    ("J", "J"),
    ("K", "J"),

    ("L", "L"),
    ("M", "L"),
    ("N", "M"),

    ("O", "O"),
    ("P", "O"),
]

# Rank를 사용하는 경우
meta = [3, 2, 2, 1, 3, 2, 1]

my_parent = listbasedparentstore(
    storage=test_data2,
    union_policy=UnionPolicy.RANK,
    meta=meta,
)

my_u = UnionFind(my_parent)
print("=== 초기 상태 ===")
print(test_data2)

print("\n=== 초기 group 확인 ===")
for x in ["A", "D", "G", "I", "K", "N", "P"]:
    print(f"{x} -> {my_parent.get_group(x)}")


print("\n=== Union ===")

my_u.union("D", "G")
print("union(D, G)")
print(test_data2)

my_u.union("I", "K")
print("union(I, K)")
print(test_data2)

my_u.union("N", "P")
print("union(N, P)")
print(test_data2)

my_u.union("A", "I")
print("union(A, I)")
print(test_data2)


print("\n=== 최종 group ===")

for x in ["A", "B", "C", "D", "E", "F", "G",
          "H", "I", "J", "K", "L", "M", "N", "O", "P"]:
    print(f"{x} -> {my_parent.get_group(x)}")


print("\n=== Path Compression 확인 ===")

print("D의 group:", my_parent.get_group("D"))
print("D의 group 이후 storage:")
print(test_data2)

print("C의 group:", my_parent.get_group("C"))
print("C의 group 이후 storage:")
print(test_data2)