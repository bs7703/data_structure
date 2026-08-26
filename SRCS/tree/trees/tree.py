from typing import Generic, TypeVar, Callable
from .node import Node


T = TypeVar("T")
Comparator = Callable[[T, T], int]

class Tree(Generic[T]):
    def __init__(self, comparator:Comparator[T], node:Node[T]=None):
        self.comparator = comparator
        self.root = node
        self._size = 0
    def __len__(self):
        return self._size
    def compare(self, a:T,b:T):
        return self.comparator(a, b)
    def insert(self, key:T)->bool:
        self.root, ins= self._insert(self.root, key)
        if ins:
            self._size += 1 
        return ins
    def delete(self, key:T):
        self.root, ins = self._delete(self.root, key)
        if (ins):
            self._size -= 1
        return ins
    def search(self, key:T)->bool:
        return self._search(self.root, key)
    def _search(self, current:Node[T] | None, key:T)->Node[T]:
        if current is None:
            return None
        comp = self.compare(current.data, key)
        if comp == 0:
            return current
        return self._search(current.left if comp > 0 else current.right, key)
    
    def __str__(self) -> str:
        if self.root is None:
            return "Tree (Empty)"

        lines, _ = self._build_top_down_string(self.root)
        header = f"Tree (size={self._size}):\n"
        return header + "\n".join(lines)

    def _build_top_down_string(self, node: Node[T] | None) -> tuple[list[str], int]:
        if node is None:
            return [], 0

        # 노드의 표시 텍스트 생성 (RED/BLACK 색상 속성이 있으면 포함)
        val_str = str(node.data)
        if hasattr(node, "color"):
            # 노드의 RED 값이 0 또는 False 등의 상수일 경우에 맞춰 표시
            color_char = "R" if getattr(node, "color") == 0 else "B"
            val_str += f"({color_char})"

        # 자식이 없는 리프 노드 처리
        if node.left is None and node.right is None:
            return [val_str], len(val_str) // 2

        # 좌/우 서브트리 재귀 호출
        left_lines, left_pos = self._build_top_down_string(node.left)
        right_lines, right_pos = self._build_top_down_string(node.right)

        left_width = len(left_lines[0]) if left_lines else 0
        right_width = len(right_lines[0]) if right_lines else 0

        # 현재 노드의 라인 및 연결선(/, \) 생성
        node_len = len(val_str)
        left_branch = "/" if node.left else " "
        right_branch = "\\" if node.right else " "

        # 간격 계산
        left_offset = max(left_pos, 0) if node.left else 0
        right_offset = (right_width - 1 - right_pos) if node.right else 0
        gap = max(2, node_len)

        # 1번째 줄: 현재 노드 값
        first_line = " " * left_offset + val_str + " " * right_offset
        root_pos = left_offset + len(val_str) // 2

        # 2번째 줄: 자식 노드로 연결되는 가지(/, \)
        second_line = [" "] * len(first_line)
        if node.left:
            second_line[left_offset] = "/"
        if node.right:
            second_line[len(first_line) - 1 - right_offset] = "\\"
        second_line_str = "".join(second_line)

        # 서브트리 블록 병합
        combined_lines = [first_line, second_line_str]
        max_depth = max(len(left_lines), len(right_lines))

        for i in range(max_depth):
            l_line = left_lines[i] if i < len(left_lines) else " " * left_width
            r_line = right_lines[i] if i < len(right_lines) else " " * right_width
            
            # 좌/우 서브트리 간격 맞춤
            spacer = " " * (len(first_line) - len(l_line) - len(r_line))
            combined_lines.append(l_line + spacer + r_line)

        return combined_lines, root_pos