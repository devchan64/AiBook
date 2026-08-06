# Part 7 웹툰 캐릭터 일관성 참고자료 노트

이 문서는 `P7-5.2 ComfyUI workflow로 LoRA, ControlNet, IP-Adapter 조합 보기`를 확장할 때 사용할 참고자료를 원고 작성 관점에서 정리한 작업 노트입니다. 목적은 웹툰 제작 도구 사용법을 길게 설명하는 것이 아니라, `같은 캐릭터를 여러 컷에서 유지하기 위해 어떤 제어 신호를 어떻게 기록할 것인가`를 학부 수준 독자가 따라갈 수 있는 설명 흐름으로 바꾸는 것입니다.

## 원고에 반영할 중심 문장

- 웹툰용 생성형 이미지 workflow의 목표는 `한 장의 좋은 이미지`가 아니라 `여러 컷에서 같은 캐릭터로 보이는 결과`를 만드는 것이다.
- 캐릭터 일관성은 한 장치로 해결하기보다 `캐릭터 기준서`, `캐릭터 LoRA 또는 DreamBooth`, `IP-Adapter 참조 이미지`, `ControlNet 또는 T2I-Adapter 구조 제어`, `inpaint/img2img 수정`, `후편집`을 나누어 기록할 때 설명하기 쉽다.
- LoRA와 DreamBooth는 `누구인가`를 모델에 더 강하게 묶는 장치로 설명한다.
- IP-Adapter는 `이 기준 이미지와 얼마나 닮게 할 것인가`를 조절하는 장치로 설명한다.
- ControlNet과 T2I-Adapter는 `어떤 자세, 선화, depth, 컷 구도를 따를 것인가`를 조절하는 장치로 설명한다.
- ComfyUI workflow는 여러 모델을 연결하는 시각적 기록 장치로 사용한다. 초심자에게는 모든 노드를 외우게 하기보다, checkpoint, LoRA, ControlNet, IP-Adapter, sampler가 어느 입력을 맡는지 따라가게 한다.
- 실패는 `이미지가 마음에 들지 않는다`가 아니라 `얼굴 일관성`, `의상 색`, `pose`, `구도`, `손과 소품`, `말풍선 공간`처럼 다음 수정 행동으로 나눠 적게 한다.
- 기존 상업 캐릭터를 그대로 학습하거나 참조 이미지로 반복 사용하는 방식은 원고 예시에서 피한다. 자체 제작 캐릭터, 직접 만든 reference sheet, 허락받은 이미지, 라이선스가 확인된 자료만 실습 대상으로 둔다.

## 자료 묶음

| 자료 | 원고에서 쓸 역할 | 반영 수준 |
| --- | --- | --- |
| DreamBooth 논문 | 소수 이미지로 특정 subject를 새 장면에 재생성한다는 개인화 생성의 기준점 | 개념 근거 |
| Diffusers DreamBooth 문서 | 학습 이미지, prompt, fine-tuning을 실습 문장으로 풀 때 참고 | 실습 보조 |
| Diffusers LoRA training 문서 | 캐릭터 LoRA를 `가볍게 추가 학습한 adapter`로 설명할 때 참고 | 실습 보조 |
| IP-Adapter 논문 | 텍스트 prompt와 이미지 prompt를 분리해 참조 이미지를 반영한다는 근거 | 개념 근거 |
| Diffusers IP-Adapter 문서 | reference image와 scale을 기록하는 이유 설명 | 실습 보조 |
| ComfyUI IPAdapter 저장소 | ComfyUI 안에서 참조 이미지 기반 노드를 연결하는 예시 | workflow 후보 |
| ControlNet 논문/저장소 | pose, edge, depth 같은 조건으로 diffusion 출력을 제어한다는 근거 | 개념 근거 |
| ComfyUI ControlNet examples | ControlNet을 ComfyUI workflow로 읽는 예시 | workflow 후보 |
| T2I-Adapter 저장소 | 조건 제어 계열을 ControlNet 하나로만 좁히지 않기 위한 보조 자료 | 확장 후보 |
| ComfyUI workflow 문서 | workflow를 저장하고 다시 열 수 있는 노드 그래프 산출물로 설명 | 기록 기준 |
| ComfyUI workflow template 문서 | 반복 제작용 workflow template 개념을 설명할 때 참고 | 확장 후보 |
| ComfyUI examples 저장소 | 초심자에게 공식 예제부터 확인하게 하는 입구 | workflow 후보 |
| kohya-ss/sd-scripts | 직접 LoRA 학습으로 넘어갈 때 사용할 오픈소스 실무 자료 | P7-5.3 연결 |

