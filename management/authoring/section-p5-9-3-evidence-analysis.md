# P5-9.3 근거 검토 메모

## 절의 역할

- LoRA의 `low-rank` 직관을 수식 없이 보강한다.
- adapter, LoRA, QLoRA의 층위 차이를 입문 수준으로 구분한다.
- P5-9.2의 실무 감각 설명을 받치는 보충학습으로 배치한다.

## 이번 절의 핵심 주장

- LoRA는 큰 가중치 전체를 다시 학습하기보다 작은 변화분만 학습하려는 흐름이다.
- `low-rank`는 변화분을 더 작은 구조로 표현하려는 직관과 연결된다.
- adapter, LoRA, QLoRA는 모두 효율적 조정 흐름에 속하지만 같은 방식은 아니다.

## 반영한 근거

- Houlsby et al., `Parameter-Efficient Transfer Learning for NLP`
- Hu et al., `LoRA: Low-Rank Adaptation of Large Language Models`
- Dettmers et al., `QLoRA: Efficient Finetuning of Quantized LLMs`

## 집필 판단

- 선형대수 전개와 양자화 수식은 제외하고, 이름을 읽는 데 필요한 구조 차이만 남겼다.
- QLoRA는 별도 철학이라기보다 LoRA의 실무 확장으로 제한해 설명했다.
- 실제 프레임워크 구현 예시는 넣지 않고, 규모 차이를 확인하는 장난감 파라미터 계산 예제로 대체했다.

## 제외한 내용

- 저랭크 분해 증명
- NF4, double quantization 같은 세부 양자화 기법 설명
- 라이브러리별 코드 예시
