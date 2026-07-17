# P5-7 보충학습 확장 검토 리포트

작성일: 2026-07-17  
검토 대상: `docs/parts/part-05/chapter-07/section-01.md` ~ `section-04.md`  
검토 기준: `AGENTS.md`, `management/guidelines/manuscript-writing-workflow.md`

## 목적

P5-7 챕터가 현재 본편에서 닫는 질문과, 본편 밖에서 별도 회수하는 편이 더 적절한 질문을 다시 나눈다.  
이번 리포트의 직접 목적은 `P5-7 챕터에는 보충학습이 여럿 추가되면 좋겠다`는 판단이 실제로 타당한지 검토하고, 추가한다면 어떤 보충학습을 어떤 순서로 두는 것이 좋은지 정리하는 것이다.

## 현재 구조 요약

현재 P5-7 챕터는 다음 네 절로 구성되어 있다.

- `P5-7.1`: optimizer가 gradient를 실제 update로 바꾸는 역할
- `P5-7.2`: learning rate가 update 보폭을 어떻게 바꾸는가
- `P5-7.3`: 적응형 업데이트의 직관을 Adam을 예로 설명
- `P5-7.4`: adaptive optimization 논문에서 수렴 분석 문장을 처음 읽는 법

현재 구조의 장점은 본편 질문과 보충학습 질문이 이미 한 차례 분리되어 있다는 점이다.

- 본편 질문
  - `누가 파라미터를 실제로 바꾸는가`
  - `같은 gradient라도 왜 보폭이 달라지는가`
  - `적응형 업데이트는 기본 update에 무엇을 더 보려 하는가`
- 보충학습 질문
  - `adaptive optimizer 논문에서 수렴 보장을 어떻게 읽는가`

즉, 현재 `P5-7.4`는 유지하는 편이 맞고, 새 보충학습 후보는 `P5-7.1 ~ P5-7.3` 본편 흐름을 흐리지 않으면서도 뒤에서 반복해서 도움이 되는 항목이어야 한다.

## 판단 기준

이번 검토에서는 아래 네 기준을 함께 적용했다.

1. 현재 본편 질문을 닫는 데 꼭 필요하지는 않지만, 독자가 바로 다음으로 물을 가능성이 높은가?
2. 그 질문이 뒤 장이나 뒤 Part에서도 반복 등장해, 한 번 별도 회수 위치를 두면 재사용 가치가 큰가?
3. 본편에 넣으면 `optimizer 직관` 설명보다 주변 구현·운영 항목이 더 길어지는가?
4. Chapter 8의 regularization/normalization 축으로 넘기는 편이 더 자연스러운가?

## 결론 요약

이번 검토에서는 `2번 안`을 기준안으로 채택하는 편이 가장 적절하다고 본다.  
즉, `P5-7.4`를 유지한 상태에서 Chapter 7 뒤쪽에 보충학습 여러 절을 연속으로 두고, 각 절이 닫아야 할 질문과 포함 주제를 분명히 나누는 방식이다.

`보충학습은 양이 많아도 괜찮다`는 전제를 두면, `P5-7`에는 보충학습을 여러 절 추가하는 편이 오히려 자연스럽다.

선택안 2의 권장 구조:

1. `P5-7.4 보충학습: adaptive optimization의 수렴 분석을 처음 읽는 법`
2. `P5-7.5 보충학습: momentum, AdaGrad, RMSProp, Adam을 처음 구분하는 법`
3. `P5-7.6 보충학습: learning rate scheduler, warmup, decay를 처음 읽는 법`
4. `P5-7.7 보충학습: optimizer state와 parameter-wise update를 처음 읽는 법`
5. `P5-7.8 보충학습: gradient clipping과 불안정한 update를 처음 구분하는 법`

조건부 후보:

1. `AdamW와 weight decay를 처음 구분하는 법`

비추천:

1. `distributed optimizer`, `gradient accumulation`, `mixed precision`, `optimizer state sharding`
2. `optimizer 내부 구현 세부`를 별도 보충학습으로 추가하는 안

## 추천 보충학습 1. optimizer 계열 비교

### 제안 제목

`P5-7.5 보충학습: momentum, AdaGrad, RMSProp, Adam을 처음 구분하는 법`

### 왜 필요한가

현재 `P5-7.3`은 의도적으로 `적응형 업데이트의 직관`만 남기고, Adam을 대표 예로 읽게 정리되어 있다.  
이 선택은 본편에서는 맞지만, 그 결과 독자는 다음 질문을 곧바로 하게 된다.

- Adam은 adaptive update의 대표 예라면, momentum이나 RMSProp은 어디에 놓이는가?
- AdaGrad와 Adam은 둘 다 adaptive처럼 보이는데 무엇이 다른가?
- `최근 흐름`, `좌표별 조절`, `누적 크기`는 각각 어떤 optimizer 계열에서 더 중심적인가?

이 질문은 현재 본편에서 닫을 필요는 없지만, Part 5 안에서 한 번 회수해 두면 뒤의 optimizer 언급을 더 안정적으로 읽을 수 있다.

### 이 보충학습이 닫을 질문

- momentum은 `현재 gradient` 외에 무엇을 더 보려는가?
- AdaGrad와 RMSProp은 `좌표별 조절`을 어떤 감각으로 읽게 하는가?
- Adam은 왜 `momentum + adaptive scale`이 함께 언급되는가?
- 계열 비교를 `성능 우열표`가 아니라 `무엇을 더 기억하고 무엇을 더 조절하는가`로 읽을 수 있는가?

### 본편에 넣지 않는 이유

이 비교를 `P5-7.3` 본문으로 끌어오면, 적응형 업데이트의 입문 직관보다 optimizer 계열 소개가 더 길어진다. 따라서 이 항목은 별도 보충학습으로 두는 편이 맞다.

### 권장 구조

- `이 보충학습의 범위`
- `직접 update -> momentum -> AdaGrad/RMSProp -> Adam`의 작은 비교 표
- `무엇을 더 기억하는가 / 무엇을 더 조절하는가 / 무엇을 해결하려 했는가` 표
- `optimizer 이름을 처음 읽는 순서`
- 작은 Python 비교 예제 1개

### 포함되어야 할 주제

- momentum이 `현재 gradient`만이 아니라 `이전 이동 방향`도 일부 남긴다는 뜻
- AdaGrad가 `좌표별 누적 gradient 크기`를 다르게 본다는 뜻
- RMSProp이 AdaGrad의 `누적이 계속 커지는 문제`를 어떻게 완화하려는지
- Adam이 `momentum + adaptive scale`을 함께 쓰는 대표 예라는 점
- `무엇을 더 기억하는가`, `무엇을 더 조절하는가`, `무엇을 해결하려 했는가`의 3축 비교
- 절대 우열표가 아니라 `읽는 기준표`로 마무리하는 구조

## 추천 보충학습 2. learning rate schedule

### 제안 제목

`P5-7.6 보충학습: learning rate scheduler, warmup, decay를 처음 읽는 법`

### 왜 필요한가

현재 `P5-7.2`는 learning rate를 `한 번의 update 보폭`으로 설명하는 절로 안정적이다.  
하지만 실제로 독자는 곧 다음 질문을 하게 된다.

- learning rate는 왜 학습 내내 고정하지 않고 바꾸는가?
- warmup은 왜 초반에 learning rate를 천천히 올린다고 말하는가?
- decay는 보폭을 줄이는 말인데, 그게 7.2의 직관과 어떻게 이어지는가?

이 질문은 현재 `P5-7.2` 안에 넣으면 절의 중심이 `정적 보폭 직관`에서 `시간에 따라 바뀌는 정책`으로 옮겨가므로, 별도 보충학습이 더 적절하다.

