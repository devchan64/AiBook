# Part 5 목차 개편안

작성일: 2026-07-16

## 목적

이 문서는 Part 5의 현재 목차가 `딥러닝을 구조와 학습 절차로 나누어 설명한다`는 원칙을 충분히 지키는지 재검토하고, 큰 폭의 개편을 허용할 때 어떤 목차 축이 더 안정적인지 정리하기 위한 작업 노트다.

이 문서는 곧바로 배포 본문을 바꾸는 문서가 아니라, 이후 `mkdocs.yml`, `docs/book/table-of-contents.md`, Part 5 시작/마무리 페이지, 개별 Section 제목과 본문을 고칠 때 기준으로 삼는 제안서다.

## 현재 판단

Part 5의 큰 방향은 맞다. 퍼셉트론에서 시작해 손실, 역전파, 옵티마이저, 정규화, 계산 환경, 표현 학습, CNN, RNN, Attention, Transformer, 생성으로 이어지는 흐름 자체는 적절하다.

문제는 초중반 목차가 `구조`, `출력 해석`, `gradient 계산`, `학습 루프`, `계산 환경`, `표현 학습`을 명확히 분리하지 못한다는 점이다. 특히 Chapter P5-5는 `역전파`라는 제목만으로는 실제로 말해야 할 범위가 좁고, P5-5.1과 P5-5.2의 역할도 겹친다.

## 현재 목차의 주요 문제

| 위치 | 문제 | 영향 |
| --- | --- | --- |
| Module 2 `출력, 손실, 역전파` | 활성화 함수가 이 모듈 안에 들어 있어 `표현 변환 구조`와 `출력/손실/gradient`가 섞인다 | 활성화 함수가 손실 이후 학습 절차처럼 보일 수 있다 |
| Chapter P5-5 `역전파` | 실제로는 손실을 gradient로 바꾸는 장이어야 하는데 제목이 절차명 하나로 좁다 | 자동미분과 계산 그래프가 부록처럼 붙고, 장의 중심 질문이 흐려진다 |
| P5-5.1 | `책임 분해` 비유, gradient 부호 예제, 자동미분 보강이 한 절 안에서 섞인다 | 독자가 역전파, 자동미분, optimizer 전 단계를 분리하기 어렵다 |
| P5-5.2 | 계산 그래프와 자동미분을 잘 다루지만 P5-5.1에서 이미 비슷한 연결을 건드린다 | 두 Section 경계가 약해지고 반복 설명이 생긴다 |
| Chapter P5-6 | 학습/실행 분리가 optimizer보다 먼저 온다 | `forward -> loss -> backward -> optimizer step` 루프가 닫히기 전에 학습/실행 구분이 추상적으로 보인다 |
| P5-8.3 | `학습 루프를 한 번에 다시 묶기`가 정규화와 드롭아웃 Chapter 아래에 있다 | Module 3 전체 요약 역할이 작게 보인다 |
| Module 4 | GPU/배치와 표현 학습이 같은 모듈에 묶인다 | 계산 환경과 표현 학습이라는 서로 다른 축이 섞인다 |

## Part 5가 말해야 하는 중심 문장

Part 5는 다음 문장을 중심축으로 삼는 편이 가장 안정적이다.

`신경망은 입력을 표현으로 바꾸고, 손실을 gradient로 바꾸며, optimizer로 파라미터를 조정하고, 데이터 구조에 맞는 모델 구조로 확장된다.`

이 문장을 기준으로 보면 Part 5의 학습 흐름은 다음 순서로 나뉜다.

| 흐름 | 맡아야 할 설명 |
| --- | --- |
| 기본 계산 구조 | 입력, 가중치, 선형 결합, 은닉층, 활성화 함수가 표현을 만든다 |
| 출력과 손실 | 출력층은 문제 유형에 맞게 해석되고, 손실은 틀림을 숫자로 만든다 |
| gradient 계산 | 손실 숫자는 직접 업데이트가 아니며, 역전파와 자동미분으로 파라미터별 gradient가 계산된다 |
| 학습 루프와 안정화 | optimizer가 gradient로 파라미터를 움직이고, regularization/dropout/training mode가 학습을 안정화한다 |
| 계산 확장 | GPU, batch, tensor 계산이 큰 모델 학습을 가능하게 한다 |
| 표현 학습과 구조 분기 | 모델은 표현을 직접 학습하고, CNN/RNN/Attention/Transformer는 데이터 구조 문제에 맞춰 갈라진다 |
| 생성 연결 | 생성 모델과 샘플링은 Part 6의 LLM 이해로 넘어가는 구조적 출발점이다 |

## 권장 개편안

큰 폭 개편을 허용한다면 Part 5 목차는 다음처럼 재정렬하는 편이 낫다.

### Module 1. 신경망의 기본 계산 구조

- Chapter P5-1. 퍼셉트론
- Chapter P5-2. 다층 신경망과 은닉 표현
- Chapter P5-3. 활성화 함수와 출력층

