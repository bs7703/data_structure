# 🌳 Data Structures & Tree Implementation

> 자료구조의 개념을 이해하고, 직접 Python으로 구현하면서
> **자료구조 → 객체 추상화 → 재사용 가능한 구조 → 균형 트리 → 불변식 검증**까지 학습한 기록

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Data Structures](https://img.shields.io/badge/Data%20Structures-Implementation-green)]
[![Trees](https://img.shields.io/badge/Trees-BST%20%7C%20AVL%20%7C%20RB-red)]

---

## 📌 Overview

이 저장소는 단순히 자료구조의 알고리즘을 구현하는 것을 목표로 하지 않는다.

학습 과정에서 다음과 같은 질문을 해결하는 것을 중심으로 발전시켰다.

* 자료구조의 **논리적 구조**는 어떻게 코드로 표현되는가?
* `Node`와 `Tree`의 책임을 어디까지 분리해야 하는가?
* 여러 Tree 구현에서 반복되는 코드를 어떻게 추상화할 수 있는가?
* 재귀적인 Tree 연산에서 노드의 연결 관계는 어떻게 유지되는가?
* AVL Tree의 회전은 어떤 불변식을 유지하기 위해 필요한가?
* Red-Black Tree는 어떤 조건을 유지하면서 균형을 보장하는가?
* 부모 포인터와 자식 포인터를 어떻게 일관되게 관리해야 하는가?
* 구현이 맞다는 것을 어떻게 **테스트와 불변식 검증**으로 확인할 수 있는가?

최종적으로 다음 구조를 구현하고 공통 추상화를 시도하였다.

```text
                         Tree (Abstract)
                              │
              ┌───────────────┼───────────────┐
              │               │               │
             BST             AVL             RB
              │               │               │
              └───────────────┼───────────────┘
                              │
                         Node Abstraction
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 AVLNode             RBNode
                                        │
                                   parent / color
```

---

# 📚 Learning Roadmap

학습은 다음과 같은 순서로 진행되었다.

```text
자료구조 기본 개념
        ↓
Node / Tree 구조
        ↓
추상화(Abstract Base Class)
        ↓
Generic / Type Annotation
        ↓
Binary Search Tree
        ↓
BST Search / Insert / Delete
        ↓
Tree 연결 구조와 재귀
        ↓
AVL Tree
        ↓
Balance Factor
        ↓
Rotation
        ↓
Rebalancing
        ↓
Red-Black Tree
        ↓
Color / Parent Pointer
        ↓
Recoloring / Rotation
        ↓
Node 공통 추상화
        ↓
불변식(Invariant) 검증
        ↓
테스트 기반 구현 검증
```

---

# 1. 🌱 자료구조와 Tree의 기본 구조

먼저 Tree를 단순한 계층적 자료구조로 이해하는 것에서 시작했다.

## Tree의 기본 요소

```text
             Root
              │
        ┌─────┴─────┐
      Node          Node
       │
   ┌───┴───┐
 Node     Node
```

핵심적으로 이해한 요소:

* Root
* Parent
* Child
* Leaf
* Subtree
* Height
* Depth
* Binary Tree
* Binary Search Tree

특히 Tree는 배열처럼 단순히 데이터를 나열하는 구조가 아니라,

> **Node 사이의 연결 관계 자체가 자료구조를 구성한다**

는 점을 이해하는 것을 중요한 출발점으로 삼았다.

---

# 2. 🧩 Node와 Tree의 책임 분리

Tree를 구현하면서 `Node`와 `Tree`가 서로 다른 책임을 가진다는 것을 학습했다.

### Node

Node는 개별 데이터와 연결 관계를 표현한다.

```python
class Node:
    data
    left
    right
```

### Tree

Tree는 전체 구조와 연산을 관리한다.

```python
class Tree:
    root
    insert()
    search()
    delete()
```

즉,

```text
Node
 └─ 하나의 구성 요소

Tree
 └─ Node들을 이용하여 전체 자료구조를 관리
```

라는 책임 분리를 이해했다.

---

# 3. 🏗️ 추상화(Abstract Base Class)

초기 구현에서 `Tree`를 추상 클래스로 정의하고 Tree가 공통적으로 제공해야 할 인터페이스를 정의했다.

```python
class Tree(ABC):

    @abstractmethod
    def insert(self, key):
        pass

    @abstractmethod
    def search(self, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass
```

이 과정에서 배운 핵심은

> **추상화는 구현을 숨기는 것만이 아니라, 여러 구현이 공유해야 하는 "계약(interface)"을 정의하는 것**

이라는 점이다.

따라서 BST, AVL, RB Tree가 서로 다른 내부 알고리즘을 사용하더라도 외부에서는

```text
insert()
search()
delete()
```

라는 동일한 인터페이스를 사용할 수 있다.

---

# 4. 🧬 Generic과 Type Abstraction

Tree가 특정 타입에 종속되지 않도록 Generic을 사용하였다.

```python
T = TypeVar("T")

class Node(Generic[T]):
    ...
```

이를 통해 Tree가 특정 숫자 타입만 처리하는 구조가 아니라,

```text
Tree[int]
Tree[float]
Tree[str]
Tree[CustomObject]
```

와 같이 다양한 데이터 타입을 처리할 수 있는 구조로 발전시켰다.

또한 비교 방법 자체를 Tree에 고정하지 않고 comparator를 전달하는 방향을 학습했다.

```python
Comparator = Callable[[T, T], int]
```

즉,

```text
Data
 ↓
Comparator
 ↓
Tree의 ordering
```

을 분리하였다.

이것은 자료구조 구현에서 **데이터와 알고리즘의 결합도를 낮추는 방법**을 이해하는 계기가 되었다.

---

# 5. 🌳 Binary Search Tree

다음 단계로 BST를 구현했다.

BST의 핵심 invariant:

```text
             Node
            /    \
       smaller   larger
```

즉,

```text
left subtree  <  node  <  right subtree
```

라는 ordering을 유지한다.

## Search

```python
if key == current.data:
    return current

if key < current.data:
    search(current.left)
else:
    search(current.right)
```

## Insert

삽입 역시 ordering을 유지하면서 적절한 위치를 찾아간다.

## Delete

BST에서 가장 중요한 부분 중 하나로,

```text
Case 1. Leaf

Case 2. Child 하나

Case 3. Child 둘
```

의 세 가지 상황을 처리했다.

특히 두 자식을 가진 Node를 삭제할 때 predecessor/successor를 이용하여 값을 대체한 뒤 다시 subtree를 삭제하는 구조를 이해했다.

---

# 6. 🔄 재귀와 Tree 연결 구조

BST 구현 과정에서 중요한 개념을 하나 더 학습했다.

Tree의 재귀 함수는 단순히 "재귀적으로 탐색한다"가 아니라,

> **재귀 함수가 새로운 subtree의 root를 반환하고, 부모가 그 값을 다시 자신의 child로 연결한다**

는 구조를 가진다.

예를 들어:

```python
node, inserted = self._insert(current.left, key)
current.left = node
```

의 의미는 단순한 함수 호출이 아니라,

```text
현재 Node
   │
   └── left subtree
          │
          └── insert()
                 │
                 └── 새로운 subtree root 반환
                           │
                           ↓
                     current.left
```

로 이해할 수 있다.

이 개념은 이후 AVL과 RB Tree를 구현할 때 매우 중요한 기반이 되었다.

---

# 7. ⚖️ AVL Tree

BST의 가장 큰 문제는 입력 순서에 따라 Tree가 한쪽으로 치우칠 수 있다는 것이다.

```text
10
  \
   20
     \
      30
        \
         40
```

이 경우 Tree가 사실상 Linked List처럼 변한다.

AVL Tree는 이를 해결하기 위해 높이 균형을 유지한다.

---

## Balance Factor

각 Node에 대해:

```text
BF = height(left) - height(right)
```

AVL Tree는 일반적으로 다음 조건을 유지한다.

```text
-1 ≤ BF ≤ 1
```

따라서 삽입 또는 삭제 이후 균형이 깨지면 rotation을 수행한다.

---

# 8. 🔄 AVL Rotation

AVL에서 학습한 핵심은 네 가지 회전 상황이다.

```text
LL → Right Rotation

RR → Left Rotation

LR → Left Rotation + Right Rotation

RL → Right Rotation + Left Rotation
```

예:

```text
LL Case

        30
       /
     20
    /
  10

        ↓ Right Rotation

      20
     /  \
   10    30
```

단순히 회전 코드를 작성하는 것보다,

> **회전 전후에도 BST ordering은 유지하면서 height imbalance만 제거한다**

는 관점으로 이해하였다.

---

# 9. 🧠 AVL Rebalancing 추상화

초기 AVL 구현에서는 각각의 경우를 직접 분기했다.

이후에는 조건을 변수로 분리하여 `rebalance()`의 구조를 단순화하는 방향으로 발전시켰다.

예:

```python
left_heavy = balance_factor > 1
right_heavy = balance_factor < -1
inner_rotation = ...
```

이를 통해 알고리즘의 복잡한 조건을

```text
상태 계산
   ↓
상태 분류
   ↓
필요한 rotation
```

으로 분리하는 방법을 학습했다.

실제 커밋에서도 AVL의 `rebalance` 조건을 논리값과 변수로 사전 정의하여 분기 구조를 단순화하는 방향으로 발전하였다.

---

# 10. 🔴⚫ Red-Black Tree

AVL 이후 Red-Black Tree를 구현하였다.

Red-Black Tree는 각 Node에 color 정보를 추가한다.

```text
RED
BLACK
```

그리고 Tree가 다음과 같은 규칙을 유지하도록 한다.

### 주요 Invariants

1. Root는 Black
2. Red Node의 Child는 Red가 될 수 없음
3. 모든 root-to-leaf 경로에서 Black Node 수가 일정해야 함
4. Tree의 ordering은 BST와 동일하게 유지

즉 RB Tree는 단순한 BST가 아니라,

```text
BST ordering
+
Color invariant
+
Black-height invariant
```

를 동시에 관리하는 자료구조다.

---

# 11. 🔗 Parent Pointer

RB Tree 구현에서 중요한 변화가 있었다.

기존 Node:

```text
parent
  ↓
Node
 ├── left
 └── right
```

구조가 없었지만 RB Tree에서는 부모를 알아야 삽입 후 위쪽으로 올라가면서 균형을 복구할 수 있다.

따라서:

```python
self.parent = parent
```

를 추가하였다.

그리고 부모-자식 관계를 일관되게 관리하기 위해:

```python
set_child()
get_parent()
```

를 도입하였다.

```text
Parent
  │
  ├── Child
  │      ↑
  └──── parent
```

이 구조를 통해 Tree의 양방향 연결 관계를 명시적으로 관리할 수 있게 되었다.

---

# 12. 🔧 Node Abstraction의 발전

이 저장소에서 가장 중요한 학습 포인트 중 하나다.

초기에는 BST와 AVL에서 다음과 같은 코드가 반복되었다.

```python
if comp > 0:
    current.left = ...
else:
    current.right = ...
```

이를 Node 수준에서 추상화하여:

```python
current.next(direction)
current.set_next(node, direction)
```

형태로 변경하였다.

그러면 Tree 구현은

```python
node = current.next(direction)

...

current.set_next(node, direction)
```

처럼 작성할 수 있다.

결과적으로:

```text
BST
AVL
RB
 │
 └──── 공통 Node abstraction
```

이라는 구조가 만들어졌다.

실제 마지막 구현에서도 BST와 AVL의 좌/우 child 접근을 `next()`와 `set_next()`로 통일하여 중복되는 분기 코드를 제거하였다.

---

# 13. 🔄 Tree Rotation과 연결 관계

Rotation을 구현하면서 단순히 값의 위치를 바꾸는 것이 아니라,

> **Node 사이의 참조 관계를 정확하게 재구성하는 작업**

이라는 점을 학습했다.

예를 들어 오른쪽 회전:

```text
        A
       /
      B
       \
        C
```

↓

```text
      B
       \
        A
       /
      C
```

실제로는 다음 관계를 동시에 수정해야 한다.

```text
A.left
B.right
parent
root
subtree
```

특히 RB Tree에서는 parent pointer까지 존재하기 때문에 rotation은 더욱 복잡해진다.

따라서 `set_child()` 같은 연결 관리 함수를 사용하는 것이 중요해졌다.

---

# 14. 🧪 테스트와 불변식 검증

구현이 복잡해지면서 단순히 `insert()`가 실행된다는 것만으로는 코드가 올바르다고 판단할 수 없다는 것을 학습했다.

특히 RB Tree에서는 다음을 검증해야 한다.

```text
BST ordering
        +
Root is Black
        +
No Double Red
        +
Black Height
        +
Parent Pointer
        +
Rotation correctness
```

따라서 테스트 코드에서 대량의 삽입/삭제와 다양한 구조를 생성하여 검증하는 방향으로 발전하였다.

마지막 커밋에서는 BST, AVL, RB Tree의 삽입·삭제·회전뿐 아니라 RB Tree의 recoloring, parent pointer, black-height 같은 핵심 불변식까지 테스트하도록 확장되어 있다.

---

# 15. 🧹 Bug Fix와 Refactoring

학습 과정에서 구현 → 테스트 → 오류 발견 → 구조 수정의 사이클도 경험하였다.

대표적으로:

* AVL의 class naming 수정
* AVL deletion 조건 수정
* Node의 height 기준 수정
* 불필요한 Tree/Node 코드 제거
* 중복되는 좌/우 child 처리 추상화
* Parent-child 관계 관리 개선
* 테스트 코드 추가

등을 진행하였다.

특히 `70e0562` 커밋에서는 AVL의 deletion 조건과 naming 문제를 수정하고 테스트 코드가 대폭 추가되었다.

---

# 🗂️ Repository Structure

```text
tree/
│
├── trees/
│   ├── node.py
│   ├── tree.py
│   ├── bst.py
│   ├── avl.py
│   └── rb.py
│
└── test/
    ├── test.py
    └── test_rb.py
```

### `tree.py`

Tree의 공통 인터페이스와 공통 동작을 정의한다.

```text
Tree
 ├── root
 ├── comparator
 ├── insert()
 ├── search()
 └── delete()
```

### `node.py`

Tree에서 사용되는 Node abstraction을 담당한다.

```text
Node
 ├── data
 ├── left
 ├── right
 ├── is_leaf()
 ├── next()
 └── set_next()

AVLNode
 └── height

RBNode
 ├── color
 └── parent
```

현재 저장소의 구조도 `node.py`, `tree.py`, `bst.py`, `avl.py`, `rb.py`로 분리되어 있다.

---

# 📈 Implementation History

실제 Git commit history를 기준으로 보면 다음과 같은 발전 과정을 거쳤다.

| 단계 | Commit    | 학습/구현 내용                                                 |
| -- | --------- | -------------------------------------------------------- |
| 01 | `f9af34e` | Tree / Node 추상 구조 시작                                     |
| 02 | `adc64b7` | Tree abstraction + Generic + BST 구현                      |
| 03 | `534496c` | 불필요한 코드 제거 및 구조 정리                                       |
| 04 | `71fe410` | AVL 구현 + Tree 공통 기능 추상화                                  |
| 05 | `70e0562` | AVL bug fix + 테스트 코드 확장                                  |
| 06 | `8114c30` | Node abstraction 강화 + RB Tree + parent pointer + 불변식 테스트 |

초기 commit은 `Node(ABC)`와 `Tree(ABC)`라는 매우 작은 추상 구조에서 시작했다.

이후 BST가 추가되면서 실제 자료구조 구현으로 확장되었고, Generic과 comparator를 이용해 자료구조와 데이터 타입/비교 방법을 분리하는 방향으로 발전하였다.

그 다음 AVL을 구현하면서 균형 유지와 rotation이라는 새로운 개념이 추가되었고, 마지막에는 RB Tree와 공통 Node abstraction까지 확장되었다.

---

# 🧠 What I Learned

## 자료구조

* [x] Tree
* [x] Binary Tree
* [x] Binary Search Tree
* [x] BST Search
* [x] BST Insert
* [x] BST Delete
* [x] Predecessor / Successor 개념
* [x] Tree Height
* [x] AVL Tree
* [x] Balance Factor
* [x] Tree Rotation
* [x] AVL Rebalancing
* [x] Red-Black Tree
* [x] Recoloring
* [x] Parent Pointer
* [x] Black Height
* [x] Tree Invariant

## 객체지향 / 추상화

* [x] Abstract Base Class
* [x] Abstract Method
* [x] Interface와 Implementation의 분리
* [x] Generic
* [x] Type Annotation
* [x] Comparator abstraction
* [x] 상속
* [x] 공통 기능 추출
* [x] Node abstraction
* [x] Parent-child 관계 encapsulation
* [x] 코드 중복 제거

## 알고리즘적 사고

* [x] Recursive Tree Traversal
* [x] Subtree를 반환하는 재귀
* [x] 상태 기반 분기
* [x] Rotation
* [x] Rebalancing
* [x] Invariant 유지
* [x] Edge Case 처리
* [x] 테스트를 통한 구현 검증

## 소프트웨어 구현

* [x] 구현 → 테스트 → 수정 사이클
* [x] Git commit 기반 개발 과정 기록
* [x] Bug fixing
* [x] Refactoring
* [x] 공통 코드 추상화
* [x] 자료구조와 테스트 코드 분리

---

# 🔍 가장 중요한 학습 변화

이 프로젝트에서 가장 큰 변화는 단순히

> "BST를 구현할 수 있다."

에서 끝난 것이 아니다.

학습이 진행되면서 다음과 같은 관점으로 발전했다.

```text
알고리즘을 구현한다
        ↓
자료구조의 invariant를 이해한다
        ↓
반복되는 구조를 발견한다
        ↓
공통 인터페이스를 정의한다
        ↓
Node / Tree의 책임을 분리한다
        ↓
공통 기능을 추상화한다
        ↓
구현 복잡도를 낮춘다
        ↓
테스트를 통해 invariant를 검증한다
```

즉, 이 프로젝트의 핵심 학습 목표는 **자료구조 자체뿐 아니라 자료구조를 소프트웨어로 설계하는 방법을 배우는 것**이다.

---

# 🛠️ Current Architecture

현재 구현의 핵심 구조는 다음과 같다.

```text
                    ┌───────────────┐
                    │      Tree     │
                    │    Generic    │
                    │   Comparator  │
                    └───────┬───────┘
                            │
            ┌───────────────┼────────────────┐
            │               │                │
            ▼               ▼                ▼
           BST             AVL               RB
            │               │                │
            └───────────────┼────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │      Node     │
                    ├───────────────┤
                    │ data          │
                    │ left          │
                    │ right         │
                    │ next()        │
                    │ set_next()    │
                    └───────┬───────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
                 AVLNode          RBNode
                    │                │
                  height       color / parent
```

---

# 🚧 Future Learning

현재 Tree 구현을 기반으로 다음 단계의 학습을 진행할 수 있다.

### Data Structures

```text
BST
 │
 ├── AVL
 ├── Red-Black Tree
 ├── B-Tree
 ├── B+ Tree
 ├── Heap / Priority Queue
 ├── Trie
 ├── Hash Table
 └── Graph
```

### Algorithm

```text
Tree
 ↓
Heap
 ↓
Graph
 ↓
BFS / DFS
 ↓
Dijkstra
 ↓
Minimum Spanning Tree
 ↓
Sorting
 ↓
Dynamic Programming
```

### Software Engineering

```text
Data Structure
      ↓
Generic Design
      ↓
Abstraction
      ↓
Testing
      ↓
Benchmark
      ↓
Memory / Cache
      ↓
C / C++ Implementation
      ↓
Production-level Data Structure
```

---

# 🎯 Final Goal

이 저장소의 궁극적인 목적은 단순히 자료구조를 암기하는 것이 아니다.

> **자료구조의 수학적/논리적 구조를 이해하고, 이를 유지하는 알고리즘을 설계하며, 공통적인 부분을 추상화하여 재사용 가능한 소프트웨어 구조로 구현하는 능력을 기르는 것**

을 목표로 한다.

현재 프로젝트는 특히 다음 네 가지를 연결하는 과정이다.

```text
        Computer Science
              │
      ┌───────┼────────┐
      │       │        │
 Data Structure Algorithm Abstraction
      │       │        │
      └───────┼────────┘
              │
           Testing
              │
              ▼
       Reliable Software
```

---

## 📜 Repository History

현재 Git history 자체가 학습 과정의 기록이다.

```text
f9af34e
  │
  └── init data_struture_tree
        │
        ▼
adc64b7
  │
  └── Tree / Node abstraction + BST
        │
        ▼
534496c
  │
  └── cleanup / bug fix
        │
        ▼
71fe410
  │
  └── AVL + abstraction
        │
        ▼
70e0562
  │
  └── AVL fix + testing
        │
        ▼
8114c30
  │
  └── Node abstraction + RB Tree
       + parent pointer
       + rotation
       + invariant testing
```

이 commit history는 단순한 코드 변경 이력이 아니라 **자료구조를 이해하는 과정이 코드 구조의 변화로 나타난 학습 기록**이다.

---

## 🔗 Repository

[GitHub Repository — bs7703/tree](https://github.com/bs7703/tree)

---

### Learning Status

```text
Tree                  ████████████████████ 100%
BST                   ████████████████████ 100%
AVL                   ████████████████████ 100%
Red-Black Tree        ███████████████░░░░░  75%
Abstraction           █████████████████░░░  85%
Testing               ███████████████░░░░░  75%
Data Structure Design ██████████████░░░░░░  70%
```

> **Next:** RB Tree deletion → Tree invariant 강화 → Heap → Hash Table → Graph