또 `P5-7.4` 수렴 분석 절에서도 `step size schedule`을 조건으로 읽는 항목이 이미 등장한다. 즉, `scheduler` 보충학습은 `P5-7.2`와 `P5-7.4` 사이를 잇는 회수 위치가 될 수 있다.

### 이 보충학습이 닫을 질문

- 고정 learning rate와 time-varying learning rate를 왜 구분하는가?
- warmup은 `처음부터 크게 움직이지 않도록 하는 장치`로 읽으면 되는가?
- decay는 `후반에 보폭을 줄여 미세 조정하는 장치`로 읽으면 되는가?
- cosine, step decay, linear decay를 수학적 취향이 아니라 `보폭 운영 정책`으로 읽을 수 있는가?

### 본편에 넣지 않는 이유

이 내용은 `P5-7.2`의 중심 질문인 `learning rate가 update에 어디에 붙는가`보다 한 단계 뒤 질문이다. 본편에 넣으면 `보폭이 무엇인가`와 `보폭을 시간에 따라 어떻게 운영하는가`가 같은 절 안에서 섞인다.

### 권장 구조

- `이 보충학습의 범위`
- 고정 보폭 vs schedule 표
- warmup, decay, cosine을 한 줄씩 읽는 표
- `어떤 로그를 보면 scheduler 질문을 먼저 떠올려야 하는가`
- 작은 learning-rate curve 그림 또는 표

### 포함되어야 할 주제

- `고정 learning rate`와 `시간에 따라 바뀌는 learning rate`의 차이
- warmup을 `초반에 보폭을 갑자기 크게 두지 않기 위한 장치`로 읽는 법
- decay를 `후반 미세 조정을 위한 보폭 축소`로 읽는 법
- step decay, cosine decay, linear decay를 `정책 이름`이 아니라 `보폭 운영 패턴`으로 읽는 기준
- `loss는 줄지만 후반 진동이 크다`, `초반 학습이 불안정하다` 같은 로그를 scheduler 질문으로 연결하는 기준
- `P5-7.2`의 보폭 직관과 `P5-7.4`의 step size schedule 조건을 이어 주는 handoff

## 추천 보충학습 3. optimizer state

### 제안 제목

`P5-7.7 보충학습: optimizer state와 parameter-wise update를 처음 읽는 법`

### 왜 필요한가

현재 `P5-7.3`은 시간축 누적과 좌표축 조절을 직관 수준에서 설명한다. 그러나 독자는 곧 다음 질문을 하게 된다.

- `최근 흐름을 본다`는 말은 어디에 저장된다는 뜻인가?
- Adam이 파라미터마다 다르게 움직인다고 할 때, 무엇이 좌표별로 따로 유지되는가?
- optimizer state가 모델 파라미터와 어떻게 다른가?

이 질문은 적응형 업데이트를 더 오래 기억하게 하는 손잡이지만, 본편 `P5-7.3` 안에 넣으면 다시 구현 설명이 길어진다. 따라서 별도 보충학습으로 두는 편이 적절하다.

### 이 보충학습이 닫을 질문

- parameter, gradient, update, optimizer state는 각각 무엇이 다른가?
- 왜 Adam류는 파라미터마다 따로 누적값을 들고 있다고 읽어야 하는가?
- `parameter-wise update`라는 말은 무엇이 좌표별로 달라진다는 뜻인가?
- optimizer를 바꾸면 모델 파라미터만이 아니라 state 구조도 함께 바뀐다고 읽을 수 있는가?

### 권장 구조

- `이 보충학습의 범위`
- parameter / gradient / update / state 구분 표
- `시간축 state`와 `좌표축 state`를 나누는 표
- 작은 Python 예제 또는 상태 추적 표
- `모델 파라미터`와 `optimizer 내부 기억`을 분리하는 체크리스트

### 포함되어야 할 주제

- `parameter`와 `optimizer state`를 같은 것으로 읽지 않는 기준
- moving average, second moment 같은 값이 좌표별로 따로 쌓인다는 뜻
- `state가 있기 때문에 같은 gradient라도 다음 step update가 달라질 수 있다`는 구조
- adaptive optimizer가 `한 번의 gradient`보다 `누적된 내부 상태`를 더 본다는 점
- optimizer state가 커질수록 메모리와 저장 질문이 왜 따라오는지의 아주 얕은 예고

## 추천 보충학습 4. gradient clipping

### 제안 제목

`P5-7.8 보충학습: gradient clipping과 불안정한 update를 처음 구분하는 법`

### 왜 필요한가

현재 Chapter 7은 `gradient 방향`, `learning rate 보폭`, `adaptive update 직관`까지는 설명한다. 그러나 실제 학습 로그를 읽다 보면 독자는 곧 다음 질문을 만나게 된다.

- gradient가 너무 커서 update가 갑자기 튀는 경우는 어떻게 읽는가?
- learning rate가 큰 문제와 exploding gradient 비슷한 문제를 어떻게 구분하는가?
- clipping은 optimizer 종류와 다른 층위의 장치인가?

이 질문은 본편에 넣으면 optimizer 직관보다 `불안정성 예외 처리`가 더 앞서게 되므로, 별도 보충학습으로 두는 편이 맞다.

### 이 보충학습이 닫을 질문

- gradient clipping은 무엇을 자르는가? gradient 자체인가, update 결과인가?
- learning rate 과대와 gradient 폭주를 어떻게 다르게 읽는가?
- clipping은 optimizer를 대체하는가, 아니면 update 전에 붙는 안전장치인가?
- RNN류 장면에서 왜 clipping이 자주 함께 언급되는가?

### 권장 구조

- `이 보충학습의 범위`
- `gradient가 너무 큼 / learning rate가 너무 큼 / 둘 다 문제` 비교 표
- clipping 전후 작은 숫자 예제
- `불안정한 loss 곡선`을 어떻게 읽는가
- 뒤의 RNN, 긴 시퀀스, 수치 안정화와의 handoff

### 포함되어야 할 주제

- clipping을 `방향을 바꾸는 장치`가 아니라 `너무 큰 이동을 제한하는 장치`로 읽는 법
- norm clipping과 value clipping을 입문 수준에서만 구분하는 기준
- `learning rate 문제`, `gradient scale 문제`, `optimizer state 문제`를 같은 것으로 읽지 않는 표
- exploding gradient와 unstable update를 구분하는 아주 작은 사례
- Chapter 8의 수치 안정성과 뒤의 RNN 장면으로 이어지는 연결 문장

## 조건부 후보. AdamW와 weight decay

### 판단

이 후보는 가치가 있지만, `P5-7`보다 `P5-8` 쪽에 두는 편이 더 적절하다.

### 이유

- `AdamW`는 이름만 보면 optimizer 비교처럼 보이지만, 독자가 실제로 막히는 지점은 `weight decay가 optimizer update와 어떻게 분리되는가`이다.
- 이 질문은 `적응형 업데이트`보다 `regularization과 optimizer의 경계`에 더 가깝다.
- 현재 `P5-8.1`은 regularization, weight decay, dropout, early stopping을 하나의 넓은 축으로 묶고 있다.

따라서 이 항목은 `P5-7` 새 보충학습보다 `P5-8` 보충학습 후보로 넘기는 편이 자연스럽다.

### 만약 실제로 만든다면 포함되어야 할 주제

- penalty로서의 L2 regularization과 decoupled weight decay의 차이
- `optimizer update 규칙`과 `regularization 항`을 같은 층위로 읽지 않는 기준
- AdamW가 왜 `Adam의 수렴`보다 `regularization 작동 방식` 쪽 질문에 가까운가
- dropout, early stopping과는 또 다른 regularization 축이라는 점

## 비추천 후보

### 1. distributed optimizer / gradient accumulation / mixed precision

이 항목들은 실제로는 중요하지만, 현재 Part 5 Chapter 7의 초심자용 설명 책임과 거리가 멀다.

- optimizer 개념보다 훈련 시스템 운영 축에 더 가깝다
- Chapter 7 본편보다 `대규모 학습 인프라` 질문을 먼저 불러온다
- 현재 책 구조에서는 Part 6 이후나 프로젝트/운영 파트에서 더 자연스럽다

따라서 `P5-7` 보충학습 후보로는 비추천한다.

### 2. optimizer 내부 구현 세부

예:

- bias correction 수식 전개 전체
- optimizer state 메모리 배치
- parameter group 구현 API 설명

이 항목들은 초심자 회수 위치보다 구현 메모에 가깝다. 현재 책의 본편과 보충학습 구조를 기준으로는 설명 대비 재사용 가치가 높지 않다.

## 선택안 2의 추가 순서

지금 기준으로는 아래 순서가 가장 안정적이다.

1. `P5-7.5 보충학습: momentum, AdaGrad, RMSProp, Adam을 처음 구분하는 법`
2. `P5-7.6 보충학습: learning rate scheduler, warmup, decay를 처음 읽는 법`
3. `P5-7.7 보충학습: optimizer state와 parameter-wise update를 처음 읽는 법`
4. `P5-7.8 보충학습: gradient clipping과 불안정한 update를 처음 구분하는 법`
5. `AdamW/weight decay`는 Chapter 8 보충학습 후보로 별도 검토

## 목차 영향 메모

새 보충학습을 실제로 추가한다면 다음 위치를 함께 갱신해야 한다.

- `mkdocs.yml`
- `docs/book/table-of-contents.md`
- `management/release-notes/sections/part-05/`
- 필요하면 `management/authoring/part-05-open-checklist.md`

## 최종 판단

현재 `P5-7.4`는 유지하는 편이 맞다.  
그 위에 `optimizer 계열 비교`, `learning rate schedule`, `optimizer state`, `gradient clipping` 보충학습을 추가하는 `선택안 2`를 채택하면, Chapter 7은 다음 세 층으로 더 안정된다.

- 본편
  - optimizer 역할
  - learning rate 보폭
  - 적응형 업데이트 직관
- 보충학습
  - optimizer 계열 비교
  - learning rate schedule 운영 감각
  - optimizer state와 parameter-wise update
  - gradient clipping과 불안정한 update
  - adaptive optimization 수렴 분석

즉, `P5-7 챕터에는 보충학습이 여럿 추가되면 좋겠다`는 판단은 타당하다.  
이번 리포트의 기준안은 `2번 안`이며, 각 보충 색션에는 아래 주제가 직접 포함되어야 한다.

1. `P5-7.5`
   - momentum, AdaGrad, RMSProp, Adam의 계열 차이
   - `무엇을 더 기억하는가`, `무엇을 더 조절하는가`, `무엇을 해결하려 했는가`의 3축 비교
2. `P5-7.6`
   - 고정 learning rate와 schedule의 차이
   - warmup, decay, cosine/linear/step 패턴을 보폭 운영 정책으로 읽는 기준
3. `P5-7.7`
   - parameter, gradient, update, optimizer state의 구분
   - state 누적 때문에 같은 gradient라도 다음 update가 달라지는 구조
4. `P5-7.8`
   - gradient clipping의 역할
   - learning rate 문제, gradient scale 문제, unstable update를 구분하는 기준

다만 아무 주제나 늘리기보다, `본편 직관을 지키면서도 뒤에서 반복 쓸 질문`만 골라 `P5-7.5`~`P5-7.8`을 연속 보충학습 후보로 두는 편이 가장 적절하다.
