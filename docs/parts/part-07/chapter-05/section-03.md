# P7-5.3 스토리보드 생성: 스토리보드에서 구조 guide 추출하기

> Section ID: `P7-5.3`
> Version: `v2026.08.06`

스토리보드는 **텍스트만으로** 먼저 만듭니다. 이전 장면, 배경, 인물 사진을 스토리보드 모델의 입력으로 넣지 않습니다. 사람이 읽을 수 있는 스토리보드만 통과시키고, 그 PNG에서 lineart·canny·상대 depth를 추출합니다. 따라서 guide는 장면을 새로 해석하는 시작점이 아니라, 이미 검수한 한 장면의 구조를 다음 생성에 전달하는 파생 산출물입니다.

## 먼저 한 장면 스토리보드를 사람 검수한다

이 실험의 고정 장면은 기암절벽 사이의 현대무용자입니다. 무용수는 양옆과 뒤쪽의 먼 절벽에서 떨어진 열린 평지에 서고, 검정 민소매 레오타드와 불투명 타이즈를 입은 채 한쪽 다리는 위로 길게 들며 다른 다리는 바닥을 지지하고, 한쪽 팔은 위로, 다른 팔은 옆으로 뻗습니다. 치마나 흩날리는 천은 다리·무릎·발의 연결을 가리므로 이 장면에 넣지 않습니다. 지지발은 발 전체와 밑창의 접지면이 보이고, 주변 바위와 외곽선이 붙거나 겹치지 않아야 합니다. 참조 사진에서 읽은 자세를 문장으로만 풀어 썼을 뿐, 사진 파일은 입력하지 않았습니다.

스토리보드에서는 인물의 이름·얼굴·의상보다 아래 구조가 읽히는지를 봅니다.

| 확인할 정보 | 이 장면에서 확인할 기준 |
| --- | --- |
| 인체 | 머리, 두 팔, 두 다리와 큰 동작 실루엣 |
| 행동 | 위로 든 다리와 바닥을 딛는 다리의 대비 |
| 공간 | 열린 평지의 인물과 양옆·뒤쪽 먼 기암절벽의 앞뒤 관계 |
| 경계 | 인물 윤곽, 절벽 통로, 바닥의 강한 경계 |
| 접지 | 지지발 전체·밑창·바닥 그림자가 읽히고, 발 외곽이 바위나 지형과 겹치지 않음 |

## 승인한 스토리보드의 입력 계약

승인한 경로는 Animagine XL 4.0 하나입니다. 태그형 prompt, `832 x 1216`, 28 step, CFG 5.0을 고정하고 텍스트만 입력합니다. 이 값은 한 장면·한 seed의 검수에서 정한 실행 계약이며, 모델 전체의 일반적인 우열을 뜻하지 않습니다.

| 고정 모델 | 적용한 계약 | 검수 결과 |
| --- | --- | --- |
| Animagine XL 4.0 | 태그형 prompt, 832 x 1216, 28 step, CFG 5.0, seed 5413 | 두 팔·두 다리, 큰 동작, 기암절벽이 함께 읽혀 사람 검수를 통과한 승인 스토리보드 |

다른 모델의 비교·미통과 판단은 이 절의 릴리즈노트에 실험 이력으로만 남기고, 실행 코드의 선택지로는 제공하지 않습니다.