## 자료별 요약

### DreamBooth

DreamBooth는 특정 subject를 몇 장의 이미지로 학습해, 그 subject가 다른 장면과 문맥에 등장하도록 만드는 방법입니다. 웹툰 원고에서는 이를 `캐릭터가 누구인지 모델에 새로 묶는 방법`의 대표 사례로 사용할 수 있습니다.

원고 반영 포인트는 다음과 같습니다.

- 캐릭터 기준 이미지가 적더라도 일관성 있는 subject를 만들려는 접근입니다.
- 과적합과 복제 위험이 있으므로, 학습 이미지의 권리와 사용 범위를 먼저 확인해야 합니다.
- Part 7 본문에서는 DreamBooth를 깊게 구현하기보다, LoRA와 함께 `캐릭터 개인화 학습`의 배경으로 짧게 연결하는 편이 적절합니다.

### LoRA training

LoRA는 전체 모델을 다시 학습하기보다 작은 adapter를 학습해 특정 스타일, 인물, 물체, 질감을 보강하는 방식으로 설명할 수 있습니다. 웹툰 확장에서는 캐릭터 LoRA가 `캐릭터의 고유 특징을 반복 컷에 붙잡아 두는 장치`가 됩니다.

원고 반영 포인트는 다음과 같습니다.

- 캐릭터 LoRA에는 trigger token, caption 규칙, sample prompt, 학습 이미지 구성 기록이 필요합니다.
- LoRA strength를 높이면 캐릭터 특징은 강해질 수 있지만 pose나 prompt 반응이 굳을 수 있습니다.
- P7-5.2에서는 LoRA를 사용하고, P7-5.3에서는 직접 학습할 때의 데이터셋·caption·sample prompt 기록으로 연결합니다.

### IP-Adapter

IP-Adapter는 텍스트 prompt와 별도로 이미지 prompt를 넣어 참조 이미지의 시각 정보를 반영하는 접근입니다. 웹툰 컷에서는 캐릭터 reference sheet나 이전 컷 이미지를 넣어 얼굴, 색감, 스타일 흔들림을 줄이는 장치로 설명할 수 있습니다.

원고 반영 포인트는 다음과 같습니다.

- IP-Adapter는 캐릭터를 새로 학습하는 장치라기보다, 컷마다 기준 이미지를 참조하게 하는 장치로 설명합니다.
- `ip_adapter_scale`은 reference image 영향이 너무 약하거나 너무 강할 때 조정할 기록값입니다.
- 얼굴은 닮았지만 pose가 굳거나 구도가 reference image 쪽으로 끌리는 실패를 함께 적게 합니다.

### ControlNet

ControlNet은 pose, canny edge, depth, segmentation, lineart 같은 조건을 diffusion 모델에 넣어 구조를 제어하는 방법입니다. 웹툰에서는 스토리보드의 pose, 카메라 각도, 컷 안 여백, 선화 구도를 유지하는 설명에 적합합니다.

원고 반영 포인트는 다음과 같습니다.

- ControlNet은 `캐릭터가 누구인가`보다 `어떤 자세와 구도를 따르는가`에 가깝습니다.
- ControlNet scale이 너무 강하면 캐릭터가 닮아도 컷이 뻣뻣해질 수 있습니다.
- 실패 기록은 `pose 입력 문제`, `conditioning scale 문제`, `prompt와 구조 조건의 충돌`로 나누어 적게 합니다.

### T2I-Adapter

T2I-Adapter는 text-to-image 모델에 추가 조건을 붙여 제어 능력을 넓히는 계열 자료입니다. 본문에서 필수 실습으로 넣기보다는, ControlNet이 전부가 아니며 조건 제어에는 여러 adapter 방식이 있다는 확장 후보로 둘 수 있습니다.

원고 반영 포인트는 다음과 같습니다.

- 학부 수준 독자에게는 ControlNet을 중심으로 설명하고, T2I-Adapter는 `비슷한 문제의 다른 adapter 접근` 정도로 짧게 둡니다.
- P7-5.2 본문에 넣는다면 각주나 참고자료 목록에 두는 편이 적절합니다.

### ComfyUI workflow

ComfyUI는 생성 과정을 노드 그래프로 보여 주기 때문에, 웹툰 컷 일관성 실습에서 `무엇을 바꿨는가`를 기록하기 좋습니다. workflow 파일, 모델 파일명, reference image, control image, seed, 바꾼 노드 값이 산출물이 됩니다.

원고 반영 포인트는 다음과 같습니다.

- ComfyUI는 제작 결과물보다 `재현 가능한 workflow 기록`을 설명하는 장치로 사용합니다.
- template은 episode나 character별 반복 workflow를 저장하는 개념으로 연결할 수 있습니다.
- 초심자에게는 custom node 생태계 전체보다 공식 예제와 최소 조합 workflow를 먼저 보게 합니다.

### 출력 해상도와 검수

SDXL 공식 문서는 기본 `1024 x 1024`를 가장 좋은 결과를 목표로 하는 해상도로 설명하고, `768`도 지원하지만 더 낮은 세부 품질을 전제로 둡니다. 따라서 웹툰 캐릭터 일관성 실습에서는 출력 해상도를 단순 저장 형식이 아니라 얼굴, 손, 머리 끝, 의상 장식의 판정 가능성을 바꾸는 실행 조건으로 기록해야 합니다.

원고 반영 포인트는 다음과 같습니다.

- 여러 pose·camera view·배경을 빠르게 훑는 매트릭스는 `768 x 1024` 같은 preview 해상도로 먼저 생성할 수 있습니다.
- 동일 인물성 판정이 애매한 컷은 목표 세로 비율에서 더 큰 해상도로 다시 생성하고, 높인 해상도, 생성 시간, VRAM 조건을 함께 남깁니다.
- VAE slicing과 CPU offload는 제한된 GPU 메모리에서 반복 실행을 가능하게 하는 방식이며, 캐릭터 일관성을 높이는 모델 제어 장치로 설명하지 않습니다.
- VAE tiling은 큰 출력에서 메모리를 낮출 수 있지만 타일별 색조 차이가 생길 수 있으므로, 결과 비교에서는 적용 여부를 기록합니다.

### OpenPose 조건 검증

`xinsir/controlnet-openpose-sdxl-1.0`은 Apache-2.0으로 표기된 공개 SDXL OpenPose ControlNet 후보입니다. 자체 작성한 색상 관절 지도를 입력한 실제 3 x 3 실행에서는 전신·허리 위·close-up 프레이밍과 정면·비대칭·측면 보행의 관절 배치 변화는 확인했습니다. 다만 OpenPose는 동일 인물의 얼굴과 머리를 고정하는 장치가 아니므로, 이 결과만으로 캐릭터 일관성이 입증되지는 않습니다.

같은 조건에 Apache-2.0 `h94/IP-Adapter`의 SDXL 가중치와 허리 위 기준 이미지 한 장을 추가한 두 번째 3 x 3 실행에서는 노란 후드, 청록 바지, 짧은 검은 단발의 반복성이 더 뚜렷해졌습니다. 그러나 얼굴 세부와 의상 배색은 계속 달라졌습니다. 원고에서는 이를 성공 사례가 아니라 `참조 이미지로 개선은 가능하지만 한 장의 참조만으로는 불충분`한 중간 결과로 기록합니다.

### 포즈 시퀀스와 애니메이션 후보

정지 이미지 한 장에 OpenPose 조건을 넣는 실험은 프레임마다 독립적으로 확산 과정을 다시 시작합니다. 따라서 관절 지도가 바뀌었다고 해서 전신 비율, 얼굴, 손, 의상이 같은 인물로 이어지거나 시간적으로 매끄럽다는 보장은 없습니다. 전신 포즈와 애니메이션을 검수하려면 `기준 캐릭터 이미지 + 구동 동작 영상 또는 pose 시퀀스 -> 연속 프레임` 구조의 사람 애니메이션 모델을 별도로 써야 합니다.

