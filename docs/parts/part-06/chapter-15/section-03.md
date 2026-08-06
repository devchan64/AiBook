# P6-15.3 보충학습: 에이전트 워크플로와 이미지 생성 워크플로는 무엇이 다른가

> Section ID: `P6-15.3`
> Version: `v2026.08.03`

P6-15.1에서는 도구와 자원을 공통 형식으로 연결하는 관점을, P6-15.2에서는 실행을 기록하고 다시 설명하는 하네스 관점을 보았습니다. 이 보충 절은 그 둘을 다른 생성형 AI 장면에서도 다시 읽어 보기 위한 비교 지도입니다.

> 모두 workflow라고 부를 때, 어떤 흐름은 다음 행동을 고르고 어떤 흐름은 데이터와 조건을 변환하는가?

InvokeAI와 ComfyUI는 설치·버튼·노드 목록을 배우기 위한 대상이 아닙니다. 이미지 생성의 파이프라인을 눈에 보이게 해, 에이전트의 제어 흐름과 같은 말로 섞지 않기 위한 사례입니다. 실제 실행과 비교 기록은 Part 7의 생성형 이미지 모델 실습에서 다룹니다.

## workflow라는 말은 같은 구조를 가리키지 않는다

에이전트 워크플로는 목표와 중간 관찰을 보고 다음 행동을 바꾸는 **제어 흐름**입니다. 반면 이미지 생성 워크플로는 프롬프트, 참조 조건, 모델, 잠재 표현, 이미지 사이의 **데이터 변환 흐름**입니다.

| 구분 | 먼저 움직이는 것 | 핵심 질문 | 대표 기록 |
| --- | --- | --- | --- |
| 에이전트 workflow | 다음 행동 | 관찰 뒤에 검색·도구 호출·사람 검토 중 무엇으로 갈까 | goal, observation, next_action, stop_reason |
| 이미지 생성 workflow | 조건과 중간 표현 | 어떤 조건과 변환이 최종 이미지를 만들었나 | model, prompt, seed, control, output |
| harness | 실행의 설명 가능성 | 같은 실행과 실패를 다시 읽을 수 있나 | trace, environment, approval, replay |

따라서 노드가 여러 개라는 사실만으로 에이전트라고 부르면 안 됩니다. 이미지 생성 그래프는 정해진 데이터 경로를 실행할 수 있고, 에이전트는 실행 중 관찰에 따라 다음 경로 자체를 바꿀 수 있습니다.

## 이미지 생성 파이프라인을 최소 단위로 읽기

Stable Diffusion 계열의 최소 흐름은 아래처럼 적을 수 있습니다.

```text
prompt·참조 조건
-> text condition
-> latent와 반복 복원
-> 이미지 변환
-> 결과 검토와 실행 기록
```

이 흐름은 P5-15.4의 `텍스트 조건 -> 잠재 노이즈 -> 반복 복원 -> 이미지`를 실행 환경의 언어로 다시 적은 것입니다. 여기서는 각 모델의 정확한 내부 구현이나 특정 노드의 모든 인자를 설명하지 않습니다.