의도:
활성화 함수는 손실/역전파보다 앞선 `표현 변환 구조`로 둔다. 출력층은 활성화 함수의 마지막 사용처이므로 Chapter P5-3 안에서 함께 닫는 편이 자연스럽다.

### Module 2. 출력과 손실 신호

- Chapter P5-4. 손실 함수
- Chapter P5-5. 손실에서 gradient로

의도:
Chapter P5-4는 `틀림을 숫자로 만드는 법`을 맡고, Chapter P5-5는 `그 숫자가 파라미터별 gradient 신호가 되는 법`을 맡는다.

권장 Section 경계:

| Section | 권장 제목 | 중심 질문 |
| --- | --- | --- |
| P5-5.1 | 손실은 어떻게 파라미터별 gradient 신호가 되는가 | 손실 숫자만으로는 왜 업데이트할 수 없고, 각 파라미터별 gradient가 왜 필요한가 |
| P5-5.2 | 계산 그래프와 자동미분 | 복잡한 계산에서는 gradient 계산을 어떻게 기록하고 자동화하는가 |

이 경우 `역전파(backpropagation)`는 Chapter 제목이 아니라 P5-5.1의 핵심 절차명으로 설명한다. `자동미분(automatic differentiation)`은 P5-5.2의 핵심 기술로 설명하되, P5-5.1에서 최소 위치 감각은 먼저 준다.

### Module 3. 학습 루프와 업데이트

- Chapter P5-6. 학습 루프: forward, loss, backward, optimizer step
- Chapter P5-7. 옵티마이저
- Chapter P5-8. 학습 안정화와 일반화 제약

의도:
학습/실행 분리는 optimizer보다 앞에 독립 장으로 두기보다, 학습 루프가 한 번 닫힌 뒤 training/inference, training/eval mode, optimizer, regularization으로 이어지게 하는 편이 좋다.

가능한 재배치:

| 현재 위치 | 개편 후 위치 |
| --- | --- |
| P5-6.1 학습과 모델 실행 | P5-6.1 학습 루프와 모델 실행 구분 |
| P5-6.2 학습 모드와 평가 모드 | P5-8 또는 학습 안정화 장으로 이동 검토 |
| P5-8.3 학습 루프를 한 번에 다시 묶기 | P5-6 앞쪽 또는 Module 3 도입/마무리 역할로 이동 검토 |
| P5-6.3, P5-6.4 초기화/수치 안정성/배치 정규화 | 학습 안정화 보충학습으로 Chapter P5-8 쪽 이동 검토 |

### Module 4. 계산 확장

- Chapter P5-9. GPU, 배치, 텐서 계산

의도:
GPU와 배치/텐서는 표현 학습과 같은 모듈에 묶기보다, 큰 모델 학습을 가능하게 한 계산 확장 축으로 별도 모듈화한다.

### Module 5. 표현 학습과 구조 분기

- Chapter P5-10. 표현 학습
- Chapter P5-11. 공간 구조와 CNN
- Chapter P5-12. 순차 구조와 RNN 계열
- Chapter P5-13. Attention
- Chapter P5-14. Transformer

의도:
표현 학습을 GPU/배치 뒤의 부가 장이 아니라 구조 분기 전체의 해석 축으로 올린다. CNN, RNN, Attention, Transformer는 모두 `표현을 어떻게 구성하고 어떤 의존성을 읽는가`의 하위 전개로 묶는다.

### Module 6. 생성 모델과 샘플링

- Chapter P5-15. 생성 모델과 샘플링

의도:
Part 6으로 넘기기 전에 생성 모델의 구조적 출발점을 닫는다. 여기서는 LLM 서비스나 토큰화 전체를 미리 설명하지 않고, `분포 학습`과 `출력 선택`만 닫는다.

## 최소 개편안

파일 이동과 Section 번호 변경을 최소화하려면 다음 수준부터 적용할 수 있다.

1. `Chapter P5-5. 역전파`를 `Chapter P5-5. 손실에서 gradient로`로 바꾼다.
2. `P5-5.1 역전파(backpropagation)의 직관`을 `P5-5.1 손실은 어떻게 gradient 신호가 되는가`로 바꾼다.
3. `P5-5.2 계산 그래프(computation graph)`를 `P5-5.2 계산 그래프와 자동미분`으로 바꾼다.
4. `Module 2. 출력, 손실, 역전파`를 `Module 2. 표현 변환과 손실 신호` 또는 `Module 2. 출력과 gradient 신호`로 바꾼다.
5. `P5-8.3 학습 루프를 한 번에 다시 묶기`가 Module 3 요약 역할임을 목차 설명과 Part 개요에서 명시한다.
6. Part 5 시작/마무리 페이지에서 `역전파` 단독 표현을 `손실을 gradient로 바꾸는 계산`으로 바꾼다.

최소 개편안은 목차 충격이 작지만, Chapter P5-6~P5-8의 순서 문제는 남는다.

## 권장 적용 순서

큰 개편을 한 번에 적용하면 링크, 릴리즈노트, 목차 설명, 내부 문장까지 같이 흔들린다. 따라서 다음 순서가 안전하다.

