# P2-9.4 보충학습: 전통적인 자료구조를 처음 읽는 법

> Section ID: `P2-9.4`
> Version: `v2026.09.08`

배열은 위치로 값을 찾고, 연결 리스트는 다음 항목을 가리키는 연결을 따라갑니다. 스택과 큐는 넣고 꺼내는 순서를 정하며, 트리와 그래프는 대상 사이의 관계를 표현합니다. 자료구조 이름은 저장 방식이나 연산 규칙을 구분합니다.

| 자료구조 | 주요 특성 | 사용 예 |
| --- | --- | --- |
| 배열(array) | 인덱스로 항목 접근 | 벡터, 이미지 픽셀 |
| 연결 리스트(linked list) | 노드의 연결로 순서 표현 | 항목 사이 연결 변경 |
| 스택(stack) | 마지막 입력을 먼저 꺼냄 | 실행 취소, 함수 호출 |
| 큐(queue) | 첫 입력을 먼저 꺼냄 | 작업 대기열 |
| 트리(tree) | 부모와 자식의 계층 | 목차, 분류 체계 |
| 그래프(graph) | 노드 사이 연결 | 친구 관계, 문서 링크 |
| 해시 테이블(hash table) | 해시를 이용한 키 조회 | ID 조회, 단어별 개수 |

스택과 큐의 꺼내기 규칙은 추상 자료형(abstract data type)의 동작입니다. 이를 실제로 저장하고 실행하는 구현(implementation)은 달라질 수 있습니다. Python 리스트의 끝에 넣고 끝에서 꺼내면 스택으로 사용할 수 있습니다.

## 배열과 위치 접근

배열은 위치(index)를 기준으로 값을 읽습니다. `[10, 20, 30, 40]`의 인덱스 2에 있는 값은 `30`입니다. 이미지 픽셀이나 벡터에서는 값의 위치를 바꾸면 계산 대상의 의미도 달라질 수 있습니다.

Python 리스트도 인덱스를 사용합니다. 다음 코드는 첫 값 `10`, 세 번째 값 `30`을 출력하고, 두 번째 값을 `25`로 바꾼 `[10, 25, 30, 40]`을 출력합니다.

```python
values = [10, 20, 30, 40]

print(values[0])
print(values[2])

values[1] = 25
print(values)
```

Python 리스트는 객체 참조를 담으며 길이를 바꿀 수 있습니다. NumPy 배열은 하나의 dtype으로 항목을 해석하는 수치 계산 구조입니다. 두 구조 모두 위치 접근을 제공하지만 같은 자료형은 아닙니다.

## 연결 리스트와 다음 노드

단일 연결 리스트는 각 노드(node)에 값과 다음 노드를 가리키는 연결(link)을 둡니다. 마지막 노드의 다음 연결은 끝을 나타냅니다.

```text
Kim → Lee → Park → None
```

다음 코드는 딕셔너리 세 개를 노드로 사용합니다. `next`에 다음 노드의 참조를 저장하고, 첫 노드에서 시작해 `Kim`, `Lee`, `Park`를 차례로 출력합니다.

```python
third = {"value": "Park", "next": None}
second = {"value": "Lee", "next": third}
first = {"value": "Kim", "next": second}

node = first
while node is not None:
    print(node["value"])
    node = node["next"]
```

`while node is not None`은 현재 노드가 있는 동안 들여쓴 코드를 반복합니다. `node = node["next"]`가 다음 노드로 이동하고, 마지막 `None`을 만나면 멈춥니다.

노드를 만드는 세 줄 다음에 `first["next"] = third`를 넣으면 출력은 `Kim`, `Park`가 됩니다. Lee 노드는 여전히 존재하지만 첫 노드에서 따라가는 연결에서는 빠집니다. 이처럼 논리적 순서는 노드 사이의 연결로 정해집니다.

## 스택: 마지막 입력부터

스택(stack)은 마지막에 넣은 항목을 먼저 꺼내는 LIFO(last in, first out) 규칙을 따릅니다. 접시를 쌓은 뒤 맨 위 접시부터 꺼내는 순서와 같습니다.

