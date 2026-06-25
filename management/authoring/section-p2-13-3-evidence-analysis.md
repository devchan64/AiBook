# P2-13.3 근거 검토: 여러 그래프를 비교하고 저장하기

## 사용한 주요 자료

| 자료 | 확인한 핵심 | 본문 반영 지점 |
| --- | --- | --- |
| Matplotlib Developers, `Quick start guide` | `Figure`와 `Axes` 구조, `pyplot.subplots()` 기반의 기본 작성 흐름을 설명한다. | 여러 `Axes`를 한 `Figure`에 배치하는 설명 |
| Matplotlib Developers, `Introduction to Axes (or Subplots)` | Figure 안에 Axes를 배치하고 subplot을 다루는 관점을 제공한다. | `plt.subplots(1, 2)`와 `axes[0]`, `axes[1]` 설명 |
| Matplotlib Developers, `matplotlib.figure.Figure.savefig` | Figure를 파일로 저장하는 API를 제공한다. | `fig.savefig(...)`와 저장 가능한 기록 설명 |

## 범위 판단

- P2-13.1은 그래프가 숫자의 모양을 드러내는 이유를 설명했다.
- P2-13.2는 기본 차트 선택과 수식·분포·손실 곡선 확인에 집중했다.
- P2-13.3은 여러 그래프를 비교하고 저장하는 흐름으로 좁혔다.
- 복잡한 스타일링, 대시보드, 인터랙티브 시각화, 논문용 도표 작성은 제외했다.

## 생성한 출력 이미지

본문에 삽입한 출력 이미지는 외부 자료가 아니라 다음 스크립트로 자체 생성했다.

- `docs/assets/part-02/chapter-13/p2_13_3_compare_and_save.py`

생성된 파일은 다음과 같다.

- `docs/assets/part-02/chapter-13/subplot-loss-accuracy.png`
- `docs/assets/part-02/chapter-13/train-validation-loss-diverge.png`

## 조심한 지점

- 손실과 정확도는 단위가 다르므로 같은 축에 억지로 올리지 않고, 나란한 subplot 예시로 설명했다.
- train loss와 validation loss는 같은 단위의 손실 값이므로 같은 축에서 비교하는 예시로 설명했다.
- validation loss가 상승하는 예시를 과적합의 확정 증거로 쓰지 않고, 추가 확인이 필요한 신호로 표현했다.
- 저장된 그래프만으로는 재현성이 충분하지 않다는 점을 명시했다.

## 이 절의 핵심 정리

- P2-13.3의 중심 질문은 “여러 그래프를 어떻게 비교하고 기록으로 남길 것인가?”다.
- 핵심 답은 하나의 `Figure` 안에 여러 `Axes`를 배치하거나, 같은 `Axes`에서 같은 단위의 값을 비교할 수 있다는 것이다.
- 그래프 저장은 이미지 파일 생성만이 아니라 코드, 데이터 조건, 라이브러리 버전과 함께 재현 가능한 기록을 만드는 일로 정리했다.
