# P7-5.1 캐릭터 참조 팩과 SD 1.5 LoRA로 기준 만들기

> Section ID: `P7-5.1`
> Version: `v2026.08.03`

웹툰 컷 생성에서는 pose보다 먼저 캐릭터 기준을 고정해야 합니다. 이 절은 새 캐릭터 `p7-mira`의 단일 이미지 참조 팩을 만들고, 학습 장면과 독립 평가 장면을 분리한 기록입니다. 이 팩은 LoRA 학습을 시작할 조건을 만족하지만, LoRA가 새 장면에서 같은 인물이나 화풍을 유지한다는 품질 증거는 아닙니다. 그 판단은 학습 뒤 held-out 비교에서 따로 합니다.

## 기준 캐릭터와 학습 분할

새 기준 자산은 한 장의 전신 이미지로 만듭니다. `p7-mira/single-01`은 청록 단발, silver hair clip, 흰 재킷, 청록 바지, 흰 운동화, 남색 가방을 기준 특징으로 정의합니다. 전신·신발과 가방의 본체·flap·단일 대각 스트랩·오른쪽 hip 위치가 한 화면에 보여야 합니다.

![p7-mira single reference candidate](../../../assets/part-07/chapter-05/p7-5-1-mira-single-reference-01.png)

| 자산군 | 확보한 구성 | 역할 |
| --- | --- | --- |
| 기준·표정·전신 이미지 | 전신 단일 PNG 19장, detail PNG 2장 | 얼굴·의상·전신·손·가방 기준 |
| train scene | 장소·동작·camera가 다른 단일 장면 PNG 16장 | 캐릭터와 장면 렌더링 학습 |
| held-out scene | train과 장소·camera·source가 겹치지 않는 단일 PNG 4장 | 학습 뒤에만 쓰는 일반화 평가 |

시트 이미지는 사람의 비교 기준으로도 쓰지 않고, 학습 입력으로도 쓰지 않습니다. 한 파일에는 한 명의 전신 캐릭터와 하나의 view만 넣습니다. 19장 기준에는 정면·좌우 3/4·측면·후면, 표정과 손 제스처, 보행·체중 이동·후면 회전이 포함됩니다. detail은 전신 비례를 대신하지 않고 얼굴·눈·머리카락 및 손·가방 결합을 보완합니다. held-out은 학습 folder에 넣지 않습니다. 같은 캐릭터를 써도 학습에 없는 camera와 장소를 남겨야 LoRA가 기준 이미지를 외운 것과 새로운 장면에 적용한 것을 구분할 수 있습니다.

## LoRA가 새 장면에서도 같은 인물인가

가설은 `p7mira` LoRA를 켠 출력이 끈 baseline보다 held-out 네 장면에서 얼굴, 머리, 의상, 신발, 화풍을 더 잘 유지한다는 것입니다. base 모델, prompt의 장면 설명, seed, camera는 고정하고 LoRA off/on만 바꿉니다.

| 단계 | 고정값 | 비교값 | 남길 결과 |
| --- | --- | --- | --- |
| 자산 등록 | 단일 이미지 revision, source ID | train / held-out | manifest와 단일 PNG |
| 학습 | SD 1.5, `384 x 512`, batch 1 | LoRA revision | 학습 설정과 가중치 |
| 평가 | scene, camera, seed | LoRA off / on | panel별 PNG 두 장 |
| 판정 | 얼굴·머리·의상·신발·화풍 | pass / fail | 4 x 2 contact sheet |

학습 loss가 낮거나 PNG가 생성됐다는 사실만으로 통과시키지 않습니다. 네 장면에서 다섯 항목이 모두 유지될 때만 다음 실험으로 진행할 수 있습니다.

## 단일 자산을 검사하고 실행을 막는 코드

네 Python 스크립트는 서로 다른 역할을 맡습니다. 이들은 그림을 자동으로 승인하거나 3D 추정값을 절대 신체 치수로 바꾸지 않습니다.

| 도구 | 하는 일 | 확인할 경계 |
| --- | --- | --- |
| Reference asset inspector | 단일 PNG의 세로 framing과 최소 해상도만 검사 | 이미지를 자르거나 분할하거나 다시 저장하지 않으며, 가방·얼굴 품질은 사람 검수 대상 |
| Pose landmark reporter | 2D landmark와 world landmark, 인물 실루엣 상단·하단을 JSON으로 기록 | 스켈레톤 이미지를 만들지 않으며, 머리 위·턱은 기록용 좌표 |
| Proportion comparator | 기준과 후보의 실루엣/어깨·몸통/다리 비율 차이를 계산 | world landmark는 합격 기준이 아니라 camera 방향 보조값 |
| Experiment checker | 필수 view, 최소 16개 train, source ID 중복을 검사 | `PASS`는 학습 시작 조건일 뿐 품질 통과가 아님 |

