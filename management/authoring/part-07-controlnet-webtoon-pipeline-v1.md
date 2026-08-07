# Part 7 ControlNet 중심 웹툰 컷 파이프라인 v1

이 문서는 Part 7의 다음 실험과 원고 예제를 위한 운영 계약이다. 목표는 동일 캐릭터가 서로 다른 장소, camera, pose에서 읽히는 **정지 웹툰 컷**을 만드는 것이며, OpenPose나 특정 모델을 성공 그 자체로 보지 않는다.

## 핵심 원칙

ControlNet은 캐릭터의 정체성을 만드는 장치가 아니라, 컷의 공간 구조를 조건으로 전달하는 중심 제어층이다. 따라서 아래 역할을 섞지 않는다.

| 역할 | 고정 원본 | ControlNet 또는 도구 | 통과 기준 |
| --- | --- | --- | --- |
| 누구인가 | 승인 character sheet와 다각도 face sheet, character LoRA 또는 reference 조건 | LoRA와 필요할 때 참조 조건 | 얼굴, 헤어, 의상, 체형이 기준서와 맞음 |
| 어디에 어떻게 있는가 | shot board와 scene control pack | ControlNet | 전신 crop, 인물 위치, pose, camera 관계가 컷 의도와 맞음 |
| 어떤 작화인가 | style sheet, 고정 checkpoint와 palette | checkpoint, LoRA, 색 보정 | 선, 색, 명암, 질감이 시퀀스에서 유지됨 |
| 무엇을 고칠 것인가 | 오류 영역과 수정 전 이미지 | mask inpaint, 직접 보정 | mask 밖의 승인 특징은 보존하고 오류만 해결함 |

OpenPose는 `인물 동작`을 표현하는 유효한 ControlNet 입력이다. 다만 손·소품 접점, 강한 원근, 배경의 소실점까지 OpenPose 하나에 맡기지 않는다. ControlNet 조건은 컷마다 하나의 **주 제어 입력**을 선택하고, 필요성이 검증된 경우에만 보조 입력을 추가한다.

## P7-WC v1 흐름

```text
character reference pack 승인
  -> style sheet + location sheet 승인
  -> shot contract
  -> scene control pack (OpenPose / depth / lineart / segmentation)
  -> 실행 성립 게이트
  -> ControlNet 단일 조건 baseline
  -> identity anchor 결합 후보
  -> mask inpaint 또는 직접 보정
  -> 4컷 continuity review + 식자
```

### 0. 승인 자산

생성 전에 다음 다섯 자산을 승인한다. 미승인 자산은 prompt나 reference image로 사용하지 않는다.

| 자산 | 최소 내용 | 이유 |
| --- | --- | --- |
| character sheet | 정면, 좌·우 3/4, 측면, 후면 전신과 의상 관찰 항목 | pose와 camera가 바뀐 뒤에도 체형·의상·전신 crop을 비교할 기준 |
| face sheet | 정면, 좌·우 3/4, 측면의 얼굴과 기본·웃음·놀람 표정, 눈·앞머리·hair clip 관찰 항목 | 한 장의 정면 얼굴을 모든 camera의 identity 기준으로 오용하지 않기 위한 기준 |
| style sheet | 선 굵기, 색 palette, 명암, 금지 질감 | 컷마다 다른 작화로 drift하는지 판정할 기준 |
| location sheet | 주요 장소의 소실점, 출입구, 주요 소품, 광원 방향 | 배경을 매번 새 prompt로 재발명하지 않기 위한 기준 |
| shot board | 컷의 서사 목적, 인물 위치, 말풍선 여백, camera 의도 | 어떤 ControlNet 입력이 필요한지 고르는 기준 |

#### 첫 산출물: character reference pack

새 파이프라인의 1순위는 ControlNet workflow나 panel PNG가 아니라 **고정할 캐릭터 일러스트 묶음**이다. 한 장의 정면 이미지가 아니라 아래 항목을 하나의 revision으로 묶어 사람이 승인한다.

| 묶음 | 최소 컷 | 고정할 관찰 항목 |
| --- | --- | --- |
| 전신 turnaround | 정면, 좌·우 3/4, 측면, 후면 | 키 비율, 어깨·골반 폭, 헤어 실루엣, 의상 구조, 신발 |
| face sheet | 정면, 좌·우 3/4, 측면 + 기본·웃음·놀람 | 얼굴형, 눈 간격·색·형태, 눈썹, 앞머리, hair clip |
| 의상·소품 sheet | 앞·옆·뒤와 자주 쓰는 소품 | 색 코드, 주름 규칙, 장식 위치, 손과 소품의 상대 크기 |
| style sheet | 선, palette, 명암, 배경과 인물의 경계 | 선 굵기, 채색 경계, 광원, 금지 질감 |

이 팩을 승인하기 전에는 LoRA 학습, IP-Adapter reference, face inpaint, ControlNet 조합 실험을 시작하지 않는다. 생성 모델로 만든 후보도 이 팩의 원본이 될 수 있지만, 복제 인물, 잘린 발, 각도별 얼굴 불일치, 의상 구조 변화가 하나라도 있으면 `draft`로만 두고 기준 원본으로 승격하지 않는다.

`management/authoring/part-07-character-reference-pack-template.md`에 이 승인 기록 양식을 둔다. character reference pack의 revision이 바뀌면, 이전 revision에서 생성한 panel과 inpaint 결과를 새 기준의 통과 근거로 재사용하지 않는다.

#### 화풍과 얼굴을 먼저 잠그는 규칙

웹툰의 반복성은 seed가 아니라 **승인 기준과 고정된 생성 조건**에서 나온다. 그러므로 첫 ControlNet 실험 전에 아래 조건을 잠근다.

1. 동일한 checkpoint, VAE, character LoRA 또는 reference 조건, style anchor, palette, negative prompt의 버전을 기록한다.
2. style anchor는 character LoRA와 역할이 다르다. character anchor는 얼굴·헤어·의상 같은 `누구인가`를, style anchor는 선·색·명암 같은 `어떻게 그리는가`를 맡는다. 둘을 한 번에 바꾸지 않는다.
3. face sheet의 정면, 3/4, 측면에서 눈 간격·눈썹·앞머리·hair clip·얼굴형을 체크 항목으로 적는다. “예쁘게 나왔다”는 얼굴 통과 기준이 아니다.
4. 첫 컷의 얼굴을 잘라 다음 컷의 유일한 reference로 쓰지 않는다. camera가 바뀌면 해당 각도의 face sheet와 대조한다.
5. inpaint에도 같은 checkpoint와 character/style anchor를 유지한다. inpaint가 다른 base model 또는 다른 style LoRA를 쓰면 결과가 좋아 보여도 해당 컷은 화풍 일관성 실패로 처리한다.

현재 8 GB 환경에서 LoRA를 학습해 identity를 고정하려면, 학습 전에 이 기준을 통과한 자체 제작 16-32장과 held-out pose·장소 검증셋이 필요하다. 미승인 소수 이미지로 만든 LoRA는 얼굴과 화풍 고정의 증거로 쓰지 않는다. 이 준비가 없을 때는 ControlNet 실험을 `구조 baseline`으로 한정하고, character consistency 통과를 주장하지 않는다.

### 1. shot contract

각 컷은 생성 전에 `panel_id`, `entry_strategy`, `required_full_body`, `primary_control`, `camera_intent`, `identity_anchor`, `repair_targets`를 기록한다. `entry_strategy`는 다음 중 하나다.

| 진입 전략 | 먼저 고정할 원본 | 주 ControlNet 입력 | 적합한 컷 |
| --- | --- | --- | --- |
| `pose-first` | 사람이 승인한 동작 frame 또는 pose board | OpenPose | 걷기, 몸짓, 인물 간 거리 |
| `camera-background-first` | 장소 원근과 camera가 담긴 scene board | depth 또는 lineart | wide, low/high angle, 장소 소개 |
| `object-first` | 소품의 윤곽과 손이 닿는 위치 | lineart 또는 segmentation | 티켓, 휴대폰, 문손잡이, 책 |
| `face-first` | 얼굴 방향과 표정 기준 이미지 | segmentation 또는 약한 lineart, 필요 시 ControlNet 없음 | 대화, 감정 반응, close-up |

OpenPose는 `pose-first`의 기본값이다. `camera-background-first`와 `object-first`에는 OpenPose를 자동으로 추가하지 않는다. 두 제어 입력이 정말 필요한 컷은 단일 ControlNet baseline을 먼저 통과한 뒤에만 다중 조건으로 비교한다.

### 2. scene control pack

각 ControlNet 입력은 모델에 전달하기 전 사람이 다음 내용을 확인한다.

| 입력 | 확인할 항목 | 이 입력만으로 보장하지 않는 것 |
| --- | --- | --- |
| OpenPose | 몸통, 팔·다리, 손목, 발목, 목-머리 방향과 전신 crop | 얼굴, 의상, 손가락, 발바닥 접지, 배경 원근 |
| depth | 인물과 배경의 앞뒤 관계, 카메라 높이, 소실 관계 | 정확한 손 모양, 캐릭터 identity |
| lineart | 윤곽, 소품 접점, 말풍선 여백, 화면 구성 | 광원, 재질, 완전한 깊이 |
| segmentation | 인물·배경·소품의 점유 영역 | 관절, 표정, 소실점 |

ControlNetApply는 전처리된 control image와 positive/negative conditioning을 받고, strength와 적용 구간을 조절한다. 초안은 strength `0.5`에서 `1.5` 범위 안의 하나의 값으로 시작해 비교하며, 값·시작·종료 구간을 컷 기록에 남긴다. 강도를 높인 결과가 이상해지면 더 높은 값으로 고정하지 않고, control image 자체가 컷 의도를 담았는지 다시 확인한다.

#### pose와 camera가 모두 중요한 컷의 두 단계 검증

low-angle 이동처럼 OpenPose와 depth/lineart가 모두 필요한 컷은 처음부터 다중 ControlNet으로 생성하지 않는다. 두 입력의 원인이 섞이면 어느 입력이 포즈, 원근, identity drift를 만들었는지 알 수 없기 때문이다.

1. `camera baseline`: depth 또는 lineart 하나로 장소, 소실점, 인물의 화면 위치를 검증한다.
2. `pose baseline`: OpenPose 하나로 전신 crop, 손목, 발목, 목-머리 방향을 검증한다. 사용할 pose detector가 손·얼굴 landmark를 낸다면, 그 정보가 실제 control image에 들어갔는지도 별도로 확인한다.
3. 두 baseline이 각각 구조를 통과한 경우에만, 같은 shot contract에서 다중 ControlNet 또는 **배경을 보호한 pose inpaint**를 비교한다. 후자는 camera baseline 이미지를 바탕으로 인물 영역만 mask inpaint하고, OpenPose를 그 영역의 제어 입력으로 적용하는 방식이다.
4. 다중 조건이 VRAM 부족, 원근 붕괴, 인물 위치 이동을 만들면 단일 ControlNet 단계로 되돌린다. 다중 ControlNet은 기본 경로가 아니라 비교 대상이다.

이 절차에서 배경은 먼저 depth/lineart로 구조를 고정하고, 인물은 OpenPose로 넣는다. 따라서 OpenPose 사용을 금지하지 않으면서도, OpenPose에 배경 원근과 camera 역할을 과도하게 요구하지 않는다.

### 3. 8 GB 실행 성립 게이트

첫 실행은 모델 품질 비교가 아니라 구성 확인이다. 기본 조건은 `SD 1.5 호환 checkpoint + 호환 ControlNet 1개 + 512 x 768 + batch 1`로 둔다. LoRA, IP-Adapter, 두 번째 ControlNet, high-resolution fix는 이 단계에서 끈다.

다음 네 항목을 모두 남겨야 다음 단계로 넘어간다.

1. checkpoint와 ControlNet의 라이선스 및 호환성
2. peak VRAM, 생성 시간, seed, 해상도, sampler, step
3. control image와 생성 PNG
4. ControlNet을 끈 비교 PNG

VRAM 부족, 파일 누락, 출력 PNG 부재, control on/off에서 구조 차이를 읽을 수 없음 중 하나라도 발생하면 해당 조합은 중단한다. 이 판단은 캐릭터 품질 판단과 별개다.

#### 실패 코드와 복귀 지점

실패 이미지를 더 많이 만들기 전에 원인을 아래 코드로 분류한다. `inpaint`는 `L` 계열에만 허용한다.

| 코드 | 관찰 | 다음 작업 | inpaint 허용 여부 |
| --- | --- | --- | --- |
| `A` asset blocked | character/style/location/shot 원본이 미승인 | 0단계 자산 승인으로 복귀 | 아니오 |
| `R` resource blocked | VRAM, 모델 호환성, workflow 파일, PNG 저장 중 하나가 실패 | 단일 ControlNet, 해상도, offload, 모델 호환성을 다시 측정 | 아니오 |
| `S` structure fail | pose, camera, 소실점, 인물 위치, 소품 접점이 shot contract와 다름 | scene control pack 또는 ControlNet strength·구간을 수정 | 아니오 |
| `I` identity fail | 얼굴, 헤어, 의상, 체형이 character/face sheet와 다름 | character·face sheet, LoRA/reference 조건, prompt를 수정 | 얼굴 방향·체형이 맞을 때만 제한적으로 |
| `T` style fail | 선, 색, 명암, 질감이 style sheet 또는 다른 컷과 다름 | checkpoint, style anchor, palette, prompt를 수정 | 다른 anchor로 화풍을 바꾸지 않고 같은 조건에서 국소 질감만 다룰 때만 |
| `L` local detail fail | 전체 구조와 identity는 맞지만 눈, 손가락, 표지, 질감 같은 국소 오류가 남음 | 영역별 mask inpaint 또는 직접 보정 | 예 |
| `C` continuity fail | 개별 컷은 통과했지만 4컷에서 색, 장소, camera, 의상이 모순 | 해당 원본과 workflow 기록을 고쳐 해당 컷부터 재생성 | 국소 오류에 한해 |

### 4. identity anchor를 한 변수로 결합

실행 성립 뒤에는 character LoRA 또는 승인 reference 조건 중 하나만 추가한다. ControlNet 입력, seed, prompt, camera 의도는 그대로 두고 `identity_anchor`만 바꿔, 구조 제어와 동일 인물성의 충돌을 분리해 관찰한다. 두 anchor를 한 번에 늘리거나 ControlNet strength도 함께 바꾸지 않는다.

전신 character sheet의 항목이 비어 있으면 LoRA 학습이나 reference 조건의 결과를 캐릭터 일관성 통과로 판정하지 않는다.

### 5. ControlNet 초안 뒤의 영역별 inpaint

새 파이프라인의 기본 전략은 **ControlNet으로 한 컷의 전체 구조를 먼저 만들고, inpaint로 얼굴·손·배경의 디테일을 올리는 것**이다. 이 순서는 전신 pose와 camera가 보이는 전체 해상도 후보를 먼저 승인한 뒤에만 적용한다. 대화 컷도 가능한 한 전신 또는 허리 위 원본을 먼저 만들고, 최종 crop은 보정 뒤에 고른다.

```text
scene control pack
  -> ControlNet full-frame candidate
  -> whole-frame structure review
  -> face mask inpaint
  -> hand/object mask inpaint
  -> background mask inpaint
  -> full-frame re-review
  -> final crop and lettering
```

inpaint는 새 이미지를 다시 생성하는 단계가 아니라, 이미 통과한 화면에서 실패 영역만 바꾸는 단계다. 같은 checkpoint, character LoRA 또는 reference 조건, style prompt, negative prompt를 유지하고, `mask`, `repair prompt`, `seed`, `denoising strength`, 수정 전후 PNG를 모두 기록한다.

| 보정 영역 | inpaint를 시작할 수 있는 조건 | mask에 포함할 문맥 | 통과 질문 | inpaint로 고치지 않고 되돌릴 경우 |
| --- | --- | --- | --- | --- |
| 얼굴·눈·앞머리 | 머리 방향, 얼굴 위치, 카메라 crop이 이미 맞음 | 얼굴 윤곽, 헤어라인, 귀와 목의 일부 | 눈 모양, 앞머리, hair clip, 얼굴형, 표정이 **해당 각도의 face sheet**와 맞는가 | 얼굴 방향·시선 자체가 shot contract와 다름 |
| 손·소품 | 손목 위치, 팔 길이, 소품의 큰 윤곽과 접점이 이미 맞음 | 손목부터 소품 경계와 주변 의상 일부 | 손 수, 손목 방향, 잡는 위치, 소품 글자·모양이 읽히는가 | 손목·팔·소품의 위치 관계 또는 가림 순서가 틀림 |
| 배경 | camera, 지평선, 주요 출입구·가구의 위치가 이미 맞음 | 오류 영역과 인접한 벽·바닥·광원 경계 | 재질, 표지, 반복 무늬, 배경 인물의 밀도가 장소 기준서와 맞는가 | 소실점, camera 높이, 인물과 배경의 앞뒤 관계가 틀림 |
| 발·접지 | 다리 길이와 발의 바닥 위치가 이미 맞음 | 발목, 바닥 그림자, 발 주변 바닥 | 신발 형태와 바닥 접점이 자연스럽고 전신 비율이 유지되는가 | 지지발, 체중, 다리 길이, 지면 자체가 틀림 |

이 표의 오른쪽 열은 중요한 중단 규칙이다. 예를 들어 OpenPose가 팔 방향을 잘못 전달했거나 depth가 low angle을 잘못 만들었다면, 손 mask를 여러 번 다시 그려도 자연스러운 장면이 되지 않는다. 그 경우에는 `scene control pack`과 ControlNet baseline으로 돌아가 control image, camera 원본, strength를 고친다.

#### 보정 순서와 해상도

1. `512 x 768` 또는 그 이상의 전신 preview에서 ControlNet 구조를 판정한다. 8 GB에서는 단일 ControlNet, batch 1을 기본으로 한다.
2. 승인한 전체 프레임을 최종 게시 비율의 작업 해상도로 올린다. upscaling 또는 VAE tiling은 실행 보조 수단일 뿐, 이 단계에서 identity·손 품질이 통과했다고 보지 않는다.
3. 얼굴·눈·앞머리, 손·소품, 발·접지, 배경을 겹치지 않는 mask로 차례로 보정한다. 손이 얼굴이나 소품을 가리는 컷처럼 mask가 겹치면, 앞 단계 보정 후 전체 프레임을 다시 검토하고 다음 mask의 경계를 새로 만든다.
4. 각 보정 뒤에는 mask 밖의 얼굴, 의상, pose, camera, 색 palette가 보존됐는지 확인한다. 얼굴 보정은 수정 mask 안에서도 face sheet의 해당 각도와 대조한다. 하나라도 바뀌면 해당 보정 결과를 폐기한다.
5. 모든 영역 보정 뒤에만 최종 crop과 말풍선 여백을 정한다. crop이 전신·발·소품 접점을 잘라 구조 판단을 숨기면, 원본 컷을 다시 설계한다.

ComfyUI inpainting은 수정할 영역을 mask로 지정하고 inpainting용 VAE conditioning에 전달한다. 따라서 mask에는 오류 픽셀만이 아니라 자연스러운 연결에 필요한 주변 문맥을 포함하되, 승인된 다른 영역을 넓게 덮지 않는다. 얼굴과 손에 같은 넓은 mask를 쓰면 두 실패 원인의 수정 기록을 분리할 수 없다.

#### 첫 실험의 비교쌍

새 전략의 첫 실험은 한 번의 “완성 컷”을 고르는 일이 아니다. 아래 비교쌍을 같은 cut과 동일한 ControlNet 입력에서 만든다.

| 비교 | 바꾸는 것 | 확인할 질문 |
| --- | --- | --- |
| A: ControlNet on/off | ControlNet 적용 여부만 | control image가 pose 또는 camera 구조를 실제로 바꾸는가 |
| B: 전체 재생성 / 얼굴 inpaint | face mask 적용 여부만 | 얼굴이 좋아지면서 mask 밖의 헤어·의상·camera가 유지되는가 |
| C: 전체 재생성 / 손·소품 inpaint | hand-object mask 적용 여부만 | 손가락보다 먼저 손목·소품 접점이 읽히게 되는가 |
| D: 전체 재생성 / 배경 inpaint | background mask 적용 여부만 | 배경 디테일이 좋아지면서 소실점과 인물 가림이 유지되는가 |

각 비교에서 inpaint 결과가 구조를 바꾸거나 character sheet 특징을 잃으면 통과가 아니다. 이 경우 “더 예쁜 이미지” 대신 어느 단계로 되돌아갈지를 기록한다.

### 6. 4컷 검증 매트릭스

처음 채택할 시퀀스는 아래 네 컷으로 고정한다. 네 컷을 개별 성공 이미지가 아니라 하나의 contact sheet로 판정한다.

| 컷 | 전략과 주 제어 입력 | 반드시 볼 것 |
| --- | --- | --- |
| 01 대화 | `face-first`, 약한 lineart 또는 없음 | 얼굴, 눈, 화풍, 말풍선 여백 |
| 02 이동 | `pose-first`, OpenPose | 전신, 지지발, 팔 관계, 손목, crop |
| 03 장소 전환 | `camera-background-first`, depth 또는 lineart | low/high angle, 원근, 인물 위치, 장소 연속성 |
| 04 소품 상호작용 | `object-first`, lineart 또는 segmentation | 손·소품 접점, 가림, 시선, 배경 위치 |

각 컷은 identity, structure, style, local-detail 네 판정을 별도로 기록한다. 하나라도 `fail`이면 해당 컷은 식자 단계로 넘어가지 않는다.

### 7. 국소 보정과 식자

얼굴·눈·앞머리, 손·소품, 발·접지, 배경을 서로 다른 mask로 나눈다. inpaint 뒤에는 수정 mask 밖의 character sheet 특징, camera, 소품 위치가 보존됐는지 다시 판정한다. 말풍선과 대사는 생성 이미지에 포함하지 않고 레이어 기반 편집 단계에서 넣는다.

## 현재 검증 경로

이전 manifest와 검사기는 제거했다. 현재 기준은 `docs/assets/part-07/chapter-05/p7_5_3_text_to_image_storyboard_spec.py`가 텍스트에서 한 장면 스토리보드를 먼저 만들고, 사람 검수 후 같은 스토리보드에서 lineart·canny·depth를 추출하는 경로다. 승인한 스토리보드는 `p7_5_3_flux2_storyboard_character.py`에서 P7-5.2 얼굴·복장 기준과 함께 FLUX.2 Klein 4B의 다중 참조 입력으로 사용한다. 승인 여부는 정적 manifest가 아니라 스토리보드·파생 guide·최종 컷의 실제 사람 검수와 P7-5.3 원고의 비교 표로 기록한다.

## 채택과 제외

- 채택: ControlNet을 구조 제어의 중심으로 두고, OpenPose를 동작 컷의 유효한 입력으로 사용한다.
- 채택: SD 1.5 단일 ControlNet baseline부터 실행하고, identity anchor와 다중 ControlNet은 한 변수씩 추가한다.
- 제외: OpenPose 하나만으로 캐릭터 일관성, 손·소품, camera, 화풍까지 통과했다고 주장하는 구성.
- 제외: LLM 관절값, 간이 2D cutout rig, 미승인 전신 reference를 새 파이프라인의 기준 원본으로 쓰는 구성.

## 근거

- [ComfyUI ControlNetApply](https://docs.comfy.org/built-in-nodes/ControlNetApply): ControlNet의 control image, strength, start/end 적용 구간과 conditioning 연결을 확인했다. 확인일: 2026-08-02.
- [Diffusers ControlNet](https://huggingface.co/docs/diffusers/en/api/pipelines/controlnet): depth, edge, segmentation, human pose 등 여러 공간 조건과 다중 ControlNet 결합 방식을 확인했다. 확인일: 2026-08-02.
- [ComfyUI Inpainting Workflow](https://docs.comfy.org/tutorials/basic/inpaint): mask를 사용한 국소 수정과 inpainting VAE 경로를 확인했다. 확인일: 2026-08-02.
