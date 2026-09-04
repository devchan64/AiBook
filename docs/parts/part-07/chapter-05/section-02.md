# P7-5.2 Mira 정면 머리 기준 만들기

> Section ID: `P7-5.2`
> Version: `v2026.09.05`

같은 인물을 다음 단계에서 다시 사용할 때는 먼저 얼굴·머리 기준을 한 장으로 고정한다. 이 절은 캐릭터 **Mira**의 정면 머리 기준을 만들고, 이를 바탕으로 카메라 각도가 달라진 참조 묶음을 만든다. 전신·착장·자세는 [P7-5.3](section-03.md)에서 다룬다.

## Mira identity 계약을 먼저 고정한다

Mira는 매우 밝은 피치 피부, 부드러운 타원형 얼굴과 V자 턱선, 호박빛이 섞인 갈색 홍채, 짙은 petrol-teal의 볼륨 있는 턱 길이 단발을 가진 성인 여성 캐릭터다. [Mira identity 계약 JSON](../../../assets/part-07/chapter-05/p7-5-2-mira-identity-contract.json)은 얼굴·헤어·기본 착장만 정의하며, 자세·카메라·장면·출력 품질은 정의하지 않는다.

| 계약 필드 | Mira에 고정하는 정보 | 이 절에서 맡기지 않는 정보 |
| --- | --- | --- |
| `identity_description` | 피부색, 얼굴형, 코·입·눈 비율, 호박빛 갈색 홍채, 앞머리와 단발 실루엣 | 포즈, 카메라 방향, 전신 비례 |
| `rear_hair_identity` | 뒷머리 실루엣, 목덜미 헤어라인, 머리색 | 새로운 헤어스타일 생성 |

## BF16 정면 머리 생성

정면 머리 T2I 생성은 공식 `Qwen/Qwen-Image` BF16 가중치를 `sequential CPU offload`로 직접 호출한다. 참조 이미지를 넣지 않으므로, 이 한 장이 이후 모든 비교의 얼굴·헤어 기준이 된다.

![Qwen 정면 얼굴 기준](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)

[정면 얼굴 result.json — T2I 입력 조건과 출력 기록](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280-result.json)

[정면 얼굴 T2I Python 생성기](../../../assets/part-07/chapter-05/p7_5_2_generate_mira_head_bf16.py)

생성기는 얼굴 일러스트 계약과 Mira identity 계약, seed·step·CFG, 완성 PNG의 해시를 result JSON에 기록한다. 기본값은 1280px·30 step·CFG 4.0이다. 조건을 바꿀 때는 정수리 여백·양쪽 눈과 귀·홍채색·단발 실루엣이 유지되는지 확인한다.

[Mira identity·화풍·일러스트 계약 JSON](../../../assets/part-07/chapter-05/p7-5-2-mira-identity-contract.json)

### 정면 생성기가 고정하는 것과 바꿀 수 있는 것

생성기는 identity 계약의 얼굴·헤어 설명과 `rendering_contract`의 정면 일러스트 지시를 합쳐 prompt를 만든다. 여기에 정면 구도 지시를 덧붙여, 정수리·양쪽 눈·귀가 프레임 안에 들어오게 한다. 캐릭터 특징은 계약이 맡고, 정면 구도는 생성기가 맡는다.

| 구현 요소 | 코드에서 하는 일 | 학습할 때 확인할 점 |
| --- | --- | --- |
| 단일 계약 입력 | identity·화풍·일러스트 지시를 하나의 JSON에서 읽는다 | 특징이 여러 프롬프트 파일에 흩어지지 않아 수정 범위가 분명하다 |
| 고정 seed | `torch.Generator`에 같은 seed를 넣는다 | step·크기·CFG를 바꾼 비교에서 무작위 변동을 줄인다 |
| 결과 기록 | 입력 계약 해시, prompt, 모델, 크기, step, CFG, 출력 해시를 result JSON에 남긴다 | 좋은 한 장을 고르는 일과 같은 조건으로 다시 만드는 일을 구분할 수 있다 |
| 순차 CPU 오프로딩 | 필요한 모듈을 GPU와 CPU 사이에서 순차적으로 이동한다 | 8GB GPU에서도 실행 범위를 만들지만, 생성 시간은 늘어난다 |

