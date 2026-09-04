# P7-5.13 OpenPose 맵으로 캐릭터 동작과 구도 변경을 시험하기

> Section ID: `P7-5.13`
> Version: `v2026.09.05`

캐릭터의 팔·다리 배치와 카메라 구도를 한 번에 바꿀 수 있을까? 이 절에서는 OpenPose map을 **캐릭터를 다시 그리는 reference가 아니라 2D 관절 배치용 구조 입력**으로 한정해 검증한다. 동작, 카메라 원근, 얼굴 identity, 착장 레이어는 서로 다른 정보를 담으므로 한 입력이 나머지 계약까지 보장한다고 읽지 않는다.

| 확인할 계약 | OpenPose map만으로 판정할 수 있는가? |
| --- | --- |
| structure | 팔·다리·접지의 2D 배치는 일부 확인할 수 있다. 카메라 원근·앞뒤 가림은 별도 guide가 필요하다. |
| identity | 아니다. 얼굴·헤어는 별도 reference와 사람 검수가 필요하다. |
| outfit | 아니다. 재킷·바지·가방의 형태와 겹침은 별도 조건이다. |
| style | 아니다. map은 선화·색·질감을 전달하지 않는다. |

!!! abstract "실험 결론"

    OpenPose와 ControlNet은 팔·다리·접지의 2D 배치를 보조했다. 그러나 high-angle 문구나 map만으로는 위에서 내려다보는 원근, 머리·흉곽의 회전, 가방의 앞뒤 가림을 결정하지 못했다. 익명 고각도 guide와 OpenPose·배경 Canny를 분리해도 현재 8 GB SDXL 경로에서는 동작·구도·identity·outfit을 함께 유지하지 못했다. 따라서 이 절의 map은 인체 동작과 2D 배치 확인에만 쓰며, 최종 캐릭터 컷의 단일 제어 수단으로 사용하지 않는다.

## 실험 흐름: 동작과 구도 조건을 분리한다

