# Data Structure & Algorithm Study

자료구조와 알고리즘을 직접 구현하면서 **개념 → 단순 구현 → 병목 분석 → 추상화 → 구체화 → 검증**의 과정을 학습하는 프로젝트.

단순히 구현 결과를 만드는 것보다, 각 자료구조와 알고리즘이 **왜 이러한 구조를 가지는지**, 그리고 하나의 논리적 문제를 **어떻게 서로 다른 저장 구조와 구현 전략으로 분리할 수 있는지**를 직접 탐구하는 것을 목표로 한다.

---

## Project Direction

이 프로젝트는 자료구조와 알고리즘을 단순히 나열하여 구현하는 것을 목표로 하지 않는다.

하나의 문제를 가능한 한 단순하게 모델링한 뒤, 구현 과정에서 발생하는 제약과 병목을 확인하고, 필요한 경우 추상화와 최적화를 도입한다.

```text
Problem
  ↓
Simple Implementation
  ↓
Invariant / Correctness
  ↓
Bottleneck Analysis
  ↓
Abstraction
  ↓
Concrete Implementation
  ↓
Optimization
  ↓
Test / Benchmark
```

### Design Principles

* **Minimal Interface**
  논리적으로 필요한 기능만 상위 인터페이스에 노출한다.

* **Separation of Concerns**
  자료구조의 논리적 연산과 실제 저장 표현을 분리한다.

* **Composition**
  Storage, Identity, Algorithm Policy와 같은 요소를 필요에 따라 조합한다.

* **Generic Implementation**
  가능한 범위에서 특정 데이터 타입이나 구체적인 저장 방식에 대한 의존을 줄인다.

* **Replaceable Strategy**
  동일한 연산에 대해 서로 다른 구현 전략을 선택할 수 있도록 구성한다.

* **Correctness First**
  자료구조의 invariant와 연산의 정당성을 먼저 확보한 뒤 성능을 고려한다.

---

# Current Structure

현재 소스는 자료구조, 공통 추상화, 알고리즘을 서로 다른 영역으로 분리하는 방향으로 구성하고 있다.

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

`HEAP`에는 Generic / Comparator 기반의 Heap 구현이 존재하며, `COMMON`에는 여러 자료구조와 알고리즘에서 재사용할 수 있는 추상화와 공통 개념을 구성하는 방향으로 발전시키고 있다.

---

# Implemented

## Heap

Heap은 본 프로젝트에서 구현한 주요 기본 자료구조 중 하나이다.

```text
Heap[T]
├── Generic[T]
├── Comparator[T]
├── insert()
├── peek()
├── pop()
├── sift_up()
└── sift_down()
```

외부에서 `Comparator`를 전달받아 원소의 구체적인 타입이나 우선순위 판단에 직접 종속되지 않도록 구성하였다.

### 주요 학습 내용

* 완전이진트리의 배열 표현
* Parent / Left / Right index 계산
* Heap invariant
* Sift Up / Sift Down
* Insert / Extract
* Priority Queue
* Generic 자료구조
* Comparator 주입
* 자료구조의 추상 인터페이스

---

# Union-Find

Union-Find를 구현하는 과정에서 단순한 Disjoint Set 구현을 넘어, **논리적 연산과 저장 구조 및 알고리즘 전략을 분리하는 추상화 구조**를 단계적으로 구성하였다.

## 1. Disjoint Set의 기본 추상화

Union-Find의 최소 연산을:

```text
Find
Union
```

으로 정의하고, 이를 최상위 추상클래스 `AbstractDisjointSet`으로 구성하였다.

상위 계층에서는 실제 그룹 저장 방식이나 Parent 구조의 내부 표현을 알지 않고 논리적인 연산만 사용할 수 있도록 하였다.

---

## 2. Group 기반 / Parent 기반 표현 분리

Union-Find의 저장 표현을 두 가지 관점으로 구분하였다.

### GroupStore

각 원소 `T`가 어떤 Group ID 또는 대표값 `K`에 속하는지를 직접 저장하는 방식.

```text
T → K
```