한 장의 이미지에서 얻는 3D world landmark는 절대적인 신체 치수가 아닙니다. 따라서 비례 합격은 흰 배경에서 자동으로 찾은 인물 실루엣 상단·하단과 어깨·골반·발 landmark의 2D 비율만 사용합니다. `single-01`의 기준값은 실루엣/어깨 비율 약 `5.263`, 몸통/다리 비율 `0.555`입니다. 중립 정면 계열은 두 값이 각각 4%를 넘게 달라지면 제외합니다. 팔·다리의 투영이 달라지는 동작은 전신 framing, 관절·가방 접촉의 사람 검수와 15% 이내의 2D 변화로 판정합니다. 측면·후면은 정면의 어깨 폭과 골반-발 투영을 비교할 수 없으므로 landmark 가시성과 사람 검수로 판정합니다. 머리 위·턱 좌표는 기록하되 수기 오차가 커 합격 기준에는 쓰지 않습니다. 3D 좌표는 어깨와 골반의 앞뒤 깊이 차이만 기록해 camera 회전과 좌우 비대칭을 검토합니다.

실습에는 `pip install mediapipe`와 공식 Pose Landmarker Full task model이 필요합니다. task model은 `.tmp/`에서만 읽고 저장소에는 넣지 않습니다. reporter의 출력은 landmark JSON뿐이며, 이미지 위에 점·선·스켈레톤을 렌더하지 않습니다.

## 학습 시작 조건을 채운 참조 팩

이 팩은 단일 character reference 19장, train scene 16장, 독립 held-out 4장을 갖췄습니다. 16개 train source ID와 4개 held-out source ID는 겹치지 않으며, 필수 view인 front, three-quarter left, three-quarter right, side, back도 각각 검수했습니다. manifest와 checker는 이 구조를 확인해 `PASS ready for training`을 반환합니다.

이 통과는 **학습 입력의 준비 상태**를 뜻합니다. 각 이미지는 얼굴, 청록 단발·clip, 재킷·바지·신발, **가로형 네이비 crossbody 가방의 단일 대각 스트랩·flap·오른쪽 hip 위치**, camera와 clean-line-art 장면을 사람 검수했습니다. 가방 구조가 틀린 기존 sheet 후보는 분할하거나 재사용하지 않았습니다. 다음 실행에서는 하나의 adapter가 identity와 scene rendering을 함께 학습하며, Mira LoRA와 style LoRA를 다시 합성하지 않습니다.

## GPU 앵커 실행은 품질 판정이 아니다

새 SD 1.5 base에서 UNet의 `to_q`, `to_k`, `to_v`, `to_out.0`만 rank 8 LoRA로 열고, 16개 train scene을 순환해 `384 x 512`, batch 1로 100 step 실행했습니다. 입력은 crop 없이 종횡비를 보존해 축소하고 흰 여백만 넣습니다. RTX 5070 Laptop GPU 8 GB에서 BF16 실행은 손실 `0.2029 -> 0.1741`, peak VRAM 약 `2,351 MiB`로 100 step을 마쳤습니다.

처음에는 같은 profile을 FP16 AdamW로 실행했지만 마지막 손실이 비유한 값이 되어 실패로 판정했습니다. 따라서 이 profile은 BF16을 사용하며, 실행 스크립트도 비유한 loss 또는 gradient가 생기면 성공 보고서를 만들지 않습니다. 이 수치는 학습 반복과 메모리 경계만 검증합니다. 이번 실행은 어댑터를 보존하지 않았고 held-out PNG도 생성하지 않았으므로 얼굴, 가방, pose, camera, clean-line-art 화풍의 품질 통과 근거가 아닙니다.

새 BF16 adapter를 저장해 네 held-out 장면에서 scene·camera·prompt·seed를 고정하고 LoRA off/on을 비교했습니다. 처음에는 원본 caption이 CLIP의 77-token 한도를 넘어 scene과 camera 뒤쪽이 잘려, 그 결과를 품질 근거에서 제외했습니다. 평가기는 이를 생성 전에 막도록 고쳤고, 압축한 네 prompt로 다시 만들었습니다.

