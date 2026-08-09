# P7-5.4 화풍·연속성 보정: 컷신의 구조와 디테일을 분리해 고치기

> Section ID: `P7-5.4`
> Version: `v2026.08.09`

이 절은 `P7-5.3`에서 인체·가림·공간 관계를 검수한 장면 기준과 전체 컷이 생긴 뒤에 시작하는 후속 단계입니다. 현재 P7-5.3에는 구조·캐릭터 정보의 수용을 승인한 A/B/C 장면이 있지만, 공간·조명·그림자까지 통과한 완성 컷은 없습니다. 따라서 보정 도구를 최종 승인처럼 앞당겨 쓰지 않습니다. 목표는 한 장의 예쁜 이미지를 만드는 것이 아니라, 다른 pose·camera·장소의 네 컷에서 인물성, 화풍, 구조, 국소 디테일을 분리해 판정하는 것입니다. ControlNet은 pose·camera·silhouette 같은 구조 입력을 확인하는 수단이고, inpaint는 그 전체 frame이 통과한 뒤에만 얼굴·손·발·소품 접점을 고치는 수단입니다.

## LoRA 전환에는 별도 데이터와 학습 환경이 필요하다

참조 이미지만으로 얼굴과 복장이 약하게 섞일 때는 LoRA를 검토할 수 있다. 현 FLUX 경로에 맞는 학습 대상은 Apache-2.0인 **FLUX.2 Klein 4B Base**다. 학습은 Base checkpoint에서 하고, 완성한 adapter는 빠른 distilled 4B 추론 모델에 붙인다.

하지만 이는 현재 8 GB GPU에서 바로 실행할 다음 단계가 아니다. 공식 Klein LoRA 안내의 4B Base 학습 예시는 약 24 GB VRAM 환경을 전제로 한다. 이는 모든 설정의 절대 최소치가 아니라 공식 예제의 검증 조건이지만, 현재 8 GB 환경에서 같은 학습을 승인할 근거로 사용할 수는 없다. FLUX.1-dev QLoRA 공식 사례의 peak도 약 9 GB이고 base model의 비상업 라이선스가 현재의 개방 라이선스 기준과 맞지 않는다.

학습을 시작하려면 먼저 올바른 데이터를 확보한다. 공식 예시의 스타일 LoRA는 서로 다른 구도와 시점을 가진 15–40장의 이미지와 각 이미지의 내용 caption·동일 trigger word를 사용한다. 현재 P7-5.2 기준 자산은 얼굴·전신·소품 보드가 섞여 있어 그 자체를 하나의 학습 데이터셋으로 보지 않는다. 실패하거나 왜곡된 생성 이미지도 학습 데이터로 사용하지 않는다.

구도 보존과 캐릭터 교체를 함께 학습하려면 입력 이미지와 목표 이미지를 짝짓는 **edit LoRA** 형식이 더 직접적이다. 공식 안내는 `control_path`로 이 쌍을 연결하지만 보편적인 최소 쌍 수를 보장하지 않는다. 따라서 필요한 데이터 수는 임의로 확정하지 않고, 같은 포즈·구도에서 캐릭터·복장이 완성된 검수 쌍과 별도 학습 환경을 확보한 뒤 실험으로 정한다.

## 8 GB에서 확인할 순서는 실행 가능성과 품질을 섞지 않는다

8 GB에서 RAM이나 SSD를 보조로 쓰는 실행기는 VRAM을 물리적으로 늘리는 장치가 아니다. 현재 쓰지 않는 가중치를 CPU RAM 또는 디스크에 두었다가 GPU로 옮기는 방식이므로, 실행이 끝났다는 사실만으로 웹툰 컷의 품질이나 학습 가능성을 뜻하지 않는다. CUDA Unified Memory도 하드웨어·운영체제 조건에 따라 메모리 초과 할당과 페이지 이동을 지원하지만, 이동과 page fault가 반복되면 속도가 크게 떨어질 수 있다. 특히 Windows와 WSL에서는 oversubscription 조건이 더 제한적이다.

