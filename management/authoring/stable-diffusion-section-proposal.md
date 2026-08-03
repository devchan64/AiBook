# Stable Diffusion 설명 Section 제안 노트

작성일: 2026-08-03

## 판단 요약

Stable Diffusion은 생성형 AI를 설명하는 대표 사례로 적합하다. 텍스트 생성의 `다음 토큰 예측`만으로 생성형 AI 전체를 이해하는 오해를 줄이고, 이미지 생성에서는 `조건부 점진 복원`과 `잠재 표현`이 중요하다는 점을 구체적으로 보여 줄 수 있기 때문이다.

다만 현재 원고에는 디퓨전 모델의 입문 직관과 Stable Diffusion 기반 실습이 이미 있다. 새 원고의 목적은 모델 이름이나 이미지 제작 기법을 더 나열하는 일이 아니라, 두 층위를 연결하는 **Stable Diffusion의 최소 계산 구조**를 독자가 설명할 수 있게 하는 데 둔다. Part 7은 현재 수정 중이므로, 이 노트에서는 Part 7의 제목·순서·본문을 바꾸는 제안을 하지 않고 나중에 이론과 실습을 연결할 때의 참고 지점으로만 둔다.

## 현재 원고에서 이미 맡는 역할

| 위치 | 현재 역할 | 남는 공백 |
| --- | --- | --- |
| `P1-10.2` | 텍스트의 다음 토큰 생성과 이미지의 디퓨전 복원을 구분한다. DDPM의 역과정과 latent diffusion의 조건부 복원 직관을 소개한다. | Stable Diffusion이라는 실제 시스템이 어떤 부품을 거쳐 이미지를 만드는지는 설명하지 않는다. |
| `P5-15.1`~`P5-15.3` | 생성물 중심 출력, 후보 분포, 샘플링 선택을 Part 6 전의 딥러닝 준비 관점으로 설명한다. | 텍스트 후보 분포 중심의 설명이므로 이미지 디퓨전의 반복 복원과 직접 연결되지는 않는다. |
| `P6-1.1`~`P6-1.3` | 생성형 AI를 LLM 중심 사례로 읽는 이유와 후보 생성·선택의 반복을 설명한다. | Part 6의 중심축은 LLM이며, 이미지 생성 모델의 구조를 본편으로 확장하기에는 경계가 다르다. |
| `P7-5.1`~`P7-5.3` | SD 1.5, LoRA, StoryDiffusion, 직접 LoRA 학습을 조건 고정·비교·실패 기록의 실습 재료로 사용한다. | 향후 이론 Section의 용어를 실습에서 다시 확인할 수 있는 참고 지점이다. 현재 수정 중인 Part 7의 구조나 본문을 이 노트로 변경하지 않는다. |

## 권장 위치와 Section 경계

새 Section은 **Part 5, Chapter 15 뒤에 추가**하는 편이 가장 자연스럽다. Part 5의 생성 모델·샘플링 입구를 이미지 생성 사례로 한 번 구체화하고, Part 6은 기존대로 LLM 중심 본편으로 유지할 수 있다.

- 후보 Section ID: `P5-15.4`
- 제목 후보: `Stable Diffusion은 텍스트 조건에서 이미지를 어떻게 복원하는가`
- 중심 질문: **프롬프트가 들어오면 Stable Diffusion은 어떤 중간 표현과 반복 과정을 거쳐 이미지를 만드는가?**
- 학습 산출물: 독자가 `텍스트 조건 -> 잠재 노이즈 -> 반복적 노이즈 제거 -> 이미지 복원`의 흐름을 말로 설명하고, prompt·seed·step·LoRA·ControlNet이 각각 무엇을 바꾸는지 구분한다.

이 위치는 `P5-15.3`의 샘플링 설명 뒤에 두는 것을 기본안으로 한다. 다만 P5-15가 “Part 6으로 넘어가기 전의 최소 준비”라는 현재 경계를 넘지 않도록, 구현 코드·Web UI 사용법·프롬프트 작성 요령·학습 튜닝은 넣지 않는다.

## 권장 설명 흐름

1. **이미지 생성은 텍스트를 그림으로 번역하는 단일 단계가 아니다.**
   프롬프트는 이미지 전체를 직접 지정하는 정답이 아니라, 복원 과정이 참고할 조건이다.

2. **이미지를 더 작은 잠재 표현으로 다룬다.**
   Stable Diffusion은 이미지 픽셀 공간이 아니라 VAE가 인코딩한 latent space에서 주된 디퓨전 과정을 수행한다. 이 선택은 고해상도 이미지 생성의 계산 부담을 줄이는 설명으로 연결한다.

