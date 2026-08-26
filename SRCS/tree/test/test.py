# test.py
# 네가 작성한 AVL 구현을 기준으로 만든 콘솔 테스트 파일
#
# 사용법:
#   1. 이 파일을 avl.py와 같은 패키지 위치에 넣거나
#   2. 아래 import 경로를 네 프로젝트 구조에 맞게 수정
#
# 현재 네 코드의 공개 API가 insert/delete/search라고 가정한다.

from random import Random

# 예: from .avl import avl
# 패키지 밖에서 직접 실행한다면: from avl import avl
from trees.avl import AVL as avl


def comparator(a, b):
    return (a > b) - (a < b)


# ------------------------------------------------------------
# 출력
# ------------------------------------------------------------

def print_tree(node, prefix="", is_left=True):
    if node is None:
        return

    if node.right is not None:
        print_tree(
            node.right,
            prefix + ("│   " if is_left else "    "),
            False
        )

    print(
        prefix
        + ("└── " if is_left else "┌── ")
        + f"{node.data} [h={node.h}, bf={bf(node)}]"
    )

    if node.left is not None:
        print_tree(
            node.left,
            prefix + ("    " if is_left else "│   "),
            True
        )


def height(node):
    if node is None:
        return 0
    return node.h


def bf(node):
    if node is None:
        return 0

    return height(node.left) - height(node.right)


# ------------------------------------------------------------
# 구조 검증
# ------------------------------------------------------------

def check_bst(node, low=None, high=None):
    if node is None:
        return True

    if low is not None and node.data <= low:
        return False

    if high is not None and node.data >= high:
        return False

    return (
        check_bst(node.left, low, node.data)
        and check_bst(node.right, node.data, high)
    )


def check_avl(node):
    """
    반환:
        (정상 여부, 실제 height)

    검사:
        - 저장된 height
        - BF
        - AVL balance
    """

    if node is None:
        return True, 0

    left_ok, left_height = check_avl(node.left)
    right_ok, right_height = check_avl(node.right)

    actual_height = 1 + max(
        left_height,
        right_height
    )

    actual_bf = left_height - right_height

    height_ok = node.h == actual_height
    balance_ok = abs(actual_bf) <= 1

    ok = (
        left_ok
        and right_ok
        and height_ok
        and balance_ok
    )

    if not height_ok:
        print(
            f"  HEIGHT ERROR: node={node.data}, "
            f"stored={node.h}, expected={actual_height}"
        )

    if not balance_ok:
        print(
            f"  BF ERROR: node={node.data}, "
            f"bf={actual_bf}"
        )

    return ok, actual_height


def validate(tree):
    bst_ok = check_bst(tree.root)
    avl_ok, _ = check_avl(tree.root)

    if not bst_ok:
        print("  BST ORDER ERROR")

    return bst_ok and avl_ok


# ------------------------------------------------------------
# 기본 회전 테스트
# ------------------------------------------------------------

def rotation_test(name, values):
    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    tree = avl(comparator)

    for value in values:
        result = tree.insert(value)

        print(f"\ninsert({value}) -> {result}")
        print_tree(tree.root)

        if not validate(tree):
            print(">>> FAIL")
            return False

    print(">>> PASS")
    return True


# ------------------------------------------------------------
# 기본 insert/search/delete 테스트
# ------------------------------------------------------------

def basic_test():
    print()
    print("=" * 60)
    print("BASIC INSERT / SEARCH / DELETE")
    print("=" * 60)

    tree = avl(comparator)

    values = [50, 30, 70, 20, 40, 60, 80]

    print("\n[INSERT]")

    for value in values:
        result = tree.insert(value)
        print(f"insert({value}) -> {result}")

        if not validate(tree):
            print(">>> FAIL")
            return False

    print_tree(tree.root)

    print("\n[SEARCH]")

    for value in values:
        result = tree.search(value)
        print(f"search({value}) -> {result}")

        if result is not True:
            print(">>> FAIL")
            return False

    for value in [999, -1, 55]:
        result = tree.search(value)
        print(f"search({value}) -> {result}")

        if result is not False:
            print(">>> FAIL")
            return False

    print("\n[DUPLICATE]")

    result = tree.insert(50)
    print(f"insert(50) -> {result}")

    if result is not False:
        print(">>> FAIL")
        return False

    print("\n[DELETE]")

    for value in [20, 30, 70, 50]:
        result = tree.delete(value)

        print(f"\ndelete({value}) -> {result}")
        print_tree(tree.root)

        if result is not True:
            print(">>> FAIL")
            return False

        if not validate(tree):
            print(">>> FAIL")
            return False

    print(">>> PASS")
    return True