리스트 끝에 A, B, C를 넣은 뒤 두 번 꺼내면 C와 B가 나오고 A가 남습니다. `append()`는 끝에 넣고, 인자 없는 `pop()`은 끝에서 꺼냅니다.

```python
stack = []

stack.append("A")
stack.append("B")
stack.append("C")

print(stack.pop())
print(stack.pop())
print(stack)
```

출력은 `C`, `B`, `['A']`입니다. 편집 작업 A, B, C를 차례로 수행했다면 실행 취소도 C, B 순으로 적용할 수 있습니다. 함수 호출에서도 나중에 들어간 호출이 먼저 끝나는 구조를 호출 스택(call stack)이라고 부릅니다.

## 큐: 첫 입력부터

큐(queue)는 먼저 들어온 항목을 먼저 꺼내는 FIFO(first in, first out) 규칙을 따릅니다. `collections.deque`는 양쪽 끝에서 넣고 뺄 수 있는 덱(deque)이며, 뒤에 넣고 앞에서 꺼내면 큐로 사용할 수 있습니다.

다음 코드는 A, B, C를 순서대로 넣고 앞에서 두 번 꺼냅니다. 출력은 `A`, `B`, `deque(['C'])`입니다.

```python
from collections import deque

queue = deque()

queue.append("A")
queue.append("B")
queue.append("C")

print(queue.popleft())
print(queue.popleft())
print(queue)
```

`append()`는 뒤에 추가하고 `popleft()`는 앞에서 꺼냅니다. 작업 대기열에 요청 A, B, C가 들어왔을 때 이 규칙을 사용하면 A부터 처리 대상으로 꺼냅니다. 여러 작업을 동시에 실행하는 서비스에서는 꺼낸 순서와 완료 순서가 달라질 수 있습니다.

## 트리: 부모와 자식

루트를 정한 트리는 루트 이외의 각 노드가 하나의 부모를 갖는 계층입니다. 목차에서는 책 아래 Part, Part 아래 Chapter를 놓을 수 있습니다.

다음 코드는 책 제목과 두 Part, 각 Part의 Chapter를 출력합니다. 바깥 반복은 Part를, 안쪽 반복은 해당 Part의 Chapter를 읽습니다.

```python
book = {
    "title": "study-book",
    "children": [
        {
            "title": "Part 1",
            "children": ["Chapter 1", "Chapter 2"],
        },
        {
            "title": "Part 2",
            "children": ["Chapter 8", "Chapter 9"],
        },
    ],
}

print(book["title"])
for part in book["children"]:
    print("-", part["title"])
    for chapter in part["children"]:
        print("  -", chapter)
```

```text
study-book
- Part 1
  - Chapter 1
  - Chapter 2
- Part 2
  - Chapter 8
  - Chapter 9
```

`Chapter 9`의 경로는 `study-book → Part 2 → Chapter 9`입니다. 부모와 자식의 연결을 따라 소속을 확인합니다.

## 그래프: 대상 사이의 연결

그래프(graph)는 노드(node)와 엣지(edge)로 연결 관계를 표현합니다. 트리는 순환 없이 연결된 그래프의 한 종류입니다. 일반 그래프는 순환이나 여러 경로도 표현할 수 있습니다.

다음 친구 관계에서 Kim의 직접 이웃은 Lee와 Park입니다. 코드의 첫 출력은 `['Lee', 'Park']`이고, 이어서 `Kim is connected to Lee`, `Kim is connected to Park`가 출력됩니다.

```python
graph = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim", "Choi"],
    "Park": ["Kim"],
    "Choi": ["Lee"],
}

print(graph["Kim"])

for friend in graph["Kim"]:
    print("Kim is connected to", friend)
```

Choi는 Kim의 직접 이웃은 아니지만 `Kim → Lee → Choi`로 연결됩니다. 사람을 소속별로 묶는 목차형 계층과 달리, 이 관계에서는 친구 연결을 따라 이동합니다.

