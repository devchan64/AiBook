# Part 7: 전신 Turnaround 개선 방향

확인일: 2026-08-04

## 현재 결론

P7-5.2의 8 GB 실험에서 승인된 전신 기준은 정면, 좌측 측면, 정후면, 우측 측면의 네 방향이다. 좌측 측면은 Canny·OpenPose·depth 없이 정면 character master와 화풍 원본 두 장을 참조해 재생성한 뒤 사람 검수를 통과했다. 전면 3/4는 다음 실패를 반복했다.

- FLUX.2 multiple reference: 얼굴, 몸통, 골반, 다리가 같은 yaw를 유지하지 못했다.
- 승인 view를 추가한 interpolation: 좌측은 측면으로 수렴했고 우측은 시선, 다리 방향, 다리 수가 분리됐다.
- Ctrl-X에 추상 3D blockout을 structure로 넣은 preflight: 실행은 됐지만 인체와 identity가 무너졌다.

따라서 다음 단계는 reference 수나 prompt를 늘리는 일이 아니다. **사람 형태를 보존하는 밀집 구조 조건**과 **appearance/identity 조건**을 분리해 한 장씩 평가해야 한다. 승인된 네 방향 baseline은 중립 전신 참조이며, 3/4 회전이나 동적 컷의 성공 근거는 아니다.

## 후보 우선순위

| 우선순위 | 후보 | 기대하는 역할 | 현재 판단 |
| --- | --- | --- | --- |
| 제외 | ControlNet++ + human pose/depth/normal guide | head, torso, pelvis, legs, feet의 yaw와 가림을 함께 조건화 | 2026-08-04 local preflight에서 sequential offload는 custom transformer meta-device 오류, model offload는 7.53 GB GPU에서 UNet 적재 OOM으로 중단됐다. |
| 보류 | FLUX.2 multiple reference | 승인 character/style reference의 appearance와 line/wash 처리 전달 | 중립 view에서는 유효했지만, prompt/anchor만으로 3/4 yaw를 고정하지 못했다. 사람 형태 구조 조건을 함께 줄 수 있을 때 재검증한다. |
| 2 | Zero123++ | 30도와 90도 등 정해진 상대 camera view의 **기하 proposal** 만들기 | 공식 예제가 약 5 GB VRAM을 안내하지만 object-centric multi-view 모델이다. 웹툰 최종 작화나 공개 실습 모델로 채택하지 않는다. |
| 제외 | LAMIC + FLUX.1 Kontext dev | multi-reference layout composition | Kontext base와 local 8 GB execution/quality가 확인되지 않았다. |
| 제외 | ViewCrafter | camera trajectory를 따른 novel-view video | 공식 512 model도 13.8 GB A100 측정치이므로 현 8 GB 조건 밖이다. |

## ControlNet++ preflight 결과: 현재 8 GB 제외

### 구조 입력과 실행 범위

`Pose Depot`처럼 같은 인체 pose에서 OpenPose, depth, normal을 함께 제공하는 공개 pose guide를 사용한다. 입력은 새로 그린 추상 blockout이 아니라 실제 사람 체적과 가림을 가진 3D pose render여야 한다. 사용자 검수는 landmark 기준으로 하되, 모델 내부 조건에는 OpenPose를 포함할 수 있다.

- target: 정지 상태의 전면 좌/우 3/4, head-to-sole crop
- 구조 계약: 코끝, 목, 흉곽, 골반, 무릎, 발끝이 같은 좌/우 방향을 향한다.
- 접지 계약: 양 발은 하나씩만 존재하고 heel/toe depth가 구조 guide와 일치한다.
- appearance: 승인된 `front` PNG 한 장만 사용한다. 여러 identity reference를 동시에 넣지 않는다.

### 실행 결과

1. 공식 `xinsir/controlnet-union-sdxl-1.0` checkpoint, local SDXL base, Apache-2.0 Pose Depot의 OpenPose + depth 3/4 guide를 `/tmp`에서 준비했다.
2. `512 x 768`, batch 1, 12 step, identity/LoRA 없이 structure-only 호출을 시도했다.
3. `sequential CPU offload`는 custom ControlNet transformer 일부가 `meta` device에 남아 device mismatch로 중단됐다.
4. `model CPU offload`는 SDXL UNet 적재 중 20 MiB 추가 할당에서 OOM이 났다. GPU total은 7.53 GiB였고 PyTorch allocation은 6.69 GiB였다.

따라서 ControlNet++는 공식적으로 multi-condition을 지원하더라도, 이 checkout과 현재 8 GB GPU 조합에서는 구조 결과를 한 장도 만들지 못했다. identity adapter, LoRA, inpaint, scale sweep은 실행하지 않는다.

## FLUX.2 다중 참조의 보류 조건

FLUX.2 multiple reference는 `배제`가 아니라 `보류`다. 이미 승인된 중립 turnaround에서 머리색, 재킷, 바지, 수채화 질감의 전달 가능성을 보였기 때문이다. 다만 reference 수와 prompt만으로는 head/body/leg yaw 또는 다리 개수를 제약하지 못했다.

재개 조건은 다음과 같다.

1. 사람 체적과 가림을 가진 target 3/4 structure image가 준비돼야 한다.
2. 그 structure가 appearance reference와 별도로 입력될 수 있어야 한다.
3. structure-only 결과가 먼저 view yaw, 다리 수, 발 접지 gate를 통과해야 한다.
4. 그 뒤에만 FLUX.2 multiple reference를 appearance/style branch로 비교한다.

즉 FLUX.2는 character/style 유지 후보이며, 단독 turnaround 생성기로 채택하지 않는다.

## Zero123++의 한정된 역할

Zero123++는 single image에서 고정된 azimuth `30, 90, 150, 210, 270, 330` view를 생성하며, 공식 README의 기본 실행은 약 5 GB VRAM, depth ControlNet 실행은 약 5.7 GB VRAM을 안내한다. 따라서 30도와 90도 output은 turnaround의 camera proposal을 비교하는 probe로는 의미가 있다.

그러나 입력을 square로 정규화하고 fixed elevation/FOV로 output을 내며, 공식 목적도 3D generation이다. 사람의 얼굴, 의상, 웹툰 선화, 보이지 않는 등판을 최종 character pack 품질로 고정한다는 근거는 아니다. 또한 code는 Apache-2.0이지만 model weights는 CC-BY-NC 4.0이므로, 공개 책의 실습 산출물에 채택하지 않는다.

## 다음 결정

현재 8 GB에서 ControlNet++ preflight까지 실패했으므로, 이 조합의 재시도나 identity branch는 중단한다. FLUX.2 multiple reference는 구조 조건을 붙일 수 있는 호환 모델이 확보될 때까지 보류한다. 3/4 turnaround 자체는 16 GB 이상 환경의 reference-conditioned human model 또는 사람이 직접 수정한 기준 view로 분리한다.

## 출처와 이용 조건 확인

- [ControlNet++ 공식 저장소](https://github.com/xinsir6/ControlNetPlus){: target="_blank" rel="noopener noreferrer" }: OpenPose, depth, normal 등 복수 조건과 OpenPose + depth/normal 조합 예시를 안내한다. 확인일: 2026-08-04.
- [Pose Depot 공식 저장소](https://github.com/a-lgil/pose-depot){: target="_blank" rel="noopener noreferrer" }: pose별 depth, normal, canny, OpenPose guide와 Apache-2.0 repository license를 안내한다. 실제 선택 asset의 이용 범위는 실행 전에 다시 확인한다. 확인일: 2026-08-04.
- [Zero123++ 공식 저장소](https://github.com/SUDO-AI-3D/zero123plus){: target="_blank" rel="noopener noreferrer" }: fixed multi-view camera, 기본/깊이 ControlNet example의 VRAM 안내, code Apache-2.0 및 model weights CC-BY-NC 4.0을 확인했다. 확인일: 2026-08-04.
- [LAMIC 공식 저장소](https://github.com/Suchenl/LAMIC){: target="_blank" rel="noopener noreferrer" }: FLUX.1 Kontext dev 기반의 multi-image layout composition 구현임을 확인했다. 현재 장비의 실행 가능성은 미검증이다. 확인일: 2026-08-04.
- [ViewCrafter 공식 저장소](https://github.com/Drexubery/ViewCrafter){: target="_blank" rel="noopener noreferrer" }: 512 model의 공식 13.8 GB GPU memory 측정치를 확인했다. 확인일: 2026-08-04.

이 문서는 법률 자문이 아니다. checkpoint, guide asset, output의 이용 조건은 채택 직전에 다시 확인한다.
