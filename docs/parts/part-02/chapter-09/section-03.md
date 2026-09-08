# P2-9.3 그래프(graph)는 관계를 어떻게 표현하는가

> Section ID: `P2-9.3`
> Version: `v2026.09.08`

## 노드와 엣지

NIST Dictionary of Algorithms and Data Structures는 그래프를 엣지(edge)로 연결된 항목들의 집합으로 설명하고, 각 항목을 정점(vertex) 또는 노드(node)라고 설명합니다.

그래프는 대상을 노드로 놓고, 대상 사이의 관계를 엣지로 연결한 구조입니다.

아래 도식은 같은 그래프를 그림과 인접 리스트(adjacency list)로 함께 보여 줍니다.

![A graph can be shown as nodes and edges or as an adjacency list](../../../assets/part-02/chapter-09/graph-node-edge-adjacency-ko.svg)

그림에서 `Kim`, `Lee`, `Park`, `Choi`는 노드입니다.

`Kim -- Lee`처럼 두 노드를 잇는 선은 엣지입니다.

같은 관계는 노드별 이웃 목록으로도 적을 수 있습니다.

| 노드 | 이웃 목록 |
| --- | --- |
| Kim | Lee, Park |
| Lee | Kim, Park |
| Park | Kim, Lee, Choi |
| Choi | Park |

이 표현을 인접 리스트(adjacency list)라고 볼 수 있습니다. 핵심은 노드마다 연결된 이웃 목록을 갖는다는 점입니다.

## 관계 행과 이웃 목록

같은 친구 데이터를 표로 적을 수도 있습니다. 표는 “관계 한 건”을 한 행(row)으로 적기에 좋습니다.

| person | friend |
| --- | --- |
| Kim | Lee |
| Kim | Park |
| Lee | Park |
| Park | Choi |

하지만 “Kim과 연결된 사람은 누구인가?”, “Park를 거쳐 Choi로 갈 수 있는가?”처럼 연결을 따라가야 하는 질문에서는 그래프 관점이 더 자연스럽습니다.

아래 도식은 같은 관계 데이터를 표로 읽을 때와 그래프로 읽을 때 질문이 어떻게 달라지는지 보여 줍니다.

![The same relationship records can be read as a table or a graph](../../../assets/part-02/chapter-09/table-to-graph-reading-ko.svg)

표 데이터를 그래프 관점으로 읽으려면 관계 행을 노드별 이웃 목록으로 다시 묶어 보면 됩니다.

## NetworkX로 이웃 조회

NetworkX는 노드와 엣지로 그래프를 만들고 이웃과 경로를 조회하는 Python 라이브러리입니다. 다음 코드는 위의 친구 관계 네 개와 페이지 링크 세 개를 입력합니다. Kim의 직접 이웃은 Lee와 Park이고, 최단 경로가 두 단계인 이웃은 Choi입니다. 페이지 링크에서는 `page_b`가 `page_c`를 가리키지만 반대 링크는 없습니다.

```python
# weight는 예시용 관계 강도이며, 아래 단계 수 계산에는 사용하지 않습니다.
import networkx as nx

friend_relationships = [
    ("Kim", "Lee", {"weight": 1.0}),
    ("Kim", "Park", {"weight": 0.9}),
    ("Lee", "Park", {"weight": 0.8}),
    ("Park", "Choi", {"weight": 0.7}),
]

friend_graph = nx.Graph()
friend_graph.add_edges_from(friend_relationships)

friend_edges = sorted(tuple(sorted(edge)) for edge in friend_graph.edges())
distances = nx.single_source_shortest_path_length(friend_graph, "Kim", cutoff=2)
two_hop_neighbors = sorted(
    node for node, distance in distances.items() if distance == 2
)

print("friend nodes:", sorted(friend_graph.nodes()))
print("friend edges:", friend_edges)
print("Kim neighbors:", sorted(friend_graph.neighbors("Kim")))
print("Kim two-hop neighbors:", two_hop_neighbors)
print("Kim-Park weight:", friend_graph["Kim"]["Park"]["weight"])

page_graph = nx.DiGraph()
page_graph.add_edge("page_a", "page_b")
page_graph.add_edge("page_a", "page_c")
page_graph.add_edge("page_b", "page_c")

print("page_b links to:", list(page_graph.successors("page_b")))
print("page_c links back to page_b:", page_graph.has_edge("page_c", "page_b"))
```

