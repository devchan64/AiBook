## query-key-value, QKV

- Meaning: attention 계산에서 현재 위치가 무엇을 찾는지 나타내는 query, 각 위치가 어떤 정보인지 알려 주는 key, 실제로 섞어 올 내용을 담는 value를 함께 묶어 부르는 표현입니다. 즉 query는 `무엇을 찾고 싶은가`, key는 `어디가 그 조건에 맞는가`, value는 `그래서 실제로 무엇을 가져올 것인가`를 나누어 맡는 구조입니다.
- Why it matters: attention 직관을 `질문하고, 맞는 위치를 찾고, 그 내용을 가져온다`는 계산 흐름으로 다시 읽게 해 주어, Transformer 설명에서 반복되는 QKV 이름을 덜 추상적으로 만들기 때문입니다. 이 개념이 있어야 attention이 단순 가중합이 아니라, 조회 기준과 내용 전달이 분리된 구조라는 점을 이해하게 됩니다. 또한 QKV를 이해해야 같은 attention 블록 안에서도 `유사도 계산용 정보`와 `실제 전달 내용`이 서로 다른 역할이라는 점을 더 분명하게 읽게 됩니다.
- Related concepts: `self-attention`, `multi-head attention`, `Transformer`
- Core Section: `P5-13.3`
- Appears in: `P5-14.1`, `P6-4.3`
