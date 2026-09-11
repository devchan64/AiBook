# P2-9.1 자료구조 선택(data structure)는 왜 필요한가

> Section ID: `P2-9.1`
> Version: `v2026.09.08`

## 데이터 조직과 연산

자료구조(data structure)는 데이터를 조직하는 방식입니다. NIST는 알고리즘의 효율성을 위해 정보를 조직한다는 관점으로 정의합니다. 같은 학생 정보도 전체 점수를 계산할지, 특정 학생을 찾을지, 친구 관계를 따라갈지에 따라 표현이 달라집니다.

| 자료구조 감각 | 중심 질문 | 예시 |
| --- | --- | --- |
| 순서 | 몇 번째 값인가? | 리스트(list) |
| 이름표 | 어떤 키로 찾는가? | 딕셔너리(dictionary) |
| 포함 여부 | 들어 있는가? | 집합(set) |
| 계층 | 상위와 하위가 있는가? | 트리(tree) |
| 관계 | 무엇과 무엇이 연결되는가? | 그래프(graph) |

자료구조 선택에는 자주 수행할 연산(operation)이 중요합니다. 연산에는 검색, 추가, 삭제, 전체 항목을 방문하는 순회(traversal) 등이 있습니다.

## 순서·계층·키 기반 구조

| 전통적 자료구조 | 입문용 질문 | 직관 |
| --- | --- | --- |
| 배열(array) | 같은 종류의 값을 연속된 위치로 다룰 것인가? | 번호가 붙은 칸 |
| 연결 리스트(linked list) | 값들이 다음 값을 가리키게 할 것인가? | 고리로 이어진 항목 |
| 스택(stack) | 마지막에 넣은 것을 먼저 꺼낼 것인가? | 접시 쌓기 |
| 큐(queue) | 먼저 들어온 것을 먼저 꺼낼 것인가? | 줄 서기 |
| 트리(tree) | 부모와 자식 관계가 있는가? | 폴더 구조 |
| 그래프(graph) | 여러 대상이 서로 연결되는가? | 관계망 |
| 해시 테이블(hash table) | 키로 값을 빠르게 찾을 것인가? | 이름표로 찾는 보관함 |

이 구조들은 다시 크게 선형(linear) 구조와 비선형(non-linear) 구조로 나누어 볼 수 있습니다.

선형 구조(linear structure)는 데이터가 한 줄의 순서로 이어지는 구조입니다. 배열, 리스트, 스택, 큐가 여기에 가깝습니다.

비선형 구조(non-linear structure)는 데이터가 한 줄로만 이어지지 않는 구조입니다. 트리와 그래프가 대표적입니다. 트리는 계층을 표현하고, 그래프는 여러 방향의 관계를 표현합니다.

| 구분 | 특징 | 예시 |
| --- | --- | --- |
| 선형 구조(linear structure) | 앞뒤 순서가 중요함 | 배열, 연결 리스트, 스택, 큐 |
| 비선형 구조(non-linear structure) | 계층이나 관계가 중요함 | 트리, 그래프 |
| 키 기반 구조(key-based structure) | 키로 값을 찾는 일이 중요함 | 딕셔너리, 해시 테이블 |

분류 기준은 서로 겹칠 수 있습니다. Python 딕셔너리는 키 기반 매핑(mapping)이며 삽입 순서도 보존합니다. 그래프를 딕셔너리와 리스트의 조합으로 표현할 수도 있습니다.

## 추상 자료형과 구현

추상 자료형(abstract data type, ADT)은 어떤 값과 연산이 가능한지를 설명하는 개념입니다.

구현(implementation)은 그 개념을 실제 메모리와 코드에서 어떻게 만들었는지를 말합니다.

예를 들어 스택(stack)은 마지막에 넣은 것을 먼저 꺼내는 구조로 설명할 수 있습니다. 이것은 동작 규칙입니다.

- `push`: 값을 넣는다.
- `pop`: 가장 나중에 넣은 값을 꺼낸다.
- 마지막에 넣은 값이 먼저 나온다.

하지만 이 스택은 내부적으로 리스트로 만들 수도 있고, 연결 리스트(linked list)로 만들 수도 있습니다. 같은 추상 자료형을 여러 방식으로 구현할 수 있습니다.

이 구분은 Python을 읽을 때도 중요합니다.

| 관점 | 질문 | 예시 |
| --- | --- | --- |
| 추상 자료형(ADT) | 어떤 동작을 약속하는가? | 스택은 마지막에 넣은 값을 먼저 꺼낸다 |
| 구현(implementation) | 실제로 어떻게 저장하는가? | 리스트로 구현할 수도 있고 연결 구조로 구현할 수도 있다 |
| Python 사용 관점 | 어떤 객체와 메서드로 제공되는가? | `list.append()`, `list.pop()` |

스택에 `A`를 넣고 `B`를 넣은 뒤 한 번 꺼내면 `B`가 나와야 합니다. Python 리스트로 구현한다면 `append("A")`, `append("B")`, `pop()`을 사용할 수 있습니다. 저장 방식을 바꾸더라도 이 꺼내기 규칙은 유지해야 같은 스택 동작입니다.

## 순회·조회·관계 표현

학생 Kim, Lee, Park의 점수는 각각 82, 75, 91입니다. 점수 조회와 친구 관계 표현에 필요한 정보를 서로 다른 구조로 담을 수 있습니다.

### 전체 순회

학생별 딕셔너리를 리스트에 담으면 전체를 순회할 수 있습니다. 다음 코드는 `Kim 82`, `Lee 75`, `Park 91`을 차례로 출력합니다.

