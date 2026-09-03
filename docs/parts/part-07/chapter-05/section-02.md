# P7-5.2 캐릭터 멀티플 뷰 생성: identity 기준과 카메라 앵글 분리하기

> Section ID: `P7-5.2`
> Version: `v2026.09.03`

같은 인물의 얼굴을 여러 방향으로 만들 때, 정면 이미지와 회전 지시를 한 prompt 안에 모두 반복하면 헤어·이목구비·화풍이 쉽게 흔들린다. 이 절은 캐릭터 **Mira**를 정의하고, **정면 얼굴은 Mira identity 기준을 마련하고, 가슴 중간까지 포함한 체스트 참조는 얼굴·헤어·어깨 연결을 전달하며, 전용 다중 앵글 LoRA는 카메라 변환만 맡는** Qwen 경로를 기록한다. 전신·착장·body-only OpenPose는 [P7-5.3](section-03.md)에서 별도로 다룬다.

## Mira identity 계약을 먼저 고정한다

Mira는 매우 밝은 피치 피부, 가늘고 작은 타원형 얼굴과 V자 턱선, 호박빛이 섞인 갈색 홍채, 짙은 petrol-teal의 볼륨 있는 턱 길이 단발을 가진 성인 여성 캐릭터다. 공용 캐릭터 계약이라는 이름 대신 [Mira identity 계약 JSON](../../../assets/part-07/chapter-05/p7-5-2-mira-identity-contract.json)을 사용한다. 이 JSON은 Mira의 얼굴·헤어·기본 착장만 정의하며, 자세·카메라·장면·출력 품질은 정의하지 않는다.

| 계약 필드 | Mira에 고정하는 정보 | 이 절에서 맡기지 않는 정보 |
| --- | --- | --- |
| `identity_description` | 피부색, 얼굴형, 코·입·눈 비율, 호박빛 갈색 홍채, 앞머리와 단발 실루엣 | 포즈, 카메라 방향, 전신 비례 |
| `rear_hair_identity` | 뒷머리 실루엣, 목덜미 헤어라인, 머리색 | 새로운 헤어스타일 생성 |
| `outfit_identity_description` | 흰 크롭 재킷, 차콜 회색 크롭탑, 딥틸 와이드 팬츠, 흰 스니커즈 | 옷의 가림 관계와 손·팔다리 형태 |

`unsloth/Qwen-Image-GGUF`의 `qwen-image-Q4_K_S.gguf`로 Mira 정면 머리를 T2I 생성하는 코드는 P7-5.9의 저메모리 구성과 같은 관리형 모델 경로를 사용한다. 단, ComfyUI 서버·포트·HTTP 워크플로를 시작하지 않고 Comfy 노드를 하나의 Python 프로세스에서 직접 호출한다. GGUF transformer, FP8 텍스트 인코더, CPU VAE를 저메모리 정책으로 배치하며, 이 생성은 참조 이미지를 입력하지 않고 Mira 계약과 일러스트 계약만 prompt에 결합한다.

[Mira 머리 Q4 GGUF 직접 생성기](../../../assets/part-07/chapter-05/p7_5_2_generate_mira_head_q4_comfy_direct.py)

## 사용한 모델과 실행 구성

이 절에서 쓰는 구성은 하나의 모델이 모든 일을 하는 방식이 아니다. 정면 기준을 새로 그리는 모델, 기준 이미지를 편집하는 모델, 카메라 변화에 특화된 adapter를 역할별로 나눴다. `Diffusers`는 이 구성을 실행하는 파이프라인 구현이다. `Nunchaku`는 별도 이미지 생성 기반 모델이 아니라, Qwen transformer를 저정밀 가중치와 전용 runtime으로 로컬 GPU에서 실행하게 하는 구성이다.

