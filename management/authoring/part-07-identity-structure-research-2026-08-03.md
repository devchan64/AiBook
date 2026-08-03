# Part 7 identity-structure 분리 파이프라인 조사

확인일: 2026-08-03

## 출발점

P7-5.1의 SDXL base LoRA + Canny scale sweep은 다음 경계를 실제 생성으로 확인했다.

- 약한 Canny는 흰 재킷, 청록 바지, 네이비 가방을 대체로 유지하지만 ticket을 향한 굽힘을 만들지 못한다.
- 중간 이상 Canny는 굽힘과 foyer 원근을 만들지만 재킷, 바지, 가방, 가방끈을 Canny 원본의 다른 인물 구조로 다시 해석한다.
- 학습 해상도를 최종 전신 frame과 같은 `512 x 768`으로 올려도 두 조건을 함께 통과시키지 못했다.

따라서 다음 실험의 질문은 `Canny scale을 더 찾을 수 있는가`가 아니다. **camera/pose의 공간 조건이 캐릭터와 소품의 식별 윤곽을 덮지 않도록, 조건과 보정 영역을 어떻게 분리할 것인가**다.

## 외부 근거와 적용 한계

| 자료 | 공식적으로 확인한 내용 | 이 프로젝트의 해석 | 8 GB 판단 |
| --- | --- | --- | --- |
| [Diffusers ControlNet guide](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/controlnet.md){: target="_blank" rel="noopener noreferrer" } | Canny, depth, pose 등 공간 조건을 ControlNet으로 전달하며, 다중 조건은 겹치지 않게 mask하고 scale을 따로 조정하라고 안내한다. | 인물 전체 Canny 하나로 pose, 배경 원근, 가방끈을 동시에 제어하지 않는다. 배경과 인물 영역의 control을 겹치지 않게 만든다. | 현재 SDXL sequential CPU offload 실행 경로가 있으므로 단일 조건부터 측정 가능. 다중 조건은 단일 조건 통과 뒤에만 검토. |
| [Diffusers inpainting guide](https://github.com/huggingface/diffusers/blob/main/docs/source/en/using-diffusers/inpaint.md){: target="_blank" rel="noopener noreferrer" } | mask의 흰 영역만 prompt로 다시 채우며 CPU offload와 memory-efficient attention을 메모리 절감 수단으로 제시한다. | 가방끈, 손-소품 접점처럼 국소 결함은 전체 재생성이 아니라 승인된 full-frame 후보의 제한된 mask에서 고친다. | 기존 full-frame 품질 gate를 통과한 뒤에만 후보. 지금의 Canny+LoRA 분기에는 추가하지 않는다. |
| [InstantID](https://github.com/instantX-research/InstantID){: target="_blank" rel="noopener noreferrer" } | SDXL pipeline에서 얼굴 분석, identity adapter, face keypoint control을 함께 쓰는 zero-shot identity 보존 구현을 제공한다. | 얼굴·눈·앞머리를 전신 LoRA의 부수 효과로 두지 않고 face 전용 조건으로 분리하는 후보. 만화 얼굴과 옆얼굴의 품질은 별도 실험이 필요하다. | GPU 최소량을 공식 README가 보장하지 않는다. adapter, antelopev2, pipeline의 다운로드와 `512 x 768` one-shot preflight가 먼저다. |
| [ConsistentID](https://github.com/JackAILab/ConsistentID){: target="_blank" rel="noopener noreferrer" } | FaceParsing과 FaceID를 사용해 세밀한 얼굴 identity를 다루며 SDXL model과 ControlNet demo를 제공한다. | 얼굴 identity 후보이지만 portrait 중심이다. 전신 비례, 의상, 가방끈을 해결하는 도구로 확대 해석하지 않는다. | 공식 GPU 최소량 미확인. 설치와 단일 컷 preflight 전에는 후보로만 둔다. |
| [CharaConsist](https://github.com/Murray-Wang/CharaConsist){: target="_blank" rel="noopener noreferrer" } | FLUX.1 기반으로 foreground character와 선택적 background consistency를 분리한다. README의 `init_mode=3`은 sequential CPU offload와 GPU 3 GB를 제시한다. | 단순한 PNG 합성이 아니라 foreground/background mask와 point matching을 이용하는, 캐릭터-배경 분리의 직접 후보다. pose generator는 아니다. | 8 GB GPU 조건은 명목상 가능하다. 다만 FLUX.1-dev 가중치, CPU RAM, 디스크, 속도는 별도 preflight가 필요하며 아직 채택하지 않는다. |
| [AnyDoor](https://github.com/ali-vilab/AnyDoor){: target="_blank" rel="noopener noreferrer" } | mask가 있는 reference object를 target 영역에 맞추는 zero-shot object-level customization을 제공한다. | 네이비 flap 가방과 하나의 대각 끈을 `character prompt`가 아니라 object reference + target mask로 검증할 수 있는 후보다. | SD 2.1/DINOv2 의존, object mask 품질, 만화 화풍 호환성을 아직 검증하지 않았다. 우선순위 3의 조사·preflight 후보. |
| [PuLID](https://github.com/ToTheBeginning/PuLID){: target="_blank" rel="noopener noreferrer" } | SDXL PuLID와 FLUX PuLID를 제공하며, README는 로컬 Gradio demo의 12 GB 지원을 언급한다. | 얼굴 identity 연구 근거로만 참고한다. | 공개된 로컬 demo 기준이 8 GB보다 크므로 현 장비의 다음 실험에서는 제외. |
| [StoryDiffusion](https://github.com/HVision-NKU/StoryDiffusion){: target="_blank" rel="noopener noreferrer" } | SD 1.5/SDXL 모델에 compatible한 consistent self-attention과 최소 3개, 권장 5-6개의 prompt를 안내한다. | 여러 장면의 반복성 검사 후보이지, 한 컷의 가방끈·손·pose 충돌을 고치는 도구는 아니다. | 현재 단일 컷 identity/structure gate가 실패했으므로 우선순위에서 뒤로 보낸다. |

## 다음 파이프라인 가설

다음 후보는 character와 background를 별 PNG로 독립 생성한 뒤 단순 합성하는 방식이 아니다. 하나의 최종 canvas와 shot contract를 먼저 만들고, **영역별로 입력 책임을 나누는 방식**이다.

```text
shot contract (camera, full-body box, perspective, pose intent, object position)
  -> scene-only camera control (character area masked out)
  -> foreground character generation in approved full-body region
       identity: character LoRA or reference adapter
       pose: human-reviewed pose/line condition in foreground region only
  -> full-frame quality gate
  -> face mask repair only when face gate fails
  -> bag + diagonal strap mask repair only when object gate fails
  -> final crop and lettering
```

이 가설의 핵심은 Canny input에서 캐릭터의 재킷, 바지, 가방, 가방끈 윤곽을 제거하는 것이다. 배경 Canny는 소실점과 장소 구조만 전달하고, 전신 자세는 사람 검수한 pose/line 원본을 **인물 mask 안에서만** 전달한다. 가방끈은 전체 pose 또는 face identity의 하위 항목이 아니라 독립 object gate다.

## 실험 우선순위

### 1. 영역 분리 ControlNet preflight

목적: `scene-only Canny`가 camera/background를 지키면서 character LoRA의 의상·가방을 덮지 않는지 확인한다.

- 고정: SDXL base, `512 x 768`, native-resolution identity LoRA, held-out cinema shot, prompt, seed.
- 변경: 전체 Canny가 아닌 character bounding region을 지운 scene-only Canny `0.0/0.35/0.75`.
- 판정: background perspective, white jacket, teal trousers, navy flap bag, one diagonal strap, full body, pose intent를 독립 체크.
- 중단: character가 upright로 남으면 pose 문제를 background Canny scale로 해결하려 하지 않는다.

이 실험은 새 모델이나 두 번째 ControlNet을 넣지 않으므로, 현재 실패 원인을 가장 직접적으로 분리한다.

실행 결과: 같은 native-resolution LoRA adapter에서 full Canny와 scene-only Canny를 `0.35`와 `0.75`로 비교했다. scene-only Canny는 전체 Canny보다 흰 재킷·청록 바지의 보존을 일부 회복하고 foyer 배경을 바꿨다. 그러나 인물은 upright로 남거나 작아졌고 가방·대각 끈도 실패했다. full Canny만 ticket 쪽 굽힘을 전달했다. 따라서 이 가설은 `배경 control과 identity의 간섭 완화`에는 부분 통과지만 `pose control`에는 실패다.

### 2. 얼굴 조건 one-shot preflight

목적: face identity adapter가 Canny/pose와 독립적으로 같이 올라갈 수 있는지, 그리고 anime reference에서 오히려 실사 얼굴을 강요하지 않는지 확인한다.

- 후보: InstantID 우선, ConsistentID는 의존성·모델 구조 확인 뒤 비교.
- 입력: 정면과 3/4 얼굴 기준, 동일한 native-resolution character LoRA, one static full-body shot.
- 평가: 얼굴형, 눈, 앞머리, clip, 목-머리 연결만 본다. pose/camera 결과를 이 실험으로 주장하지 않는다.
- 중단: 단일 `512 x 768` PNG가 저장되지 않거나 만화 화풍이 실사화되면 현재 8 GB 경로에서 제외한다.

### 3. 가방/가방끈 object repair 후보 비교

목적: 한 컷의 승인된 전신 결과에서 `right hip navy flap bag + one diagonal strap`을 국소적으로 고칠 수 있는지 확인한다.

- 가장 먼저는 base inpaint + 사람이 만든 precise mask를 사용한다.
- AnyDoor는 reference object mask와 target mask가 필요한 object-level 대안으로만 비교한다.
- object repair는 full-frame pose·camera·face gate를 통과한 뒤에만 실행한다.
- 판정: mask 밖의 의상, 손, 카메라, 배경이 바뀌면 실패다.

### 4. CharaConsist 실행 성립 preflight

목적: foreground/background consistency 방식을 8 GB에서 실제로 실행할 수 있는지 확인한다.

- 먼저 model size, required CPU RAM, disk, license, FLUX.1-dev 조건을 확인한다.
- 공식 `init_mode=3` sequential offload로 단일 이미지와 두 prompt만 실행해 PNG 저장, peak VRAM, CPU RAM, 시간, foreground/background mask 저장 여부만 기록한다.
- 성공해도 pose/camera/가방끈 품질 통과로 해석하지 않는다.

## 채택하지 않는 다음 단계

- Canny scale을 `0.10`과 `0.35` 사이에서 미세 탐색하는 일: 이미 identity/pose가 교차하지 않는 방향을 확인했다.
- Canny와 두 번째 ControlNet을 즉시 겹치는 일: 원인 분리가 안 되며, 공식 문서도 condition mask 분리를 권한다.
- 실패한 full-frame 후보에 얼굴·손 inpaint를 먼저 얹는 일: pose와 의상 구조가 틀린 원인을 가린다.
- StoryDiffusion을 먼저 붙이는 일: sequence repetition은 아직 단일 컷의 identity/structure gate를 통과하지 못한 상태에서 평가할 대상이 아니다.

## 현재 권고

scene-only Canny 비교 뒤에는 pose/control 입력을 Canny에서 분리한다. 다음 실행은 **foreground 영역의 별도 human-pose 조건**이며, face adapter, object repair, CharaConsist는 그 뒤의 독립 gate다. 하나의 거대한 workflow에 동시에 결합하지 않는다.

## 후속 검토: foreground pose 조건 후보

확인일: 2026-08-03

### 외부 자료에서 확인한 선택지

| 후보 | 확인한 공개 근거 | 현재 판단 |
| --- | --- | --- |
| [TencentARC OpenPose T2I-Adapter for SDXL](https://huggingface.co/TencentARC/t2i-adapter-openpose-sdxl-1.0){: target="_blank" rel="noopener noreferrer" } | Apache-2.0, 316 MB의 SDXL OpenPose adapter를 제공한다. | 다음 one-shot preflight의 1순위. 기존 full OpenPose ControlNet 재실행과 달리 foreground-only pose map과 native-resolution identity LoRA만 결합한다. |
| [Diffusers T2I-Adapter guide](https://huggingface.co/docs/diffusers/main/using-diffusers/t2i_adapter){: target="_blank" rel="noopener noreferrer" } | `StableDiffusionXLAdapterPipeline`과 `MultiAdapter`로 여러 control image와 개별 scale을 전달하는 예제를 제공한다. | pose 단일 조건이 통과한 뒤에만 scene-only Canny와 OpenPose를 MultiAdapter로 결합한다. |
| [Diffusers T2I-Adapter training guide](https://huggingface.co/docs/diffusers/v0.35.1/en/training/t2i_adapters){: target="_blank" rel="noopener noreferrer" } | T2I-Adapter는 약 77M parameter, 약 300 MB이며 UNet 전체 복사 대신 weight를 삽입하는 경량 조건 모듈이라고 설명한다. | 8 GB에서는 두 번째 full ControlNet보다 먼저 실행할 근거가 있다. 실제 peak VRAM과 PNG 저장은 별도 측정한다. |
| [Diffusers Multi-ControlNet guide](https://huggingface.co/docs/diffusers/main/en/using-diffusers/controlnet){: target="_blank" rel="noopener noreferrer" } | 여러 condition은 서로 겹치지 않게 mask하고 scale을 따로 조정하라고 안내한다. | scene Canny는 foreground ROI를 비우고, pose map은 그 ROI 밖을 검게 한다. 두 입력의 책임을 겹치지 않는다. |
| [ControlNet++](https://github.com/xinsir6/ControlNetPlus){: target="_blank" rel="noopener noreferrer" } | 공개 예시는 pose skeleton으로 foreground를, depth로 background를 담당시키고, hand/foot에는 별도 thin line을 권한다. | 역할 분리는 현재 결론과 맞지만 새 unified ControlNet을 먼저 도입하지 않는다. T2I-Adapter 단일 pose gate 뒤의 비교 후보로 보류한다. |

현재 `.venv`의 `diffusers`는 `0.37.0`이며 `T2IAdapter`, `MultiAdapter`, `StableDiffusionXLAdapterPipeline` import를 확인했다. 두 TencentARC SDXL adapter 가중치는 현재 캐시에 없다. 따라서 모델 다운로드 뒤에 API·모델 파일·sequential CPU offload·한 장 PNG·peak VRAM을 확인해야 한다.

### 왜 기존 OpenPose 재실행이 아닌가

이전 OpenPose 계열 실험은 전 화면 pose map 또는 IP-Adapter와의 결합에서 인물성, 장소, pose 원인을 분리하지 못했다. 다음 조건은 아래 차이가 있어야 한다.

| 항목 | 이전 실패 경로 | 다음 preflight |
| --- | --- | --- |
| identity | IP-Adapter 또는 전체 화면 조건이 pose와 동시에 변함 | native-resolution character LoRA만 고정 |
| pose map | 전 화면에 전달 | 인물 full-body ROI에만 전달, 바깥은 검정 |
| background | pose map과 함께 재생성됨 | 첫 preflight에서는 끔; 통과 뒤 scene-only Canny를 별도 추가 |
| pose 관절 | raw detector 결과가 손·얼굴까지 과도하게 영향 | 목, 어깨, 팔꿈치, 손목, 골반, 무릎, 발목의 전신 구조만 사용; 얼굴·가방·손가락은 별도 gate |
| 평가 | 한 이미지의 인상 | full body, head-neck direction, wrist endpoint, foot placement, white jacket, teal trousers, navy flap bag, one diagonal strap을 별도 기록 |

### 실행 순서

1. **다운로드·API preflight**: OpenPose T2I-Adapter 하나만 받아 `512 x 768`, batch 1, sequential CPU offload에서 PNG 저장과 peak VRAM을 확인한다. 가중치 파일·라이선스·정확한 snapshot을 기록한다.
2. **foreground-only pose single-condition**: 사람 검수한 target pose map에서 얼굴·가방 선을 빼고, full-body ROI 밖을 검정으로 만든다. SDXL LoRA와 OpenPose adapter만 `0.0/0.35/0.70`으로 비교한다.
3. **quality gate**: `0.0`보다 굽힘, 목-머리 방향, 양 손목, 양 발목의 위치가 실제로 바뀌면서 흰 재킷·청록 바지·네이비 flap 가방·한 대각 끈이 유지되는지 본다. 한 항목이라도 유지되지 않으면 Canny를 다시 붙이지 않는다.
4. **non-overlap multi-condition**: 3단계가 부분 통과했을 때만 scene-only Canny adapter와 pose adapter를 `MultiAdapter`로 결합한다. Canny는 foreground ROI에서 0, pose는 ROI 밖에서 0으로 둔다. scale은 pose와 scene에 독립적으로 기록한다.
5. **국소 보정**: full-frame gate 통과 후보에서만 face 또는 bag+strap mask repair를 별도 비교한다.

### 중단 규칙

- OpenPose adapter의 한 장 preflight가 8 GB에서 PNG 저장까지 가지 못하면, MultiAdapter와 face adapter 다운로드를 시작하지 않는다.
- foreground-only pose가 identity를 유지하지 못하면, pose scale 미세 sweep이나 Canny 결합을 계속하지 않는다.
- pose가 통과해도 가방끈이 실패하면 그 문제를 pose adapter에 맡기지 않는다. object mask repair의 독립 gate로 넘긴다.
- MultiAdapter는 단일 pose와 단일 scene control이 각각 부분 통과한 뒤에만 실행한다.

### foreground-only OpenPose T2I-Adapter 실행 결과: 미채택

공식 `TencentARC/t2i-adapter-openpose-sdxl-1.0`을 받아 SDXL base에서 `512 x 768` 단일 PNG를 sequential CPU offload로 저장했다. 따라서 adapter 파일·API·OpenPose detector 우회 import·8 GB 실행 성립은 통과했다.

그러나 같은 native-resolution identity LoRA와 foreground ROI 안의 OpenPose body map을 `0.0`, `0.35`, `0.70`으로 비교했을 때 품질은 통과하지 못했다. `0.35`는 인물을 upright로 남긴 채 의상을 바꿨고, `0.70`은 뒷모습과 큰 배낭으로 이탈했다. low bent ticket action, 얼굴, 흰 재킷, 청록 바지, 네이비 flap 가방, 하나의 대각 끈을 함께 유지한 경우는 없었다.

그러므로 이 branch는 scene-only Canny와 결합하지 않는다. raw OpenPose map의 강도를 더 나누어도 현재 실패 원인을 줄이지 못하므로, PNG와 adapter 학습 산출물은 제거하고 [판정 기록](../../docs/assets/part-07/chapter-05/p7-5-2-foreground-openpose-adapter-review.json)만 남긴다. 다음 후보는 reference identity를 직접 받는 pose-transfer 구현이다.

## 후속 검토: reference-conditioned pose transfer

확인일: 2026-08-03

OpenPose는 목표가 아니라 구조 입력 중 하나일 뿐이다. 다음 비교에서는 `reference character image`와 `target shot/pose image`를 별도 입력으로 받는 구현을 우선 조사했다. 이 구조가 필요한 이유는 현재 LoRA + OpenPose가 자세를 강하게 줄수록 재킷, 바지, 가방과 가방끈을 target pose 이미지의 다른 인물 외형으로 다시 해석했기 때문이다.

| 후보 | 공개 자료에서 확인한 역할 | 8 GB에서의 현재 판단 | 다음 행동 |
| --- | --- | --- | --- |
| [One-to-All Animation](https://github.com/ssj9596/One-to-All-Animation){: target="_blank" rel="noopener noreferrer" } | 기준 이미지와 driving pose를 받아 direct image pose transfer와 character animation을 지원한다. 1.3B 예시는 16 GB T4를 전제로 제시한다. | 8 GB 실행 근거가 없으므로 현재 장비에서 다운로드·실행하지 않는다. 16 GB 이상 환경의 고품질 후보로 기록한다. | 보류 |
| [MusePose](https://github.com/TMElyralab/MusePose){: target="_blank" rel="noopener noreferrer" } | reference image와 pose video를 받아 animation을 생성하고, pose alignment를 제공한다. 공식 README는 `512 x 512 x 48`에 16 GB, `768 x 768 x 48`에 28 GB를 명시한다. | 현 장비의 전신 영상 경로에는 맞지 않는다. 또한 README 자체가 복잡한 의상과 얼굴 detail consistency, background flicker를 한계로 든다. | 제외 |
| [MagicDance / MagicPose](https://github.com/Boese0601/MagicDance){: target="_blank" rel="noopener noreferrer" } | appearance control과 OpenPose control을 분리한 identity-aware human pose retargeting 구현이다. | SD 1.5, appearance model, OpenPose control model을 별도 요구하고, 공개 환경은 오래된 PyTorch/CUDA 조합이다. 8 GB 수치가 없어 현재 프로젝트 환경을 깨뜨리는 설치 실험을 하지 않는다. | 보류 |
| [OnePoseTrans](https://github.com/Dongqi-Fan/OnePoseTrans){: target="_blank" rel="noopener noreferrer" } | 단일 source image의 test-time fine-tuning과 face/text/image consistency를 이용한 정적 pose transfer다. foreground/background 분리와 후속 합성 단계도 제공한다. | SDXL 외에 SAM ViT-H, GroundingDINO, LaMa, inpaint 등 대형 의존성을 요구한다. V100에서 약 48초라는 결과는 8 GB 보장이 아니며, 현 GPU에서는 preflight 비용이 과도하다. | 제외 |
| [Leffa](https://github.com/franciszzj/Leffa){: target="_blank" rel="noopener noreferrer" } | reference appearance와 DensePose 기반 target pose를 입력으로 받는 pose-transfer 모델이며, 세밀한 외형 detail 보존을 목표로 한다. | 공식 저장소는 최소 VRAM을 명시하지 않는다. 별도 reference UNet, DensePose, mask 생성기가 있어 현 SDXL 경로보다 무겁다. 제3자 설치 기록의 pose mode 16 GB는 참고 수준이므로 8 GB 가능으로 쓰지 않는다. | 보류 |
| [Ctrl-X](https://genforce.github.io/ctrl-x/){: target="_blank" rel="noopener noreferrer" } | structure image와 appearance image를 분리해 SDXL의 feature/attention에 주입하는 training-free, guidance-free 방법이다. 구조 입력은 Canny, normal, wireframe 등을 포함할 수 있다. | 공식 자료가 8 GB 최소량을 보장하지는 않는다. 그러나 별도 pose model 학습·대형 video module 없이 기존 SDXL base와 character reference, target shot을 재사용하므로, sequential CPU offload 한 장 preflight의 비용이 가장 낮다. | **다음 실행 후보** |

### Ctrl-X preflight의 범위와 판정

Ctrl-X는 한 컷에서 `target shot image`를 구조 입력, 승인한 Mira 단일 전신 reference를 appearance 입력으로 나눈다. target shot은 사람 검수한 full-body pose와 camera/projection을 담되, 가방·얼굴·의상 texture를 넣지 않은 단색 mannequin 또는 line/flat-color scene으로 만든다. appearance reference는 단일 캐릭터 이미지로 고정한다.

이 preflight는 기존 OpenPose adapter의 재실행이나 Canny scale sweep이 아니다. `512 x 768`, batch 1, SDXL base, sequential CPU offload에서 다음만 먼저 측정한다.

1. PNG 저장, peak VRAM, wall time, 필요한 checkpoint와 라이선스.
2. target shot의 몸통 굽힘, 목-머리 방향, 양 손목, 양 발목, 전신 box, low-angle projection이 실제로 옮겨지는가.
3. appearance reference의 bob hair, 흰 재킷, 청록 바지, 네이비 flap bag, 한 대각 끈이 동시에 남는가.

이 중 하나라도 통과하지 않으면 scene control, inpaint, sequence generation을 붙이지 않는다. 특히 Ctrl-X의 공개 결과는 일반 이미지의 structure/appearance transfer 근거이지, 만화 전신 캐릭터와 가방끈 품질을 보장하지 않는다. 따라서 이 실행은 채택 실험이 아니라 **다음 분기의 실행 성립 및 품질 gate**다.

### 현재 선택

현재 8 GB에서 바로 실행할 수 있는 고품질 전용 pose-transfer 모델은 외부 자료만으로 확인하지 못했다. 이 결론은 기능 부재가 아니라 VRAM, 대형 의존성, video sequence의 시간/해상도 비용 때문이다. 다음 분기는 Ctrl-X를 정적 한 컷으로 preflight하고, 성공한 경우에만 foreground/background non-overlap 조건과 face·bag 국소 gate를 연결한다. 실패하면 같은 OpenPose 계열 scale을 다시 탐색하지 않고, 16 GB 이상 환경의 One-to-All Animation 또는 Leffa를 별도 실행 환경 후보로 분리한다.

### Ctrl-X static preflight 실행 결과: 미채택

공식 Ctrl-X runner를 별도 `/tmp` 복사본에서 검토했다. upstream은 `sequential_offload + disable_refiner`에서 structure+appearance control의 약 3.8 GiB VRAM을 제시하며, 현 `.venv`의 `diffusers 0.37.0`에서도 핵심 pipeline import는 됐다. 다만 upstream의 `--model` 경로 처리는 directory 형태의 local Diffusers snapshot을 다루지 못하고 scheduler도 원격 model ID에서 읽었다. 실험용 복사본에서만 local scheduler와 directory `from_pretrained`로 보완했으며, 저장소와 upstream 원본은 변경하지 않았다.

`512 x 768`, batch 1, refiner off, sequential CPU offload, 20 step으로 실행했다. structure input은 cinema ticket held-out 컷에서 손·얼굴을 뺀 body OpenPose map, appearance input은 승인된 Mira front reference 하나다. PNG 저장까지는 통과했다.

그러나 결과는 low bend와 하체 방향을 일부 옮겼을 뿐, cinema background가 사라지고 얼굴·앞머리가 붕괴했으며 흰 재킷이 청록 계열로 바뀌었다. navy flap bag과 하나의 대각 끈도 남지 않았다. peak VRAM은 quality failure 뒤 benchmark만을 위한 재실행을 하지 않아 확정 기록하지 않는다. 이 사실은 실행 불능이 아니라 **full-frame quality failure**다.

따라서 Ctrl-X 역시 scene control, face inpaint, bag repair, sequence stage와 결합하지 않는다. 생성 PNG와 temporary structure script는 제거하고 [판정 기록](../../docs/assets/part-07/chapter-05/p7-5-2-ctrlx-static-pose-transfer-review.json)만 남긴다. 다음 탐색은 8 GB 단일 GPU에서 동작이 명시된 다른 reference-conditioned 정적 방법이 있는지 확인하거나, 고품질 전용 pose-transfer는 16 GB 이상 별도 환경으로 분리하는 두 갈래다.

### 추가 제외: attention injection 계열의 VRAM 경계

[MasaCtrl](https://github.com/tencentarc/masactrl){: target="_blank" rel="noopener noreferrer" }은 source image의 content와 prompt/control이 만든 target layout을 mutual self-attention으로 결합하며, T2I-Adapter와 ControlNet 결합도 제공한다. 구조와 외형을 분리한다는 점에서 Ctrl-X와 다른 구현 경로이므로 검토했지만, 공식 README가 synthesis에 단일 GPU 최소 16 GB VRAM을 명시한다. 따라서 sequential offload의 비공식 변형을 8 GB에서 다시 구현하는 실험은 하지 않는다.

이로써 현재 공식 공개자료에서 확인한 static reference-conditioned 후보 중 `Ctrl-X`만 8 GB 실행 성립까지 갔고 품질에서 탈락했다. `MasaCtrl`, `Leffa`, One-to-All Animation, MusePose, OnePoseTrans은 각각 명시된 VRAM, 대형 의존성, 또는 video workload 때문에 현재 장비의 다음 실험 후보가 아니다. 다음 탐색은 새 attention injection 구현의 반복이 아니라, **생성 전에 character-specific pose-to-image 쌍을 충분히 만드는 데이터/학습 경로** 또는 16 GB 이상 별도 실행 환경으로 나눠야 한다.

## 학습 경로 재검토: 왜 19장 reference pack에 pose adapter를 바로 학습하지 않는가

[DreamPose](https://grail.cs.washington.edu/projects/dreampose/){: target="_blank" rel="noopener noreferrer" }는 pose와 reference image를 함께 조건으로 받는 구조를 만들기 위해 먼저 패션 video의 서로 다른 frame pair를 사용해 범용 모델을 학습하고, 그 다음 대상 subject에 적응한다. 논문은 한 image-pose pair만으로 적응하면 texture sticking 같은 artifact가 빨리 생긴다고 보고하고, pose·reference pair의 augmentation을 사용한다. 즉 reference-conditioned pose transfer는 character LoRA보다 한 단계 더 많은 `pose -> image` 대응 지식을 필요로 한다.

[ControlNet](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }의 zero-convolution 설계는 pretrained base를 유지하면서 image-pair 조건을 추가 학습할 수 있고 small-scale/personal device 학습도 목표로 한다. 그러나 이는 작은 dataset으로 범용 pose transfer가 자동으로 생긴다는 뜻은 아니다. Mira reference pack의 19장은 character identity view와 의상·가방 기준을 검증하는 데는 유효하지만, 각각이 다른 camera, action, occlusion, background를 포괄하는 paired pose curriculum은 아니다.

따라서 다음 학습 preflight의 질문은 "이 19장을 OpenPose와 함께 학습하면 되는가"가 아니다. 아래처럼 분리한다.

1. **범용 조건 결합**: 공개 라이선스가 명확한 human pose-image pair dataset 또는 기존 pretrained reference-conditioned pose model이 필요하다. 8 GB에서 adapter/ControlLoRA 수준의 학습이 가능한지, base model·license·dataset·VRAM을 별도 검증한다.
2. **캐릭터 적응**: 범용 조건 결합이 이미 통과한 모델에만 Mira의 승인된 full-body reference와 사람이 검수한 pose target을 사용한다. camera, side/rear view, object interaction, background를 포함한 hold-out split을 유지한다.
3. **품질 gate**: reference face/hair, white jacket, teal trousers, navy flap bag, one diagonal strap과 target head-neck, wrist, ankle, full-body projection을 독립 평가한다. 이 중 하나가 빠지면 face/bag inpaint로 덮지 않는다.

현재 repository의 19장 reference pack만으로 1단계를 대체하는 학습은 데이터 부족과 overfit 위험이 크므로 시작하지 않는다. 다음 조사는 8 GB에서 실제 학습 가능한 pose-conditioned adapter 또는 ControlLoRA의 공식 implementation, 학습 데이터 license, 그리고 general-to-character two-stage 재현 가능성에 집중한다.

### pretrained OpenPose T2I-Adapter character fine-tuning 실행 결과: 미채택

공식 Diffusers `v0.37.0` T2I-Adapter 학습 예제를 기반으로, TencentARC의 pretrained SDXL OpenPose adapter만 update하는 `512 x 768`, batch 1 실험을 했다. base UNet은 동결했다. 기본 runner는 square center crop, 모든 caption embedding의 한 번에 계산, 그리고 VAE 반복 encode 때문에 8 GB에서 그대로는 성립하지 않았다. 실험용 `/tmp` 복사본에서 native width/height resize, caption batch size 1, text encoder CPU offload, FP32 VAE latent 사전 cache를 적용했다. 이 변경으로 19개 training pair를 150 step까지 finite loss로 학습하고 adapter 가중치를 저장했다.

그러나 held-out cinema ticket pose를 원 adapter와 같은 seed로 비교하면 adapter 학습본도 low bend를 만들지 못했다. full body와 cinema 배경은 일부 남았지만, teal bob/얼굴, 흰 재킷, 청록 바지, navy flap bag, 하나의 대각 끈을 동시에 보존하지 못했다. 즉 이 결과는 **8 GB에서 adapter fine-tuning이 기술적으로 실행 가능**함을 보였지만, 19개의 character pose-image pair가 reference-conditioned pose transfer의 일반화·identity 품질을 만들기에는 부족함을 확인한 실패다.

학습 adapter, comparison PNG, VAE latent cache, temporary dataset과 scripts는 제거하고 [판정 기록](../../docs/assets/part-07/chapter-05/p7-5-2-t2i-adapter-finetune-review.json)만 남긴다. 이 경로를 ControlNet, Canny, inpaint와 결합해도 target pose와 character identity가 동시에 통과했다는 근거가 없으므로 진행하지 않는다.

## 후속 후보: MimicMotion 접근성 preflight

[Tencent MimicMotion](https://github.com/Tencent/MimicMotion){: target="_blank" rel="noopener noreferrer" }은 reference image와 pose sequence를 함께 받는 사전학습 video pose-transfer 구현이다. 공식 README는 16-frame U-Net의 최소 VRAM을 8 GB로, VAE decoder는 CPU 실행 가능으로 설명한다. 이는 image-only adapter와 다른 reference-conditioned architecture이므로 다음 후보로 선택했다.

현재 `.venv`에서 MimicMotion loader import와 repository CPU offload 경로를 확인했고, `MimicMotion_1-1.pth` checkpoint 다운로드도 완료했다. 그러나 필수 base `stabilityai/stable-video-diffusion-img2vid-xt-1-1`는 Hugging Face gated repository이며 현 인증 상태에서 `401 GatedRepoError`가 발생했다. 따라서 현재는 16-frame inference PNG/video와 VRAM 측정이 없으며, 품질 통과나 실패로 기록하지 않는다. gated base 접근을 우회하거나 다른 공개 base로 바꾸지 않는다. 이 후보는 **외부 접근 조건 대기**로 분리하고, 다음 탐색은 ungated reference-conditioned pose-transfer 구현으로 이어간다.

## 후속 후보: Wan2.1 VACE 1.3B

확인일: 2026-08-03

[Wan2.1 VACE 공식 저장소](https://github.com/Wan-Video/Wan2.1){: target="_blank" rel="noopener noreferrer" }는 text, optional reference image, optional video와 mask를 함께 입력받아 reference-to-video(R2V), video-to-video, masked video-to-video를 처리한다고 설명한다. pose, depth 같은 구조 조건은 V2V/MV2V의 입력 비디오를 전처리해 만든다. 따라서 이 후보는 reference image 하나와 **사람 검수한 pose/camera target 영상**을 분리할 수 있으며, OpenPose 자체가 목적은 아니다.

[공식 VACE 1.3B model card](https://huggingface.co/Wan-AI/Wan2.1-VACE-1.3B){: target="_blank" rel="noopener noreferrer" }는 Apache-2.0 라이선스와 Diffusers pipeline을 제공한다. 1.3B VACE는 480p만 권장·지원하고, 공식 Wan 문서는 1.3B 계열의 consumer-grade 기준을 8.19 GB VRAM으로 제시한다. 그러나 이 수치는 일반 1.3B 계열의 공식 효율 지표이며, VACE의 reference image, control video, 81-frame 기본 생성, 현 8 GB GPU에서의 peak VRAM과 시간까지 보장하는 수치는 아니다. 또한 공개 snapshot은 약 19 GB이므로 다운로드 공간도 별도 확인한다.

### 현재 적합성 판단

| 요구 | VACE가 제공하는 입력 책임 | 아직 검증되지 않은 위험 |
| --- | --- | --- |
| Mira 정체성 | 하나 이상의 `src_ref_images`에 승인한 단일 전신 reference를 준다. | 만화의 teal bob, hair clip, 얼굴, 흰 재킷, 청록 바지, navy flap bag, 하나의 대각 끈을 유지하는지는 미확인이다. |
| pose와 projection | neutral mannequin 또는 landmark/pose only target을 control video에 넣는다. | pose video가 reference appearance를 덮어쓰지 않는지, low angle/side/rear view에서 전신 비례가 유지되는지 미확인이다. |
| 장소와 camera | target video의 background를 구조 조건으로 사용하거나, R2V에서는 prompt로 지정한다. | V2V는 배경을 복사해 인물과 장소의 비례를 고정할 수 있지만, 인물 의상·가방의 윤곽을 다시 해석할 수 있다. |
| 웹툰 정지 컷 | 생성 영상에서 승인 frame을 골라 후속 crop·lettering에 쓴다. | 걷기 frame 하나가 자연스럽다고 해서 독립된 4개 shot의 camera/pose/identity 조건을 통과한 것은 아니다. |

### VACE preflight 설계

이 후보는 예쁜 한 frame을 찾는 실험이 아니라 **동일 reference로 서로 다른 정지 shot을 얻을 수 있는지** 확인하는 실험이다. driving video가 필수 구조는 아니지만, V2V pose/camera 제어를 검증하는 경우에는 짧은 target sequence가 가장 직접적인 입력이다.

1. 모델·API·메모리: 공개 Diffusers snapshot을 받아, CPU offload와 `480 x 832` 이하의 짧은 sequence에서 video 저장, peak VRAM, wall time을 기록한다. 이 단계가 실패하면 model quantization이나 ComfyUI 변형을 추가하지 않는다.
2. reference-only 기준: Mira single reference + prompt만으로 R2V를 실행한다. reference character의 전신·의상·가방 contract가 첫 frame과 후속 frame에서 남는지 검사한다.
3. structure-only 비교: 같은 reference에 두 개 이상의 사람이 검수한 neutral pose/camera control video를 준다. face, 가방, 의상 texture는 control video에서 제거한다. 예시는 low bend ticket, side-step, low-angle reach처럼 서로 다른 full-body box와 projection을 사용한다.
4. quality gate: 각 shot에서 full body before crop, head-neck direction, wrist endpoint, ankle/foot placement, teal bob + clip, white jacket, teal trousers, navy flap bag, one diagonal strap, 장소와 인물의 scale을 따로 판정한다. 연속 frame의 temporal smoothness는 보조 지표일 뿐이다.
5. 후속 보정: full-frame contract를 통과한 shot에서만 face 또는 bag/strap mask repair를 별도 후보로 둔다. VACE output에 inpaint를 즉시 결합해 구조 실패를 숨기지 않는다.

### 현재 결론

VACE 1.3B는 MimicMotion과 달리 공개 접근 가능한 모델이며, image reference와 pose/camera condition을 서로 다른 입력으로 줄 수 있다는 점에서 다음 실행 후보가 된다. 다만 video model이고 480p가 공식 안정 해상도이므로, 원고의 정적 웹툰 cut 생성 파이프라인으로 채택하기 전에 위의 다중 shot quality gate를 통과해야 한다. 현재는 다운로드·실행 결과가 없으므로 성공 사례로 기록하지 않는다.

### Wan2.1 VACE 1.3B reference-only preflight 실행 결과: 미채택

공개 Diffusers snapshot을 받아 `WanVACEPipeline`으로 실행했다. 기본 `enable_model_cpu_offload()`만 적용하면 T5 text encoder가 GPU에서 약 6.9 GB를 점유해 8 GB를 초과했다. prompt embedding을 CPU에서 한 번 계산한 뒤 embedding만 GPU로 보내고, video model을 sequential CPU offload하는 순서로 바꾸자 `832 x 480`, 5 frame, 50 step의 MP4 저장이 통과했다. peak VRAM은 4.739 GiB, wall time은 73.9초였다.

그러나 이 실행은 quality gate에서 탈락했다. 전신 윤곽과 흰 재킷은 일부 남았지만 teal bob과 silver clip은 흐려졌고, 청록 바지, navy horizontal flap bag, 하나의 대각 끈, railway station background가 모두 유지되지 않았다. 세 frame은 정지한 옆모습으로 수렴했으며 pose/camera control은 아직 넣지 않았다. 이 baseline이 Mira contract를 통과하지 못했으므로 control video를 더하거나 inpaint로 고치지 않는다. 생성 MP4, contact sheet, temporary runner와 local snapshot은 제거하고 [판정 기록](../../docs/assets/part-07/chapter-05/p7-5-2-wan-vace-runtime-review.json)만 보관한다.

## 다음 후보: StableAnimator basic

확인일: 2026-08-03

[StableAnimator 공식 저장소](https://github.com/Francis-Rings/StableAnimator){: target="_blank" rel="noopener noreferrer" }는 reference image와 pose sequence를 조건으로 받는 end-to-end human image animation 모델이다. image embedding과 face embedding을 함께 다루는 identity adapter를 두며, post-hoc face swap이나 restoration 없이 identity-preserving 결과를 목표로 한다. 이는 VACE와 달리 Mira의 얼굴을 단순 prompt 항목이 아니라 별도 입력 표현으로 다룬다는 점에서 다음 후보가 된다.

공식 README는 basic checkpoint가 `512 x 512` 또는 `576 x 1024`를 지원하고, 16-frame basic model이 `512 x 512`에서 8 GB VRAM을 요구한다고 명시한다. 체크포인트 구조에 Stable Video Diffusion(SVD), pose network, face encoder, U-Net 및 DWPose가 포함되고 Hugging Face repository를 직접 clone하도록 안내한다. base SVD가 gated Hugging Face dependency였던 MimicMotion과 달리, 이 프로젝트는 필요한 SVD 구조·가중치를 StableAnimator checkpoint tree에 포함한다고 문서화한다. 실제 clone 및 파일 완전성은 다운로드 후 확인한다.

### 적합성과 한계

| 항목 | StableAnimator가 직접 다루는 범위 | 이 프로젝트에서 별도 검증할 한계 |
| --- | --- | --- |
| 얼굴 identity | reference image와 face embedding을 함께 쓴다. | anime Mira에서 실사 face extractor가 얼굴·눈·hair clip을 손상시키지 않는지 확인해야 한다. |
| 전신 pose | target pose sequence를 입력으로 받는다. | target skeleton은 reference와 body shape가 align되어야 한다고 공식 README가 명시한다. 비례가 다른 target을 주면 실패 원인이 된다. |
| 의상·가방 | reference appearance를 animation에 전달한다. | navy horizontal flap bag과 하나의 대각 끈은 평가 항목으로 따로 둔다. 논문의 identity 주장이 소품 geometry를 보장하지는 않는다. |
| camera·projection | pose sequence의 각 frame에서 간접적으로 줄 수 있다. | 모델의 공개 training 조건은 static background를 권한다. low/high angle, 장소 교체, 극단 camera motion은 첫 preflight 범위가 아니다. |
| 웹툰 정지 컷 | 16-frame animation의 승인 frame을 cut 후보로 쓸 수 있다. | 한 영상의 temporal smoothness가 여러 장소와 independent shot의 camera consistency를 증명하지 않는다. |

### preflight 순서와 중단 규칙

1. **접근성·runtime**: official checkpoint와 source를 받아 `512 x 512`, 4 frame, basic inference가 8 GB GPU에서 PNG frame 저장까지 가는지 확인한다. face optimization(HJB)은 첫 실행에서 끈다.
2. **reference baseline**: Mira front full-body reference 하나와 참조에 맞춘 neutral pose sequence만 쓴다. full body, teal bob + clip, white jacket, teal trousers, navy flap bag, diagonal strap을 검수한다.
3. **pose transfer**: 같은 reference에 low bend와 side-step이라는 두 사람 검수 pose sequence를 따로 넣는다. neck direction, wrists, ankles, full-body box와 모든 identity/object contract를 독립적으로 판정한다.
4. **camera/background 경계**: 2-3이 통과해도 장소 교체나 low-angle shot을 곧바로 붙이지 않는다. static background 조건은 foreground animation 전용 제약으로 기록하며, scene generation/merge는 다른 stage로 분리한다.

첫 단계에서 checkpoint 접근, 8 GB frame 저장, 또는 anime reference의 face extraction 중 하나라도 실패하면 HJB, pose frame 수 증가, scene merge를 시작하지 않는다. 반대로 basic pose transfer가 identity와 full body를 통과하면, StableAnimator는 `character foreground pose stage` 후보가 되고 scene/camera stage는 별도 pipeline으로 재검토한다.

### StableAnimator basic 8 GB preflight 실행 결과: foreground 한정 부분 통과

공식 `FrancisRing/StableAnimator` checkpoint repository에서 animation U-Net, face encoder, pose net, DWPose와 FP16 SVD components를 확인하고 내려받았다. upstream runner는 모든 component를 GPU로 보내므로 8 GB에서 바로 실행되지 않는다. `/tmp` 복사본에서 FP16 component variant를 읽고 registered model CPU offload를 적용했으며, custom pipeline 안의 U-Net·pose net·VAE decoder 강제 GPU 이동을 제거했다. 이 경로는 `512 x 512`, 4 frame, `decode_chunk_size=1`에서 10 및 25 step 모두 PNG frame 저장까지 통과했다. Face embedding도 Mira illustration에서 생성됐다. DWPose는 현 onnxruntime가 CUDA provider를 노출하지 않아 CPU로 전처리됐다.

neutral pose에서는 full body, face, teal bob, white jacket, teal trousers, white sneakers, navy flap bag, 하나의 대각끈이 네 frame에 남았다. 하지만 이는 reference reconstruction이므로 pose transfer의 증거는 아니다. deep crouch는 공식 linear alignment가 standing reference에 맞추며 skeleton을 늘려 frame crop을 만들었다. alignment를 끈 raw pose map은 crouch-like body를 만들었지만 10과 25 step 모두 얼굴·hair clip·bag flap 계약을 잃었다.

반면 raw full-body reach pose에서는 팔 방향과 전신 box, 얼굴, 재킷·바지·신발이 남았다. hair clip은 안정적이지 않았고 navy flap bag은 사라졌으며 배경은 흰색이었다. 따라서 이 모델은 **중간 난도 전신 pose의 foreground generator**로는 후보가 되지만, face/clip 및 bag repair와 독립 scene/camera stage를 통과하기 전에는 final webtoon cut pipeline으로 채택하지 않는다. 생성 frame과 temporary runner는 제거하고 [판정 기록](../../docs/assets/part-07/chapter-05/p7-5-2-stableanimator-basic-review.json)만 보관한다.

## 후속 조사: 객체 계약 보정과 다중 참조 편집

확인일: 2026-08-03

StableAnimator의 moderate reach 결과는 전신 pose와 일부 identity를 함께 보존했지만, navy horizontal flap bag과 하나의 대각 끈을 잃었다. 이 결함은 인물 전체를 다시 생성할 이유가 아니라, **full-frame gate를 먼저 통과한 뒤 제한된 object gate로 검사할 항목**이다. 단, 현재 결과는 full-frame gate를 통과하지 않았으므로 어떤 보정 모델도 아직 연결하지 않는다. 아래 조사는 이후 보정 stage의 실행 후보를 좁히기 위한 것이다.

| 후보 | 공식 자료에서 확인한 범위 | 8 GB 및 만화 화풍 판단 | 현재 결정 |
| --- | --- | --- | --- |
| [AnyDoor](https://github.com/ali-vilab/AnyDoor){: target="_blank" rel="noopener noreferrer" } | source object mask와 target mask로 object-level customization을 수행한다. | 가방 reference와 가방 영역을 분리한다는 구조는 적합하다. 그러나 official inference는 SD 2.1와 DINOv2를 요구하며 기본 경로가 FP32 `model.cuda()`다. README에는 8 GB VRAM 예산이 없다. | 저VRAM 비공식 변경이나 대형 checkpoint 다운로드를 시작하지 않는다. 보류. |
| [ACE++](https://github.com/ali-vilab/ACE_plus){: target="_blank" rel="noopener noreferrer" } | subject LoRA는 subject consistency generation/editing을, local-editing LoRA는 mask 영역 redraw를 제공한다. | object reference와 target edit mask의 책임 분리는 적합하다. 다만 공식 workflow가 FLUX.1-Fill-dev를 base로 요구하고, 공식 학습 기본값은 38--40 GB다. 8 GB inference 예산은 명시하지 않았다. 프로젝트가 artifacts와 hand distortion도 한계로 기록한다. | 현재 장비의 다음 실행 후보에서 제외. |
| [ICEdit](https://github.com/River-Zhang/ICEdit){: target="_blank" rel="noopener noreferrer" } | instruction-based local editing과 ID persistence를 제공하며, official ComfyUI-nunchaku workflow는 4 GB VRAM 경로를 안내한다. | 8 GB preflight가 가능한 유일한 local-edit 후보로 남는다. 그러나 제작진은 base FLUX가 다양한 style을 본래 지원하지 않아 화풍을 바꿀 수 있고, realistic data 중심이라 anime/non-realistic 입력의 성공률과 품질이 낮아질 수 있다고 명시한다. | full-frame 통과 컷이 생긴 뒤 `bag+strap` mask 한 장만으로 독립 preflight한다. 화풍·face·pose·mask 밖 pixel 보존 중 하나라도 실패하면 폐기한다. |
| [FLUX.2 Klein 4B](https://github.com/black-forest-labs/flux2){: target="_blank" rel="noopener noreferrer" } | single-reference와 multi-reference editing을 모두 지원하며, 공식 README가 Klein 4B의 약 8 GB VRAM 실행을 명시한다. 4B는 Apache-2.0이다. | capability는 현 요구와 맞지만, actual official CLI가 Qwen3 text encoder와 autoencoder를 GPU에 먼저 load한다. 8 GB는 flow weight 단독 수치로 해석해야 한다. | initial candidate였으나 official runner 검토 뒤 보류. 아래의 `official runner 재검토` 판정을 따른다. |

### 초기 우선순위: official runner 재검토로 폐기

1. **FLUX.2 Klein 4B whole-shot runtime preflight**: 공개 모델, license, 정확한 inference revision을 고정하고 `512 x 768`, batch 1, Mira 단일 reference, 서로 다른 두 camera/pose contract에서 PNG 저장, peak VRAM과 시간을 기록한다. 이 단계는 object repair가 아니라 `reference-conditioned whole-shot`의 실행성과 기본 identity를 검사한다.
2. **다중 reference quality gate**: 1단계가 Mira 전신·얼굴·의상·가방 contract를 유지한 경우에만 character reference와 isolated bag reference를 함께 넣는다. background/camera target은 사람 검수 layout 또는 prompt로 별도 주되, bag reference가 body proportion이나 얼굴을 바꾸는지 검사한다.
3. **ICEdit object-only gate**: 2단계 또는 다른 branch에서 full-frame contract를 통과한 컷이 있을 때만 한 컷의 bag+strap mask를 보정한다. StableAnimator reach처럼 가방이 이미 사라지고 배경도 없는 출력에는 적용하지 않는다.

이 순서는 local inpaint로 현재 구조 실패를 감추는 것이 아니라, reference-conditioned whole-shot에서 full-frame 합격 컷을 먼저 확보하고 그 뒤 소품의 계약만 제한적으로 확인하려는 것이다. AnyDoor와 ACE++는 기능 설명만으로 8 GB 실행 가능하다고 가정하지 않으며, 공식 메모리 근거가 생기기 전까지 실행하지 않는다.

### FLUX.2 Klein 4B official runner 재검토: 실행 전 보류

공식 `black-forest-labs/flux2` source의 current CLI를 확인했다. 모델 표에는 Klein 4B가 약 8 GB VRAM에 들어간다고 쓰여 있지만, runner는 `load_text_encoder(model_name, device=torch_device)`로 Qwen3 4B text encoder를 먼저 GPU에 올리고, Klein일 때는 prompt moderation/upsampling용 별 text encoder도 추가로 준비한다. 그 뒤 autoencoder 역시 GPU 기본 device로 load한다. `--cpu_offloading`은 flow model을 CPU에서 시작하게 할 뿐, 이 초기 text encoder와 autoencoder의 GPU load 순서를 바꾸지 않는다.

따라서 이 구현을 현 8 GB GPU에서 그대로 single-reference preflight하는 것은 `Klein flow weight가 약 8 GB`라는 주장과 별개로, text encoder/autoencoder를 포함한 실제 peak VRAM을 넘어설 가능성이 높다. 이전 local CLI가 auxiliary model loading에서 실패한 관측과도 일치한다. 모든 component를 CPU/GPU 사이에서 교대로 이동하도록 unofficial runner를 새로 만드는 일은 model 자체의 8 GB 실행성을 검증하는 실험이 아니므로 시작하지 않는다. Klein 4B를 현 pipeline의 다음 whole-shot 후보에서 **보류**한다.

이에 따라 우선순위 1은 실행하지 않고 종료한다. ICEdit은 공식 4 GB ComfyUI-nunchaku 경로가 있으나, full-frame 합격 컷이 생긴 뒤 object-only gate로 한정한다. 현 시점에서 foreground pose의 부분 통과만 있으며 scene/camera와 bag contract를 만족한 full-frame source가 없으므로 ICEdit도 아직 실행하지 않는다. 다음 외부 조사는 low-VRAM whole-shot reference generation이 아니라, StableAnimator foreground 결과를 scene/camera stage로 연결할 수 있는 공개 8 GB composition 방법의 공식 실행 근거를 찾는 것으로 전환한다.

## 후속 후보: CharaConsist composition 접근성 preflight

확인일: 2026-08-03

[CharaConsist 공식 저장소](https://github.com/Murray-Wang/CharaConsist){: target="_blank" rel="noopener noreferrer" }는 FLUX.1 기반 training-free character consistency 구현이며, 고정 배경의 foreground/background 일관성, 다른 배경의 foreground 일관성, 일부만 고정하는 mixed background를 notebook과 batch runner로 분리해 제공한다. 이는 StableAnimator가 부분 통과한 `foreground pose`와 장소·camera stage를 같은 모델에 억지로 결합하지 않고, foreground/background 책임을 분리하는 설계 근거가 된다.

공식 README는 `init_mode=3`을 single GPU sequential CPU offload, GPU memory 3 GB로 표기한다. source의 `init_model_mode_3()`도 실제로 `CharaConsistPipeline.from_pretrained(..., torch_dtype=torch.bfloat16)` 뒤 `enable_sequential_cpu_offload()`를 호출한다. `share_bg`와 `save_mask` 옵션이 있고, 한 prompt group 안에서 먼저 ID image를 만든 뒤 이어지는 frame의 foreground/background attention과 자동 mask를 다룬다. 즉 단순 PNG alpha merge와는 다른, 생성 단계의 composition 후보이다.

### 현 환경 preflight 결과: 접근 조건 대기

공식 source commit `759018c`를 `/tmp`에서 확인했다. 현재 repository `.venv`의 `torch 2.11.0+cu128`, `diffusers 0.37.0`, `transformers 4.57.6`, `accelerate 1.13.0`는 README의 tested requirements보다 새 버전이지만 custom `CharaConsistPipeline` import는 통과했다. 디스크 여유는 1.5 TB, 사용 가능 CPU RAM은 55 GiB라서 model snapshot과 sequential offload의 host-side 요구량은 수용 가능하다.

그러나 runner가 요구하는 `black-forest-labs/FLUX.1-dev` Hugging Face model card는 unauthenticated API에서 `gated=auto`이며, 현 환경의 Hugging Face CLI는 로그인되지 않은 상태다. 따라서 weights download, `init_mode=3` PNG 저장, peak VRAM, quality gate는 아직 실행하지 않았다. gated access를 우회하거나 다른 base model을 끼워 넣지 않는다. 사용자가 해당 model license 접근을 승인하고 이 환경에 인증한 뒤에만 다음의 한 장 preflight를 실행한다.

1. `512 x 768`, `init_mode=3`, `share_bg`와 `save_mask`를 켜고 ID image와 한 개 frame PNG/mask를 저장한다.
2. VRAM peak, CPU RAM peak, time, generated mask가 실제 foreground와 맞는지 기록한다.
3. 실행이 통과해도 Mira pose, face, bag/strap, low-angle camera를 통과한 것으로 주장하지 않는다. 그 뒤 StableAnimator foreground와 CharaConsist scene을 연결할 수 있는 입력/출력 경계부터 별도 검증한다.

## 보조 조사: VNCCS는 final cut generator가 아니라 reference asset 보강 도구

[ComfyUI VNCCS](https://github.com/AHEKOT/ComfyUI_VNCCS){: target="_blank" rel="noopener noreferrer" }는 8 GB에서 동작한다고 안내하는 visual-novel character sprite workflow다. character creator, cloner, clothing, emotion, pose studio, background removal을 묶어 full-body sprite와 LoRA dataset을 만드는 목적이며, `Pose Studio`에서 reference character와 맞는 age, height, body type을 선택하도록 한다. official README도 clone input이 full body가 아니면 보이지 않는 부분을 model이 invent한다고 명시한다.

이는 이 프로젝트의 `full body before crop`, 단일 reference라도 head-to-sole와 clothing/object가 보이는 구성이 필요하다는 판단을 보강한다. 그러나 같은 README가 현 기능의 끝을 sprite generation으로 두고 animation, 3D environment, environment 안 CG 생성은 planned feature로 제시한다. 따라서 이 workflow를 low-angle 장소 컷, foreground/background scale, bag의 physical attachment를 검증하는 final webtoon pipeline으로 채택하지 않는다. reference pack의 missing view를 만들 때의 보조 후보로만 보류한다.

## 제외 확인: StoryDiffusion의 실제 VRAM 경계

[StoryDiffusion 공식 저장소](https://github.com/HVision-NKU/StoryDiffusion){: target="_blank" rel="noopener noreferrer" }는 SD 1.5/SDXL 기반 모델에 consistent self-attention을 hot-plug하고 최소 3개, 권장 5--6개의 text prompt로 long-range character consistency를 생성한다. 여러 독립 컷의 character repetition을 검사할 수 있다는 점은 webtoon workflow에 관련 있다.

그러나 official local demo의 low GPU memory version도 Tesla A10 24 GB GPU와 30 GB RAM에서 시험됐으며, 20 GB 초과 GPU에서 잘 동작할 것으로 안내한다. 이는 8 GB RTX 5070 Laptop GPU 조건과 양립하지 않는다. 또한 prompt group 반복은 pose endpoint, camera projection, object attachment를 직접 조건으로 주는 경로가 아니다. 따라서 StoryDiffusion을 이 환경의 재실행 후보와 8 GB 최종 pipeline 후보에서 제외한다.

## 상위 하드웨어 기준선: One-to-All Animation

[One-to-All Animation 공식 저장소](https://github.com/ssj9596/One-to-All-Animation){: target="_blank" rel="noopener noreferrer" }는 single reference image에서 retargeted pose와 direct pose를 받아 character animation 및 static image pose transfer를 수행한다. 1.3B-v2는 large camera movement data와 더 큰 image ratio로 추가 학습되어, 1.3B 계열 중 dynamic video와 image benchmark에 더 적합하다고 명시한다. 공개 training data에 cartoon data를 포함하고 Apache-2.0 code/checkpoint 경로도 제공하므로, face·hair·object가 있는 만화 캐릭터에 다양한 pose와 camera 변화를 적용한다는 현재 목표의 강한 공개 기준선이다.

그러나 공식 GPU-poor 실행 안내조차 1.3B + ComfyUI를 Kaggle 16 GB T4에서 `832 x 480`, 10초 영상 약 11분으로 제시한다. 8 GB 실행 수치나 sequential CPU offload 경로는 제공하지 않는다. 따라서 이 모델은 현 장비에서 비공식 저VRAM 변형을 만들거나 다운로드해 실행하지 않으며, **16 GB 이상 환경에서 검증할 상위 품질 branch**로 분리한다. 현 8 GB branch의 output을 이 결과 수준과 동일하다고 주장하지 않는다.

## 3D 구조 보조 후보: LHM의 적용 경계

[LHM 공식 저장소](https://github.com/aigc3d/LHM){: target="_blank" rel="noopener noreferrer" }는 single full-body image에서 animatable human reconstruction과 mesh export를 제공한다. 전신 reference를 camera view, depth, silhouette, 관절 landmark의 구조 기준으로 전환하려는 목적에는 관련이 있다. 특히 image-only skeleton보다 body volume과 camera projection을 함께 검수할 수 있다는 점은 의미가 있다.

하지만 original LHM의 custom motion Gradio path는 pose estimator 때문에 LHM-500M에서도 24 GB GPU를 요구한다. 2026년 LHM++의 `8-view input, 8 GB` 표기는 eight-view **input** reconstruction 효율이며, single image source와 target pose/camera로 webtoon cut을 생성하는 8 GB animation 경로를 의미하지 않는다. 따라서 LHM을 StableAnimator나 SDXL의 대체 final generator로 쓰지 않는다. 16/24 GB 이상에서 mesh를 얻을 수 있을 때만, pose map 대신 target camera의 silhouette/depth/landmark를 설계·검수하는 structural auxiliary로 재검토한다.

## Wan VACE 재실행 제외: framework가 아니라 full-frame 품질의 문제

[DiffSynth-Studio Wan 문서](https://github.com/modelscope/DiffSynth-Studio/blob/main/docs/en/Model_Details/Wan.md){: target="_blank" rel="noopener noreferrer" }는 `Wan-AI/Wan2.1-VACE-1.3B`에 reference image, VACE pose/control video, `camera_control_direction`, low-VRAM offload를 노출한다. 즉 VACE를 다른 runner로 실행하면 camera direction이나 disk offload를 추가할 수 있다. 이는 runtime feature의 차이이지 character model의 identity 능력이 더 생긴다는 근거는 아니다.

VACE 공식/커뮤니티 workflow의 6 GB 사례도 reference image + DWPose driving video는 동작하지만 white background 외 장면에는 아직 성공하지 못했다고 기록한다. 이는 이 프로젝트의 VACE reference-only 결과에서 railway station, teal trousers, flap bag, diagonal strap이 사라지고 정지한 옆모습으로 수렴한 관측과 같은 위험을 보강한다. 이미 baseline full-frame contract가 탈락했으므로, DiffSynth나 ComfyUI wrapper의 low-VRAM runtime만 바꾸어 pose video·camera control·inpaint를 추가하는 실험은 하지 않는다.

## Hugging Face 무인증 경로: InvokeAI FLUX.2 Klein 4B whole-shot preflight

확인일: 2026-08-03

사용자 환경에는 Hugging Face 인증정보가 없다. 따라서 gated `FLUX.1-dev`를 요구하는 CharaConsist와 gated SVD를 요구하는 MimicMotion은 접근 조건 대기가 아니라 현재 8 GB branch에서 **제외**한다. 공개 model card를 무인증 API로 다시 확인한 결과 `black-forest-labs/FLUX.2-klein-4B`와 `unsloth/FLUX.2-klein-4B-GGUF`는 gated가 아니었다.

이전 BFL raw CLI의 실패는 FLUX.2 Klein 자체의 즉시 배제가 아니라 runner의 component load 순서 문제였다. [InvokeAI 공식 source](https://github.com/invoke-ai/InvokeAI){: target="_blank" rel="noopener noreferrer" }는 Klein 4B GGUF Q4 변환기와 별도 VAE/Qwen3 encoder를 model manager로 등록하고, Qwen3 text encoder invocation을 idle GPU offload 대상으로 다룬다. 공개 bundle의 실제 local 구성은 GGUF Q4 `2,604,311,104` bytes, VAE `168,121,699` bytes, Qwen3 4B encoder+tokenizer `8,060,907,021` bytes였다. 이는 raw BFL CLI를 patch하는 일이 아니라 공식 InvokeAI runner의 공개 model integration을 검증하는 별도 경로다.

### 단일 reference whole-shot 실행 결과: 부분 통과

RTX 5070 Laptop GPU 8 GB에서 InvokeAI 6.14 source runtime과 CUDA 12.8 PyTorch를 격리 설치했다. Mira `single-01`을 reference conditioning에 연결하고 `512 x 768`, Euler, 4 step, seed `320241`, Qwen3 max sequence length `256`으로 두 개의 독립 prompt를 실행했다.

| gate | 관측 runtime | full-frame 사람 검수 |
| --- | --- | --- |
| 영화관 counter에서 ticket을 보는 전신 | 14.4초, peak `5,552 MiB` | 전신, teal bob + silver clip, white jacket, teal trousers, white sneakers, right-hip navy flap bag, one diagonal strap, ticket, cinema background 통과 |
| 지하철 계단을 내려가는 low-angle 3/4 보행 | 20.6초, peak `5,673 MiB` | 전신 보행·계단 원근·팔 균형과 동일 character/object contract 통과 |

두 결과는 raw BFL CLI와 달리 public model만으로 8 GB에서 reference-conditioned whole-shot이 실제 PNG까지 생성됨을 보인다. 또한 OpenPose driving input 없이 natural-language action과 camera direction이 reference의 정체성 contract와 함께 나타난 첫 보존 출력이다. 다만 sample은 하나의 identity reference와 두 prompt뿐이다. side/rear, 극단 camera, hand-object contact, multi-reference bag binding, 같은 캐릭터의 여러 장소 반복, inpaint 후 pixel preservation은 아직 검증하지 않았다. 따라서 FLUX.2 Klein 4B InvokeAI 경로는 다음 diversity gate의 **후보**이고, final webtoon pipeline 채택이나 object repair stage 진입의 근거는 아니다.

### InvokeAI 의존성 분리: direct Diffusers 실행 결과

InvokeAI 결과가 application-specific capability인지 분리하기 위해 repository `.venv`의 `diffusers 0.37.0`을 확인했다. 이 버전에는 `Flux2KleinPipeline`과 `enable_sequential_cpu_offload()`가 포함돼 있다. 같은 공개 `black-forest-labs/FLUX.2-klein-4B` 원본 BF16 pipeline을 `from_pretrained()`로 CPU에 읽고 sequential CPU offload만 켰다. InvokeAI server, model manager, GGUF loader, workflow graph를 사용하지 않았다.

| 항목 | BFL raw CLI | InvokeAI Q4 | Direct Diffusers BF16 |
| --- | --- | --- | --- |
| Transformer/encoder 배치 | Qwen3·보조 모델·VAE를 GPU에 먼저 load | component manager가 교대 | accelerate hook이 module 단위 GPU/CPU 교대 |
| 실행 결과 | auxiliary model GPU load에서 실패 | two single-reference gate 통과 | same two gate 통과 |
| 기준 scene | 없음 | 14.4초, peak 5,552 MiB | 11.7초, peak 1,834 MiB |
| low-angle walk | 없음 | 20.6초, peak 5,673 MiB | 11.6초, peak 2,090 MiB |
| 운영 비용 | runner 수정 없이는 8 GB 부적합 | Q4 transformer + separate 8 GB encoder install | 원본 BF16 pipeline cache 약 13 GB, CPU RAM과 매 run component reload |

직접 Diffusers의 영화관 출력은 full body, teal bob + silver clip, white jacket, teal trousers, white sneakers, right-hip navy flap bag, one diagonal strap, ticket과 cinema background를 통과했다. low-angle 계단 보행도 전신 보행·원근과 동일 identity/object contract를 통과했다. Q4와 BF16 precision, loader, random-number implementation이 달라 image pixels는 InvokeAI output과 일치하지 않지만, 품질 gate의 결론은 같다.

따라서 차이는 generation model이나 reference conditioning의 유무가 아니라 **component를 GPU에 동시에 올리는가, forward 시점에 순차적으로 올리는가**다. 현재 8 GB minimal pipeline 후보는 `Diffusers Flux2KleinPipeline + public 4B model + enable_sequential_cpu_offload()`이며, InvokeAI는 같은 capability를 Q4·model manager UI로 포장한 선택 실행기일 뿐 필수 의존성이 아니다. 다만 아직 multi-reference, side/rear/extreme camera, hand-object contact, multi-scene repetition은 둘 다 검증하지 않았다.
