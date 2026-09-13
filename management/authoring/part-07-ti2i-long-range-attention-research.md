# TI2I와 장거리 이미지 일관성 탐색

- 조사일: 2026-09-11
- 목적: 텍스트·참조 이미지 입력으로 새 장면을 생성하면서 컷 사이의 attention 또는 시각 문맥을 유지하는 방법 탐색.
- 조건: 로컬 8GB VRAM 실험 가능성을 별도로 평가한다. 이번 조사는 생성 실행을 포함하지 않는다.

## 선정 기준

1. 외부 참조 이미지 또는 이전 이미지·설명을 실제 입력으로 받는가?
2. 새 장면 생성 중 참조 특징이나 시퀀스 문맥을 attention에 사용하는가?
3. 같은 원본을 낮은 denoise로 반복 보강하는 것 이상의 연속 장면 예제가 있는가?
4. 공개 코드·가중치와 메모리 조건을 확인할 수 있는가?

‘같은 참조를 매번 입력’하는 구조와 ‘이전 컷의 문맥을 누적’하는 구조를 구분한다. 두 구조 모두 일관성에 도움을 줄 수 있지만 장거리 기억을 구현하는 위치가 다르다.

## 직접 부합하는 후보

| 후보 | 이미지·텍스트 입력 | 연결 구조 | 코드와 실행 판단 |
| --- | --- | --- | --- |
| StoryDiffusion + PhotoMaker | 얼굴 참조 이미지와 장면별 프롬프트 | PhotoMaker로 인물을 조건화하고 CSA의 기준 특징을 후속 컷에서 재사용 | 공식 Gradio 코드에 두 기능 결합 확인. 기본 low-memory 안내는 20GB 초과 예상이며 8GB 미검증 |
| StoryGen / Intelligent Grimm | 현재 프롬프트와 이전 이미지·캡션 쌍 | 학습된 vision-language context module을 통해 자기회귀적 이미지 생성 | 공식 코드·체크포인트 링크 있음. SD 1.5 기반, 공개 추론은 512×512. 8GB 실측은 미확인 |
| StoryTailor | 장문 이야기, 인물별 참조 이미지, grounding box | Gaussian-Centered Attention과 Selective Forgetting Cache로 인물 및 배경 문맥 연결 | 프로젝트는 RTX 4090 24GB 실행 명시. 코드 링크는 있으나 이번에 실행 구현 전체는 미검토 |
| SEED-Story | 이야기 시작 이미지와 텍스트 | MLLM의 이미지·텍스트 시퀀스 문맥과 multimodal attention sink, SDXL 기반 이미지 복원 | 공식 코드·가중치 공개. SDXL·Llama-2-7B·시각 인코더 등 복합 구성. 8GB 우선 후보로 삼기 어려움 |

### StoryDiffusion 참조 이미지 경로

공식 `gradio_app_sdxl_specific_id_low_vram.py`는 `Using Ref Images`를 `Photomaker`로 전환하고 `input_id_images`를 입력한다. 동시에 U-Net에 `set_attention_processor`를 적용하며, 기준 생성의 `write=True`와 후속 생성의 `write=False`가 유지된다. 따라서 ‘TI2I 조건 + 컷 간 self-attention 공유’를 확인하기에 가장 명확한 기준 구현이다. 얼굴 참조를 사용한다고 착장·신발까지 정확히 이식된다고 보지는 않는다.