| 구성 요소 | 이 절에서 맡은 역할 | 맡기지 않은 역할 |
| --- | --- | --- |
| `Qwen/Qwen-Image` | 이미지 입력 없이 Mira 정면 얼굴 기준을 text-to-image로 생성 | 얼굴 기준과 체스트 구도를 다중 참조로 결합 |
| `Qwen/Qwen-Image-Edit-2511` | 정면 얼굴 identity와 기존 체스트 프레이밍을 다중 참조로 결합해 이너탑을 포함한 체스트 기준을 생성 | 전신 착장·장면·카메라 회전을 한 번에 결정 |
| `Qwen/Qwen-Image-Edit-2509` | 체스트 기준 이미지를 받아 카메라 명령에 따라 image-to-image 편집 | 카메라 방향 자체를 정확한 3D 회전값으로 보정 |
| `dx8152/Qwen-Edit-2509-Multiple-angles` LoRA | 기반 편집 모델에 카메라 이동·회전·위아래 보기 명령에 반응하는 추가 경향 제공 | identity·헤어·화풍을 독립적으로 새로 정의 |
| Nunchaku FP4 transformer | `Qwen-Image-Edit-2509` 카메라 변환을 저정밀 가중치와 runtime으로 로컬 GPU에서 실행 | 출력의 identity·화풍·방향 품질을 보장 |