따라서 아직 전체 frame을 통과한 P7-5.3 컷이 없는 현재 단계에서는, 아래 순서를 **제작 컷이 아닌 권리·입력 조건이 확인된 고정 시험 이미지**에서 먼저 확인한다. 시험용 이미지의 통과는 P7-5.3 장면의 승인이 아니며, 그 장면을 inpaint할 권한도 만들지 않는다.

| 순서 | 비교할 수단 | 고정 조건과 기록 | 다음 단계로 갈 조건 |
| --- | --- | --- | --- |
| 0 | 실행 환경 | GPU·드라이버·OS·CUDA, 물리 VRAM, RAM, SSD 여유 공간을 기록한다. | 외부 GPU에서 CUDA가 실제로 보인다. |
| 1 | SDXL inpaint 실행기 | 기존 Diffusers sequential CPU offload와 ComfyUI Dynamic VRAM을 같은 모델·mask·seed·해상도로 비교한다. VRAM peak, RAM, SSD I/O, 장당 시간을 남긴다. | 둘 중 하나가 OOM 없이 반복 실행된다. |
| 2 | 저정밀 추론 | 같은 SDXL inpaint에서 FP8 layerwise casting 또는 4-bit 양자화를 한 번에 하나씩 비교한다. 원본과 mask 경계·색·얼굴 손상을 함께 판정한다. | 기준 실행보다 메모리 또는 시간이 개선되고 품질 하락이 허용 범위다. |
| 3 | LoRA 최소 학습 | SD 1.5, `512 x 768`, batch 1에서 style과 character를 섞지 않은 소규모 LoRA를 학습한다. 데이터 권리, caption, loss, peak VRAM, sample grid를 남긴다. | 학습이 끝나고 held-out prompt에서 trigger와 화풍 또는 인물성 중 하나를 재현한다. |
| 4 | LoRA와 국소 편집의 결합 | 통과한 adapter 하나만 SD 1.5 inpaint checkpoint에 연결하고, LoRA 없음/on을 같은 mask·seed로 비교한다. 이어서 수동 mask와 DiffEdit 자동 mask를 같은 수정 요청에서 비교한다. | 변경 영역 밖의 화풍·인물성이 유지되고, 경계 누수와 새 구조 오류가 없다. |
| 5 | 제작 컷 적용 | P7-5.3의 전체 frame이 별도 검수를 통과한 뒤에만, 통과한 한 조합을 얼굴·손·발·소품의 승인 mask에 적용한다. | 네 컷 ledger에서 identity·structure·style·local detail이 모두 통과한다. |

ComfyUI Dynamic VRAM은 메모리 운영을 바꾸는 후보이고, SDXL inpaint의 화풍·인물 품질을 보장하는 모델 교체가 아니다. Diffusers의 FP8 layerwise casting과 4-bit 양자화도 가중치 저장 메모리를 줄일 수 있지만 활성값 peak와 출력 품질은 별도로 측정해야 한다. 특히 layerwise casting은 PEFT/LoRA가 들어간 사용자 정의 경로에서 호환되지 않을 수 있으므로, LoRA를 붙이기 전과 후를 분리한다.

SD 3.5 Medium의 4-bit 추론은 현대적인 저정밀 base의 별도 후보로 남긴다. 그러나 이 절의 목표인 LoRA와 mask inpaint를 같은 계약으로 비교할 공식 inpainting checkpoint를 확인하지 못했으므로, 순서 1–4의 기준선으로 바꾸지 않는다. T2I-Adapter와 StyleAligned도 각각 구조 제어와 학습 없는 화풍 일관성의 연구 후보이지만, T2I-Adapter의 공식 SDXL 예시는 최소 15 GB 추론을 명시하고 StyleAligned의 8 GB 재현 조건도 확인되지 않았다. 현재 8 GB 실험 순서에는 넣지 않고, 기준선이 통과한 뒤 별도 비교로만 다룬다.