아래 [로컬 GPU 실험 코드](../../../assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py)는 승인한 Animagine 계약만 사용합니다. 프롬프트는 소스 안에 고정되어 있고, 실행할 때마다 타임스탬프가 든 `storyboard`, `lineart`, `canny`, `depth` PNG를 저장합니다. `--runs`를 주면 모델은 한 번만 불러오고 seed를 1씩 늘려 여러 후보를 만든다. 후보는 각각 사람 검수한 뒤에만 승인 자산으로 옮긴다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py --seed 5411
# seed 5411, 5412, 5413으로 후보 세 장을 생성한다.
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py --seed 5411 --runs 3
```

### 승인 스토리보드와 파생 guide를 함께 비교한다

아래 네 장은 같은 승인 스토리보드에서 나온 한 세트다. 원본을 먼저 보고, 같은 장면에서 윤곽·강한 경계·상대 거리가 각각 얼마나 남는지 오른쪽과 다음 행에서 비교한다. 이 표의 guide PNG는 다음 생성에 쓰기 전에도 각각 사람 검수해야 한다.

| 원본과 전체 윤곽 | 강한 경계와 상대 거리 |
| --- | --- |
| **승인 스토리보드**<br>![승인한 텍스트 전용 현대무용·기암절벽 스토리보드](../../../assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-storyboard.png)<br>텍스트만으로 생성한 `seed=5413` 원본 | **lineart guide**<br>![스토리보드에서 추출한 lineart guide](../../../assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-lineart.png)<br>인물과 절벽의 전체 윤곽 |
| **Canny guide**<br>![스토리보드에서 추출한 Canny guide](../../../assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-canny.png)<br>강한 경계와 동작 실루엣 | **상대 depth guide**<br>![스토리보드에서 실제 추정한 상대 depth guide](../../../assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-depth.png)<br>인물·바닥·절벽의 앞뒤 관계 |

lineart는 전체 윤곽, canny는 강한 경계, depth는 상대적인 거리만 담습니다. 세 guide는 스토리보드의 오류까지 함께 보존할 수 있으므로, 추출 뒤에도 한 번 더 확인해야 합니다. 특히 지지발·바닥 그림자와 주변 지형이 붙거나 겹치면 guide를 만들지 않고, 텍스트 스토리보드 단계로 되돌아가 접지면과 지형 배치를 다시 생성합니다.

## guide마다 보존하는 구조가 다르다

[구조 guide 웹툰 생성 코드](../../../assets/part-07/chapter-05/p7_5_3_structural_guided_webtoon.py)는 스토리보드 RGB를 초기 이미지로 쓰지 않습니다. seed 노이즈에서 시작하는 text-to-image ControlNet에 검수한 depth·Canny·lineart PNG를 하나 또는 둘만 전달합니다. 이 비교 단계의 기본 prompt는 `full body dancer`로 최소화한다. 그러므로 결과 차이의 우선 관찰 대상은 장면 묘사의 풍부함이 아니라 guide가 인물 윤곽, 발과 지면의 분리, 절벽의 상대 위치를 얼마나 유지하는가이다.

기본값은 소형 SDXL Canny의 `768 x 1152`, 28 step, Canny `0.50`이며, `--guide`와 `--seed`만 주면 이 계약으로 실행됩니다. `--backbone sd15`를 고르면 기본값은 `512 x 768`, 24 step, depth `0.65`로 바뀝니다. `--backbone flux1-dev`는 InstantX Flux.1-dev Canny·depth ControlNet을 받을 비교 후보이며, 비상업 조건을 확인했다는 뜻의 `--allow-restricted-license`가 있어야 실행된다. `qwen-image`와 `z-image-turbo`는 각각 Union ControlNet의 단일 guide 계약과 권장 step·CFG·scale을 사용한다. 모든 실행은 PNG 옆에 seed, guide 종류·강도, 해상도, step, VRAM peak, 생성 시간, 사람 검수 항목을 담은 JSON 기록을 남긴다. 아직 로컬에 없는 가중치를 내려받거나 GPU 실행을 완료했다는 뜻은 아니다.

| backbone | 구조 입력 계약 | 기본 비교 설정 | 8 GB 판정 상태 |
| --- | --- | --- | --- |
| `sd15` | Canny·depth·lineart, 두 guide 가능 | `512 x 768`, 24 step | 기존 실행 경로 있음 |
| `sdxl` | Canny·depth, 두 guide 가능 | `768 x 1152`, 28 step | CPU offload 전제 |
| `flux1-dev` | Canny·depth, 두 guide 가능 | `1024²`, 28 step, CFG 3.5 | 비상업 비교·미검수 |
| `qwen-image` | Union Canny·depth·soft-edge(선화), 한 guide | `1024²`, 30 step, true CFG 4.0 | 20B라 제외 후보 |
| `z-image-turbo` | Union Canny·depth·HED(선화), 한 guide | `1024²`, 9 step, CFG 0 | 8 GB 미검수 |

### Flux.1 구조 제어와 Flux.2 다중 참조를 구분한다

Flux 계열을 한 모델의 기능처럼 섞지 않습니다. `flux1-dev`는 Canny·depth를 구조 조건으로 넣는 이 절의 ControlNet 후보입니다. 반면 이 저장소에서 P7-5.1·P7-5.2에 사용한 Flux.2 Klein은 `image=`에 한 장 또는 여러 장의 참조 이미지를 직접 넣는 이미지 편집·다중 참조 경로입니다. 현 Diffusers에는 Flux.1용 `FluxControlNetPipeline`은 있지만 Flux.2용 ControlNet pipeline은 없으므로, Flux.2를 Canny/depth 전용 `BACKBONE_DEFAULTS`에 넣지 않습니다.

| 계열 | 이 장면에서 검토할 입력 | 현재 판단 |
| --- | --- | --- |
| Flux.1-dev | Canny 또는 depth guide와 text | `flux1-dev` 정적 후보로 추가. 가중치·8 GB 실행 성립·품질은 미검수 |
| Flux.2 Klein | 승인한 캐릭터·화풍·장소 참조 이미지 한 장 또는 여러 장과 text | 다중 참조 편집 후보. 스토리보드 RGB를 넣지 않는 현재 P7-5.3 ControlNet 실험과는 입력 계약이 달라 별도 비교로 분리 |

```bash
python docs/assets/part-07/chapter-05/p7_5_3_structural_guided_webtoon.py \
  --guide docs/assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-canny.png \
  --seed 5411