`Qwen-Image`는 Qwen이 공개한 text-to-image 기반 모델이며, 이 절에서는 참조가 없는 정면 기준을 만드는 데만 쓴다. `Qwen-Image-Edit-2511`은 정면 얼굴과 체스트 프레이밍 두 이미지를 순서대로 받아 새 체스트 기준을 만들며, 이너탑 표현은 prompt가 아니라 Mira identity 계약에서 읽는다. `Qwen-Image-Edit-2509`는 이 체스트 기준을 유지한 채 카메라 변화만 비교하는 다음 단계에 쓴다. 공식 모델 카드는 다중 이미지 입력과 인물 편집 일관성 개선을 설명하지만, 이 절의 결과는 로컬 실행 기록에서만 판단한다. [Qwen, *Qwen-Image model card* (Hugging Face, 확인: 2026-08-29)](https://huggingface.co/Qwen/Qwen-Image){: target="_blank" rel="noopener noreferrer"} [Qwen, *Qwen-Image-Edit-2511 model card* (Hugging Face, 확인: 2026-09-03)](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer"} [Qwen, *Qwen-Image-Edit-2509 model card* (Hugging Face, 확인: 2026-08-29)](https://huggingface.co/Qwen/Qwen-Image-Edit-2509){: target="_blank" rel="noopener noreferrer"}

다중 앵글 LoRA는 별도 생성 모델이 아니라 `Qwen-Image-Edit-2509` 위에 적용하는 adapter다. 따라서 이 절의 비교는 ‘LoRA가 인물을 다시 설계했다’가 아니라, 체스트 입력이 주는 identity·헤어·상반신 연결과 LoRA가 보강한 카메라 명령을 분리해 관찰하는 실험이다. 저정밀 transformer는 메모리 사용량을 다루는 실행 선택일 뿐, 품질의 원인으로 단정하지 않는다. 적용한 LoRA 가중치와 transformer 경로·해시는 각 result JSON에 남긴다. [dx8152, *Qwen-Edit-2509-Multiple-angles model card* (Hugging Face, 확인: 2026-08-29)](https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles){: target="_blank" rel="noopener noreferrer"} [Nunchaku AI, *nunchaku-qwen-image model card* (Hugging Face, 확인: 2026-08-29)](https://huggingface.co/nunchaku-ai/nunchaku-qwen-image){: target="_blank" rel="noopener noreferrer"} [Nunchaku AI, *nunchaku-qwen-image-edit-2509 model card* (Hugging Face, 확인: 2026-08-29)](https://huggingface.co/nunchaku-ai/nunchaku-qwen-image-edit-2509){: target="_blank" rel="noopener noreferrer"}

## 1. 정면 얼굴과 체스트가 서로 다른 기준을 제공한다

정면 얼굴은 참조 이미지 없이 Qwen으로 생성한 Mira 기준 이미지다. 중앙 정면 구도와 정수리 전체, 20대 초반 성인의 부드러운 타원형 얼굴 비율, 호박빛 갈색 홍채, petrol-teal 단발 실루엣을 대조하는 데 쓴다.

![Qwen 정면 얼굴 기준](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-q4ks-comfy-direct-young-adult-v1-seed-62294-steps-30-size-1280.png)

[정면 얼굴 result.json — T2I 입력 조건과 출력 기록](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-q4ks-comfy-direct-young-adult-v1-seed-62294-steps-30-size-1280-result.json)

[정면 얼굴 T2I Python 생성기](../../../assets/part-07/chapter-05/p7_5_2_generate_mira_head_q4_comfy_direct.py)

이 기준 이미지를 만드는 핵심 코드는 다음과 같습니다. 이 호출에는 참조 이미지가 없으므로 Qwen Image의 text-to-image 실행이며, ComfyUI 서버를 띄우지 않고 Comfy 노드를 한 Python 프로세스에서 직접 호출한다. 일러스트 계약과 Mira identity 계약만 결합하고, 정면 기준 PNG와 `result.json`을 한 쌍으로 기록한다.

```python
WEIGHT = ROOT / ".tmp/download/weight-unsloth-qwen-image-q4-ks-gguf/qwen-image-Q4_K_S.gguf"
DEFAULT_SIZE = 1280
DEFAULT_STEPS = 30

unet = classes["UnetLoaderGGUF"]().load_unet(WEIGHT.name)[0]
model = classes["ModelSamplingAuraFlow"]().patch_aura(unet, 3.0)[0]
clip = classes["CLIPLoader"]().load_clip(TEXT_ENCODER, "qwen_image", "default")[0]
vae = classes["VAELoader"]().load_vae(VAE)[0]
positive = classes["CLIPTextEncode"]().encode(clip, prompt())[0]
negative = classes["CLIPTextEncode"]().encode(clip, "")[0]
latent = classes["EmptySD3LatentImage"]().generate(args.size, args.size, 1)[0]
samples = classes["KSampler"]().sample(
    model, args.seed, args.steps, args.cfg, "euler", "simple", positive, negative, latent, 1.0
)[0]
image = vae.decode(samples["samples"])[0][0].cpu().numpy()
```

`result.json`에는 사용 모델, Mira identity 계약, 실행 조건과 완성 PNG 경로를 함께 기록한다. 본문 코드 발췌는 생성의 핵심을, 위 Python 원문과 실행 기록은 전체 조건을 제공한다.

정면 얼굴 생성의 기본값은 이 기준 이미지와 같은 1280px·30 step이다. 카메라 앵글 생성의 step 수까지 이 값으로 고정하지 않는다.

[Mira identity 계약 JSON](../../../assets/part-07/chapter-05/p7-5-2-mira-identity-contract.json)

[얼굴 화풍 계약](../../../assets/part-07/chapter-05/p7-5-2-face-style-prompt-contract.json)

[일러스트 계약](../../../assets/part-07/chapter-05/p7-5-2-face-illustration-prompt-contract.json)

가슴 중간까지 포함한 체스트 참조는 얼굴뿐 아니라 어깨·쇄골·상반신이 카메라 앵글 변화에서 어떻게 이어지는지 확인하기 위한 입력이다. 현재 카메라 앵글 생성기의 기본 입력으로 사용한다. 정면 Mira 얼굴은 첫 번째 참조, 기존 체스트 이미지는 프레이밍 전용 두 번째 참조이며, 회색 이너 크롭탑은 Mira identity 계약의 `inner_top_identity_description`으로 관리한다. 전신·재킷·바지·장면 조건은 이 파일에 넣지 않는다.

![Mira 이너탑 포함 체스트 정면 기준](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-front-identity-framing-gray-inner-top-multiref-v2-size-1280x1280-seed-62294-steps-10.png)

[체스트 정면 result.json — 다중 참조 입력과 이너탑 계약 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-torso-front-identity-framing-gray-inner-top-multiref-v2-size-1280x1280-seed-62294-steps-10-result.json)

[Qwen 2511 다중참조 체스트 생성기](../../../assets/part-07/chapter-05/p7_5_2_qwen_edit_2511_generate_mira_torso_multireference.py)

## 2. 카메라 변환은 LoRA와 한 축의 명령으로 분리한다

이 경로의 기반 편집 모델은 `Qwen/Qwen-Image-Edit-2509`이다. Qwen의 공식 모델 카드는 이 모델을 이미지-투-이미지 편집 모델로 제공하며, 단일 입력에서 사람 편집의 얼굴 identity 보존을 개선 대상으로 설명한다. 이 절에서는 그 성질을 보장된 결과로 받아들이지 않고, **정면 참조 한 장을 기준 입력으로 놓은 실제 출력에서만** 확인한다. [Qwen, *Qwen-Image-Edit-2509 model card* (Hugging Face, 확인: 2026-08-29)](https://huggingface.co/Qwen/Qwen-Image-Edit-2509){: target="_blank" rel="noopener noreferrer"}

카메라 조건에는 `dx8152/Qwen-Edit-2509-Multiple-angles` LoRA를 덧붙였다. 이 adapter의 모델 카드는 기반 모델을 `Qwen-Image-Edit-2509`로 표시하고, 별도 trigger word 없이 카메라 이동·좌우 회전·위아래 보기 명령을 사용할 수 있다고 안내한다. 같은 카드가 일관성이 불안정할 수 있다는 사용자 보고와 재학습본 업로드도 함께 남기므로, 모델 카드의 예시만으로 출력 성질을 일반화하지 않는다. [dx8152, *Qwen-Edit-2509-Multiple-angles model card* (Hugging Face, 확인: 2026-08-29)](https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles){: target="_blank" rel="noopener noreferrer"}

### 다중 앵글 LoRA는 카메라 제어용 adapter다

LoRA는 기반 모델 전체를 다시 저장한 독립 모델이 아니라, 일부 가중치에 작은 추가 갱신을 붙여 특정 작업으로 출력을 유도하는 parameter-efficient adapter 방식이다. 이 가중치는 `Qwen-Image-Edit-2509` 위에 함께 로드되며, 이 절에서는 **입력 이미지가 인물 identity·헤어·화풍을, 다중 앵글 LoRA가 카메라 명령에 반응하는 경향을** 맡도록 역할을 나눈다. [Hugging Face, *LoRA documentation* (확인: 2026-08-22)](https://huggingface.co/docs/peft/v0.20.0/package_reference/lora){: target="_blank" rel="noopener noreferrer"} [dx8152, *Qwen-Edit-2509-Multiple-angles model card* (확인: 2026-08-29)](https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles){: target="_blank" rel="noopener noreferrer"}

이 adapter가 `왼쪽으로 45도 회전` 같은 문장을 받는다고 해서, 이미지 안의 인물을 측정 가능한 3차원 공간에서 정확히 회전시키는 것은 아니다. 보이지 않던 귀·머리카락·어깨·배경은 편집 모델이 새로 합성해야 한다. 따라서 result JSON의 `yaw`와 `pitch`는 이 실험에서 비교하기 위한 **카메라 명령 라벨**이며, 실제 카메라의 보정된 물리 각도라는 뜻은 아니다. 방향이 맞더라도 identity나 헤어가 달라질 수 있는 이유도 여기에 있다.

| 제어 범주 | 모델 카드가 제시한 명령의 예 | P7-5.2에서의 처리 |
| --- | --- | --- |
| 이동 | 카메라를 앞·왼쪽·오른쪽·아래로 이동 | 화면 위치 변화가 함께 섞이므로 yaw·pitch 비교와 분리 |
| 좌우 회전 | 카메라를 왼쪽 또는 오른쪽으로 45°/90° 회전 | `yaw` 한 축으로만 생성 |
| 위·아래 보기 | 카메라를 위에서 내려다보거나 아래에서 올려다보기 | `pitch` 한 축으로만 생성 |
| 렌즈 | 광각 또는 클로즈업 | 프레이밍 변수가 추가되므로 현재 비교표에서는 제외 |

현재 로컬 실행기는 저정밀 Nunchaku transformer에 일반 PEFT 로더 대신 전용 `apply_lora` 처리를 사용한다. 적용된 transformer 모듈 수, LoRA 가중치 해시, 강도(`1.0`)를 result JSON에 남겨 가중치가 실제 적용되지 않은 실행과 구분한다. 또한 yaw·pitch·이동·렌즈를 한 prompt에 섞지 않고 한 축만 허용한다. 이는 복합 명령에서 화면 전체가 불안정하게 회전했던 이 실험의 관찰을 분리해 재현 가능하게 비교하기 위한 설계다.

카메라 앵글 생성에는 체스트 참조 한 장만 이미지 입력으로 넣는다. 이 입력이 identity·헤어·일러스트 표현과 어깨·상반신의 연결을 맡는다. 다중 앵글 LoRA와 짧은 중국어 카메라 명령은 yaw·pitch 변환만 맡는다. 얼굴 OpenPose, 전신 OpenPose, 착장 이미지는 이 경로에 넣지 않는다.

### 회전 축을 적용하는 코드

[Qwen 2509 다중 앵글 체스트 카메라 앵글 생성기](../../../assets/part-07/chapter-05/p7_5_2_qwen_camera_angle_2509_probe.py)

회전 실행기는 기준 체스트 이미지를 유일한 이미지 입력으로 읽고, `yaw` 또는 `pitch` 중 하나의 짧은 중국어 카메라 명령만 만든 뒤 LoRA를 적용한 `QwenImageEditPlusPipeline`에 넘깁니다. 다음 발췌에서 `camera_prompt_components()`는 다른 축을 빈 문자열로 남겨 복합 명령을 만들지 않으며, `result.json`에는 입력 이미지와 적용한 LoRA의 해시·축·값·출력 해시를 기록합니다.

```python
YAW_PROMPTS = {
    "quarter_right": "将镜头向右旋转45度。",
    "quarter_left": "将镜头向左旋转45度。",
    "profile_right": "将镜头向右旋转90度。",
    "profile_left": "将镜头向左旋转90度。",
}
PITCH_PROMPTS = {
    "high_angle": "将镜头转为俯视。",
    "level": "",
    "low_angle": "将镜头转为仰视。",
}

prompt_components = camera_prompt_components(args.axis, value)
prompt = build_camera_prompt(args.axis, value)  # yaw 또는 pitch 한 축
image = pipeline(
    prompt=prompt,
    image=[load_image(str(reference_image)).convert("RGB")],
    generator=torch.Generator("cpu").manual_seed(args.seed),
    true_cfg_scale=4.0,
    guidance_scale=1.0,
    negative_prompt=" ",
    num_inference_steps=args.steps,
    width=SIZE[0],
    height=SIZE[1],
).images[0]
image.save(output)

record = {
    "inputs": [asset_record(reference_image)],
    "input_roles": ["reference_identity_and_illustration"],
    "angle_lora": {"repository": ANGLE_LORA_REPO, "weight": asset_record(angle_lora)},
    "axis": args.axis,
    "axis_value": value,
    "prompt_components": prompt_components,
    "output": asset_record(output),
}
result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\\n")
```

| 입력 또는 조건 | 맡는 역할 | 맡지 않는 역할 |
| --- | --- | --- |
| 정면 얼굴 기준 | identity, 홍채, 앞머리·볼륨 단발, 선·음영의 기준 관찰 | 카메라 각도·상반신 연결 |
| 체스트 정면 참조 | identity·헤어·화풍, 회색 이너 크롭탑, 어깨·상반신 연결 | 전신·재킷·바지·장면 조건 |
| 다중 앵글 LoRA | 카메라 yaw·pitch | 다른 인물의 얼굴·헤어를 새로 정의하는 일 |
| 짧은 카메라 명령 | 좌·우 45°/90°, 위·아래 각도 | identity 설명의 반복 |

이 분리는 정면 얼굴을 길게 설명해 회전을 강제하는 방법보다 어느 조건이 실패했는지 구분하기 쉽다.

정면 얼굴을 먼저 기준으로 만들고, 이를 바탕으로 체스트 참조를 준비한다. 카메라 변환에서는 yaw와 pitch를 한 번에 섞지 않는다. `pitch 0°`에서 yaw를 먼저 비교하거나, `yaw 0°`에서 만든 high/low 체스트를 새 입력으로 두고 yaw를 적용한 뒤, 같은 네 축으로 결과를 읽는다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-2-chest-camera-angle-workflow-ko.mmd"
```

## 3. 체스트 기준 카메라 앵글 결과를 비교한다

아래 결과는 체스트 생성기를 교체하기 전에, 기존 1024 정면 체스트 참조만을 입력으로 쓴 8-step 카메라 비교 기록이다. 따라서 이 표는 현재 기본 체스트 기준의 검증 결과가 아니라 yaw·pitch를 한 축씩 분리했을 때의 비교 이력으로 읽는다. 먼저 `pitch 0°`에서 yaw를 비교하고, 다음으로 `yaw 0°`에서 pitch를 비교한다. 마지막으로 high/low 체스트 이미지를 새 입력으로 써 yaw를 적용한 결과를 확인한다. 기존 얼굴 전용 회전 이미지는 이 비교의 근거로 사용하지 않는다.

### 3.1 정면 체스트에서 yaw만 바꾸기 (`pitch 0°`)

이 절의 `좌측`과 `우측`은 **기준 정면에서 카메라가 왼쪽 또는 오른쪽으로 회전한 명령**을 뜻한다. 인물이 화면에서 어느 쪽을 바라보는지와 같은 뜻으로 쓰지 않는다. 따라서 `yaw -90°` 결과의 인물이 화면 오른쪽을 향해 보여도 표기 오류가 아니다.

| 좌측 측면 `yaw −90°` | 좌측 쿼터 `yaw −45°` | 정면 `yaw 0°` |
| --- | --- | --- |
| ![체스트 기준 좌측 측면 결과](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-profile-left-cfg4-yaw-1024-v4-seed-62294-steps-8.png) | ![체스트 기준 좌측 쿼터 결과](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-left-cfg4-yaw-1024-v4-seed-62294-steps-8.png) | ![체스트 정면 결과](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-front-cfg4-front-1024-v4-seed-62294-steps-8.png) |

| 우측 쿼터 `yaw +45°` | 우측 측면 `yaw +90°` |
| --- | --- |
| ![체스트 기준 우측 쿼터 결과](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-right-cfg4-yaw-1024-v4-seed-62294-steps-8.png) | ![체스트 기준 우측 측면 결과](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-profile-right-cfg4-yaw-1024-v4-seed-62294-steps-8.png) |

[좌측 쿼터 result.json — `yaw -45°` 실행 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-left-cfg4-yaw-1024-v4-seed-62294-steps-8-result.json)

[우측 쿼터 result.json — `yaw +45°` 실행 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-right-cfg4-yaw-1024-v4-seed-62294-steps-8-result.json)

[좌측 측면 result.json — `yaw -90°` 실행 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-profile-left-cfg4-yaw-1024-v4-seed-62294-steps-8-result.json)

[우측 측면 result.json — `yaw +90°` 실행 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-profile-right-cfg4-yaw-1024-v4-seed-62294-steps-8-result.json)

이 실행의 다섯 결과에서는 청록색 머리와 주황색 홍채라는 정면 기준의 큰 특징은 대체로 남아 있지만, 측면으로 갈수록 머리 외곽과 앞머리의 가림, 얼굴 윤곽은 달라진다. 즉 카메라 방향의 변화는 읽을 수 있어도, `yaw` 지시만으로 같은 인물의 세부 특징이 보존되었다고 판단할 수는 없다.

여러 방향의 체스트 참조를 미리 만드는 이유는 이후 장면의 카메라와 가까운 방향을 입력으로 선택하기 위해서다. 정면 한 장만 쓸 때보다 측면 윤곽, 앞머리의 가림, 귀·목·어깨의 연결 단서를 직접 제공할 수 있어 모델이 새 얼굴·헤어 구조를 추측해야 하는 범위를 줄인다. 따라서 캐릭터 재현 성공률을 높일 가능성이 있다. 다만 이는 품질 보장이 아니다. 실제 장면에서는 identity·화풍·의상·구도가 함께 유지되는지 별도로 관찰한다.

### 3.2 정면 체스트에서 pitch만 바꾸기 (`yaw 0°`)

| 하이앵글 | 로우앵글 |
| --- | --- |
| ![체스트 정면 기준 하이앵글 결과](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-pitch-high-angle-front-pitch-v6-seed-62294-steps-8.png) | ![체스트 정면 기준 로우앵글 결과](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-pitch-low-angle-front-pitch-v6-seed-62294-steps-8.png) |

[하이앵글 result.json — `pitch high` 실행 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-pitch-high-angle-front-pitch-v6-seed-62294-steps-8-result.json)

[로우앵글 result.json — `pitch low` 실행 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-pitch-low-angle-front-pitch-v6-seed-62294-steps-8-result.json)

### 3.3 pitch 결과를 새 입력으로 두고 yaw 적용하기

pitch와 yaw를 한 prompt에 결합하지 않는다. 먼저 만든 high/low 체스트 이미지는 입력 이미지 역할을, 좌·우 쿼터는 카메라 명령 역할을 맡는다.

| 하이앵글 체스트 → 좌측 쿼터 `yaw −45°` | 하이앵글 체스트 → 우측 쿼터 `yaw +45°` |
| --- | --- |
| ![하이앵글 정면 기준 좌측 쿼터](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-left-high-angle-front-v6-yaw-v3-seed-62294-steps-8.png) | ![하이앵글 정면 기준 우측 쿼터](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-right-high-angle-front-v6-yaw-v3-seed-62294-steps-8.png) |

| 로우앵글 체스트 → 좌측 쿼터 `yaw −45°` | 로우앵글 체스트 → 우측 쿼터 `yaw +45°` |
| --- | --- |
| ![로우앵글 정면 기준 좌측 쿼터](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-left-low-angle-front-v6-yaw-v3-seed-62294-steps-8.png) | ![로우앵글 정면 기준 우측 쿼터](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-right-low-angle-front-v6-yaw-v3-seed-62294-steps-8.png) |

[하이앵글 좌측 쿼터 result.json — high 입력의 `yaw -45°` 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-left-high-angle-front-v6-yaw-v3-seed-62294-steps-8-result.json)

[하이앵글 우측 쿼터 result.json — high 입력의 `yaw +45°` 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-right-high-angle-front-v6-yaw-v3-seed-62294-steps-8-result.json)

[로우앵글 좌측 쿼터 result.json — low 입력의 `yaw -45°` 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-left-low-angle-front-v6-yaw-v3-seed-62294-steps-8-result.json)

[로우앵글 우측 쿼터 result.json — low 입력의 `yaw +45°` 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-torso-yaw-quarter-right-low-angle-front-v6-yaw-v3-seed-62294-steps-8-result.json)

세 표를 함께 보면 카메라 명령은 옆얼굴의 실루엣과 위·아래에서 보이는 얼굴 비율을 바꾸지만, 그 과정에서 앞머리 묶음과 얼굴 윤곽도 함께 흔들린다. 따라서 다방향 결과는 다음 장면에 쓸 수 있는 참조 후보이지, 정면 기준의 헤어스타일·이목구비·화풍이 자동으로 보존된다는 증거는 아니다.

## 4. 출력은 네 축으로 비교한다

| 항목 | 확인할 질문 |
| --- | --- |
| 방향 | 코끝, 가까운 쪽 눈·볼, 귀와 머리카락의 가림이 요청한 쿼터·측면 방향과 맞는가? |
| 얼굴 identity | 정면 기준과 얼굴 폭, 눈 간격, 코선, 홍채색이 같은 인물로 읽히는가? |
| 헤어·상반신 연결 | 청록·검정 색 분할, 앞머리, 볼륨, S웨이브와 안쪽 컬, 목·어깨·가슴 위 경계가 유지되는가? |
| 화풍 | 체스트 기준의 선, 대비, 음영이 단순화되거나 사진풍으로 바뀌지 않았는가? |

방향만 맞고 머리카락·상반신 연결이나 이목구비가 달라진 출력과, 닮았지만 카메라 방향이 달라진 출력을 구분해 읽는다. 이 비교는 다음에 step·LoRA 강도·명령 문구를 한 축씩 바꾸는 근거로 남긴다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 기준 | 정면 얼굴 기준과 체스트 입력의 역할이 구분되어 있고, result JSON에 각각 남아 있는가? |
| 역할 | identity·헤어·화풍의 기준은 정면 얼굴에, 카메라 변환의 입력은 체스트에, yaw·pitch는 LoRA와 카메라 명령에 분리되어 있는가? |
| 방향 | 요청한 카메라 변환과 얼굴·목·어깨의 가림 관계가 같은 방향을 가리키는가? |
| 재현 | seed, step, LoRA, prompt와 `prompt_word_count`가 result JSON에 남아 있는가? |
| 범위 | 체스트 참조에 없는 전신·재킷·바지·장면 조건을 결과에 덧붙여 해석하지 않았는가? |
| 다음 단계 | 관찰된 역할과 한계를 기록한 뒤에만 P7-5.3 전신 또는 P7-5.4 장면 실험의 입력으로 쓰는가? |

## 출처와 참고 자료

- 정면 얼굴 기준의 생성 조건은 이 절에서 연결한 local 실행 기록을 기준으로 확인한다.
- 체스트 참조와 yaw·pitch 카메라 앵글 결과의 입력·출력 해시는 각 local result JSON을 기준으로 확인한다.
- 다중 앵글 LoRA의 저장소·가중치 정보는 result JSON에 기록한다. 외부 가중치는 재배포하지 않는다.
- Qwen, [*Qwen-Image model card*](https://huggingface.co/Qwen/Qwen-Image){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-08-29.
- Qwen, [*Qwen-Image-Edit-2511 model card*](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-09-03.
- Hugging Face, [*LoRA documentation*](https://huggingface.co/docs/peft/v0.20.0/package_reference/lora){: target="_blank" rel="noopener noreferrer"}, 확인: 2026-08-22.
- Qwen, [*Qwen-Image-Edit-2509 model card*](https://huggingface.co/Qwen/Qwen-Image-Edit-2509){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-08-29.
- dx8152, [*Qwen-Edit-2509-Multiple-angles model card*](https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-08-29.
- Nunchaku AI, [*nunchaku-qwen-image model card*](https://huggingface.co/nunchaku-ai/nunchaku-qwen-image){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-08-29.
- Nunchaku AI, [*nunchaku-qwen-image-edit-2509 model card*](https://huggingface.co/nunchaku-ai/nunchaku-qwen-image-edit-2509){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-08-29.
- Hugging Face, [*Diffusers GGUF quantization documentation*](https://huggingface.co/docs/diffusers/quantization/gguf){: target="_blank" rel="noopener noreferrer"}, GGUF transformer를 `from_single_file`로 직접 읽는 구성 참고, 확인: 2026-09-03.
