# Part 7: 로컬 기준 참조 대체 사전 검증

확인일: 2026-08-03

## 질문과 현재 판정

질문은 Codex `image_gen.imagegen`으로 만든 Mira 기준 참조를 8 GB 로컬 GPU의 공개 모델 출력으로 대체해도 되는가이다. 현재 답은 **아직 대체하지 않는다**다. 로컬 Diffusers FLUX.2 Klein 4B는 다른 pose·camera·장소의 whole-shot을 만들었지만, 후면에서는 double bag과 crossing strap 결함이 남았다. 따라서 실행 가능성과 일부 컷 품질은 확인됐지만, canonical character reference의 일관된 품질은 아직 증명되지 않았다.

이 문서는 Codex 생성물을 학습 정답이나 로컬 출력의 화풍 정답으로 쓰지 않는다. 대체 실험 동안 기존 `single-01`은 provenance와 전신·소품 품질 gate의 비교 기준으로만 보존하고, 로컬 후보는 모두 `draft`로 시작한다. 로컬 pack은 기존 Mira와 다른 선·palette·명암 규칙을 가질 수 있으며, 그 자체의 승인된 style contract 안에서 일관되면 된다.

## 후보와 역할

| 단계 | 후보 | 역할 | 현재 상태 |
| --- | --- | --- | --- |
| A | `black-forest-labs/FLUX.2-klein-base-4B` | 로컬 text-to-image와 향후 character/style LoRA의 base | 미실행 |
| B | `black-forest-labs/FLUX.2-klein-4B` | 승인된 로컬 master reference를 입력으로 하는 reference-conditioned view 확장 | whole-shot 실행 성립, canonical 대체 미승인 |
| C | 기존 Codex `single-01` | 비교 기준과 provenance가 있는 기존 기준 이미지 | 유지 |

4B Base는 distilled 4-step 생산 모델이 아니라 fine-tuning과 최대 유연성을 위한 base로 공개됐다. 따라서 A의 품질 결과를 B와 같은 sampling 설정으로 해석하지 않는다. 모델별 출력, seed, 해상도, step, VRAM, 사람 검수표를 분리한다.

## 단계 A: 로컬 master 선택 gate

목적은 local-only text-to-image가 canonical reference 후보 한 장을 만들 수 있는지 확인하는 것이다. Codex reference를 입력으로 넣지 않는다.

1. 공개 4B Base를 `768 x 1152`, batch 1, CPU/sequential offload로 한 장씩 실행한다.
2. 같은 character contract로 서로 다른 seed의 **서로 다른 인물 후보**를 만든다. 이 후보들은 얼굴형·피부색이 같아야 하는 비교군이 아니며, prompt는 Mira의 이름이나 기존 파일명을 쓰지 않고 관찰 가능한 외형만 쓴다.
3. 사람 검수에서 전신·양쪽 신발, 청록 bob·silver clip, 흰 재킷, 청록 바지, 정확히 하나의 가로형 navy flap bag, 정확히 하나의 대각 strap, 그리고 후보 내부에서 명확히 읽히는 선·palette·명암 규칙을 모두 통과한 **한 장**을 local master로 선택한다.
4. 선택된 한 장의 얼굴형, 피부색, 눈·앞머리, 선·palette·명암은 이후 pack의 identity/style contract가 된다. 선택 전 후보끼리 얼굴이나 피부색이 다른 것은 실패가 아니라 후보 선택의 전제다.

이 단계의 성공은 좋은 정면/3-4분신 한 장을 얻었다는 뜻뿐이다. character reference pack, LoRA, 웹툰 컷 파이프라인의 성공을 의미하지 않는다.

## 단계 B: 로컬 master의 다각도 확장 gate

단계 A에서 사람 검수로 고른 local master 하나만 입력으로 사용한다. FLUX.2 Klein 4B direct reference conditioning으로 정면, 좌·우 3/4, 측면, 후면 3/4, 보행을 각각 한 장씩 만든다.