python docs/assets/part-07/chapter-05/p7_5_3_structural_guided_webtoon.py \
  --backbone sdxl --guide docs/assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-canny.png \
  --guide-kind canny --seed 5411 --scale 0.50 --steps 28 --width 768 --height 1152
python docs/assets/part-07/chapter-05/p7_5_3_structural_guided_webtoon.py \
  --guide docs/assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-canny.png \
  --guide-kind canny --seed 5411 --scale 0.65
python docs/assets/part-07/chapter-05/p7_5_3_structural_guided_webtoon.py \
  --guide docs/assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-canny.png \
  --guide-kind canny --scale 0.65 \
  --second-guide docs/assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-depth.png \
  --second-guide-kind depth --second-scale 0.35 --seed 5411
python docs/assets/part-07/chapter-05/p7_5_3_structural_guided_webtoon.py \
  --guide docs/assets/part-07/chapter-05/p7-5-3-20260806-233009-animagine-run-03-seed-5413-depth.png \
  --guide-kind depth --seed 5411 --scale 0.0
```

이전 guide 조건 웹툰 후보는 승인 자산이 아니므로 저장소에서 제거했습니다. 위 명령으로 새 컷을 만들 때마다 행동·인체·공간 관계와 화풍을 다시 사람 검수해야 하며, 얼굴 일관성·섬세한 손·최종 화풍 승인은 별도 단계에서 판단합니다.

## 출처와 참고 자료

- Hugging Face Diffusers는 ControlNet이 text prompt에 Canny·depth 같은 구조 제어를 더하고, 제어 강도를 별도로 조절하는 방식을 설명합니다. [ControlNet 문서](https://huggingface.co/docs/diffusers/using-diffusers/controlnet){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- Depth Anything V2 Small은 단일 이미지에서 상대 깊이를 추정하는 경량 모델입니다. 이 실험은 Transformers 호환 checkpoint를 `.tmp/`에 내려받아 사용했습니다. [Depth Anything V2 Small 모델 카드](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- Animagine XL 4.0 모델 카드는 태그형 caption, `masterpiece`·점수 태그, CFG 5와 28 step의 예시를 제시합니다. [Animagine XL 4.0 모델 카드](https://huggingface.co/cagliostrolab/animagine-xl-4.0){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- depth 조건 모델은 SD 1.5와 함께 쓰도록 변환된 ControlNet v1.1 checkpoint입니다. [ControlNet depth 모델 카드](https://huggingface.co/lllyasviel/control_v11f1p_sd15_depth){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- lineart 조건 모델은 SD 1.5와 함께 쓰는 ControlNet v1.1 checkpoint이며 Diffusers 사용 예시를 제공합니다. [ControlNet lineart 모델 카드](https://huggingface.co/lllyasviel/control_v11p_sd15_lineart){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- 소형 SDXL Canny ControlNet은 SDXL Base 1.0용으로 학습된 원본보다 7배 작은 실험적 checkpoint입니다. 모델 카드는 Canny 조건 강도 0.5와 CPU offload 예시를 제시하며, 복잡한 조건에서는 큰 checkpoint가 더 나을 수 있다고 설명합니다. [소형 SDXL Canny ControlNet 모델 카드](https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0-small){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- Diffusers는 Flux.1의 `FluxControlNetPipeline`에서 InstantX의 Canny·depth·Union ControlNet과 XLabs의 Canny·depth·HED ControlNet을 지원한다고 안내합니다. 이 절은 공식 예시의 InstantX Flux.1-dev Canny 설정만 정적 후보로 추가했으며, 아직 실행 결과를 주장하지 않습니다. [Flux.1 ControlNet 문서](https://huggingface.co/docs/diffusers/api/pipelines/controlnet_flux){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- Flux.2 Klein은 이미지 한 장 또는 여러 장을 `image=`로 받는 이미지 조건 경로를 제공하며, Hugging Face는 최대 10장의 다중 참조를 설명합니다. 이 문서에서는 Flux.1 ControlNet과 기능을 혼동하지 않도록 별도 후보로만 기록합니다. [Flux.2 문서](https://huggingface.co/docs/diffusers/api/pipelines/flux2){: target="_blank" rel="noopener noreferrer"}, [Flux.2 다중 참조 안내](https://huggingface.co/blog/flux-2){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- Qwen-Image Union ControlNet은 Canny·soft edge·depth·pose를 하나의 구조 조건 모델로 받으며, 공식 예시는 30 step·true CFG 4.0·control scale 1.0을 사용합니다. Qwen-Image 본체는 20B이므로 이 절의 8 GB 기본 후보로 채택하지 않고 입력 계약 비교에만 둡니다. [Qwen-Image ControlNet 문서](https://huggingface.co/docs/diffusers/api/pipelines/qwenimage){: target="_blank" rel="noopener noreferrer"}, [Qwen-Image 모델 카드](https://huggingface.co/Qwen/Qwen-Image){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- Z-Image Turbo Union ControlNet은 Canny·HED·depth·pose·MLSD를 지원하며, Diffusers 예시는 9 step·CFG 0·control scale 0.75를 사용합니다. 공식 본체 안내는 16 GB 소비자 GPU 기준이므로 8 GB 실행 가능 여부는 실제 측정 전까지 미검수다. [Z-Image ControlNet 문서](https://huggingface.co/docs/diffusers/api/pipelines/z_image){: target="_blank" rel="noopener noreferrer"}, [Z-Image Turbo 모델 카드](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)
- 후속 컷신에서는 SD 계열의 IP-Adapter 참조 입력과 ControlNet 구조 입력을 함께 쓸 수 있다. 다만 참조는 인물·화풍, ControlNet은 포즈·접지·구도처럼 역할을 분리하고 각각의 강도를 한 번에 하나씩 바꿔 검수한다. [IP-Adapter와 ControlNet 결합 문서](https://huggingface.co/docs/diffusers/using-diffusers/ip_adapter){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-06)

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 스토리보드 | 행동·인체·거리 관계와 지지발의 윤곽·접지면이 먼저 읽히는가? |
| 입력 계약 | 승인 모델의 prompt 형식·해상도·step·guidance를 맞췄는가? |
| lineart·canny | 필요한 윤곽·경계만 남기고 잡음까지 고정하지 않았는가? |
| 구조 guide | depth·Canny·lineart 중 이 장면에서 실제로 필요한 구조를 더 잘 보존한 것은 무엇인가? |
| 채택 | 스토리보드와 모든 guide를 사람 검수한 뒤에만 다음 생성 입력으로 넘겼는가? |