1. Chapter P5-5의 이름과 P5-5.1/P5-5.2 역할을 먼저 확정한다.
2. P5-5.1 본문을 `손실 -> gradient -> 역전파 -> 자동미분 위치 -> optimizer 전 단계` 흐름으로 다시 쓴다.
3. P5-5.2 본문은 `계산 그래프와 자동미분`으로 역할을 좁히고, P5-5.1과 반복되는 책임 분해 문장을 줄인다.
4. `mkdocs.yml`과 `docs/book/table-of-contents.md`에 Chapter P5-5 제목 변경을 반영한다.
5. Part 5 시작/마무리 페이지의 전체 흐름 문장을 `손실과 역전파`에서 `손실에서 gradient로` 중심으로 고친다.
6. 이후 Chapter P5-6~P5-8의 순서와 P5-8.3 위치를 별도 패치로 검토한다.
7. 마지막으로 Module 4와 표현 학습 위치를 재검토한다.

## 수정 시 함께 확인할 파일

| 대상 | 확인 이유 |
| --- | --- |
| `mkdocs.yml` | 배포 목차 기준 |
| `docs/book/table-of-contents.md` | 독자용 목차 설명 |
| `docs/parts/part-05/index.md` | Part 5 시작 페이지의 전체 학습 흐름 |
| `docs/parts/part-05/summary.md` | Part 5 마무리 페이지의 핵심 회수 문장 |
| `docs/parts/part-05/chapter-05/section-01.md` | P5-5.1 본문 전면 재구성 대상 |
| `docs/parts/part-05/chapter-05/section-02.md` | P5-5.2 제목과 자동미분 역할 조정 대상 |
| `management/release-notes/sections/part-05/P5-5.1.md` | Section 수정 이력 |
| `management/release-notes/sections/part-05/P5-5.2.md` | Section 수정 이력 |
| `management/release-notes/sections/book/BOOK-toc.md` | 독자용 목차 설명 변경 이력 |
| `management/release-notes/sections/part-05/P5-index.md` | Part 시작 페이지 변경 이력 |
| `management/release-notes/sections/part-05/P5-summary.md` | Part 마무리 페이지 변경 이력 |

## 열린 결정

- Chapter P5-5의 최종 제목을 `손실에서 gradient로`로 확정할지, `역전파와 자동미분`으로 둘지 결정해야 한다.
- P5-8.3을 실제로 이동할지, 제목과 설명만 조정해 Module 3 요약 역할을 명시할지 결정해야 한다.
- 표현 학습을 GPU/배치 뒤에 유지할지, 구조 분기 모듈의 도입 장으로 위치를 재정의할지 결정해야 한다.
- 파일 경로와 Section ID를 유지할지, 목차 재배치에 맞춰 chapter 디렉터리와 Section 번호까지 바꿀지 결정해야 한다.

## 현재 권고

현재 단계에서는 파일 경로와 Section ID는 유지하고, 먼저 목차 표기와 본문 중심축을 고치는 편이 안전하다. 특히 P5-5.1/P5-5.2는 즉시 재구성 대상이다.

가장 먼저 적용할 변경은 다음이다.

`Chapter P5-5. 역전파` -> `Chapter P5-5. 손실에서 gradient로`

이 변경은 Part 5의 학습 절차 축을 바로잡는 효과가 크고, 파일 이동 없이 적용할 수 있다.

## 2026-07-16 적용 메모

이번 개편에서는 원본 원고 손상을 피하기 위해 파일 경로와 Section ID를 유지하고, 공개 목차와 Part 시작/마무리 페이지의 구조 축을 먼저 조정했다.

적용한 결정은 다음과 같다.

- Chapter P5-5의 공개 제목은 `손실에서 gradient로`로 확정했다.
- P5-5.1은 손실 숫자가 파라미터별 gradient 신호가 되는 이유를 설명하는 Section으로 재구성했다.
- P5-5.2는 계산 그래프(computation graph)와 자동미분(automatic differentiation)의 역할을 함께 설명하는 Section으로 조정했다.
- P5-3 활성화 함수는 `출력과 gradient 신호`가 아니라 `신경망의 기본 계산 구조` 흐름으로 읽히도록 목차상 Module 1에 둔다.
- P5-9 GPU, 배치, 텐서 계산은 `계산 확장` Module로 분리한다.
- P5-10~P5-14는 `표현 학습과 구조 분기` Module로 묶어, CNN, RNN, Attention, Transformer를 모델 이름 나열이 아니라 표현과 의존성 구조의 분기로 읽게 한다.
- P5-15는 `생성 모델과 샘플링` Module로 분리해 Part 6의 LLM 설명으로 넘어가기 전 구조적 출발점을 닫는다.

아직 파일 이동과 Section 번호 재부여는 하지 않았다. 이후 실제 원고 재배치를 더 크게 진행하려면 현재 아카이브를 기준 원본으로 두고, 별도 패치에서 chapter 디렉터리와 릴리즈노트 정책까지 함께 검토해야 한다.
