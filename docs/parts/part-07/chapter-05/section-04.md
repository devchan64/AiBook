# P7-5.4 화풍·연속성 보정: 컷신의 구조와 디테일을 분리해 고치기

> Section ID: `P7-5.4`
> Version: `v2026.08.16`

같은 캐릭터를 다른 카메라와 동작에서도 다시 그릴 수 있을까? 이 절에서는 한 장이 그럴듯한지를 보지 않고, 아래 네 계약을 동시에 확인했다. 실험은 하나의 도구를 고르는 과정이 아니라, 어느 계약이 깨지는지 찾아 다음 입력의 역할을 좁히는 과정이었다.

| 계약 | 확인할 질문 |
| --- | --- |
| structure | 카메라, 인체 동작, 거리와 가림이 장면 의도에 맞는가? |
| identity | 얼굴과 신체 비율이 같은 캐릭터로 읽히는가? |
| outfit | 재킷·상의·바지·신발·가방의 형태와 레이어가 유지됐는가? |
| style | 승인한 선화·색·질감의 범위 안에 있는가? |

!!! abstract "주요 서사"

    수평 시점에서 확인한 캐릭터 계약은 고각도에서 함께 깨졌다. 얼굴·동작·카메라·복장을 하나의 조건에 맡긴 보조 실험들은 각각 일부 계약만 보존했다. 최종적으로 고각도 guide, 정면 얼굴, 완성 착장을 서로 다른 입력 역할로 나눈 Qwen 편집에서 네 계약을 함께 통과했다. 아래의 `보조 실험`은 이 역할 분리가 필요한 이유와 적용 범위를 확인한 기록이다.