예상 출력은 다음과 같습니다.

```text
friend nodes: ['Choi', 'Kim', 'Lee', 'Park']
friend edges: [('Choi', 'Park'), ('Kim', 'Lee'), ('Kim', 'Park'), ('Lee', 'Park')]
Kim neighbors: ['Lee', 'Park']
Kim two-hop neighbors: ['Choi']
Kim-Park weight: 0.9
page_b links to: ['page_c']
page_c links back to page_b: False
```

`nx.Graph()`는 친구 관계처럼 양쪽으로 읽는 연결을 만들고, `nx.DiGraph()`는 웹 링크처럼 한쪽 방향으로만 읽는 연결을 만듭니다. `neighbors()`는 한 노드의 직접 이웃을 찾고, `single_source_shortest_path_length()`는 시작 노드에서 몇 단계 떨어져 있는지 계산합니다. 이 코드의 `weight`는 예시로 정한 관계 강도입니다. 단계 수를 계산하는 함수는 가중치를 사용하지 않고 엣지 하나를 한 단계로 셉니다.

## 트리와 순환

트리(tree)는 그래프의 특수한 형태로 설명할 수 있습니다. NIST의 그래프 설명도 트리를 그래프의 한 종류로 언급합니다.

여기서는 다음처럼 구분합니다.

무방향 그래프에서 트리는 모든 노드가 연결되어 있고 순환이 없는 구조입니다. 루트를 정하면 부모와 자식의 계층으로 읽을 수 있습니다.

예를 들어 책 목차는 보통 트리로 읽기 좋습니다.

```text
study-book
└─ Part 2
   └─ Chapter 9
      └─ Section 9.3
```

하지만 사람 사이의 관계는 트리로 정리하기 어렵습니다.

```text
Kim -- Lee
Kim -- Park
Lee -- Park
Park -- Choi
```

이 친구 관계에는 `Kim → Lee → Park → Kim`처럼 같은 노드로 돌아오는 순환이 있습니다. 따라서 이 그래프는 트리가 아닙니다.

## 연결의 방향

그래프의 엣지는 방향이 없을 수도 있고, 방향이 있을 수도 있습니다.

무방향 그래프(undirected graph)는 관계가 양쪽으로 같은 의미를 갖는 경우에 사용합니다.

친구 관계를 단순하게 볼 때는 `Kim -- Lee`라고 표현할 수 있습니다. Kim이 Lee와 친구라면 Lee도 Kim과 친구라고 보는 방식입니다.

무방향 그래프에서는 같은 연결을 양쪽 노드에서 모두 읽을 수 있어야 합니다.

| 노드 | 이웃 |
| --- | --- |
| Kim | Lee |
| Lee | Kim |

방향 그래프(directed graph)는 관계의 방향이 중요한 경우에 사용합니다.

예를 들어 웹 링크는 방향이 있습니다. A 문서가 B 문서로 링크한다고 해서 B 문서가 A 문서로 링크하는 것은 아닙니다.

방향 그래프에서는 연결이 향하는 쪽만 적습니다.

| 출발 노드 | 향하는 노드 |
| --- | --- |
| page_a | page_b, page_c |
| page_b | page_c |
| page_c | 없음 |

AI와 검색 문맥에서는 방향이 중요할 때가 많습니다. 문서가 다른 문서를 인용하거나, 작업 흐름이 다음 단계로 넘어가거나, 사용자가 항목을 클릭하는 흐름은 방향 그래프로 볼 수 있습니다.

아래 도식은 방향과 가중치가 엣지의 의미를 어떻게 바꾸는지 보여 줍니다.

