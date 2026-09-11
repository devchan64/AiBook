# P7-5.4 라인아트 구도에서 스토리보드 장면까지

> Section ID: `P7-5.4`
> Version: `v2026.09.11`

스토리보드 장면에서는 구도, 캐릭터 외형, 주변 대상의 배치를 각각 확인해야 한다. 이 절은 **라인아트 구도 → Mira 이식 → 주변 인물·동물 추가**로 장면을 만든다. 직전 결과를 다음 입력으로 이어 쓰며, 새로 반영된 특징과 함께 달라진 부분을 비교한다.

| 단계 | 입력 | 비교할 내용 |
| --- | --- | --- |
| 라인아트 구도 | 텍스트 | 카메라 높이·동작·배경 공간·여백 |
| Mira 이식 | 구도판, Mira 전신 착장 참조 | 구도 유지와 얼굴·헤어·착장·화풍의 반영 |
| 주변 대상 추가 | Mira 이식 결과 한 장 | 대상의 종류·자세·위치와 기존 인물·배경의 변화 |

아래 이미지는 2026년 9월 9일에 세 생성기로 A·B·C의 전 단계를 실행한 결과다. 모두 1280×1280·20스텝·true CFG `4.0`이며, 장면별 seed는 A `5420`, B `5421`, C `5422`다. PNG와 짝을 이루는 `result.json`에 실제 입력·프롬프트·모델·설정·해시를 남겼다.

## 라인아트에서 카메라·동작·공간을 확인한다

첫 단계는 `Qwen/Qwen-Image-2512`에 텍스트만 넣는다. Mira 참조를 쓰지 않고 카메라 높이, 동작, 배경 공간을 평가할 구도판을 만든다. 생성기의 `STYLE_PROMPT`는 공통 화풍, `SCENE_PROMPTS`는 장면별 구도와 사건을 맡는다. 아래 결과의 실행 이름은 `lineart-audit-20260909-v1`이다.

- Scene A: 지면 높이에서 카메라를 향해 달리는 인물과 열린 하늘
- Scene B: 석양의 숲 공터에서 하는 grand jeté — 공중에서 두 다리를 앞뒤로 크게 벌리는 도약
- Scene C: 도시가 내려다보이는 언덕에서 책을 읽는 두 사람

| Scene A · 도시 달리기 | Scene B · 숲 공터 도약 | Scene C · 언덕 독서 |
| --- | --- | --- |
| ![Qwen Image 2512으로 만든 Scene A 라인아트 구도](../../../assets/part-07/chapter-05/p7-5-4-qwen-image-2512-scene-a-lineart-audit-20260909-v1-size-1280x1280-seed-5420-steps-20.png) | ![Qwen Image 2512으로 만든 Scene B 라인아트 구도](../../../assets/part-07/chapter-05/p7-5-4-qwen-image-2512-scene-b-lineart-audit-20260909-v1-size-1280x1280-seed-5421-steps-20.png) | ![Qwen Image 2512으로 만든 Scene C 라인아트 구도](../../../assets/part-07/chapter-05/p7-5-4-qwen-image-2512-scene-c-lineart-audit-20260909-v1-size-1280x1280-seed-5422-steps-20.png) |

[Scene A line-art result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-image-2512-scene-a-lineart-audit-20260909-v1-size-1280x1280-seed-5420-steps-20-result.json){ .lazy-source }

[Scene B line-art result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-image-2512-scene-b-lineart-audit-20260909-v1-size-1280x1280-seed-5421-steps-20-result.json){ .lazy-source }

[Scene C line-art result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-image-2512-scene-c-lineart-audit-20260909-v1-size-1280x1280-seed-5422-steps-20-result.json){ .lazy-source }

A에서는 전경 신발의 밑창이 크게 강조됐다. 앞부분과 뒤꿈치를 나누어 보고, 다음 편집에서도 이 원근 표현이 이어지는지 비교한다. B에서는 도약 자세, 열린 하늘, 나무와 양치식물이 만드는 공간을 확인한다. 선 중심의 그림을 요청했지만 색·명암과 석양 조명도 생성됐다. 따라서 라인아트를 무채색 윤곽선만의 출력으로 해석하지 않는다. C에서는 두 인물·책·난간·먼 도시의 배치를 기준으로 삼는다.

## 구도를 이어 쓰며 Mira의 외형을 비교한다

구도판을 Picture 1, [P7-5.3의 3단계 재킷 착장 참조](../../../assets/part-07/chapter-05/p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png)를 Picture 2로 넣어 `Qwen-Image-Edit-2511`로 편집한다. Picture 1은 포즈·카메라·배경을, Picture 2는 Mira의 얼굴·헤어·착장·선화·색을 맡긴다. 이 역할은 프롬프트로 요청하는 조건이며, 이미지 일부를 잠그는 기능은 아니다.