아래 흐름은 도구의 이름이 아니라 **실패한 계약이 다음 선택을 어떻게 바꾸었는지**를 압축한다. 뒤의 보조 실험은 각 화살표의 근거다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-4-experiment-decision-flow-ko.mmd"
```

## 주요 서사 1. 수평 시점에서는 되던 일이 고각도에서 깨졌다

FLUX는 수평에 가까운 정면·쿼터 전신에서 청록 단발, 호박색 눈, 흰 크롭 재킷, 청록 와이드 바지, 흰 운동화, 남색 가방의 관계를 비교적 안정적으로 재현했다. 문제가 된 것은 카메라가 위로 올라간 뒤였다. 고각도에서는 얼굴, 재킷 레이어, 와이드 바지 실루엣, 가방의 앞뒤 가림이 함께 흔들렸다.

그래서 이후의 질문은 “수평 결과를 조금 더 다듬을 수 있는가?”가 아니었다. **고각도에서 바뀌는 구조를 누가 맡고, 그 안에서 얼굴·복장·화풍을 누가 보존할 것인가?**가 되었다.

## 보조 실험 A. 얼굴 형성과 전신 캐릭터 재현은 다르다

> **이 보조 실험이 확인한 것:** 50 step의 base model은 얼굴을 만들 수 있지만, 전신에 조건을 결합한 뒤의 identity·outfit 실패를 그 문제로 환원할 수는 없다.

먼저 reference·ControlNet·LoRA를 모두 제외한 SDXL Base 1.0 단독으로 정상적인 정면 얼굴이 형성되는지 확인했다. `1024×1024`, 50 step, CFG `5.0`, seed `62295`에서 청록 단발·호박색 눈·수채화 웹툰이라는 텍스트만 주었다. 이 결과는 Mira identity의 승인 기준이 아니라, **base model이 얼굴 자체를 만들 수 있는가**를 분리한 기준선이다.

![SDXL Base 1.0 단독 50 step 얼굴 probe](../../../assets/part-07/chapter-05/p7-5-4-sdxl-base-face-50steps.png)

따라서 전신 결과에서 얼굴이나 정체성이 흔들린다고 해서 base model이 얼굴을 전혀 만들지 못한다고 해석할 수는 없다. [실행 기록](../../../assets/part-07/chapter-05/p7-5-4-sdxl-base-face-50step-run.json)은 이 기준선의 prompt·seed·해상도와 제외한 조건을 보관한다.

같은 생각으로 전신에서는 FaceID와 전신 착장 image adapter를 빼고 Plus Face `0.15`, character LoRA `0.30`, seed `62295`, CFG `5.0`, `960×1440`, 50 step을 고정해 OpenPose off/on을 비교했다. OpenPose를 켜면 다리·몸통의 2D 배치는 더 따랐지만, 고양이 귀·머리 길이·복장이 이탈했다. off도 얼굴 윤곽과 전신은 만들었으나 승인 재킷·바지·가방은 유지하지 못했다.

![SDXL 전신 safe-face 조건의 OpenPose off/on 비교](../../../assets/part-07/chapter-05/p7-5-4-sdxl-safe-face-openpose-ab-contact-sheet.png)

![SDXL safe-face 전신 후보와 승인 얼굴 기준 비교](../../../assets/part-07/chapter-05/p7-5-4-sdxl-safe-face-contact-sheet.png)

저해상도 `512×768`에서 50/100 step도 비교했다. step을 늘려도 identity·outfit이 자동으로 승인 기준에 수렴하지 않았다. step과 해상도는 얼굴·구조 형성의 조건일 수 있지만, 캐릭터 고정이나 복장 가림 관계를 대신하지 않는다. [전신 off 기록](../../../assets/part-07/chapter-05/p7-5-4-sdxl-safe-face-without-openpose-960x1440-run.json)과 [on 기록](../../../assets/part-07/chapter-05/p7-5-4-sdxl-safe-face-with-openpose-960x1440-run.json)에 조건을 남겼다.

얼굴 조건을 더 강하게 넣어도 전신 계약이 따라오지는 않았다. FaceID 단독은 전신 frame을 남겼지만 검은 장발·다른 착장으로 바뀌었고, FullFace 결합은 청록 단발·호박색 눈 단서를 늘렸지만 흉상 구도로 수렴했다. 이 비교는 얼굴 embedding을 세게 주는 것만으로 전신 캐릭터가 재현되지는 않는다는 뜻이다.

| FaceID 단독 | FaceID + FullFace |
| --- | --- |
| ![FaceID 단독 후보](../../../assets/part-07/chapter-05/p7-5-4-faceid-only-candidate.png) | ![FaceID와 FullFace 결합 후보](../../../assets/part-07/chapter-05/p7-5-4-faceid-fullface-candidate.png) |
| 전신 frame 일부 유지, identity·outfit 미통과 | 얼굴 단서는 일부 회복, 전신·outfit 미통과 |

## 보조 실험 B. 캐릭터 조건을 강화하려고 54컷을 따로 구성했다

> **이 보조 실험이 확인한 것:** LoRA의 입력은 사람 승인 identity 18장과 동작 36장을 구분해 구성해야 하며, LoRA는 화풍·복장을 보조할 수 있어도 단독 identity·pose 해결책은 아니다.

참조 한 장이나 얼굴 adapter만으로 부족하다는 판단 뒤, character LoRA가 반복되는 화풍과 수평 시점의 복장을 얼마나 보조하는지 별도로 시험했다. 입력은 P7-5.2에서 사람 승인한 identity anchor 18장(얼굴·기본 전신·리파인 전신의 여섯 방향)과 P7-5.4에서 사람 승인한 동작 36장이다.

동작 데이터는 서기·보행·쪼그리기·점프·스포츠처럼 전신 변화가 큰 장면을 넣었다. 1단계에서 포즈·비례·의상 실루엣을 만들고, 2단계에서 같은 인물에 절제된 웹툰 수채화 화풍을 입힌 뒤 각 단계의 review JSON으로 승인 여부를 기록했다. 이는 고각도·새 동작·가림 관계의 자동 일반화를 증명하는 데이터가 아니라, character LoRA의 입력 계약을 분명히 한 실험이다.

<details id="character-lora-54-dataset" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7-5-4-character-lora-54/dataset-manifest.json" data-language="json">
<summary>54컷 character LoRA 데이터셋 manifest 보기</summary>
<div class="aibook-lazy-source__body">identity 18장과 사람 승인 동작 36장의 파일·caption·hash·분류를 불러옵니다.</div>
</details>

<details id="character-lora-54-preparation" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_4_prepare_character_lora_action_dataset.py" data-language="python">
<summary>54컷 데이터셋을 로컬 학습 디렉터리로 준비하는 코드 보기</summary>
<div class="aibook-lazy-source__body">승인 record를 검증하고 PNG symlink·caption·manifest를 만드는 코드를 불러옵니다.</div>
</details>

LoRA on은 off보다 화풍과 착장 경향을 끌어왔지만, 정확한 얼굴·동작·가방을 단독으로 고정하지는 못했다. FacePlus와 FaceID를 함께 써도 얼굴 단서는 보조할 뿐 전신 계약을 통과시키지 못했다.

| character LoRA on/off | FacePlus + FaceID |
| --- | --- |
| ![character LoRA on/off 비교](../../../assets/part-07/chapter-05/p7-5-4-character-lora-on-off-contact-sheet.png) | ![FacePlus와 FaceID 결합 후보](../../../assets/part-07/chapter-05/p7-5-4-faceplus-faceid-contact-sheet.png) |
| 화풍·착장 경향은 보조 | 얼굴 단서는 생겨도 전신 계약 미통과 |

## 보조 실험 C. OpenPose는 동작의 2D 배치를 보조했다

> **이 보조 실험이 확인한 것:** OpenPose는 팔·다리·접지의 2D 배치를 전달하지만, 고각도 카메라와 3D 가림 관계를 결정하지는 않는다.

강화한 LoRA를 넣은 뒤에는 OpenPose가 무엇을 실제로 맡는지 다시 확인했다. P7-5.2의 승인 전신에서 정면·우측 쿼터·좌우 측면·후면 skeleton map 다섯 장을 저장해 detector를 매번 다시 실행하지 않도록 했다. [정면](../../../assets/part-07/chapter-05/p7-5-4-openpose-fullbody-front-reference.png) · [우측 쿼터](../../../assets/part-07/chapter-05/p7-5-4-openpose-fullbody-front-quarter-right-reference.png) · [좌측 측면](../../../assets/part-07/chapter-05/p7-5-4-openpose-fullbody-profile-left-reference.png) · [우측 측면](../../../assets/part-07/chapter-05/p7-5-4-openpose-fullbody-profile-right-reference.png) · [후면](../../../assets/part-07/chapter-05/p7-5-4-openpose-fullbody-rear-reference.png)을 재사용했다.

Animagine XL `960×1440`, 30 step에서 LoRA `0.6`을 고정했을 때, 저장 우측 쿼터 map의 ControlNet `1.0`은 `0.0`보다 다리·발의 2D 배치를 더 잘 따르면서 단발·눈·재킷·와이드 바지·가방을 일부 남겼다. 선언형 오른팔 올리기 map에서도 `1.0`은 팔의 방향을 따라갔다. 반면 LoRA를 `0.8`로 올리면 바지가 거의 흰색이 되고, high-angle 문구를 보태도 위에서 내려다보는 원근은 생기지 않았다.

| 동작 guide off/on | LoRA `0.6/0.8` |
| --- | --- |
| ![선언형 OpenPose map ControlNet off/on](../../../assets/part-07/chapter-05/p7-5-4-openpose-declarative-reach-up-controlnet-ab-contact-sheet.png) | ![선언형 OpenPose map LoRA scale 비교](../../../assets/part-07/chapter-05/p7-5-4-openpose-declarative-reach-up-lora-scale-ab-contact-sheet.png) |
| 팔의 2D 구조는 map에 맞춰짐 | scale 상승은 색 계약의 해법이 아님 |

![선언형 OpenPose map에서 카메라 문구를 바꾼 비교](../../../assets/part-07/chapter-05/p7-5-4-openpose-declarative-reach-up-camera-ab-contact-sheet.png)

이 결과가 가리킨 다음 문제는 분명했다. OpenPose는 팔·다리·접지의 **2D 배치**를 전달할 수 있지만, 카메라의 3D 원근, 머리·흉곽 회전, 가방의 앞뒤 가림을 결정하지는 못한다. 따라서 고각도에는 별도의 구조용 guide가 필요했다. 각 비교의 실행 기록은 [저장 map](../../../assets/part-07/chapter-05/p7-5-4-openpose-static-quarter-right-report.json), [동작 off/on](../../../assets/part-07/chapter-05/p7-5-4-openpose-declarative-reach-up-controlnet-ab-report.json), [LoRA scale](../../../assets/part-07/chapter-05/p7-5-4-openpose-declarative-reach-up-lora-scale-ab-report.json), [카메라 문구](../../../assets/part-07/chapter-05/p7-5-4-openpose-declarative-reach-up-camera-ab-report.json)에 보관했다.

## 주요 서사 2. 고각도 guide를 만들고 캐릭터 조건을 전이한다

고각도 스토리보드 자체가 병목은 아니었다. 캐릭터 정보가 없는 익명 인물로 지붕·원근·보행 배치만 가진 구조용 초안을 만들 수 있었다. 여기서 Animagine은 최종 캐릭터 생성기가 아니라, 카메라와 동작을 분리하는 guide 생성기다.

![익명 인물로 만든 고각도 보행 guide](../../../assets/part-07/chapter-05/p7-5-4-experimental-animagine-high-angle-guide.png)

### 보조 실험: SDXL 전이에서 구조 조건을 분리한 결과

> **이 보조 실험이 확인한 것:** 인물 외곽을 뺀 background Canny와 OpenPose는 분리할 수 있지만, 현 8 GB SDXL 경로는 고각도·동작·identity·outfit을 함께 통과시키지 못했다.

그 guide의 인물 RGB·얼굴·복장은 버리고, OpenPose와 **인물을 제외한 배경 Canny**만 SDXL에 전달했다. SDXL Base 1.0, character LoRA `0.6`, seed `62431`, 50 step, `768×1152`에서 구조 조건을 하나씩 켠 비교다.

![익명 guide·OpenPose·인물 제외 배경 Canny와 SDXL Mira 전이 후보](../../../assets/part-07/chapter-05/p7-5-4-sdxl-anonymous-high-angle-transfer-review-sheet.png)

구조 조건이 없으면 high-angle이 사라졌다. OpenPose만 켜면 위쪽 카메라의 단서는 일부 남아도 달리기 동작이 앉거나 쪼그린 자세로 바뀌었다. 배경 Canny만 켜면 타일 원근은 남지만 인물 실루엣이 중복되었다. 두 ControlNet을 함께 쓰는 조건은 `768×1152`와 `512×768` 모두 현재 8 GB sequential-offload Diffusers 경로에서 완료되지 않았다. 사람 외곽을 뺀 background Canny와 pose/camera 입력 분리는 유효한 체크포인트였지만, 이 SDXL 경로는 고각도·동작·Mira identity·복장을 함께 재현하는 제작 도구로는 미통과다. [검수 기록](../../../assets/part-07/chapter-05/p7-5-4-sdxl-anonymous-high-angle-transfer-review.json)과 [실행 조건](../../../assets/part-07/chapter-05/p7-5-4-sdxl-anonymous-high-angle-transfer-report.json)을 보관했다.

### 보조 실험: depth·Canny와 역할 분리 adapter의 경계

depth와 역할 분리 adapter도 같은 경계를 보였다. 고각도 depth scaffold, 전신 완성 착장 global 조건, 얼굴 face 조건, character·outfit LoRA를 나눠 연결하면 타일 바닥 원근과 머리·눈 단서는 일부 남았다. 그러나 흰 크롭 재킷은 짧은 흰 상의가 되고 가방·strap은 사라졌다.

![SDXL depth와 역할 분리 adapter의 고각도 결과](../../../assets/part-07/chapter-05/p7-5-4-sdxl-depth-role-separated-review-sheet.png)

Canny도 카메라·실루엣의 보조 조건으로는 쓸 수 있었지만, 최근 사선 보행 후보에서는 얼굴·바지·가방 일부가 남는 대신 흰 재킷 레이어가 빠졌다. 구조를 더 강하게 전달하는 일과 승인 복장을 보존하는 일은 여전히 경쟁했다.

![Canny camera 조건의 사선 보행 비교](../../../assets/part-07/chapter-05/p7-5-4-canny-camera-condition-contact-sheet.png)

### 보조 실험을 다음 선택으로 읽기

| 관찰한 결과 | 피한 해석 | 다음 선택 |
| --- | --- | --- |
| 50 step Base는 얼굴을 만들지만 전신 조건에서는 identity·outfit이 이탈 | step만 늘리면 캐릭터가 고정된다는 해석 | 얼굴·착장·구조 조건의 역할을 분리 |
| OpenPose는 팔·다리의 2D 배치를 따르게 함 | OpenPose가 카메라 회전까지 결정한다는 해석 | 고각도 camera는 별도 guide로 제공 |
| depth·Canny는 원근 또는 실루엣을 남기지만 재킷·가방이 빠짐 | 구조 조건을 강하게 주면 복장도 따라온다는 해석 | 완성 착장을 독립 reference로 유지 |
| mask·VTON은 수평 레이어를 부분 보정 | 국소 편집이 새 3D 가림 관계를 만들 수 있다는 해석 | 전신 계약이 맞는 생성 단계로 되돌아감 |

이 표가 중요한 이유는 “어떤 모델이 좋았는가”보다, 실패를 다음 조건의 역할로 번역했기 때문이다. 이 번역이 없으면 adapter·step·mask를 계속 누적하는 실험이 되지만, 역할을 분리하면 어느 입력을 바꿔야 하는지 다시 판단할 수 있다.

## 보조 실험 D. 국소 보정은 새 카메라의 3D 관계를 만들지 못했다

> **이 보조 실험이 확인한 것:** mask·VTON은 이미 성립한 수평 레이어를 부분 보정할 수 있어도, 고각도에서 새로 보이거나 가려지는 전신 관계를 재구성하지는 못한다.

고각도에서 문제를 국소 영역만 고쳐 해결할 수 있는지도 확인했다. 자동 DiffEdit mask는 머리와 신발까지 퍼져 재킷만 고치지 못했다. FitDiT에는 고각도 원본의 카메라·자세·하체를 고정하고 상반신만 감싼 좁은 mask와 완성 착장을 주었지만, 재킷은 회색 덩어리와 짧은 흰 앞면으로 바뀌고 가방·strap이 사라졌다. CatVTON은 수평 전면에서 재킷 레이어를 부분적으로 전달했지만, 고각도 전신을 다시 구성하는 증거는 아니었다.

| DiffEdit 자동 mask | FitDiT 고각도 상반신 | CatVTON 수평 재킷 |
| --- | --- | --- |
| ![DiffEdit 자동 mask 실패](../../../assets/part-07/chapter-05/p7-5-4-diffedit-first-probe-contact-sheet.png) | ![FitDiT 고각도 상반신 착장 교체](../../../assets/part-07/chapter-05/p7-5-4-fitdit-high-angle-upperbody-complete-outfit-review-sheet.png) | ![CatVTON 전면 재킷 비교](../../../assets/part-07/chapter-05/p7-5-4-catvton-jacket-contact-sheet.png) |
| 편집 범위가 전신으로 확산 | 어깨·재킷·가방의 새 가림 관계 미통과 | 수평 재킷 레이어만 부분 통과 |

이 결과는 mask를 더 정교하게 그리거나 reference를 더 주는 일이 고각도에서 새로 보이거나 가려지는 팔·몸통·다리·가방의 관계를 대신하지 못한다는 뜻이다. [FitDiT 실행 기록](../../../assets/part-07/chapter-05/p7-5-4-fitdit-high-angle-upperbody-complete-outfit-run.json)과 [SDXL depth 역할 분리 기록](../../../assets/part-07/chapter-05/p7-5-4-sdxl-depth-role-separated-run.json)은 각 조건을 남긴다.

## 주요 서사 3. Qwen에서는 세 입력의 역할을 분리해 통과 경로를 만들었다

앞선 결과는 한 입력에 카메라·얼굴·완성 착장을 함께 맡기지 말아야 한다는 결론으로 모였다. Qwen-Image-Edit-2509에서는 세 입력의 역할을 분리했다.

| 입력 | 맡긴 정보 |
| --- | --- |
| image 1 | 지붕, 고각도 카메라, 보행 배치 |
| image 2 | 정면 얼굴 identity |
| image 3 | 재킷·바지·신발·가방을 포함한 완성 착장 |

처음의 2입력은 재킷·가방을 잃었고, 역할을 충분히 분리하지 않은 3입력은 분홍 신발·좁은 바지를 만들었다. 이것이 복장 입력을 별도 역할로 고정한 이유다.

| 2입력: 착장·가방 누락 | 역할 미분리 3입력: 신발·바지 드리프트 |
| --- | --- |
| ![Qwen 2입력 고각도 결과](../../../assets/part-07/chapter-05/p7-5-4-qwen-edit-two-input-outfit-loss.png) | ![Qwen 역할 미분리 3입력 결과](../../../assets/part-07/chapter-05/p7-5-4-qwen-edit-three-input-uncompressed-outfit-drift.png) |
| 재킷·가방·strap 미통과 | 흰 운동화·와이드 바지 미통과 |

Nunchaku FP4 r128과 per-layer CPU offload에서 `768×1152`, 40 step으로 실행한 역할 분리 조건은 GPU 약 `3.5–3.7 GiB`, 장당 약 16분 32초가 걸렸다. seed `62294/62295` 두 후보 모두 고각도 투영, 보행, 얼굴, 재킷·바지·신발·가방과 재킷 바깥 strap을 함께 유지했다.

| seed `62294` | seed `62295` |
| --- | --- |
| ![Qwen 역할 분리 고각도 후보 seed 62294](../../../assets/part-07/chapter-05/p7-5-4-qwen-edit-high-angle-seed-62294-reference.png) | ![Qwen 역할 분리 고각도 후보 seed 62295](../../../assets/part-07/chapter-05/p7-5-4-qwen-edit-high-angle-seed-62295-reference.png) |
| 네 계약 통과 | 같은 입력 역할에서 교차 seed 통과 |

따라서 고정한 보행 guide 범위에서는 **구조용 guide로 카메라·행동·배경을 정하고, 얼굴과 완성 착장을 역할별 reference로 분리하는 경로**가 8 GB에서도 기본적인 컷신 구성과 캐릭터 재현을 가능하게 했다. 다른 pose·guide·후면·강한 가림에는 같은 역할 분리를 유지한 새 후보와 사람 검수가 필요하다. 이 두 결과는 P7-5.3 스토리보드를 자동으로 교체하거나 LoRA 학습 데이터로 승격하지 않는다.

### 보조 실험의 입력 연결

OpenPose와 depth·Canny는 구조 조건, FaceID·FacePlus·IP-Adapter·LoRA는 캐릭터 조건, mask·VTON은 생성 뒤 국소 보정으로 분리했다. 아래 도식은 보조 실험에서 이 조건들이 만나는 위치만 보여 준다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-4-supporting-pipeline-ko.mmd"
```

## 출처와 참고 자료

- Qwen Team, [Qwen-Image-Edit-2509](https://github.com/QwenLM/Qwen-Image/blob/main/Qwen-Image-Edit-2509.md){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. 1–3 입력 이미지 편집 범위를 확인했다.
- Nunchaku, [Qwen-Image-Edit-2509 실행 예제](https://github.com/nunchaku-ai/nunchaku/blob/main/examples/v1/qwen-image-edit-2509.py){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. FP4 transformer와 offload 기반 로컬 실행 경로를 확인했다.
- Zhang et al., [ControlNet](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. 구조 조건의 기본 역할을 참고했다.
- Tencent AI Lab, [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. 이미지 참조 조건의 기본 역할을 참고했다.
- Hugging Face, [Diffusers inpainting guide](https://huggingface.co/docs/diffusers/en/using-diffusers/inpaint){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. mask 기반 국소 편집의 동작 범위를 참고했다.