| 후보 | 입력과 강점 | 라이선스 및 실행 판단 | 이 책에서의 위치 |
| --- | --- | --- | --- |
| AnimateDiff + ControlNet | motion adapter와 프레임별 OpenPose 조건을 결합할 수 있습니다. Diffusers에는 video-to-video ControlNet 예제가 있습니다. | AnimateDiff 저장소 코드는 Apache-2.0이지만, 함께 쓰는 base model, motion adapter, LoRA, ControlNet의 가중치 라이선스는 각각 확인해야 합니다. 참조 캐릭터를 고정하는 전용 모델은 아니므로 단독 채택하지 않습니다. | `시간축 조건을 추가한 대조 실험` 후보 |
| MimicMotion | 기준 인물 이미지와 pose guidance로 사람 동작 영상을 생성하며, pose confidence와 latent fusion으로 긴 영상의 매끄러움을 목표로 합니다. | 저장소 코드는 Apache-2.0입니다. 배포 가중치는 SVD를 이용해 fine-tuning됐고 `other` 라이선스로 표기되므로, SVD Community License의 사용 범위·고지·접근 동의도 함께 확인해야 합니다. 72-frame 설정은 576 x 1024와 16 GB VRAM을 안내하며, 8 GB 환경에서는 VAE CPU 실행 또는 더 작은 검증이 필요합니다. | `전신 포즈 추종`의 우선 검증 후보 |
| MagicAnimate | 기준 이미지와 구동 영상을 입력해 reference attention, appearance encoder, DensePose 조건으로 시간적으로 일관된 사람 영상을 생성합니다. | 코드는 BSD-3-Clause, 전용 가중치는 BSD-3-Clause입니다. 기반 Stable Diffusion 1.5는 OpenRAIL-M, MSE VAE는 MIT입니다. 전용 가중치만 약 8.5 GB이며 공식 스크립트는 모든 주요 모듈을 GPU로 옮기므로 8 GB에서는 순차 CPU offload 적용과 짧은 clip 검증이 필요합니다. | `가중치 접근 가능`한 전신 pose animation 후보 |
| MusePose | 기준 이미지 속 인물을 pose sequence에 따라 움직이는 공개 구현이며 pose align 단계를 제공합니다. | 코드는 MIT이지만 배포 모델과 테스트 데이터는 비상업 연구용으로 제한됩니다. 이 책의 일반 실습 결과물 후보에서는 제외합니다. | 구조와 한계를 읽는 참고자료 |
| Animate Anyone | 기준 이미지와 pose sequence로 캐릭터 애니메이션을 목표로 한 대표 연구입니다. | 저장소 코드는 Apache-2.0이지만, 공개 저장소에는 재현 가능한 배포 가중치·추론 절차가 충분히 갖춰져 있는지 별도 검증이 필요합니다. | 방법론의 기준 논문/저장소 |
| Wan-Animate | 기준 캐릭터 이미지와 구동 영상으로 몸 동작과 표정을 함께 옮기며, skeleton과 얼굴 특징을 분리해 사용합니다. | 공식 프로젝트 페이지가 학술 연구와 효과 시연 전용임을 밝히므로, 범용 공개 실습 결과물에는 채택하지 않습니다. | 최신 접근의 비교 참고자료 |
| ComfyUI Frame Interpolation | 이미 생성한 인접 프레임 사이에 RIFE, FILM 등 보간기를 적용합니다. | 확장 저장소는 MIT이지만, 보간기는 새 pose를 만들거나 캐릭터 정체성을 복구하지 않습니다. 원본 프레임 검수를 통과한 뒤에만 사용합니다. | 후처리 보조 도구 |

#### 권장 검증 순서