## DiffEdit 자동 mask의 첫 8 GB 결과

가장 작은 추가 모델 경로가 실제로 국소 보정을 대신할 수 있는지 먼저 확인했다. P7-5.2의 승인 전신 정면을 **고정 시험 입력**으로 두고, charcoal crop top에 cropped white jacket을 추가하라는 목표 prompt로 DiffEdit mask를 만들었다. 이 입력은 P7-5.3의 승인 full-frame 컷이 아니므로, 이 실행은 제작 컷 보정이나 승인 후보 생성이 아니라 자동 mask의 실행·실패 조건을 확인하는 preflight다.

![DiffEdit 첫 8 GB probe: 고정 입력, 자동 mask, 편집 출력](../../../assets/part-07/chapter-05/p7-5-4-diffedit-first-probe-contact-sheet.png)

`512 x 768`, 20 step, mask map 4개, seed `5404`에서 SD 1.5 base와 DiffEdit만 사용했다. sequential CPU offload와 attention slicing으로 실행은 `20.6초`, 관측 peak VRAM은 `2,723 MiB`였고, ControlNet·IP-Adapter·LoRA는 추가하지 않았다. 따라서 **8 GB에서 실행 가능**이라는 항목은 통과했다.

그러나 자동 mask는 재킷이 있어야 할 몸통에 머물지 않고 머리·얼굴·바지·신발·바닥까지 넓게 잡았다. 출력은 흰 cropped jacket 대신 로고처럼 보이는 어두운 상의를 만들었고, 얼굴·머리·신발도 함께 바꿨다. 즉 변경 영역 밖 보존, 요청한 의상 반영, 경계 누수 없음의 세 품질 gate는 모두 실패했다. 이 PNG를 제작 자산이나 후속 inpaint 입력으로 승인하지 않으며, DiffEdit은 현재 **자동 mask 실패 대조군**으로만 보관한다.

prompt와 mask 설정을 바꾼 반복도 세 번으로 닫았다. threshold를 `8.0`으로 높이고 mask encode strength를 `0.2`로 낮춘 첫 반복은 `35.1초`, peak `6,336 MiB`에서 mask 확산을 줄였지만 재킷 영역까지 거의 없애 버렸다. threshold를 `5.0`으로 완화하고 목표를 white cropped jacket 하나로 줄인 마지막 반복은 `34.0초`, peak `7,236 MiB`였지만, 다시 얼굴·바지·신발까지 선택했고 상의·허리띠 artifact만 남겼다.

| 설정 | mask 판정 | 요청 편집 | 편집 밖 보존 | 판정 |
| --- | --- | --- | --- |
| 초기 20 step, ratio 3.0 | 전신·바닥으로 확산 | 흰 재킷 실패 | 얼굴·머리·신발 변경 | fail |
| 반복 30 step, ratio 8.0 | 지나치게 희소 | 재킷을 거의 바꾸지 않음 | 작은 비의도 변경 | fail |
| 반복 30 step, ratio 5.0, 재킷+상의 | 얼굴·하체·신발로 재확산 | 재킷 실패 | 작은 의상·신발 artifact | fail |
| 반복 30 step, ratio 5.0, 단일 의상 목표 | 얼굴·하체·신발로 재확산 | 흰 재킷 대신 상의·허리띠 artifact | 비의도 변경 | fail |

![DiffEdit 반복 3: 단일 의상 목표와 완화한 threshold](../../../assets/part-07/chapter-05/p7-5-4-diffedit-repeat-03-contact-sheet.png)

따라서 다음 비교는 DiffEdit의 prompt나 step을 계속 늘리는 것이 아니다. 전체 frame이 통과한 panel이 생긴 뒤, 사람이 제한한 mask와 같은 수정 요청을 나란히 놓아 자동 mask가 정말 필요한지 판단한다. 그 전까지는 이 반복 실패 결과로 DiffEdit을 제작 파이프라인에서 제외한다.

<details id="diffedit-first-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_4_diffedit_first_probe.py" data-language="python">
<summary>DiffEdit 첫 8 GB probe 전문 보기</summary>
<div class="aibook-lazy-source__body">`--steps`와 `--mask-maps`를 바꾸면 자동 mask·VRAM·시간이 어떻게 달라지는지 다시 확인할 수 있습니다.</div>
</details>

<details id="diffedit-first-probe-review" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7-5-4-diffedit-first-probe-review.json" data-language="json">
<summary>DiffEdit 첫 probe 검수 기록 보기</summary>
<div class="aibook-lazy-source__body">실행 조건과 자동 mask·보존·요청 편집의 실패 판정을 확인합니다.</div>
</details>

<details id="diffedit-repeat-review" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7-5-4-diffedit-repeat-review.json" data-language="json">
<summary>DiffEdit 반복 실험 검수 기록 보기</summary>
<div class="aibook-lazy-source__body">세 설정의 mask 범위, 출력 보존, VRAM·시간과 제외 결정을 확인합니다.</div>
</details>

## 한 컷에 하나의 주 제어만 둔다

| panel | 진입 전략 | 주 ControlNet | 먼저 통과할 항목 | inpaint 대상 |
| --- | --- | --- | --- | --- |
| 01 | face-first | lineart | 얼굴과 시선 | 눈, 앞머리 |
| 02 | pose-first | OpenPose | 전신, 손목, 발 접지 | 손목, 발 |
| 03 | camera-background-first | depth | 원근과 전신 구도 | 실루엣, 배경 |
| 04 | object-first | lineart | 손-소품 접점 | 손, 시선 |

시작 조건은 SD 1.5, character LoRA, ControlNet 하나, `512 x 768`, batch 1입니다. IP-Adapter, 두 번째 ControlNet, high-resolution fix는 동시에 추가하지 않습니다. 전체 frame이 structure와 identity를 통과한 뒤에만 얼굴, 손, 발, 배경 mask를 따로 inpaint합니다.

## 구조만 분리한 OpenPose 실행

먼저 identity 조건을 넣지 않고, 표준 SD 1.5와 `control_v11p_sd15_openpose` 하나만 실제 실행했습니다. 네 held-out 장면에서 OpenPose body map만 추출했습니다. 이 map에는 source 이미지의 얼굴, 머리색, 의상, 가방, 배경 픽셀이 들어가지 않습니다. 같은 짧은 prompt와 seed에서 ControlNet scale `0.0`과 `1.0`만 바꿨습니다.

![SD 1.5 OpenPose ControlNet off/on](../../../assets/part-07/chapter-05/p7-5-4-sd15-openpose-controlnet-on-off-contact-sheet.png)

scale `1.0`은 scale `0.0`보다 pose map의 팔·몸통·다리 방향을 따르고, 주방·난간·영화관·작업대의 큰 구조를 더 자주 만들었습니다. peak VRAM은 약 `3,211 MiB`였습니다. 반면 얼굴, 머리, 의상, 가방은 Mira 기준과 일치하지 않습니다. 이는 실패가 아니라 **structure만 부분 통과**한 결과입니다. 이 실험에는 identity 입력이 없으므로 동일 인물성의 근거로 쓰지 않습니다.

WD 1.5와 같은 OpenPose ControlNet을 묶으려는 시도는 text context 차원이 `1024` 대 `768`로 달라 실행 전에 중단했습니다. 따라서 이후 identity 결합은 WD base에 억지로 붙이지 않고, 이 SD 1.5 구조 baseline과 호환되는 별도 identity 조건을 off/on 비교해야 합니다.

## 호환되는 identity 조건을 더한 비교

SDXL OpenPose ControlNet과 SDXL IP-Adapter는 같은 계열이라 결합할 수 있습니다. 새 Mira 전신 기준을 IP-Adapter에 넣고 scale `0.0`과 `0.45`를 비교했습니다. `512 x 768`, 15 step은 일반 CPU offload에서 8 GB OOM이 났지만 sequential CPU offload에서는 완료했습니다.

