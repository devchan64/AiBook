# P7-5.5 스토리보드 장면에 캐릭터를 합성하는 경로

> Section ID: `P7-5.5`
> Version: `v2026.09.08`

이 절은 [P7-5.4](section-04.md)의 마지막 단계에서 주변 인물과 동물까지 추가한 A·B·C를 입력으로 이어받는다. 장면의 구도와 Mira의 외형이 이미 반영된 상태에서, 수정할 인물 영역과 보존할 주변 대상을 구분하고 캐릭터·배경·조명을 단계별로 편집하는 것이 중심이다. 별도의 그림자 추가 단계는 두지 않는다. 각 후속 결과의 `result.json`에는 실제 입력 파일, SHA-256과 실행 조건을 남겨 입력 장면과 출력의 관계를 확인한다.

## P7-5.4의 최종 장면을 입력으로 고정한다

세 입력은 모두 1280×1280이다. A는 주변 인물을 추가한 `extras-v5`, B는 토끼와 다람쥐를 추가한 `extras-v8`, C는 새 세 마리를 배치한 `extras-v7`을 사용한다. 원본 자산을 P7-5.5용으로 복제하지 않고 P7-5.4의 파일을 직접 참조한다.

![Scene A 입력: 도시 거리에서 달리는 Mira와 주변 인물](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-extras-v5-size-1280x1280-seed-5420-steps-20.png)

[Scene A 입력 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-extras-v5-size-1280x1280-seed-5420-steps-20-result.json){ .lazy-source }

![Scene B 입력: 숲 공터에서 도약하는 Mira와 토끼·다람쥐](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-extras-v8-size-1280x1280-seed-5421-steps-20.png)

[Scene B 입력 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-extras-v8-size-1280x1280-seed-5421-steps-20-result.json){ .lazy-source }

![Scene C 입력: 언덕에서 책을 읽는 두 인물과 앉아 있는 새 세 마리](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-extras-v7-size-1280x1280-seed-5422-steps-20.png)

[Scene C 입력 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-extras-v7-size-1280x1280-seed-5422-steps-20-result.json){ .lazy-source }

## 편집할 인물과 보존할 대상을 나눈다

| 장면 | 인물 마스크·컷아웃 대상 | 인물 편집에서 보존할 주변 대상 |
| --- | --- | --- |
| A | 화면 중앙에서 달리는 Mira | 주변 인물 여섯 명, 도로와 건물 |
| B | 공중에서 도약하는 Mira | 왼쪽 아래 토끼, 오른쪽 나무 밑 다람쥐, 나무와 양치식물 |
| C | 왼쪽 Mira와 오른쪽 조연을 각각 별도 마스크로 분리 | 각 마스크에서 다른 인물, 책, 새 세 마리, 난간과 도시 배경 |

A와 C에는 여러 인물이 있으므로 `a person` 검출 결과를 그대로 모두 합치지 않고 Mira에 해당하는 상자와 마스크를 확인해야 한다. C에서는 손과 책이 겹치는 경계도 확인한다. Mira를 제거한 배경판을 만들 때도 주변 인물·동물까지 함께 지워서는 안 된다.

후속 편집은 `입력 장면 → 인물별 마스크·컷아웃 → 필요한 캐릭터 보정 → 배경판과 통합 → 조명 조정`으로 구성한다. 컷아웃은 포즈·인물 크기·프레이밍을 전달하며, 얼굴·착장을 보정할 때만 해당 참조를 추가한다. 기존 Mira의 외형을 그대로 사용할 경우 같은 아이덴티티를 다시 이식할 필요는 없다. 그림자는 별도 생성 단계로 추가하지 않고, 입력 장면에 있는 그림자와 편집 결과의 변화를 비교한다.

## Mira와 조연을 각각 분리한다