# ------------------------------------------------------------
# 랜덤 테스트
# ------------------------------------------------------------

def random_test(seed=42, n=100):
    print()
    print("=" * 60)
    print(f"RANDOM TEST seed={seed}, n={n}")
    print("=" * 60)

    rng = Random(seed)

    values = list(range(1, n + 1))
    insert_order = values[:]
    rng.shuffle(insert_order)

    tree = avl(comparator)
    reference = set()

    print("\n[INSERT]")

    for i, value in enumerate(insert_order, 1):
        result = tree.insert(value)

        if result is not True:
            print(f"FAIL: insert({value}) returned {result}")
            return False

        reference.add(value)

        if not validate(tree):
            print(f"FAIL: AVL invalid after insert({value})")
            print_tree(tree.root)
            return False

        if i % 10 == 0:
            print(f"  {i}/{n} inserted -> PASS")

    print("\n[SEARCH]")

    for value in range(1, n + 1):
        actual = tree.search(value)
        expected = value in reference

        if actual != expected:
            print(
                f"FAIL: search({value}) "
                f"actual={actual}, expected={expected}"
            )
            return False

    print("  all searches -> PASS")

    print("\n[DELETE]")

    delete_order = values[:]
    rng.shuffle(delete_order)

    for i, value in enumerate(delete_order, 1):
        result = tree.delete(value)

        if result is not True:
            print(f"FAIL: delete({value}) returned {result}")
            return False

        reference.remove(value)

        if not validate(tree):
            print(f"FAIL: AVL invalid after delete({value})")
            print_tree(tree.root)
            return False

        for check_value in values:
            actual = tree.search(check_value)
            expected = check_value in reference

            if actual != expected:
                print(
                    f"FAIL: after delete({value}), "
                    f"search({check_value}) = {actual}, "
                    f"expected={expected}"
                )
                return False

        if i % 10 == 0:
            print(f"  {i}/{n} deleted -> PASS")

    if tree.root is not None:
        print("FAIL: tree root is not None")
        return False

    print("\n>>> RANDOM TEST PASS")
    return True


# ------------------------------------------------------------
# 빈 트리 / root 삭제 테스트
# ------------------------------------------------------------

def edge_test():
    print()
    print("=" * 60)
    print("EDGE CASE TEST")
    print("=" * 60)

    tree = avl(comparator)

    print("\n빈 트리 삭제:")
    result = tree.delete(10)
    print(f"delete(10) -> {result}")

    if result is not False:
        print("FAIL")
        return False

    print("\n하나만 삽입:")
    result = tree.insert(10)
    print(f"insert(10) -> {result}")
    print_tree(tree.root)

    if not validate(tree):
        print("FAIL")
        return False

    print("\nroot 삭제:")
    result = tree.delete(10)
    print(f"delete(10) -> {result}")

    if result is not True:
        print("FAIL")
        return False

    if tree.root is not None:
        print("FAIL: root should be None")
        return False

    print("\n중복 삭제:")
    result = tree.delete(10)
    print(f"delete(10) -> {result}")

    if result is not False:
        print("FAIL")
        return False

    print(">>> PASS")
    return True


# ------------------------------------------------------------
# 실행
# ------------------------------------------------------------

def main():
    total = 0
    passed = 0

    tests = [
        ("LL ROTATION", [30, 20, 10]),
        ("RR ROTATION", [10, 20, 30]),
        ("LR ROTATION", [30, 10, 20]),
        ("RL ROTATION", [10, 30, 20]),
    ]

    for name, values in tests:
        total += 1
        if rotation_test(name, values):
            passed += 1

    total += 1
    if basic_test():
        passed += 1

    total += 1
    if edge_test():
        passed += 1

    total += 1
    if random_test():
        passed += 1

    print()
    print("=" * 60)
    print(f"RESULT: {passed}/{total} TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()