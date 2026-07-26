<a id="token-id"></a>

### token ID

- 뜻: tokenizer가 만든 토큰 조각을 모델의 vocabulary 안에서 가리키는 번호입니다. 사람이 읽는 문자열 뜻이 아니라, 해당 조각을 내부 사전의 어느 항목으로 조회할지 나타내는 식별자입니다.
- 왜 중요한가: LLM은 원문 문자열을 직접 계산하지 않고, 토큰 ID 순서열을 받아 임베딩 벡터로 바꾼 뒤 계산합니다. 이 개념이 있어야 `토큰 문자열`, `토큰 수`, `token ID`를 섞지 않고, ID 숫자의 크기를 의미나 중요도로 오해하지 않게 됩니다.
- 함께 볼 개념: `토큰(token)`, `토큰화(tokenization)`, `어휘 사전(vocabulary)`, `임베딩(embedding)`
- 중심 Section: `P6-2.2`
- 등장 Section:
