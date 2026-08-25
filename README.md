# Data Structure & Algorithm

자료구조와 알고리즘을 직접 구현하면서, 단순한 기능 구현을 넘어 **추상화, 재사용성, 확장성, 자료구조와 알고리즘의 결합 방식**을 학습하기 위한 프로젝트입니다.

처음에는 자료구조를 직접 구현하는 것에서 시작했지만, 현재는 하나의 구현에 종속되지 않는 **범용적인 자료구조와 알고리즘 구조**를 만드는 것을 목표로 확장하고 있습니다.

> **핵심 목표:**
> 자료구조를 구현하고 → 알고리즘에 적용하고 → 공통 인터페이스를 정의하고 → 서로 다른 구현과 전략을 교체해보며 → 정확성, 복잡도, 성능의 차이를 직접 확인합니다.

---

## Project Direction

이 프로젝트에서 가장 중요하게 생각하는 것은 단순히 많은 자료구조와 알고리즘을 구현하는 것이 아닙니다.

하나의 자료구조를 구현한 뒤 끝내는 것이 아니라, 다음과 같은 계층으로 발전시키는 것을 목표로 합니다.

```text
                     Abstract Data Type
                            │
                            ▼
                       Interface
                            │
             ┌──────────────┴──────────────┐
             │                             │
      Data Structure                    Algorithm
             │                             │
      ┌──────┴──────┐              ┌───────┴───────┐
      │             │              │               │
   구현 A        구현 B          Algorithm A    Algorithm B
      │             │              │               │
      └──────┬──────┘              └───────┬───────┘
             │                             │
             └──────────────┬──────────────┘
                            ▼
                    Tests / Benchmark
```

### 설계 원칙

**Minimal Interface**

자료구조와 알고리즘 사이에는 실제로 필요한 기능만 노출합니다.

**Composition**

저장 방식과 최적화 전략을 독립적인 구성요소로 분리하고 필요에 따라 조합합니다.

**Generic Implementation**

가능한 한 특정 데이터 타입이나 구체적인 구현에 종속되지 않도록 설계합니다.

**Replaceable Strategy**

같은 알고리즘에 서로 다른 자료구조 또는 최적화 전략을 적용할 수 있도록 구성합니다.

**Correctness First**

자료구조의 invariant와 알고리즘의 정당성을 먼저 확보한 뒤 성능을 최적화합니다.

---

# Current Structure

현재 소스 구조는 다음 방향으로 구성하고 있습니다.

```text
SRCS/
├── ALGORITHMS/
│   └── kruskal.py
│
├── COMMON/
│   └── union_find.py
│
└── HEAP/
    └── heap.py
```

`HEAP`에는 Generic/Comparator 기반의 Heap 구현이 있으며, `COMMON`에는 여러 자료구조와 알고리즘에서 사용할 수 있는 공통 추상화가 들어가는 방향으로 확장하고 있습니다. `ALGORITHMS`에는 자료구조를 실제 알고리즘에 적용하는 구현을 추가할 예정입니다.

---

# Implemented / In Progress

## Heap

현재 저장소에서 가장 먼저 구현된 주요 자료구조입니다.

```text
Heap[T]
│
├── Generic[T]
├── Comparator[T]
├── insert()
├── peek()
├── pop()
├── sift_up()
└── sift_down()
```

외부에서 `Comparator`를 전달받아 원소의 구체적인 타입이나 정렬 기준에 직접 종속되지 않도록 설계했습니다.

이를 통해 동일한 Heap 구조에서:

```text
Min Heap
Max Heap
Custom Priority
Custom Object
```

등을 비교 정책에 따라 구현할 수 있도록 하는 것을 목표로 합니다.

### Heap에서 학습한 내용

* 완전이진트리의 배열 표현
* Parent / Left / Right index 계산
* Heap invariant
* Sift Up
* Sift Down
* Insert / Extract
* Priority Queue
* Generic 자료구조
* Comparator 주입
* 자료구조의 추상 인터페이스

---

# Union-Find

현재 `COMMON/union_find.py`에서 가장 높은 수준의 추상화를 실험하고 있는 자료구조입니다.

현재 설계는 단순한 `parent[] + rank[]` 구현을 넘어 다음과 같이 구성되어 있습니다.

```text
DisjointSet
      │
      ▼
AbstractDisjointSet
      │
      ▼
UnionFind
  │
  ├── Identity
  │
  ├── ParentStore
  │
  └── UnionStrategy
         │
         ├── NoRank
         │
         └── UnionByRank
                │
                └── RankStore
```

### DisjointSet

Union-Find가 외부에 제공해야 하는 최소 논리 연산을:

```text
find(x)
union(x, y)
```

로 정의합니다.

### Identity

원소가 특정 클래스인지, 정수인지, 문자열인지 Union-Find가 직접 알지 않도록 원소의 동일성 판단을 외부 정책으로 분리하는 방향을 사용합니다.

기본적으로는:

```python
lambda a, b: a == b
```

