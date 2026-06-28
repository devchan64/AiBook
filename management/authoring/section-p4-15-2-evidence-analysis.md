# P4-15.2 근거 검토 메모

## 절의 역할

- Part 4의 생성 모델 설명을 `샘플링` 개념으로 닫는다.
- Part 5의 토큰, 다음 토큰 예측, 생성 설정 개념으로 넘어가는 다리를 만든다.

## 이번 절의 핵심 주장

- 생성 출력은 하나의 정답만 있는 구조가 아닐 수 있다.
- 샘플링은 후보들 중 실제 출력을 선택하는 절차다.
- 생성 결과의 다양성과 안정성은 선택 전략과 연결된다.

## 반영한 근거

- Goodfellow, Bengio, Courville, `Deep Learning`
  - 생성 모델과 확률 분포 관점의 일반 설명 근거로 사용.
- Manning and Schutze, `Foundations of Statistical Natural Language Processing`
  - 언어 생성과 확률적 선택의 고전적 배경 설명 근거로 사용.
- Jurafsky and Martin, `Speech and Language Processing`
  - 언어 모델과 생성 출력 선택을 입문 수준으로 일반화하는 근거로 사용.

## 집필 판단

- Part 4에서는 temperature, top-k, top-p의 세부 구현은 넣지 않았다.
- 대신 `argmax와 sampling 차이`를 작은 Python 예제로 보여 주었다.
- 이 절의 목적은 수학적 엄밀성보다 생성형 AI 출력의 성격을 초심자에게 설명하는 데 있다.

## 제외한 내용

- beam search 세부 구현
- diffusion sampling 세부 과정
- 생성 설정 파라미터의 제품별 차이

이 내용은 Part 5의 LLM 생성 과정에서 더 구체적으로 다룰 수 있다.
