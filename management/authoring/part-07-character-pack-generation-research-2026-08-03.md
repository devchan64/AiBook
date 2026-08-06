# Part 7: 캐릭터팩 생성 수단 조사

확인일: 2026-08-03

## 질문

8 GB GPU 환경에서 웹툰용 캐릭터팩을 어떻게 만들 수 있는가. 여기서 캐릭터팩은 한 장의 정면 인물 이미지가 아니라, 다음 항목을 사람이 같은 revision으로 승인한 원본 묶음이다.

- 전신: front, 좌·우 3/4, side, rear 3/4 또는 rear
- face: front, 좌·우 3/4, side와 기본 표정
- 의상·소품: 앞·옆·뒤에서 색, 위치, strap, flap, 신발 구조가 읽히는 장면
- style: 선 굵기, palette, 명암, 질감의 명시적 계약

이 원본은 이후 LoRA, IP-Adapter, ControlNet, inpaint의 입력과 검수 기준이다. 따라서 생성 결과가 예쁘다는 것과 character pack 승인은 다르다.

## 조사 결과

| 후보 | 해결하려는 문제 | 8 GB와 웹툰팩의 적합성 | 판정 |
| --- | --- | --- | --- |
| FLUX.2 direct reference conditioning | 한 장 master의 얼굴·색·화풍을 다음 컷에 전달 | 현재 실험에서 identity 일부는 유지했지만 side/3-4 camera와 가방 위치가 무너짐 | **불합격. pack 생성기가 아님** |
| SDXL IP-Adapter / Face IP-Adapter | 얼굴 또는 style reference를 T2I에 추가 | 여러 reference와 face adapter를 더해도 현재 P7-5.3에서 face·bag geometry를 고정하지 못함 | **불합격. 완성 팩의 소비자 후보일 뿐** |
| MV-Adapter | text/image에서 동시에 multi-view 생성 | 공식 구현이 image-to-multiview에 약 14 GB GPU memory를 제시함. 8 GB 조건 밖이며 object/3D view 중심의 산출물을 웹툰 face sheet로 바로 승인할 근거도 없음 | **현재 장비 제외** |
| SyncDreamer | single-view에서 동시 multi-view 생성 | 공식 제한 모드는 10 GB 미만이라고만 제시한다. 8 GB 통과는 보장되지 않고, multiple seed 선택을 권한다. single-view 3D reconstruction 성격이라 stylized human face·의상 sheet의 품질을 가정할 수 없음 | **조사 보류** |
| Zero123++ | 단일 이미지에서 정규화된 multi-view 생성 | 3D generation 목적이고 고정 elevation/output view를 만든다. weights는 CC-BY-NC 4.0이므로 공개 책의 실습 모델 채택 전 별도 이용 조건 검토가 필요함 | **실습 자산으로 미채택** |
| CharaConsist | training-free foreground/background character consistency | FLUX.1 기반 연구 구현으로 consistent generation을 목표로 하나, character turnaround를 보장하거나 8 GB VRAM을 명시하지 않는다 | **재현성/자원 preflight 전에는 미채택** |
| Animagine XL 4.0 prompt-only | SDXL base가 clean webtoon character sheet의 기본 작화가 될 수 있는지 확인 | `512 x 768`, 20 step, 4 seed에서 thick graphic line, white hair, malformed/누락 bag, grid·text-like artifact가 반복됨 | **실험 후 제외** |
| 사람이 승인한 turnaround 원본 + 구조 제어 | camera별 원본을 먼저 고정하고 이후 생성 모델에 identity와 style 기준 제공 | 모델의 독립 seed, reference strength, camera drift를 원본 승인 단계에서 분리할 수 있음 | **현재의 유일한 채택 경로** |

## 중요한 구분

### 다각도 모델은 웹툰 character sheet와 같은 문제가 아니다

MV-Adapter, SyncDreamer, Zero123++는 한 입력에서 다각도를 함께 다루는 연구·구현이다. 그러나 이들은 기본적으로 view consistency 또는 3D reconstruction의 문제를 푼다. 웹툰 character pack은 여기에 얼굴형·앞머리·hair clip, 의상 재단, 가방 strap과 flap, 선·색·명암을 **독자가 비교할 수 있게 고정하는 편집 문제**를 추가한다.

특히 사람 전신의 side/rear에서는 보이지 않는 면을 새로 추론한다. 한 장의 front master에 없던 뒷머리, 재킷 뒤판, strap의 등쪽 경로는 reference image가 정답을 제공하지 않는다. 이 정보가 없는 상태에서 seed를 늘리거나 output 하나를 고르는 것은 multi-view consistency의 증명이 아니다.

### reference adapter는 pack 생성기가 아니라 pack의 소비자다

Diffusers의 IP-Adapter는 image prompt를 추가하는 adapter이며, multiple image와 mask, face/style adapter 조합을 제공한다. 이는 완성된 face·style·소품 원본을 서로 다른 역할로 전달할 수 있다는 뜻이다. 그러나 adapter가 missing side/rear reference를 만들거나, 서로 충돌하는 reference를 자동 조정한다는 뜻은 아니다.

현재 P7-5.3도 이 경계를 확인했다. one-reference, multi-reference, Plus + Plus Face 순으로 reference를 늘렸지만, 얼굴과 가방 geometry를 함께 승인하지 못했다. 따라서 다음 실험에서 reference 수나 scale만 다시 바꾸는 것은 새 가설이 아니다.

## 현재 채택할 생성 절차

### 1. 생성과 승인을 분리한다

캐릭터의 첫 후보는 text-to-image나 외부 일러스트 도구로 만들 수 있다. 다만 첫 후보는 `draft master`다. 이를 그대로 LoRA 학습이나 ControlNet input으로 쓰지 않는다.

### 2. turnarounds는 독립 원본으로 확보한다

front, 3/4, side, rear를 한 seed의 반복 산출물로 간주하지 않는다. 각 방향은 사람 검수 또는 직접 수정으로 다음을 명시해야 한다.

- 머리 실루엣, hair clip의 고정 위치와 rear에서 보이지 않을 때의 규칙
- 눈·눈썹·앞머리·얼굴 윤곽의 view별 관찰 항목
- 재킷의 pocket, collar, sleeve와 바지의 waist·hem 구조
- 가방 하나, flap 하나, strap 하나의 앞·옆·뒤 경로
- 머리 기준 등신, 어깨·골반 폭, 손목·발목 위치와 양쪽 신발

한 방향에서 오류가 있으면 해당 view만 다시 만들거나 직접 고친다. 다른 view를 기준으로 crop하거나 inpaint해서 연결하지 않는다. 이는 structural source를 바꾸는 작업이며 local detail 보정이 아니다.

### 3. face·prop·style sheet를 별도로 만든다

전신 turnaround는 얼굴의 작은 차이와 소품의 연결 구조를 충분히 검수하기 어렵다. 그러므로 face sheet와 bag/strap sheet를 별도 원본으로 추가한다. style sheet에는 허용 line width, palette, shadow edge, 금지 texture를 기록한다.

### 4. revision 단위로 승인한다

전신, face, prop, style 중 하나를 고치면 pack revision을 새로 만든다. 이전 revision에서 생성한 LoRA, IP-Adapter 비교, inpaint 결과는 새 기준의 통과 근거로 재사용하지 않는다. 학습은 승인된 모든 source에 prompt, seed, license/provenance, review record가 갖춰진 뒤에만 시작한다.

## 8 GB에서 다음에 검증할 한 가지

다각도 모델을 새로 설치하거나 여러 adapter를 더하지 않는다. 다음 실험은 **승인된 사람 제작 turnaround 한 장을 camera control source로 사용했을 때**, SD 1.5 또는 SDXL의 단일 ControlNet이 target view의 body projection과 frame을 유지하는지 확인하는 `structure-only` baseline이다.

- identity adapter, LoRA, inpaint는 끈다.
- 입력 turnaround와 생성 결과에서 head-neck direction, shoulder/hip orientation, wrist/ankle, full-body crop, bag 위치를 비교한다.
- control on/off 쌍에서 실제 camera 구조 차이가 있어야 통과다.
- 통과해도 character identity 또는 style 통과를 주장하지 않는다.

이 baseline이 성립하면 다음에만 승인된 face/style/character anchor 하나를 더해 결합 효과를 측정한다. baseline이 실패하면 character reference의 수나 LoRA 학습을 늘리지 않고 camera control source와 모델 호환성을 고친다.

## InvokeAI에서 가져올 것과 가져오지 않을 것

InvokeAI는 character consistency를 자동으로 보장하는 별도 model family가 아니다. 공개 저장소가 설명하는 강점은 local generation, Canvas의 inpaint/outpaint와 brush, node workflow, gallery/board의 image metadata 관리다. 따라서 현 파이프라인에서는 **승인 원본을 만들고 revision을 추적하는 도구**로 평가한다.

### 가져올 수 있는 운영 방식

1. 한 board를 character pack revision 하나에만 연결하고 front, 3/4, side, rear, face, bag/strap을 별도 원본으로 둔다.
2. Canvas의 mask는 전체 structure가 통과한 뒤 얼굴·손·가방 flap 같은 `L local detail fail`에만 쓴다. camera, 다리 길이, bag wearing position이 틀린 이미지를 Canvas 보정으로 승인하지 않는다.
3. 생성마다 prompt, seed, model, adapter, mask, source image를 gallery metadata와 함께 저장하고, 승인본만 pack board에 옮긴다. 이 기록은 현재의 JSON manifest와 같은 역할을 한다.
4. Workflow는 `structure source -> ControlNet baseline -> whole-frame review -> local mask repair` 순서를 고정하고, identity adapter나 LoRA는 별도 off/on branch로 둔다.

