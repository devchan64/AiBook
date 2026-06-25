# P2-13.2 근거 검토: 기본 차트와 수식의 모양 확인

## 사용한 주요 자료

| 자료 | 확인한 핵심 | 본문 반영 지점 |
| --- | --- | --- |
| Matplotlib Developers, `Quick start guide` | `pyplot.subplots()`로 Figure와 Axes를 만들고 `Axes.plot`으로 데이터를 그리는 기본 흐름을 제시한다. | `fig, ax = plt.subplots()` 중심의 예제 구성 |
| Matplotlib Developers, `Plot types` | `plot(x, y)`, `scatter(x, y)`, `bar(x, height)`, `hist(x)` 같은 여러 기본 plot type을 제공한다. | 선 그래프, 산점도, 히스토그램을 질문별로 구분하는 설명 |
| Matplotlib Developers, `matplotlib.pyplot` | Matplotlib의 plotting 함수 인터페이스로 pyplot을 제공한다. | pyplot 기반의 작은 실습 코드 구성 |

## 범위 판단

- P2-13.1은 그래프의 역할과 Figure/Axes 직관을 설명했다.
- P2-13.2는 실제 기본 차트로 수식, 관계, 분포, 손실 변화를 확인하는 절로 작성했다.
- 막대 그래프는 13.1에서 언급했지만, 이 절에서는 AI 기초 복구와 직접 연결되는 선 그래프, 산점도, 히스토그램, 손실 곡선에 집중했다.
- 스타일 꾸미기, 여러 subplot 배치, 시각화 디자인 원칙은 이 절의 핵심이 아니므로 제외했다.

## 생성한 출력 이미지

본문에 삽입한 출력 이미지는 외부 자료가 아니라 다음 스크립트로 자체 생성했다.

- `docs/assets/part-02/chapter-13/p2_13_2_basic_plots.py`

생성된 파일은 다음과 같다.

- `docs/assets/part-02/chapter-13/basic-line-function-shape.png`
- `docs/assets/part-02/chapter-13/basic-scatter-relationship.png`
- `docs/assets/part-02/chapter-13/basic-hist-distribution.png`
- `docs/assets/part-02/chapter-13/basic-loss-curve-comparison.png`

## 조심한 지점

- 산점도에서 관계처럼 보이는 것을 원인으로 단정하지 않았다.
- 히스토그램을 분포의 엄밀한 통계 추정으로 설명하지 않고, 값의 몰림을 보는 입문 도구로 설명했다.
- 손실 곡선을 좋은 모델의 증거로 단정하지 않고, 학습 흐름을 점검하는 질문으로 연결했다.
- 13.2에서 Matplotlib의 스타일링이나 복잡한 시각화 API로 확장하지 않았다.

## 이 절의 핵심 정리

- P2-13.2의 중심 질문은 “기본 차트로 무엇을 확인할 수 있는가?”다.
- 핵심 답은 선 그래프는 변화와 수식의 모양, 산점도는 관계와 변동, 히스토그램은 값의 몰림, 손실 곡선은 학습 흐름을 확인한다는 것이다.
- 그래프는 결론을 대신하지 않고 다음 질문을 만들게 하는 점검 도구로 설명했다.
