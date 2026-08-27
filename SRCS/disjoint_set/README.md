# Union-Find

## 1. Union-Find의 기본정의와 개념을 학습

---

## 2. 유니온-셋의 기본단위 구축

Union-set의 가장 기본단위는 값에 해당하는 저장체(store)와 기능에 해당하는 서로소시 합치는 연산(Union), 원소의 소속을 찾는(Find)로 나뉘어짐.

따라서 가장 기본단위의 추상클래스를 작성하고 해당추상클래스를 외부에서 제공시 맞추어야할 규칙에 해당하는 프로토콜을 작성.

따라서 최상위계층 `AbstractDisjointSet`이라는 추상인터페이스와, 해당 인터페이스 규격을 맞춰서 타입검사기가 확인가능한 프로토콜 `DisjointSet` 작성.

각각 최소 필요한 함수 `FIND`, `UNION`을 의미있게 명시함. 추가적으로 `AbstractDisjointSet`에서는 Storage의 필요성과 Storage가 지녀야할 protocol타입을 명시적으로 지정해 구현.

---

## 3. Generic T와 K를 사용해 두개의 추상타입을 만듬

이때 `T`는 실제데이터 value를, `K`는 group의 동일성을 검증하는 검증값을 지니게된다.

`T`와 `K`는 실제타입이 변할수있지만 반드시 필요한요소이며 `K`가 일반적으로 기본제공자료형이라면 equality는 `==`로 확인가능할것이다.

하지만 그것이 불가능한 복합구조인경우를 대비해 `Identity`라는 자격기준을 외부에 함수로 받아서 초기화하도록 구현하는것이 필요할수도있다.

따라서 `Identity`를 `Callable`을 이용해서 `K`인자두개의 비교를 수행하며 참거짓을 반환하는 계약으로 규정.

> 기본타입형인 경우에는 생성자에서 identity를 `==` 으로받는 람다식으로, 특수한경우에서는 외부에서 `Identity`를 받아오는식으로 구현.

---

## 4. 기본적인 Union-set 구현

다음단계에서는 Union-set에는 가장 기본적으로 기능에 해당하는 두축 `Union`, `Find`와 속성에 해당하는 `Storage`가 있다.

기본적인 union-set은 가장추상화된 단계에서의 구현이므로:

### Find

해당 인자의 그륩ID 또는 그것에 대응되는 값을 가져오는것이므로 → 단순히 해당인자의 `K`값을 반환하는계약.

(`K`가 어떤구현일지는 상위추상구현체에서 알필요없이 추상화유지)

### Union

이때 `K`값을 `Find`로 가져온후 두개의 `K`값을 비교해 다른경우 한쪽의 그륩을 다른그륩으로 전부 통일하는 추상구조.

### 생성자

그륩의 정체성 `K`값의 동일성을 구분할 `Identity`와 속성값에 해당하는 `Storage`를 추상클래스의 기본값으로 상속.

이때 `Identity`가 비어있는경우 인자차원에서 초기화대신 타입검사기에서 명확성을위해 블록내부에서 `None`시 할당방식.

또한 `Storage`는 실제로 `Find`, `Union`을 구현차원의 Level에 맞는 조건을 만족할수있는 프로토콜로 맞춰 자격을 제한.

 ### union의 invariant 조건

 ### 1. Union-Find의 연산 대상은 Storage에 등록된 원소로 제한한다.(기본 전제)
 ### 2. Find 및 Union에 전달되는 원소는 반드시 Storage에 존재한다고 가정한다. (1에따른 당연한귀결)
 ###    따라서 Storage 조회 결과가 존재하지 않는 경우는 정상적인 연산 범위에 포함하지 않는다. 
 ### 3. Store가 비어 있는 경우 등록된 원소가 존재하지 않으므로 (1에따른 당연한귀결)
 ###    유효한 Find 및 Union 연산의 대상이 존재하지 않는다.


### 5.Union-set이 최상위 단위면 그 하위의 Storage 표현을 ParentStorage와 GroupStorage로 나눔.
### 하나는 Group ID인 K를 이용하여 각 원소의 소속 그룹을 직접 표현하고, 반대로 ParentStorage는 각 원소가 부모를 가리키는 관계를 이용하여 가상의 트리 구조를 표현한다.
### 마찬가지로 Store는 추상클래스 단계의 구성으로, 하위의 GroupStore는 가장 기본적인 틀인 속성 Storage, IdentityOfT, IdentityOfK와 함수 get_group, merge_group을 최소 단위로 가진다.
### 반면 ParentStore는 K를 별도로 두지 않고 원소 T 자체를 parent 및 representative로 사용하므로 Generic[T]만으로 구성할 수 있으며, 추가적으로 Storage, IdentityOfT, GetGroupPolicy, UnionPolicy, SetParent를 가진다. 여기서 get_group은 parent를 따라가 최종 root를 반환하고, merge_group은 두 root를 결합하며, set_parent는 실제 parent 관계를 변경하는 역할을 담당한다.

### 6. 실제 ListBased 저장소는 선택한 구체적인 데이터 표현에 맞춰 구현을 닫는다.
### ListBasedGroupStore는 list[tuple[T,K]]와 같이 실제 저장 형식을 명시하고, 해당 표현에 맞는 get_group과 merge_group을 각각 하나의 구체적인 동작으로 구현하여 상위 GroupStore의 계약을 만족시킨다.
### 반면 ListBasedParentStore는 list[tuple[T,T]]와 같이 parent 관계를 리스트로 표현하며, Union에서는 DEFAULT, RANK, SIZE, Find에서는 기본 탐색과 PATH_COMPRESSION과 같이 여러 전략이 존재할 수 있으므로 이를 Policy로 분리한다.
### 이때 구체적인 List 표현에 종속된 공통 구현은 util 함수로 작성하고, Enum 또는 flag로 선택된 정책과 partial을 이용해 storage, metadata, identity 등의 구현 세부 인자를 사전에 결합한다. 그 결과 상위 추상화 계층에서는 get_group(x), merge_group(a,b), set_parent(x,parent)와 같이 고정된 callable 계약만 사용하면서도, 실제 List 구현에서는 필요한 전략을 독립적으로 선택하고 조합할 수 있도록 한다.