| 검수 축 | 합격 조건 |
| --- | --- |
| identity | bob 실루엣, clip 위치, 얼굴형, 재킷·바지·신발의 색과 구조가 master와 맞음 |
| prop | 매 컷에서 가방 본체 하나, flap 하나, strap 하나, 오른쪽 hip 위치가 보임 |
| proportion | 전신과 양쪽 신발이 frame 안에 있고, 중립 view는 기존 비례 gate를 통과함 |
| style | local master에서 승인한 선 굵기, palette, 명암, 질감 규칙을 모든 view에서 유지함 |
| camera | 각 view의 요구 방향이 실제로 보이며, 단순 정면 서기 반복이 아님 |

다섯 컷 중 하나라도 prop 또는 style 조건을 잃으면 pack은 `draft`다. 후면에서의 double bag/crossing strap은 즉시 불합격이며 inpaint로 수습하지 않는다. local master는 다섯 컷 모두 통과할 때만 새 canonical 후보가 된다.

## 단계 C: LoRA 학습 feasibility gate

단계 B의 pack이 통과하기 전에는 학습하지 않는다. 통과한 뒤에만 4B Base LoRA의 실행 가능성을 별도 측정한다.

1. train/held-out source를 분리하고 전체 frame을 유지한다. crop, mirror 복제, 같은 장면의 미세 변형은 데이터 수로 세지 않는다.
2. `512 x 768`, batch 1, BF16, gradient checkpointing과 CPU offload에서 1-step forward/backward를 먼저 확인한다.
3. finite loss, trainable parameter 수, peak VRAM, wall time을 기록한다. 8 GB에서 실행됐다는 사실만으로 품질 통과를 주장하지 않는다.
4. held-out의 side/rear, low-angle, hand-object 장면에서 identity·style·prop·camera를 분리 채점한다.

LoRA 이후에도 후면 prop이나 style이 무너지면 Canonical 교체는 중단한다. 현행 Codex 기준을 유지하거나, 공개 라이선스의 사람이 만든 원본 일러스트를 별도 기준 자산으로 확보하는 경로를 검토한다.

## 보존과 공개 원칙

- 통과 PNG, prompt, seed, 모델 source, 모델 및 변환물의 라이선스 확인, 실행 스크립트, 사람 검수 JSON만 보존한다.
- 실패 PNG, checkpoint, 임시 cache는 제거하고 실패 원인·VRAM·검수 결론만 남긴다.
- 실행 runtime의 라이선스와 model/weight/adapter의 라이선스를 분리 기록한다.
- 로컬 대체 결과가 나와도 Codex API가 만든 기존 reference의 저작권 상태나 이용 조건을 소급해 바꾸지 않는다.

## Section 분리 승인 조건

현재 P7-5.1은 reference pack, LoRA, whole-shot 검증을 함께 기록한다. 로컬 reference generation을 별도 Section으로 분리하는 것은 다음 조건을 모두 충족한 뒤에만 검토한다.

1. 단계 A에서 사람 검수로 선택한 local master 한 장이 identity/style contract를 명시한다.
2. 단계 B의 정면·3/4·측면·후면 3/4·보행이 그 master의 얼굴형·피부색·헤어, style, 가방 본체·flap·단일 strap을 모두 통과한다.
3. Codex `image_gen` 기준과 같은 전신·소품·해부학 검수 강도를 적용하되, local-only pack에는 자체 승인 style contract를 적용한다. 기존 화풍의 복제는 요구하지 않는다.
4. 모델 source, runtime, prompt, seed, 라이선스 확인, 실패 자산 제외 규칙을 독자가 재현할 수 있게 공개한다.

이 조건을 만족하면 새 Section은 `로컬 GPU로 character reference pack 만들기`를 중심 질문으로 삼는다. P7-5.1에는 그 Section에서 승인한 pack을 LoRA/whole-shot 입력으로 사용하는 경계만 남긴다. 어느 하나라도 미통과면 이 실험은 P7-5.1의 비교 기록으로만 유지하며 목차를 늘리지 않는다.