![Direction and weight change what a graph edge means](../../../assets/part-02/chapter-09/directed-weighted-graph-ko.svg)

방향 그래프를 읽을 때는 양쪽에 모두 관계가 있다고 가정하지 않습니다. 관계가 실제로 향하는 쪽만 읽습니다.

| 질문 | 답 |
| --- | --- |
| `page_b`가 가리키는 다음 페이지는 무엇인가 | `page_c` |
| `page_c`가 다시 `page_b`를 가리키는가 | 이 표만으로는 아니오 |

이 예제에서 `page_b`는 `page_c`로 링크하지만, `page_c`가 다시 `page_b`로 링크한다고 말할 수는 없습니다.

## 가중치의 의미

모든 연결이 같은 강도를 갖지는 않습니다. 어떤 관계는 가깝고, 어떤 관계는 멀고, 어떤 관계는 비용이 큽니다.

이때 엣지에 숫자를 붙일 수 있습니다. 이것을 가중치(weight)라고 부릅니다.

예를 들어 지점 A, B, C 사이의 이동 비용을 다음과 같이 가정할 수 있습니다. 숫자는 실제 지역의 거리가 아닌 비교용 비용입니다.

| 출발 노드 | 도착 노드 | 가중치 |
| --- | --- | ---: |
| A | B | 160 |
| A | C | 325 |
| B | C | 200 |

A에서 C로 바로 가는 비용은 325이고, B를 거치는 비용은 160 + 200 = 360입니다. 비용을 최소화한다면 직접 연결을 고릅니다. A–C 비용을 400으로 바꾸면 B를 거치는 경로가 더 저렴합니다.

가중치가 유사도(similarity)라면 큰 값이 더 가까운 관계를 뜻할 수 있습니다. 비용인지 유사도인지에 따라 좋은 값의 방향도 달라집니다.

가중치가 붙으면 “연결되어 있는가”에서 끝나지 않고 “얼마나 가까운가”, “얼마나 비용이 드는가”, “얼마나 강하게 관련되는가”를 물을 수 있습니다.

검색 후보나 추천 후보 사이의 관계 점수를 읽을 때도 같은 관점을 적용할 수 있습니다. 아래 장면은 이미 계산된 관계 점수를 기준선과 비교해 해석하는 예시입니다.

| 후보 문서 | 질의와의 관계 점수 | 기준 `0.7`과 비교 | 해석 |
| --- | ---: | --- | --- |
| `doc_a` | 0.91 | 기준 이상 | 먼저 살펴볼 강한 후보 |
| `doc_b` | 0.72 | 기준 이상 | 함께 살펴볼 후보 |
| `doc_c` | 0.18 | 기준 미만 | 현재 기준에서는 뒤로 미룰 후보 |

기준을 `0.8`로 올리면 `doc_b`의 0.72는 기준 미만이 되고 `doc_a`만 남습니다. 관계 점수는 후보 선택에 사용하는 값이며, 문서 내용이 정확하다는 보증은 아닙니다.

## 직접 이웃과 두 단계 이웃

시작 노드를 Kim으로 두고 최단 경로의 엣지 수로 거리를 셉니다. 직접 이웃과 최단 거리가 두 단계인 노드는 다음과 같습니다.

| 기준 | 포함되는 노드 | 읽는 방법 |
| --- | --- | --- |
| 직접 이웃 | Lee, Park | Kim과 바로 연결된 노드 |
| 두 단계 후보 | Choi | Kim → Park → Choi로 이동하며 최단 거리가 2인 노드 |

아래 도식은 Kim을 기준으로 직접 이웃과 두 단계 이웃을 구분해 보여 줍니다.

![A graph distinguishes direct neighbors and two-hop neighbors](../../../assets/part-02/chapter-09/graph-neighbor-hop-ko.svg)

Lee도 Kim → Park → Lee로 두 단계를 걸어 도달할 수 있지만, Kim과 직접 연결되어 최단 거리는 1입니다. 따라서 앞 코드의 두 단계 이웃에는 포함되지 않습니다.