`get_group()`을 통해 그룹 대표값을 얻고, `merge_group()`을 통해 두 그룹의 대표값을 하나로 통일한다.

### ParentStore

각 원소가 다른 원소를 부모로 가리키는 관계를 이용하여 가상의 forest를 구성하는 방식.

```text
T → parent → parent → ... → root
```

Parent 기반 표현에서는 대표자 자체가 `T`이므로 별도의 `K`가 필요하지 않도록 구성하였다.

---

## 3. Generic과 Identity

자료구조의 실제 값과 그룹 대표값을 분리하기 위해 `T`, `K`를 사용하였다.

```text
T → 실제 원소
K → 그룹 대표값
```

동일성 판단은 특정 타입의 구현에 종속시키지 않고 `Identity`를 외부에서 전달할 수 있도록 구성하였다.

일반적인 자료형에서는 기본적으로:

```python
lambda a, b: a == b
```

를 사용하고, 복합 자료형이나 특수한 동일성 기준이 필요한 경우 외부에서 비교 함수를 주입할 수 있도록 하였다.

---

## 4. Protocol / ABC

인터페이스와 구현 규칙을 분리하기 위해 `Protocol`과 `ABC`를 함께 사용하였다.

```text
Protocol
→ 구조적으로 필요한 기능과 외부 계약 정의

ABC
→ 프로젝트 내부의 추상 계층과 상속 구조 정의
```

이를 통해 구현체가 특정한 저장 표현을 사용하더라도 상위 계층에서는 동일한 인터페이스를 통해 접근할 수 있도록 구성하였다.

---

## 5. ParentStore의 Policy 기반 설계

Parent 기반 Union-Find에서는 Find와 Union에 여러 가지 구현 전략이 존재한다.

```text
Find
├── 기본 Find
└── Path Compression

Union
├── Default
├── Union by Rank
└── Union by Size
```

이를 하나의 concrete class 내부에서 모두 직접 분기하는 대신 **Policy를 교체 가능한 callable로 분리**하였다.

### Policy 구성

정책의 종류는 Enum으로 표현하고, 실제 구현 함수는 별도의 util로 분리하였다.

```text
Enum
  ↓
Policy 선택
  ↓
partial로 구현 함수 결합
  ↓
상위 인터페이스에서 고정된 callable로 사용
```

구체적인 List 기반 구현에서 필요한 `storage`, `metadata`, `identity`, `flag` 등의 인자는 초기화 단계에서 결합하고, 상위 계층에서는 단순화된 형태로 호출하도록 구성하였다.

예를 들어 최종적으로 상위 계층에서는:

```text
get_group(x)
merge_group(a, b)
set_parent(x, parent)
```

와 같은 형태만 사용하고, 실제 List 저장 방식에 필요한 내부 인자는 concrete implementation에 남겨두었다.

---

## 6. List 기반 Parent 구현

`ListBasedParentStore`에서는 실제 저장 표현을 다음과 같이 구체화하였다.

```text
list[tuple[T, T]]
```

각 원소는:

```text
(value, parent)
```

형태로 저장되며, root는 자기 자신을 parent로 가지도록 정의하였다.

예:

```text
(A, A)
(B, A)
(C, B)
(D, C)
```

이 구조는:

```text
A
└── B
    └── C
        └── D
```

라는 논리적 parent tree를 표현한다.

### 공통 List util

저장 구조에 반복적으로 등장하는 위치 탐색을 하나의 util로 분리하였다.

```text
T
↓
list 내부 탐색
↓
정확한 index 반환
```

이를 기반으로:

* parent 변경
* union
* find
* path compression

에서 중복되는 List 탐색 로직을 재사용하였다.

---

## 7. Path Compression과 Union Optimization

Path Compression은 Find 과정에서 탐색한 경로의 parent를 최종 root로 직접 연결하여 이후의 탐색 경로를 단축하는 방식으로 구현하였다.

```text
Before

D → C → B → A


After find(D)

D → A
C → A
B → A
```

Union에서는 Rank 또는 Size metadata를 선택적으로 사용하여 어떤 root를 유지할지 결정할 수 있도록 구성하였다.

