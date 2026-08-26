# Data Structure & Algorithm Study

자료구조와 알고리즘을 직접 구현하며 **개념 → 단순 구현 → 병목 분석 → 추상화 → 최적화**의 흐름으로 학습하는 프로젝트.

단순히 구현 결과를 따라가는 것보다, 각 자료구조와 알고리즘이 **왜 현재의 구조를 가지게 되었는지**를 직접 확인하는 것을 목표로 한다.

---

## 현재 구현

### Data Structures

* Heap
* Binary Search Tree
* AVL Tree
* Red-Black Tree
* Hash Map
* 기타 기본 자료구조 구현 및 테스트

### Algorithms

* 기본 탐색 및 정렬 관련 구현
* Graph 기반 알고리즘 학습
* Dijkstra
* Kruskal / Minimum Spanning Tree 학습 및 구현 과정 진행

### Current Focus

#### Union-Find

현재 Union-Find를 중심으로 다음 구조를 단계적으로 학습하고 있다.

* Disjoint Set의 기본 개념
* `Find` / `Union`의 최소 인터페이스
* `Generic T`, `K`를 이용한 추상화
* `GroupStore` 기반의 가장 기본적인 구현
* `Protocol` / `ABC`를 이용한 인터페이스 계층
* `Identity`를 이용한 동일성 정책 분리
* Storage와 알고리즘의 분리
* 이후 Parent 기반 표현, Path Compression, Union by Rank/Size로 확장 예정

---

## 학습 과정에서 얻은 주요 통찰

### 1. 추상화와 구현의 분리

자료구조의 논리적인 정의와 실제 저장 구조는 서로 다른 계층으로 분리할 수 있다.

예를 들어 Union-Find의 핵심은 `Find`와 `Union`이며, `Parent`, `Group ID`, `Rank` 등은 이를 구현하기 위한 구체적인 표현과 최적화로 볼 수 있다.

### 2. 최소 구현에서 출발

처음부터 최적화된 구조를 만들기보다 가장 단순한 표현을 먼저 구현하고, 실제 병목이 발생했을 때 새로운 구조를 도입한다.

```text
문제 정의
→ 단순 구현
→ 병목 발견
→ 새로운 표현
→ 최적화
```

### 3. Composition을 통한 확장

알고리즘의 핵심과 저장 구조 및 정책을 분리하면 하나의 알고리즘에 다양한 구현을 조합할 수 있다.

```text
Algorithm
├── Storage
├── Identity / Policy
└── Optimization Strategy
```

이를 통해 구현 방식의 변경이 핵심 알고리즘에 미치는 영향을 줄일 수 있다.

### 4. 인터페이스의 역할

`Protocol`은 구조적으로 필요한 기능을 정의하고, `ABC`는 프로젝트 내부 구현체가 따라야 할 상속 기반 규칙을 정의하는 방식으로 역할을 구분한다.

---

## 앞으로 구현할 것

### Data Structures

* Queue / Deque
* Linked List 계열 확장
* Trie
* B-Tree / B+ Tree
* Segment Tree
* Fenwick Tree
* Union-Find 고도화
* 추가적인 Heap 변형

### Algorithms

* Sorting algorithms 전체 정리
* BFS / DFS
* Topological Sort
* Prim / Kruskal 비교
* Bellman-Ford
* Floyd-Warshall
* Dynamic Programming
* Greedy
* Divide & Conquer
* Backtracking
* String Algorithms

### 구현 및 분석

* 동일 알고리즘의 다양한 Storage 구현 비교
* 시간/공간 복잡도 비교
* 자료구조별 Trade-off 분석
* Interface / Composition / Strategy 기반 설계 확장
* 테스트 및 Benchmark 체계화

---

## Learning Direction

이 프로젝트의 최종 목표는 단순히 자료구조와 알고리즘을 구현하는 것이 아니라,

> **문제를 가장 단순하게 모델링하고 → 구현상의 한계를 발견하고 → 더 나은 자료구조와 알고리즘을 도입하고 → 이를 추상화하여 재사용 가능한 구조로 발전시키는 능력**

을 갖추는 것이다.