ComfyUI는 이런 흐름을 노드와 연결선으로 나타내는 환경입니다. 공식 문서도 workflow를 연결된 노드의 그래프로 정의하고, 이를 이미지 메타데이터나 JSON으로 저장할 수 있다고 설명합니다. [ComfyUI Workflow](https://docs.comfy.org/development/core-concepts/workflow){: target="_blank" rel="noopener noreferrer" }

InvokeAI는 Canvas와 워크플로 환경에서 이미지 생성·편집 과정을 다룹니다. Canvas 프로젝트는 레이어, 마스크, 참조 이미지, 생성 설정, LoRA를 하나의 프로젝트 파일로 저장할 수 있어, 어떤 조건에서 이미지를 비교했는지 남기는 사례로 볼 수 있습니다. [InvokeAI Canvas Projects](https://invoke.ai/features/canvas/canvas-projects/){: target="_blank" rel="noopener noreferrer" }

## 같은 workflow라는 말에서 먼저 분리할 것

| 장면 | 흐름을 읽는 방법 | 에이전트와 섞으면 생기는 오해 |
| --- | --- | --- |
| ComfyUI 노드 그래프 | 모델·조건·잠재 표현·이미지가 어떻게 이어지는지 본다 | 노드 연결 자체가 목표 판단이나 재계획을 한다고 느끼기 쉽다 |
| InvokeAI Canvas | 이미지 편집 조건과 결과 비교 상태를 본다 | Canvas 조작을 모델 내부 추론이나 에이전트 행동으로 혼동하기 쉽다 |
| AI 에이전트 | 관찰 뒤에 다음 도구·재시도·중단을 고르는지 본다 | 모든 다단계 실행을 같은 데이터 파이프라인으로 평평하게 볼 수 있다 |

두 이미지 환경은 생성 조건과 변환 경로를 드러내는 데 도움이 됩니다. 그러나 프롬프트를 받았다고 스스로 목표를 분해하거나, 결과를 보고 자율적으로 다음 도구를 고르는 구조가 자동으로 생기지는 않습니다.

## 파이프라인 카드를 남겨 보기

도구를 실행하기 전에 아래 다섯 칸을 먼저 채워 보면, 결과 이미지 한 장만 남기는 일을 피할 수 있습니다.

| 기록 칸 | 이미지 생성 파이프라인에서 적을 것 | 에이전트 파이프라인과 비교할 때 볼 것 |
| --- | --- | --- |
| 입력 | prompt, 참조 이미지, 마스크, seed | 목표와 현재 관찰이 구분되는가 |
| 변환 | model, LoRA, control, sampler, steps | 다음 행동 선택이 아니라 데이터 변환인가 |
| 출력 | 생성 이미지와 검토 기준 | 최종 답변 또는 실행 결과와 무엇이 다른가 |
| 변경 | 한 번에 하나만 바꾼 조건 | 어떤 관찰이 다음 행동을 바꾸었는가 |
| 재현 | workflow, 프로젝트 파일, 메타데이터 | trace와 replay에 무엇을 남겨야 하는가 |

이 카드는 모델이나 도구의 성능 순위를 매기기 위한 표가 아닙니다. 파이프라인의 어느 지점이 결과를 바꾸었는지, 그리고 다음 비교를 위해 무엇을 남겨야 하는지를 말로 설명하기 위한 최소 기록입니다.

## Part 7으로 넘기는 경계

- Part 6에서는 workflow의 종류, 연결·변환·기록의 역할을 비교합니다.
- Part 7에서는 ComfyUI나 InvokeAI 같은 실행 환경에서 실제 입력 하나를 바꾸고 결과 차이와 실패 신호를 기록합니다.
- 설치 방법, 커스텀 노드 목록, 특정 모델의 순위, 이미지 제작 요령은 이 절의 범위가 아닙니다.

## 체크리스트

- 에이전트 workflow와 이미지 생성 workflow가 각각 제어 흐름과 데이터 변환 흐름에 가깝다는 점을 구분할 수 있는가?
- ComfyUI·InvokeAI를 모델 자체가 아니라 파이프라인을 관찰하고 기록하는 실행 환경으로 설명할 수 있는가?
- 이미지 생성에서 입력, 변환, 출력, 변경, 재현 기록을 나누어 적을 수 있는가?
- 실제 도구 조작과 조건 비교 실습은 Part 7의 범위임을 설명할 수 있는가?

## 출처와 참고 자료

- ComfyUI, [Workflow](https://docs.comfy.org/development/core-concepts/workflow){: target="_blank" rel="noopener noreferrer" }, 공식 문서, 확인 날짜: 2026-08-03.
- ComfyUI, [Nodes](https://docs.comfy.org/development/core-concepts/nodes){: target="_blank" rel="noopener noreferrer" }, 공식 문서, 확인 날짜: 2026-08-03.
- InvokeAI, [Canvas Projects](https://invoke.ai/features/canvas/canvas-projects/){: target="_blank" rel="noopener noreferrer" }, 공식 문서, 확인 날짜: 2026-08-03.
