# Part 7: 8 GB 기반 웹툰 컷 생성 세 실험 가능성 검토

확인일: 2026-08-02

## 결론

세 실험은 **순서대로 수행할 때** 8 GB VRAM에서 검토할 수 있다. 그러나 외부 사례가 보여 주는 완성형 만화 생성 경로를 그대로 가져올 수는 없다. StoryDiffusion의 저메모리 구현은 공식적으로 20 GB 초과 GPU를 예상하고, PhotoMaker는 최소 11 GB를 제시한다. 이 두 도구는 품질 목표의 참고 사례이지 현재 장비의 실행 수단이 아니다.

| 실험 | 8 GB 가능성 | 외부 사례가 뒷받침하는 부분 | 현 장비에서의 제한 | 판정 |
| --- | --- | --- | --- | --- |
| 1. 화풍·캐릭터 고정 sheet | **조건부 가능** | SD 1.x LoRA 학습·생성과 inpainting은 공개 구현이 있으며, LoRA는 동결 base에 작은 adapter만 학습한다. | 자동으로 완전한 다각도 sheet를 보장하는 모델은 8 GB에서 확인되지 않았다. 승인 원본과 held-out 검증이 먼저 필요하다. | `실행 후보` |
| 2. SD 1.5 StoryDiffusion 최소 probe | **미검증 후보** | consistent self-attention은 SD 1.5/SDXL 기반 모델과 호환되고, 다중 prompt의 반복성을 목표로 한다. | 공식 저메모리 경로는 20 GB 초과 GPU를 예상한다. 8 GB의 SD 1.5 경로는 실제 peak VRAM과 품질을 별도로 측정해야 한다. | `최소 probe만` |
| 3. LoRA 기반 최종 cut-scene | **조건부 가능** | SD 1.5 ControlNet은 pose, depth, line, segmentation 조건을 받으며 ComfyUI는 전처리와 ControlNet 적용을 분리한다. | 8 GB에서 다중 ControlNet, 여러 identity adapter, 고해상도 inpaint를 한 번에 쓰는 구성은 검증되지 않았다. | `단일 ControlNet부터 검증` |

따라서 이 작업의 “가능”은 세 실험이 순서대로 PNG와 검수 기록을 낼 수 있다는 뜻이다. 동일 인물·화풍·동작·camera가 자동으로 통과한다는 뜻은 아니다.

## 외부 사례와 현재 장비의 경계

### 캐릭터 일관성 사례

- [StoryDiffusion](https://github.com/HVision-NKU/StoryDiffusion)는 SD 1.5/SDXL 기반 장거리 캐릭터 일관성과 comic generation을 목표로 한다. 다만 제공하는 low-memory 경로도 20 GB 초과 GPU를 예상한다. 따라서 **일관성 평가 기준**으로 참고하되 8 GB 기본 경로로 채택하지 않는다.
- [PhotoMaker V2](https://github.com/TencentARC/PhotoMaker)는 여러 ID 입력, LoRA 및 ControlNet 결합을 안내하지만 공식 최소 GPU 메모리가 11 GB다. 다각도 얼굴 reference를 하나의 identity 입력으로 다루는 사례이지만 현재 장비에서는 실행하지 않는다.
- [Diffusers LoRA 학습 문서](https://huggingface.co/docs/diffusers/main/training/lora)와 [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts)는 SD 1.x LoRA 학습을 지원한다. LoRA는 base model 전체가 아니라 adapter를 학습하므로 현재 8 GB에서 시도할 개인화 경로는 SDXL·FLUX보다 SD 1.5가 우선이다. Diffusers의 예시 완주 환경은 11 GB RTX 2080 Ti이므로, 8 GB 통과는 반드시 실제 peak VRAM으로 다시 확인한다.

### 콘티와 pose data 사례

- [Story2Board](https://github.com/DavidDinkevich/Story2Board)는 off-the-shelf LLM으로 자유 서사를 panel-level prompt로 바꾸는 training-free storyboard 생성 사례다. 이 결과는 LLM을 **콘티 구조화 도구**로 쓰는 근거이며, 인체 관절 생성의 근거는 아니다.
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)는 body, face, hand, foot을 합쳐 최대 135 keypoint를 검출하고 JSON 저장을 지원한다. CPU-only를 포함한 실행 경로를 제공하므로 pose image·JSON을 만드는 단계는 8 GB 생성 GPU의 핵심 병목이 아니다.
- [MotionGPT](https://github.com/OpenMotionLab/MotionGPT)는 text-to-motion 결과를 `(nframe, 22, 3)`으로 낸다. 이는 자연어가 동작 후보를 만들 수 있다는 사례지만, 기존 실제 검토에서 22-joint 보행이 사람 눈에 자연스럽지 않았다. 따라서 MotionGPT나 LLM output은 **후보 pose source**일 뿐, OpenPose control image로 쓰기 전 사람 검수 대상이다.

### ControlNet 최종 컷 사례

- [ControlNet 공식 구현](https://github.com/lllyasviel/ControlNet)은 SD 1.5와 human pose, depth, edge, segmentation 등 조건별 예제를 제공한다. pose는 OpenPose로 인식한 입력 이미지를 쓰는 경로가 명시돼 있다.
- [ComfyUI ControlNet 예제](https://docs.comfy.org/tutorials/controlnet/controlnet)와 [전처리 workflow](https://docs.comfy.org/tutorials/utility/preprocessors)는 pose, depth, lineart 등 전처리와 generation을 분리하고 ControlNet을 연결하는 workflow를 제시한다. 이는 control image를 독립 자산으로 기록하고 on/off baseline을 비교하는 근거다.
- [ComfyUI inpainting 문서](https://docs.comfy.org/tutorials/basic/inpaint)는 mask 기반 국소 보정을 별도 VAE conditioning으로 다룬다. 따라서 얼굴·손·배경 오류를 구조 오류와 분리하는 현재 전략에 맞는다.

## ComfyUI로 StoryDiffusion을 쓰는 경우

### 판정: 현재 8 GB VRAM의 기본 경로로는 미채택

`ComfyUI를 쓰면 StoryDiffusion이 8 GB에서 실행된다`는 결론을 뒷받침하는 공식 근거는 없다. ComfyUI는 workflow와 모델을 관리하는 실행 환경이고, StoryDiffusion의 consistent self-attention과 ID 관련 추가 모델의 VRAM 요구를 없애지는 않는다.

| 구성 | 확인한 근거 | 8 GB 판정 |
| --- | --- | --- |
| StoryDiffusion 공식 low-VRAM Gradio (SDXL specific-ID 경로) | 공식 저장소는 이 경로를 Tesla A10 24 GB에서 시험했고 20 GB 초과 GPU에서 잘 동작할 것으로 예상한다고 적는다. | **이 경로는 불가로 간주.** 8 GB 실행 근거 없음 |
| StoryDiffusion 공식 consistent self-attention + SD 1.5 | 공식 저장소는 consistent self-attention이 SD 1.5와 SDXL 기반 diffusion model에 호환된다고 명시하고, 최소 3개 prompt를 요구한다. | **미검증 최소 probe 후보.** SDXL보다 작지만 8 GB VRAM, ComfyUI, ControlNet 결합의 공식 실행 기록은 없음 |
| `smthemex/ComfyUI_StoryDiffusion` | 원 저자가 아닌 ComfyUI custom node이며 StoryDiffusion 외 PhotoMaker, MS-Diffusion, StoryMaker 등 여러 ID 방법을 묶는다. | **실행 환경일 뿐 메모리 해결책 아님.** 방법별 요구량을 따로 봐야 함 |
| 같은 계열 ComfyUI node의 StoryMaker + ControlNet | 저장소가 ControlNet 결합 시 VRAM 12 GB 미만에서 OOM 가능성을 명시한다. 12 GB CPU offload 단일 이미지 실행 기록도 약 317.6초다. | **8 GB에서 ControlNet 결합 불가로 간주.** 다운로드·설치 실험을 우선하지 않음 |
| 일반 ComfyUI SD 1.5 + ControlNet | ComfyUI 공식 문서는 전처리된 control image와 하나의 ControlNet workflow를 별도 모델로 구성하는 방법을 제공한다. | **실험 가능 후보.** StoryDiffusion node 없이 E3의 baseline으로 사용 |

공식 [StoryDiffusion 저장소](https://github.com/HVision-NKU/StoryDiffusion)는 consistent self-attention이 SD 1.5와 SDXL에 호환된다고 명시하지만, low GPU-memory로 공개한 것은 SDXL specific-ID 경로이며 이는 24 GB GPU에서 시험되고 20 GB 초과를 권장한다. [ComfyUI_StoryDiffusion 계열 custom node](https://github.com/wswszhys/ComfyUI_StoryDiffusion)는 StoryMaker에서 ControlNet을 결합하면 VRAM 12 GB 미만 OOM 가능성을 적고, 주 `story-diffusion` 기능에 SDXL model을 선택하도록 안내한다. custom node가 적는 `regular SD1.5` 지원은 ComfyUI 일반 workflow를 연결한다는 뜻이며, SD 1.5 StoryDiffusion attention 경로의 8 GB 통과 근거는 아니다.

따라서 현재 장비에서 StoryDiffusion의 SDXL/PhotoMaker/StoryMaker/ControlNet 결합을 설치해 큰 모델을 내려받거나 CPU offload로 장시간 실행하는 실험은 하지 않는다. 이를 실행해도 `실행됐다`는 사실이 character sheet, pose, camera, inpaint 품질 통과를 증명하지 못하며, 기존 Qwen·FLUX 저메모리 probe처럼 대용량 다운로드와 OOM 위험만 반복할 가능성이 높다.

반대로 **SD 1.5 base만 쓰는 StoryDiffusion 최소 probe**는 별도 후보로 남긴다. 조건은 `512 x 512`, batch 1, 3개 prompt, consistent self-attention만, LoRA·IP-Adapter·ControlNet·inpaint 없음이다. 이 probe의 목적은 character sheet나 웹툰 컷 제작이 아니라 `peak VRAM`, 3개 prompt에서의 큰 외형 반복성, 실행 시간만 확인하는 것이다. PNG가 나오더라도 3개 prompt의 얼굴·의상·camera를 사람 검수로 통과하지 못하면 다음 단계로 넘기지 않는다.

### 8 GB 대안

1. SD 1.5 StoryDiffusion 최소 probe가 통과하기 전까지 StoryDiffusion의 목표인 장거리 캐릭터 일관성은 **평가 기준**으로만 가져온다.
2. E1에서는 승인 character reference pack과 SD 1.5 LoRA의 held-out identity 비교를 한다.
3. E2에서는 LLM shot contract와 OpenPose/depth/line control data를 독립 자산으로 만든다.
4. E3에서는 일반 ComfyUI의 `SD 1.5 + character LoRA + ControlNet 1개`로 먼저 구조와 identity를 비교한다. 이 결과가 통과하기 전에는 StoryDiffusion custom node, 두 번째 ControlNet, PhotoMaker/IP-Adapter를 추가하지 않는다.

## 실험 1: 화풍·캐릭터 고정 sheet

### 질문

자체 제작 캐릭터를 여러 camera와 pose에서 비교할 수 있을 만큼, 전신·face·의상·화풍 기준을 고정할 수 있는가?

### 8 GB 실험 설계

1. 권리가 확인된 원본에서 `character reference pack`의 전신 turnaround 5장, face sheet 5장 이상, 의상·소품·style sheet를 만든다. 이 단계의 생성 후보는 자동 승인하지 않고 사람이 선별·직접 보정한다.
2. 이 중 승인한 16-32장을 학습용으로 사용하고, 3/4 전신·다른 장소·다른 표정을 held-out으로 남긴다. 같은 정면 crop의 복제본은 데이터 수로 세지 않는다.
3. SD 1.5 호환 base에서 batch 1, 512 계열 해상도, mixed precision, gradient checkpointing으로 character LoRA 실행 성립을 먼저 확인한다. style anchor는 character anchor와 분리해 한 번에 하나만 바꾼다.
4. LoRA 없음/있음의 같은 seed, prompt, camera 조건 비교를 만들고, held-out view에서 얼굴형·눈·앞머리·hair clip·의상·신발을 character reference pack과 대조한다.

### 성공과 중단 기준

- 성공: 전신과 face sheet의 필수 view가 승인되고, LoRA가 학습에 없던 3/4 view·장소에서도 identity와 style 항목을 함께 유지한다.
- 중단: 원본 pack에 복제 인물, 잘린 발, 각도별 얼굴 불일치가 남아 있거나, 학습 loss만 낮고 held-out identity가 흔들린다. 이 경우 LoRA rank나 step을 먼저 늘리지 않고 원본 pack과 caption을 고친다.
- 현재 상태: 이전의 소수 이미지 SD 1.5 LoRA probe는 실행은 됐지만 held-out 품질이 부족했다. 따라서 **새 reference pack을 확보하기 전에는 1번 성공을 주장할 수 없다.**

## 실험 2: SD 1.5 StoryDiffusion 최소 probe

### 질문

SD 1.5 기반 StoryDiffusion이 참조 팩과 character LoRA의 기준을 세 prompt에서 반복할 수 있으며, 8 GB VRAM에서 실행을 시작할 수 있는가?

### 8 GB 실험 설계

1. P7-5.1에서 승인한 SD 1.5 base, character LoRA revision, identity 문장을 고정한다.
2. 장소와 camera만 다른 세 prompt를 만들고 `512 x 512`, batch 1, consistent self-attention만 사용한다.
3. ControlNet, IP-Adapter, inpaint, 두 번째 LoRA는 사용하지 않는다.
4. 각 PNG의 seed, 생성 시간, peak VRAM을 기록하고 참조 팩의 얼굴·헤어·의상·화풍 항목을 세 컷 모두에서 검사한다.

### 성공과 중단 기준

- 성공: 세 PNG가 생성되고, 얼굴·헤어·의상·화풍의 필수 항목이 모두 유지되며 VRAM과 시간이 기록된다.
- 중단: out-of-memory가 나거나, 큰 색상만 반복되고 얼굴·의상 기준이 흔들린다. 이때 ControlNet을 붙여 결과를 구제하지 않는다.
- 현재 상태: SD 1.5 StoryDiffusion의 8 GB 통과 기록은 없다. 따라서 2번은 **제작 경로가 아닌 최소 probe**로만 진행한다.

## 실험 3: 1+2 기반 최종 cut-scene

### 질문

승인 character reference pack/LoRA와 승인된 ControlNet data를 결합해, 서로 다른 pose·camera·장소의 4컷을 만들고 국소 inpaint 뒤에도 인물성과 화풍을 유지할 수 있는가?

### 8 GB 실험 설계

1. SD 1.5 호환 checkpoint와 ControlNet 하나, `512 x 768`, batch 1으로 시작한다. panel 02는 OpenPose, panel 03은 depth 또는 lineart, panel 04는 lineart 또는 segmentation처럼 컷별 주 조건을 하나씩만 사용한다.
2. 모든 panel에서 ControlNet on/off 비교 PNG를 만든다. control image가 pose·camera·소품의 큰 관계를 바꾸는지 먼저 판단한다.
3. 실험 1의 character LoRA 또는 승인 reference 조건 하나만 더해 같은 seed·prompt·control image에서 identity 효과를 비교한다. IP-Adapter, 두 번째 ControlNet, high-resolution fix를 동시에 추가하지 않는다.
4. 전체 frame이 structure와 identity를 통과한 경우에만 face, hand-object, foot-contact, background mask를 서로 분리해 inpaint한다. face/style anchor는 전체 생성과 동일한 버전으로 고정한다.
5. 최종 4컷 contact sheet에서 identity, style, structure, local detail, continuity를 각각 `pass/fail`로 판정한다.

### 성공과 중단 기준

- 성공: 네 컷 모두에서 character reference pack의 얼굴·헤어·의상·화풍 항목과 shot contract의 pose·camera·소품 접점이 함께 통과하고, inpaint가 mask 밖의 승인 특징을 바꾸지 않는다.
- 중단: `structure fail`이면 ControlNet source/strength로, `identity fail`이면 character pack/LoRA로, `style fail`이면 style anchor로 돌아간다. 구조 오류를 손·얼굴 inpaint로 고치지 않는다.
- 현재 상태: SDXL + OpenPose/IP-Adapter 실험은 큰 외형 반복성과 일부 framing만 보여 줬고, 최종 4컷 품질에는 미달했다. 3번은 **가능성 검증 전 단계**이며, 1·2의 승인 자산 없이는 실행하지 않는다.

## 권장 순서와 산출물

```text
E1 character-reference-pack/
  -> approved-character-pack.md
  -> train/ and held-out/ manifest
  -> lora-on-off-contact-sheet.png

E2 cut-scene-data/
  -> panel-01..04-shot-contract.json
  -> panel-01..04-pose-source.png
  -> panel-01..04-openpose.png + keypoints.json
  -> human-structure-review.md

E3 final-cut-scene/
  -> panel-01..04-controlnet-on-off.png
  -> panel-01..04-identity-ablation.png
  -> panel-01..04-repair-mask-*.png
  -> episode-contact-sheet.png
  -> continuity-review.md
```

E1이 승인되지 않으면 E2와 E3는 시작하지 않는다. E2가 중단되더라도 E3의 ControlNet baseline은 별도 조건으로 검토할 수 있지만, StoryDiffusion 성공으로 E3의 품질을 주장할 수는 없다. E3의 첫 성공 이미지는 파이프라인 통과가 아니며, 반드시 4컷 배열의 통과 기록이 있어야 한다.