두 번째 비교도 **품질 미통과**입니다. LoRA on은 일부 컷을 청록·흰 의상 쪽으로 바꾸었지만, 네 컷 모두에서 승인된 얼굴, 청록 단발·clip, 가로형 네이비 flap 가방과 하나의 대각 스트랩, 전신 framing, 요청한 장소·camera, 절제된 clean-line-art를 함께 유지하지 못했습니다. 따라서 이 100-step adapter와 생성 PNG는 보존 자산으로 남기지 않습니다. 다음 run은 이 checkpoint의 step을 늘리는 일이 아니라 SD 1.5 base의 표현 사전과 data-to-prompt 결속을 먼저 진단하는 별도 gate여야 합니다.

## Base 모델을 먼저 분리해 본 결과

LoRA 없이 같은 짧은 prompt, negative prompt, seed, 해상도, 25 inference step으로 일반 SD 1.5와 WD 1.5를 비교했습니다. 네 prompt는 모두 CLIP 77-token 한도 안인지 코드로 검사했습니다. 아래는 그 비교 결과이며, 이 그림은 Mira의 품질 통과 근거가 아니라 다음 실험의 base 후보를 좁히기 위한 진단입니다.

![SD 1.5와 WD 1.5 prompt-only base probe](../../../assets/part-07/chapter-05/p7-5-1-prompt-only-base-probe-contact-sheet.png)

일반 SD 1.5는 얼굴·인체·화풍이 네 컷에서 크게 달라졌습니다. WD 1.5는 청록 단발, 흰 재킷, 청록 바지, 전신 일러스트를 더 자주 만들었고 peak VRAM도 약 `2,927 MiB`로 8 GB 안에 들었습니다. 그러나 네이비 flap 가방, 손 동작, 장소와 camera, 절제된 clean-line-art는 안정적이지 않았습니다. 그러므로 둘 다 prompt-only 웹툰 컷 생성기로 채택하지 않습니다. WD 1.5는 다음의 **참조 제어 기반 identity·소품 결속 실험 후보**일 뿐이며, 이 결과만으로 LoRA 재학습을 시작하지 않습니다.

## 참조 이미지를 직접 넣으면 무엇이 고정되는가

SD 1.5용 IP-Adapter 가중치는 현재 캐시에 없고, 있는 IP-Adapter는 SDXL 전용입니다. 추가 다운로드로 조건을 바꾸지 않고, WD 1.5 img2img에 승인된 `single-01` 전신 이미지를 초기 입력으로 넣었습니다. 네 held-out prompt와 seed는 고정하고 초기 이미지 영향인 `strength`만 `0.25`, `0.55`, `0.80`으로 바꿨습니다.

![WD 1.5 reference img2img strength 0.25](../../../assets/part-07/chapter-05/p7-5-1-wd15-reference-img2img-strength-025-contact-sheet.png)

![WD 1.5 reference img2img strength 0.80](../../../assets/part-07/chapter-05/p7-5-1-wd15-reference-img2img-strength-080-contact-sheet.png)

`0.25`에서는 얼굴, 전신, 의상, 가방이 비교적 남지만 네 결과가 모두 흰 배경의 비슷한 서 있는 전신 구도에 머뭅니다. `0.55`도 요청 장면·camera·동작을 만들지 못하고 세부가 흐트러졌습니다. `0.80`은 팔·몸통과 난간 일부를 바꾸지만 요청한 주방, 페리, 영화관, 도예 작업실의 camera와 동작에는 도달하지 못하며 얼굴·머리·재킷·가방도 더 이탈합니다. 따라서 단일 참조 img2img는 **가까운 전신 기준을 보존하는 도구**일 뿐, pose·projection·camera·배경을 독립적으로 바꾸는 웹툰 컷 생성기에는 채택하지 않습니다.

## 실행 자산과 원문 { #execution-assets }

아래 항목을 펼치면 원문을 비동기로 한 번만 불러옵니다. 본문을 읽는 동안에는 긴 생성 지시문과 코드가 내려받아지지 않습니다.

| 구분 | 확인할 항목 |
| --- | --- |
| 생성 기록 | [Mira image_gen 기록](#mira-generation-record) |
| 기준 이미지 | [single-01 전신 후보](../../../assets/part-07/chapter-05/p7-5-1-mira-single-reference-01.png) |
| landmark 기준값 | [single-01 landmark report](../../../assets/part-07/chapter-05/p7-5-1-mira-single-reference-01-landmarks.json) |
| 정면·동작 기준 예시 | [single-05 정면](../../../assets/part-07/chapter-05/p7-5-1-mira-single-reference-05-front.png), [single-13 인사](../../../assets/part-07/chapter-05/p7-5-1-mira-single-reference-13-wave.png), [single-18 열린 손](../../../assets/part-07/chapter-05/p7-5-1-mira-single-reference-18-invite-palm.png) |
| 독립 평가 장면 예시 | [주방 측면](../../../assets/part-07/chapter-05/p7-5-1-mira-heldout-01-kitchen-cupboard.png), [페리 덱](../../../assets/part-07/chapter-05/p7-5-1-mira-heldout-02-ferry-deck.png), [영화관](../../../assets/part-07/chapter-05/p7-5-1-mira-heldout-03-cinema-ticket.png), [도예 작업실](../../../assets/part-07/chapter-05/p7-5-1-mira-heldout-04-ceramics-cup.png) |
| 보존 범위 | 생성 기록, manifest, inspector, checker, 릴리즈노트 |
| landmark 분석 코드 | [reporter](#pose-landmark-reporter), [proportion comparator](#landmark-proportion-comparator) |
| dataset 준비 코드 | [materializer](#mira-dataset-materializer) |
| GPU 실행 코드 | [UNet LoRA preflight and anchor profile](#mira-scene-lora-preflight) |
| held-out 비교 코드 | [fixed-prompt LoRA evaluator](#mira-scene-lora-evaluator) |
| base 비교 코드 | [prompt-only base probe](#prompt-only-base-probe) |
| 참조 img2img 코드 | [WD 1.5 reference img2img probe](#wd15-reference-img2img-probe) |
| 실험 계약 | [manifest](#experiment-manifest) |
| 현재 실행 도구 | [Mira splitter](#reference-pack-splitter), [checker](#experiment-checker) |

<details id="mira-generation-record" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7-5-1-mira-generation-record.md" data-language="markdown">
<summary>Mira 생성 기록 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 생성 기록을 불러옵니다.</div>
</details>

<details id="experiment-manifest" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7-5-1-character-lora-experiment.json" data-language="json">
<summary>실험 manifest 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 manifest를 불러옵니다.</div>
</details>

<details id="reference-pack-splitter" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_reference_pack_split.py" data-language="python">
<summary>Reference asset inspector 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="pose-landmark-reporter" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_pose_landmark_report.py" data-language="python">
<summary>Pose landmark reporter 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="landmark-proportion-comparator" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_landmark_proportion_compare.py" data-language="python">
<summary>Landmark proportion comparator 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="mira-dataset-materializer" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_prepare_mira_lora_dataset.py" data-language="python">
<summary>Mira LoRA dataset materializer 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="mira-scene-lora-preflight" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_mira_scene_lora_preflight.py" data-language="python">
<summary>Mira scene LoRA preflight와 anchor profile 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="mira-scene-lora-evaluator" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_evaluate_mira_scene_lora.py" data-language="python">
<summary>Mira held-out LoRA off/on evaluator 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="prompt-only-base-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_prompt_only_base_probe.py" data-language="python">
<summary>Prompt-only base probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="wd15-reference-img2img-probe" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_wd15_reference_img2img_probe.py" data-language="python">
<summary>WD 1.5 reference img2img probe 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

<details id="experiment-checker" class="aibook-lazy-source" data-source="../../../../assets/part-07/chapter-05/p7_5_1_character_lora_experiment_check.py" data-language="python">
<summary>Experiment checker 전문 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 등록 | 전신 기준 19장, train 16장, held-out 4장이 모두 manifest와 실제 파일에 있는가? |
| 분리 | held-out 원본이 train source ID·장소·camera와 겹치지 않는가? |
| 비례 | 중립 정면 계열은 4%, 동작은 15% 기준을 적용하고, 측면·후면은 사람 검수로 구분했는가? |
| 비교 | 같은 scene·camera·seed에서 LoRA off/on을 만들었는가? |
| 품질 | 얼굴, 머리, 의상, 신발, 화풍을 각각 판정했는가? |
| 다음 단계 | LoRA 품질 통과 전에는 StoryDiffusion 또는 ControlNet 품질을 주장하지 않았는가? |

## 출처와 참고 자료

- Hugging Face, [Diffusers LoRA training](https://huggingface.co/docs/diffusers/main/training/lora){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
- kohya-ss, [sd-scripts](https://github.com/kohya-ss/sd-scripts){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
- Google AI Edge, [MediaPipe Pose Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/python){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-02.
