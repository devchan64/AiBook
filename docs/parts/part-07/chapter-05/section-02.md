# P7-5.3 컷신 생성: 참조 셋으로 pose·camera·장면 만들기

> Section ID: `P7-5.3`
> Version: `v2026.08.03`

`P7-5.1`의 화풍 참조 셋과 `P7-5.2`의 캐릭터 참조 셋이 승인된 뒤에만 컷신을 생성합니다. 이 절의 산출물은 한 장의 예쁜 그림이 아니라, pose·camera·장소·시간을 바꾼 전체 컷 후보와 각 후보의 구조·인물성·화풍 판정입니다. StoryDiffusion의 consistent self-attention은 여러 prompt 사이의 캐릭터 반복성을 목표로 하며 SD 1.5와 SDXL 기반 모델에 호환된다고 안내됩니다. 여기서는 ComfyUI를 전제로 하지 않고, SD 1.5 기반의 최소 probe를 컷신 생성 후보로 다룹니다.

## 최소 probe의 경계

| 고정 | 값 | 이유 |
| --- | --- | --- |
| 입력 | P7-5.1 화풍 참조 셋 + P7-5.2 캐릭터 참조 셋 및 승인한 생성 조건 | 장면만 바꾸고 기준 계약을 유지하기 위해 |
| base | P7-5.2에서 승인한 SD 1.5 + character LoRA | 기준 인물과 화풍을 바꾸지 않기 위해 |
| 이미지 조건 | 512 x 512, batch 1, 3 prompts | StoryDiffusion의 최소 prompt 수와 8 GB 경계 확인 |
| 사용 기능 | consistent self-attention만 | LoRA, IP-Adapter, ControlNet, inpaint 효과를 섞지 않기 위해 |
| 관찰 | peak VRAM, 시간, 얼굴·의상 반복성 | 실행 성공과 품질 통과를 분리하기 위해 |

공식 저메모리 Gradio 경로는 SDXL specific-ID 구성으로 24 GB GPU에서 시험됐고 20 GB 초과를 예상합니다. 따라서 이 절의 SD 1.5 probe는 8 GB에서의 통과가 확인된 제작 경로가 아니라, 별도로 측정해야 하는 후보입니다.

## Python으로 prompt 계약을 고정하기

세 prompt는 같은 identity 문장을 공유하고 scene·camera만 바꿉니다. 아래 코드에서 `identity_anchor`를 바꾸면 세 컷 전체의 기준이 바뀌며, `shots`를 바꾸면 구성 변화만 남습니다.

```python
identity_anchor = "mira_char, teal bob haircut, silver hair clip, white jacket, teal trousers"
shots = [
    ("bookstore aisle", "full body, eye-level"),
    ("subway platform", "three-quarter view, low angle"),
    ("rooftop at dusk", "medium shot, eye-level"),
]

prompts = [
    f"{identity_anchor}, {place}, {camera}, clean webtoon line art"
    for place, camera in shots
]

assert len(prompts) >= 3
for index, prompt in enumerate(prompts, start=1):
    print(f"panel-{index}: {prompt}")
```

실행 기록에는 각 PNG 파일, seed, model revision, LoRA weight, VRAM peak, 생성 시간을 남깁니다. 세 장이 출력돼도 얼굴·눈·앞머리·의상·camera를 참조 팩과 대조해 모두 통과해야 합니다.

## 중단 기준

8 GB에서 out-of-memory가 나거나, 세 컷의 큰 색상만 반복되고 얼굴·의상 기준이 흔들리면 이 경로는 중단합니다. ControlNet, IP-Adapter, inpaint를 붙여 결과를 고치지 않습니다. 보정은 P7-5.4의 별도 입력으로만 검증하며, 여기서는 컷신 생성 자체의 pose·camera·장면·인물성 판정을 남깁니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 기준 자산 | P7-5.2의 승인 참조 팩과 LoRA revision을 사용했는가? |
| 분리 | ControlNet, 참조 adapter, inpaint를 끈 상태인가? |
| 기록 | 세 prompt의 seed, 시간, VRAM peak, PNG를 모두 남겼는가? |
| 판정 | 실행 여부가 아니라 세 컷의 얼굴·의상 반복성으로 통과를 판정했는가? |

## 출처와 참고 자료

- Zhou et al., [StoryDiffusion official implementation](https://github.com/HVision-NKU/StoryDiffusion){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