1. 자체 제작한 전신 캐릭터 기준 이미지와 권리 확인이 끝난 2~4초 구동 영상을 준비합니다. 구동 영상에서는 전신이 잘리지 않고, 팔·다리·손이 보이는 동작을 먼저 고릅니다.
2. 구동 영상에서 DWPose 또는 동등한 관절 추정기로 frame별 pose를 뽑고, 원 영상 위에 관절을 겹쳐 그립니다. 관절이 손목·발목·무릎을 놓치면 생성 모델을 바꾸기 전에 입력을 고칩니다.
3. 사람 애니메이션 모델의 첫 16프레임만 생성합니다. 전신 높이, 좌우 팔다리, 손 개수, 머리 길이, 의상 색을 프레임별로 검사해 pose 추종과 동일 인물성을 분리해 판정합니다.
4. 이 검수를 통과한 모델만 2~4초 구간으로 늘립니다. 프레임 보간은 이 단계 뒤에 fps를 높이기 위한 선택 사항이며, 불량 프레임을 숨기는 방법으로 사용하지 않습니다.
5. 얼굴, 눈, 손, 머리카락의 국소 보정은 연속 프레임의 기준 외형이 확보된 뒤에 mask 기반 inpaint 또는 참조 기반 보정으로 적용합니다. 독립 프레임마다 별도 보정하면 시간적 깜박임이 늘어날 수 있습니다.

현재 8 GB GPU에서 이미 검증한 SDXL OpenPose/IP-Adapter 조합은 1단계의 정지 이미지 기준서 제작에는 쓸 수 있지만, 2~4단계의 포즈 애니메이션 검증을 대신하지 못합니다. 다음 실행은 MimicMotion처럼 기준 이미지와 pose sequence를 함께 받는 후보의 모델 가중치 조건을 확인한 뒤, 짧은 전신 동작으로 시작해야 합니다.

### 2026-08-01 접근성 확인

- MimicMotion 코드의 `LICENSE`는 Apache-2.0이지만, 실제 가중치는 SVD 기반 fine-tuning입니다. SVD의 `model_index.json` 접근을 시도한 결과 현재 실행 계정에는 gated repository 인증·접근 동의가 없어 `401 GatedRepoError`가 발생했습니다. 동의를 자동화하거나 우회하지 않았으므로, 이 환경에서는 아직 MimicMotion 실행 자산을 받을 수 없습니다.
- MagicAnimate의 전용 가중치와 `runwayml/stable-diffusion-v1-5`, `stabilityai/sd-vae-ft-mse`는 모두 비게이트로 조회됐습니다. 그러나 전용 appearance encoder, DensePose ControlNet, temporal attention 가중치의 합계가 약 8.5 GB이고, 기본 추론 코드는 이 모듈들을 모두 GPU에 올립니다. 따라서 다운로드 전에 `16 frame`, 낮은 출력 해상도, 순차 CPU offload를 적용할 수 있는 별도 실행 경로를 마련하고 실제 VRAM·출력 품질을 검수해야 합니다.
- `guoyww/animatediff-motion-adapter-sdxl-beta`는 비게이트지만 모델 카드에 라이선스 값이 없습니다. 코드 저장소의 Apache-2.0만으로 가중치 사용 범위를 대신할 수 없으므로, 이 예제의 배포 자산 후보에서는 제외합니다.

### 기준 캐릭터 리깅 경로

전신 pose와 얼굴·의상·화풍의 완전한 동일성을 동시에 보여 주어야 할 때는, diffusion이 매 컷을 다시 그리는 경로만 고집하지 않습니다. 자체 생성 기준 캐릭터의 머리, 몸통, 팔, 다리를 분리한 뒤 cutout rig로 움직이면 동일 부품을 재사용하므로 얼굴·눈·머리카락·의상은 검증 가능한 불변값이 됩니다. 이 방식은 pose generation 모델의 대체가 아니라, `동일 인물성은 반드시 유지`해야 하는 컷을 위한 하이브리드 제작 경로입니다.

- Blender Grease Pencil은 armature나 parent object에 연결해 2D stroke를 animation할 수 있습니다.
- OpenToonz Plastic은 한 drawing에 skeleton과 mesh를 설정해 cutout animation으로 변형할 수 있습니다.
- Python 실습에서는 외부 도구 설치 전에 이 원리를 축소해, 자체 생성한 전신 기준 이미지의 부품 mask와 관절 anchor를 코드로 기록하고 rest, wave, step을 실제로 출력합니다.
- 이 경로의 검수는 `같은 pixel 부품을 썼는가`, `팔·다리 pose가 달라졌는가`, `camera crop이 같은 전신 원본에서 파생됐는가`로 합니다. 뒤돌기, 큰 원근 변화, 가림은 한 장의 평면 rig 한계이므로 정면·반측면·측면 기준 부품 또는 3D rig가 추가로 필요합니다.

