import random
import pytest

# 실제 프로젝트 구조에 맞게 수정
from trees.rb import RB
from trees.node import RED, BLACK


def int_compare(a: int, b: int) -> int:
    return (a > b) - (a < b)


def validate_rb_tree(tree: RB):
    """RB-tree의 BST 및 Red-Black 불변조건을 검증한다."""
    root = tree.root

    if root is None:
        return

    # Root는 반드시 BLACK
    assert root.color == BLACK

    def check(node, lower=None, upper=None):
        if node is None:
            return 1

        # BST ordering
        if lower is not None:
            assert node.data > lower

        if upper is not None:
            assert node.data < upper

        # RED 노드의 자식은 BLACK
        if node.color == RED:
            if node.left is not None:
                assert node.left.color == BLACK
            if node.right is not None:
                assert node.right.color == BLACK

        left_black_height = check(node.left, lower, node.data)
        right_black_height = check(node.right, node.data, upper)

        # 모든 경로의 black-height가 동일해야 함
        assert left_black_height == right_black_height

        return left_black_height + (1 if node.color == BLACK else 0)

    check(root)


@pytest.fixture
def tree():
    return RB(int_compare)


def test_insert(tree):
    values = [10, 20, 30, 15, 5, 1, 7, 25, 40, 50]

    for value in values:
        assert tree.insert(value)
        validate_rb_tree(tree)

    # 중복 삽입은 실패
    for value in values:
        assert not tree.insert(value)

    validate_rb_tree(tree)


def test_search(tree):
    values = [10, 20, 30, 15, 5, 1, 7, 25, 40]

    for value in values:
        assert tree.insert(value)

    for value in values:
        node = tree.search(value)
        assert node is not None
        assert node.data == value

    # 존재하지 않는 값
    assert tree.search(999) is None
    assert tree.search(-999) is None

    validate_rb_tree(tree)


def test_delete(tree):
    values = [10, 20, 30, 15, 5, 1, 7, 25, 40, 50, 60, 80, 11, 22]

    for value in values:
        assert tree.insert(value)

    delete_order = [20, 80, 50, 10, 25, 7, 30, 5, 15, 40, 60, 1, 11, 22]

    for value in delete_order:
        assert tree.delete(value)
        # 삭제된 값은 검색되지 않아야 함
        assert tree.search(value) is None

        # 나머지 값은 모두 존재해야 함
        remaining = set(values) - set(delete_order[:delete_order.index(value) + 1])
        for remaining_value in remaining:
            node = tree.search(remaining_value)
            assert node is not None
            assert node.data == remaining_value

        validate_rb_tree(tree)

    assert tree.root is None


def test_delete_nonexistent(tree):
    values = [10, 20, 30, 15, 5]

    for value in values:
        assert tree.insert(value)

    before = [tree.search(value).data for value in values]

    assert not tree.delete(999)
    assert not tree.delete(-999)

    for value in before:
        assert tree.search(value) is not None

    validate_rb_tree(tree)


def test_random_insert_delete(tree):
    values = list(range(1, 101))
    random.shuffle(values)

    # 무작위 삽입
    for value in values:
        assert tree.insert(value)
        validate_rb_tree(tree)

    # 검색 전체 검증
    for value in values:
        node = tree.search(value)
        assert node is not None
        assert node.data == value

    # 무작위 삭제
    random.shuffle(values)

    for value in values:
        assert tree.delete(value)
        assert tree.search(value) is None
        validate_rb_tree(tree)


def test_random_duplicate_insert(tree):
    values = list(range(1, 101))

    for value in values:
        assert tree.insert(value)

    shuffled = values.copy()
    random.shuffle(shuffled)

    for value in shuffled:
        assert not tree.insert(value)

    validate_rb_tree(tree)


def test_sequential_insert_delete(tree):
    values = list(range(1, 101))

    for value in values:
        assert tree.insert(value)
        validate_rb_tree(tree)

    for value in values:
        assert tree.delete(value)
        validate_rb_tree(tree)

    assert tree.root is None