# P7-5.2 Mira 정면 머리 기준 만들기

> Section ID: `P7-5.2`
> Version: `v2026.09.03`

같은 인물을 다음 단계에서 다시 사용할 때는 먼저 얼굴·머리 기준을 한 장으로 고정한다. 이 절은 캐릭터 **Mira**의 정면 머리 기준을 text-to-image로 생성하고, 그 머리 한 장을 참조한 카메라 각도 실험의 입력·실행 조건을 `result.json`에 남긴다. 전신·착장·자세는 [P7-5.3](section-03.md) 이후의 별도 작업이다.

## Mira identity 계약을 먼저 고정한다

Mira는 매우 밝은 피치 피부, 부드러운 타원형 얼굴과 V자 턱선, 호박빛이 섞인 갈색 홍채, 짙은 petrol-teal의 볼륨 있는 턱 길이 단발을 가진 성인 여성 캐릭터다. [Mira identity 계약 JSON](../../../assets/part-07/chapter-05/p7-5-2-mira-identity-contract.json)은 얼굴·헤어·기본 착장만 정의하며, 자세·카메라·장면·출력 품질은 정의하지 않는다.

| 계약 필드 | Mira에 고정하는 정보 | 이 절에서 맡기지 않는 정보 |
| --- | --- | --- |
| `identity_description` | 피부색, 얼굴형, 코·입·눈 비율, 호박빛 갈색 홍채, 앞머리와 단발 실루엣 | 포즈, 카메라 방향, 전신 비례 |
| `rear_hair_identity` | 뒷머리 실루엣, 목덜미 헤어라인, 머리색 | 새로운 헤어스타일 생성 |
| `outfit_identity_description` | 후속 전신 작업에서 사용할 기본 착장 설명 | 옷의 가림 관계와 손·팔다리 형태 |
| `inner_top_identity` | 후속 착장 작업에서 사용할 이너탑의 색·핏·기장 | 헤어 색이나 카메라 변화 |

## BF16 정면 머리 생성

정면 머리 T2I 생성은 공식 `Qwen/Qwen-Image` BF16 가중치를 `sequential CPU offload`로 직접 호출한다. ComfyUI 서버·포트·HTTP 워크플로와 참조 이미지는 사용하지 않는다. 1280px·30 step 로컬 실행은 8GB GPU에서 완료됐지만, 생성 중 GPU 여유가 작으므로 다른 GPU 작업과 병행하지 않는다.

![Qwen 정면 얼굴 기준](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)

[정면 얼굴 result.json — T2I 입력 조건과 출력 기록](../../../assets/part-07/chapter-05/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280-result.json)

[정면 얼굴 T2I Python 생성기](../../../assets/part-07/chapter-05/p7_5_2_generate_mira_head_bf16.py)

생성기는 얼굴 일러스트 계약과 Mira identity 계약을 결합한 prompt, BF16·오프로딩 조건, seed·step·CFG, 완성 PNG의 해시를 result JSON에 기록한다.

```python
pipeline = QwenImagePipeline.from_pretrained(
    model_path, torch_dtype=torch.bfloat16, local_files_only=True
)
pipeline.enable_sequential_cpu_offload()
image = pipeline(
    prompt=prompt,
    generator=torch.Generator("cpu").manual_seed(args.seed),
    true_cfg_scale=args.cfg,
    num_inference_steps=args.steps,
    width=args.size,
    height=args.size,
).images[0]
```

기본값은 1280px·30 step·CFG 4.0이다. `--steps`, `--size`, `--cfg`를 바꿀 때는 결과에서 단순한 해상도 차이만 보지 말고, 정수리 여백·양쪽 눈·귀 노출·홍채색·단발 실루엣이 유지되는지 함께 확인한다.

[Mira identity 계약 JSON](../../../assets/part-07/chapter-05/p7-5-2-mira-identity-contract.json)

[얼굴 화풍 계약](../../../assets/part-07/chapter-05/p7-5-2-face-style-prompt-contract.json)

[일러스트 계약](../../../assets/part-07/chapter-05/p7-5-2-face-illustration-prompt-contract.json)

## 엘리베이티드 쿼터뷰를 머리 참조 한 장으로 실험한다

`Qwen-Image-Edit-2511`에 `fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA`를 로드해, Mira 정면 머리 기준만 Picture 1로 입력했다. 모델 카드의 토큰 순서 `<sks> [azimuth] [elevation] [distance]`를 그대로 사용하며, 이 실험의 prompt는 `<sks> front-left quarter view elevated shot medium shot`이다. [fal, *Qwen-Image-Edit-2511 Multiple-Angles LoRA model card*](https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA){: target="_blank" rel="noopener noreferrer"}

![Mira 엘리베이티드 좌전방 쿼터뷰 20 step](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-head-multiview-vertical-elevated-yaw-minus-45-steps20-v1-size-1280x1280-seed-62294-steps-20.png)

[엘리베이티드 좌전방 쿼터뷰 result.json — 단일 머리 참조·LoRA·카메라 토큰 기록](../../../assets/part-07/chapter-05/p7-5-2-qwen-2511-mira-head-multiview-vertical-elevated-yaw-minus-45-steps20-v1-size-1280x1280-seed-62294-steps-20-result.json)

[Mira 머리 15방향 Multiple-Angles 생성기](../../../assets/part-07/chapter-05/p7_5_2_qwen_edit_2511_generate_mira_head_multiview.py)

20 step은 10 step보다 선과 얼굴 디테일을 정리했지만, 단발 실루엣이 길어지고 참조에 없던 상반신·옷도 새로 그렸다. 따라서 이 결과는 카메라 토큰이 방향 변화를 유도하는지 관찰하는 실험 기록이지, Mira identity가 유지된 회전 기준으로 사용하지 않는다. 생성기는 수평 `−90°, −45°, 0°, +45°, +90°`와 수직 `low`, `level`, `elevated`의 15개 조합을 지원하며 기본 step은 20이다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 계약 | result JSON에 Mira identity와 일러스트 계약의 경로·해시가 남아 있는가? |
| 정면 구도 | 정수리 전체, 양쪽 눈과 귀, 목선이 잘리지 않았는가? |
| identity | 피부·얼굴형·호박빛 갈색 홍채·petrol-teal 단발이 계약과 같은 인물로 읽히는가? |
| 재현 | seed, step, CFG, 크기와 오프로딩 조건이 result JSON에 남아 있는가? |
| 범위 | 단일 머리 참조의 카메라 변환에서 새 상반신·옷·헤어가 생긴 경우, 이를 Mira identity 보존 결과로 해석하지 않았는가? |

## 출처와 참고 자료

- 정면 얼굴 기준의 생성 조건과 해시는 이 절에서 연결한 local result JSON을 기준으로 확인한다.
- Qwen, [*Qwen-Image model card*](https://huggingface.co/Qwen/Qwen-Image){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-08-29.
- fal, [*Qwen-Image-Edit-2511 Multiple-Angles LoRA model card*](https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA){: target="_blank" rel="noopener noreferrer"}, Hugging Face, 확인: 2026-09-03.
