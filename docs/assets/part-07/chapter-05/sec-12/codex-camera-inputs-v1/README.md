# P7-5.12 새 인물·카메라 입력 이미지

Codex 내장 ImageGen으로 생성한 가상 남성·여성·유아 각 1명의 상반신 이미지다. 인물별 세로 3단계 × 가로 5단계로 15장씩, 총 45장을 구성한다. 배경·포즈·표정은 생성 조건에 포함했다.

- 최종 입력: `*-512.png`, 512×512 PNG.
- 개별 생성 기록: 이미지와 같은 이름의 `*-512.json` 45개. 인물·앵글·프롬프트·최종 경로·해상도·해시·축소 조건을 기록한다. 경로는 이 디렉터리를 기준으로 해석하며 `source`는 최초 생성 위치의 이력이다.
- 생성 원본 파일은 사용자 요청으로 삭제했다. 원본 해상도·해시와 최초 생성 위치는 이력으로만 남긴다. 최종 이미지는 정사각형 원본 전체를 LANCZOS 축소했으며 추가 크롭은 하지 않았다.
- [전체 생성 프롬프트·앵글·파일 해시](generation-manifest.json)
- 세로: 로우(`low`)·눈높이(`level`)·엘리베이티드(`elevated`).
- 가로: −90°·−45°·0°·+45°·+90°. 기존 [15방향 생성기의 분류](../../sec-02/p7_5_2_qwen_edit_2511_generate_mira_torso_multiview.py)를 따른다.

각도는 생성 요청의 범주이며 측정한 카메라 좌표가 아니다. 인물별 외형 설명을 반복했지만 정확한 동일인이나 3D 회전을 보장하지 않는다. 배경 세부·포즈·표정도 달라지므로 앵글만을 독립 변수로 둔 통제 실험 자료는 아니다. 기존 193쌍 학습 자료에 포함하지 않은 새로운 합성 입력이며, 이 이미지에 대한 BFS LoRA 편집 평가는 아직 수행하지 않았다.

## 남성 · 카페

| 로우 · -90° | 로우 · -45° | 로우 · +0° | 로우 · +45° | 로우 · +90° |
| --- | --- | --- | --- | --- |
| [![man-low-minus-90](man-low-minus-90-512.png)](man-low-minus-90-512.png) | [![man-low-minus-45](man-low-minus-45-512.png)](man-low-minus-45-512.png) | [![man-low-zero](man-low-zero-512.png)](man-low-zero-512.png) | [![man-low-plus-45](man-low-plus-45-512.png)](man-low-plus-45-512.png) | [![man-low-plus-90](man-low-plus-90-512.png)](man-low-plus-90-512.png) |

| 눈높이 · -90° | 눈높이 · -45° | 눈높이 · +0° | 눈높이 · +45° | 눈높이 · +90° |
| --- | --- | --- | --- | --- |
| [![man-level-minus-90](man-level-minus-90-512.png)](man-level-minus-90-512.png) | [![man-level-minus-45](man-level-minus-45-512.png)](man-level-minus-45-512.png) | [![man-level-zero](man-level-zero-512.png)](man-level-zero-512.png) | [![man-level-plus-45](man-level-plus-45-512.png)](man-level-plus-45-512.png) | [![man-level-plus-90](man-level-plus-90-512.png)](man-level-plus-90-512.png) |

| 엘리베이티드 · -90° | 엘리베이티드 · -45° | 엘리베이티드 · +0° | 엘리베이티드 · +45° | 엘리베이티드 · +90° |
| --- | --- | --- | --- | --- |
| [![man-elevated-minus-90](man-elevated-minus-90-512.png)](man-elevated-minus-90-512.png) | [![man-elevated-minus-45](man-elevated-minus-45-512.png)](man-elevated-minus-45-512.png) | [![man-elevated-zero](man-elevated-zero-512.png)](man-elevated-zero-512.png) | [![man-elevated-plus-45](man-elevated-plus-45-512.png)](man-elevated-plus-45-512.png) | [![man-elevated-plus-90](man-elevated-plus-90-512.png)](man-elevated-plus-90-512.png) |

## 여성 · 도서관

