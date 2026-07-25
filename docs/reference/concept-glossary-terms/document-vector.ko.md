<a id="document-vector"></a>

### 문서 벡터(document vector)

- 뜻: 문서, 문단, 문서 조각을 임베딩으로 바꾼 벡터입니다. 유사도 검색에서는 질문 벡터와 문서 벡터를 비교해 어떤 문서 조각이 관련 후보인지 고릅니다. 즉 문서 벡터는 사람이 읽는 문서를 검색 시스템이 비교할 수 있게 만든 계산용 표현입니다.
- 왜 중요한가: 문서 원문과 검색용 표현을 구분하게 해 주기 때문입니다. 문서 벡터가 가깝다는 것은 관련 있을 가능성이 높다는 뜻이지, 그 문서가 반드시 정확한 답이라는 뜻은 아닙니다. 이 개념이 있어야 RAG에서 검색된 문서가 정답 보장이 아니라 LLM 입력에 넣을 근거 후보라는 점을 분명히 볼 수 있습니다.
- 함께 볼 개념: `질문 벡터(query vector)`, `문장·문단·문서 임베딩(sentence, paragraph, and document embedding)`, `유사도 검색(similarity search)`, `검색 증강 생성(retrieval-augmented generation, RAG)`
- 중심 Section: `P1-13.2`
- 등장 Section: `P1-13.3`