아래 흐름은 OpenPose가 맡을 수 있는 정보와 맡을 수 없는 정보를 구분한 순서다. 최종 이미지가 한 번 그럴듯해도, 각 조건이 실제로 전달한 정보를 따로 확인한다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-11-experiment-decision-flow-ko.mmd"
```

## 전신 조건에서 OpenPose off/on을 먼저 비교했다

FaceID와 전신 착장 image adapter를 빼고 Plus Face `0.15`, character LoRA `0.30`, seed `62295`, CFG `5.0`, `960×1440`, 50 step을 고정해 OpenPose off/on을 비교했다. OpenPose를 켜면 다리·몸통의 2D 배치는 더 따랐지만, 머리 길이와 복장이 이탈했다. off도 얼굴 윤곽과 전신은 만들었으나 기준 재킷·바지·가방은 유지하지 못했다.

![SDXL 전신 safe-face 조건의 OpenPose off/on 비교](../../../assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-openpose-ab-contact-sheet.png)

![SDXL safe-face 전신 후보와 기준 얼굴 비교](../../../assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-contact-sheet.png)

이 비교에서는 “얼굴이 그럴듯한가”만 보지 않는다. OpenPose on/off 시트에서는 다리·몸통의 배치가 map에 가까워졌는지를, 얼굴 기준 비교에서는 그 과정에서 청록 단발·기준 재킷·와이드 바지·가방이 같은 캐릭터 계약으로 남았는지를 따로 본다. 구조 단서가 좋아진 한 후보를 전체 재현의 근거로 읽지 않는 이유다.

저해상도 `512×768`에서 50/100 step도 비교했다. step을 늘려도 identity·outfit이 자동으로 기준에 수렴하지 않았다. step과 해상도는 얼굴·구조 형성의 조건일 수 있지만, 캐릭터 고정이나 복장 가림 관계를 대신하지 않는다.

[p7-5-11-sdxl-safe-face-without-openpose-960x1440-result.json — JSON — OpenPose off 실행 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-without-openpose-960x1440-result.json)

[p7-5-11-sdxl-safe-face-with-openpose-960x1440-result.json — JSON — OpenPose on 실행 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-with-openpose-960x1440-result.json)

얼굴 조건을 더 강하게 넣어도 전신 계약이 따라오지는 않았다. FaceID 단독은 전신 frame을 남겼지만 검은 장발·다른 착장으로 바뀌었고, FullFace 결합은 청록 단발·호박색 눈 단서를 늘렸지만 흉상 구도로 수렴했다.

| FaceID 단독 | FaceID + FullFace |
| --- | --- |
| ![FaceID 단독 후보](../../../assets/part-07/chapter-05/p7-5-11-faceid-only-candidate.png) | ![FaceID와 FullFace 결합 후보](../../../assets/part-07/chapter-05/p7-5-11-faceid-fullface-candidate.png) |
| 전신 frame 일부 유지, identity·outfit 이탈 | 얼굴 단서는 일부 회복, 전신·outfit 이탈 |

왼쪽 후보는 전신 구도를 남겼지만 얼굴과 착장이 기준에서 벗어나고, 오른쪽 후보는 얼굴 단서를 늘리는 대신 흉상으로 좁아진다. 얼굴 reference의 강도를 올리는 일이 전신 구도·복장을 보존하는 조건과 독립적이지 않다는 관찰이다.

## OpenPose는 2D 관절 배치까지만 전달했다

> **이 보조 실험이 확인한 것:** OpenPose는 팔·다리·접지의 2D 배치를 전달하지만, 고각도 카메라와 3D 가림 관계를 결정하지는 않는다.

P7-5.3 전신에서 저장한 우측 쿼터 skeleton map을 재사용해 detector를 매번 다시 실행하지 않도록 했다. 아래 비교는 왼쪽의 입력 map과 그 map을 사용한 ControlNet off/on 산출물을 함께 보여 준다.

![저장 우측 쿼터 OpenPose map과 ControlNet off/on 산출물](../../../assets/part-07/chapter-05/p7-5-11-openpose-static-quarter-right-contact-sheet.png)

검수 시트의 왼쪽은 입력 map, 가운데는 ControlNet off, 오른쪽은 `1.0` 조건이다. 오른쪽 후보의 다리·발 배치가 map 쪽으로 더 가까워진 것이 이 실험에서 확인할 수 있는 효과다. 반면 map에는 카메라의 위치, 머리와 흉곽의 회전, 가방이 몸의 앞·뒤 어느 쪽을 지나야 하는지가 들어 있지 않다.

Animagine XL `960×1440`, 30 step에서 LoRA `0.6`을 고정했을 때, 저장 우측 쿼터 map의 ControlNet `1.0`은 `0.0`보다 다리·발의 2D 배치를 더 잘 따르면서 단발·눈·재킷·와이드 바지·가방을 일부 남겼다. 선언형 오른팔 올리기 map에서도 `1.0`은 팔의 방향을 따라갔다. 반면 LoRA를 `0.8`로 올리면 바지가 거의 흰색이 되고, high-angle 문구를 보태도 위에서 내려다보는 원근은 생기지 않았다.

| 동작 guide off/on | LoRA `0.6/0.8` |
| --- | --- |
| ![선언형 OpenPose map ControlNet off/on](../../../assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-controlnet-ab-contact-sheet.png) | ![선언형 OpenPose map LoRA scale 비교](../../../assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-lora-scale-ab-contact-sheet.png) |
| 팔의 2D 구조는 map에 맞춰짐 | scale 상승은 색 계약의 해법이 아님 |

![선언형 OpenPose map에서 카메라 문구를 바꾼 비교](../../../assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-camera-ab-contact-sheet.png)

동작 시트는 같은 팔 방향을 요구할 때 ControlNet이 팔의 2D 방향을 어느 정도 따르게 하는지, LoRA scale 시트는 강도를 높인다고 의상 색이 자동으로 안정되지는 않는지를 보여 준다. 마지막 시트는 high-angle 문구만 추가해도 시점 원근이 바뀌지 않는 경우다.

[p7-5-11-openpose-static-quarter-right-report.json — JSON — 저장 map 비교 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-openpose-static-quarter-right-report.json)

[p7-5-11-openpose-declarative-reach-up-controlnet-ab-report.json — JSON — 동작 OpenPose off/on 비교 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-controlnet-ab-report.json)

[p7-5-11-openpose-declarative-reach-up-lora-scale-ab-report.json — JSON — LoRA scale 비교 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-lora-scale-ab-report.json)

[p7-5-11-openpose-declarative-reach-up-camera-ab-report.json — JSON — 카메라 문구 비교 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-camera-ab-report.json)

## 고각도 guide와 캐릭터 전이는 따로 검증해야 했다

고각도 스토리보드 자체가 병목은 아니었다. 캐릭터 정보가 없는 익명 인물로 지붕·원근·보행 배치만 가진 초안을 만들 수 있었다. 이 실험에서는 Animagine으로 고각도 스토리보드를 만들고, 그 결과를 카메라와 동작을 분리한 구조용 guide로 사용했다. 이 용도는 Animagine의 일반적 역할이나 최종 캐릭터 생성 가능성을 규정하지 않는다.

![익명 인물로 만든 고각도 보행 guide](../../../assets/part-07/chapter-05/p7-5-11-experimental-animagine-high-angle-guide.png)

### SDXL에서는 구조 조건을 나눠도 네 계약을 합치지 못했다

> **이 보조 실험이 확인한 것:** 인물 외곽을 뺀 background Canny와 OpenPose는 분리할 수 있지만, 현 8 GB SDXL 경로는 고각도·동작·identity·outfit을 함께 유지하지 못했다.

guide의 인물 RGB·얼굴·복장은 버리고, OpenPose와 **인물을 제외한 배경 Canny**만 SDXL에 전달했다. SDXL Base 1.0, character LoRA `0.6`, seed `62431`, 50 step, `768×1152`에서 구조 조건을 하나씩 켠 비교다.

![익명 guide·OpenPose·인물 제외 배경 Canny와 SDXL Mira 전이 후보](../../../assets/part-07/chapter-05/p7-5-11-sdxl-anonymous-high-angle-transfer-review-sheet.png)

익명 guide는 최종 캐릭터 reference가 아니다. 원본 guide의 인물 RGB·얼굴·복장을 버린 뒤, 몸의 2D 배치와 사람을 뺀 배경의 원근 단서만 각각 전달했을 때를 비교한다.

구조 조건이 없으면 high-angle이 사라졌다. OpenPose만 켜면 위쪽 카메라의 단서는 일부 남아도 달리기 동작이 앉거나 쪼그린 자세로 바뀌었다. 배경 Canny만 켜면 타일 원근은 남지만 인물 실루엣이 중복되었다. 두 ControlNet을 함께 쓰는 조건은 `768×1152`와 `512×768` 모두 현재 8 GB sequential-offload Diffusers 경로에서 완료되지 않았다. 사람 외곽을 뺀 background Canny와 pose/camera 입력 분리는 유효한 체크포인트였지만, 이 SDXL 경로는 고각도·동작·Mira identity·복장을 함께 재현하는 제작 도구로 사용하지 않는다.

[p7-5-11-sdxl-anonymous-high-angle-transfer-result.json — JSON — 익명 고각도 전이 실행 결과 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-anonymous-high-angle-transfer-result.json)

[p7-5-11-sdxl-anonymous-high-angle-transfer-report.json — JSON — 익명 고각도 전이 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-anonymous-high-angle-transfer-report.json)

### depth·Canny는 원근을 남겨도 기준 복장을 보장하지 않았다

depth와 역할 분리 adapter도 같은 경계를 보였다. 고각도 depth scaffold, 전신 완성 착장 global 조건, 얼굴 face 조건, character·outfit LoRA를 나눠 연결하면 타일 바닥 원근과 머리·눈 단서는 일부 남았다. 그러나 흰 크롭 재킷은 짧은 흰 상의가 되고 가방·strap은 사라졌다.

![SDXL depth와 역할 분리 adapter의 고각도 결과](../../../assets/part-07/chapter-05/p7-5-11-sdxl-depth-role-separated-review-sheet.png)

[p7-5-11-sdxl-depth-role-separated-result.json — JSON — SDXL depth 역할 분리 실행 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-depth-role-separated-result.json)

Canny도 카메라·실루엣의 보조 조건으로는 쓸 수 있었지만, 최근 사선 보행 후보에서는 얼굴·바지·가방 일부가 남는 대신 흰 재킷 레이어가 빠졌다. 구조를 더 강하게 전달하는 일과 기준 복장을 보존하는 일은 여전히 경쟁했다.

![Canny camera 조건의 사선 보행 비교](../../../assets/part-07/chapter-05/p7-5-11-canny-camera-condition-contact-sheet.png)

두 시트는 depth나 Canny가 쓸모없다는 판정이 아니다. depth 시트는 바닥 원근과 얼굴 단서가 남아도 재킷·가방의 겹침까지 보장하지 않는 사례이고, Canny 시트는 사선 camera와 실루엣을 보조해도 의상 레이어를 독립적으로 지켜 주지 않는 사례다. 따라서 구조 조건을 더 세게 누적하기보다, 최종 캐릭터 생성에서는 얼굴과 완성 착장을 독립 reference로 유지해야 했다.

### 보조 조건의 결합은 보조 실험 안에 한정됐다

OpenPose와 depth·Canny는 구조 조건, FaceID·FacePlus·IP-Adapter·LoRA는 캐릭터 조건, mask·VTON은 생성 뒤 국소 보정으로 분리했다. 아래 도식은 **SDXL·Animagine 보조 실험에서만** 이 조건들이 만나는 위치를 보여 준다. Qwen의 세 입력 경로에는 이 adapter·ControlNet·mask·VTON 조건을 연결하지 않았다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-11-supporting-pipeline-ko.mmd"
```