`--steps`, `--size`, `--cfg`는 비교를 위한 조작값이다. 한 번에 하나만 바꾸고 result JSON을 남기면, 결과 차이를 모델의 무작위성보다 그 조건 변화에 더 가깝게 해석할 수 있다.

### 정면 기준에는 T2I 모델을 쓴다

`Qwen/Qwen-Image`는 텍스트 prompt에서 이미지를 만드는 기반 모델이다. 공식 모델 카드는 Diffusers와 BF16 실행 예시를 제공하며, 다양한 화풍의 이미지 생성을 지원한다고 설명한다. 이 절에서는 참조 이미지가 없는 정면 머리 기준을 만들 때만 사용한다. 따라서 입력 이미지의 우연한 구도나 의상 정보가 얼굴 기준에 섞이지 않는다.

모델 카드의 BF16 예시는 충분한 GPU 메모리를 전제로 한다. 이 생성기는 같은 BF16 가중치를 사용하되 `sequential CPU offload`를 적용한다. 이는 모델 자체의 품질 기능이 아니라, 제한된 VRAM에서 실행하기 위한 메모리 배치 전략이다. 속도와 VRAM 사용량은 서로 바꿔 얻는 조건이므로, 이 절의 1280px·30 step 결과를 모든 하드웨어에서의 권장 시간이자 품질 보증으로 해석하지 않는다.

## 상반신 기준에서 15방향 카메라 참조를 만든다

정면 머리 기준만 회전시키면 어깨와 이너탑을 새로 추측해야 한다. 그래서 정면 머리를 참조해 어깨가 보이는 상반신 기준 한 장을 먼저 만들고, 그 이미지만 `Picture 1`로 넣어 카메라 조건을 바꿨다. 이 단계는 새 포즈나 새 착장을 만드는 단계가 아니라, 이후 캐릭터 시트에서 비교할 **카메라 참조 묶음**을 만드는 단계다.

![Mira 정면 상반신 기준](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png)

[정면 상반신 기준 result JSON](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30-result.json)

`Qwen/Qwen-Image-Edit-2511`에 Multiple-Angles LoRA와 Lightning 4-step LoRA를 함께 적용한다. 카메라 prompt는 `<sks> [azimuth] [elevation] [distance]` 순서로 두며, 각 결과는 `640×640`, 같은 seed, 4 step으로 생성한다. 이렇게 조건을 고정하면 yaw와 수직 시점 변화가 캐릭터 특징과 어떻게 분리되는지 비교할 수 있다.

[상반신 15방향 Python 생성기](../../../assets/part-07/chapter-05/p7_5_2_qwen_edit_2511_generate_mira_torso_multiview.py)

생성기에서 `--sampling-profile lightning4 --size 640 --steps 4`를 선택한다. `--yaw`와 `--vertical`로 필요한 방향만 생성할 수 있다. 실제 입력·출력 조건은 각 이미지와 짝을 이루는 result JSON에서 확인한다.

### 카메라 참조에는 편집 모델과 두 LoRA를 쓴다

상반신 기준을 변형하는 단계는 텍스트만으로 새 얼굴을 만드는 작업이 아니라, 한 장의 입력을 유지하며 카메라 조건을 바꾸는 image-to-image 작업이다. 그래서 `Qwen/Qwen-Image-Edit-2511`을 사용한다. 공식 모델 카드는 이전 판보다 이미지 드리프트 완화와 캐릭터 일관성을 강화했다고 설명하며, 여러 이미지와 prompt를 함께 받는 Diffusers 예시도 제공한다. 여기서는 입력을 `Picture 1` 한 장으로 제한해, 그 이미지가 얼굴·헤어·어깨·이너탑의 기준 역할을 하게 한다.

Multiple-Angles LoRA는 `<sks> [azimuth] [elevation] [distance]`라는 정해진 카메라 문법을 추가한다. 이 절은 그중 전방 반원 다섯 yaw, 로우·아이레벨·엘리베이티드 세 수직 시점, medium shot만 선택한다. LoRA가 물체의 완전한 3D 모델을 만드는 것은 아니다. 표에서 identity나 배경이 흔들리면, 그 결과는 회전된 정답이 아니라 같은 입력에 카메라 조건을 적용했을 때의 후보로 검수해야 한다.

