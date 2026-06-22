# 시각화 작성 원칙

차트와 다이어그램은 가능한 한 오픈소스 도구와 텍스트 기반 정의를 사용합니다. 원고 안에 시각화의 원본을 남겨두면 수정 이력이 명확하고, 정적 사이트 빌드와 배포 과정에서도 결과를 재현하기 쉽습니다.

## 기본 원칙

- 다이어그램은 우선 Mermaid 코드 블록으로 작성합니다.
- 간단한 비교와 수치 정리는 Markdown 표를 먼저 사용합니다.
- 데이터 기반 차트는 원본 데이터, 생성 스크립트, 결과 이미지를 함께 관리합니다.
- 복잡한 그림은 `docs/assets/` 아래에 SVG 또는 PNG로 저장하고, 가능하면 생성 원본도 함께 보관합니다.
- 외부 자료의 도식이나 차트를 재작성한 경우에도 출처를 남깁니다.

## 도구 선택 기준

| 목적 | 우선 도구 | 저장 방식 |
| --- | --- | --- |
| 개념 흐름, 모델 구조, 학습 순서 | Mermaid | Markdown 코드 블록 |
| 간단한 수치 비교 | Markdown 표 | Markdown |
| 데이터 기반 정적 차트 | Python 또는 Vega-Lite | 스크립트와 이미지 |
| 복잡한 시스템 구조 | Mermaid, Graphviz, PlantUML | 원본 코드와 SVG |
| 논문 그림 재구성 | 직접 작성한 SVG/PNG | 이미지와 출처 |

## Mermaid 예시

```mermaid
flowchart LR
  A[기초 복구] --> B[머신러닝]
  B --> C[딥러닝]
  C --> D[LLM과 생성형 AI]
  D --> E[프로젝트]
```

## 작성 규칙

다이어그램은 장식이 아니라 설명을 줄이기 위한 도구로 사용합니다. 본문에서 이미 충분히 설명한 내용을 단순히 다시 그리는 그림은 피하고, 관계, 순서, 비교, 구조를 빠르게 파악해야 할 때 추가합니다.

시각화 파일을 추가할 때는 다음 정보를 함께 남깁니다.

- 무엇을 설명하는 그림인지
- 어떤 데이터나 자료를 바탕으로 만들었는지
- 자동 생성인지 수작업 작성인지
- 외부 자료를 참고했다면 출처

## 출처와 참고 자료

- Material for MkDocs, "Diagrams", <https://squidfunk.github.io/mkdocs-material/reference/diagrams/>, 확인 날짜: 2026-06-22.
- PyMdown Extensions, "SuperFences", <https://facelessuser.github.io/pymdown-extensions/extensions/superfences/>, 확인 날짜: 2026-06-22.
