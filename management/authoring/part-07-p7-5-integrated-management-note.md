# Part 07 Chapter 05 P7-5 통합 관리노트

- 통합 범위: `P7-5.1`~`P7-5.8`
- 대응 본문: `docs/parts/part-07/chapter-05/section-01.md`~`section-08.md`
- 통합일: 2026-08-14
- 문서 성격: 원고 릴리즈 이력의 대체 관리노트. 독자용 본문이나 `mkdocs.yml`의 nav에 연결하지 않는다.

## 1. 통합 원칙

P7-5의 기록은 `화풍 기준 → 인물 기준 → 장면·구조 → 보정 → 다중참조 → 3D 구조 입력 → 얼굴·카메라 회전`의 순서로 읽는다. 같은 prompt의 단어 수, seed, step, CFG, mask border만 바꾼 반복은 개별 이력으로 남기지 않고 다음 세 가지로 압축한다.

1. 어떤 계약을 검증했는가.
2. 어떤 입력 역할과 조건에서 어떤 특징이 일치하거나 이탈했는가.
3. 반복을 중단하고 다음 가설로 넘어간 이유는 무엇인가.

P7-5는 이미지·guide·JSON에 `승인`, `미승인`, `보류` 상태를 부여하지 않으며 이를 다음 단계의 gate로 사용하지 않는다. 다음 단계의 입력은 상태가 아니라 문서화된 역할, 실행 조건, 관찰된 일치·이탈, 알려진 한계를 보고 선택한다. 한 단계의 계약을 바꾸면 기존 PNG의 상태를 갱신하는 대신, 영향 범위와 새 비교 조건을 결과 기록에 남긴다. 아래에 남은 승인·탈락·gate 표현은 2026-08-21 이전 실험 이력이며 현재 운영 규칙이 아니다.

## 2. Section별 현재 계약과 통합 결론

### P7-5.1 — 배경 화풍 기준

- 인물 없이 배경만 생성하고, 장소·시간·카메라를 장면 변수로 분리한다.
- 공통 화풍은 `docs/assets/part-07/chapter-05/p7-5-1-style-prompt-contract.json`으로 관리한다.
- 로컬 GPU 배경 참조 셋과 `p7-5-1-approved-style-reference-pack.json`은 화풍 입력으로 쓰되, 각 이미지의 장소·시간·카메라·선·채색 역할과 관찰 한계를 함께 기록한다.
- 참조 표는 빈 열 없이 4열 중심으로 정리하며, 표의 장소 라벨은 이미지와 분리하지 않는다.
- P7-5.1 화풍 입력과 P7-5.3 인물 identity 입력은 서로 대체하지 않는다.

### P7-5.3 — 얼굴·전신·소품 기준

- 방향 얼굴, 정면 전신, 방향 전신, 리파인 전신, 소품은 각각 다른 입력 역할과 관찰 범위로 분리한다.
- 공용 identity·비율 계약은 현재 `p7-5-3-face-identity-contract.json`과 `p7-5-3-fullbody-proportion-contract.json`의 통합 방향을 따른다. 눈 색·머리·비율 문장을 각 생성기의 prompt에 중복 확장하지 않는다.
- 전신 생성은 정면 얼굴과 방향에 맞는 얼굴 시트를 참조하며, 방향·pose·camera 범위를 얼굴 이미지가 보장하는 범위로 오인하지 않는다.
- 기본 seed는 `62294` 계열을 사용하되, seed 변경은 별도의 생성 조건으로 기록한다.
- 정면 전신 고해상도 기준은 `960×1440`, 전신 기본 생성은 1차 `3 step`, 2차 `6 step`으로 비교한다. 좌·우 측면의 2차 고스텝 실험은 질감 개선을 보장하지 않았으므로 기본 조건으로 일반화하지 않는다.
- 얼굴 6장, 기본 전신 6장, 리파인 전신 6장은 P7-5.11 학습·증강에서 역할·조건·한계를 명시한 참고 입력이다. JSON은 상태 판정이 아니라 실행 결과와 관찰을 남긴다.
- 원고 표는 방향별 이미지를 반복 행으로 배치하며, `1열·2열·3열` 같은 구현 열 이름을 독자용 기준으로 노출하지 않는다.

### P7-5.4 — 장면·구조·guide

- 장면 계약과 캐릭터 계약을 분리한다. RGB는 색·질감·조명을, 상대 depth/Canny는 공간 윤곽·거리·가림의 보조 기준으로만 사용한다.
- RGB/depth는 얼굴·복장·화풍·사지 비율을 보장하지 않으며, 구조 입력으로 관찰한 범위만 전달한다.
- 단일 guide와 방향에 가까운 전신 한 장을 먼저 검수하고, 다중 전신 참조·crop 합성·lineart-only 경로는 형태 붕괴·사각형 이음새·추가 사지 때문에 제작 경로에서 제외했다.
- Animagine 및 과거 lineart 경로는 현재 비교 범위에서 제외한다. 구조 guide는 역할과 파생 원본을 명시한 RGB에서 만든다.
- P7-5.4는 최종 캐릭터 일관성 학습 단계가 아니라 pose·camera·장면을 독립적으로 관찰하는 단계다.

### P7-5.11 — 화풍·연속성·LoRA·VTON 보정

- LoRA 학습 데이터는 P7-5.1 화풍 참조와 P7-5.3 인물 기준의 역할을 분리한다. 화풍 없는 전신과 화풍 포함 증강을 섞을 때는 학습 목표를 명시하고 별도 검수한다.
- 손·발·관절 수, 얼굴 identity, 복장, 화풍, 배경 유무는 한 결과에 묶어 상태 판정하지 않는다. 학습 세트에는 입력 역할, 권리 근거, 생성 조건, 관찰된 한계를 명시한 자료만 넣는다.
- DiffEdit·수동 SDXL inpaint·일반 IP-Adapter의 반복 mask/CFG/strength sweep은 자동 mask 범위와 색·재질 전달 한계를 확인한 뒤 중단했다. mask가 얼굴·바지·신발까지 번지면 step 증가로 해결된다고 보지 않는다.
- CatVTON은 person·garment·mask를 분리하는 복장 후보 경로로 채택했다. source와 mask의 종횡비·좌표가 맞지 않으면 팔 바깥과 하체가 재킷으로 칠해진다.
- source-aligned mask 실험에서는 재킷과 바지의 부분 보존 신호가 있었고, 가방은 스트랩·실루엣 보존에 실패했다. 가방 포함 조합은 현재 일반화된 입력 경로로 쓰지 않는다.
- LoRA는 얼굴·복장·신체 비율을 동시에 보장하는 만능 제어로 해석하지 않는다. 학습 실패는 데이터 역할, 해상도, caption, rank/alpha, 추론 조건을 분리해 재검증한다.

역사적으로 P7-5.11에서 확인한 대표 경계도 다음처럼 압축한다.

- P7-5.1 배경 20장과 P7-5.3 얼굴·전신 기준으로 화풍 포함 스포츠 후보를 36장까지 확장했지만, 손발 수·비율·화풍 불일치 후보가 반복 탈락했다. 승인 전 후보와 review JSON은 학습 입력이 아니다.
- Animagine XL 화풍 LoRA pilot·SDXL base style LoRA는 8 GB에서 실행·adapter 저장까지 가능했지만, held-out 장면의 화풍 이득과 구도 안정성을 제작 gate로 승인할 근거는 얻지 못했다. 화풍 LoRA를 얼굴·복장·pose 해결책으로 일반화하지 않는다.
- DiffEdit 자동 mask와 수동 SDXL inpaint의 10회 이상 반복은 얼굴·하체·신발로 번지는 mask 또는 회색 재킷을 만들었다. step·CFG·strength·seed만 반복하는 경로는 중단하고, 입력 mask·garment conditioning·모델 선택을 별도 가설로 분리했다.
- 일반 IP-Adapter와 흰 재킷 reference의 scale·padding·border sweep은 포켓·소매 끝만 전달하고 흰 몸판·open-front·긴 소매를 안정화하지 못했다. CatVTON으로 전환한 이유는 person·garment·mask 계약을 분리하기 위해서다.
- SD15 OpenPose와 SDXL Canny는 구조·silhouette 보조로는 부분 통과했지만, identity·화풍·가방 geometry를 보장하지 않았다. 구조 gate와 identity/style gate를 합치지 않는다.

### P7-5.8 — 텍스트 모션·OpenPose 키프레임 준비

- 텍스트 모션 모델은 시간 순서가 있는 3D 관절 시퀀스를 만들고, OpenPose는 이를 같은 camera에서 2D 구조 guide로 기록하는 다음 단계로 분리한다.
- 8GB GPU의 첫 조건은 MoMask batch 1, 보행 48포즈 한 시퀀스다. 12개 키프레임은 인덱스 `0, 4, …, 44`를 균등 추출한다.
- 이 준비 조건은 모델 설치·실행 성공이나 identity·착장·화풍 보장을 뜻하지 않는다. 실제 result JSON에는 모델·가중치 버전, seed, frame 수, peak VRAM, 투영 규칙과 관찰 결과를 기록한다.

## 3. 이번 세션의 순차 실험 기록

이번 세션은 얼굴 → 복장 → 비율 → 쌍별 → 3중 결합의 순서로 실행했다. 공통 seed는 `62296`(스타일 얼굴 비교), 복장 CatVTON은 `62296`, 기존 기준과의 비교에는 `62294` 계열을 사용했다. 해상도는 얼굴·전신 비교에서 `768×1152`, CatVTON은 모델 반환 계약에 따라 `768×1024`를 사용했다.

### 3.1 얼굴 Adapter gate

- 입력: 승인된 스타일 얼굴 정면 PNG의 전체 입력과 얼굴·머리 crop.
- Plus Face Adapter: Euler/DDIM, scale `0.30/0.50` 비교. 스타일 입력에서는 3개 seed 중 2개가 단일 stylized face·청록 단발·호박색 눈의 조건부 gate를 통과했고, 한 seed는 collage였다.
- FaceID Plus v2: InsightFace landmark crop과 공식 FaceID+CLIP 경로를 실행했으나, 얼굴 embedding과 일러스트 기준의 분포 차이로 identity가 맞지 않아 탈락했다.
- 결론: 스타일 얼굴 Plus Face Adapter만 조건부 기준으로 고정한다. 정면 전체와 crop은 서로 대체하지 않으며, FaceID는 현재 제작 gate에 채택하지 않는다.

### 3.2 단계별 복장 gate

- 첫 CatVTON 실행에서 기존 마스크를 그대로 resize하자 재킷 영역 밖의 팔·하체까지 칠해지고 얼굴이 흔들렸다. 원인은 step 부족이 아니라 source/mask 좌표 불일치였다.
- source 크기에 맞춘 재킷 마스크로 재실행하자 얼굴과 하체가 유지되고 흰 cropped jacket이 목표 영역에 형성되었다. 재킷은 조건부 통과 후보로 기록한다.
- 같은 방식의 바지 마스크는 와이드 팬츠 실루엣을 복원했다. 바지는 조건부 통과 후보로 기록한다.
- 국소 가방 mask는 직사각형 덩어리 또는 스트랩이 사라진 형태를 만들었다. 가방은 탈락이며, 다음 실행에서 승인 가방 PNG와 스트랩 방향을 별도 조건으로 다시 설계해야 한다.

### 3.3 중립 전신·OpenPose gate

- 중립 전신은 얼굴·전신 비율이 상대적으로 안정적이었다.
- OpenPose는 큰 pose 구조를 제어했지만 얼굴·복장 색·세부 identity drift가 증가했다.
- 결론: OpenPose는 신체 비율·자세 보조로만 사용하고 얼굴 Adapter와 강하게 결합하지 않는다. 50 step은 얼굴 형성에 충분했으며, 단순 step 증가만으로 identity drift가 해결되지 않았다.

### 3.4 쌍별 검수

- 얼굴+복장: source-aligned 재킷·바지는 조건부 통과, 가방 포함은 탈락.
- 얼굴+비율: OpenPose scale `0.3/0.6/0.9`를 비교했다. `0.3`은 복장·얼굴 drift가 크고, `0.6`이 가장 나은 절충 후보였으며, `0.9`는 과제어 후보로 분리했다.
- 복장+비율: CatVTON 결과를 SDXL ControlNet img2img에 넣었다. strength `0.25`는 복장 보존은 좋지만 pose 반영이 약했고, `0.50`은 pose 제어와 가방 스트랩이 일부 회복되지만 얼굴·복장 세부가 더 흔들렸다. 완전 통과가 아닌 조건부 비교 결과다.

### 3.5 세 제어 결합 격자

- 구성: CatVTON 재킷·바지 source + SDXL img2img + Plus Face Adapter + OpenPose.
- 가중치: face scale/control scale을 각각 `0.3/0.6/0.9`로 맞춘 3개 후보를 생성했다. 세 후보 모두 복장 실루엣은 대체로 유지했지만 OpenPose 자세 변화는 약했고 가방은 직사각형으로 남았다.
- 판정: 전체 캐릭터 계약은 탈락. `face adapter + source-aligned 재킷·바지 + OpenPose 0.6, 가방 제외`만 실험 체크포인트로 보존한다. 승인 제작 자산이나 학습 입력으로 자동 승격하지 않는다.

### 가방·스트랩 conditioning 비교

- 같은 source(`.tmp/p7-5-11-face-fixed-catvton-pants/candidate.png`), source-aligned 가방+스트랩 마스크, `768×1024`, CatVTON 30 step, guidance `2.5`, seed `62294`를 고정하고 참조만 바꿨다.
- 승인된 가방 단독 PNG와 전면 착장 PNG를 각각 넣었지만 두 결과 모두 가방 영역이 갈색 둥근 덩어리로 치환되고 대각선 스트랩이 복원되지 않았다. 얼굴도 보존 gate를 통과하지 못했다.
- 결론: 이번 결과는 참조 PNG 선택 문제가 아니라 CatVTON의 국소 가방 conditioning과 현재 마스크 표현이 가방 실루엣·스트랩 구조를 전달하지 못한 실패로 기록한다. 두 PNG는 승인·학습 입력으로 승격하지 않는다.
- 검수 기록: `.tmp/p7-5-11-bag-conditioning-comparison-review.json`. 이 결과는 최종 보정 수단의 사전 체크포인트로만 남긴다.

### SDXL 국소 inpaint 대안

- CatVTON과 동일한 source-aligned 가방·스트랩 mask와 seed `62294`를 사용해 SDXL inpainting `768×1024`, 30 step, strength `0.65`, guidance `7.0`을 실행했다.
- SDXL 결과는 얼굴·흰 재킷·청록 바지를 보존했고, 어깨에서 이미지 오른쪽 힙으로 내려오는 스트랩도 복원했다. 다만 가방 본체가 승인 PNG의 네이비 플랩형 실루엣이 아닌 어두운 질감의 사다리꼴로 생성되어 본체 gate는 조건부다.
- 판정: 얼굴·복장·스트랩은 부분 통과, 가방 본체·색·플랩 디테일은 미통과. 이 PNG는 제작 승인·학습 입력으로 승격하지 않고, CatVTON 대비 SDXL 국소 inpaint가 더 유망한 체크포인트로만 보존한다.
- 검수 기록: `.tmp/p7-5-11-sdxl-bag-inpaint-review.json`. Inpaint·VTON은 기본 생성 경로가 아니라 마지막 보정 단계에서만 재검토한다.

### LoRA 단독 기준 실험

- Inpaint·VTON·ControlNet·이미지 reference를 모두 제외하고 Animagine XL 4.0에 캐릭터 LoRA만 적용했다. `512×768`, 30 step, LoRA scale `0.6`, seed `62295/62296`을 사용했다.
- 정면 후보는 얼굴·단발·복장 색·전신 비율이 부분적으로 유지됐지만, 3/4 후보는 화풍·복장 구조·가방 형태가 크게 흔들렸다.
- 판정: LoRA는 identity와 색상 경향을 보조하는 조건부 체크포인트이며, pose/camera와 복장 구조를 단독으로 고정하지 못한다. 다음 순서는 LoRA를 고정한 뒤 pose/camera 구조 제어를 별도 비교하는 것이다. Inpaint·VTON은 여전히 마지막 보정 단계로 둔다.
- 검수 기록: `.tmp/p7-5-11-lora-only-next-review.json`.

### LoRA 단독 960×1440 해상도 비교

- 동일한 LoRA scale `0.6`, 30 step, seed `62295/62296`, 프롬프트와 모델을 유지하고 출력만 `960×1440`으로 올렸다. 이미지 reference·ControlNet·Inpaint·VTON은 사용하지 않았다.
- 저해상도 대비 전신 구조, 옷 경계, 가방·스트랩 배치가 안정되었다. 그러나 우측 3/4에서 머리색 변형과 화풍·복장 편차가 남아 해상도만으로 identity 고정이 해결되지는 않았다.
- 판정: `960×1440`을 이후 실험의 기본 해상도로 채택한다. 다음은 이 해상도에서 identity/style conditioning을 별도 비교하고, 그 뒤 pose/camera 제어를 추가한다.
- 검수 기록: `.tmp/p7-5-11-lora-only-960x1440-review.json`.

### 960×1440 LoRA 60 step 비교

- `960×1440`, LoRA scale `0.6`, seed `62295/62296`을 고정하고 30 step에서 60 step으로만 올렸다.
- 60 step은 선과 복장 경계를 약간 선명하게 했지만, 우측 3/4에서 나타난 머리색·화풍·복장 편차는 거의 그대로였다. 정면은 여전히 조건부 통과, 3/4도 구조는 유지되지만 identity/style은 조건부다.
- 결론: step 증가는 세부 품질 개선에는 유효하지만 캐릭터 고정력의 단독 해결책은 아니다. 다음에는 960×1440을 유지한 채 identity/style conditioning을 추가하고, 이후 pose/camera를 비교한다.
- 검수 기록: `.tmp/p7-5-11-lora-only-960x1440-steps60-review.json`.

### 960×1440 Face Adapter + LoRA 비교

- `960×1440`, 30 step, LoRA scale `0.6`, Face Adapter scale `0.35`, seed `62295/62296`을 사용했다. ControlNet·Inpaint·VTON은 제외하고 정면 얼굴 reference만 추가했다.
- LoRA 단독보다 청록 단발·호박색 눈·얼굴 identity가 안정됐고 스트랩도 나타났다. 그러나 재킷과 바지 실루엣이 승인 복장과 달라 복장 gate는 실패했다.
- 판정: Face Adapter는 identity 보조로 유효하지만 복장 보존과 충돌한다. 다음 실험은 identity와 outfit/reference 역할을 분리하고, pose/camera 제어는 그 이후에 추가한다.
- 검수 기록: `.tmp/p7-5-11-face-adapter-lora-960x1440-review.json`.

### 960×1440 Face + outfit reference + LoRA 비교

- 얼굴 reference와 승인 전면 착장 reference를 dual IP-Adapter로 넣고 LoRA scale `0.6`, adapter scale `[0.25, 0.35]`, 30 step, seed `62295/62296`을 사용했다. ControlNet·Inpaint·VTON은 제외했다.
- 정면에서는 재킷·가방·스트랩이 더 잘 나타났지만 바지가 발목까지 내려오지 않았다. 우측 3/4에서는 바지와 다리 형태가 크게 붕괴했다.
- 판정: 복장 reference는 정면 보조에는 효과가 있으나 방향 일반화와 구조 보존은 실패했다. 다음은 pose/camera 구조 제어를 별도 추가해 reference의 방향 의존성을 검증한다.
- 검수 기록: `.tmp/p7-5-11-face-outfit-adapter-lora-960x1440-review.json`.

### 960×1440 OpenPose 구조 제어 비교

- 첫 실행은 OpenPose skeleton이 아닌 인물 RGB를 ControlNet 입력으로 넘긴 오류가 있어 OpenPose 결과로 무효 처리했다. 해당 후보는 판정 근거로 사용하지 않는다.
- 실제 skeleton map으로 `960×1440`, 30 step, seed `62296`, 얼굴·전면 착장 dual reference와 LoRA를 고정하고 ControlNet scale `0.8/1.0`을 비교했다.
- `1.0`은 다리·몸통의 큰 배치를 더 강하게 따르게 했지만, 두 조건 모두 목표 우측 3/4 카메라 회전을 충분히 만들지 못했다. 복장·가방·스트랩은 조건부로 남고 identity도 부분 통과다.
- 판정: OpenPose는 2D 관절·전신 배치에는 유효하지만 camera/rotation을 단독으로 고정하지 못한다. 다음 구조 실험은 camera-specific conditioning을 별도로 검증한다.
- 검수 기록: `.tmp/p7-5-11-true-openpose-scale-ab-review.json`.

### 우측 3/4 얼굴 reference 교체

- OpenPose·전면 착장 reference·LoRA·`960×1440` 조건을 고정하고 얼굴 reference만 우측 3/4 자산으로 바꿨다.
- 결과는 우측 3/4 카메라로 안정되지 않았고, 가방이 이탈하며 어깨-힙 스트랩이 끊겼다. 얼굴도 조건부에 그쳤다.
- 판정: 방향별 얼굴 reference 교체만으로 pose/camera나 소품 구조를 해결할 수 없다. 다음 비교는 얼굴 reference를 고정하고 OpenPose 제어 강도만 분리한다.
- 검수 기록: `.tmp/p7-5-11-face-right-quarter-outfit-lora-openpose-960x1440-review.json`.

### 우측 3/4 Canny camera 구조 비교

- 우측 3/4 전신 기준의 Canny edge를 구조 입력으로 사용하고, 얼굴·전면 착장 dual reference와 LoRA를 `960×1440`, 30 step, seed `62296`에서 고정했다.
- Canny는 우측 3/4 걷기 방향과 전신 비율을 가장 잘 전달했다. 그러나 흰 재킷이 사라지고 한쪽 눈이 무너졌으며 가방·스트랩도 부분 통과에 그쳤다.
- 판정: Canny는 camera/pose 조건으로 부분 통과하지만 appearance 조건과 경쟁한다. 기본 생성·reference·LoRA·구조 조건이 모두 검증된 뒤에도 camera·silhouette 결함이 남을 때만 최후 보정 후보로 검토하며, 이 후보는 승인하지 않는다.
- 검수 기록: `.tmp/p7-5-11-face-outfit-lora-canny-960x1440-review.json`.

> 한계: Canny는 기준 이미지에 이미 보이는 외곽·가림 관계를 전달할 뿐, 새 동작을 선언적으로 지정하는 조건이 아니다. 특히 팔·다리·소품이 서로 가려지는 동작에서는 edge가 부족하거나 충돌해 신체 형태와 가림 순서를 고정하지 못했다. 따라서 다양한 포즈 생성의 기준 경로로는 사용하지 않고, Inpaint·VTON과 마찬가지로 camera·silhouette의 최후 보정 후보로만 제한한다.

### Canny + Face Adapter scale 0.50 비교

- Canny scale `0.75`, 착장 adapter `0.25`, LoRA `0.6`, `960×1440`, 30 step, seed `62296`을 고정하고 Face Adapter만 `0.35`에서 `0.50`으로 올렸다.
- camera·걷기 구조와 전신 비율은 유지됐지만, 한쪽 눈 붕괴와 흰 재킷 소실은 회복되지 않았다.
- 판정: 이 Canny 결합에서 Face Adapter scale은 identity·복장 실패의 해결 변수가 아니다. 추가 scale sweep은 중단한다.
- 검수 기록: `.tmp/p7-5-11-face-outfit-lora-canny-960x1440-face50-review.json`.

### 재사용 OpenPose map 자산

- detector를 매 실험에서 다시 실행하지 않도록 승인 전신 기준의 정면·우측 3/4·좌측 측면·우측 측면·후면 OpenPose skeleton map을 정적 자산으로 저장했다.
- 생성기는 `p7_5_11_prepare_openpose_maps.py`이며, 저장 파일은 모두 `p7-5-11-openpose-...-reference.png` 형식으로 `openpose` 키워드를 포함한다.
- 이후 OpenPose 실험은 이 자산을 직접 입력으로 사용한다. 구조 실험의 재현성은 높아지지만, 2D skeleton map이 camera/rotation 정보를 충분히 주지 못한다는 기존 판정은 유지한다.

### LoRA 학습 기반 일치 비교

- 앞선 LoRA 단독·Face Adapter·OpenPose·Canny 결합 중 SDXL Base 1.0으로 학습한 `.tmp/p7-5-11-character-lora-sdxl-base-identity-18-bucketed/`를 Animagine XL 4.0에 연결한 결과는 학습 기반과 추론 기반이 달랐다. 해당 결과는 해상도·step·조건 결합의 탐색 기록으로만 유지하며, LoRA 자체의 성능 판정 근거에서는 제외한다.
- 기반이 일치하는 두 LoRA를 image reference·ControlNet·Inpaint·VTON 없이 `960×1440`, 30 step, scale `0.6`, seed `62295/62296`으로 다시 비교했다. tagged 12장 학습 LoRA와 P7-5.3 승인 turnaround/full-body 학습 LoRA 모두 정면에서 청록 단발·호박색 눈·흰 재킷·청록 와이드 바지·네이비 가방을 식별 가능하게 유지했다.
- 학습 기록을 재검수했다. P7-5.3 turnaround LoRA는 11장·300 step·`384×512`이고 모든 sample에 같은 긴 identity caption을 사용해 방향·복장 차이를 명시적으로 학습하지 않은 8 GB feasibility pilot이다. tagged LoRA도 12장·300 step·`320×448`의 identity-anchor pilot이다. 54장 action LoRA는 `320×448`, 600 step으로 이미지당 약 11회 노출에 그쳐, identity·복장·동작을 함께 학습하기에는 부족하다.
- 따라서 turnaround LoRA가 정면에서 상대적으로 안정적이더라도 기준선으로 승인하지 않는다. 우측 3/4의 옅은 바지색과 신발 겹침은 이 결론과 일치한다. 현재 Animagine XL 캐릭터 LoRA 중 제작 기준선으로 쓸 만큼 충분히 학습된 adapter는 없다.
- 다음은 방향·복장·동작을 구분한 caption과 고해상도 bucket을 갖춘 새 Animagine XL character-LoRA 학습 설계다. Canny·Inpaint·VTON은 이 학습 검증 경로에 넣지 않는다.
- 검수 기록: `.tmp/p7-5-11-lora-adapter-compatibility-review.json`.

### 54장 고해상도 Animagine XL character-LoRA 성능시험

- 승인된 화풍 적용 54장(18 identity anchor·36 action), 고유 caption 54개, 정사각·세로 원본 비율을 확인했다. 기존 `320×448` pilot 대신 square `640×640`·full-body `640×960` bucket, rank/alpha `8`, bf16, learning rate `1e-4`, 1,200 step으로 학습했다.
- `768/1152`와 `640/960` bucket은 일반 UNet 역전파에서 8 GB GPU OOM이 났다. UNet gradient checkpointing을 추가하자 `640/960` 학습은 peak `5,314 MiB`에서 완료했다. 이는 activation 재계산으로 속도와 메모리를 교환한 학습 경로다.
- 같은 Animagine XL 4.0, `960×1440`, 30 step, seed `62295/62296`, scale `0.6`에서 LoRA off/on을 비교했다. on 정면은 청록 단발·호박색 눈·흰 크롭 재킷·차콜 crop top·청록 와이드 바지·네이비 가방을 함께 유지했고, 보행 변형도 off보다 캐릭터와 복장 계약을 훨씬 안정적으로 유지했다.
- 판정: 이 adapter는 이전 300/600-step 저해상도 pilot과 달리 화풍·복장 기준의 성능시험을 통과한 조건부 후보다. 얼굴 동일성은 방향·동작이 바뀌면 약하므로 LoRA 단독 통과로 보지 않는다. 보행 prompt는 정적인 쿼터 포즈로 수렴했으므로 새 동작의 정확한 제어까지 통과한 것은 아니다. Canny·Inpaint·VTON 없이 pose 제어를 분리해 다음 gate에서 검증한다.
- 재현 기록: `.tmp/p7-5-11-animagine-character-lora-54-640-1200-gc/report.json`, `.tmp/p7-5-11-animagine-character-lora-54-640-1200-gc-eval/`.

### 새 character-LoRA + 정적 OpenPose map 재검증

- 새 54장 LoRA만 적용한 뒤, 재사용 자산 `p7-5-11-openpose-fullbody-front-quarter-right-reference.png`를 직접 입력으로 넣었다. 이미지 reference·Canny·Inpaint·VTON은 모두 제외했고, Animagine XL 4.0, `960×1440`, 30 step, seed `62296`, LoRA scale `0.6`을 고정해 ControlNet scale `0.0/1.0`만 비교했다.
- `0.0`은 캐릭터·재킷·가방은 안정적이나 map의 넓어진 하체 배치를 따르지 않았다. `1.0`은 다리·발의 큰 배치를 더 강하게 따르면서 청록 단발·호박색 눈·흰 재킷·와이드 바지·가방을 유지했다. peak VRAM은 `3,371 MiB`였다.
- 판정: 새 LoRA는 이전 저해상도 pilot과 달리 OpenPose의 2D pose 조건과 함께 사용해도 appearance를 유지하는 부분 통과다. 머리·흉곽의 정확한 회전과 가방의 가림 순서는 map만으로 고정되지 않으므로 camera/3D pose 통과로 일반화하지 않는다.
- 재현 기록: `.tmp/p7-5-11-animagine-lora54-static-openpose-quarter-right/`.

### 새 character-LoRA + 선언형 OpenPose 동작 map

- 기존 인물 PNG에서 skeleton을 추출하지 않고, 오른팔을 위로 뻗고 양발로 선 18개 관절 좌표를 `960×1440` OpenPose map으로 한 번 정의했다. 캐릭터·의상·배경 픽셀 reference, Canny·Inpaint·VTON은 넣지 않았다.
- 같은 Animagine XL, 새 54장 LoRA scale `0.6`, 30 step, seed `62301`에서 ControlNet `0.0/1.0`을 비교했다. `0.0`은 팔이 옆으로 뻗고 재킷 레이어가 허리로 흘러 동작·복장이 함께 흔들렸다. `1.0`은 오른팔을 위로 올린 map의 구조를 따르면서 청록 단발·호박색 눈·흰 크롭 재킷·가방·두 다리를 유지했다. 바지는 옅은 청록으로 변했지만 전신 비율은 정상이다.
- 판정: 새 LoRA와 선언형 OpenPose는 새 상체 동작의 2D 구조 및 캐릭터·화풍·복장 계약을 동시에 유지하는 조건부 통과다. 색·가방 세부와 3D camera는 남은 gate이며, 이 결과만으로 모든 동작 generalization을 주장하지 않는다.
- 재현 기록: `.tmp/p7-5-11-animagine-lora54-declarative-openpose-reach-up/`.

### 선언형 OpenPose 하이앵글 camera 문구 비교

- 오른팔 올리기 선언형 OpenPose map, Animagine XL `960×1440`, 30 step, seed `62302`, 새 54장 LoRA scale `0.6`, ControlNet `1.0`을 고정하고 camera 문구만 eye-level/high-angle으로 바꿨다. image reference·Canny·Inpaint·VTON은 사용하지 않았다.
- 두 출력 모두 재킷·상의·바지·가방 계약은 유지했지만, high-angle 후보도 거의 정면 전신 구도에 남았다. 하이앵글의 위에서 내려다보는 원근·머리 윗면·바닥 비율은 만들어지지 않았다.
- 판정: OpenPose map과 camera 문구만으로 하이앵글은 미통과다. 이 결과는 OpenPose가 2D 관절 위치를 전달할 뿐 camera 깊이·원근을 전달하지 않는다는 기존 경계를 강화한다. 다음 camera 실험은 별도 camera-specific 구조 조건을 검증해야 하며, Canny는 여전히 마지막 보정 후보로 제한한다.
- 재현 기록: `.tmp/p7-5-11-animagine-lora54-openpose-high-angle-ab/`.

### PreciseCam text-only 하이앵글 feasibility

- Blender·SMPL·RGB reference 없이, prompt·seed `62303`·`1024×1024`·30 step을 고정하고 PreciseCam PF-US의 pitch만 `0°/55°`로 비교했다. roll `0°`, vertical FOV `50°`, distortion `xi=0.2`를 고정했다.
- 공식 `model CPU offload`는 8 GB에서 UNet 이동 직전 20 MiB 부족으로 OOM이었다. `sequential CPU offload`에서는 peak `2,560 MiB`, `86.7초`로 두 후보 생성이 완료됐다.
- `55°` 후보는 `0°` 후보와 다른 위에서 내려다보는 시점·건축 원근을 보여 PF-US camera condition 자체는 작동했다. 하지만 공개 모델 단독은 전신 구도, Mira 얼굴, 승인 복장·가방 계약을 유지하지 못했다.
- 판정: 8 GB text-only camera control의 실행·시점 변화는 부분 통과다. 이 공개 PreciseCam은 캐릭터 LoRA·OpenPose와의 결합 전에는 제작 자산으로 승인하지 않는다. 다음 gate는 custom Diffusers 기반에서 character-LoRA를 결합할 수 있는지와, 결합 뒤에도 pitch 효과와 캐릭터 계약이 함께 남는지의 분리 검증이다.
- 재현 기록: `.tmp/p7-5-11-precisecam-high-angle-pitch-ab/`.

### PreciseCam high-angle + character-LoRA 결합 검증

- PreciseCam PF-US pitch `55°`, prompt·seed `62304`·`1024×1024`·30 step을 고정하고, 기존 54장 Animagine XL character LoRA만 off/on(scale `0.6`)으로 비교했다. mesh·pose map·RGB reference·Canny·Inpaint·VTON은 사용하지 않았으며 sequential CPU offload에서 peak `2,560 MiB`, `90.7초`로 완료됐다.
- LoRA off는 high-angle 구도 안에서 기본 복장을 일부 유지했지만, LoRA on은 모자·과장된 청록 재킷·새 소품·비정상 신체를 만들었다. 캐릭터 계약을 강화하는 결과가 아니었다.
- 판정: 이 결과는 character LoRA의 하이앵글 일반화 실패가 아니라 **base model 불일치**다. LoRA는 Animagine XL 4.0에서 학습됐고 PreciseCam은 SDXL Base 1.0을 기반으로 하므로, 결합 결과를 LoRA 성능의 근거에서 제외한다. 이후 같은 SDXL Base 1.0에서 학습된 기존 54장 LoRA(`768/1152`, 1,200 step)를 찾아 별도 A/B로 다시 검증한다.
- 재현 기록: `.tmp/p7-5-11-precisecam-character-lora-high-angle-ab/`.

### PreciseCam high-angle + same-SDXL-base 54장 character-LoRA

- PreciseCam PF-US pitch `55°`, prompt·seed `62304`·`1024×1024`·30 step을 고정하고, SDXL Base 1.0 기반 54장 character LoRA(`768/1152`, 1,200 step)만 off/on(scale `0.6`)으로 비교했다. mesh·pose map·RGB reference·Canny·Inpaint·VTON은 사용하지 않았으며 sequential CPU offload에서 peak `2,560 MiB`, `90.8초`로 완료됐다.
- LoRA on은 절제된 화풍, 청록 단발, 흰 크롭 재킷, 청록 와이드 바지를 off보다 더 일관되게 만들었다. 반면 화면은 여전히 거의 수평 전신 구도이며, 기대한 하이앵글의 원근·얼굴 동일성·가방 세부 계약은 제작 기준에 도달하지 못했다.
- 판정: base model을 맞추면 LoRA의 화풍·복장 보조 효과는 확인된다. 하지만 이번 조건에서 병목은 LoRA가 아니라 camera condition의 강도와 identity 세부다. PreciseCam+LoRA를 제작 자산 생성 경로로 승인하지 않으며, 별도 camera 구조 조건과 얼굴 gate가 남는다.
- 재현 기록: `.tmp/p7-5-11-precisecam-sdxl54-character-lora-high-angle-ab/`.

### PreciseCam same-base LoRA pitch sweep

- 같은 SDXL Base 54장 LoRA scale `0.6`, prompt·seed `62304`·`1024×1024`·30 step·vertical FOV `50°`·`xi=0.2`를 고정하고 PF-US pitch만 `25°/40°/55°/70°`으로 바꿨다. mesh·pose map·RGB reference·Canny·Inpaint·VTON은 사용하지 않았고, four-condition 실행의 peak는 `2,560 MiB`, 총 `220.1초`였다.
- 네 후보는 화풍·청록 단발·흰 크롭 재킷·청록 바지라는 LoRA 계약은 대체로 유지했지만, pitch가 커져도 인물의 위치와 머리 기울기만 조금 달라졌다. 위에서 내려다보는 전신 원근과 의도한 팔 올리기 동작은 형성되지 않았다.
- 판정: 이 공개 PreciseCam과 현재 full-body text 조건에서 pitch 단독 sweep은 camera gate를 통과하지 못했다. FOV를 추가로 바꾸는 것은 같은 실패 원인을 겹칠 가능성이 크므로 중단한다. 이후 하이앵글은 camera를 실제로 구속하는 구조 조건 또는 별도 camera-compatible 생성 경로가 생길 때만 다시 연다.
- 재현 기록: `.tmp/p7-5-11-precisecam-sdxl54-pitch-sweep/`.

### SDXL rank-128 Depth Control-LoRA 고각도 scaffold

- 공식 rank-128 Depth Control-LoRA, 같은 SDXL Base 54장 character LoRA scale `0.6`, 승인된 P7-5.3 고각도 storyboard depth scaffold를 결합했다. `768×768`, 50 step, seed `62305`에서 depth condition scale `0.0/1.0`만 비교했다. sequential CPU offload의 peak는 `1,445 MiB`, 총 `151.3초`였다.
- condition `1.0`은 공중 동작의 넓은 팔다리 실루엣과 청록 머리·흰 재킷·청록 바지를 `0.0`보다 강하게 따랐다. 다만 얼굴과 몸통은 거의 정면 투영에 머물러 scaffold의 버드아이뷰 camera까지 옮기지는 못했다.
- 판정: Control-LoRA의 경량 실행성은 8GB에서 통과했지만, 공식 Depth Control-LoRA는 camera adapter가 아니라 depth 구조 adapter다. 하이앵글 제작 경로로 승인하지 않고, 동작 실루엣 보조 후보로만 남긴다.
- 재현 기록: `.tmp/p7-5-11-sdxl-control-lora-high-angle-depth/`.

### 선언형 동작에서 LoRA scale `0.6/0.8` 비교

- 오른팔 올리기 OpenPose map, ControlNet `1.0`, seed `62301`, `960×1440`, 30 step을 고정하고 LoRA scale만 `0.6/0.8`로 비교했다.
- 두 후보 모두 팔·전신 비율·재킷·가방은 유지했다. 그러나 `0.8`은 와이드 바지를 거의 흰색으로 과도하게 끌어가며 `0.6`보다 색 계약에서 더 멀어졌다.
- 판정: 이 LoRA에서 scale 증가는 바지 색 이탈의 해결책이 아니다. ControlNet 결합의 기준 scale은 `0.6`으로 유지하고, 더 높은 scale sweep은 중단한다.
- 재현 기록: `.tmp/p7-5-11-animagine-lora54-declarative-openpose-reach-up-lora-scale-ab/`.

### Depth 고각도에서 전신·얼굴 IP-Adapter 역할 분리

- 동일한 high-angle relative-depth 입력, SDXL Base 1.0 character LoRA scale `0.6`, depth scale `0.8`, `768×1152`, seed `62431`, 50 step을 고정했다. 이전의 일반 Plus 하나에 전신·얼굴 참조를 함께 넣은 조건과 달리, 승인 전신 참조는 일반 Plus scale `0.18`, 정면 얼굴 참조는 별도 Plus-Face scale `0.35`로 분리했다. sequential CPU offload에서 `96.0초`에 완료됐다.
- 결과는 고각도·전신 배치를 유지하면서 청록 단발과 양쪽 호박색 눈 신호를 이전 단일 Plus 결합보다 더 뚜렷하게 남겼다. **얼굴 조건을 전용 adapter로 분리하면 identity 단서가 개선될 수 있다는 의미 있는 부분 통과**로 분류한다.
- 전신 참조 Plus를 `0.30`으로 올린 비교 조건에서도 고각도·얼굴은 유지됐고, 흰색·차콜·청록·네이비의 **의상 색상**은 목표 범위로 수렴했다. 이 색상 일치도는 역할 분리와 전신 참조 강화가 만든 추가 개선으로 기록한다.
- 다만 흰 cropped jacket은 반소매처럼 변형되고, charcoal crop top의 레이어·와이드 바지의 실루엣·네이비 crossbody bag의 형태는 유지되지 않았다. 따라서 이 결과는 얼굴 identity와 의상 색상 개선 체크포인트일 뿐, **의상 형태 계약은 미통과**이며 복장·소품까지 포함한 캐릭터 일관성 또는 제작 자산 통과가 아니다. 얼굴·전신 조건을 한 adapter에 합치는 경로보다 역할 분리를 우선하되, 복장 형태 계약은 별도의 1차 생성 조건에서 독립적으로 검증한다.
- 같은 camera·depth·참조·seed 조건에 승인 의상 7장으로 학습한 same-SDXL-base outfit LoRA를 scale `0.30`으로 추가했다. 결과는 픽셀 단위로는 달라졌지만 재킷의 반소매화, 상의 레이어 누락, 가방 형태 미형성이라는 핵심 실패가 그대로였다. 이 소규모 outfit LoRA는 이번 고각도 1차 생성에서 색상 보조 이상의 **의상 형태 조건으로 작동하지 않았다**. scale sweep은 반복하지 않는다.
- 재현 기록: `.tmp/p7-5-11-sdxl-mira-anonymous-high-angle-depth-role-separated/run.json`, `depth-role-separated-review-sheet.png`, `.tmp/p7-5-11-sdxl-mira-anonymous-high-angle-depth-role-separated-global-0.30-face-0.35/run.json`, `depth-role-separated-review-sheet.png`.

### 카메라 구조와 후반 보정의 경계

- 고각도·원근·인물의 화면상 투영은 첫 생성 단계의 구조 조건이 결정한다. 이 구조가 불안정하거나 목표 의상과 함께 형성되지 않은 후보에 인페인트·VTON·국소 IP-Adapter를 나중에 적용해도, 카메라 계약을 회복하거나 안정화하는 경로로 보지 않는다.
- 이번 high-angle 얼굴 개선 후보에 source-aligned 재킷 CatVTON을 적용한 결과도 같은 경계를 재확인했다. 얼굴과 배경의 큰 위치는 남았지만, 흰 cropped jacket은 과대한 어두운 상의로 변했다. 이는 camera 고정 해법이나 다음 복장 단계의 입력으로 사용하지 않으며, 바지·가방 후속 전환도 진행하지 않는다.
- 운영 규칙: 후반 보정은 이미 사람 검수를 통과한 camera·pose·전신 비율을 **보존**하는 국소 의상·소품·경계 수정에만 허용한다. camera/pose 실패 후보에는 후반 보정을 연결하지 않고, 다음 실험은 1차 생성에서 camera·face·outfit의 동시 형성 가능성을 검증한다.
- 재현 기록: `.tmp/p7-5-11-high-angle-catvton-jacket/run-01/contact-sheet.png`.

### FitDiT 고각도 상의 형태 조건 비교

- [FitDiT](https://github.com/BoyuanJiang/FitDiT)는 garment transformer와 VTON transformer를 분리한 virtual try-on 모델이다. 공식 데모의 aggressive offload 구현은 offload 전에 전체 pipeline을 GPU로 이동시키므로, 8 GB 조건에서는 이를 건너뛰고 처음부터 sequential CPU offload로 올리는 최소 실행기로 재현했다. `768×1024`, 30 step, guidance `2.5`, seed `62431`에서 두 실행 모두 약 `33초`에 완료됐다.
- camera-approved 고각도 source와 pose map은 고정하고, 사람 검수로 만든 상체 mask만 전달했다. 단독 `jacket-crop-top-front` reference와 승인 `complete-outfit-front-hip` reference를 각각 비교했다. 두 조건 모두 흰 재킷의 중앙 몸판, 포켓, 앞여밈, crop 밑단을 새로 만들었지만, 이는 승인 의상 객체의 고유 구조가 아니라 일반적인 재킷 문법에 가까웠다.
- 두 조건 모두 탑뷰의 양팔·소매 영역은 회색 덩어리로 바뀌었고, 전면 착장 reference도 기준의 소매·레이어·스트랩을 복원하지 못했다. 따라서 FitDiT는 **8 GB 실행성 및 mask 내부 형태 변화만 부분 통과**이며, 의상 객체 identity·전신 의상 계약은 미통과다. 더 중요한 결론은 mask 기반 VTON/inpaint가 새 camera에서 동일 의상 객체를 재표현해야 하는 현재 목표의 주 경로에 맞지 않는다는 점이다. 이 결과를 camera 복구나 의상 identity 생성 경로로 사용하지 않는다.
- 재현 기록: `.tmp/p7-5-11-fitdit-high-angle-upperbody-tight-mask/`, `.tmp/p7-5-11-fitdit-high-angle-upperbody-complete-outfit-tight-mask/`.

### DreamFit 의상 참조와 착용자 참조 대리 실험

- [DreamFit](https://github.com/bytedance/DreamFit)의 SD 1.5 image-to-image 경로는 평면 의상 이미지를 reference UNet에 직접 조건으로 넣는다. 공식 SD 1.5·DreamFit 가중치를 FP16으로 올리면 7.5 GB VRAM에서도 동작했다. FP32 전체 적재는 약 6.18 GB에서 추가 50 MB조차 확보하지 못해 실패했다.
- 이 경로에는 pose 또는 camera 조건 입력이 없다. 이번 출력은 정면 전신 구도만 생성했으며, **DreamFit이 고각도 camera를 만들거나 보존한다는 결론은 내리지 않는다.** camera는 별도의 1차 생성에서 먼저 통과해야 한다.
- 착용자 전신 참조를 고정한 채 `high-angle view, looking down`, `overhead camera directly above`, `birdseye view`, `elevated high-angle camera`를 각각 텍스트로만 추가한 네 조건을 비교했다. 네 출력 모두 눈높이 정면에 가까운 구도를 유지했다. 문구는 머리 기울기·시선·가방 위치에는 일부 영향을 주었지만 위에서 내려다보는 원근을 만들지 못했다. 따라서 이 설정에서 DreamFit의 text-only camera 제어는 고각도 재현 수단으로 탈락이다.
- 승인 `jacket-crop-top-front`를 입력해 `ref_scale` `0.6`, `1.0`, `1.4`를 비교했다. 세 조건 모두 흰 크롭 재킷의 짧은 밑단·깃·앞단추·포켓·긴소매와 청록 바지는 유지했지만, Mira의 얼굴과 헤어 identity는 무너지고 가방도 사라졌다. reference strength 조절은 이를 고치지 못했다.
- 평면 의상 대신 승인 `fullbody-front-refined-reference`처럼 **같은 의상을 입은 Mira 전신 이미지**를 전달한 대리 조건에서는 재킷·가방 스트랩·가방·청록 바지·청록 단발이 동시에 유지됐다. 얼굴은 여전히 비식별형이어서 최종 캐릭터 생성에는 미통과지만, 착용자 참조가 의상 객체의 실제 착용 형태와 소품 관계를 보강한다는 신호는 확인됐다.
- 이 신호는 RefTon의 `cloth + person + image_ref` 설계와 정합한다. RefTon은 실제 착용자 `image_ref`를 지원하지만 FLUX-Kontext가 필요하며, 공식 스크립트는 전체 파이프라인을 GPU로 이동한다. 따라서 8 GB에서는 CPU offload를 적용한 `512×384`, 단일 샘플의 상위 비교군으로만 검토한다. DreamFit은 의상 객체 조건의 실용 검증 경로이고, RefTon은 그 착용자 참조 가설을 검증할 후속 경로다.
- 재현 기록: `.tmp/p7-5-11-dreamfit-sd15-jacket-ab/`, `.tmp/p7-5-11-dreamfit-sd15-worn-reference-proxy/`, `.tmp/p7-5-11-dreamfit-sd15-high-angle-prompt/`, `.tmp/p7-5-11-dreamfit-sd15-high-angle-ab/`.

### Qwen-Image-Edit-2509 3입력 역할 분리 고각도 편집

- [Qwen-Image-Edit-2509 공식 문서](https://github.com/QwenLM/Qwen-Image/blob/main/Qwen-Image-Edit-2509.md)의 1–3 입력 편집 범위와 [Nunchaku의 Qwen 편집 예제](https://github.com/nunchaku-ai/nunchaku/blob/main/examples/v1/qwen-image-edit-2509.py)를 바탕으로, Nunchaku FP4 r128·per-layer CPU offload로 실행했다. `768×1152`, 40 step, 약 `16분 32초`, GPU 사용량 약 `3.5–3.7 GiB`로 두 실행 모두 8 GB 안에서 완료했다.
- 입력 역할은 고정했다. image 1은 승인된 고각도 지붕 구도·camera·보행·배경, image 2는 승인된 정면 얼굴 identity, image 3은 승인된 전면 complete outfit이다. prompt는 네 역할을 혼합하지 않고, image 1의 구도 보존·image 2의 청록 단발과 양쪽 호박색 눈·image 3의 흰 크롭 재킷/청록 와이드 바지/흰 운동화/남색 crossbody bag 및 재킷 바깥 strap만 짧게 계약했다.
- seed `62294`와 `62295`에서 모두 고각도 투영, 청록 턱선 단발, 양쪽 호박색 눈, 흰 크롭 재킷, 청록 바지, 흰 운동화, 남색 가방과 외부 strap을 함께 유지했다. 전신이 화면 안에서 축소·가려지는 고각도 pose에서도 팔·다리 수와 비율에는 눈에 띄는 붕괴가 없었다. **이 조합은 현재까지 8 GB에서 camera·face·style·outfit·body gate를 동시에 통과한 첫 고각도 1차 생성 체크포인트**다.
- 범위: 고정한 guide와 보행 pose의 두 seed만 검수한 결과다. `p7-5-11-qwen-edit-high-angle-*-reference.png`와 대응 review JSON은 P7-5.11 승인 실험 자산으로 승격했지만, 다른 guide·다른 동작·후면/가림·밀집 소품까지 일반화되었다고 보지 않는다. LoRA 학습 입력으로는 사용하지 않으며, 다음 검증은 guide 하나를 바꾸고 동일한 세 역할을 유지해 camera와 캐릭터 계약이 동시에 남는지 확인한다.
- 재현 기록: `docs/assets/part-07/chapter-05/p7-5-11-qwen-edit-high-angle-*-reference.png`, `p7-5-11-qwen-edit-high-angle-reference-review.json`, `.tmp/p7-5-11-qwen-edit-face-outfit-contract.log`, `.tmp/p7-5-11-qwen-edit-face-outfit-seed-62295.log`.

## 4. 현재 승인 경계와 다음 실험 규칙

| 단계 | 현재 판정 | 다음 단계 조건 |
|---|---|---|
| 얼굴 | 스타일 Plus Face 조건부 통과, FaceID 탈락 | 사람 확대 검수에서 단일 얼굴·identity 확인 |
| 재킷 | source-aligned mask 조건부 통과 | 소매·밑단·얼굴 보존 확인 |
| 바지 | source-aligned mask 조건부 통과 | 하이웨이스트·와이드 실루엣과 발목 길이 확인 |
| 가방 | 탈락 | 승인 가방·스트랩 방향을 포함한 새 국소 mask 설계 |
| 중립 전신 | 통과 후보 | 비율 기준 anchor로 고정 |
| OpenPose | 0.6 조건부 | 자세가 바뀌면서 얼굴·복장이 유지되는지 검수 |
| 3중 결합 | 탈락 | 실패한 가방 쌍을 제외하고 재검증 |

다음 실행은 같은 prompt·seed 반복이 아니라 실패한 계약만 바꾼다. 우선 기본 생성, 얼굴·복장 reference, LoRA, pose/camera 구조 제어를 독립적으로 검증하고, 이 경로들이 통과한 뒤에도 국소 결함이 남을 때만 Inpaint·VTON을 마지막 보정 단계로 검토한다. 승인 PNG·review JSON·guide를 사람이 확인하기 전에는 학습 데이터나 제작 입력으로 승격하지 않는다.

## 5. 재현 기록과 흡수된 중복 노트

- 이번 세션의 요약 JSON: `.tmp/p7-5-11-sequential-control-gate-report.json`
- 얼굴 비교 후보: `.tmp/p7-5-11-sdxl-safe-face-openpose-fullbody-probe/`
- source-aligned CatVTON 후보: `.tmp/p7-5-11-face-fixed-catvton-jacket-aligned/`, `.tmp/p7-5-11-face-fixed-catvton-pants/`, `.tmp/p7-5-11-face-fixed-catvton-outfit/`
- 쌍별·3중 결합 후보: `.tmp/p7-5-11-outfit-plus-proportion-*`, `.tmp/p7-5-11-triple-grid-*`
- `.tmp/`는 재현·검수용 임시 기록이며 커밋 대상이 아니다.
- 기존 `management/release-notes/sections/part-07/`의 P7-5.1~P7-5.4와 P7-5.8~P7-5.11 릴리즈노트는 Section별 이력으로 유지한다. 이 문서는 해당 릴리즈노트를 대체하지 않고, 이번 세션의 공통 실험 결론·중복 제거 기준·다음 gate만 요약한다.
- 아래 `authoring/` 공통 노트 8개는 고유 내용을 이 문서의 6절로 흡수한 뒤 삭제한다. 오픈 체크리스트와 Section 분석은 Part 전체 운영 문서이므로 유지한다.
  - `part-07-character-pack-generation-research-2026-08-03.md`
  - `part-07-controlnet-webtoon-pipeline-v1.md`
  - `part-07-identity-structure-research-2026-08-03.md`
  - `part-07-local-reference-replacement-preflight.md`
  - `part-07-turnaround-improvement-options-2026-08-04.md`
  - `part-07-webtoon-character-consistency-source-notes.md`
  - `part-07-webtoon-production-pipeline-research.md`
  - `part-07-three-experiment-feasibility.md`

## 6. 흡수한 공통 관리노트의 고유 내용

다음 8개 공통 관리노트는 P7-5 관련 내용과 Part 7 전체 파이프라인 제안이 섞여 있었다. 원문을 파일별로 유지하지 않고, 아래의 고유 판단만 이 통합노트에 흡수한다. 동일한 모델·seed·mask 반복은 앞 절의 대표 결과로 대체한다.

### 캐릭터팩·로컬 참조 대체

- 캐릭터팩은 단일 정면 이미지가 아니라 얼굴·전신·의상·소품·화풍을 같은 revision으로 승인한 원본 묶음이다. 다각도 모델과 character sheet, reference adapter와 pack 생성기를 동일시하지 않는다.
- 로컬 GPU 후보는 실행 가능성·각도 확장·LoRA feasibility의 세 gate를 순서대로 거친다. canonical 기준을 대체하려면 각 방향의 얼굴·전신·복장·소품과 held-out 검수가 모두 통과해야 한다.
- 로컬 후보는 기존 승인 기준을 자동 대체하지 않는다. 승인 전에는 draft로만 보존하고, 미통과 결과를 새 학습 입력으로 재사용하지 않는다.

### ControlNet 중심 파이프라인

- `identity`, `scene/shot`, `style`, `local repair`를 서로 다른 조건으로 기록한다. ControlNet은 누구인지가 아니라 어디에 어떻게 있는지를 전달한다.
- 최소 흐름은 승인 reference pack → shot contract → scene control pack → 구조 생성 → identity/style 결합 → 영역별 inpaint → 4컷 연속성 검수다.
- 한 컷에 주 구조 조건 하나를 먼저 적용하고, 보조 조건은 단독 gate를 통과한 뒤에만 추가한다. mask 밖의 승인 특징을 보존하지 못하면 다음 단계로 진행하지 않는다.

### Identity·structure 조사에서 남긴 경계

- Canny/OpenPose scale을 계속 올리는 것만으로 identity·소품 geometry를 동시에 고정할 수 없었다. 구조 조건은 silhouette·camera·pose 보조로만 판정한다.
- OpenPose/T2I-Adapter, Ctrl-X, attention injection, MimicMotion, VACE, StableAnimator, CharaConsist 등은 8 GB에서 실행·품질·접근 조건 중 하나 이상이 제작 gate를 충족하지 못해 보류했다.
- reference 수 증가나 adapter scale 반복은 새 가설이 아니다. 다음 실험은 입력 역할·마스크·해상도·모델 계열 중 하나를 바꿔야 한다.

### Turnaround 개선 기록

- 정면·좌우 측면·후면의 중립 전신은 기준으로 승인할 수 있지만, 3/4 회전과 동적 pose의 성공을 보장하지 않는다.
- 추상 blockout, 다중 전신 reference, FLUX 다중참조에서 얼굴·골반·다리 방향과 가방 strap이 분리되는 실패가 반복됐다. 밀집 구조 입력과 appearance 입력을 분리한다.
- ControlNet++·Zero123++는 현 8 GB 환경의 실행·품질 근거가 부족하고, FLUX multi-reference는 reference 수보다 역할 충돌을 먼저 검수해야 하므로 기본 경로로 채택하지 않는다.

### 캐릭터 일관성 참고자료의 역할표

- LoRA/DreamBooth: 누구인가를 학습하는 모델 보정.
- IP-Adapter/Face Adapter: 기준 이미지와 닮는 정도를 조절하는 참조 조건.
- ControlNet/T2I-Adapter: pose·선화·depth·구도를 전달하는 구조 조건.
- inpaint/img2img: 전체 frame gate 이후 실패 영역만 수정하는 국소 보정.
- ComfyUI workflow: 위 역할과 sampler·scheduler·scale·seed를 재현 가능한 순서로 기록하는 실행 지도.

### Part 7 제작 파이프라인의 공통 gate

- 최종 목표는 한 장의 미려한 출력이 아니라 여러 컷에서 같은 캐릭터로 읽히는 시퀀스다.
- 품질 gate는 `identity/face`, `style`, `pose·body`, `camera·scene`, `hands·props·feet`를 분리하고 4컷 contact sheet에서 함께 검수한다.
- pose-first, face-first, camera/background-first, object-first 중 컷 목적에 맞는 시작 원본을 선택한다. 생성 모델이 관절·가림·접지를 모두 보정할 것이라고 가정하지 않는다.
- 식자·세로 배치·말풍선 공간은 이미지 생성 품질과 별도 gate다.

### 8 GB 실험 순서의 통합 기준

1. 실행 환경과 checkpoint·dtype·offload를 확인한다.
2. 화풍·캐릭터 기준을 고정하고 held-out 입력을 분리한다.
3. 단일 구조 조건과 단일 identity 조건을 각각 실행한다.
4. 통과한 조건만 쌍별, 이후 3중 결합으로 확장한다.
5. OOM, VRAM, 시간, mask 경계, identity·style·pose 판정을 실행 JSON에 남긴다.

이 절차는 P7-5.1~5.6의 Section 릴리즈노트와 독립된 공통 운영 요약이다. `part-07-open-checklist.md`와 `part-07-section-analysis.md`는 Part 전체 체크포인트·분석 문서이므로 삭제하지 않는다.