## 결과를 다음 입력 역할로 번역한다

| 관찰한 결과 | 피한 해석 | 다음 선택 |
| --- | --- | --- |
| OpenPose는 팔·다리의 2D 배치를 따르게 함 | OpenPose가 카메라 회전까지 결정한다는 해석 | 카메라 구도는 별도 guide로 제공 |
| depth·Canny는 원근 또는 실루엣을 남기지만 재킷·가방이 빠짐 | 구조 조건을 강하게 주면 복장도 따라온다는 해석 | 얼굴·완성 착장을 독립 reference로 유지 |
| 두 ControlNet 결합은 8 GB 경로에서 완료되지 않음 | 조건을 더 누적하면 네 계약을 합칠 수 있다는 해석 | 완료한 단일 조건 관찰과 최종 reference 편집을 구분 |

이 표의 목적은 “어떤 모델이 좋았는가”를 정하는 일이 아니라, 실패를 다음 입력의 역할로 번역하는 데 있다. 동작·구도·identity·outfit은 서로를 대체하지 않는다.

## 체크리스트

- OpenPose off/on 비교에서 달라진 부분을 하나 고르고, 그것이 structure·identity·outfit·style 중 어느 계약인지 적는다. 다른 세 계약은 결과 이미지에서 따로 판정한다.
- 선언형 동작 map의 off/on과 LoRA scale 비교를 읽고, 2D 팔 방향의 변화와 의상 색 이탈을 같은 성공으로 세지 않는다.
- 고각도 guide 비교에서 OpenPose, background Canny, depth가 각각 남긴 단서를 적고, 카메라 원근·동작·복장이 한 조건으로 고정되었다고 일반화하지 않는다.

## 출처와 참고 자료

- Stability AI, [SDXL Generative Models](https://github.com/Stability-AI/generative-models){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. SDXL Base 1.0의 기준 모델을 확인했다.
- Cagliostro Research Lab, [Animagine XL 4.0 model card](https://huggingface.co/cagliostrolab/animagine-xl-4.0){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. guide와 LoRA 비교에 쓴 SDXL 계열 모델의 실행·제한 정보를 확인했다.
- Cao et al., [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. 2D 신체 keypoint map의 출발점을 확인했다.
- Hu et al., [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. low-rank adapter의 기본 개념을 확인했다.
- cubiq, [ComfyUI InstantID](https://github.com/cubiq/ComfyUI_InstantID){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. FaceID·얼굴 reference 조건의 실행 경계를 확인했다.
- Zhang et al., [ControlNet](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. 구조 조건의 기본 역할을 참고했다.
- Tencent AI Lab, [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. 이미지 참조 조건의 기본 역할을 참고했다.