```python
students = [
    {"name": "Kim", "score": 82},
    {"name": "Lee", "score": 75},
    {"name": "Park", "score": 91},
]

for student in students:
    print(student["name"], student["score"])
```

세 점수의 합계는 248이고 평균은 약 82.67입니다. 평균에는 전체 점수가 필요하므로 특정 이름 하나를 찾는 조회와 달리 전체 항목을 대상으로 계산합니다.

### 이름 조회

이름을 키로 사용하면 특정 학생의 점수에 바로 접근할 수 있습니다. 아래에서 `student_by_name["Kim"]["score"]`의 출력은 `82`입니다.

```python
student_by_name = {
    "Kim": {"score": 82},
    "Lee": {"score": 75},
    "Park": {"score": 91},
}

print(student_by_name["Kim"]["score"])
```

이 구조는 이름으로 특정 학생을 찾기 좋습니다.

### 친구 관계

친구 관계는 각 학생 이름에 연결된 친구 목록으로 표현할 수 있습니다. 아래에서 Kim의 친구 목록은 `['Lee', 'Park']`입니다.

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim"],
    "Park": ["Kim"],
}

print(friends["Kim"])
```

학생을 대상, 친구 사이를 연결로 표현한 그래프입니다. 예제에서는 서로 친구인 관계를 양쪽 목록에 모두 기록했습니다. Kim과 Lee의 관계를 없애려면 Kim 목록의 `"Lee"`와 Lee 목록의 `"Kim"`을 함께 지워야 합니다.

같은 사람 데이터라도 목적이 다르면 구조가 달라집니다. 이것이 자료구조가 필요한 이유입니다.

## AI 데이터의 구조

문장 입력, 라벨 대응표, 문서 연결은 서로 다른 조회와 처리를 요구합니다.

| AI 실습 상황 | 자주 보이는 구조 | 읽는 관점 |
| --- | --- | --- |
| 여러 문장 입력 | 리스트(list) | 문장을 하나씩 처리 |
| 라벨 번호와 이름 연결 | 딕셔너리(dictionary) | 키로 라벨 이름 찾기 |
| 중복 토큰 확인 | 집합(set) | 들어 있는지 확인 |
| 표 형식 데이터 | 테이블(table), DataFrame | 행과 열로 접근 |
| 문장 안의 토큰 흐름 | 시퀀스(sequence) | 순서대로 처리 |
| 문서와 문서의 연결 | 그래프(graph) | 관계를 따라 이동 |

## 사례: 동명이인의 점수

이름이 같은 학생 두 명의 점수가 `82`, `91`이라고 하겠습니다. 리스트는 두 기록을 모두 보관하지만, 이름을 딕셔너리 키로 사용하면 뒤의 점수가 앞의 점수를 덮어씁니다. 다음 코드는 두 기록과 `{'Kim': 91}`을 차례로 출력합니다.

```python
students = [
    {"id": "s001", "name": "Kim", "score": 82},
    {"id": "s002", "name": "Kim", "score": 91},
]
score_by_name = {}

for student in students:
    score_by_name[student["name"]] = student["score"]

print(students)
print(score_by_name)
```

키로 무엇을 고르는지는 보존할 정보와 연결됩니다. 각 학생의 고유 ID를 키로 사용하면 두 점수를 구분할 수 있습니다. 같은 입력으로 다음 코드를 실행하면 `{'s001': 82, 's002': 91}`이 출력됩니다.

```python
students = [
    {"id": "s001", "name": "Kim", "score": 82},
    {"id": "s002", "name": "Kim", "score": 91},
]
score_by_id = {}

for student in students:
    score_by_id[student["id"]] = student["score"]

print(score_by_id)
```

두 번째 학생의 ID를 `"s001"`로 바꾸면 다시 하나의 키만 남습니다. 조회가 짧아지는 것뿐 아니라 키가 실제로 학생을 구별하는지도 확인해야 합니다. 이름별로 여러 점수를 모으려는 목적이라면 딕셔너리 값에 점수 리스트를 둘 수 있습니다.

## 체크리스트

- 자료구조(data structure)를 데이터를 조직하는 방식으로 설명할 수 있다.
- 전통적 자료구조 개론에서 배열, 연결 리스트, 스택, 큐, 트리, 그래프, 해시 테이블이 어떤 질문을 대표하는지 설명할 수 있다.
- 선형 구조와 비선형 구조의 차이를 입문 수준에서 설명할 수 있다.
- 자료구조가 검색, 추가, 삭제, 순회 같은 연산과 연결됨을 설명할 수 있다.
- 같은 데이터도 순서, 키, 관계에 따라 다른 구조로 표현될 수 있음을 설명할 수 있다.
- 추상 자료형(ADT)과 구현(implementation)을 입문 수준에서 구분할 수 있다.
- AI 실습에서 리스트, 딕셔너리, 집합, 표, 그래프가 서로 다른 질문에 답하기 위한 구조임을 설명할 수 있다.
- 데이터를 그냥 모아 두는 것이 아니라 어떤 질문에 답하게 만들 것인지와 자료구조 선택을 연결할 수 있다.

## 출처와 참고 자료

- Paul E. Black, [data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, 확인 날짜: 2026-07-20. 자료구조를 데이터를 조직하는 방식으로 설명하는 정의 확인에 사용했다.
- Paul E. Black, [abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, 확인 날짜: 2026-07-20. 추상 자료형을 구현보다 동작 관점의 틀로 구분하는 근거로 사용했다.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python 리스트와 딕셔너리 예시를 자료구조 선택 설명에 연결하는 근거로 사용했다.