### Rank

두 root의 rank가 같은 경우에만 새로운 root의 rank를 1 증가시킨다.

```text
rank(A) > rank(B)
→ B를 A 아래에 연결

rank(A) < rank(B)
→ A를 B 아래에 연결

rank(A) == rank(B)
→ 한쪽을 다른 쪽에 연결
→ 새로운 root의 rank += 1
```

Path Compression이 발생하더라도 rank는 실제 현재 tree height가 아니라 Union 과정에서 축적된 구조적 등급으로 유지한다.

### Size

각 root에 현재 component의 크기를 저장하고, 두 그룹을 병합할 때 크기를 합산한다.

```text
size(new root)
=
size(root A) + size(root B)
```

Rank와 Size는 둘 다 Union 시 root 선택을 위한 보조 metadata이며, 동시에 사용할 필요가 없도록 정책을 분리하였다.

---

# Union-Find Invariants

구현 과정에서 다음과 같은 기본 invariant를 유지하도록 하였다.

1. Union-Find의 연산 대상은 Storage에 등록된 원소로 제한한다.
2. Find와 Union에 전달되는 원소는 Storage에 존재한다고 가정한다.
3. 하나의 원소는 Storage에 중복해서 존재하지 않는다.
4. Parent 기반 표현에서는 각 원소가 하나의 parent만 가진다.
5. 각 connected component는 정확히 하나의 root를 가진다.
6. Root는 자기 자신을 parent로 가진다.
7. Parent 관계에는 cycle이 존재하지 않는다.

이러한 invariant를 먼저 정의하고 구현의 각 단계에서 이를 유지하도록 구성하였다.

---

# Main Design Insight

이번 Union-Find 구현에서 가장 중요한 학습은 하나의 알고리즘을 단순히 구현하는 것이 아니라, **논리적 구조와 물리적 표현을 분리하는 방법**을 확인한 것이다.

```text
Logical Operation
       ↓
Abstract Store
       ↓
Policy / Identity
       ↓
Concrete Storage
       ↓
Actual Data Representation
```

예를 들어 동일한 `Find` / `Union`이라는 논리적 연산도:

```text
Group representation
Parent representation
```

으로 표현할 수 있고, Parent 기반 구현에서는 다시:

```text
List
Array
Dict
Tree
...
```

와 같은 저장 구조로 확장할 수 있다.

또한 Find와 Union을 Policy로 분리하면 동일한 저장 구조에서도:

```text
Default
Rank
Size
Path Compression
```

등의 전략을 독립적으로 조합할 수 있다.

---

# Current Learning Status

현재 Union-Find 학습에서는 다음 내용을 구현 및 정리하였다.

```text
✓ Disjoint Set 기본 개념
✓ Find / Union 최소 인터페이스
✓ Generic T / K
✓ Identity 주입
✓ Protocol / ABC
✓ GroupStore
✓ ParentStore
✓ Storage와 연산의 분리
✓ List 기반 concrete implementation
✓ Parent tree 표현
✓ Path Compression
✓ Union by Rank
✓ Union by Size
✓ Root metadata
✓ Policy 기반 설계
✓ Callable / partial을 이용한 정책 결합
✓ Invariant 정의
✓ 기본 동작 검증
```

이번 단계에서는 특정 구현에 대한 추가적인 일반화보다, 지금까지 구성한 구조를 기준으로 **추상화가 실제 구현에서 어떻게 유지되는지 확인하는 것**에 초점을 두었다.

---

# Learning Direction

이 프로젝트의 목표는 자료구조와 알고리즘의 구현 자체에 머무르지 않는다.

최종적으로는:

```text
문제 정의
→ 가장 단순한 모델
→ 구현
→ 한계와 병목 발견
→ 적절한 추상화
→ 구체 구현
→ 최적화
→ 검증
```

의 과정을 반복하며, **자료구조와 알고리즘을 단순히 사용하는 것이 아니라 어떤 구조가 필요하고 왜 그러한 설계가 효율적인지를 판단할 수 있는 능력**을 기르는 것을 목표로 한다.