3. **노이즈에서 시작해 여러 단계로 복원한다.**
   초기 잠재 노이즈에 대해 U-Net이 현재 단계에서 줄일 노이즈를 예측하고, scheduler/sampler가 다음 잠재 상태로 이동시킨다. 이 반복 뒤 VAE decoder가 잠재 표현을 사람이 볼 수 있는 이미지로 바꾼다.

4. **텍스트 조건은 cross-attention으로 복원 과정에 들어간다.**
   text encoder가 프롬프트를 표현으로 바꾸고, U-Net이 복원 과정에서 그 조건을 참고한다. 따라서 프롬프트는 결과를 완전히 고정하지 않고 복원 방향에 영향을 준다.

5. **실습에서 바꾸는 값의 역할을 분리한다.**

| 값 또는 구성요소 | 우선 설명할 역할 | 혼동하지 않을 구분 |
| --- | --- | --- |
| prompt | 텍스트 조건 | 결과를 완전히 결정하는 설계도는 아니다. |
| seed | 초기 노이즈의 출발점 | 품질 점수나 스타일 자체가 아니다. |
| steps / sampler | 반복 복원의 횟수와 이동 규칙 | 모델 자체의 학습 파라미터가 아니다. |
| CFG | 조건을 얼마나 강하게 따르도록 유도할지의 조절값 | 프롬프트 충실도만 높이는 만능 값은 아니다. |
| base model | 학습된 이미지 패턴과 복원 능력의 기반 | LoRA와 같은 작은 추가 가중치와 구분한다. |
| LoRA | base model에 덧붙이는 적은 수의 조정 가중치 | base model 전체를 새로 학습한 결과와 구분한다. |
| ControlNet / IP-Adapter | 텍스트 외의 구조·참조 조건을 더하는 제어 경로 | LoRA의 대상·스타일 적응과 같은 역할로 묶지 않는다. |

6. **향후 Part 7을 읽을 때 참고한다.**
   Part 7의 수정이 마무리된 뒤, base model·LoRA weight·prompt·seed 비교와 여러 조건 신호의 분리가 위 구성요소를 실제로 구분하는 실습인지 대조한다. 이 노트는 그 대조 기준일 뿐, 현재 Part 7에 대한 수정 지시나 작업 목록은 아니다.

## 넣지 않을 내용

- AUTOMATIC1111, ComfyUI, Diffusers의 설치·버튼·노드별 사용법
- 프롬프트 문구를 많이 모은 제작 팁
- 특정 checkpoint의 순위나 현재 서비스 기능 비교
- LoRA 학습 hyperparameter 튜닝 안내
- 저작권·라이선스를 단순한 체크리스트로 처리하는 설명

이 항목들은 기술 변화가 빠르거나 Part 7의 실습·운영 기록 역할과 겹친다. 실습 자산을 채택할 때의 모델 라이선스, 참조 이미지 권리, 배포 조건은 독자용 설명을 과도하게 늘리지 않되 별도의 검토 기록으로 확인한다.

## 자료 기준

- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752): latent space에서의 diffusion과 cross-attention conditioning의 1차 근거.
- Jonathan Ho, Ajay Jain, Pieter Abbeel, [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239): 노이즈 추가 과정과 역방향 denoising의 1차 근거.
- Stability AI, [Stable Diffusion 3 Research Paper](https://stability.ai/news/stable-diffusion-3-research-paper): Stable Diffusion 계열의 최신 세대 설명을 확인할 때 참고하되, 본문 구조 설명의 주 근거는 원 논문과 공식 구현 문서로 유지한다.
- Hugging Face, [Diffusers documentation](https://huggingface.co/docs/diffusers/index): 실행 예제와 현재 구성요소 명칭을 반영할 때 확인한다. 제품·라이브러리 세부는 작성 시점에 다시 검증한다.

## 반영 시 확인할 연결

- `management/authoring/part-05-open-checklist.md`의 Chapter 15 체크포인트에 `P5-15.4` 중심축을 추가한다.
- `docs/table-of-contents.md`, `mkdocs.yml`에 새 Section을 같은 제목과 순서로 반영한다.
- Section 본문 메타데이터, 릴리즈노트, 다국어 대응은 Section 작성 시점의 가이드라인에 따라 함께 관리한다.
- `diffusion model`, `latent space`, `VAE`, `U-Net`, `cross-attention`, `classifier-free guidance`의 개념사전 등재·대표 설명 위치는 실제 원고 범위를 확정한 뒤 별도로 판정한다.
- Part 7은 수정 완료 뒤에만, 이론 Section의 용어와 실습의 입력·조작값·기록 항목이 자연스럽게 대응되는지 참고 수준에서 재검토한다.
