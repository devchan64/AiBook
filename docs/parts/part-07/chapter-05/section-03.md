# P7-5.3 스토리보드 생성: FLUX 후보를 guide 이전에 검수하기

> Section ID: `P7-5.3`
> Version: `v2026.08.08`

이 절의 목적은 예쁜 한 장을 고르는 일이 아니라, 이후 단계가 믿고 읽을 수 있는 장면 기준을 만드는 일이다. 스토리보드의 인체·발·절벽·앞뒤 관계가 무너지면, 그 PNG에서 뽑은 Canny·상대 depth도 같은 오류를 구조 조건으로 전달한다. 따라서 후보 생성, 사람 승인, guide 추출, 참조 비교를 차례로 분리하며, 형상이 읽히지 않는 출력은 guide로 넘기지 않고 폐기한다.

## FLUX 후보는 장면 계약과 분리해 검수한다

현재 생성 경로는 FLUX.2 Klein 4B만 사용한다. 인체·가림·접지 검수를 통과한 PNG만 다음 guide 단계로 넘긴다.

| 고정 항목 | FLUX.2 Klein 4B |
| --- | --- |
| 기본 seed | `5420` |
| 해상도·step | `768 x 1152`, 캐릭터 3 step + 배경 3 step |
| 인물 | 턱선 길이 단발, 긴 머리·포니테일 제외 |
| 자세·시선 | 넓은 하이 앵글 뷰에서 인물 전신과 협곡 바닥·절벽 지형을 함께 보인다. 정확한 카메라 거리·탑뷰 각도는 고정하지 않는다. 인물은 앞쪽 진행 방향으로 뛰어 나가는 현대무용수다. 한 다리는 앞쪽으로 뻗고 다른 다리는 뒤로 길게 뻗는다. 눈과 얼굴은 화면 오른쪽을 본다. 팔의 개수·방향·위치는 별도로 지정하지 않는다. |
| 공간 | 밝은 사암·자갈의 자연 계곡 바닥이 가까운 절벽 밑으로 이어짐. 기암절벽은 인물의 양옆과 뒤에 즉시 솟아 좁은 협곡을 이루되, 인물 외곽과는 좁은 보이는 간격을 둠 |

아래 [FLUX 스토리보드 코드](../../../assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py)는 후보 PNG만 만든다. 첫 단계는 중립 배경에서 인물과 동작을 prompt로만 만들고, 둘째 단계는 그 생성 결과만 입력으로 받아 인물의 포즈·실루엣·비율을 바꾸지 않은 채 협곡 배경만 추가한다. 얼굴·전신·복장 같은 외부 캐릭터 특징 PNG는 어느 단계에도 입력하지 않는다. 두 단계의 기본값은 각각 3 step이며, `--character-steps`와 `--background-steps`로 따로 바꿀 수 있다. 생성 성공은 통과가 아니며, 다음 질문에 모두 답할 수 있을 때만 PNG를 승인한다.

동작 자체를 먼저 검수하려면 `--character-only`로 1차 캐릭터 PNG만 만들 수 있다. 이 옵션은 2차 배경 생성을 호출하지 않으므로, 동작·시선·전신 실루엣의 오류를 협곡 배경 재해석과 분리해 확인할 수 있다.

1차를 통과한 캐릭터 PNG만 2차에 넣으려면 `--character-from`에 그 파일을 명시한다. 이 옵션은 1차를 다시 만들지 않고, 해당 PNG의 인물 포즈·실루엣·복장을 유지한 채 협곡 배경만 생성한다.

이미 검수할 배경 후보가 있다면 `--background-from`에 그 파일을 명시해 기존처럼 캐릭터 단계만 실행할 수 있다. 이는 순서 전환 전의 단독 실험을 재현하기 위한 호환 경로이며, 기본 2단계 경로는 캐릭터→배경 순서다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --seed 5420 --runs 1 \
  --background-steps 3 --character-steps 3

python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --seed 5420 \
  --background-from docs/assets/part-07/chapter-05/example-background.png \
  --character-steps 12
```

## 카메라 관점은 RGB 후보마다 하나의 계약으로 고정한다

달리기·전진 도약 장면에서 카메라 위치와 렌즈까지 seed에 맡기면, 인체 오류인지 구도 차이인지 나중에 분리하기 어렵다. 그래서 이 실험은 **카메라 관점**과 **렌즈·화각**을 별도 후보 계약으로 둔다. 한 번의 비교에서는 다른 축, seed·해상도·두 단계의 step을 같게 유지한다. 이는 영화 촬영의 모든 샷 크기 문법을 분류하는 목록이 아니라, 현재의 세로 전신 스토리보드에서 위치·높이·기울기와 화각·원근 인상을 분리해 관찰하기 위한 작업용 선택지다.

| 옵션 | 작업용 한국어 이름 | 프레이밍에서 먼저 볼 것 |
| --- | --- | --- |
| `eye-level` | 아이레벨 정면 | 자연스러운 수평선과 전신 비율 |
| `low-angle` | 로우 앵글 | 바닥에서 올려다본 인물·절벽의 크기 관계 |
| `extreme-low-angle` | 강화 로우 앵글(웜스아이) | 지면에 붙은 시점에서도 전신 실루엣이 읽히는지 |
| `high-angle` | 하이 앵글 | 인물 뒤로 물러나는 협곡 바닥 |
| `bird-eye` | 버드아이 | 위에서 본 전신 실루엣과 바닥 경로 |
| `overhead` | 수직 오버헤드 | 바로 위에서 본 전신과 협곡 바닥 패턴 |
| `dutch` | 더치 앵글 | 약 20도 기울어진 화면에서도 중력·인체가 유지되는지 |
| `left-profile` | 왼쪽 프로필 | 진행 방향에 수직인 옆 실루엣 |
| `front-three-quarter` | 정면 3/4 | 얼굴과 진행 방향을 함께 읽을 수 있는지 |
| `rear-three-quarter` | 후면 3/4 | 등·진행 방향·협곡의 깊이 관계 |
| `front-on` | 정면 | 진행 방향과 일치하는 정면 전신 |
| `rear-on` | 후면 | 진행 방향과 일치하는 후면 전신 |

렌즈는 별도로 아래 다섯 프로필을 쓴다. 수치는 35 mm 풀프레임 환산값이며, 실제 생성 모델이 물리 렌즈를 장착하는 것은 아니다. 광각은 넓은 화각과 가까운 카메라 거리의 조합으로 앞뒤 깊이를 강조하고, 망원은 멀리서 본 좁은 화각으로 배경이 가까워 보이는 인상을 시험한다. 이 인상은 렌즈 자체만의 효과가 아니라, 같은 인물 크기를 유지하려고 달라지는 카메라 거리와 함께 해석해야 한다. [Sony Lens Basics](https://www.sony.com/electronics/support/articles/00268239){: target="_blank" rel="noopener noreferrer"}, [Sony: focal length, angle of view, and perspective](https://www.sony.com/en-qa/electronics/focal-length-angle-of-view-perspective){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-08)

| 옵션 | 작업용 한국어 이름 | 비교할 인상 |
| --- | --- | --- |
| `ultra-wide` | 초광각 18 mm | 가까운 전경과 크게 벌어진 앞뒤 깊이 |
| `wide` | 광각 24 mm | 넓은 협곡과 강조된 깊이 |
| `standard` | 표준 50 mm | 자연스러운 화각 기준선 |
| `short-telephoto` | 중망원 85 mm | 완만하게 압축된 협곡 깊이 |
| `telephoto` | 망원 135 mm | 멀리서 본 전신과 강하게 압축된 깊이 |

한 관점만 만들 때는 `--camera-angle`, 한 렌즈만 고를 때는 `--lens`를 쓴다. 기본값은 기존의 높은 시점과 가까운 `high-angle` 및 표준 `50 mm`다. 아래 명령은 같은 seed `5420`과 기본 3+3 step으로 선택한 표준 렌즈의 12개 **RGB 스토리보드 후보**를 각각 만든다. `--all-lenses`는 선택한 관점에서 5개 렌즈를 비교한다. 두 옵션을 함께 쓰면 12 × 5, 총 60개의 후보를 생성하므로 먼저 한 축만 비교하는 것을 기본값으로 둔다. 파일명과 해시에는 카메라·렌즈 옵션 및 prompt 계약이 포함되므로, 후보를 섞지 않고 검수할 수 있다. 이 옵션들은 guide나 depth를 만들지 않는다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --seed 5420 --all-camera-angles \
  --output-dir docs/assets/part-07/chapter-05

python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --seed 5420 --camera-angle extreme-low-angle --all-lenses \
  --output-dir docs/assets/part-07/chapter-05
```

기본값은 모든 화면에서 캐릭터 3 step + 배경 3 step이다. 이 기본값을 먼저 고정해야 카메라와 렌즈의 차이를 비교할 수 있다. 이후 사람 검수에서 특정 화면만 더 긴 복원이 필요하다는 가설이 생기면 `--shot-steps CAMERA/LENS=CHARACTER,BACKGROUND`로 **그 화면만** 조정한다. 예를 들어 강화 로우 앵글·초광각 조합의 인체만 다시 검수하려면 다음처럼 쓴다. 이 조정은 새 비교 계약이므로, 기존 3+3 후보와 같은 품질 표본으로 합치지 않는다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --seed 5420 --camera-angle extreme-low-angle --lens ultra-wide \
  --shot-steps extreme-low-angle/ultra-wide=5,4 \
  --output-dir docs/assets/part-07/chapter-05
```

GPU를 쓰기 전에 계약만 확인하려면 다음처럼 실행한다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --all-camera-angles --all-lenses --dry-run
```

`--dry-run` 출력에는 각 화면에 실제 적용될 캐릭터·배경 step도 함께 나타난다. 이번 단계의 산출물은 RGB 후보뿐이다. 각 후보에서 인체·전신 프레이밍·진행 방향·카메라 의도가 읽히는지를 사람이 먼저 확인하고, 통과한 한 장을 명시한 뒤에만 Canny와 상대 depth를 파생한다. 따라서 depth 확장은 카메라별 RGB 승인 기준과 어떤 depth 표현을 비교할지 정한 별도 실험으로 남긴다.

## seed는 후보 수만 늘린다

한 seed의 통과는 한 장면 후보의 관찰일 뿐이다. 같은 모델·prompt·해상도·step을 고정한 채 seed만 바꾸면 카메라의 세부 해석, 팔과 다리의 분리, 발의 접지, 절벽과 인물의 간격이 다른 콘티 후보로 나타난다. 이때 seed는 품질을 올리는 숫자가 아니라 **검수할 후보를 늘리는 조작 변수**다.

`--runs`는 시작 seed부터 연속된 후보를 만든다. 예를 들어 FLUX에서 `5420`부터 세 장을 비교하려면 다음처럼 실행한다. 각 PNG는 사람 검수 전까지는 후보일 뿐이며, 가장 예쁜 결과가 아니라 인체·가림·접지·공간 기준을 모두 만족한 결과 하나만 승인한다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --seed 5420 --runs 3
```

## 승인 전에는 guide를 만들지 않는다

다음 항목 하나라도 실패하면 PNG와 guide를 모두 남기지 않는다.

| 확인 항목 | 통과 기준 |
| --- | --- |
| 인체 | 두 팔·두 다리·머리·몸통의 연결이 한 사람으로 읽힘 |
| 자세와 가림 | 높은 대각선의 일자 든 다리·지지발·양팔이 한 사람의 자연스러운 균형 동작으로 읽힘 |
| 접지와 공간 | 지지발 외곽이 사암·자갈 바닥과 분리되고, 가까운 절벽이 인물을 삼키지 않음 |
| 기준 정보 | 짧은 단발과 검정 레오타드·타이즈가 다음 작화 단계의 최소 기준으로 읽힘 |

사람 검수로 통과한 스토리보드 파일을 명시할 때만 guide를 만든다. 이 분리는 불완전한 인체나 지형의 오류가 후속 ControlNet·참조 병합의 입력으로 굳어지는 것을 막는다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py \
  --derive-guides-from docs/assets/part-07/chapter-05/p7-5-3-flux2-klein-storyboard-forward-leap-approved.png \
  --output-dir docs/assets/part-07/chapter-05
```

seed `5420` 결과를 사람 검수로 승인했다. 이 장면에서는 화면 오른쪽으로 뛰어 나가는 공중 현대무용 동작, 앞·뒤로 분리된 두 다리와 두 팔, 사암·자갈 바닥과 가까운 절벽이 함께 읽힌다. 아래 RGB 원본과 Canny·상대 depth guide만 장면 기준으로 유지한다. 한 장면의 승인 결과가 다른 카메라·동작에서도 자동으로 통과함을 뜻하지는 않는다.

| 승인 RGB | Canny guide | 상대 depth guide |
| --- | --- | --- |
| ![승인한 FLUX.2 Klein 전진 도약 스토리보드](../../../assets/part-07/chapter-05/p7-5-3-flux2-klein-storyboard-forward-leap-approved.png) | ![승인 전진 도약 스토리보드의 Canny guide](../../../assets/part-07/chapter-05/p7-5-3-flux2-klein-storyboard-forward-leap-approved-guide-canny.png) | ![승인 전진 도약 스토리보드의 상대 depth guide](../../../assets/part-07/chapter-05/p7-5-3-flux2-klein-storyboard-forward-leap-approved-guide-depth.png) |
| 사람 검수로 승인한 장면 기준 RGB다. | 승인 RGB에서 추출한 강한 경계 guide다. | 승인 RGB의 앞뒤 관계를 회색 농도로 나타낸 상대 depth guide다. |

## depth 리파인은 별도 가설로 검증한다

승인 스토리보드를 만들 때는 외부 캐릭터 PNG를 넣지 않는다. 반면 후속 리파인에서는 **상대 depth가 공중 도약의 실루엣만 전달하고**, P7-5.2의 착장·얼굴 기준 이미지가 인물의 외형을 보완할 수 있는지를 별도로 시험할 수 있다. 두 흐름을 섞으면 캐릭터 참조가 스토리보드 자체를 통과시킨 것처럼 보일 수 있으므로, 이 실험 결과에서는 guide를 다시 만들지 않고 최종 컷에도 사용하지 않는다.

아래 실행은 상대 depth, 전·후면 착장 기준, 얼굴 정면 기준을 함께 넣어 배경 없는 한 명의 도약 인물을 만든다. 기본값은 3 step이며, 결과 파일과 같은 이름의 검수 JSON에는 가설과 확인 항목을 남긴다.

```bash
python docs/assets/part-07/chapter-05/p7_5_3_refine_storyboard_four_outputs.py \
  --stage depth-character \
  --output-prefix p7-5-3-refine-hypothesis-depth-character
```

![상대 depth와 착장·얼굴 기준을 함께 사용한 depth-character 가설 검증 결과](../../../assets/part-07/chapter-05/p7-5-3-refine-hypothesis-depth-character-depth-hash-eb58e6e519-seed-62377-steps-3-depth-character-stage.png)

| 검수 항목 | 이번 표본의 관찰 | 판정 |
| --- | --- | --- |
| 동작·프레이밍 | 공중 전진 도약, 두 팔·두 다리, 전신 프레이밍이 상대 depth의 큰 실루엣과 함께 남았다. | 통과 |
| 얼굴·머리 | 밝은 피부, 청록 단발, 보이는 얼굴이 얼굴 정면 기준과 같은 방향으로 다시 나타났다. | 통과 |
| 착장 | 배꼽 높이의 하이웨이스트·넓은 통·발목 위 밑단과 재킷 바깥의 대각선 가방 스트랩이 읽힌다. | 통과 |
| 배경 분리 | 협곡·바닥을 다시 그리지 않고 옅은 중립 배경에 인물만 남겼다. | 통과 |
| 신발 | 입력 착장 기준에 신발 참조가 없어서 맨발로 생성됐다. | 미통과 |

이 표본은 짧은 리파인 계약이 자세·얼굴·바지·가방 경로를 함께 보존할 수 있다는 **가설의 일부만** 뒷받침한다. 신발처럼 기준 이미지에 없는 항목은 prompt만으로 자동 보완됐다고 판단하지 않는다. 따라서 이 결과는 신발 기준을 추가할 다음 실험의 비교 기준이며, 승인 스토리보드나 최종 장면 자산이 아니다.

### 구조 입력을 바꾼 세 경로 비교

같은 seed `62377`, 3 step에서 구조 입력 경로만 바꿔 세 후보를 만들었다. RGB 직접 리파인은 착장·배경·얼굴을 차례로 거치는 3단계 경로다. 두 2단계 경로는 먼저 depth-character로 인물만 만들고, 두 번째 단계에서 RGB 또는 Canny와 상대 depth로 협곡을 붙인다. 따라서 이 표는 모델 일반 성능이 아니라, 이 장면에서 **어떤 입력 조합이 무엇을 잃는가**를 읽기 위한 비교다.

| RGB 직접 3단계 | depth-character → RGB 2단계 | depth-character → Canny 2단계 |
| --- | --- | --- |
| ![RGB 직접 전체 리파인 후보](../../../assets/part-07/chapter-05/p7-5-3-refine-rgb-full-storyboard-hash-058fe20bfd-seed-62377-steps-3-candidate.png) | ![depth-character 뒤 RGB를 쓴 2단계 후보](../../../assets/part-07/chapter-05/p7-5-3-refine-two-stage-rgb-storyboard-hash-f4b2a908f4-seed-62377-steps-3-background-stage.png) | ![depth-character 뒤 Canny를 쓴 2단계 후보](../../../assets/part-07/chapter-05/p7-5-3-refine-two-stage-canny-canny-hash-872d29f9a9-seed-62377-steps-3-background-stage.png) |
| 협곡·신발까지 다시 나타났지만, 단계가 많아 원본 RGB의 재해석도 함께 일어난다. | 인물 기준의 얼굴·넓은 바지·짧은 밑단을 비교적 보존하지만, 1단계의 맨발이 그대로 남는다. | 인물 기준은 대체로 남지만 Canny 경계가 협곡 표면을 더 강하게 다시 해석하며, 맨발도 해결하지 못한다. |

이 비교에서 바로 한 경로를 최종 경로로 고르지 않는다. 신발처럼 누락되면 안 되는 항목은 별도 기준 이미지나 명시적 후속 보정으로 해결할 문제이며, 현재 세 후보 모두 승인 스토리보드를 대체하지 않는다.

## LoRA 전환에는 별도 데이터와 학습 환경이 필요하다

다중참조만으로 얼굴과 복장이 약하게 섞이면 LoRA를 검토할 수 있다. 현 경로에 맞는 모델은 Apache-2.0인 **FLUX.2 Klein 4B Base**다. 학습은 Base checkpoint에서 하고, 완성한 adapter는 빠른 distilled 4B 추론 모델에 붙인다.

하지만 이는 현재 8 GB GPU에서 바로 실행할 다음 단계는 아니다. 공식 Klein LoRA 안내는 4B Base 학습을 약 24 GB VRAM·RTX 4090급에서 검증했다. 8 GB는 현재 승인 스토리보드 생성·다중참조 추론에는 맞지만, LoRA 학습 승인 기준에는 미달이다. FLUX.1-dev QLoRA의 약 9 GB 사례도 8 GB보다 크고 base model의 비상업 라이선스가 현재의 개방 라이선스 기준과 맞지 않는다.

학습을 시작하려면 먼저 올바른 데이터를 확보한다. 스타일·캐릭터 LoRA는 서로 다른 구도와 시점을 가진 15–40장의 검수된 이미지와 각 이미지의 내용 caption·동일 trigger word가 필요하다. 현재 P7-5.2의 23개 자산은 얼굴·전신·소품 기준 보드가 섞여 있어 그대로는 이 조건을 충족하지 않는다. 실패하거나 왜곡된 생성 이미지를 늘려 학습 데이터로 삼으면 얼굴·복장 오류를 adapter에 고정하므로 사용하지 않는다.

구도 보존과 캐릭터 교체를 함께 학습하려면 스타일 LoRA보다 **edit LoRA**가 더 직접적이다. 이 경우 승인 스토리보드 같은 입력과, 같은 포즈·구도에서 캐릭터·복장이 완성된 목표 이미지를 파일명별로 짝지은 50–200개의 검수된 쌍이 필요하다. 이 데이터와 24 GB 이상 학습 환경을 확보한 뒤에만 별도 실험으로 진행한다.

## 체크리스트

- 후보 PNG를 guide나 후속 생성 입력으로 쓰기 전에 사람이 인체·가림·접지·거리 조건을 확인했는가?
- 미통과 후보와 그 후보에서 뽑은 guide를 함께 삭제했는가?
- 승인한 한 장이 생긴 뒤에도 다른 seed·카메라·동작에서 같은 결과가 자동으로 보장된다고 가정하지 않는가?

## 출처와 참고 자료

- FLUX.2 Klein 4B는 텍스트 생성과 단일·다중 참조 이미지 편집을 지원하며 Apache-2.0으로 배포된다. 이 절에서는 텍스트만으로 장면 후보를 만들고, 사람 검수 뒤에만 파생 guide를 만든다. [FLUX.2 공식 저장소](https://github.com/black-forest-labs/flux2){: target="_blank" rel="noopener noreferrer"}, [FLUX.2 Klein 4B 모델 카드](https://huggingface.co/black-forest-labs/FLUX.2-klein-base-4b-fp8){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-07)
- FLUX.2 Klein LoRA의 공식 학습 안내는 Base 4B에서의 학습, 15–40장 스타일 데이터, 24 GB VRAM·RTX 4090급, 그리고 adapter를 distilled 4B 추론에 로드하는 흐름을 제시한다. edit LoRA는 입력·목표 이미지의 짝 데이터와 `control_path`를 사용한다. [FLUX.2 Klein LoRA 안내](https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-07)
- FLUX.1-dev QLoRA는 4-bit base·8-bit optimizer·gradient checkpointing·latent/text embedding cache를 함께 써도 공식 사례의 peak가 약 9 GB이며, 본 절의 8 GB·Apache-2.0 기준을 충족하는 대체 학습 경로로 보지 않는다. [Diffusers FLUX.1 QLoRA 안내](https://huggingface.co/blog/flux-qlora){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-07)
- SDXL inpaint는 mask 영역만 다시 그릴 수 있고, IP-Adapter Plus Face는 잘라낸 얼굴 이미지 조건을 SDXL에 넣을 수 있다. 이 절에서는 전신을 다시 생성하지 않는 국소 얼굴·헤어 보정 후보로만 검수한다. [Diffusers inpainting 안내](https://huggingface.co/docs/diffusers/main/api/pipelines/stable_diffusion/inpaint){: target="_blank" rel="noopener noreferrer"}, [Diffusers IP-Adapter 안내](https://huggingface.co/docs/diffusers/v0.31.0/using-diffusers/ip_adapter){: target="_blank" rel="noopener noreferrer"}, [IP-Adapter Plus Face SDXL 가중치](https://huggingface.co/h94/IP-Adapter/blob/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors){: target="_blank" rel="noopener noreferrer"} (확인: 2026-08-07)