![SDXL IP-Adapter와 OpenPose 비교](../../../assets/part-07/chapter-05/p7-5-4-sdxl-ipadapter-openpose-on-off-contact-sheet.png)

IP-Adapter on은 청록 단발, 흰 재킷, 청록 바지, crossbody 가방을 더 자주 남기면서 큰 pose와 장면 구조도 유지했습니다. 그러나 얼굴 세부, 가방 geometry, 손, 일부 camera와 장소는 여전히 흔들립니다. 따라서 이는 identity와 structure의 **부분 통과**이며, 최종 웹툰 컷 품질 통과가 아닙니다. 실행 조건은 아래 코드에서 확인합니다.

정면·3/4·얼굴·가방 detail을 포함한 다섯 reference도 같은 조건에서 비교했지만, 얼굴·가방 geometry는 안정화되지 않았고 일부 컷은 더 옅어졌습니다. [다중 reference 결과](../../../assets/part-07/chapter-05/p7-5-4-sdxl-multiref-ipadapter-openpose-contact-sheet.png)는 reference 수만 늘려서는 현재 결함을 고치지 못함을 보입니다. 이 경로는 inpaint나 두 번째 ControlNet으로 확장하지 않습니다.

<details id="sdxl-ipadapter-openpose-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_4_sdxl_ipadapter_openpose_probe.py" data-language="python">
<summary>SDXL IP-Adapter OpenPose probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

## 카메라 구조를 Canny로 분리해 보기

저각도 cinema 컷에서는 OpenPose보다 인물 실루엣과 배경 원근을 더 많이 담는 Canny 조건도 비교했습니다. 동일한 SDXL 범용 IP-Adapter와 seed에서 Canny scale만 `0.0`과 `0.75`로 바꿨습니다. 입력 Canny에는 기준 이미지의 색·질감이 아니라 윤곽선만 남습니다.

![SDXL Canny 카메라 조건 off/on](../../../assets/part-07/chapter-05/p7-5-4-sdxl-canny-camera-on-off.png)

Canny on은 몸을 굽혀 ticket 쪽으로 향하는 큰 방향과 foyer의 사선 원근을 off보다 더 따릅니다. 그러나 얼굴, 가방, 손, 전신 비례는 모두 품질 gate를 통과하지 못했습니다. 이 결과는 Canny가 **camera와 silhouette의 구조 보조 입력**으로는 유효하지만, identity나 작화 품질을 대신하지 못한다는 근거입니다. 이 PNG를 웹툰 완성 컷으로 채택하지 않습니다.

<details id="sdxl-canny-camera-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_4_sdxl_canny_camera_probe.py" data-language="python">
<summary>SDXL Canny 카메라 비교 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

## Identity 없이 Canny 구조만 비교하기

앞 비교에는 범용 IP-Adapter가 함께 들어가 있어, Canny가 camera를 바꾼 효과와 identity reference가 만든 효과를 완전히 분리하지 못했습니다. 그래서 옆면 전신 turnaround에서 Canny edge만 추출하고, RGB 원본·IP-Adapter·LoRA·inpaint를 모두 빼고 다시 비교했습니다. 같은 seed `5101`에서 ControlNet scale `0.0`과 `0.75`만 바꿨습니다.

![SDXL Canny structure-only off/on](../../../assets/part-07/chapter-05/p7-5-4-sdxl-canny-structure-only-contact-sheet.png)

off 결과는 옆면과 전신 비례를 따르지 못한 단순 인물입니다. 반면 on 결과는 왼쪽 side profile, 머리-목-어깨 방향, 전신 frame, 가방과 손의 큰 상대 위치를 Canny source에 가깝게 만듭니다. `512 x 768`, 15 step, sequential CPU offload에서 `33.5초`, 관측 peak VRAM `1,733MiB`로 실행됐습니다. 이 실험은 **camera·silhouette 구조 통과**의 근거입니다. 색, 얼굴, hair clip, 재킷·가방의 정확한 형태는 입력하지 않았으므로 identity나 style의 통과 근거는 아닙니다.

