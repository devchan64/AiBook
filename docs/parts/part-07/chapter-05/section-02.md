# P7-5.2 캐릭터 착장·전신 참조 셋: 입력 역할을 나누기

> Section ID: `P7-5.2`
> Version: `v2026.08.26`

같은 캐릭터를 다른 장면과 자세에서도 이어 그리려면, 얼굴·착장·전신 구조를 한 이미지나 한 프롬프트에 모두 맡기지 않아야 한다. 이 절에서는 로컬 GPU의 Qwen으로 만든 캐릭터 입력을 **무엇을 고정하는가**에 따라 나눈다. 얼굴 정면의 identity와 얼굴 회전은 [P7-5.7](section-07.md)에서 별도로 관리한다.

이 절의 질문은 간단하다. 새 전신 장면을 만들 때 어떤 입력이 얼굴을, 어떤 입력이 의상을, 어떤 입력이 관절 구조를 맡아야 서로의 정보를 덮어쓰지 않을까?

## 한 이미지에 모든 조건을 맡기지 않는다

얼굴, 의상, 자세, 회전을 계속 같은 입력으로 삼으면 한 조건을 고치는 동안 다른 조건도 바뀌기 쉽다. 현재 참조 셋은 역할을 다음처럼 분리한다.

| 자산 | 고정하는 정보 | 사용 범위 |
| --- | --- | --- |
| P7-5.7 정면 토르소 | 얼굴형, 눈·홍채, 앞머리, 청록 단발, 선과 음영 | 얼굴·헤어·화풍 |
| 1단계 착장·전신 | 회색 크롭탑, 와이드 팬츠, 흰 운동화, 정면 전신 비례 | 기본 착장 |
| 2단계 전신·회전 착장 | 열린 흰 크롭 재킷과 손, 네 방향의 의상 가림 관계 | 자켓·손·방향별 착장 |
| body-only OpenPose | 관절 관계, 전신 비례, 화면 안의 방향 | 포즈·프레이밍 |

따라서 토르소 참조는 목·어깨·의상 비례를 정하지 않고, 착장 이미지는 얼굴 identity를 다시 정하지 않는다. OpenPose는 얼굴·손가락·의상 픽셀이 없는 구조 맵으로만 쓴다. 새 입력을 더할 때는 먼저 이 표의 기존 역할과 겹치는지 확인한다.

## 기본 의상은 얼굴 참조와 구조 맵으로 만든다

1단계는 P7-5.7의 1024×1024 정면 머리 참조와 양팔을 자연스럽게 내린 정면 body-only OpenPose를 입력으로 사용한다. 머리 참조는 얼굴·헤어만, OpenPose는 정면 전신 구조만 맡는다. 결과에는 가슴 바로 아래에서 끝나는 회색 슬림 크롭탑, 딥틸 하이웨이스트 여성용 와이드 팬츠, 흰 스니커즈만 넣는다. 자켓·가방·스트랩은 이 단계에서 만들지 않는다.

![1단계 Qwen 전신 착장 기준](../../../assets/part-07/chapter-05/p7-5-2-qwen-edit-prompt-style-outfit_stage1_face_openpose-long-trousers-defined-waist-v4-seed-62294-steps-30.png)

<p><a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-qwen-edit-prompt-style-outfit_stage1_face_openpose-long-trousers-defined-waist-v4-seed-62294-steps-30-result.json" data-language="json">960×1440, 30-step result.json</a></p>

## 자켓은 다음 단계에서 더한다

2단계는 1단계 전신 착장 결과와 P7-5.7의 1024×1024 정면 머리 참조만 사용한다. OpenPose를 다시 넣지 않아 1단계에서 정한 바지·신발·비례와 경쟁하지 않게 한다. 이 단계에서는 앞판이 서로 닿지 않는 열린 흰 크롭 재킷, 접혀 내려오는 칼라, 손목까지 오는 소매와 소매 끝 아래의 양손을 더한다. 회색 크롭티의 몸통과 맨허리 띠는 보이게 하고, 이너 소매·가방·스트랩은 넣지 않는다.

