<a id="retrieval"></a>

### 검색(retrieval)

- 뜻: RAG 흐름에서 사용자 질문과 관련 있을 가능성이 높은 외부 문서나 문서 조각을 찾아오는 단계입니다. 일반적인 탐색(search)이나 사람이 웹에서 자료를 찾는 활동보다, 생성 입력에 넣을 근거 후보를 준비하는 정보 검색 단계로 좁혀 읽습니다.
- 왜 중요한가: `검색`이라는 한국어 표현이 탐색 알고리즘, 문서 검색, 웹 검색, RAG의 retrieval을 모두 가리킬 수 있어 오해가 생기기 쉽기 때문입니다. RAG에서 retrieval은 답을 직접 생성하는 단계가 아니라, 생성 모델이 참고할 외부 자료 후보를 고르는 단계입니다. 이 구분이 있어야 검색 결과가 곧 정답이 아니라 추가 입력 맥락의 재료라는 점을 분명히 이해할 수 있습니다.
- 함께 볼 개념: `검색 증강 생성(retrieval-augmented generation, RAG)`, `정보 검색(information retrieval)`, `외부 리소스(external resource)`, `생성(generation)`
- 중심 Section: `P1-13.3`
- 등장 Section:
