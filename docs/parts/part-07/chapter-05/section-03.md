# P7-5.3 스토리보드 생성: Qwen으로 장면 구조를 만들기

> Section ID: `P7-5.3`
> Version: `v2026.08.27`

P7-5.2가 같은 인물의 얼굴·착장·전신 구조를 따로 준비했다면, 이 절은 그 참조를 넣기 전에 장면 자체의 카메라·공간·동작을 만든다. 캐릭터 포즈는 배경과 카메라 문장에서 분리한 `--pose-description`으로 새로 정의한다. 스토리보드의 인체나 지형 관계가 무너지면 그 이미지에서 얻은 depth도 같은 오류를 전달한다. 따라서 생성 결과는 완성 컷이 아니라 다음 입력에서 무엇을 보존하고 무엇을 다시 그릴지 확인하는 구조 참조다.

## Qwen은 장면 RGB와 상대 depth를 함께 만든다

현재 스토리보드 생성기는 Qwen Image를 사용한다. 한 번의 text-to-image 생성으로 장면 RGB를 만들고, 같은 RGB에서 상대 depth를 추출한다. depth 추정에 실패하면 RGB만 남기지 않아 두 파일이 항상 같은 장면을 가리키게 한다.

장면은 같은 `--pose-description`을 세 야외 장소에 넣는다. 1단계에서는 장소와 인물만 만들고 카메라 축은 아직 바꾸지 않는다.

| 장면 | 카메라와 공간 |
| --- | --- |
| A | 바다와 바위·바람 부는 풀밭이 보이는 해안 절벽 산책로 |
| B | 야생화·키 큰 풀이 있고 낮은 산등성이가 보이는 넓은 초원 |
| C | 나무·석재 포장·현대 조형물이 있는 도심 공원 |

아래는 같은 포즈 설명과 장면별 seed로 실제 생성한 1단계 RGB다. 세 장면 모두 후속 단계에서 카메라·공간 관계를 전달하는 기준 이미지이며, 아직 pitch와 yaw를 적용하지 않은 상태다.

| A 해안 절벽 산책로 | B 야생화 초원 | C 도심 공원 |
| --- | --- | --- |
| ![해안 절벽 산책로에서 공중 도약하는 인물 스토리보드](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-a-549191-seed-5420-steps-20.png) | ![야생화 초원에서 공중 도약하는 인물 스토리보드](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-b-837592-seed-5421-steps-20.png) | ![도심 공원에서 공중 도약하는 인물 스토리보드](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-c-481118-seed-5422-steps-20.png) |
| [result.json](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-a-549191-seed-5420-steps-20-result.json) | [result.json](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-b-837592-seed-5421-steps-20-result.json) | [result.json](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-c-481118-seed-5422-steps-20-result.json) |

기본값은 장면별 seed A `5420`, B `5421`, C `5422`, 정사각형 `1024×1024`, 20 step이다. seed는 품질을 높이는 수치가 아니라, 카메라·사지 분리·공간 여백의 다른 해석을 비교하는 조작 변수다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --scenes A B C --steps 20 --size 1024
```

GPU를 쓰기 전에는 `--dry-run`으로 예상 파일명을 확인할 수 있다. `--runs 3`은 시작 seed부터 연속 세 장면을 만든다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --scene A --seed 5420 --runs 3 --dry-run
```

생성기는 RGB PNG, 상대-depth PNG, 그리고 model·seed·step·pose description·prompt·`prompt_word_count`·두 출력의 SHA-256을 담은 `result.json`을 쓴다.

<details id="p7-5-3-storyboard-generator" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py" data-language="python">
<summary>Qwen A/B/C 스토리보드 생성 코드 보기</summary>
<div class="aibook-lazy-source__body">Qwen Image로 RGB를 만들고, 같은 PNG에서 상대 depth를 추출합니다.</div>
</details>

## 상대 depth와 캐릭터 참조는 다른 역할을 맡는다

상대 depth는 카메라, 프레이밍, 자세, 앞뒤 거리만 전달한다. RGB guide는 여기에 배경 색·조명·그림자도 함께 전달한다. 반면 P7-5.2의 2단계 전신 착장은 의상·전신 비례를, P7-5.7 정면 토르소는 얼굴·헤어·선과 음영을 맡는다.

Qwen Edit 생성기는 이 세 입력을 고정 순서로 받는다.

1. guide: 카메라·프레이밍·자세·공간 정보
2. 2단계 전신 착장: 재킷·이너·팬츠·신발과 전신 비례
3. 정면 토르소: 얼굴·헤어·선·색·음영

guide가 RGB인지 depth인지만 바꾸면 구조만 남길 때와 구조·조명까지 함께 남길 때를 비교할 수 있다. `--guide`는 필수이며, 기본 전신 착장·토르소 대신 다른 입력을 비교하려면 `--outfit`, `--torso`를 바꾼다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_refine_storyboard_four_outputs.py \
  --guide path/to/storyboard-depth.png \
  --stage outfit --guide-type depth --steps 10 --size 1024