## 중단된 seed 반복 실험 기록

4B Base의 `768 x 1152`, 50-step local-only preflight는 seed `410001`에서 `469.1초`, peak `2,375MiB`로 PNG 저장까지는 통과했다. 이어 seed `410002`부터 12장을 같은 인물의 반복성 비교로 생성하려 했으나, 첫 두 후보의 얼굴형·눈·턱 비율과 피부색이 달랐다. 이는 text-to-image seed가 독립 인물 후보라는 점을 무시한 설계 결함이다. batch는 1장 생성 뒤 중단했고 PNG와 임시 실행 기록은 제거했다. 이 실패는 local master 후보의 품질 실패가 아니라, 동일 인물성 검증 방법의 실패로 기록한다.

## 단계 A 실행 결과: local master 선택

`FLUX.2-klein-base-4B`에서 `768 x 1152`, 50 step, guidance 4.0, sequential CPU offload로 seed `410021`부터 `410024`까지 독립 후보 네 장을 생성했다. 한 장당 약 `149.7~149.9초`, 관측 peak VRAM은 `1,937~2,895MiB`였다. 이들은 동일 인물 반복 검증이 아니라 서로 다른 후보였고, 그중 `410023`을 사람이 수기 선택했다.

선택 이유는 전신·양쪽 신발, 읽을 수 있는 손, 청록 bob과 silver clip, 흰 재킷·청록 바지, 오른쪽 hip의 가로형 navy flap bag과 단일 strap, 그리고 선·palette·명암 규칙이 한 이미지 안에서 가장 명확했기 때문이다. 이 이미지의 얼굴형·피부색·눈·앞머리와 화풍을 이후 local pack의 임시 identity/style contract로 삼았다. 아직 저장소의 canonical reference로 복사하지 않는다.

## 단계 B 실행 결과: direct reference conditioning 불합격

선택한 master를 입력으로 `FLUX.2-klein-4B` direct reference conditioning에서 정면, 좌 3/4, 우 측면, 후면 3/4, 보행으로 한 장씩 생성했다. `768 x 1152`, 4 step, guidance 1.0, sequential CPU offload를 사용했다. 얼굴형·피부색·hair·의상·line/palette는 다섯 장에서 비교적 유지됐다. 후면 3/4는 실제 방향 전환을 보였고 보행도 한 발을 옮긴 동작을 보였다.

그러나 좌 3/4는 정면과 거의 같은 구도이며, 우 측면도 측면 profile이 아닌 정면에 가까운 결과였다. 후면 3/4의 가방은 오른쪽 hip 대신 등에 올라가 contract를 잃었다. 따라서 camera와 prop gate가 동시에 실패했다. 이 결과는 `한 장 reference가 얼굴·피부색·화풍을 잡는 데에는 유효하지만, 요구한 camera를 강제하지 못한다`는 한계만 남기고, 생성 PNG와 임시 실행 산출물은 보존하지 않는다.

## 다음 실행

다음 단계는 reference-conditioned 4-step의 camera 고정력을 높이는 별도 방법을 비교하는 것이다. 후보는 (1) 방향별 reference를 먼저 확보해 다음 view의 입력으로 쓰는 chained view expansion, (2) camera/turnaround 제어를 별도 condition으로 주는 모델 또는 adapter, (3) camera 요구를 만족하는 whole-shot을 먼저 생성하고 master reference로 identity/style을 복원하는 two-pass 방식이다. 어느 방법도 정면 반복, double bag, crossed strap, rear bag 위치 변경을 통과로 처리하지 않는다.

## 후속 실행: mirror-safe local character/style anchor pack