출처: HVision-NKU, [공식 참조 이미지 실행 코드](https://github.com/HVision-NKU/StoryDiffusion/blob/main/gradio_app_sdxl_specific_id_low_vram.py), [공식 메모리 안내](https://github.com/HVision-NKU/StoryDiffusion#how-to-use), 2026-09-11 확인.

### StoryGen의 입력 계약

공식 `inference.py`에는 `ref_image`, `ref_prompt`, `image_guidance_scale`와 `auto-regressive`·`multi-image-condition` 모드가 있다. 파이프라인에 이미지와 이전 설명을 함께 넘기며 공개 예제의 출력 크기는 512×512다. SD 1.5 기반이라는 점은 8GB 적합성을 조사할 이유지만 성공 근거는 아니다. 전용 학습 체크포인트를 사용해야 하며 일반 SD 1.5 img2img로 대체할 수 없다.

실행 준비 시 오래된 diffusers·xformers 의존성과 예제의 로컬 체크포인트 경로를 점검해야 한다. 기본 샘플 수는 10이므로 최초 메모리 측정은 1로 제한하는 자체 시험이 적절하다. 이 조정의 결과·성공률은 아직 없다.

출처: Haoning Wu 외, [StoryGen 논문](https://arxiv.org/abs/2306.00973), [공식 저장소](https://github.com/haoningwu3639/StoryGen), [추론 코드](https://github.com/haoningwu3639/StoryGen/blob/master/inference.py), 2026-09-11 확인.

### 장문 시퀀스 확장 후보

StoryTailor는 텍스트·인물 참조·공간 조건을 받으므로 요청한 형태에 직접 부합한다. 다만 24GB 결과를 8GB로 환산하지 않는다. SEED-Story는 초기 이미지와 텍스트에서 최대 25개 멀티모달 시퀀스를 생성한다고 설명하며, 이미지 생성기의 CSA 대신 MLLM 문맥 유지가 중심이다.

출처: Jinghao Hu 외, [StoryTailor 공식 프로젝트](https://jinghaos-research.github.io/StoryTailor.io/), TencentARC, [SEED-Story 공식 구현](https://github.com/TencentARC/SEED-Story), 2026-09-11 확인.

## 유사하지만 별도로 분류할 후보

- **AnyStory**: 참조 이미지·마스크와 텍스트를 받는 개인화 생성 및 storyboard 코드가 있다. 공개 버전은 FLUX.1-dev와 Redux, 전용 가중치를 사용한다. storyboard 인터페이스만으로 컷 사이의 장거리 cache가 있다고 판정하지 않는다. [공식 코드](https://github.com/junjiehe96/AnyStory).
- **Story-Iter**: 이전 라운드의 생성 이미지 전체를 GRCA로 재사용한다. 임의의 외부 참조 이미지로 시작하는 TI2I 인터페이스와는 구분한다. [공식 코드](https://github.com/UCSC-VLAA/story-iter).
- **CharaConsist**: 단일 identity 이미지의 특징으로 일관성 생성하는 관련 연구다. ‘단일 기준 이미지’가 임의 외부 PNG를 즉시 입력할 수 있다는 뜻인지, 기준 생성의 중간 특징이 필요한지는 추가 코드 확인 전 단정하지 않는다. [공식 코드](https://github.com/Murray-Wang/CharaConsist).
- **DreamStory**: 논문은 MMSA·MMCA로 참조 이미지와 텍스트의 일관성을 제어한다. 이번 조회에서 논문에 기재된 프로젝트 URL은 404였으므로 실행 후보로 확정하지 않는다. [논문](https://arxiv.org/abs/2407.12899).

위 자료는 모두 2026-09-11 확인. 코드 공개 여부와 별도로 이미지·모델별 배포 조건은 실제 자산 채택 전에 확인한다.

## 실험 우선순위

- **요청한 attention 구조를 명확히 보여줄 기준:** StoryDiffusion + PhotoMaker.
- **8GB에서 먼저 실행 적합성을 점검할 추가 후보:** StoryGen. SD 1.5·512px 구조에 근거한 우선순위이며 VRAM 실측에 근거한 보장은 아니다.
- **장거리 배경 문맥까지 비교할 후속 연구:** StoryTailor, SEED-Story.

검증은 기준 이미지 하나와 서로 다른 장면 프롬프트를 사용해 진행한다. 입력 보존, 새 동작·구도 반영, 컷 수 증가에 따른 drift, 참조/문맥을 끈 대조군을 각각 기록한다. 첫 출력 성공과 장거리 일관성 목표 달성을 따로 판정한다.

## 캐릭터 일관성 중심의 추가 조사

2026-09-11 사용자 지시에 따라 attention 구조 자체보다 ‘같은 캐릭터의 포즈·카메라·배경 변경’을 중심으로 재평가했다. 아래는 실험 우선순위이며 품질 순위나 로컬 실행 성공 기록이 아니다.

| 방식·후보 | 유지하는 기준 | 확인된 실행 근거 | 검토 결론 |
| --- | --- | --- | --- |
| 참조 기반: DreamO v1.1 | IP는 인물·복장을 포함한 참조, ID는 얼굴 중심 참조 | 공식 README와 app.py는 Nunchaku+offload 약 6.5GB 및 8GB 지원 안내 | 준비된 캐릭터를 다른 장면으로 옮기는 첫 후보. IP부터 비교 |
| 참조 기반: InstantCharacter | 한 장의 subject image와 전용 adapter | FLUX.1-dev, SigLIP·DINOv2 인코더 사용. 공식 offload 안내는 22GB 미만 | 캐릭터 전용 방법의 비교 자료. 8GB 우선 후보로 확정하지 않음 |
| 특징 공유: CharaConsist | 첫 프롬프트로 만든 ID 이미지와 중간 특징 | 공식 표는 sequential offload `init_mode=3`에서 3GB 안내 | 새 캐릭터를 먼저 만든 뒤 이어 생성하는 방식의 첫 후보 |
| 전용 학습: DreamBooth LoRA | 여러 캐릭터 이미지에서 학습한 추가 가중치 | 공식 학습 코드와 메모리 절감 방법 존재 | 참조 세트가 확보된 뒤 비교. 8GB 학습 성공은 베이스·해상도·설정별 검증 필요 |

DreamO의 6.5GB는 제작자 측 코드 설명이며 이번 장비에서 실측한 값이 아니다. 코드 주석의 예시는 RTX 3080 10GB다. README의 일부 실행 문구는 `--nunchaku`를 사용하지만 현재 `app.py` parser는 `--quant nunchaku --offload`를 받는다. 설치 시 README 문장만 복사하지 않고 실제 CLI와 Nunchaku·CUDA 버전을 확인한다. 이 모델의 inference cache를 장거리 캐릭터 기억으로 해석하지 않는다.

CharaConsist는 추가 확인으로 앞선 불확실성을 좁혔다. 공식 `inference.py`는 첫 프롬프트를 `id_prompt`로 분리하고 `is_id=True`로 기준 이미지·특징을 생성한 뒤 후속 프롬프트에 `spatial_kwargs`를 전달한다. 공개 경로는 임의 외부 캐릭터 PNG 입력 방식이 아니다. 3GB 안내는 VRAM 수치이며 FLUX.1-dev 가중치·시스템 RAM·offload 시간까지 작다는 뜻은 아니다.

학습 비교에서는 DreamBooth가 과적합과 학습 설정에 민감하다는 공식 안내를 반영한다. 기존 그림의 캐릭터와 함께 배경·포즈까지 외워 버렸는지 확인하려면 학습에 쓰지 않은 방향·장소를 평가해야 한다. 합성 이미지가 여러 장이라는 이유만으로 올바른 캐릭터 학습 세트가 완성됐다고 보지 않는다.

비교 실험은 같은 캐릭터 기준으로 정면·3/4·측면, 앉기·걷기·팔 들기, 실내·야외를 포함한다. 얼굴뿐 아니라 헤어 실루엣, 체형, 재킷 길이, 바지 폭, 신발과 화풍을 별도 평가한다. 장면을 바꾸지 못하고 기준 그림을 복제하는 결과는 높은 일관성 점수만으로 성공 처리하지 않는다. 단일 참조 방법은 같은 원본을 재사용하는 조건과 이전 출력을 다시 넣는 조건을 분리한다.

출처(2026-09-11 확인):

- ByteDance, [DreamO README](https://github.com/bytedance/DreamO), [app.py 입력·메모리·CLI](https://github.com/bytedance/DreamO/blob/main/app.py).
- Tencent-Hunyuan, [InstantCharacter 공식 코드·offload 안내](https://github.com/Tencent-Hunyuan/InstantCharacter).
- Murray-Wang, [CharaConsist 메모리 표](https://github.com/Murray-Wang/CharaConsist), [기준·후속 생성 코드](https://github.com/Murray-Wang/CharaConsist/blob/main/inference.py).
- Hugging Face, [DreamBooth 학습 안내](https://huggingface.co/docs/diffusers/training/dreambooth), [LoRA 학습 안내](https://huggingface.co/docs/diffusers/training/lora).

현재 제안: 준비된 캐릭터를 유지하는 실험은 DreamO IP 모드와 기존 Qwen 편집 경로를 비교하고, 새 캐릭터의 컷 간 특징 공유는 CharaConsist를 별도 비교한다. 캐릭터 LoRA는 충분한 기준 이미지가 마련된 뒤 세 번째 방식으로 추가한다. 이번에는 코드·문서 탐색만 수행했다.
