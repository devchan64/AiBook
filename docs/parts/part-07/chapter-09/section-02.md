# P7-9.2 SAM 2로 이미지 입력 prompt와 segmentation 결과 비교하기

> Section ID: `P7-9.2`
> Version: `v2026.07.31`

비전 모델은 이미지를 통째로 보는 것처럼 보이지만, 실제 프로젝트에서는 어떤 입력을 주느냐에 따라 출력이 크게 달라집니다. 이 절에서는 SAM 2 같은 promptable segmentation 모델을 기준으로, 같은 이미지에 point prompt, box prompt, 추가 수정 prompt를 넣어 결과 mask가 어떻게 달라지는지 비교합니다.

목표는 segmentation 모델을 깊게 학습시키는 것이 아닙니다. Part 5에서 배운 입력 구조와 표현 학습을 실제 이미지 실습으로 다시 확인하는 것입니다. 같은 이미지라도 어디를 찍고 어떤 box를 주느냐에 따라 모델이 `무엇을 대상이라고 이해했는가`가 달라집니다.

## 무엇을 바꿀 것인가

| 비교 축 | 바꿀 값 | 읽어야 할 질문 |
| --- | --- | --- |
| prompt 종류 | point, box, point+box | 입력 prompt가 mask 범위를 어떻게 바꾸는가 |
| 대상 경계 | 분명한 물체, 겹친 물체 | 모델이 어디서 배경과 대상을 헷갈리는가 |
| 수정 prompt | positive point, negative point | 한 번의 결과를 어떻게 다시 좁히거나 넓히는가 |
| 이미지 조건 | 단순 배경, 복잡한 배경 | 입력 복잡도가 실패 양상을 어떻게 바꾸는가 |

## 실습 순서

1. 물체 하나가 분명한 이미지를 고릅니다.
   첫 실행은 좋은 결과를 얻기보다 입력 prompt와 출력 mask의 관계를 읽는 데 둡니다.

2. point prompt만 넣어 mask를 저장합니다.
   한 점만으로 모델이 어디까지 대상을 잡는지 봅니다.

3. 같은 이미지에 box prompt를 넣어 다시 저장합니다.
   box가 target 범위를 좁히는지, 아니면 주변 배경까지 끌어오는지 비교합니다.

4. 겹친 대상 이미지에서 같은 절차를 반복합니다.
   실패가 더 잘 보이는 이미지를 넣어야 비전 모델의 입력 의존성을 읽을 수 있습니다.

5. 결과를 `잘 됨/안 됨`이 아니라 `대상 누락`, `배경 포함`, `경계 흔들림`, `수정 prompt 필요`로 나눕니다.

## 최소 실행 예시

SAM 2는 checkpoint와 실행 환경 준비가 필요합니다. 여기서는 공식 예제 흐름에 맞춰 `image -> prompt -> mask`가 기록에 어떻게 남는지만 봅니다.

```python
import numpy as np
import torch
from PIL import Image
from sam2.sam2_image_predictor import SAM2ImagePredictor

image_file = "inputs/p7-9-2-desk-object.jpg"
image = np.array(Image.open(image_file).convert("RGB"))

predictor = SAM2ImagePredictor.from_pretrained("facebook/sam2-hiera-large")

with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
    predictor.set_image(image)

    point_coords = np.array([[420, 310]])
    point_labels = np.array([1])
    point_masks, _, _ = predictor.predict(
        point_coords=point_coords,
        point_labels=point_labels,
        multimask_output=True,
    )

    box = np.array([260, 160, 610, 480])
    box_masks, _, _ = predictor.predict(
        box=box,
        multimask_output=True,
    )
```

이 예제에서는 이미지 파일, point 좌표, box 좌표를 반드시 함께 남깁니다. mask 파일을 저장했다면 point 결과와 box 결과를 같은 이름 규칙으로 저장합니다.

```text
p7-9-2-desk-object-point-mask.png
p7-9-2-desk-object-box-mask.png
```

## 기록 양식

```text
run_id:
model:
image_file:
prompt_type:
prompt_coordinates:
target_object:
mask_file:
observed_error:
next_prompt_fix:
```

`observed_error`에는 `왼쪽 팔 일부 누락`, `배경 그림자 포함`, `겹친 물체를 하나로 묶음`처럼 눈으로 확인한 실패를 씁니다. 그래야 다음 prompt 수정이 열립니다.

## Part 1~6으로 되돌아가기

| 다시 확인할 개념 | 이 실습에서 보이는 장면 |
| --- | --- |
| Part 3의 샘플 단위 | 이미지 한 장 안에서도 target object를 어떻게 잡는지가 달라집니다. |
| Part 5의 입력 구조 | point와 box는 같은 이미지에 다른 입력 구조를 더합니다. |
| Part 5의 attention | 모델은 이미지 전체와 prompt 위치의 관계를 함께 봅니다. |
| Part 7의 실패 해석 | mask 실패를 다음 prompt 수정으로 연결해야 실습이 닫힙니다. |

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 이미지 조건 | 단순 이미지와 어려운 이미지를 모두 써 봤는가? |
| prompt 기록 | point 또는 box 좌표를 남겼는가? |
| mask 비교 | point 결과와 box 결과를 나란히 비교했는가? |
| 실패 분류 | 누락, 과포함, 경계 흔들림을 구분했는가? |
| 다음 수정 | 다음 prompt를 어떻게 바꿀지 적었는가? |

## 출처와 참고 자료

- Meta, [SAM 2 GitHub 저장소](https://github.com/facebookresearch/sam2){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