## AI에서의 관계 표현

| 장면 | 그래프 관점 |
| --- | --- |
| 지식 그래프(knowledge graph) | 개념, 사람, 장소, 사건을 노드로 두고 관계를 엣지로 표현 |
| 추천 시스템(recommender system) | 사용자와 항목, 항목과 항목의 연결을 표현 |
| 검색(search) | 문서, 링크, 키워드, 출처 사이의 연결을 표현 |
| RAG | 문서 조각, 메타데이터, 출처, 질문 사이의 관계를 표현 |
| 워크플로우(workflow) | 작업 단계와 다음 단계의 연결을 표현 |

## 사례: 친구 관계 하나를 추가하면

앞 NetworkX 예제에서 Kim과 Choi 사이에 직접 연결을 추가한다고 하겠습니다. `friend_graph.add_edges_from(friend_relationships)` 바로 아래에 `friend_graph.add_edge("Kim", "Choi", weight=0.6)`를 넣고 다시 실행합니다.

Kim의 직접 이웃은 `['Choi', 'Lee', 'Park']`로 늘고, 최단 거리가 두 단계인 이웃은 `[]`가 됩니다. Choi까지의 거리가 2에서 1로 줄었기 때문입니다. 연결 강도 `0.6`은 이 단계 수 계산에 사용되지 않습니다.

추가한 줄을 제거한 뒤 기존 `("Park", "Choi", {"weight": 0.7})` 관계만 삭제하면 Choi는 입력 엣지에서 완전히 사라집니다. 코드가 엣지에서 노드를 생성하므로 노드 목록도 `['Kim', 'Lee', 'Park']`가 됩니다. 연결 없는 Choi도 보관하려면 그래프 생성 후 `friend_graph.add_node("Choi")`로 노드를 명시해야 합니다. 그러면 Choi는 노드 목록에 있지만 Kim에서는 도달할 수 없습니다.

그림에서 노드의 배치를 바꾸는 것과 엣지를 추가·삭제하는 것은 다릅니다. 노드 위치만 바꾸고 연결을 유지하면 이웃과 경로는 그대로입니다.

## 체크리스트

- 그래프(graph)를 노드(node)와 엣지(edge)의 구조로 설명할 수 있다.
- 인접 리스트(adjacency list)를 각 노드의 이웃 목록으로 설명할 수 있다.
- 표와 그래프가 서로 다른 질문에 답한다는 점을 설명할 수 있다.
- 트리(tree)를 그래프의 특수한 형태로 입문 수준에서 설명할 수 있다.
- 무방향 그래프와 방향 그래프의 차이를 설명할 수 있다.
- 가중치(weight)가 관계에 숫자 정보를 붙인다는 점을 설명할 수 있다.
- 작은 그래프를 노드별 이웃 목록으로 표현하고 이웃을 따라가 볼 수 있다.
- NetworkX 같은 Python 그래프 도구가 노드, 엣지, 이웃, 방향, 가중치를 어떻게 다루는지 읽을 수 있다.
- 연결이 핵심인 데이터를 만났을 때 그래프 관점을 먼저 떠올릴 수 있다.

## 출처와 참고 자료

- Paul E. Black and Paul J. Tanenbaum, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, 확인 날짜: 2026-07-20. 그래프를 vertices/nodes와 edges/arcs로 구성된 구조로 설명하는 근거로 사용했다.
- NetworkX Developers, [Graph - Undirected graphs with self loops](https://networkx.org/documentation/stable/reference/classes/graph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation, 확인 날짜: 2026-07-20. 작은 무방향 그래프, 노드, 엣지, 인접 관계를 확인하는 근거로 사용했다.
- NetworkX Developers, [DiGraph - Directed graphs with self loops](https://networkx.org/documentation/stable/reference/classes/digraph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation, 확인 날짜: 2026-07-20. 방향 그래프와 successor 관계를 확인하는 근거로 사용했다.