### 새 품질 해법으로 채택하지 않는 이유

- InvokeAI v6.11 release의 FLUX.2 Klein 안내는 4B FP8을 8 GB 이상, Q4를 6-8 GB에서 실행 가능 후보로 설명한다. 그러나 quantization에는 생성 정확도 손실이 있고, multiple reference image는 각각 VRAM 사용량을 늘린다.
- 같은 release는 F2K image editing이 여러 reference와 명령형 prompt를 받을 수 있다고 설명하지만, reference마다 weight를 조절할 수 없다고 명시한다. 이는 우리 실험에서 확인한 `reference 수를 늘려도 face·bag을 고정하지 못함`을 해결하는 제어가 아니다.
- v6.11은 FLUX.2 Klein ControlNet을 지원하지 않는다고 안내했다. 이후 v6.12 release는 FLUX.2 Klein LoRA format 지원을 추가했지만, F2K ControlNet 지원은 확인하지 못했다. 설치 시점의 model matrix는 다시 검증해야 한다.
- Direct Diffusers FLUX.2 Klein reference-conditioning도 이미 side/3-4 camera 반복과 rear bag 위치 변경으로 character-pack gate에 실패했다. InvokeAI UI로 같은 underlying model을 호출하는 것만으로 이 결과가 뒤집힌다고 가정하지 않는다.
- InvokeAI v6.13의 Qwen Image Edit는 최대 세 reference와 명령형 편집을 지원하지만, full model starter가 약 40 GB라고 안내한다. quantized variant의 현재 8 GB quality/VRAM은 별도 실측 전에는 채택하지 않는다.

따라서 InvokeAI의 다음 가치 있는 사용은 새 model download나 automatic turnaround 생성 실험이 아니라, **사람이 승인한 character pack revision을 Canvas/Board workflow로 보정·기록하는 운영 preflight**다. 이 도구를 사용하더라도 최종 승인 기준은 이 문서의 turnaround, face, prop, style contract를 그대로 유지한다.

## 출처와 이용 조건 확인

- [MV-Adapter: Multi-view Consistent Image Generation Made Easy, 공식 저장소](https://github.com/huanngzh/MV-Adapter){: target="_blank" rel="noopener noreferrer" }: image-to-multiview에 약 14 GB GPU memory가 필요하다고 명시한다. 확인일 2026-08-03.
- [SyncDreamer: Generating Multiview-consistent Images from a Single-view Image, 공식 저장소](https://github.com/liuyuan-pal/SyncDreamer){: target="_blank" rel="noopener noreferrer" }: limited-memory mode가 10 GB 미만이라고 설명하며 seed/crop/elevation에 따른 선택을 권한다. 확인일 2026-08-03.
- [Zero123++ 공식 저장소](https://github.com/SUDO-AI-3D/zero123plus){: target="_blank" rel="noopener noreferrer" }: multi-view가 3D generation에 초점이 있고, code Apache-2.0 / model weights CC-BY-NC 4.0이라고 안내한다. 확인일 2026-08-03.
- [CharaConsist 공식 저장소](https://github.com/Murray-Wang/CharaConsist){: target="_blank" rel="noopener noreferrer" }: FLUX.1 기반의 training-free consistent character generation을 소개하지만 8 GB requirement나 turnaround 품질 보장은 확인하지 못했다. 확인일 2026-08-03.
- [Diffusers IP-Adapter 안내](https://huggingface.co/docs/diffusers/v0.30.3/using-diffusers/ip_adapter){: target="_blank" rel="noopener noreferrer" }: image prompt, multi-image, masked reference, Face/Plus adapter의 역할과 scale 조절을 설명한다. 확인일 2026-08-03.
- [InvokeAI 공식 저장소](https://github.com/invoke-ai/InvokeAI){: target="_blank" rel="noopener noreferrer" }: Canvas, workflow, board/gallery metadata와 지원 model 범위를 설명한다. 확인일 2026-08-03.
- [InvokeAI release notes](https://github.com/invoke-ai/InvokeAI/releases){: target="_blank" rel="noopener noreferrer" }: FLUX.2 Klein 4B의 quantized VRAM 안내, multiple reference 편집의 weight/VRAM 제한, F2K ControlNet 및 이후 LoRA 지원 변화를 확인했다. 확인일 2026-08-03.

이 문서는 법률 자문이 아니다. 외부 model weight, input image, output의 이용 조건은 코드 license와 분리해 실제 채택 직전에 다시 확인한다.