### kohya-ss/sd-scripts

`kohya-ss/sd-scripts`는 LoRA 학습 실무 자료로 의미가 있습니다. P7-5.2에서는 캐릭터 LoRA가 필요하다는 문제만 열고, 직접 학습의 세부는 P7-5.3으로 넘기는 연결 자료로 쓰는 것이 좋습니다.

원고 반영 포인트는 다음과 같습니다.

- 학습 이미지셋, caption 규칙, 반복 횟수, sample prompt를 기록해야 합니다.
- 웹툰 캐릭터에서는 정면 이미지만 모으지 말고 표정, 측면, 의상, 손·소품 상태를 기준서와 맞추어 구성해야 합니다.
- 직접 학습은 저작권과 사용권 확인이 특히 중요합니다.

## 원고 확장 제안

P7-5.2에는 이미 `웹툰 컷에서 캐릭터 일관성 유지하기` 절이 들어갔으므로, 다음 개선은 짧은 문단과 출처 보강 수준이 적절합니다.

1. `자료 묶음`에서 DreamBooth, Diffusers LoRA training, ComfyUI workflow template, ComfyUI ControlNet examples, T2I-Adapter, kohya-ss/sd-scripts를 출처 목록에 추가합니다.
2. 본문에는 `캐릭터 LoRA 또는 DreamBooth`라는 표현을 한 번 넣어, 캐릭터 개인화 학습 계열의 배경을 열어 둡니다.
3. `ControlNet` 설명에 `pose, lineart, depth`를 명시해 웹툰 스토리보드와 연결합니다.
4. `workflow 기록 양식`에 `template_name`이나 `workflow_version`을 추가할지 검토합니다.
5. P7-5.3에서는 직접 LoRA 학습 절로 넘겨, 캐릭터 기준서와 caption 규칙을 학습 데이터셋 점검표로 확장합니다.

## 본문에 넣지 않을 것

- 특정 상업 캐릭터를 복제하는 예시
- 특정 작가 화풍을 모사하는 prompt 예시
- 출처가 불명확한 character reference image 묶음
- 웹툰 플랫폼별 업로드 규격이나 수익화 전략
- custom node 설치법을 길게 따라 하는 절차
- 저작권 판단을 단정하는 법률 조언

## 출처와 참고 자료

