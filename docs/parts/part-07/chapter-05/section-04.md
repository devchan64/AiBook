# P7-5.4 화풍·연속성 보정: 컷신의 구조와 디테일을 분리해 고치기

> Section ID: `P7-5.4`
> Version: `v2026.08.06`

마지막 실험은 `P7-5.3`에서 생성한 컷신 후보 중 전체 frame이 읽히는 결과만 대상으로, 화풍과 컷 사이 연속성을 보정하는 단계입니다. 목표는 한 장의 예쁜 이미지를 만드는 것이 아니라, 다른 pose·camera·장소의 네 컷에서 인물성, 화풍, 구조, 국소 디테일을 분리해 판정하는 것입니다. ControlNet은 pose·camera·silhouette 같은 구조 입력을 확인하는 수단이고, inpaint는 그 전체 frame이 통과한 뒤에만 얼굴·손·발·소품 접점을 고치는 수단입니다.

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

## Python으로 실행 전 계약을 검사하기

저장소의 검증기는 참조 팩 승인 전에는 generation 단계로 넘어가지 못하게 하고, panel마다 camera, identity anchor, repair target을 요구합니다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_3_controlnet_pipeline_check.py \
  docs/assets/part-07/chapter-05/p7-5-3-controlnet-pipeline-manifest.json
```

현재 템플릿의 출력은 `BLOCKED asset ...`입니다. 이는 오류가 아니라 전신·얼굴·화풍·장소 sheet가 승인되기 전에는 생성 결과를 최종 웹툰 컷으로 올리지 않는다는 경계입니다. [검사 스크립트](../../../assets/part-07/chapter-05/p7_5_3_controlnet_pipeline_check.py)와 [현재 출력](../../../assets/part-07/chapter-05/p7-5-3-controlnet-pipeline-check.txt)을 함께 확인합니다.

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