와 같은 equality를 사용할 수 있으며, 필요하면 별도의 동일성 기준을 주입할 수 있습니다.

### ParentStore

Union-Find의 parent 관계를 실제 어디에 저장할지 추상화합니다.

```text
ParentStore
├── initialize()
├── get_parent()
└── set_parent()
```

향후 다음과 같은 구현을 실험할 수 있습니다.

```text
Array
HashMap
Tree
Custom Storage
```

### RankStore

Rank 또는 Size 기반 최적화에 필요한 상태를 별도의 저장소로 분리합니다.

이를 통해 Rank가 Union-Find의 필수 개념이 아니라 **선택적인 최적화 전략**이라는 점을 코드 구조에 반영합니다.

### UnionStrategy

Union 자체의 최적화 방법을 전략으로 분리합니다.

```text
UnionStrategy
├── NoRank
├── UnionByRank
└── UnionBySize
```

향후 다른 Union 정책도 동일한 인터페이스 아래 확장할 수 있도록 설계합니다.

> 현재 Union-Find의 추상 구조는 구현 중이며 `find()`와 `union()`의 실제 알고리즘 구현 및 각 Storage의 구체 구현이 다음 단계입니다.

---

# Algorithms

알고리즘은 특정 자료구조에 종속시키기보다 필요한 추상 기능에 의존하도록 설계하는 것을 목표로 합니다.

현재 `ALGORITHMS/kruskal.py`에는 Kruskal 구현을 위한 기본 골격이 있으며, 실제 알고리즘 구현을 Union-Find와 결합하는 단계로 확장할 예정입니다.

---

## Kruskal

Kruskal은 다음 구조를 통해 구현할 예정입니다.

```text
Graph
  │
  ▼
Edge List
  │
  ▼
Sort by Weight
  │
  ▼
Union-Find
  │
  ├── find()
  └── union()
  │
  ▼
Minimum Spanning Tree
```

학습 목표는 단순히 알고리즘을 코드로 옮기는 것이 아니라:

* Greedy Choice
* Cut Property
* Cycle Detection
* Union-Find
* Edge Sorting
* Minimum Spanning Tree

가 어떻게 서로 결합되는지를 구현 수준에서 확인하는 것입니다.

---

# Learning Progress

현재까지 집중적으로 학습하고 구현한 자료구조 영역은 다음과 같습니다.

```text
Data Structures
├── Heap
├── Binary Search Tree
├── AVL Tree
├── Red-Black Tree
└── Union-Find
```

트리 계열에서는 단순 삽입/검색보다:

```text
Invariant
    ↓
Modification
    ↓
Violation
    ↓
Repair
    ↓
Invariant Restoration
```

이라는 구조를 중심으로 이해하고 구현했습니다.

특히 AVL과 Red-Black Tree를 통해 Rotation, balancing, deletion fix-up 등 **구조적 불변식을 유지하는 자료구조 설계**를 학습했습니다.

---

# Algorithm Roadmap

자료구조와 알고리즘을 다음과 같은 계층으로 확장할 계획입니다.

## Searching

```text
Linear Search
Binary Search
Tree Search
Graph Search
├── BFS
└── DFS
```

## Sorting

```text
Insertion Sort
Selection Sort
Merge Sort
Quick Sort
Heap Sort
Counting Sort
Radix Sort
```

각 정렬 알고리즘에 대해:

```text
Time Complexity
Space Complexity
Stable / Unstable
In-place / Out-of-place
Best / Average / Worst Case
```

를 비교합니다.

---

# Graph Algorithms

Graph는 하나의 고정된 구현이 아니라 추상적인 관계 구조로 정의하고, 실제 표현 방법을 별도로 선택하는 방향으로 설계합니다.

```text
Graph
├── Adjacency List
├── Adjacency Matrix
└── Edge List
```

이후:

```text
BFS
DFS
Topological Sort
Kruskal
Prim
Dijkstra
Bellman-Ford
Floyd-Warshall
Strongly Connected Components
Minimum Cut / Maximum Flow
```

등으로 확장합니다.

---

# Greedy

대표적인 Greedy 알고리즘을 구현하고, 단순히 "현재 가장 좋은 선택"을 하는 것이 아니라 **왜 그 선택이 전체 최적해를 보장하는지**를 함께 학습합니다.

예정 항목:

```text
Activity Selection
Huffman Coding
Kruskal
Prim
Dijkstra
```

---

# Dynamic Programming

DP는 특정 문제 유형을 암기하기보다 다음 구조를 직접 설계하는 것을 목표로 합니다.

```text
State
  ↓
Transition
  ↓
Base Case
  ↓
Evaluation Order
```

예정 항목:

```text
Knapsack
LIS
LCS
Coin Change
Interval DP
Tree DP
Bitmask DP
```

---

# Advanced Data Structures

자료구조의 추상화 수준을 높이며 다음 구조를 단계적으로 구현할 예정입니다.

```text
Priority Queue
Indexed Heap
d-ary Heap
Trie
Radix Tree
Segment Tree
Fenwick Tree
B-Tree
B+Tree
Interval Tree
Persistent Tree
Skip List
Fibonacci Heap
```