## 해시 테이블과 키 조회

해시 테이블은 키의 해시값(hash value)을 이용해 저장 위치를 정하고 값을 찾는 구조입니다. 서로 다른 키가 같은 위치에 대응하는 충돌(collision)이 생길 수 있으므로 이를 처리하는 규칙도 필요합니다.

Python 딕셔너리는 키와 값을 연결하는 매핑(mapping)이며 해시 기반 조회를 사용합니다. 다음 코드는 `"Kim"`의 점수 `82`를 출력한 뒤 `"Choi": 88`을 추가합니다.

```python
score_by_name = {
    "Kim": 82,
    "Lee": 75,
    "Park": 91,
}

print(score_by_name["Kim"])

score_by_name["Choi"] = 88
print(score_by_name)
```

두 번째 출력은 `{'Kim': 82, 'Lee': 75, 'Park': 91, 'Choi': 88}`입니다. 딕셔너리 사용법인 `score_by_name["Kim"]`과 내부에서 저장 위치를 찾는 해시 테이블 구현은 서로 다른 설명 수준입니다.

## 사례: 대기열과 실행 취소

요청 A, B, C가 들어온 순서대로 실행하려면 큐에서 A를 먼저 꺼냅니다. 이미 수행한 작업 A, B, C를 되돌리려면 스택에서 C를 먼저 꺼냅니다. 같은 항목을 담아도 꺼내는 규칙이 목적에 따라 다릅니다.

| 입력 순서 | 스택에서 두 번 꺼내기 | 큐에서 두 번 꺼내기 |
| --- | --- | --- |
| A, B, C | C, B | A, B |
| A, B, C, D | D, C | A, B |

앞 스택과 큐 코드에서 `append("C")` 다음에 `append("D")`를 추가하면 두 번째 행의 결과를 확인할 수 있습니다. 스택에는 `['A', 'B']`, 큐에는 `deque(['C', 'D'])`가 남습니다. 입력 순서만 같다고 처리 순서까지 같아지는 것은 아닙니다.

## AI 작업과 자료구조

| 작업 | 필요한 특성 | 구조 예시 |
| --- | --- | --- |
| 토큰 순서 유지 | 위치와 순서 | 배열, 시퀀스 |
| 라벨 번호로 이름 조회 | 키와 값의 대응 | 딕셔너리 |
| 단어 중복 제거 | 원소의 포함 여부 | 집합 |
| 문서 링크 탐색 | 연결과 경로 | 그래프 |
| 요청을 들어온 순서로 꺼내기 | FIFO | 큐 |
| 문서의 상위 제목 찾기 | 부모와 자식 | 트리 |

## 체크리스트

- 배열(array)을 위치(index)로 값을 다루는 구조로 설명할 수 있다.
- 연결 리스트(linked list)를 항목이 다음 항목을 가리키는 구조로 설명할 수 있다.
- 스택(stack)을 LIFO, 큐(queue)를 FIFO 규칙으로 설명할 수 있다.
- 트리(tree)를 계층 구조, 그래프(graph)를 관계 구조로 구분할 수 있다.
- 딕셔너리(dictionary)와 해시 테이블(hash table)이 키 기반 검색과 연결됨을 설명할 수 있다.
- Python의 편리한 문법 뒤에도 전통 자료구조 감각이 숨어 있음을 설명할 수 있다.
- 배열, 연결 리스트, 스택, 큐, 트리, 그래프, 딕셔너리 예제를 Python으로 실행해 보고 출력 흐름을 설명할 수 있다.

## 출처와 참고 자료

- NIST, [Data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, 확인 날짜: 2026-07-20. 전통 자료구조 이름을 데이터 조직 방식으로 읽는 기본 정의 확인에 사용했다.
- NIST, [Abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, 확인 날짜: 2026-07-20. 스택·큐 같은 구조를 구현보다 제공 동작 중심으로 설명하는 근거로 사용했다.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python 리스트와 딕셔너리 문법이 전통 자료구조 감각과 어떻게 연결되는지 확인하는 근거로 사용했다.