Lightning 4-step LoRA는 긴 확산 과정을 네 step으로 줄이는 속도 중심 어댑터다. 이 원고에서는 15개 방향을 빠르게 비교하기 위한 저비용 프로필로만 쓴다. 세부 묘사나 identity가 불안정하면 step 수가 적다는 조건을 먼저 의심하고, 정면 기준과 비교해 재생성 여부를 판단한다.

| 구성 | 이 절에서의 역할 | 고정하지 않는 것 |
| --- | --- | --- |
| `Qwen-Image` | 참조 없이 정면 머리 기준을 생성 | 후속 카메라 회전 |
| `Qwen-Image-Edit-2511` | 상반신 기준을 입력으로 받아 편집 | 각도를 수치적으로 완벽히 보장하는 3D 변환 |
| Multiple-Angles LoRA | yaw·수직 시점·거리의 카메라 문법 제공 | identity·배경·프레이밍의 완전한 보존 |
| Lightning 4-step LoRA | 15방향 비교 비용을 낮춤 | 고 step 품질과 동등한 결과 |

| 로우앵글 `−90°` | 로우앵글 `−45°` | 로우앵글 `0°` | 로우앵글 `+45°` | 로우앵글 `+90°` |
| --- | --- | --- | --- | --- |
| ![Mira 로우앵글 −90도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-90-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 로우앵글 −45도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 로우앵글 정면](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-zero-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 로우앵글 +45도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 로우앵글 +90도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-90-lowcost-v2-size-640x640-seed-62294-steps-4.png) |

| 아이레벨 `−90°` | 아이레벨 `−45°` | 아이레벨 `0°` | 아이레벨 `+45°` | 아이레벨 `+90°` |
| --- | --- | --- | --- | --- |
| ![Mira 아이레벨 −90도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 아이레벨 −45도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 아이레벨 정면](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-zero-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 아이레벨 +45도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 아이레벨 +90도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-lowcost-v2-size-640x640-seed-62294-steps-4.png) |

| 엘리베이티드 `−90°` | 엘리베이티드 `−45°` | 엘리베이티드 `0°` | 엘리베이티드 `+45°` | 엘리베이티드 `+90°` |
| --- | --- | --- | --- | --- |
| ![Mira 엘리베이티드 −90도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-90-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 엘리베이티드 −45도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 엘리베이티드 정면](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 엘리베이티드 +45도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-lowcost-v2-size-640x640-seed-62294-steps-4.png) | ![Mira 엘리베이티드 +90도](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-90-lowcost-v2-size-640x640-seed-62294-steps-4.png) |

세 행을 함께 보면 yaw와 수직 시점은 대부분 분리된다. 로우앵글 `−90°`처럼 프레이밍이 크게 흔들리는 결과는 캐릭터의 새 특징이 아니라, 카메라 조건을 바꿀 때 생긴 변형으로 읽는다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 계약 | result JSON에 Mira identity와 일러스트 계약의 경로·해시가 남아 있는가? |
| 정면 구도 | 정수리 전체, 양쪽 눈과 귀, 목선이 잘리지 않았는가? |
| identity | 피부·얼굴형·호박빛 갈색 홍채·petrol-teal 단발이 계약과 같은 인물로 읽히는가? |
| 재현 | seed, step, CFG, 크기와 오프로딩 조건이 result JSON에 남아 있는가? |

## 출처와 참고 자료

- 정면 얼굴 기준의 생성 조건과 해시는 이 절에서 연결한 local result JSON을 기준으로 확인한다.
- Qwen, [*Qwen-Image model card*](https://huggingface.co/Qwen/Qwen-Image){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-09-05.
- Qwen, [*Qwen-Image-Edit-2511 model card*](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-09-05.
- fal, [*Qwen-Image-Edit-2511 Multiple-Angles LoRA model card*](https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-09-05.
- lightx2v, [*Qwen-Image-Edit-2511 Lightning model card*](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-09-05.