각 자료구조는 단순 구현보다:

```text
What problem does it solve?
        ↓
What invariant does it maintain?
        ↓
What operations does it expose?
        ↓
What is the implementation strategy?
        ↓
What is the complexity?
        ↓
What are the trade-offs?
```

를 중심으로 학습합니다.

---

# Abstraction Roadmap

프로젝트의 중요한 장기 목표 중 하나는 **자료구조와 알고리즘의 구현을 교체 가능한 구성요소로 만드는 것**입니다.

예를 들어:

```text
PriorityQueue
      │
 ┌────┼───────────┐
 ▼    ▼           ▼
Heap  d-ary Heap  Fibonacci Heap
      │
      ▼
    Dijkstra
```

또는:

```text
Graph
      │
 ┌────┼──────────────┐
 ▼    ▼              ▼
List Matrix           CSR
      │
      ▼
 Graph Algorithms
```

그리고:

```text
UnionFind
      │
 ┌────┼─────────────┐
 ▼    ▼             ▼
NoRank Rank         Size
      │
      ▼
 ParentStore
 ├── Array
 ├── HashMap
 └── Tree
```

처럼 구성합니다.

이 구조를 통해 **알고리즘의 논리와 구체적인 자료구조 구현을 분리**하고, 동일한 알고리즘에 여러 구현을 적용하여 차이를 비교하는 것을 목표로 합니다.

---

# Testing

각 자료구조와 알고리즘은 단순한 예제 실행보다 **불변식과 경계조건을 검증하는 테스트**를 중심으로 확장할 예정입니다.

## Data Structure Tests

```text
Empty
Single Element
Duplicate
Insert
Delete
Search
Update
Iteration
Large Input
Boundary Cases
```

## Tree Tests

```text
BST Ordering
AVL Balance
Rotation
Red-Black Properties
Black Height
Parent / Child Consistency
```

## Heap Tests

```text
Heap Property
Insert / Pop Ordering
Empty Heap
Duplicate Values
Custom Comparator
```

## Algorithm Tests

```text
Correctness
Disconnected Graph
Duplicate Edges
Negative / Invalid Input
Degenerate Input
Randomized Input
Large Input
```

---

# Benchmark

정확성이 확보된 이후에는 동일한 인터페이스를 만족하는 서로 다른 구현을 실제 실행시간과 메모리 사용량 측면에서 비교합니다.

```text
                    Same Algorithm
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Implementation A Implementation B Implementation C
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    Benchmark
```

비교 대상:

```text
Time
Memory
Operation Count
Average / Worst Case
Input Distribution
```

를 단계적으로 추가할 예정입니다.

---

# Design Philosophy

이 프로젝트에서 추상화는 단순히 코드를 짧게 만들기 위한 목적이 아닙니다.

하나의 구현만 존재할 때는 추상화가 오히려 코드량을 증가시킬 수 있지만, 구현과 전략의 종류가 늘어나면:

```text
구체 구현을 모두 개별적으로 작성
            ↓
       중복 증가
            ↓
       변경 비용 증가
```

가 발생합니다.

Composition과 Interface를 사용하면:

```text
             Core Algorithm
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    Storage      Strategy     Identity
       │            │            │
   여러 구현       여러 구현      여러 기준
```

으로 분리할 수 있고, 하나의 구성요소를 변경해도 다른 부분의 구현을 수정할 필요가 줄어듭니다.

따라서 이 프로젝트에서 추상화는:

[
\boxed{
현재의 복잡도를 증가시키는 대신
미래의 구현·변경·확장 비용을 감소시키는 것
}
]

을 목표로 합니다.

---

# Current Status

```text
[Implemented / Studied]

Heap
Binary Search Tree
AVL Tree
Red-Black Tree

[In Progress]

Union-Find abstraction
ParentStore
RankStore
UnionStrategy
Identity
Kruskal

[Planned]

Sorting
Searching
Graph
Greedy
Dynamic Programming
Advanced Data Structures
Testing
Benchmark
```

현재 저장소에서는 Heap 구현이 실제 코드로 존재하고, Union-Find는 추상화 및 전략 구성까지 설계된 상태이며 `find()` / `union()` 구현을 진행하는 단계입니다. Kruskal 역시 현재 구현을 시작하기 위한 골격 단계입니다.

---

# Long-Term Goal

최종적으로 이 저장소를 단순한 자료구조 구현 모음이 아니라,

> **자료구조의 원리를 직접 구현하고, 알고리즘과 결합하며, 추상화와 Composition을 통해 여러 구현을 교체하고, 테스트와 benchmark를 통해 각각의 trade-off를 비교하는 학습용 알고리즘 라이브러리**

로 발전시키는 것을 목표로 합니다.

```text
Data Structure
      ↓
Abstract Data Type
      ↓
Concrete Implementation
      ↓
Algorithm
      ↓
Testing
      ↓
Benchmark
      ↓
Alternative Implementation
      ↓
Performance / Design Comparison
```
