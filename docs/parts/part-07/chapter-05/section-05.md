# P7-5.5 스토리보드 장면에서 캐릭터를 분리하고 적용하는 경로

> Section ID: `P7-5.5`
> Version: `v2026.09.10`

이 절은 [P7-5.4](section-04.md)의 마지막 단계에서 주변 인물과 동물까지 추가한 A·B·C를 입력으로 이어받는다. 장면에서 Mira와 조연을 각각 분리한 뒤, 분리된 캐릭터에 아이덴티티를 적용한다. 여기서 아이덴티티는 같은 인물로 알아볼 수 있는 얼굴·머리 모양·착장 등의 외형을 뜻한다. 분리 단계는 원본에서 보이는 픽셀을 고르는 작업이고, 아이덴티티 적용 단계는 참조나 텍스트에 따라 외형을 다시 생성하는 작업이다. 이 절은 외형 반영과 포즈·가림 경계 보존을 같은 성공으로 판단하지 않는 방법을 확인한다. 별도의 그림자 추가 단계는 두지 않는다. 각 후속 결과의 `result.json`에는 실제 입력 파일, SHA-256과 실행 조건을 남겨 입력 장면과 출력의 관계를 확인한다.

## P7-5.4의 최종 장면을 입력으로 고정한다

세 입력은 모두 1280×1280이다. A·B·C 모두 P7-5.4에서 재생성한 `extras-audit-20260909-v1`을 사용한다. A는 주변 인물 여섯 명, B는 토끼와 다람쥐, C는 앉아 있는 새 세 마리를 포함한다. 원본 자산을 P7-5.5용으로 복제하지 않고 P7-5.4의 파일을 직접 참조한다.

| Scene A | Scene B | Scene C |
| --- | --- | --- |
| ![도시 거리에서 달리는 Mira와 주변 인물](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-extras-audit-20260909-v1-size-1280x1280-seed-5420-steps-20.png) | ![숲 공터에서 도약하는 Mira와 토끼·다람쥐](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-extras-audit-20260909-v1-size-1280x1280-seed-5421-steps-20.png) | ![언덕에서 책을 읽는 두 인물과 앉아 있는 새 세 마리](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-extras-audit-20260909-v1-size-1280x1280-seed-5422-steps-20.png) |

[Scene A 입력 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-extras-audit-20260909-v1-size-1280x1280-seed-5420-steps-20-result.json){ .lazy-source }

[Scene B 입력 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-extras-audit-20260909-v1-size-1280x1280-seed-5421-steps-20-result.json){ .lazy-source }

[Scene C 입력 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-extras-audit-20260909-v1-size-1280x1280-seed-5422-steps-20-result.json){ .lazy-source }

## 편집할 인물과 보존할 대상을 나눈다

| 장면 | 인물 마스크·컷아웃 대상 | 인물 편집에서 보존할 주변 대상 |
| --- | --- | --- |
| A | 화면 중앙에서 달리는 Mira | 주변 인물 여섯 명, 도로와 건물 |
| B | 공중에서 도약하는 Mira | 왼쪽 아래 토끼, 오른쪽 나무 밑 다람쥐, 나무와 양치식물 |
| C | 왼쪽 Mira와 오른쪽 조연을 각각 별도 마스크로 분리 | 각 마스크에서 다른 인물, 책, 새 세 마리, 난간과 도시 배경 |

A와 C에는 여러 인물이 있으므로 `a person` 검출 결과를 그대로 모두 합치지 않고 Mira에 해당하는 상자와 마스크를 확인해야 한다. C에서는 손과 책이 겹치는 경계도 확인한다. Mira를 제거한 배경판을 만들 때도 주변 인물·동물까지 함께 지워서는 안 된다.

현재 실행 흐름은 `P7-5.4 최종 장면 → 인물별 마스크·컷아웃 → 아이덴티티 적용 → 결과 비교`다. A·B·C의 Mira는 P7-5.3 최종 착장을 참조하고, C 조연은 텍스트로 새 외형을 지정한다. 컷아웃이 포즈·인물 크기·프레이밍을 전달하더라도 생성 결과에서 그대로 유지되는지는 별도로 확인한다. 직접 적용 경로와 분리해 B·C에는 컷아웃을 마네킨으로 바꾸는 단계를 제시한다. 마네킨 경로에서는 C의 착장 반영을 확인한다. 이전 입력의 마네킨·배경·조명 통합 실험은 보충학습에서 구분한다.