- Ruiz et al., [DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Hugging Face, [DreamBooth training](https://huggingface.co/docs/diffusers/training/dreambooth){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Hugging Face, [LoRA training](https://huggingface.co/docs/diffusers/training/lora){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Ye et al., [IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models](https://arxiv.org/abs/2308.06721){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Hugging Face, [IP-Adapter guide](https://huggingface.co/docs/diffusers/en/using-diffusers/ip_adapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- h94, [IP-Adapter model card](https://huggingface.co/h94/IP-Adapter){: target="_blank" rel="noopener noreferrer" }, Apache-2.0 표기 확인일: 2026-08-01.
- comfyorg, [comfyui-ipadapter GitHub 저장소](https://github.com/comfyorg/comfyui-ipadapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Zhang et al., [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- lllyasviel, [ControlNet GitHub 저장소](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- comfyanonymous, [ComfyUI ControlNet examples](https://comfyanonymous.github.io/ComfyUI_examples/controlnet/){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- TencentARC, [T2I-Adapter GitHub 저장소](https://github.com/TencentARC/T2I-Adapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Comfy-Org, [Workflow - ComfyUI](https://docs.comfy.org/development/core-concepts/workflow){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Comfy-Org, [Workflow Templates - ComfyUI](https://docs.comfy.org/interface/features/template){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Hugging Face, [Stable Diffusion XL guide](https://huggingface.co/docs/diffusers/en/using-diffusers/sdxl){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- Hugging Face, [Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- xinsir, [controlnet-openpose-sdxl-1.0 model card](https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0){: target="_blank" rel="noopener noreferrer" }, Apache-2.0 표기 확인일: 2026-08-01.
- Guo et al., [AnimateDiff GitHub 저장소](https://github.com/guoyww/AnimateDiff){: target="_blank" rel="noopener noreferrer" }, Apache-2.0 코드 라이선스와 motion adapter, SparseCtrl 설명 확인일: 2026-08-01.
- Hugging Face, [AnimateDiff API](https://huggingface.co/docs/diffusers/api/pipelines/animatediff){: target="_blank" rel="noopener noreferrer" }, video-to-video ControlNet과 프레임별 OpenPose conditioning 예시 확인일: 2026-08-01.
- Zhang et al., [MimicMotion GitHub 저장소](https://github.com/tencent/MimicMotion){: target="_blank" rel="noopener noreferrer" }, Apache-2.0 코드 라이선스, pose guidance, 72-frame 576 x 1024 설정, VRAM 안내 확인일: 2026-08-01.
- Tencent, [MimicMotion model card](https://huggingface.co/tencent/MimicMotion){: target="_blank" rel="noopener noreferrer" }, 가중치가 SVD 기반 fine-tuning이며 LICENSE·NOTICE를 함께 확인해야 한다는 고지 확인일: 2026-08-01.
- Stability AI, [Stable Video Diffusion 1.1 model card](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt-1-1){: target="_blank" rel="noopener noreferrer" }, Community License의 연구·비상업·조건부 상업 사용 범위, 접근 동의와 고지 조건 확인일: 2026-08-01.
- Xu et al., [MagicAnimate GitHub 저장소](https://github.com/magic-research/magic-animate){: target="_blank" rel="noopener noreferrer" }, BSD-3-Clause 코드, 기준 이미지·구동 영상 입력과 공식 가중치 구조 확인일: 2026-08-01.
- zcxu-eric, [MagicAnimate model card](https://huggingface.co/zcxu-eric/MagicAnimate){: target="_blank" rel="noopener noreferrer" }, BSD-3-Clause 전용 가중치와 파일 크기 확인일: 2026-08-01.
- runwayml, [Stable Diffusion v1.5 model card](https://huggingface.co/runwayml/stable-diffusion-v1-5){: target="_blank" rel="noopener noreferrer" }, CreativeML OpenRAIL-M 표기 확인일: 2026-08-01.
- Stability AI, [MSE-finetuned VAE model card](https://huggingface.co/stabilityai/sd-vae-ft-mse){: target="_blank" rel="noopener noreferrer" }, MIT 표기 확인일: 2026-08-01.
- Blender Foundation, [Grease Pencil animation introduction](https://docs.blender.org/manual/en/2.93/grease_pencil/animation/introduction.html){: target="_blank" rel="noopener noreferrer" }, armature와 2D stroke animation 연결 확인일: 2026-08-01.
- OpenToonz, [Plastic tool animation documentation](https://opentoonz.readthedocs.io/en/latest/create_animations_using_plastic_tool.html){: target="_blank" rel="noopener noreferrer" }, skeleton과 mesh 기반 cutout animation 확인일: 2026-08-01.
- Tong et al., [MusePose GitHub 저장소](https://github.com/TMElyralab/MusePose){: target="_blank" rel="noopener noreferrer" }, 코드 MIT와 모델·테스트 데이터 비상업 연구용 제한 확인일: 2026-08-01.
- Hu et al., [Animate Anyone GitHub 저장소](https://github.com/HumanAIGC/AnimateAnyone){: target="_blank" rel="noopener noreferrer" }, Apache-2.0 코드 라이선스 확인일: 2026-08-01.
- Tongyi Lab, [Wan-Animate 프로젝트 페이지](https://humanaigc.github.io/wan-animate/){: target="_blank" rel="noopener noreferrer" }, 기준 이미지·구동 영상·skeleton·얼굴 특징 분리와 학술 연구 전용 고지 확인일: 2026-08-01.
- Fannovel16, [ComfyUI Frame Interpolation GitHub 저장소](https://github.com/Fannovel16/ComfyUI-Frame-Interpolation){: target="_blank" rel="noopener noreferrer" }, MIT 코드 라이선스와 RIFE/FILM 등 보간 노드 목록 확인일: 2026-08-01.
- comfyanonymous, [ComfyUI_examples GitHub 저장소](https://github.com/comfyanonymous/ComfyUI_examples){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- kohya-ss, [sd-scripts GitHub 저장소](https://github.com/kohya-ss/sd-scripts){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