이 결과에서 조작할 값은 `controlnet_conditioning_scale`입니다. `0.0`과 `0.75`를 비교해 side profile과 bag 위치가 실제로 바뀌는지 본 뒤에만, 다음 실험에서 승인한 identity anchor 하나를 추가할 수 있습니다. 아래 코드에서 scale 또는 seed를 바꿔 같은 비교를 반복할 수 있습니다.

<details id="sdxl-canny-structure-only-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_4_sdxl_canny_structure_only_probe.py" data-language="python">
<summary>SDXL Canny structure-only probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

이 구조 baseline에 전신 identity reference 하나를 IP-Adapter scale `0.35`로 추가한 뒤에도 같은 비교를 했다. 정면/3-4 master와 Canny source와 같은 side reference를 각각 넣었지만, 두 경우 모두 side profile 구조는 남은 반면 hair가 옅은 흰색으로 바뀌고 face·bag geometry가 기준으로 돌아오지 않았다. 이 결함은 국소 inpaint 대상이 아니다. 이미 다중 reference와 Plus/Plus Face 비교도 실패했으므로 scale sweep, reference 추가, 두 번째 ControlNet으로 확장하지 않는다.

## Inpaint 전에 하는 panel 판정

결합 출력의 IP-Adapter on 네 panel을 다시 검토한 결과, identity·structure·style이 모두 `pass`인 panel은 없습니다. 따라서 현재 inpaint 가능 panel 수는 `0`입니다. 얼굴, 가방, 손, 소품 접점은 모두 문제이지만, full-frame identity 또는 structure가 먼저 실패한 상태에서 mask 보정으로 통과시키지 않습니다.

로컬 panel review ledger는 각 컷의 결함과 gate를 기록합니다. [review checker](../../../assets/part-07/chapter-05/p7_5_4_panel_review_check.py)는 이 기록에서 full-frame 통과와 repair eligibility가 모순되지 않는지 검사합니다.

후보 교체도 실제로 확인했습니다. SDXL Plus와 Plus Face를 기존 bigG 인코더 대신 ViT-H 인코더에 연결하고, 전신 기준과 독립 얼굴 detail을 별도 adapter slot으로 넣었습니다. `512 x 768`, 15 step, sequential CPU offload에서 두 조합 모두 생성은 완료했으므로 모델 계열·인코더·복수 adapter API·8 GB 실행 경로는 호환됩니다. 그러나 Plus 단독은 가방 geometry와 색 일관성을 충분히 개선하지 못했고, Plus Face 추가는 옆얼굴에 잘못된 세부를 만들며 배경도 약화했습니다. 따라서 이 교체는 quality gate에서 제외합니다. 실패 PNG와 실행 리포트는 보관하지 않습니다.

<details id="sdxl-plus-face-ipadapter-preflight" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_4_sdxl_plus_face_ipadapter_preflight.py" data-language="python">
<summary>SDXL Plus 및 Plus Face 교체 프리플라이트 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

## 생성 전에 지키는 입력 계약

이전 manifest 검사기는 삭제했다. P7-5.3의 [FLUX 스토리보드 코드](../../../assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py)는 후보 스토리보드를 만들고, 사람 검수로 승인한 PNG를 명시할 때만 lineart·Canny·depth를 파생한다. 현재 A/B/C의 구조 수용 결과는 있지만 공간·조명·그림자까지 통과한 완성 컷은 없으므로, 이 절의 inpaint 판단은 전체 frame 검수 뒤에만 시작한다.

P7-5.4에서 inpaint를 검토할 수 있는 조건도 같다. 먼저 P7-5.3에서 행동·인체·거리 관계가 읽히는 스토리보드와 전체 웹툰 컷을 사람 검수한다. 그 전체 frame이 통과하지 않으면 얼굴·손·발·소품의 mask 보정으로 넘어가지 않는다.

