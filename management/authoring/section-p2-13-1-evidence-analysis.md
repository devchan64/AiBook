# P2-13.1 근거 검토: 그래프(plot)는 무엇을 드러내는가

## 사용한 주요 자료

| 자료 | 확인한 핵심 | 본문 반영 지점 |
| --- | --- | --- |
| Matplotlib Developers, `Quick start guide` | Matplotlib은 데이터를 `Figure`에 그리고, `Figure`는 하나 이상의 `Axes`를 포함할 수 있으며, `pyplot.subplots()`로 Figure와 Axes를 만드는 예제를 제시한다. | `Figure`와 `Axes`의 직관, `fig, ax = plt.subplots()` 기본 형태 |
| Matplotlib Developers, `Plot types` | `plot(x, y)`, `scatter(x, y)`, `bar(x, height)`, `hist(x)` 등 여러 기본 plot type을 제공한다. | 질문에 따라 선 그래프, 산점도, 막대 그래프, 히스토그램을 고르는 설명 |
| Matplotlib Developers, `matplotlib.pyplot` | pyplot은 Matplotlib의 plotting 함수 인터페이스로 제공된다. | `pyplot` 사용 예제와 Matplotlib 입문 코드 흐름 |

## 범위 판단

- P2-13.1은 Matplotlib 기능 목록을 설명하는 절이 아니라, 그래프를 왜 그리는지 설명하는 도입부다.
- 선 그래프, 산점도, 히스토그램의 구체적 사용은 P2-13.2로 넘긴다.
- 차트 디자인, 색상, 레이아웃, 출판용 그래프 제작은 이 절 범위가 아니다.
- 그래프 해석에서 원인 추론을 과도하게 하지 않도록, 그래프는 판단의 시작점이라는 표현을 유지했다.

## 일반화 원칙

- `plot`은 넓은 의미의 그래프와 Matplotlib 함수명 양쪽에서 쓰일 수 있으므로, 본문에서는 그래프(plot)로 병기했다.
- `Figure`, `Axes`는 Matplotlib 공식 용어이므로 영어 원어를 유지하고, 한국어 직관을 덧붙였다.
- “차트 종류를 외우기보다 질문을 먼저 정한다”는 방향으로 초심자 설명을 구성했다.

## 조심한 지점

- 그래프가 관계를 보여 준다고 해서 인과(causality)를 증명한다고 쓰지 않았다.
- 13.2에서 다룰 구체 차트 작성법을 13.1에서 과도하게 전개하지 않았다.
- 차트 가이드라인의 세부 디자인 규칙은 본문 독자용 설명이 아니라 관리 문서의 역할이므로 이 절에 포함하지 않았다.
- 본문에 삽입한 pyplot 출력 이미지는 외부 자료를 가져온 것이 아니라 `docs/assets/part-02/chapter-13/p2_13_1_pyplot_outputs.py`로 자체 생성한 예제 출력이다.

## 이 절의 핵심 정리

- P2-13.1의 중심 질문은 “숫자 표를 그래프로 바꾸면 무엇이 보이는가?”다.
- 핵심 답은 값 자체보다 모양(shape), 변화(trend), 관계(relationship), 분포(distribution), 이상값(outlier)을 빠르게 확인할 수 있다는 것이다.
- Matplotlib은 이후 실습에서 이 확인 과정을 코드로 반복하기 위한 기본 도구로 소개한다.