![2단계 Qwen 열린 자켓 전신 착장 기준](../../../assets/part-07/chapter-05/p7-5-2-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png)

<p><a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30-result.json" data-language="json">960×1440, 30-step result.json</a></p>

## 회전한 착장과 구조 맵은 다른 질문에 답한다

방향이 바뀌면 의상이 몸을 가리는 방식과 관절의 원근을 한 이미지로 고정하기 어렵다. 그래서 회전 착장은 재킷·크롭티·팬츠·스니커즈·손의 가림 관계를, OpenPose는 전신 관절과 프레이밍을 따로 대조한다.

정면 2단계 착장을 유일한 이미지 입력으로 사용하고, 멀티플 앵글 LoRA의 카메라 yaw 지시만 더해 네 방향의 착장을 만들었다. 얼굴 identity나 관절 구조를 별도 이미지로 중복 지시하지 않았다.

| −90° 2단계 착장 | −45° 2단계 착장 |
| --- | --- |
| ![−90도 2단계 멀티플 앵글 착장](../../../assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_minus_90-multiple-angle-v1-seed-62294-steps-8.png) | ![−45도 2단계 멀티플 앵글 착장](../../../assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_minus_45-multiple-angle-v1-seed-62294-steps-8.png) |

| +45° 2단계 착장 | +90° 2단계 착장 |
| --- | --- |
| ![+45도 2단계 멀티플 앵글 착장](../../../assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_plus_45-multiple-angle-v1-seed-62294-steps-8.png) | ![+90도 2단계 멀티플 앵글 착장](../../../assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_plus_90-multiple-angle-v1-seed-62294-steps-8.png) |

<p>결과 JSON: <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_minus_90-multiple-angle-v1-seed-62294-steps-8-result.json" data-language="json">−90°</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_minus_45-multiple-angle-v1-seed-62294-steps-8-result.json" data-language="json">−45°</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_plus_45-multiple-angle-v1-seed-62294-steps-8-result.json" data-language="json">+45°</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-qwen-outfit-stage2-yaw_plus_90-multiple-angle-v1-seed-62294-steps-8-result.json" data-language="json">+90°</a></p>

body-only OpenPose는 같은 상완·전완 길이를 유지한 BODY_18 템플릿을 3D 회전·투영해 −90°·−45°·0°·+45°·+90°로 만든다. 정면 0°는 2단계 전신의 프레임을 기준으로 머리·어깨·골반 폭을 유지하고 다리 길이만 15% 늘린 v7 맵이다. 양팔은 바깥쪽 아래로 벌려 손목이 몸통 밖에 남는다. 나머지 네 방향은 같은 비율로 다시 생성하기 전까지 기존 비교 맵을 사용한다.

| −90° | −45° | 0° | +45° | +90° |
| --- | --- | --- | --- | --- |
| ![−90도 body-only OpenPose](../../../assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw-90_pitch+00.png) | ![−45도 body-only OpenPose](../../../assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw-45_pitch+00.png) | ![양팔을 벌린 정면 body-only OpenPose, 다리 15% 연장](../../../assets/part-07/chapter-05/p7-5-2-openpose-fullbody-stage2-open-arms-short-long-legs-v7-yaw+00_pitch+00.png) | ![+45도 body-only OpenPose](../../../assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+45_pitch+00.png) | ![+90도 body-only OpenPose](../../../assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+90_pitch+00.png) |

<p>좌표 JSON: <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw-90_pitch+00.json" data-language="json">−90°</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw-45_pitch+00.json" data-language="json">−45°</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-openpose-fullbody-stage2-open-arms-short-long-legs-v7-yaw+00_pitch+00.json" data-language="json">0° (양팔 벌림·다리 15% 연장 v7)</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+45_pitch+00.json" data-language="json">+45°</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+90_pitch+00.json" data-language="json">+90°</a></p>