실제 structure probe의 조건은 아래 실행 코드에서 확인합니다.

<details id="sd15-openpose-structure-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_4_sd15_openpose_structure_probe.py" data-language="python">
<summary>SD 1.5 OpenPose structure probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

## 네 컷으로 최종 판정하기

각 panel은 ControlNet off/on PNG와 identity anchor off/on PNG를 남깁니다. 마지막 contact sheet에서 아래 네 값을 독립적으로 `pass` 또는 `fail`로 기록합니다.

| 항목 | 실패하면 돌아갈 곳 |
| --- | --- |
| identity | 참조 팩, LoRA 데이터, caption |
| structure | pose/depth/line control 입력과 scale |
| style | style sheet, LoRA weight, prompt |
| local detail | 승인한 mask의 inpaint 설정 |

구조가 틀린 컷을 얼굴 inpaint로 고치거나, identity가 흔들리는 컷을 ControlNet scale로 해결하려 하면 원인을 잃습니다. 네 컷 모두가 통과하기 전의 단일 PNG는 파이프라인 통과 근거가 아닙니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 승인 | 참조 팩·권리·컷별 control image가 모두 승인됐는가? |
| 비교 | ControlNet과 identity anchor의 on/off 비교를 분리했는가? |
| 보정 | 전체 구조 통과 뒤에만 mask inpaint를 했는가? |
| 연속성 | 네 컷 contact sheet에서 같은 기준으로 pass/fail을 기록했는가? |

## 출처와 참고 자료

- Zhang et al., [ControlNet](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
- Tencent AI Lab, [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-03.
- Hugging Face, [Diffusers IP-Adapter guide](https://huggingface.co/docs/diffusers/v0.36.0/using-diffusers/ip_adapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-03.
- Comfy-Org, [ControlNet workflow](https://docs.comfy.org/tutorials/controlnet/controlnet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
- Comfy-Org, [Inpainting](https://docs.comfy.org/tutorials/basic/inpaint){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
- NVIDIA, [Unified and System Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. CUDA Unified Memory의 운영체제·하드웨어별 조건, Linux HMM/ATS와 Windows·WSL 제한을 확인했다.
- Comfy-Org, [Changelog](https://docs.comfy.org/changelog){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. Dynamic VRAM, FP16 intermediates, FP8·동적 offload 관련 변경을 확인했다.
- Hugging Face, [Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. sequential/group/disk offload와 layerwise casting의 메모리·속도·PEFT 호환성 한계를 확인했다.
- Hugging Face, [SDXL Inpainting 0.1](https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. SDXL inpaint 기준 checkpoint와 라이선스·학습 해상도를 확인했다.
- Hugging Face, [DiffEdit](https://huggingface.co/docs/diffusers/v0.17.0/api/pipelines/diffedit){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. prompt 차이로 semantic edit mask를 추정하는 비교 수단을 확인했다.
- Hugging Face, [SD 3.5 Medium](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. 공식 4-bit 추론 예시와 모델 라이선스를 확인했다.
- Tencent ARC, [T2I-Adapter](https://github.com/TencentARC/T2I-Adapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. 공식 SDXL 예시의 최소 15 GB 추론 조건을 확인했다.
- Hertz et al., [StyleAligned](https://style-aligned-gen.github.io/){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-09. 학습 없이 reference style을 공유 attention으로 맞추는 연구 후보와 재현 조건의 한계를 확인했다.
- Black Forest Labs, [FLUX.2 Klein LoRA 학습 안내](https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-07. Base 4B 학습, 15–40장 스타일 예시, 약 24 GB VRAM의 공식 예제 조건과 edit LoRA의 `control_path` 형식을 확인했다.
- Hugging Face, [FLUX.1-dev QLoRA 안내](https://huggingface.co/blog/flux-qlora){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-07. 공식 사례의 약 9 GB peak와 저메모리 설정을 비교 근거로 사용했다.