| 로우 · -90° | 로우 · -45° | 로우 · +0° | 로우 · +45° | 로우 · +90° |
| --- | --- | --- | --- | --- |
| [![woman-low-minus-90](woman-low-minus-90-512.png)](woman-low-minus-90-512.png) | [![woman-low-minus-45](woman-low-minus-45-512.png)](woman-low-minus-45-512.png) | [![woman-low-zero](woman-low-zero-512.png)](woman-low-zero-512.png) | [![woman-low-plus-45](woman-low-plus-45-512.png)](woman-low-plus-45-512.png) | [![woman-low-plus-90](woman-low-plus-90-512.png)](woman-low-plus-90-512.png) |

| 눈높이 · -90° | 눈높이 · -45° | 눈높이 · +0° | 눈높이 · +45° | 눈높이 · +90° |
| --- | --- | --- | --- | --- |
| [![woman-level-minus-90](woman-level-minus-90-512.png)](woman-level-minus-90-512.png) | [![woman-level-minus-45](woman-level-minus-45-512.png)](woman-level-minus-45-512.png) | [![woman-level-zero](woman-level-zero-512.png)](woman-level-zero-512.png) | [![woman-level-plus-45](woman-level-plus-45-512.png)](woman-level-plus-45-512.png) | [![woman-level-plus-90](woman-level-plus-90-512.png)](woman-level-plus-90-512.png) |

| 엘리베이티드 · -90° | 엘리베이티드 · -45° | 엘리베이티드 · +0° | 엘리베이티드 · +45° | 엘리베이티드 · +90° |
| --- | --- | --- | --- | --- |
| [![woman-elevated-minus-90](woman-elevated-minus-90-512.png)](woman-elevated-minus-90-512.png) | [![woman-elevated-minus-45](woman-elevated-minus-45-512.png)](woman-elevated-minus-45-512.png) | [![woman-elevated-zero](woman-elevated-zero-512.png)](woman-elevated-zero-512.png) | [![woman-elevated-plus-45](woman-elevated-plus-45-512.png)](woman-elevated-plus-45-512.png) | [![woman-elevated-plus-90](woman-elevated-plus-90-512.png)](woman-elevated-plus-90-512.png) |

## 유아 · 놀이방

| 로우 · -90° | 로우 · -45° | 로우 · +0° | 로우 · +45° | 로우 · +90° |
| --- | --- | --- | --- | --- |
| [![toddler-low-minus-90](toddler-low-minus-90-512.png)](toddler-low-minus-90-512.png) | [![toddler-low-minus-45](toddler-low-minus-45-512.png)](toddler-low-minus-45-512.png) | [![toddler-low-zero](toddler-low-zero-512.png)](toddler-low-zero-512.png) | [![toddler-low-plus-45](toddler-low-plus-45-512.png)](toddler-low-plus-45-512.png) | [![toddler-low-plus-90](toddler-low-plus-90-512.png)](toddler-low-plus-90-512.png) |

| 눈높이 · -90° | 눈높이 · -45° | 눈높이 · +0° | 눈높이 · +45° | 눈높이 · +90° |
| --- | --- | --- | --- | --- |
| [![toddler-level-minus-90](toddler-level-minus-90-512.png)](toddler-level-minus-90-512.png) | [![toddler-level-minus-45](toddler-level-minus-45-512.png)](toddler-level-minus-45-512.png) | [![toddler-level-zero](toddler-level-zero-512.png)](toddler-level-zero-512.png) | [![toddler-level-plus-45](toddler-level-plus-45-512.png)](toddler-level-plus-45-512.png) | [![toddler-level-plus-90](toddler-level-plus-90-512.png)](toddler-level-plus-90-512.png) |

| 엘리베이티드 · -90° | 엘리베이티드 · -45° | 엘리베이티드 · +0° | 엘리베이티드 · +45° | 엘리베이티드 · +90° |
| --- | --- | --- | --- | --- |
| [![toddler-elevated-minus-90](toddler-elevated-minus-90-512.png)](toddler-elevated-minus-90-512.png) | [![toddler-elevated-minus-45](toddler-elevated-minus-45-512.png)](toddler-elevated-minus-45-512.png) | [![toddler-elevated-zero](toddler-elevated-zero-512.png)](toddler-elevated-zero-512.png) | [![toddler-elevated-plus-45](toddler-elevated-plus-45-512.png)](toddler-elevated-plus-45-512.png) | [![toddler-elevated-plus-90](toddler-elevated-plus-90-512.png)](toddler-elevated-plus-90-512.png) |
