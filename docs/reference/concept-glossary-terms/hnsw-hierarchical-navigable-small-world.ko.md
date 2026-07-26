<a id="hnsw-hierarchical-navigable-small-world"></a>

### HNSW(hierarchical navigable small world)

- 뜻: 가까운 벡터들 사이의 그래프 연결을 이용해 근사 최근접 이웃을 빠르게 찾는 대표적인 벡터 검색 인덱스 방법입니다. 여러 층의 그래프를 사용해 대략 가까운 영역으로 이동한 뒤, 그 안에서 더 가까운 후보를 좁히는 방식으로 이해할 수 있습니다.
- 왜 중요한가: 벡터 검색이 단순히 모든 벡터를 비교하는 일이 아니라, 가까운 후보로 이동하는 경로를 미리 만들어 두는 구현 문제라는 점을 보여 주기 때문입니다. HNSW를 깊이 구현하지 않더라도, 그래프 기반 검색이 왜 대규모 벡터 검색에서 자주 언급되는지 이해하면 벡터 데이터베이스와 검색 인덱스의 역할을 더 잘 읽을 수 있습니다.
- 함께 볼 개념: `그래프 기반 검색(graph-based search)`, `근사 최근접 이웃(ANN, approximate nearest neighbor)`, `검색 인덱스(search index)`, `벡터 데이터베이스(vector database)`
- 중심 Section: `P1-13.4`
- 등장 Section: `P6-3.4`
- 등장 Section:
