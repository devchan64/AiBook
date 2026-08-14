# Part 07 Chapter 05 P7-5 통합 관리노트

- 통합 범위: `P7-5.1`~`P7-5.6`
- 대응 본문: `docs/parts/part-07/chapter-05/section-01.md`~`section-06.md`
- 통합일: 2026-08-14
- 문서 성격: 원고 릴리즈 이력의 대체 관리노트. 독자용 본문이나 `mkdocs.yml`의 nav에 연결하지 않는다.

## 1. 통합 원칙

P7-5의 기록은 `화풍 기준 → 인물 기준 → 장면·구조 → 보정 → 다중참조 → 3D 구조 입력`의 순서로 읽는다. 같은 prompt의 단어 수, seed, step, CFG, mask border만 바꾼 반복은 개별 이력으로 남기지 않고 다음 세 가지로 압축한다.

1. 어떤 계약을 검증했는가.
2. 사람 검수에서 통과·조건부 통과·탈락한 기준은 무엇인가.
3. 반복을 중단하고 다음 가설로 넘어간 이유는 무엇인가.

후보 PNG·guide·review JSON은 승인 자산이 아니다. 사람 승인과 입력 계약이 함께 확인된 경우에만 다음 단계 입력으로 사용할 수 있다. 한 단계의 JSON 계약을 바꿔도 기존 PNG를 자동 재승인하지 않으며, 영향받은 방향은 다시 생성·검수한다.

## 2. Section별 현재 계약과 통합 결론

### P7-5.1 — 배경 화풍 기준

- 인물 없이 배경만 생성하고, 장소·시간·카메라를 장면 변수로 분리한다.
- 공통 화풍은 `docs/assets/part-07/chapter-05/p7-5-1-style-prompt-contract.json`으로 관리한다.
- 사람 승인한 로컬 GPU 배경 참조 셋과 `p7-5-1-approved-style-reference-pack.json`만 다음 단계 화풍 입력이다. 미승인 후보·타일·중간 시트는 입력으로 쓰지 않는다.
- 승인 표는 빈 열 없이 4열 중심으로 정리하며, 표의 장소 라벨은 이미지와 분리하지 않는다.
- P7-5.1 화풍 승인과 P7-5.2 인물 identity 승인은 서로 대체하지 않는다.

### P7-5.2 — 얼굴·전신·소품 기준

- 사람 승인 기준은 방향 얼굴, 정면 전신, 방향 전신, 리파인 전신, 소품 기준으로 분리한다.
- 공용 identity·비율 계약은 현재 `p7-5-2-face-identity-contract.json`과 `p7-5-2-fullbody-proportion-contract.json`의 통합 방향을 따른다. 눈 색·머리·비율 문장을 각 생성기의 prompt에 중복 확장하지 않는다.
- 전신 생성은 승인 정면 얼굴과 방향에 맞는 얼굴 시트를 참조하며, 방향·pose·camera 범위를 얼굴 승인 범위로 오인하지 않는다.
- 기본 seed는 `62294` 계열을 사용하되, seed 변경은 새 생성으로 취급한다. 기존 승인 PNG를 seed 변경만으로 자동 대체하지 않는다.
- 정면 전신 고해상도 기준은 `960×1440`, 전신 기본 생성은 1차 `3 step`, 2차 `6 step`을 기준으로 검수한다. 좌·우 측면의 2차 고스텝 실험은 질감 개선을 보장하지 않았으므로 별도 승인 없이는 기본값으로 일반화하지 않는다.
- 사람 승인한 18개 원본(얼굴 6, 기본 전신 6, 리파인 전신 6)은 P7-5.4 학습·증강의 기준 입력이다. 후보 review JSON은 승인 전 학습 입력이 아니다.
- 원고 표는 방향별 이미지를 반복 행으로 배치하며, `1열·2열·3열` 같은 구현 열 이름을 독자용 기준으로 노출하지 않는다.

### P7-5.3 — 장면·구조·guide

- 장면 계약과 캐릭터 계약을 분리한다. RGB는 색·질감·조명을, 상대 depth/Canny는 공간 윤곽·거리·가림의 보조 기준으로만 사용한다.
- 승인된 RGB/depth가 있어도 얼굴·복장·화풍·사지 비율을 자동 승인하지 않는다.
- 단일 guide와 방향에 가까운 전신 한 장을 먼저 검수하고, 다중 전신 참조·crop 합성·lineart-only 경로는 형태 붕괴·사각형 이음새·추가 사지 때문에 제작 경로에서 제외했다.
- Animagine 및 과거 lineart 경로는 현재 승인 체인에서 제외한다. 구조 guide는 사람 승인한 RGB에서 파생한다.
- P7-5.3은 최종 캐릭터 일관성 학습 단계가 아니라 pose·camera·장면의 독립 gate다.

### P7-5.4 — 화풍·연속성·LoRA·VTON 보정

- LoRA 학습 데이터는 P7-5.1 화풍 참조와 P7-5.2 인물 기준의 역할을 분리한다. 화풍 없는 전신과 화풍 포함 증강을 섞을 때는 학습 목표를 명시하고 별도 검수한다.
- 손·발·관절 수, 얼굴 identity, 복장, 화풍, 배경 유무를 한 번에 승인하지 않는다. 각 후보는 사람 검수 후에만 학습 세트에 넣는다.
- DiffEdit·수동 SDXL inpaint·일반 IP-Adapter의 반복 mask/CFG/strength sweep은 자동 mask 범위와 색·재질 전달 한계를 확인한 뒤 중단했다. mask가 얼굴·바지·신발까지 번지면 step 증가로 해결된다고 보지 않는다.
- CatVTON은 person·garment·mask를 분리하는 복장 후보 경로로 채택했다. source와 mask의 종횡비·좌표가 맞지 않으면 팔 바깥과 하체가 재킷으로 칠해진다.
- source-aligned mask 실험에서는 재킷과 바지가 조건부 통과 후보였고, 가방은 스트랩·실루엣 보존에 실패했다. 가방 포함 조합은 승인하지 않는다.
- LoRA는 얼굴·복장·신체 비율을 동시에 보장하는 만능 제어로 해석하지 않는다. 학습 실패는 데이터 역할, 해상도, caption, rank/alpha, 추론 조건을 분리해 재검증한다.

역사적으로 P7-5.4에서 확인한 대표 경계도 다음처럼 압축한다.

- P7-5.1 배경 20장과 P7-5.2 얼굴·전신 기준으로 화풍 포함 스포츠 후보를 36장까지 확장했지만, 손발 수·비율·화풍 불일치 후보가 반복 탈락했다. 승인 전 후보와 review JSON은 학습 입력이 아니다.
- Animagine XL 화풍 LoRA pilot·SDXL base style LoRA는 8 GB에서 실행·adapter 저장까지 가능했지만, held-out 장면의 화풍 이득과 구도 안정성을 제작 gate로 승인할 근거는 얻지 못했다. 화풍 LoRA를 얼굴·복장·pose 해결책으로 일반화하지 않는다.
- DiffEdit 자동 mask와 수동 SDXL inpaint의 10회 이상 반복은 얼굴·하체·신발로 번지는 mask 또는 회색 재킷을 만들었다. step·CFG·strength·seed만 반복하는 경로는 중단하고, 입력 mask·garment conditioning·모델 선택을 별도 가설로 분리했다.
- 일반 IP-Adapter와 흰 재킷 reference의 scale·padding·border sweep은 포켓·소매 끝만 전달하고 흰 몸판·open-front·긴 소매를 안정화하지 못했다. CatVTON으로 전환한 이유는 person·garment·mask 계약을 분리하기 위해서다.
- SD15 OpenPose와 SDXL Canny는 구조·silhouette 보조로는 부분 통과했지만, identity·화풍·가방 geometry를 보장하지 않았다. 구조 gate와 identity/style gate를 합치지 않는다.

### P7-5.5 — FLUX 다중참조 보충학습

- 참조 수를 늘리는 것이 아니라 `style`, `character_identity`, `pose_structure`, `scene_context`, `local_detail` 역할을 분리해 검수한다.
- 한 참조가 다른 계약을 덮어쓸 수 있으므로 다중참조는 P7-5.1~5.4 gate를 우회하지 않는다.
- 8 GB 환경에서는 참조를 하나씩 추가하는 ablation을 우선하며, 승인 전 후보를 후속 입력으로 재사용하지 않는다.

### P7-5.6 — 3D 선화·depth+선화 보충학습

- 선화는 윤곽·관절·화면 위치, depth는 상대 거리·앞뒤 가림을 전달한다.
- 둘 다 identity·화풍·세부 해부학을 보장하지 않으므로 P7-5.2 얼굴/전신 기준과 별도 검수한다.
- 구조 맵 생성 예제는 입력 의미를 설명하는 실습이며, 사람 승인 장면을 자동 생성하는 파이프라인으로 취급하지 않는다.

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

다음 실행은 같은 prompt·seed 반복이 아니라 실패한 계약만 바꾼다. 특히 가방 mask, source/mask 종횡비, img2img strength, OpenPose scale을 분리해 한 번에 하나만 변경한다. 승인 PNG·review JSON·guide를 사람이 확인하기 전에는 학습 데이터나 제작 입력으로 승격하지 않는다.

## 5. 재현 기록과 삭제된 중복 노트

- 이번 세션의 요약 JSON: `.tmp/p7-5-4-sequential-control-gate-report.json`
- 얼굴 비교 후보: `.tmp/p7-5-4-sdxl-safe-face-openpose-fullbody-probe/`
- source-aligned CatVTON 후보: `.tmp/p7-5-4-face-fixed-catvton-jacket-aligned/`, `.tmp/p7-5-4-face-fixed-catvton-pants/`, `.tmp/p7-5-4-face-fixed-catvton-outfit/`
- 쌍별·3중 결합 후보: `.tmp/p7-5-4-outfit-plus-proportion-*`, `.tmp/p7-5-4-triple-grid-*`
- `.tmp/`는 재현·검수용 임시 기록이며 커밋 대상이 아니다.
- 기존 `management/release-notes/sections/part-07/P7-5.1.md`~`P7-5.6.md`는 Section별 릴리즈 이력으로 유지한다. 이 문서는 해당 릴리즈노트를 대체하지 않고, 이번 세션의 공통 실험 결론·중복 제거 기준·다음 gate만 요약한다.