<p>실행 기록: <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-openpose-fullbody-stage2-open-arms-short-long-legs-v7-result.json" data-language="json">정면 v7 result.json</a> · <a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-openpose-fullbody-hand-on-waist-pitch0-result.json" data-language="json">기존 5방향 result.json</a></p>

FACE_70처럼 턱선·눈·코·입을 모두 포함한 점군은 얼굴 기하를 다시 지정해 토르소의 얼굴형과 경쟁하므로 현재 입력에서 제외한다.

## 동적 장면은 전신 기준을 조합해 시험한다

정면 2단계 착장은 전신 의상·비례를, P7-5.7 정면 토르소는 얼굴·헤어·선과 음영을 맡긴다. 이 두 이미지만 입력으로 넣어 실내 코트에서 공중에 뜬 앨리웁 직전 동작을 만들었다. 공 하나를 든 오른팔, 균형을 잡는 왼팔, 앞쪽으로 든 왼 무릎과 뒤로 뻗은 오른다리를 짧게 지시했다.

![2단계 전신 기준으로 생성한 앨리웁 동작](../../../assets/part-07/chapter-05/p7-5-2-qwen-edit-fullbody-alley-oop-v1-seed-62294-steps-20.png)

<p><a class="aibook-source-link" href="/AiBook/assets/part-07/chapter-05/p7-5-2-qwen-edit-fullbody-alley-oop-v1-seed-62294-steps-20-result.json" data-language="json">1024×1536, 20-step result.json</a></p>

이 결과는 정면 기준을 대체하지 않는다. 전신 참조 두 장으로도 공중 자세와 농구 장면을 만들 수 있는지 살피는 실험이며, 장면·소품·동작의 일치는 다음 생성에서 다시 비교한다.

## 재현에 필요한 조건을 기록한다

전신 생성 기록에는 입력 파일과 각 입력의 역할, seed, step, 크기, prompt, `prompt_word_count`를 남긴다. `prompt_word_count`는 품질 점수가 아니라 같은 특징을 반복해서 지시하면서 계약이 비대해졌는지 확인하는 보조 정보다.

<details id="qwen-outfit-stages" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_2_qwen_edit_outfit_stages.py" data-language="python">
<summary>Qwen 정면 착장 1~2단계 생성 코드 보기</summary>
<div class="aibook-lazy-source__body">1단계는 정면 머리·OpenPose로 이너와 하의를 만들고, 2단계는 열린 재킷을 더합니다.</div>
</details>

<details id="qwen-fullbody-alley-oop" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_2_qwen_edit_fullbody_alley_oop.py" data-language="python">
<summary>Qwen 앨리웁 전신 생성 코드 보기</summary>
<div class="aibook-lazy-source__body">2단계 전신 착장과 P7-5.7 정면 토르소를 순서대로 입력하고, 동작에 필요한 지시만 추가합니다.</div>
</details>

## 캐릭터 입력 역할을 점검한다

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 역할 | 얼굴·헤어, 의상·손, 관절·프레이밍 중 무엇을 어느 입력이 맡는가? |
| 충돌 | 새 입력이 기존 입력의 얼굴형·착장·관절 역할을 다시 지정하지 않는가? |
| 전신 구조 | 회전 결과에서 어깨·팔·다리·신발이 요청한 방향과 프레임 안에 유지되는가? |
| 재현 | seed, step, 입력 자산, prompt와 `prompt_word_count`가 `result.json`에 남아 있는가? |
| 다음 비교 | 새 구도·장면·소품에서 무엇이 유지됐고 무엇이 달라졌는가? |

## 출처와 참고 자료

- 전신·착장·OpenPose의 실행 조건은 이 절에서 연결한 로컬 `result.json`에서 확인한다.
- 얼굴 정면과 카메라 회전의 기준은 [P7-5.7](section-07.md)에서 확인한다.