## Mira와 조연을 각각 분리한다

아래 네 컷아웃과 마스크는 위의 신규 `extras-audit-20260909-v1` A·B·C에서 재생성한 결과다. 인물별 입력 해시와 검출 문구, 상자, 포함점·제외점을 설정 파일에 고정했다. 분리는 Grounding DINO와 SAM 2.1의 추론으로 수행하며, 흰 배경·투명 컷아웃은 추론된 마스크에 따라 원본 픽셀을 복사한다.

먼저 장면에서 어느 인물을 분리할지 지정한다. 로컬 GPU에서 Grounding DINO Tiny로 인물 상자를 찾고 SAM 2.1 Hiera Small로 마스크를 만들었다. 여기서 마스크는 복사할 인물 픽셀을 흰색, 제외할 영역을 검은색으로 표시한 이미지다. 모델이 Mira라는 이름을 알아본 것은 아니다. 청록색 머리와 위치를 눈으로 확인한 뒤 대상 좌표를 지정했으며, 겹친 영역은 상자·포함점·제외점을 모델에 전달해 다시 추론했다. C에서는 포함점이 놓인 마스크 조각을 유지하고 작은 내부 구멍을 채우는 후처리도 사용했다. [Grounding DINO 모델 카드](https://huggingface.co/IDEA-Research/grounding-dino-tiny){: target="_blank" rel="noopener noreferrer"} · [SAM 2.1 모델 카드](https://huggingface.co/facebook/sam2.1-hiera-small){: target="_blank" rel="noopener noreferrer"}

A에서는 화면 앞으로 크게 나온 신발 끝까지 포함하고 배경의 달리는 사람은 제외했다. B에서는 도약하는 Mira만 선택하고 토끼와 다람쥐를 제외했다. C에서는 Mira와 조연을 따로 선택했다. 조연은 Mira에 가려 상체와 하체가 떨어져 보이므로, 가장 큰 덩어리 하나만 남기면 상체가 사라질 수 있다. 이번에는 포함점이 놓인 여러 덩어리를 함께 유지했다.

아래 흰 배경 컷아웃은 분리 영역을 확인하는 이미지다. 함께 저장한 투명 PNG는 같은 마스크를 알파 채널로 사용한다. 네 파일 모두 원본과 같은 1280×1280 캔버스와 인물 위치를 유지하며, 선택된 픽셀의 색을 원본에서 그대로 복사했다.

**마스크 오버레이**

| Scene A Mira | Scene B Mira | Scene C Mira | Scene C 조연 |
| --- | --- | --- | --- |
| ![Scene A Mira 마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-a-mira-audit-20260909-v1-overlay.png) | ![Scene B Mira 마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-b-mira-audit-20260909-v1-overlay.png) | ![Scene C Mira 마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-mira-audit-20260909-v6-overlay.png) | ![Scene C 조연 마스크 오버레이](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-supporting-audit-20260909-v2-overlay.png) |

**마스크 이미지**

| Scene A Mira | Scene B Mira | Scene C Mira | Scene C 조연 |
| --- | --- | --- | --- |
| ![Scene A Mira 마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-a-mira-audit-20260909-v1.png) | ![Scene B Mira 마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-b-mira-audit-20260909-v1.png) | ![Scene C Mira 마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-mira-audit-20260909-v6.png) | ![Scene C 조연 마스크](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-supporting-audit-20260909-v2.png) |

**분리 결과**

| Scene A Mira | Scene B Mira | Scene C Mira | Scene C 조연 |
| --- | --- | --- | --- |
| ![Scene A Mira의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-a-mira-audit-20260909-v1.png) | ![Scene B Mira의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-b-mira-audit-20260909-v1.png) | ![Scene C Mira의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-mira-audit-20260909-v6.png) | ![Scene C 조연의 보이는 영역을 추출한 흰 배경 컷아웃](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-supporting-audit-20260909-v2.png) |

**Scene A Mira**

[마스크 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-a-mira-audit-20260909-v1-result.json){ .lazy-source }

[컷아웃 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-a-mira-audit-20260909-v1-result.json){ .lazy-source }

**Scene B Mira**

[마스크 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-b-mira-audit-20260909-v1-result.json){ .lazy-source }

[컷아웃 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-b-mira-audit-20260909-v1-result.json){ .lazy-source }

**Scene C Mira**

[마스크 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-mira-audit-20260909-v6-result.json){ .lazy-source }

[컷아웃 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-mira-audit-20260909-v6-result.json){ .lazy-source }

**Scene C 조연**

[마스크 기록](../../../assets/part-07/chapter-05/p7-5-5-sam2-person-mask-scene-c-supporting-audit-20260909-v2-result.json){ .lazy-source }

[컷아웃 기록](../../../assets/part-07/chapter-05/p7-5-5-character-cutout-scene-c-supporting-audit-20260909-v2-result.json){ .lazy-source }

### 분리 결과의 한계

C의 빈 부분은 다른 인물·책·새에 가려져 원본에 보이지 않는 영역을 포함한다. 이번 작업은 보이는 픽셀을 분리한 것이며, 가려진 신체를 새로 그리지 않았다. 손과 책, 머리카락과 배경이 맞닿는 경계에는 일부 거친 가장자리와 미세 누락이 남아 있다. 다른 배경에 옮길 때는 이 경계를 다시 확인해야 한다. 두 C 마스크 사이에는 경계의 중복 픽셀 10개가 남아 있으며, 네 투명 PNG의 알파 채널이 해당 마스크와 일치하는지 확인했다.

[인물별 입력·선택 조건과 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-character-separation-audit-20260909-v1-result.json){ .lazy-source }에 네 분리 결과를 모았다.

### Mira와 조연을 분리하는 재현 코드

재현 코드는 A·B·C Mira와 C 조연을 각각 마스크·오버레이·흰 배경 컷아웃·투명 PNG로 출력한다. 설정 파일에는 현재 1280×1280 입력의 SHA-256, 대상 인물의 선택점, 추가 포함점·제외점, 상자와 후처리 옵션을 기록한다. 다른 이미지에 그대로 적용하는 일반 좌표가 아니므로 입력 해시가 다르면 실행 전에 중단한다.

[분리 재현 실행 코드](../../../assets/part-07/chapter-05/p7_5_5_reproduce_character_separation.py)

[인물별 설정 파일](../../../assets/part-07/chapter-05/p7-5-5-character-separation-recipe-v1.json){ .lazy-source }

저장소 루트에서 필요한 패키지가 설치된 `.venv`로 실행한다. Grounding DINO Tiny와 SAM 2.1 Hiera Small 모델은 `.tmp/download/huggingface/hub`에 준비돼 있어야 하며, 추론에는 CUDA GPU를 사용한다. 우선 다음 명령으로 모델을 읽지 않고 네 인물의 입력과 출력 계획을 확인한다.

~~~bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_reproduce_character_separation.py \
  --output-dir /tmp/p7-5-5-separation-repeat --dry-run
~~~

다음 명령은 A·B·C 미라와 C 조연을 차례로 분리한다. 각 인물마다 마스크·오버레이·흰 배경 컷아웃·투명 PNG와 두 실행 JSON을 저장한다. 마지막에는 전체 검증 결과 JSON도 저장한다.

~~~bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_reproduce_character_separation.py \
  --output-dir /tmp/p7-5-5-separation-repeat
~~~

C 미라와 조연만 재현하려면 대상을 선택한다.

~~~bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_reproduce_character_separation.py \
  --targets c-mira c-supporting \
  --output-dir /tmp/p7-5-5-separation-c-repeat
~~~

기존 파일이 있는 출력 경로는 전체 실행 전에 거부한다. 다시 실행할 때는 새 출력 폴더 또는 `--run-label`을 지정한다. 실행 코드는 출력 이름을 기준으로 다음 컷아웃 입력을 연결하므로, 마스크 경로를 따로 고칠 필요가 없다. 인물별 상자와 좌표를 바꾸는 실험은 설정 파일의 `mask_args`에서 조정하며, 이 경우 기존 기준 이미지와 일치하지 않을 수 있다.

[실제 재실행 검증 기록](../../../assets/part-07/chapter-05/p7-5-5-character-separation-reproduction-check-v1-result.json){ .lazy-source }에서는 네 인물 모두 마스크·흰 배경·투명 PNG가 기준 이미지와 픽셀 단위로 일치했다. 검증은 투명 PNG의 알파와 마스크 일치, 선택된 원본 픽셀의 보존, 흰 배경과 출력 크기도 확인한다. 기준과 다르거나 픽셀 검사가 실패하면 결과 JSON을 남기고 오류로 종료한다. 이 재현 확인은 기록된 로컬 환경에서 수행했으며, 모델·패키지 환경이 달라지면 결과 JSON의 실행 환경과 차이 항목을 확인해야 한다. 경계의 미세 누락이나 C의 가림 영역까지 복구됐다는 의미는 아니다.

실제 추론은 [인물 마스크 생성 코드](../../../assets/part-07/chapter-05/p7_5_5_generate_person_mask.py)가, 픽셀 복사와 알파 저장은 [흰 배경·투명 컷아웃 생성 코드](../../../assets/part-07/chapter-05/p7_5_5_extract_pose_cutout.py)가 담당한다.

## 분리한 캐릭터에 아이덴티티를 적용한다

위에서 얻은 흰 배경 컷아웃 네 장을 Qwen Image Edit 2511에 직접 넣는다. 분리할 때 만든 마스크는 이 편집 단계에 전달하지 않는다. 따라서 결과는 원본 픽셀을 복사한 컷아웃과 달리, 포즈·얼굴·옷·경계가 함께 바뀔 수 있는 생성 이미지다. 출력 PNG도 투명 레이어가 아닌 흰 배경 이미지다.

| 대상 | Picture 1 | Picture 2 또는 텍스트의 역할 |
| --- | --- | --- |
| A·B·C Mira | 각 장면의 신규 Mira 컷아웃 | P7-5.3 최종 3단계 착장에서 인물 외형·착장 참조 |
| C 조연 | 신규 조연 컷아웃 | 두 번째 이미지 없이 텍스트로 새 외형 지정 |

[Mira의 P7-5.3 최종 3단계 착장 참조](../../../assets/part-07/chapter-05/p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png)를 세 장에 공통으로 사용한다. Mira의 외형을 텍스트로 다시 묘사하지 않고 다음 지시를 전달했다.

> Replace the woman in Picture 1 with the woman in Picture 2, preserving the pose. Preserve the framing and white background of Picture 1.

이는 1번 여성의 포즈를 유지하면서 2번 여성으로 교체하고, 1번의 프레이밍과 흰 배경을 보존하라는 뜻이다. C 조연에게는 별도 인물 참조 대신 다음 지시로 짧은 갈색 머리, 둥근 안경, 파란 후드티, 차콜색 바지와 흰 스니커즈를 지정했다.

> Give the man in Picture 1 a new character identity: a young adult man with short dark brown hair, round glasses, a muted blue hoodie, charcoal trousers, and white sneakers. Preserve the seated pose, body proportions, framing and white background of Picture 1.

### 직접 아이덴티티 적용의 입력 조건을 고정한다

[컷아웃 아이덴티티 생성기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_cutout_identity.py)는 신규 컷아웃 경로와 Mira 참조를 기본값으로 고정한다. 기존 포즈 생성기의 경로·이미지 전처리·해시·실행 환경 기록 함수를 재사용하며, 네 대상의 입력 구성과 프롬프트, 생성 루프는 신규 코드에서 관리한다. 로컬 CUDA GPU에서 BF16, sequential CPU offload로 실행했고, 추가 LoRA는 사용하지 않았다.

출력은 네 장 모두 1280×1280, 30스텝, seed `62294`, true CFG `4.0`이다. CPU 난수 생성기를 사용하며, 각 입력은 비율을 유지해 1280×1280 흰 캔버스에 배치한다. 저장소의 `.venv`와 로컬 모델 캐시를 준비한 상태에서 다음 명령으로 입력·프롬프트·출력 계획을 확인한다.

~~~bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_cutout_identity.py \
  --targets a-mira b-mira c-mira c-supporting \
  --steps 30 --run-label identity-repeat-v1 \
  --supporting-prompt "Give the man in Picture 1 a new character identity: a young adult man with short dark brown hair, round glasses, a muted blue hoodie, charcoal trousers, and white sneakers. Preserve the seated pose, body proportions, framing and white background of Picture 1." \
  --dry-run
~~~

`--dry-run`을 빼면 네 장을 순서대로 생성한다. `--targets`로 대상, `--reference`로 Mira 참조, `--supporting-prompt`로 조연 외형, `--steps`와 `--seed`로 생성 조건을 바꿀 수 있다. 기존 PNG·JSON이 있으면 실행 전에 중단하므로 재실행에는 새 `--run-label`이나 `--output-dir`을 지정한다. 각 JSON에는 실제 입력·참조·출력 해시와 프롬프트·실행 환경을 기록한다. 조연의 텍스트 전용 실행에서는 참조 경로가 `null`, `text_only`가 `true`다.

**아이덴티티 적용 결과**

| Scene A Mira | Scene B Mira | Scene C Mira | Scene C 조연 |
| --- | --- | --- | --- |
| ![Scene A Mira 아이덴티티 적용 30스텝 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-identity-a-mira-audit-20260909-v1-size-1280x1280-seed-62294-steps-30.png) | ![Scene B Mira 아이덴티티 적용 30스텝 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-identity-b-mira-audit-20260909-v1-size-1280x1280-seed-62294-steps-30.png) | ![Scene C Mira 아이덴티티 적용 30스텝 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-identity-c-mira-audit-20260909-v1-size-1280x1280-seed-62294-steps-30.png) | ![Scene C 조연 아이덴티티 적용 30스텝 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-identity-c-supporting-audit-20260909-v1-size-1280x1280-seed-62294-steps-30.png) |

A는 신발 부분에 오류가 남았다. 앞쪽 발에서 밑창이 크게 보이는 구조라 신발 형태를 안정적으로 바꾸지 못했고, 이 입력·참조·30스텝 조건에서는 적용 가능한 개선 방안을 확보하지 못했다. 따라서 이 사례는 신발 밑창처럼 큰 전경 구조를 참조 외형으로 바꾸는 데서 드러난 현재 모델 경로의 한계로 기록한다.

B도 신발 부분에 오류가 남았다. 다만 원본 컷아웃의 기존 외형을 줄인 마네킨에서 다시 시작하면, 신발과 착장을 별도로 적용할 입력을 만들 수 있다. 다음 마네킨 경로는 이 대응 가능성을 확인한다.

C도 신발 부분에 오류가 남았다. B와 마찬가지로 마네킨에서 시작하는 경로를 사용해 기존 외형의 영향을 줄인 뒤 착장을 적용하는 방법을 확인한다.

C 조연은 책이 사라졌으므로, 장면으로 되돌리기 전에 책 보존 또는 복원을 별도로 보완해야 한다.

## B·C 컷아웃의 외형을 마네킨으로 바꿔 본다

직접 아이덴티티 적용 경로와 분리하여, B·C에는 `원본 컷아웃 → 마네킨 → 착장 적용`의 중간 단계를 준비한다. 여기서 마네킨은 얼굴 없는 회색 모형이 아니라, 얼굴과 관절 방향을 읽을 수 있는 성인 여성의 포즈용 이미지다. 아주 짧은 스포츠머리, 회색 스포츠 브라와 짧은 하의, 맨발을 지정해 기존 외형을 바꾼다.

입력은 아이덴티티 적용 결과가 아닌 분리 단계의 원본 Mira 컷아웃이다. 한 장의 컷아웃만 로컬 Qwen Image Edit 2511에 넣고, 마스크·캐릭터 참조·추가 LoRA는 사용하지 않는다. B는 도약 자세를, C는 앉은 자세를 보존하도록 지시했다. 다만 원본에 가려져 보이지 않는 신체와 옷 아래 형상을 모델이 새로 그리므로, 마네킨에서도 포즈와 신체 비율을 다시 확인해야 한다.

### B Mira의 20스텝 마네킨

![B 원본 컷아웃에서 생성한 마네킨](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-mannequin-b-mira-cutout-v1-size-1280x1280-seed-62294-steps-20.png)

긴 머리·재킷·바지·신발이 짧은 머리와 회색 운동복·맨발로 바뀌었다. 다리를 벌린 도약 자세의 큰 형태는 남았지만 얼굴 방향과 팔·다리의 세부 각도가 변했다.

[B 마네킨 입력·프롬프트·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-mannequin-b-mira-cutout-v1-size-1280x1280-seed-62294-steps-20-result.json){ .lazy-source }

### C Mira의 20스텝 마네킨

![C 원본 컷아웃에서 생성한 마네킨](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-mannequin-c-mira-cutout-v1-size-1280x1280-seed-62294-steps-20.png)

짧은 머리와 회색 운동복·맨발이 반영됐다. 앉은 자세는 남았지만 원본 컷아웃의 빈 가림 영역이 채워지고 손·다리 형태가 변했다. 채워진 신체는 원본에서 확인된 형상이 아니다.

[C 마네킨 입력·프롬프트·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-cutout-mannequin-c-mira-cutout-v1-size-1280x1280-seed-62294-steps-20-result.json){ .lazy-source }

### B·C 마네킨 생성 조건을 재현한다

[신규 컷아웃 마네킨 생성기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_cutout_mannequin.py)는 분리 설정 파일에서 각 Mira의 흰 배경 컷아웃을 찾는다. 출력은 1280×1280, 20스텝, seed `62294`, true CFG `4.0`이며 CPU 난수 생성기를 사용했다. 원본 캔버스를 그대로 입력하고, BF16과 sequential CPU offload로 로컬 CUDA GPU에서 생성했다. 다음 명령은 B·C 두 컷의 입력·프롬프트를 확인한다.

~~~bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_cutout_mannequin.py \
  --scenes b c --steps 20 --run-label manuscript-repeat-v1 --dry-run
~~~

`--dry-run`을 빼면 생성한다. `--scenes`로 대상, `--prompt`로 공통 외형 지시, `--steps`와 `--seed`로 조건을 바꿀 수 있다. 기존 결과를 덮어쓰지 않으므로 새 `--run-label`이나 `--output-dir`을 사용한다. 실행 JSON에는 실제 프롬프트와 입력·출력 해시를 남긴다. B·C의 실제 지시는 각각의 JSON으로 확인한다.

앞서 제시한 30스텝 아이덴티티 결과는 원본 컷아웃에서 직접 생성한 것이다. B·C는 위 마네킨을 입력으로 착장을 입히는 별도의 경로를 사용한다.

## B·C 마네킨에 공통으로 아이덴티티를 적용한다

원본 컷아웃의 외형을 줄인 뒤에도 참조의 옷과 신발을 반영할 수 있는지 확인한다. B·C 모두 Picture 1에는 각 장면의 마네킨, Picture 2에는 P7-5.3의 최종 3단계 착장 이미지를 넣는다. 공통 흐름은 `원본 컷아웃 → 마네킨 → 아이덴티티 1차 적용(착장·신발)`이다. 이번 단계는 착장과 신발을 적용하며, 얼굴·머리 아이덴티티 보강은 이후 BFS 단계에서 다룬다.

[공통 3단계 착장 참조](../../../assets/part-07/chapter-05/p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png)를 사용하고, 옷의 색·길이·디자인을 텍스트로 다시 풀어 쓰지 않았다. 실제 프롬프트는 다음 두 문장이다.

> Dress the woman in Picture 1 in the complete outfit, including shoes, from Picture 2. Keep the face, hairstyle, pose, perspective, framing and white background of Picture 1.

이는 2번의 전체 착장과 신발을 1번 여성에게 입히되, 1번의 얼굴·머리·포즈·원근·프레이밍과 흰 배경은 유지하라는 뜻이다. B·C 결과에서 착장 반영과 함께 자세·크기 보존을 각각 확인한다.

### 착장 1차 적용 생성기

[마네킨 착장 생성기](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_mannequin_outfit.py)는 B·C 마네킨을 장면별 입력으로 읽고 동일한 착장 참조와 프롬프트로 각각 편집한다. 로컬 Qwen Image Edit 2511의 `QwenImageEditPlusPipeline`을 BF16과 sequential CPU offload로 실행했다. 마스크·추가 LoRA·결과 합성은 사용하지 않았다. 두 입력은 비율을 유지해 각각 1280×1280 흰 캔버스에 배치한다.

B·C 출력은 각각 1280×1280, 20스텝, seed `62294`, true CFG `4.0`이며 CPU 난수 생성기를 사용했다. 다음 명령은 모델을 불러오지 않고 입력과 공통 프롬프트·출력 계획을 확인한다.

~~~bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_mannequin_outfit.py \
  --scenes b c --steps 20 --run-label stage3-repeat-v1 --dry-run
~~~

`--dry-run`을 빼면 B·C를 순서대로 생성한다. `--scenes`는 대상, `--reference`는 착장 참조, `--prompt`는 편집 지시, `--steps`와 `--seed`는 생성 조건을 바꾼다. 기존 PNG·JSON이 있으면 실행 전에 중단하므로 재실행에는 새 `--run-label`이나 `--output-dir`을 지정한다. JSON에는 실제 두 입력·출력의 해시, 프롬프트, 코드 해시와 실행 환경을 저장한다.

### B·C 아이덴티티 1차 적용 결과

| Scene B | Scene C |
| --- | --- |
| ![B 마네킨에 최종 3단계 착장을 적용한 20스텝 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-mannequin-outfit-b-mira-stage3-v1-size-1280x1280-seed-62294-steps-20.png) | ![C 마네킨에 최종 3단계 착장을 적용한 20스텝 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-mannequin-outfit-c-mira-stage3-v1-size-1280x1280-seed-62294-steps-20.png) |

B에는 흰 재킷·넓은 바지와 양쪽 흰 스니커즈가 반영됐다. 도약 자세의 큰 형태는 남았지만 마네킨 입력보다 인물이 커지고 팔·다리의 위치가 달라졌다. 착장 반영과 포즈·크기 보존은 별도로 판단한다.

C에도 흰 재킷·넓은 바지와 양쪽 흰 스니커즈가 반영됐고, 앉은 자세의 큰 형태는 대체로 유지됐다. 두 결과 모두 마네킨의 짧은 머리가 남아 있으며, Mira의 얼굴·헤어 아이덴티티까지 완성한 결과는 아니다.

[B 착장 입력·프롬프트·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-mannequin-outfit-b-mira-stage3-v1-size-1280x1280-seed-62294-steps-20-result.json){ .lazy-source }

[C 착장 입력·프롬프트·출력 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-mannequin-outfit-c-mira-stage3-v1-size-1280x1280-seed-62294-steps-20-result.json){ .lazy-source }

## BFS·DeLight·Relight의 이전 테스트 흔적

아래 테스트는 현재 P7-5.4 최종 장면과 신규 분리·마네킨 경로가 아닌, 이전 카메라판과 그 파생 이미지를 입력으로 사용했다. 따라서 현재 경로의 다음 단계나 최종 합성 결과로 해석하지 않는다. 각 표는 당시 어떤 보정이 시도됐는지를 남긴 테스트 흔적이다.

### Studio DeLight로 캐릭터 조명을 중립화한다

Studio DeLight는 이전 경로에서 인물 이미지를 균일한 조명으로 바꾸는 데 사용했다. 아래 A·B·C는 각각 이전 경로의 캐릭터 입력에서 나온 결과다.

| Scene A | Scene B | Scene C |
| --- | --- | --- |
| ![Scene A Studio DeLight 캐릭터 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-cutout-identity-v1-size-1280x1280-seed-62294-steps-10.png) | ![Scene B Studio DeLight 캐릭터 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-b-size-1280x1280-seed-62294-steps-10.png) | ![Scene C Studio DeLight 캐릭터 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-c-shadow-stage2-outfit-no-closeup-v3-size-1280x1280-seed-62294-steps-10.png) |

[Studio DeLight 테스트 코드](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2509_studio_delight.py)

[Scene A Studio DeLight 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-cutout-identity-v1-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

[Scene B Studio DeLight 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-b-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

[Scene C Studio DeLight 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-studio-delight-character-c-shadow-stage2-outfit-no-closeup-v3-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

### BFS Head V5로 얼굴·헤어를 보정한다

BFS Head V5 테스트는 위와 같은 이전 DeLight 캐릭터를 Picture 1에, 45도 얼굴 참조를 Picture 2에 넣어 얼굴·헤어만 바꾸도록 지시했다. 착장·포즈·카메라·조명 참조는 추가하지 않았다.

| Scene A | Scene B | Scene C |
| --- | --- | --- |
| ![Scene A BFS Head V5 얼굴 헤어 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-a-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![Scene B BFS Head V5 얼굴 헤어 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-b-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![Scene C BFS Head V5 얼굴 헤어 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-c-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) |

[BFS Head V5 테스트 코드](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2511_bfs_head_identity.py)

[Scene A BFS Head V5 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-a-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

[Scene B BFS Head V5 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-b-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

[Scene C BFS Head V5 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2511-bfs-head-v5-delight-character-cutout-c-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

### Relight로 통합 장면의 방향광을 다시 적용한다

Relight 테스트는 이전 BFS 통합 장면 한 장에 방향광을 다시 부여한 단일 이미지 편집이다. 새 인물 참조나 마스크는 입력하지 않았다.

| Scene A | Scene B | Scene C |
| --- | --- | --- |
| ![Scene A Relight 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-a-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![Scene B Relight 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-b-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) | ![Scene C Relight 테스트 결과](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-c-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png) |

[Relight 테스트 코드](../../../assets/part-07/chapter-05/p7_5_5_qwen_edit_2509_relight.py)

[Scene A Relight 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-a-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

[Scene B Relight 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-b-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

[Scene C Relight 실행 기록](../../../assets/part-07/chapter-05/p7-5-5-qwen-2509-relight-scene-c-bfs-quarter-left-v1-size-1280x1280-seed-62294-steps-10-result.json){ .lazy-source }

## 체크리스트

- [ ] P7-5.4의 신규 `extras-audit-20260909-v1` A·B·C와 각 입력 JSON을 연결했는가?
- [ ] A·B·C Mira와 C 조연을 각각 분리하고, 가림 영역·경계 누락·두 C 마스크의 중복을 확인했는가?
- [ ] 원본 픽셀을 복사하는 분리 단계와 외형을 다시 생성하는 아이덴티티 적용 단계를 구분했는가?
- [ ] Mira는 Picture 2의 5.3 최종 3단계 착장을, 조연은 텍스트만 사용했는가?
- [ ] 원본 컷아웃의 직접 아이덴티티 적용과 마네킨을 거친 착장 1차 적용의 입력을 구분했는가?
- [ ] B·C 결과에서 착장 반영과 포즈·크기 보존을 따로 확인하고, 얼굴·헤어 아이덴티티가 아직 미완성임을 구분했는가?
- [ ] BFS·DeLight·Relight 테스트는 이전 입력으로 수행한 별도 기록이며, 현재 신규 경로의 후속 결과로 해석하지 않았는가?

## 출처와 참고 자료

- [Qwen-Image-Edit-2511 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer"}: 컷아웃 아이덴티티 적용과 마네킨 착장 편집에 사용한 공식 파이프라인의 입력 형식과 사용 예제를 확인합니다.
- [Grounding DINO Tiny 모델 카드](https://huggingface.co/IDEA-Research/grounding-dino-tiny){: target="_blank" rel="noopener noreferrer"} · [SAM 2 공식 저장소](https://github.com/facebookresearch/sam2){: target="_blank" rel="noopener noreferrer"}: 인물 탐색 상자와 정밀 마스크를 만드는 두 단계의 근거입니다.
- [Qwen-Image-Edit-2509 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2509){: target="_blank" rel="noopener noreferrer"} · [Studio DeLight 모델 카드](https://huggingface.co/prithivMLmods/QIE-2511-Studio-DeLight){: target="_blank" rel="noopener noreferrer"} · [BFS 모델 카드](https://huggingface.co/mr2along/BFS){: target="_blank" rel="noopener noreferrer"} · [Relight 모델 카드](https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Relight){: target="_blank" rel="noopener noreferrer"}: 이전 입력의 조명 중립화, 얼굴·헤어 보정, 방향광 재적용 테스트의 모델·LoRA 계약을 확인합니다.

모델 카드의 일반 기능 설명과 별도로, 이 절에서 실제로 사용한 입력 순서·파일 해시·seed·step·출력 경로는 각 `result.json`을 기준으로 확인합니다.