A의 달리는 여성, B의 도약하는 여성, C의 왼쪽 독자를 Mira로 바꾼다. C의 오른쪽 독자는 별도 참조 없이 기존 인물과 배경 관계를 유지하도록 요청한다. 아래 `mira-audit-20260909-v1`은 각 장면의 새 라인아트와 같은 착장 참조를 사용한 결과다.

| Scene A · 도시 달리기 | Scene B · 숲 공터 도약 | Scene C · 언덕 독서 |
| --- | --- | --- |
| ![Mira 아이덴티티와 화풍을 이식한 Scene A](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-mira-audit-20260909-v1-size-1280x1280-seed-5420-steps-20.png) | ![Mira 아이덴티티와 화풍을 이식한 Scene B](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-mira-audit-20260909-v1-size-1280x1280-seed-5421-steps-20.png) | ![Mira 아이덴티티와 화풍을 이식한 Scene C](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-mira-audit-20260909-v1-size-1280x1280-seed-5422-steps-20.png) |

[Scene A Mira 이식 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-mira-audit-20260909-v1-size-1280x1280-seed-5420-steps-20-result.json){ .lazy-source }

[Scene B Mira 이식 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-mira-audit-20260909-v1-size-1280x1280-seed-5421-steps-20-result.json){ .lazy-source }

[Scene C Mira 이식 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-mira-audit-20260909-v1-size-1280x1280-seed-5422-steps-20-result.json){ .lazy-source }

구도판과는 포즈·배경을, 전신 참조와는 외형을 비교한다. 청록 머리와 흰 재킷의 반영만으로 전체 외형이 보존됐다고 판단하지 않는다.

| 장면 | 반영된 특징 | 차이와 확인 한계 |
| --- | --- | --- |
| A | 청록 단발, 흰 크롭 재킷, 회색 이너, 청록 팬츠 | 재킷 소매가 걷힌 형태이며 얼굴의 눈·윤곽 표현이 달라짐. 신발 밑창이 크게 보이는 구도라 참조 정면만으로 밑창 무늬의 일치를 판단하기 어려움 |
| B | 청록 머리, 흰 재킷, 딥틸 팬츠와 도약 자세 | 머리카락이 단발보다 길어지고, 스니커즈가 발레화 같은 형태로 바뀜. 바지 끝이 발목 위로 올라감 |
| C | 청록 단발, 흰 재킷, 딥틸 하의와 독서 자세. 오른쪽 독자와 배경의 배치 | 바지 밑단 아래로 발목이 드러남. 신발이 참조의 흰 캔버스화와 다른 회색 운동화 형태이며, 얼굴의 눈·윤곽 표현도 달라짐 |

이 차이는 다음 단계에서 주변 대상을 추가한다고 자동으로 교정되지 않는다. 최종 장면에서도 전신 참조와 외형을 다시 대조한다.

## 주변 대상의 배치와 기존 장면의 변화를 나누어 본다

주변 대상 추가에는 Mira 이식 결과 한 장만 Image 1로 넣는다. 아래 `extras-audit-20260909-v1`은 각 장면의 새 Mira 이식 PNG를 그대로 입력한 결과다. 추가 대상의 수·자세·위치와 기존 인물·배경의 보존을 따로 비교한다.

| Scene A · 도시 달리기 | Scene B · 숲 공터 도약 | Scene C · 언덕 독서 |
| --- | --- | --- |
| ![캐주얼 복장으로 달리는 주변 인물을 추가한 Scene A](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-extras-audit-20260909-v1-size-1280x1280-seed-5420-steps-20.png) | ![왼쪽 아래 토끼와 오른쪽 나무 밑 다람쥐를 추가한 Scene B](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-extras-audit-20260909-v1-size-1280x1280-seed-5421-steps-20.png) | ![난간 기둥 두 곳과 왼쪽 아래 바위에 새 세 마리를 추가한 Scene C](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-extras-audit-20260909-v1-size-1280x1280-seed-5422-steps-20.png) |

[Scene A 주변 인물 보강 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-a-extras-audit-20260909-v1-size-1280x1280-seed-5420-steps-20-result.json){ .lazy-source }

[Scene B 작은 동물 배치 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-b-extras-audit-20260909-v1-size-1280x1280-seed-5421-steps-20-result.json){ .lazy-source }

[Scene C 새 배치 result.json](../../../assets/part-07/chapter-05/p7-5-4-qwen-2511-lineart-scene-c-extras-audit-20260909-v1-size-1280x1280-seed-5422-steps-20-result.json){ .lazy-source }

