# 차트 도구 대체 검토

확인 날짜: 2026-06-24

## 검토 기준

- 단순한 단계, 개념 관계, 박스-화살표 흐름은 Mermaid를 우선한다.
- 좌표축, 곡선, 점의 위치, 벡터 방향, 분포 모양처럼 위치 자체가 설명인 차트는 SVG를 유지한다.
- 시스템 구조가 복잡해지면 D2, PlantUML, Graphviz DOT 같은 도구를 검토하되, 현재 MkDocs 빌드 파이프라인에서 렌더링 가능 여부를 먼저 확인한다.

## Mermaid로 대체한 도식

| 위치 | 기존 파일 | 판단 |
| --- | --- | --- |
| `docs/parts/part-02/chapter-05/section-01.md` | `docs/assets/part-02/chapter-05/bayes-rule-belief-update.svg` | `prior belief -> evidence -> posterior belief`의 단순 흐름이므로 Mermaid가 유지보수에 유리하다. |
| `docs/parts/part-02/chapter-05/section-03.md` | `docs/assets/part-02/chapter-05/population-sample-dataset-relation.svg` | 모집단, 표본, 데이터셋의 포함 관계와 정리 흐름을 설명하는 개념 도식이므로 Mermaid로 충분하다. |
| `docs/parts/part-02/chapter-05/section-03.md` | `docs/assets/part-02/chapter-05/train-test-as-samples.svg` | 현실 세계, 데이터셋, train/test 분할의 흐름이 중심이므로 Mermaid가 적합하다. |
| `docs/parts/part-02/chapter-06/section-02.md` | `docs/assets/part-02/chapter-06/loss-objective-flow.svg` | 입력, 모델, 예측, 손실, 목적 함수의 단계 흐름이 중심이므로 Mermaid로 대체했다. |
| `docs/parts/part-02/chapter-06/section-03.md` | `docs/assets/part-02/chapter-06/gradient-descent-loop.svg`의 update loop 영역 | 손실 곡선은 SVG로 유지하고, 현재 파라미터·그래디언트·학습률·업데이트 반복은 Mermaid로 분리했다. |

## SVG를 유지한 주요 유형

| 유형 | 예시 | 유지 이유 |
| --- | --- | --- |
| 수학 그래프 | `linear-slope-constant.svg`, `curve-slope-changing.svg` | 축, 선, 접선, 변화율 위치가 설명의 핵심이다. |
| 벡터·행렬 변환 | `matrix-multiplication-position-change.svg` | 좌표 위에서 위치가 바뀌는 모습을 보여야 한다. |
| 분포와 표본 변동 | `same-mean-different-variance.svg`, `sampling-variation-vs-bias.svg` | 점과 분포의 상대 위치가 핵심 설명이다. |
| 경사와 최적화 곡선 | `gradient-direction-loss-contour.svg`, `gradient-descent-loss-curve.svg` | 곡선, 방향, 이동 단계가 동시에 필요하다. |
| 서비스 판단 시각화 | `probability-score-decision-threshold.svg` | 점수, 정책, 결정이 분리된다는 시각적 배치가 본문 이해를 돕는다. |

## 후속 기준

- 새 도식을 만들 때는 `management/authoring/chart-guidelines.md`의 도구 선택 표를 먼저 확인한다.
- SVG로 만들기 전에 Mermaid, Markdown 표, Graphviz DOT로 충분한지 검토한다.
- SVG가 필요한 경우에도 텍스트 겹침, 화살표 머리, 색상 역할, 모바일 폭을 확인한다.
