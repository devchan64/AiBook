# P5-1.1 근거 검토 메모

## 절의 역할

- Part 5의 출발점으로서 토큰(token)을 정의한다.
- 입력 길이, 비용, context window가 왜 토큰 기준인지 초심자에게 설명한다.

## 이번 절의 핵심 주장

- 토큰은 모델이 텍스트를 계산하기 위해 사용하는 기본 단위다.
- 토큰은 단어와 항상 같지 않다.
- LLM의 길이, 비용, 생성은 토큰 단위와 직접 연결된다.

## 반영한 근거

- Jurafsky and Martin, `Speech and Language Processing`
  - NLP에서 텍스트 단위화와 언어 모델 입력 단위를 설명하는 일반 배경으로 사용.
- Manning and Schutze, `Foundations of Statistical Natural Language Processing`
  - 토큰화와 단위화의 고전적 배경 설명에 사용.
- OpenAI API Docs
  - 실제 서비스에서 길이와 비용이 토큰 기준으로 다뤄진다는 점의 실무 근거로 사용.

## 집필 판단

- 알고리즘 구현보다 개념 정의와 실무 연결을 우선했다.
- 단순 `split()` 예제를 사용해 실제 토크나이저 구현과 개념 입구를 구분했다.

## 제외한 내용

- BPE, WordPiece, SentencePiece 상세 구현
- 모델별 토큰 사전 차이

이는 P5-1.2 이후 필요할 때 다시 보강한다.