**Scene A — 주변 인물.** 프롬프트는 `Add several pedestrians and several people running in casual clothing to Image 1.`이다. 인물 수·상대 크기·기존 장면 보존은 별도로 지정하지 않았다. 캐주얼 복장의 여섯 명이 추가됐지만 대부분 달리는 자세여서, 행인과 달리는 사람의 구분이 뚜렷한지는 따로 판단해야 한다. Mira의 구도·착장은 대체로 유지됐고 배경 나무·구름의 세부 표현은 달라졌다.

**Scene B — 작은 동물.** 토끼는 왼쪽 아래 양치식물 옆 공터 바닥에 앉히고, 다람쥐는 오른쪽 나무 밑 지면에 서도록 요청했다. 결과에서 토끼는 지정한 지면에, 다람쥐는 나무뿌리 위에 앉아 있다. 두 동물은 Mira와 떨어져 있지만 다람쥐의 자세·지지 위치는 요청과 다르다. Mira의 긴 머리·발레화 형태·발목 노출도 이전 단계에서 이어졌다.

**Scene C — 앉아 있는 새.** 세 마리의 위치를 남성 독자 오른쪽의 사각 난간 기둥, 오른쪽 가장자리의 상단 나무 난간, Mira 옆 왼쪽 아래 바위로 각각 지정했다. 결과에서는 난간 기둥 두 곳과 바위에 앉아 있으며, 오른쪽 새는 가로 난간 대신 끝 기둥에 놓였다. 하늘에 떠 있는 새나 분리된 가지는 보이지 않는다. 조연의 옷 주름과 배경 선도 바뀌었으므로 배치 유지와 세부 픽셀 보존을 구분한다.

B의 다람쥐와 C의 오른쪽 새를 보고 종류·자세·위치가 각각 요청과 일치하는지 표시해 보자. 동물이 생성됐거나 새가 앉아 있다는 관찰만으로 정확한 지지 위치까지 맞았다고 판정할 수는 없다.

## 직전 단계의 PNG를 연결해 재실행한다

명령은 필요한 패키지가 설치된 `.venv`를 사용해 저장소 루트에서 실행한다. 세 생성기는 ComfyUI 서버 없이 Diffusers로 직접 실행하며, CUDA GPU와 BF16 순차 CPU 오프로딩을 사용한다. 패키지 구성은 결과 JSON의 `runtime.packages`에서 확인한다. 모델은 `.tmp/download/huggingface/hub` 캐시에서 읽으며, 준비되지 않았다면 명령에 `--allow-download`를 추가한다.

출력은 `/tmp/p7-5-4-practice`에 저장한다. 이미 같은 출력이 있으면 중단되므로 새 `--output-dir` 또는 `--run-label`을 지정하고 후속 입력 경로도 함께 바꾼다. `/tmp`는 임시 공간이므로 보관할 PNG와 JSON은 함께 별도 저장한다. 이전 실행과 주요 설정이 같아도 픽셀·파일 해시가 완전히 같지 않았으므로, 이전 기록을 덮어쓰지 않고 실행별로 보관한다.

### 라인아트 생성

`--scene`으로 장면을 선택한다. 구도 표현의 영향을 볼 때는 seed·스텝을 고정하고 `--prompt`의 표현 하나를 바꾼다. 반복 횟수의 영향을 볼 때는 나머지 조건을 고정하고 `--steps`만 바꾼다.

[P7-5.4 라인아트 씬 생성기](../../../assets/part-07/chapter-05/p7_5_4_qwen_image_2512_generate_lineart_scene.py)

```bash
assets=docs/assets/part-07/chapter-05
for scene in a b c; do
  .venv/bin/python "$assets/p7_5_4_qwen_image_2512_generate_lineart_scene.py" \
    --scene "$scene" --run-label lineart-audit-20260909-v1 \
    --size 1280 --steps 20 --output-dir /tmp/p7-5-4-practice || break
done
```

### Mira 이식

`--lineart`에 방금 생성한 구도판을, `--mira-reference`에 전신 착장 참조를 지정한다. 기본 입력에 의존하면 이전 구도판을 읽을 수 있으므로 경로를 직접 연결한다. `--scenes b c`로 기본 입력의 여러 장면을 한 번 로드한 모델에서 처리할 수도 있지만, 아래처럼 새 구도판을 지정할 때는 한 장면씩 실행한다.

[라인아트 Mira 아이덴티티 이식 생성기](../../../assets/part-07/chapter-05/p7_5_4_qwen_edit_2511_apply_mira_to_lineart.py)

