<a id="vocabulary"></a>

### 어휘 사전(vocabulary)

- 뜻: tokenizer가 만들 수 있는 token 조각과 그 조각에 대응하는 ID를 모아 둔 내부 목록입니다. 여기서의 vocabulary는 사람이 보는 국어사전이나 영어사전이 아니라, 모델 입력으로 들어갈 조각을 어떤 번호로 조회할지 정한 계산용 사전입니다.
- 왜 중요한가: 같은 문자열이라도 어떤 vocabulary와 분할 규칙을 쓰는지에 따라 token 조각, token 수, token ID가 달라질 수 있습니다. 이 개념이 있어야 token ID를 뜻풀이가 아니라 vocabulary 항목 번호로 읽고, tokenizer 차이가 비용과 문맥 길이에 영향을 주는 이유도 이해할 수 있습니다.
- 함께 볼 개념: `토큰(token)`, `토큰화(tokenization)`, `token ID`, `임베딩(embedding)`
- 중심 Section: `P6-2.2`
- 등장 Section: `P6-2.2`, `P6-2.5`, `P7-4.1`