```

<details id="p7-5-3-depth-character-scene-refine" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_3_refine_storyboard_four_outputs.py" data-language="python">
<summary>Qwen Edit로 guide와 캐릭터 참조를 결합하는 코드 보기</summary>
<div class="aibook-lazy-source__body">guide·전신 착장·정면 토르소의 역할을 분리하고 결과 조건을 `result.json`에 기록합니다.</div>
</details>

## 인물 제거에는 재생성 영역을 먼저 정한다

장면 전체를 입력한 Qwen Edit에 `Remove the person from Image 1.`만 지시했을 때, 인물은 남고 배경의 색조만 달라졌다. 편집할 대상이 화면에서 작지 않더라도 전역 지시만으로는 어떤 픽셀을 다시 그릴지 고정되지 않는다. 배경판을 만들 때는 인물 영역만 흰색으로 표시한 마스크를 함께 주고, 흰색 영역만 인페인트해야 한다.

이 실험은 Apache-2.0인 Grounding DINO와 SAM 2.1 Hiera Small을 순차로 사용했다. 먼저 Grounding DINO가 `a woman` 또는 `a person`이라는 텍스트로 인물 상자를 찾고, SAM 2.1 Small이 그 상자 안에서 전신 윤곽을 마스크로 다듬는다. 두 모델을 동시에 GPU에 올리지 않으므로, 마스크 PNG를 저장한 뒤 Qwen 인페인트를 별도 실행할 수 있다.

| 1단계 장면 | 인물 마스크 오버레이 |
| --- | --- |
| ![해안 절벽 장면에서 무용 도약을 하는 인물](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-a-character-plus90-character-features-dancer-leap-v4-seed-62294-steps-10.png) | ![빨간색으로 인물 마스크가 겹쳐진 해안 절벽 장면](../../../assets/part-07/chapter-05/p7-5-3-sam2-person-mask-dancer-leap-v1-overlay.png) |
| [1단계 result.json](../../../assets/part-07/chapter-05/p7-5-3-qwen-storyboard-scene-a-character-plus90-character-features-dancer-leap-v4-seed-62294-steps-10-result.json) | [마스크 PNG](../../../assets/part-07/chapter-05/p7-5-3-sam2-person-mask-dancer-leap-v1.png) · [result.json](../../../assets/part-07/chapter-05/p7-5-3-sam2-person-mask-dancer-leap-v1-result.json) |

오버레이의 빨간 영역은 Qwen 인페인트에서 다시 그릴 인물이고, 검은 영역은 보존할 배경이다. 이 사례에서는 머리·손끝·몸통·양다리·발끝이 모두 빨간 영역에 들어갔다. 상자는 인물을 찾는 힌트일 뿐 최종 제거 영역이 아니므로, 결과를 확인할 때는 상자보다 마스크 외곽을 검수한다.

<details id="p7-5-3-person-mask-generator" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_3_generate_person_mask.py" data-language="python">
<summary>Grounding DINO와 SAM 2.1로 인물 마스크를 만드는 코드 보기</summary>
<div class="aibook-lazy-source__body">텍스트 검출 상자를 SAM 2.1 Small에 전달해 Qwen 인페인트용 흰색 인물 마스크와 검수 오버레이를 저장합니다.</div>
</details>

## 2단계 pitch와 3단계 yaw를 순서대로 적용한다

멀티플 앵글 LoRA는 한 번에 yaw 또는 pitch 한 축만 적용한다. 그래서 2단계에서는 1단계 PNG에 pitch만 적용하고, 3단계에서는 그 출력 PNG에 yaw만 적용한다. 세 장면은 A=로우앵글·정면 yaw, B=하이앵글·좌측 45° yaw, C=로우앵글·우측 45° yaw 순서로 구성한다.

| 장면 | 2단계 pitch | 3단계 yaw |
| --- | --- | --- |
| A 해안 절벽 산책로 | 로우앵글 | 정면 |
| B 야생화 초원 | 하이앵글 | 좌측 45° |
| C 도심 공원 | 로우앵글 | 우측 45° |

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --reference path/to/stage1-scene-a.png --stage pitch --scene A
```

같은 생성기에서 `--stage yaw --scene A --reference path/to/stage2-a.png`처럼 3단계를 실행한다. 하나의 실행에서는 pitch와 yaw를 함께 지시하지 않는다.

## 결과는 유지와 이탈을 함께 읽는다

생성 결과를 볼 때는 한 장이 좋거나 나쁘다는 판정보다 입력 역할별로 무엇이 남았는지 확인한다. depth guide에서는 카메라·자세·인물 크기가, RGB guide에서는 배경 색·조명·그림자가 추가로 유지되는지를 비교한다. 두 경우 모두 얼굴·헤어와 의상이 참조 이미지에서 지나치게 바뀌지 않는지도 함께 본다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 구조 | guide의 카메라·포즈·공간 관계가 결과에서 읽히는가? |
| 역할 | guide, 전신 착장, 토르소가 서로의 정보를 다시 지정하지 않는가? |
| RGB와 depth | 색·조명·그림자까지 보존할 필요가 있는가, 아니면 구조만 필요한가? |
| 재현 | model, seed, step, 입력 파일, prompt가 `result.json`에 남아 있는가? |
| 다음 비교 | 장면·소품·동작 중 어느 조건이 유지됐고 어느 조건이 달라졌는가? |

## 출처와 참고 자료

- Qwen 실행 조건과 입력·출력 기록은 이 절에서 연결한 로컬 `result.json`에서 확인한다.
- 인물 상자 검출에 사용한 Grounding DINO는 Apache-2.0으로 배포된다. [Grounding DINO 공식 저장소](https://github.com/IDEA-Research/GroundingDINO){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-27)
- 마스크 정밀화에 사용한 SAM 2.1 Hiera Small의 모델 카드와 가중치는 Apache-2.0으로 표시된다. [SAM 2.1 Hiera Small 모델 카드](https://huggingface.co/facebook/sam2.1-hiera-small){: target="_blank" rel="noopener noreferrer"}, [SAM 2 공식 저장소](https://github.com/facebookresearch/sam2){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-27)
- 얼굴·전신 참조의 역할 분리는 [P7-5.2](section-02.md)와 [P7-5.7](section-07.md)에서 확인한다.