```bash
assets=docs/assets/part-07/chapter-05
output=/tmp/p7-5-4-practice
for pair in a:5420 b:5421 c:5422; do
  scene=${pair%:*}
  seed=${pair#*:}
  .venv/bin/python "$assets/p7_5_4_qwen_edit_2511_apply_mira_to_lineart.py" \
    --scenes "$scene" \
    --lineart "$output/p7-5-4-qwen-image-2512-scene-$scene-lineart-audit-20260909-v1-size-1280x1280-seed-$seed-steps-20.png" \
    --mira-reference "$assets/p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png" \
    --run-label mira-audit-20260909-v1 --size 1280 --steps 20 \
    --output-dir "$output" || break
done
```

### 주변 인물·동물 추가

`--scene-image`에 직전 Mira 이식 결과를 지정한다. A·B·C는 각각 주변 인물, 토끼·다람쥐, 새를 추가한다. Mira 이식과 주변 대상 추가 명령에 `--dry-run`을 붙이면 모델을 실행하지 않고 입력·프롬프트·출력 경로를 확인할 수 있다.

[Mira 장면 주변 인물·오브젝트 보강 생성기](../../../assets/part-07/chapter-05/p7_5_4_qwen_edit_2511_enrich_mira_scene_extras.py)

```bash
assets=docs/assets/part-07/chapter-05
output=/tmp/p7-5-4-practice
.venv/bin/python "$assets/p7_5_4_qwen_edit_2511_enrich_mira_scene_extras.py" \
  --scenes a \
  --scene-image "$output/p7-5-4-qwen-2511-lineart-scene-a-mira-audit-20260909-v1-size-1280x1280-seed-5420-steps-20.png" \
  --run-label extras-audit-20260909-v1 --size 1280 --steps 20 \
  --output-dir "$output"
```

```bash
assets=docs/assets/part-07/chapter-05
output=/tmp/p7-5-4-practice
.venv/bin/python "$assets/p7_5_4_qwen_edit_2511_enrich_mira_scene_extras.py" \
  --scenes b \
  --scene-image "$output/p7-5-4-qwen-2511-lineart-scene-b-mira-audit-20260909-v1-size-1280x1280-seed-5421-steps-20.png" \
  --run-label extras-audit-20260909-v1 --size 1280 --steps 20 \
  --output-dir "$output"
```

```bash
assets=docs/assets/part-07/chapter-05
output=/tmp/p7-5-4-practice
.venv/bin/python "$assets/p7_5_4_qwen_edit_2511_enrich_mira_scene_extras.py" \
  --scenes c \
  --scene-image "$output/p7-5-4-qwen-2511-lineart-scene-c-mira-audit-20260909-v1-size-1280x1280-seed-5422-steps-20.png" \
  --run-label extras-audit-20260909-v1 --size 1280 --steps 20 \
  --output-dir "$output"
```

전체 실행 점검 기록에는 소스코드 해시, 실제 명령, 아홉 결과의 입력·출력 해시와 설정, 시각 검토를 모았다. 위 명령은 실습용 출력 폴더를 제외하면 기록과 같은 입력 연결·설정을 사용한다. 실행과 산출물 연결의 검증 통과는 외형·위치의 완전한 재현을 뜻하지 않는다.

[전체 실행 점검 기록](../../../assets/part-07/chapter-05/p7-5-4-generation-audit-20260909-v1.json){ .lazy-source }

## 체크리스트

- [ ] Scene A·B·C의 라인아트 구도는 화풍 상수와 장면별 프롬프트를 분리해 생성했는가?
- [ ] 라인아트 결과에서는 카메라·동작·배경 공간을, 이후 편집 결과에서는 Mira·착장·오브젝트를 각각 검수하는가?
- [ ] 편집 단계가 구도를 다시 바꾸지 않고 구도판을 유지하는지 입력 순서와 결과 이미지로 확인하는가?
- [ ] 머리색·착장색의 반영과 머리 길이·바지 길이·신발 형태의 보존을 구분해 기록했는가?
- [ ] 재실행 출력 경로가 기존 자산과 겹치지 않으며, 후속 단계가 실제로 비교하려는 PNG를 입력으로 사용하는가?
- [ ] 각 단계의 PNG와 `result.json`을 함께 보관해 어떤 입력과 설정이 결과를 만들었는지 추적할 수 있는가?

## 출처와 참고 자료

- Qwen, [Qwen-Image-2512 모델 카드](https://huggingface.co/Qwen/Qwen-Image-2512){: target="_blank" rel="noopener noreferrer" }, Hugging Face, 확인일: 2026-09-11.
- Qwen, [Qwen-Image 컬렉션](https://huggingface.co/collections/Qwen/qwen-image){: target="_blank" rel="noopener noreferrer" }, Hugging Face, 확인일: 2026-09-11.
- Qwen, [Qwen-Image-Edit-2511 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2511){: target="_blank" rel="noopener noreferrer" }, Hugging Face, 확인일: 2026-09-11.