앞선 실패는 hair clip과 가방처럼 비대칭인 정보를 한 장 master에서 반대쪽으로 추론시키려 했기 때문이다. `FLUX.2-klein-base-4B`로 대칭 deep-teal bob, 대칭 jacket, 무가방·무소품의 local-only master를 새로 만들고, 한쪽 3/4·strict profile·rear 3/4만 direct reference conditioning으로 생성했다. 반대쪽은 새 AI 출력을 재선택하지 않고, 대칭 contract를 만족하는 source를 deterministic horizontal mirror로 변환했다.

`768 x 1152`, 50 step, guidance `4.0`, seed `410201` master는 `152.5`초, peak `2,894 MiB`에서 통과했다. direct reference 4-step은 strict profile과 rear 3/4를 실제 방향으로 만들었고, thin charcoal line·low-saturation teal/white/charcoal palette·subtle fold shadow도 유지했다. 결과 [contact sheet](../../docs/assets/part-07/chapter-05/p7-5-1-local-character-style-pack-v1-contact-sheet.png)는 front, 좌·우 3/4, 좌·우 profile, 좌·우 rear 3/4를 제공한다. [manifest](../../docs/assets/part-07/chapter-05/p7-5-1-local-character-style-pack-v1.json)는 generated/mirrored view와 사용한 model·seed·계약을 분리 기록한다.

판정은 `approved_limited_scope`다. 즉 이것은 8 GB에서 재현 가능한 **중립 전신 character/style anchor pack**이며, 비대칭 액세서리·가방·strap·손-소품 접점·dynamic pose·배경·face close-up의 정답은 아니다. direct single-reference와 multi-reference로 right 3/4를 독립 생성한 출력은 정면으로 수렴하거나 얼굴·앞머리가 drift해 미통과였고 PNG는 보존하지 않는다. 이 제한을 숨기지 않는 것이 local pack을 다음 LoRA나 scene generation의 학습 정답으로 과대사용하지 않는 조건이다.

## 후속 실행: style pack과 character pack의 분리

후속 실험에서는 인물이 없는 station·library·rainy residential lane 세 장을 local style pack으로 먼저 승인하고, station master를 입력으로 새 style-conditioned character master를 만들었다. character pack은 정면, 좌·우 strict profile, 좌·우 rear three-quarter만 보존한다. 3/4 front 요구는 정면 또는 profile로 수렴했으므로 제외했다. 이 조합은 style·identity contract를 한 기준 이미지에 과적재하지 않는 방법의 실행 가능성을 보여주지만, canonical reference의 대체 근거는 아니다.

같은 우천 주거 골목 full-body walk에서 character-only와 style-plus-character conditioning을 비교했을 때, 두 출력 모두 전신·보행·의상·장소는 유지했다. 그러나 style reference를 추가해도 배경의 flatness가 뚜렷하게 개선되지는 않았다. whole-cut을 다시 style correction한 출력은 골목을 실내 계단으로 바꿔 scene continuity에서 탈락했다. 따라서 현재 결론은 **style pack -> character pack -> whole-cut 사람 검수 -> 제한 마스크 보정의 별도 gate**이며, 전체 컷 재생성을 자동 보정으로 쓰지 않는다는 것이다.

## 화풍 팩 분리와 v2 폐기

v1 station 중심 flat-color pack은 구도·원근·실내외·시간대의 폭이 좁았다. 이후 수채화 v2는 contour/structure line과 투명 색층을 분리하려 했지만, 일부 base 원본이 outer frame을 생성해 crop이 필요했고 표본도 수직 중앙 소실점 계열로 수렴했다. 이 둘은 character reference 입력으로 승인하지 않는다.

화풍 생성·검수는 `P7-5.0`으로 분리했다. 이 Section은 frame-free 원본, line-preserving watercolor, 실내/실외·시간대·camera family 행렬을 통과 조건으로 사용한다. v2 PNG와 crop builder는 제거하고, 실패 원인과 다음 입력 행렬은 `p7-5-0-local-style-pack-review.json`에 남긴다.