먼저 장면에서 어느 인물을 분리할지 지정한다. 로컬 GPU에서 Grounding DINO Tiny로 인물 상자를 찾고 SAM 2.1 Hiera Small로 마스크를 만들었다. 여기서 마스크는 복사할 인물 픽셀을 흰색, 제외할 영역을 검은색으로 표시한 이미지다. 모델이 Mira라는 이름을 알아본 것은 아니다. 청록색 머리와 위치를 눈으로 확인한 뒤 대상 좌표를 지정했으며, 겹친 영역은 상자·포함점·제외점과 제외 영역으로 보정했다. [Grounding DINO 모델 카드](https://huggingface.co/IDEA-Research/grounding-dino-tiny){: target="_blank" rel="noopener noreferrer"} · [SAM 2.1 모델 카드](https://huggingface.co/facebook/sam2.1-hiera-small){: target="_blank" rel="noopener noreferrer"}

A에서는 화면 앞으로 크게 나온 신발 끝까지 포함하고 배경의 달리는 사람은 제외했다. B에서는 도약하는 Mira만 선택하고 토끼와 다람쥐를 제외했다. C에서는 Mira와 조연을 따로 선택했다. 조연은 Mira에 가려 상체와 하체가 떨어져 보이므로, 가장 큰 덩어리 하나만 남기면 상체가 사라질 수 있다. 이번에는 포함점이 놓인 여러 덩어리를 함께 유지했다.

아래 흰 배경 컷아웃은 분리 영역을 확인하는 이미지다. 함께 저장한 투명 PNG는 같은 마스크를 알파 채널로 사용한다. 네 파일 모두 원본과 같은 1280×1280 캔버스와 인물 위치를 유지하며, 선택된 픽셀의 색을 원본에서 그대로 복사했다.

### Scene A Mira

![Scene A Mira의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-a-mira-extras-v5-v1.png)

[Scene A Mira 투명 PNG](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-a-mira-extras-v5-v1-rgba.png) · [마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-a-mira-extras-v5-v2.png) · [마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-a-mira-extras-v5-v2-overlay.png)

[마스크 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-a-mira-extras-v5-v2-result.json){ .lazy-source } · [컷아웃 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-a-mira-extras-v5-v1-result.json){ .lazy-source }

### Scene B Mira

![Scene B Mira의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-b-mira-extras-v8-v1.png)

[Scene B Mira 투명 PNG](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-b-mira-extras-v8-v1-rgba.png) · [마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-b-mira-extras-v8-v1.png) · [마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-b-mira-extras-v8-v1-overlay.png)

[마스크 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-b-mira-extras-v8-v1-result.json){ .lazy-source } · [컷아웃 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-b-mira-extras-v8-v1-result.json){ .lazy-source }

### Scene C Mira

![Scene C Mira의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-mira-extras-v7-v1.png)

[Scene C Mira 투명 PNG](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-mira-extras-v7-v1-rgba.png) · [마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-mira-extras-v7-v4.png) · [마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-mira-extras-v7-v4-overlay.png)

[마스크 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-mira-extras-v7-v4-result.json){ .lazy-source } · [컷아웃 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-mira-extras-v7-v1-result.json){ .lazy-source }

### Scene C 조연

![Scene C 조연의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-supporting-extras-v7-v4.png)

[Scene C 조연 투명 PNG](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-supporting-extras-v7-v4-rgba.png) · [마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-supporting-extras-v7-v7.png) · [마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-supporting-extras-v7-v7-overlay.png)

[마스크 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-supporting-extras-v7-v7-result.json){ .lazy-source } · [컷아웃 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-supporting-extras-v7-v4-result.json){ .lazy-source }

### 분리 결과의 한계와 재현

C의 빈 부분은 다른 인물·책·새에 가려져 원본에 보이지 않는 영역을 포함한다. 이번 작업은 보이는 픽셀을 분리한 것이며, 가려진 신체를 새로 그리지 않았다. 손과 책, 머리카락과 배경이 맞닿는 경계에는 일부 거친 가장자리와 미세 누락이 남아 있다. 다른 배경에 옮길 때는 이 경계를 다시 확인해야 한다. 두 C 마스크 사이의 중복 픽셀은 없으며, 네 투명 PNG의 알파 채널이 해당 마스크와 일치하는지 확인했다.

[인물별 입력·선택 조건과 재현 명령](../../../assets/part-07/chapter-05/p7-5-5-character-separation-v1-result.json){ .lazy-source }에 네 실행을 모았다. 저장소 루트에서 마스크 명령을 실행한 뒤 컷아웃 명령을 실행한다. 기존 출력 덮어쓰기를 막으므로 다시 실행할 때는 새 실행 이름 또는 출력 디렉터리를 지정한다. 검출·분할 모델은 로컬 캐시에 있어야 하며 CUDA를 사용한다. 컷아웃 저장은 이미지 픽셀을 복사하는 처리다.

[인물 마스크 생성 코드](../../../assets/part-07/chapter-05/p7_5_5_generate_person_mask.py) · [흰 배경·투명 컷아웃 생성 코드](../../../assets/part-07/chapter-05/p7_5_5_extract_pose_cutout.py)

## B의 포즈를 남긴 마네킨에 Mira를 다시 적용한다

착장 일부를 반복해서 보정하면 앞 단계의 형태가 남거나 옷 주름이 단순해질 수 있다. B에서는 기존 얼굴·착장의 영향을 줄여 볼 목적으로, 원본 컷아웃을 짧은 스포츠머리와 스포츠 브라·짧은 하의를 입은 성인 여성으로 바꾼 뒤 Mira 참조를 적용했다. 여기서 마네킨은 얼굴이 없는 회색 모형이 아니라, 얼굴과 팔다리 자세가 보이는 생성 이미지다. `B 원본 컷아웃 → 20스텝 마네킨 → 5.3 착장 참조를 사용한 30스텝 인물 교체`로 이어지며, 조명 보정을 거치지 않고 원본 컷아웃에서 시작했다.

![B 원본 컷아웃에서 만든 얼굴 있는 20스텝 마네킨](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-scene-b-pose-person-v1-size-1280x1280-seed-62294-steps-20.png)

[마네킨 입력·생성 지시·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-scene-b-pose-person-v1-size-1280x1280-seed-62294-steps-20-result.json){ .lazy-source }

Picture 1에는 위 마네킨을, Picture 2에는 [P7-5.3의 최종 전신 착장 이미지](../../../assets/part-07/chapter-05/p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png)를 넣었다. 얼굴 전용 head 파일은 이번 실행의 참조가 아니다. 머리색이나 의복 형태를 텍스트로 덧붙이지 않고 다음 두 문장을 사용했다.

> Replace the woman in Picture 1 with the woman in Picture 2, preserving the pose. Preserve the split-leap pose and the cast shadow beneath the woman.

이 지시는 1번 여성의 자세를 유지하면서 2번 여성으로 교체하고, 다리를 벌린 도약 자세와 인물 아래 그림자를 보존하라는 뜻이다. 마지막 그림자 문장은 그림자가 있던 이전 실험의 표현을 그대로 비교한 조건이다. 이번 마네킨에는 바닥 그림자가 없으므로, 지시와 입력이 일치하는지도 결과에서 확인해야 한다.

![B 마네킨에 Mira 전신 착장을 참조한 30스텝 결과: 단발과 재킷·넓은 바지는 반영됐으나 맨발이 남고 그림자가 추가됨](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-scene-b-pose-person-face-hair-v5-outfit-size-1280x1280-seed-62294-steps-30.png)

[v5-outfit 입력 순서·프롬프트·설정·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-scene-b-pose-person-face-hair-v5-outfit-size-1280x1280-seed-62294-steps-30-result.json){ .lazy-source }

청록색 단발, 흰 재킷과 넓은 바지가 반영됐고 다리를 벌린 도약 자세도 대체로 남았다. 그러나 참조의 운동화는 적용되지 않아 양쪽 발이 맨발이며, 얼굴·팔다리 윤곽과 의복 세부도 입력 및 참조와 다르다. 마네킨에 없던 바닥 그림자까지 추가됐다. 이 결과는 인물 교체가 진행된 사례이며, 착장과 배경 보존까지 완료된 최종 합성 자산은 아니다. 특히 `보존`이라는 단어를 썼더라도 입력에 없는 대상을 언급하면 새 요소가 생길 수 있음을 이번 출력에서 관찰했다.

로컬 Qwen Image Edit 2511의 `QwenImageEditPlusPipeline`을 BF16과 sequential CPU offload로 실행했다. 출력은 1280×1280, 30스텝, seed `62294`, true CFG `4.0`이다. 1번 입력은 1280×1280, 2번은 960×1440의 비율을 유지해 전달했으며, 마스크·추가 LoRA·출력 합성은 사용하지 않았다. 두 입력과 출력의 SHA-256은 JSON 기록과 일치한다.

[마네킨·다중 참조 실험 생성기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_mannequin_identity.py)에서 이번 실행은 `pose-person-face-hair` 단계의 프롬프트를 전체 인물 교체로 바꾸고 `--face-reference`로 전신 착장을 지정했다. 파일명과 옵션에 `face`가 남아 있어도 실제 편집 범위는 위 프롬프트와 참조 파일로 판단한다. 저장소 루트에서 재실행하려면 다음처럼 새 출력 이름을 사용한다.

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_mannequin_identity.py \
  --stage pose-person-face-hair --run-label v5-outfit-repeat --steps 30 \
  --face-reference docs/assets/part-07/chapter-05/p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png
```

이 명령은 저장된 20스텝 마네킨에서 시작한다. 코드의 프롬프트가 이후 바뀌었다면 먼저 위 JSON의 문장과 대조한다. 이번 실행은 CUDA 난수 생성기를 사용하므로, 같은 seed를 CPU 난수 생성기에 전달한 이전 실행과 초기 노이즈가 같다고 보지 않는다.

아래 보충학습에는 이전 조명 보정의 후속 결과와 카메라판 합성 실험을 모았다. 현재 컷아웃·마네킨 경로와 입력이 다르므로 서로 이어진 출력으로 해석하지 않는다. 기존 후속 생성 코드의 기본 입력은 이전 실험을 가리킬 수 있으므로 실행 전에 입력을 확인한다.

## 보충학습: 이전 조명·합성 실험

C의 신발·화풍 보정은 현재 컷아웃에서 파생된 이전 조명 실험의 결과다. 그 뒤 카메라판 합성 실험의 Scene A·B·C는 각각 해안 절벽·야생화 초원·도심 공원의 이전 입력을 뜻한다. 그림자를 포함한 중간 산출물도 당시 입력 기록 그대로 남아 있지만, 그림자를 추가하는 절차와 실행 안내는 현재 경로에서 제외한다.

### 이전 C 실험의 신발과 조연 화풍 보정

다음 두 결과는 이전 조명 보정 실험의 중간 산출물을 입력으로 사용했다. 현재 컷아웃에서 바로 이어지는 보정 단계가 아니며, 각 JSON의 실제 입력을 기준으로 확인한다. C Mira의 신발은 P7-5.3 착장 참조를 사용하고, C 조연은 C Mira의 DeLight 결과에서 선과 절제된 채색 표현만 참조한다. 여자 캐릭터의 얼굴·머리·의상까지 조연에게 옮기는 작업은 아니다.

| 보정 항목 | Image 1: 편집 대상 | Image 2: 참조할 특징 |
| --- | --- | --- |
| C 신발 | C Mira DeLight 결과 | P7-5.3 2단계 착장 참조의 흰 로우탑 스니커즈 |
| C 조연 화풍 | C 조연 DeLight 결과 | C Mira DeLight 결과의 선·채색 표현 |

[추가 보정 생성기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_refine_delight.py)는 로컬 GPU의 Qwen Image Edit 2511에 두 이미지를 순서대로 넣는다. 두 작업은 각각의 DeLight 원본에서 시작한다. 새 그림자나 배경을 만드는 단계는 추가하지 않는다.

먼저 다음 명령으로 모델을 불러오지 않고 입력·참조·프롬프트·출력 경로를 확인한다. `--dry-run`을 빼면 지정한 두 보정을 실행한다. 기본값은 1280×1280, seed `62294`, 20 step, true CFG `4.0`이다.

~~~bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_refine_delight.py --tasks c-shoes c-supporting-style --dry-run
~~~

다른 결과를 이어받으려면 단일 작업에 `--input`을 지정한다. 단일 작업의 참조와 지시는 `--reference`, `--prompt`로 바꿀 수 있으며, 두 작업의 참조는 각각 `--mira-reference`, `--style-reference`로 바꾼다. 재실행에는 새 `--run-label`을 사용한다.

이 생성기의 기본 프롬프트는 해당 부위나 화풍만 수정하고 자세·얼굴·의상·배경을 보존하도록 지시한다. 마스크로 픽셀을 고정하는 방식은 아니므로 결과를 확인할 때는 수정한 항목과 수정하지 않은 부분을 함께 대조해야 한다. C의 가림 영역 복원과 DeLight에서 생긴 그림자 문제는 이 보정들로 해결됐다고 간주하지 않는다. 다음은 두 작업을 기본 조건으로 로컬 GPU에서 실행한 결과다. 각 JSON에는 실제 입력·참조의 SHA-256과 프롬프트를 기록했다.

#### C 신발 보정

![C 신발 보정 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-refine-c-shoes-v1-size-1280x1280-seed-62294-steps-20.png)

앉은 자세의 양쪽 회색 신발이 흰 끈 스니커즈로 바뀌었다. 청록 단발과 의상, 두 다리의 큰 배치는 유지됐다. 발목과 바지 밑단의 세부선에도 변화가 있고, 기존 왼쪽 아래 방향의 그림자는 남아 있다.

[입력·참조·프롬프트·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-refine-c-shoes-v1-size-1280x1280-seed-62294-steps-20-result.json){ .lazy-source }

#### C 조연 화풍 보정

![C 조연 화풍 보정 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-refine-c-supporting-style-v1-size-1280x1280-seed-62294-steps-20.png)

DeLight 결과의 입체적인 피부·옷 질감이 선과 평면적인 채색 중심의 표현으로 바뀌었다. 검은 머리, 회색 후드와 바지, 고개를 숙여 앉은 자세는 유지됐다. 얼굴·손·주름의 세부와 바닥 그림자도 달라졌으며, 앞 단계에서 채워진 몸통은 그대로 남아 있다.

[입력·참조·프롬프트·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-refine-c-supporting-style-v1-size-1280x1280-seed-62294-steps-20-result.json){ .lazy-source }

두 보정 결과는 1280×1280이다. C Mira는 `c-shoes`, C 조연은 `c-supporting-style`을 각각 구분해 사용한다. 추가 보정은 마스크 없이 Qwen Edit에 수정 대상과 보존할 내용을 지시한다. 수정 대상 외의 내용을 최대한 유지하는 것이 이 편집 방식의 목적이며, 결과에서는 해당 부위의 개선과 다른 부분의 보존을 함께 확인한다.

### 한 모델이 아니라 역할이 다른 구성 요소

이전 합성 실험의 결과는 하나의 이미지 모델에서 바로 나온 것이 아니다. 당시 카메라판에서 인물의 영역을 찾고, 포즈에 캐릭터를 이식하고, 배경판을 만들고, 둘을 통합하는 일을 분리했다. 같은 입력을 여러 모델에 반복해 넣기보다, 각 단계에 필요한 정보만 넘기는 것이 이 절의 핵심이다.

| 구성 요소 | 맡긴 일 | 이 절에서의 입력·출력 경계 |
| --- | --- | --- |
| `Qwen/Qwen-Image-Edit-2511` | 카메라판의 인물·배경판 편집과 DeLight 배경·캐릭터의 다중 참조 통합 | 카메라판·단일 인물 또는 배경판·캐릭터 → 장면 한 장 |
| Grounding DINO Tiny | `a woman`, `a person` 텍스트로 인물 상자 탐색 | 카메라판 → 인물 상자 |
| SAM 2.1 Hiera Small | 선택된 상자를 흰색 인물 마스크로 정밀화 | 인물 상자·카메라판 → 마스크 |
| `Qwen/Qwen-Image-Edit-2509` + Studio DeLight LoRA | 배경판 또는 통합 장면의 방향광 색조를 중립화 | 배경판 또는 방향광 장면 → 중립 광원 장면 |
| `Qwen/Qwen-Image-Edit-2509` + dx8152 Relight LoRA | 통합 장면의 방향광을 다시 부여 | 중립화된 통합 장면 → 방향광 장면 |

`Qwen-Image-Edit-2509`은 DeLight·리라이트처럼 한 장에서 조명을 편집하는 단계에 쓴다. Studio DeLight LoRA는 이미 생긴 방향광을 균일한 스튜디오 광원으로 중립화한다. `Qwen-Image-Edit-2511`은 카메라판에서 인물·배경을 편집하고 다중 참조를 통합한다. 당시 카메라판과 현재 P7-5.4 최종 장면은 서로 다른 입력이다. [Qwen-Image-Edit-2509 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2509){: target="_blank" rel="noopener noreferrer"} · [Qwen-Image-Edit-2511 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer"} · [Studio DeLight 모델 카드](https://huggingface.co/prithivMLmods/QIE-2511-Studio-DeLight){: target="_blank" rel="noopener noreferrer"}

마스크 단계의 Grounding DINO Tiny는 텍스트로 대상 상자를 찾는 zero-shot 객체 검출 모델이고, SAM 2.1 Hiera Small은 그 상자를 인물 외곽 마스크로 바꾼다. 두 구성 요소는 캐릭터를 생성하거나 화풍을 정하지 않고, 카메라판에서 **어느 픽셀을 인물로 읽고 보존할지** 정한다. 빈 배경판은 이후 Qwen Image Edit 2511이 카메라판 한 장을 직접 편집해 만든다. [Grounding DINO Tiny 모델 카드](https://huggingface.co/IDEA-Research/grounding-dino-tiny){: target="_blank" rel="noopener noreferrer"} · [SAM 2 공식 저장소](https://github.com/facebookresearch/sam2){: target="_blank" rel="noopener noreferrer"}

위 공개 모델 카드와 저장소의 기능·배포 정보는 2026-08-29에 확인했다. 실제 실행에 쓴 입력 순서와 seed·step은 각 단계의 `result.json`을 기준으로 확인한다.

### 카메라판에서 마스크와 컷아웃을 쓴다

마스크의 흰색은 인물, 검은색은 보존할 배경을 뜻한다. 오버레이에서는 빨간색으로 덮인 영역과 노란색 검출 상자를 함께 보므로, 머리·손가락·발끝 같은 전신 경계가 빠졌는지 컷아웃보다 먼저 확인할 수 있다.

| Scene A 마스크 오버레이 | Scene B 마스크 오버레이 | Scene C 마스크 오버레이 |
| --- | --- | --- |
| ![해안 절벽 아이레벨 카메라판의 전신 인물 마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-3-sam2-person-mask-official-camera-scene-a-v6-overlay.png) | ![야생화 초원 재생성 카메라판의 전신 인물 마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-official-camera-scene-b-v7-overlay.png) | ![거리 토큰 없는 도심 공원 카메라판의 전신 인물 마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-official-camera-scene-c-no-closeup-v9-overlay.png) |

| Scene A 포즈 컷아웃 | Scene B 포즈 컷아웃 | Scene C 포즈 컷아웃 |
| --- | --- | --- |
| ![해안 절벽 아이레벨 카메라판에서 추출한 흰 배경 스플릿 점프 포즈](../../../assets/part-07/chapter-05/p7-5-3-character-pose-cutout-white-official-camera-scene-a-v6.png) | ![야생화 초원 재생성 카메라판에서 추출한 흰 배경 스플릿 점프 포즈](../../../assets/part-07/chapter-05/p7-5-3-character-pose-cutout-white-official-camera-scene-b-v7.png) | ![거리 토큰 없는 도심 공원 카메라판에서 추출한 흰 배경 스플릿 포즈](../../../assets/part-07/chapter-05/p7-5-5-character-pose-cutout-white-official-camera-scene-c-no-closeup-v9-size-1280x1280.png) |

[Scene A mask result.json — JSON — 아이레벨 카메라판의 검출 상자와 SAM2 마스크 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-3-sam2-person-mask-official-camera-scene-a-v6-result.json)

[Scene A cutout result.json — JSON — 아이레벨 카메라판의 흰 배경 포즈 컷아웃 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-3-character-pose-cutout-white-official-camera-scene-a-v6-result.json)

[Scene B mask result.json — JSON — 재생성 카메라판의 검출 상자와 SAM2 마스크 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-sam2-person-mask-official-camera-scene-b-v7-result.json)

[Scene B cutout result.json — JSON — 재생성 카메라판의 흰 배경 포즈 컷아웃 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-3-character-pose-cutout-white-official-camera-scene-b-v7-result.json)

[Scene C mask result.json — JSON — 거리 토큰 없는 카메라판의 검출 상자와 SAM2 마스크 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-sam2-person-mask-official-camera-scene-c-no-closeup-v9-result.json)

[Scene C cutout result.json — JSON — 거리 토큰 없는 카메라판의 흰 배경 포즈 컷아웃 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-character-pose-cutout-white-official-camera-scene-c-no-closeup-v9-size-1280x1280-result.json)

세 마스크는 머리·양팔·양다리·발끝을 포함했다. 거리 토큰을 생략해 다시 만든 Scene C에서는 SAM2 마스크가 인물만 분리하고, 하단의 분리된 그림자는 배경으로 남겼다. 이처럼 마스크가 완벽하지 않을 때는 컷아웃을 캐릭터 identity의 기준으로 쓰지 않으며, 픽셀 단위 외곽이 필요한 단계에서만 그 경계를 정제한다.

[인물 마스크 생성 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_generate_person_mask.py)

[흰 배경 포즈 컷아웃 생성 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_extract_pose_cutout.py)

흰 배경 컷아웃은 포즈와 프레이밍을 전달하는 참조이며, 알파 채널을 보존하는 최종 합성 자산은 아니다. 인물 레이어 보관과 빈 배경판 생성은 같은 마스크를 활용하는 별도 작업이다.

#### 포즈에 측면 캐릭터 identity를 이식한 이전 결과

Scene B·C는 각각 그림자 포함 컷아웃을 `Picture 1`, P7-5.3의 2단계 착장 이미지를 `Picture 2`로 넣었다. `Picture 1`은 스플릿 점프·인물 크기·프레이밍·바닥 그림자를, `Picture 2`는 청록 단발·흰 크롭 재킷·회색 이너·청록 바지를 맡는다. 카메라 LoRA나 추가 포즈 설명은 넣지 않고, `Replace the woman in Picture 1 with the woman in Picture 2, preserving the pose.`와 그림자 보존 지시만 사용했다.

| Scene A 그림자 컷아웃 다중 참조 결과 | Scene B 그림자 컷아웃 다중 참조 결과 | Scene C 그림자 컷아웃 다중 참조 결과 |
| --- | --- | --- |
| ![그림자 포함 Scene A 스플릿 점프 포즈에 Stage 2 착장을 이식한 30 step 다중 참조 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-pose-identity-official-camera-scene-a-shadow-stage2-outfit-v2-size-1280x1280-seed-62294-steps-30.png) | ![그림자 포함 스플릿 점프 포즈에 Stage 2 착장의 청록 단발, 흰 크롭 재킷, 회색 이너와 청록 바지를 이식한 30 step 다중 참조 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-pose-identity-official-camera-scene-b-shadow-stage2-outfit-v1-size-1280x1280-seed-62294-steps-30.png) | ![거리 토큰 없는 Scene C 그림자 컷아웃과 Stage 2 착장을 다중 참조로 이식한 30 step 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-pose-identity-official-camera-scene-c-shadow-stage2-outfit-no-closeup-v2-size-1280x1280-seed-62294-steps-30.png) |

[Scene A 다중 참조 result.json — JSON — 그림자 컷아웃·Stage 2 착장의 입력 순서, 2511과 30 step 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-pose-identity-official-camera-scene-a-shadow-stage2-outfit-v2-size-1280x1280-seed-62294-steps-30-result.json)

[Scene B 다중 참조 result.json — JSON — 그림자 컷아웃·Stage 2 착장의 입력 순서, 2511과 30 step 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-pose-identity-official-camera-scene-b-shadow-stage2-outfit-v1-size-1280x1280-seed-62294-steps-30-result.json)

[Scene C 다중 참조 result.json — JSON — 거리 토큰 없는 그림자 컷아웃·Stage 2 착장의 입력 순서, 2511과 30 step 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-pose-identity-official-camera-scene-c-shadow-stage2-outfit-no-closeup-v2-size-1280x1280-seed-62294-steps-30-result.json)

1280×1280, seed `62294`, 30 step, true CFG `4.0`에서 공중 스플릿 점프와 그 아래 그림자는 유지됐고, 두 번째 참조의 재킷·회색 이너·청록 바지도 함께 반영됐다. 이전 실험에서는 역할을 나눈 두 이미지의 Qwen Image Edit 2511 다중 참조 이식을 사용했다. 착장 추출과 Try-On LoRA의 비교 실험은 P7-5.12에서 별도로 다룬다.

이전 결과의 입력 순서와 실행 조건은 위 JSON에 남아 있다. 아래 코드는 이전 실험의 재현용이며, 새 장면의 그림자 없는 컷아웃을 적용하려면 입력 선택과 그림자 보존 지시를 먼저 조정해야 한다.

[Qwen Image Edit 2511 다중 참조 이식 Python 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_pose_identity.py)

#### 컷아웃 캐릭터 identity에 Studio DeLight를 적용한다

직접 이식한 단일 인물은 배경과 합치기 전에 한 번 중립 광원으로 정리한다. Qwen Image Edit 2509와 Studio DeLight LoRA에 이 이미지 한 장만 넣고 모델 카드의 trigger prompt `Neutral uniform lighting Preserve identity and composition`을 사용했다. 이때 입력은 포즈·얼굴·헤어·재킷·이너·바지·신발을 모두 가진 인물 이미지이고, 해안 배경은 입력하지 않는다.

| Scene A DeLight 캐릭터 | Scene B DeLight 캐릭터 | Scene C DeLight 캐릭터 |
| --- | --- | --- |
| ![Studio DeLight로 중립 조명을 적용한 흰 크롭 재킷과 청록 바지의 공중 스플릿 점프 캐릭터](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-cutout-identity-v1-size-1280x1280-seed-62294-steps-10.png) | ![Studio DeLight로 중립 조명을 적용한 Scene B의 청록 단발, 흰 재킷과 청록 바지 스플릿 점프 캐릭터](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-b-size-1280x1280-seed-62294-steps-10.png) | ![Studio DeLight로 중립 조명을 적용한 Scene C의 Stage 2 착장 스플릿 점프 캐릭터](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-c-shadow-stage2-outfit-no-closeup-v3-size-1280x1280-seed-62294-steps-10.png) |

1280×1280, seed `62294`, 10 step, true CFG `4.0`에서 A·B·C는 포즈·얼굴 방향·헤어·재킷·이너·바지·신발을 유지했다. C는 거리 토큰 없는 그림자 포함 포즈에 이식한 Stage 2 착장을 입력으로 사용했다. 회색 바탕과 바닥 그림자는 중립화됐지만, 그림자의 지면 원근은 최종 합성의 접지감으로 판단하지 않는다.

[Studio DeLight 2509 실행 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2509_studio_delight.py)

[Scene A DeLight 캐릭터 result.json — JSON — identity 이식 입력, trigger prompt와 2509 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-cutout-identity-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene B DeLight 캐릭터 result.json — JSON — 캐릭터 입력, trigger prompt와 2509 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-b-size-1280x1280-seed-62294-steps-10-result.json)

[Scene C DeLight 캐릭터 result.json — JSON — Stage 2 착장 아이덴티 입력, trigger prompt와 2509 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-c-shadow-stage2-outfit-no-closeup-v3-size-1280x1280-seed-62294-steps-10-result.json)

#### DeLight 캐릭터에 45도 얼굴 identity를 이식한다

DeLight 캐릭터는 배경과 분리된 상태이므로, 얼굴·헤어만 바꾸는 BFS Head V5의 입력으로 사용하기 좋다. Picture 1에는 Scene B·C DeLight 캐릭터 컷아웃, Picture 2에는 45도 얼굴 참조를 넣었다. 포즈·흰 재킷·회색 이너·청록 바지·바닥 그림자는 Picture 1에 남기고, 얼굴 방향·앰버 홍채·청록 헤어의 기준만 Picture 2가 맡는다.

| Scene A BFS 45도 얼굴 이식 | Scene B BFS 45도 얼굴 이식 | Scene C BFS 45도 얼굴 이식 |
| --- | --- | --- |
| ![45도 얼굴 참조를 이식한 Scene A 그림자 포함 캐릭터](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-a-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![45도 얼굴 참조를 이식한 Scene B DeLight 캐릭터](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-b-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![45도 얼굴 참조를 이식한 Scene C DeLight 캐릭터](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-c-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) |

Scene A·B·C 모두 10 step에서 45도 얼굴 방향과 앰버 홍채가 반영됐다. C의 30 step 비교는 눈·머리카락의 세부를 뚜렷하게 개선하지 못했으므로, 이 실행기의 기본값은 10 step으로 둔다. 이 결과는 다음 리라이트 통합본의 얼굴 이식 결과와 비교할 수 있도록, 그림자 포함 캐릭터와 DeLight 캐릭터 컷아웃을 입력으로 남긴다.

[BFS Head V5 얼굴·헤어 이식 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_bfs_head_identity.py)

[Scene A 45도 얼굴 참조 BFS result.json — JSON — 그림자 포함 입력과 얼굴 참조의 순서, LoRA 파일, seed와 step 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-a-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene B 45도 얼굴 참조 BFS result.json — JSON — 두 입력의 순서, LoRA 파일, seed와 step 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-b-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene C 45도 얼굴 참조 BFS result.json — JSON — 두 입력의 순서, LoRA 파일, seed와 step 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-c-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

#### 카메라판에서 캐릭터를 제거해 배경판을 만든다

컷아웃에 캐릭터 identity를 이식한 뒤에는, 같은 카메라판에서 인물을 비운 배경판도 별도 자산으로 만든다. 이 배경판은 인물의 얼굴·착장 기준을 다시 넣지 않는다. Qwen Image Edit 2511에 카메라판 한 장만 넣고, 인물 자리만 주변 배경으로 메우며 장소의 주요 지형·식생·구도를 보존하도록 짧게 지시했다. 이 단계의 목적은 포즈를 만들거나 캐릭터를 보정하는 것이 아니라, 이후 합성에서 쓸 배경 입력을 한 장으로 고정하는 것이다.

| Scene A 캐릭터 제거 배경판 | Scene B 캐릭터 제거 배경판 | Scene C 캐릭터 제거 배경판 |
| --- | --- | --- |
| ![카메라 A에서 공중 스플릿 점프 인물을 제거하고 해안 절벽과 바다를 남긴 1280 정사각형 배경판](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-camera-a-background-camera-a-v1-size-1280x1280-seed-62294-steps-10.png) | ![카메라 B에서 공중 스플릿 점프 인물을 제거하고 야생화 초원과 먼 산을 남긴 1280 정사각형 배경판](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-camera-b-background-camera-b-v1-size-1280x1280-seed-62294-steps-10.png) | ![카메라 C에서 인물을 제거하고 공원 나무, 벤치, 가로등과 보도를 남긴 1280 정사각형 배경판](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-camera-c-background-camera-c-v1-size-1280x1280-seed-62294-steps-10.png) |

두 실행은 모두 1280×1280, seed `62294`, 10 step, true CFG `4.0`이다. 인물은 사라졌지만, A의 하늘은 밝고 단순한 색면으로 바뀌었고 B의 초원 중심부도 원본보다 단순해졌다. 따라서 인물 제거와 원본 배경의 모든 색·질감을 픽셀 단위로 보존하는 일은 같은 요구가 아니다.

[카메라판 배경 생성 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_extract_camera_a_background.py)

[카메라 A 배경판 result.json — JSON — 카메라 입력, 인물 제거 지시와 2511 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-camera-a-background-camera-a-v1-size-1280x1280-seed-62294-steps-10-result.json)

[카메라 B 배경판 result.json — JSON — 카메라 입력, 인물 제거 지시와 2511 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-camera-b-background-camera-b-v1-size-1280x1280-seed-62294-steps-10-result.json)

[카메라 C 배경판 result.json — JSON — 카메라 입력, 인물 제거 지시와 2511 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-camera-c-background-camera-c-v1-size-1280x1280-seed-62294-steps-10-result.json)

#### 배경판에 Studio DeLight를 적용한다

바로 위 배경판을 Qwen Image Edit 2509의 Studio DeLight 입력으로 사용해 중립 광원 처리를 한 번 더 적용했다. 프롬프트는 모델 카드의 trigger prompt인 `Neutral uniform lighting Preserve identity and composition`만 사용한다. 인물이 없는 배경판으로 분리했으므로, 이 단계에서 바뀌는 대상은 인물 identity나 포즈가 아니라 하늘·바다·바위·풀의 조명과 색조다.

| Scene A DeLight 배경판 | Scene B DeLight 배경판 | Scene C DeLight 배경판 |
| --- | --- | --- |
| ![Studio DeLight로 중립 조명을 적용한 인물 없는 해안 절벽 배경판](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-camera-a-background-v1-size-1280x1280-seed-62294-steps-10.png) | ![Studio DeLight로 중립 조명을 적용한 인물 없는 야생화 초원 배경판](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-background-b-size-1280x1280-seed-62294-steps-10.png) | ![Studio DeLight로 중립 조명을 적용한 인물 없는 도심 공원 배경판](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-background-c-size-1280x1280-seed-62294-steps-10.png) |

1280×1280, seed `62294`, 10 step, true CFG `4.0`에서 하늘·바다는 더 균일하고 밝아졌고 바위·풀·해안의 배치는 남았다. 그러나 야외 장면의 하늘은 거의 흰색에 가까워졌다. 이 출력은 중립화가 적용되는지 확인하는 배경 후보이며, 해안의 원래 광원과 색감을 보존해야 하는 최종 배경으로 자동 채택하지 않는다.

[Studio DeLight 2509 실행 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2509_studio_delight.py)

[Studio DeLight 배경판 result.json — JSON — 배경판 입력, trigger prompt와 2509 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-camera-a-background-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene B DeLight 배경판 result.json — JSON — 배경판 입력, trigger prompt와 2509 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-background-b-size-1280x1280-seed-62294-steps-10-result.json)

[Scene C DeLight 배경판 result.json — JSON — 배경판 입력, trigger prompt와 2509 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-background-c-size-1280x1280-seed-62294-steps-10-result.json)

#### DeLight 배경과 캐릭터를 다중 참조로 통합한다

첫 통합에서는 이 마스크를 쓰지 않았다. Qwen Image Edit 2511의 다중 참조에 DeLight 배경판을 `Picture 1`, BFS 45도 얼굴 참조를 이식한 캐릭터를 `Picture 2`로만 넣었다. 프롬프트도 배경은 Picture 1의 장소·구도, 인물은 Picture 2의 스플릿 점프·identity·착장을 각각 보존하라는 양성 지시로 한정했다.

| Scene A BFS DeLight 통합 | Scene B BFS DeLight 통합 | Scene C BFS DeLight 통합 |
| --- | --- | --- |
| ![BFS 45도 얼굴 참조를 이식한 Scene A 그림자 캐릭터와 DeLight 해안 배경을 Qwen 2511 다중 참조로 통합한 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-multireference-composite-scene-a-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![BFS 45도 얼굴 참조를 이식한 Scene B 캐릭터와 DeLight 야생화 초원 배경을 Qwen 2511 다중 참조로 통합한 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-multireference-composite-scene-b-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![BFS Head V5의 45도 얼굴 참조를 이식한 DeLight C 캐릭터와 도심 공원 배경을 Qwen 2511 다중 참조로 통합한 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-multireference-composite-scene-c-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) |

1280×1280, seed `62294`, 10 step, true CFG `4.0`에서 회색 컷아웃 배경은 남지 않고 각 장소와 인물 경계가 통합됐다. A·B·C 모두 45도 얼굴 참조의 청록 헤어를 가진 흰 재킷·회색 이너·청록 바지 캐릭터를 각 배경에 넣었다. 즉 다중 참조 통합은 두 이미지의 역할을 따르며, `Picture 2`에 없는 착장을 새로 복원하지 않는다. 공중 인물의 지면 그림자는 새로 설계되지 않았으므로, 이 결과는 마스크 없는 다중 참조 합성의 관찰용 출력이며 접지 그림자 보정까지 끝난 최종 장면은 아니다.

[Qwen 2511 DeLight 다중 참조 통합 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_composite_delight_multireference.py)

[Scene A BFS DeLight 다중 참조 통합 result.json — JSON — 해안 배경·그림자 포함 BFS 캐릭터의 입력 순서와 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-multireference-composite-scene-a-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene B BFS DeLight 다중 참조 통합 result.json — JSON — 꽃밭 배경·BFS 캐릭터의 입력 순서와 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-multireference-composite-scene-b-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene C DeLight 다중 참조 통합 result.json — JSON — 공원 배경·45도 얼굴 참조 캐릭터의 입력 순서와 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2511-delight-multireference-composite-scene-c-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

#### 통합 장면에 방향광을 다시 적용한다

DeLight는 캐릭터와 배경의 광원을 중립화했으므로, 통합 후에는 단일 이미지 리라이트로 장면의 광원 방향을 다시 정할 수 있다. 여기서는 `dx8152/Qwen-Image-Edit-2509-Relight` LoRA를 사용해 앞의 통합 이미지를 한 장만 입력하고, trigger `重新照明`과 `soft sunlight from the upper right`만 지시했다. 새 캐릭터 참조나 마스크는 이 단계에 넣지 않는다. [dx8152 Relight 모델 카드](https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Relight){: target="_blank" rel="noopener noreferrer"}

| Scene A BFS 통합 리라이트 | Scene B BFS 통합 리라이트 | Scene C BFS 통합 리라이트 |
| --- | --- | --- |
| ![상단 우측의 따뜻한 햇빛이 Scene A 해안의 BFS 캐릭터와 배경에 적용된 통합 리라이트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-a-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![상단 우측의 따뜻한 햇빛이 Scene B 야생화 초원의 BFS 캐릭터와 배경에 적용된 통합 리라이트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-b-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![상단 우측의 따뜻한 햇빛이 Scene C 공원의 BFS 캐릭터와 배경에 적용된 통합 리라이트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-c-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) |

1280×1280, seed `62294`, 10 step, LoRA scale `1.0`, true CFG `4.0`에서 A·B·C는 상단 우측이 따뜻하게 밝아지고 반대편은 더 어두워졌다. 인물의 포즈·착장과 각 장소의 구도는 유지됐지만, 이 단일 이미지 리라이트가 공중 인물에 맞는 별도 접지 그림자를 새로 설계한 것은 아니다.

[Qwen 2509 Relight 실행 코드 보기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2509_relight.py)

[Scene A BFS 통합 리라이트 result.json — JSON — BFS 통합 입력, Relight trigger와 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-a-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene B BFS 통합 리라이트 result.json — JSON — BFS 통합 입력, Relight trigger와 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-b-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

[Scene C BFS 통합 리라이트 result.json — JSON — BFS 통합 입력, Relight trigger와 실행 조건 보기](/AiBook/assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-c-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json)

## 체크리스트

- [ ] P7-5.4의 A v5·B v8·C v7과 각 입력 JSON을 같은 장면에 연결했는가?
- [ ] A·B·C의 Mira와 C의 조연을 각각 분리하고, 다른 인물·동물·새가 섞이지 않았는가?
- [ ] C에서 가려진 영역과 마스크 경계의 누락을 구분하고, 투명 PNG의 알파가 마스크와 일치하는가?
- [ ] 별도 그림자 추가 단계 없이도 모델 출력에 그림자가 생길 수 있음을 결과에서 확인했는가?
- [ ] B 마네킨의 인물 교체에서 착장 반영과 신발 누락·그림자 추가를 구분하고, 파일명보다 실제 참조와 프롬프트를 확인했는가?
- [ ] 새 입력의 후속 결과와 이전 카메라판의 실험 결과를 구분했는가?

## 출처와 참고 자료

- [Qwen-Image-Edit-2511 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer"}: 그림자 포함 포즈·캐릭터 다중 참조 이식, 배경·캐릭터 통합에 사용한 공식 파이프라인의 입력 형식과 사용 예제를 확인합니다.
- [Grounding DINO Tiny 모델 카드](https://huggingface.co/IDEA-Research/grounding-dino-tiny){: target="_blank" rel="noopener noreferrer"} · [SAM 2 공식 저장소](https://github.com/facebookresearch/sam2){: target="_blank" rel="noopener noreferrer"}: 인물 탐색 상자와 정밀 마스크를 만드는 두 단계의 근거입니다.
- [Qwen-Image-Edit-2509 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2509){: target="_blank" rel="noopener noreferrer"} · [Studio DeLight 모델 카드](https://huggingface.co/prithivMLmods/QIE-2511-Studio-DeLight){: target="_blank" rel="noopener noreferrer"} · [Relight 모델 카드](https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Relight){: target="_blank" rel="noopener noreferrer"}: 배경·캐릭터의 중립 광원과 통합 장면의 방향광을 확인한 편집 경로입니다.

모델 카드의 일반 기능 설명과 별도로, 이 절에서 실제로 사용한 입력 순서·파일 해시·seed·step·출력 경로는 각 `result.json`을 기준으로 확인합니다.
