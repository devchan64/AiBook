# P7-5.12 입력 후보 비교표

검수 기록 기준일: 2026-09-15

남은 입력 후보 **193개**를 Mira 목표와 비교한다. 최초 생성 조건 220개 중 사용자 확정 폐기는 **27개(방향 3·배경 5·표정 19)**다. 기존 AI 검수 상태는 실험용 채택 2개·확대 검수 보류 191개이며, 이번 폐기가 나머지 전체에 대한 추가 검수 완료를 뜻하지 않는다.

현재 목표는 얼굴·헤어를 Mira 아이덴티로, 전체 화풍을 Mira 목표 화풍으로 변환하면서 **입력 표정과 구도·포즈, 배경의 사물·배치를 보존**하는 것이다.

관리번호 `P711-IN-NNN`은 원래 생성 순번에 고정한다. 폐기 후에도 번호를 당겨 쓰거나 재사용하지 않는다.

[검수 목록 JSON](p7-5-11-input-review-v1.json)

[후보 카탈로그 JSON](input-images/candidate-catalog.json)

## 목표별 비교

구도·몸 자세·얼굴 방향·표정·의상·배경 요소를 구분해 확인한다. 체형이나 화풍 차이만으로 포즈 변화라고 단정하지 않는다. 이미지를 클릭하면 원본을 볼 수 있다.

## target-01

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-001**<br>bfs-input-01-soft-photo | [![Mira 목표](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png) | [![P711-IN-001 입력](input-images/bfs-input-01-soft-photo.png)](input-images/bfs-input-01-soft-photo.png) | **확대 검수 보류**<br>정면 얼굴에서 입력별 얼굴·헤어·표현 방식은 달라졌다. 사진풍의 의상 추가와 목·어깨 범위, 입력별 입 벌림을 추가 확인한다. |
| **P711-IN-045**<br>bfs-input-01-watercolor | [![Mira 목표](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png) | [![P711-IN-045 입력](input-images/bfs-input-01-watercolor.png)](input-images/bfs-input-01-watercolor.png) | **확대 검수 보류**<br>정면 얼굴에서 입력별 얼굴·헤어·표현 방식은 달라졌다. 사진풍의 의상 추가와 목·어깨 범위, 입력별 입 벌림을 추가 확인한다. |
| **P711-IN-089**<br>bfs-input-01-clay-render | [![Mira 목표](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png) | [![P711-IN-089 입력](input-images/bfs-input-01-clay-render.png)](input-images/bfs-input-01-clay-render.png) | **확대 검수 보류**<br>정면 얼굴에서 입력별 얼굴·헤어·표현 방식은 달라졌다. 사진풍의 의상 추가와 목·어깨 범위, 입력별 입 벌림을 추가 확인한다. |
| **P711-IN-133**<br>bfs-input-01-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png)](../sec-02/p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png) | [![P711-IN-133 입력](input-images/bfs-input-01-ink-illustration.png)](input-images/bfs-input-01-ink-illustration.png) | **확대 검수 보류**<br>정면 얼굴에서 입력별 얼굴·헤어·표현 방식은 달라졌다. 사진풍의 의상 추가와 목·어깨 범위, 입력별 입 벌림을 추가 확인한다. |

## target-02

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-002**<br>bfs-input-02-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png) | [![P711-IN-002 입력](input-images/bfs-input-02-watercolor.png)](input-images/bfs-input-02-watercolor.png) | **확대 검수 보류**<br>정면 회색 상의와 배치는 이어지나 상체 굴곡·몸 비례가 입력마다 달라진다. |
| **P711-IN-046**<br>bfs-input-02-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png) | [![P711-IN-046 입력](input-images/bfs-input-02-clay-render.png)](input-images/bfs-input-02-clay-render.png) | **확대 검수 보류**<br>정면 회색 상의와 배치는 이어지나 상체 굴곡·몸 비례가 입력마다 달라진다. |
| **P711-IN-090**<br>bfs-input-02-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png) | [![P711-IN-090 입력](input-images/bfs-input-02-ink-illustration.png)](input-images/bfs-input-02-ink-illustration.png) | **확대 검수 보류**<br>정면 회색 상의와 배치는 이어지나 상체 굴곡·몸 비례가 입력마다 달라진다. |
| **P711-IN-134**<br>bfs-input-02-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png) | [![P711-IN-134 입력](input-images/bfs-input-02-oil-painting.png)](input-images/bfs-input-02-oil-painting.png) | **확대 검수 보류**<br>정면 회색 상의와 배치는 이어지나 상체 굴곡·몸 비례가 입력마다 달라진다. |
| **P711-IN-178**<br>bfs-input-02-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png) | [![P711-IN-178 입력](input-images/bfs-input-02-soft-photo.png)](input-images/bfs-input-02-soft-photo.png) | **확대 검수 보류**<br>정면 회색 상의와 배치는 이어지나 상체 굴곡·몸 비례가 입력마다 달라진다. |

## target-03

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-003**<br>bfs-input-03-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-003 입력](input-images/bfs-input-03-clay-render.png)](input-images/bfs-input-03-clay-render.png) | **확대 검수 보류**<br>로우앵글 사선과 회색 크롭 상의·바지 배치는 대체로 이어진다. 입 벌림과 허리·가슴 비례는 확대 검수가 필요하다. |
| **P711-IN-047**<br>bfs-input-03-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-047 입력](input-images/bfs-input-03-ink-illustration.png)](input-images/bfs-input-03-ink-illustration.png) | **확대 검수 보류**<br>로우앵글 사선과 회색 크롭 상의·바지 배치는 대체로 이어진다. 입 벌림과 허리·가슴 비례는 확대 검수가 필요하다. |
| **P711-IN-091**<br>bfs-input-03-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-091 입력](input-images/bfs-input-03-oil-painting.png)](input-images/bfs-input-03-oil-painting.png) | **확대 검수 보류**<br>로우앵글 사선과 회색 크롭 상의·바지 배치는 대체로 이어진다. 입 벌림과 허리·가슴 비례는 확대 검수가 필요하다. |
| **P711-IN-135**<br>bfs-input-03-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-135 입력](input-images/bfs-input-03-soft-photo.png)](input-images/bfs-input-03-soft-photo.png) | **확대 검수 보류**<br>로우앵글 사선과 회색 크롭 상의·바지 배치는 대체로 이어진다. 입 벌림과 허리·가슴 비례는 확대 검수가 필요하다. |
| **P711-IN-179**<br>bfs-input-03-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-179 입력](input-images/bfs-input-03-watercolor.png)](input-images/bfs-input-03-watercolor.png) | **확대 검수 보류**<br>로우앵글 사선과 회색 크롭 상의·바지 배치는 대체로 이어진다. 입 벌림과 허리·가슴 비례는 확대 검수가 필요하다. |

## target-04

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-004**<br>bfs-input-04-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-zero-lowzero-repeat-v1-size-1280x1280-seed-62295-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-zero-lowzero-repeat-v1-size-1280x1280-seed-62295-steps-4.png) | [![P711-IN-004 입력](input-images/bfs-input-04-ink-illustration.png)](input-images/bfs-input-04-ink-illustration.png) | **확대 검수 보류**<br>올려다보는 방향은 이어지지만 여러 입력에서 원래보다 입을 크게 벌렸다. |

## target-05

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-005**<br>bfs-input-05-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-005 입력](input-images/bfs-input-05-oil-painting.png)](input-images/bfs-input-05-oil-painting.png) | **확대 검수 보류**<br>낮은 사선 방향과 회색 크롭 상의는 이어진다. 목·가슴·허리 비례와 화풍별 입 벌림을 확인한다. |
| **P711-IN-049**<br>bfs-input-05-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-049 입력](input-images/bfs-input-05-soft-photo.png)](input-images/bfs-input-05-soft-photo.png) | **확대 검수 보류**<br>낮은 사선 방향과 회색 크롭 상의는 이어진다. 목·가슴·허리 비례와 화풍별 입 벌림을 확인한다. |
| **P711-IN-093**<br>bfs-input-05-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-093 입력](input-images/bfs-input-05-watercolor.png)](input-images/bfs-input-05-watercolor.png) | **확대 검수 보류**<br>낮은 사선 방향과 회색 크롭 상의는 이어진다. 목·가슴·허리 비례와 화풍별 입 벌림을 확인한다. |
| **P711-IN-137**<br>bfs-input-05-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-137 입력](input-images/bfs-input-05-clay-render.png)](input-images/bfs-input-05-clay-render.png) | **확대 검수 보류**<br>낮은 사선 방향과 회색 크롭 상의는 이어진다. 목·가슴·허리 비례와 화풍별 입 벌림을 확인한다. |
| **P711-IN-181**<br>bfs-input-05-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-plus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-181 입력](input-images/bfs-input-05-ink-illustration.png)](input-images/bfs-input-05-ink-illustration.png) | **확대 검수 보류**<br>낮은 사선 방향과 회색 크롭 상의는 이어진다. 목·가슴·허리 비례와 화풍별 입 벌림을 확인한다. |

## target-06

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-006**<br>bfs-input-06-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-006 입력](input-images/bfs-input-06-soft-photo.png)](input-images/bfs-input-06-soft-photo.png) | **확대 검수 보류**<br>측면 방향은 대체로 이어진다. 얼굴 회전량과 상체 두께 변화의 허용 범위를 확인한다. |
| **P711-IN-050**<br>bfs-input-06-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-050 입력](input-images/bfs-input-06-watercolor.png)](input-images/bfs-input-06-watercolor.png) | **확대 검수 보류**<br>측면 방향은 대체로 이어진다. 얼굴 회전량과 상체 두께 변화의 허용 범위를 확인한다. |
| **P711-IN-094**<br>bfs-input-06-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-094 입력](input-images/bfs-input-06-clay-render.png)](input-images/bfs-input-06-clay-render.png) | **확대 검수 보류**<br>측면 방향은 대체로 이어진다. 얼굴 회전량과 상체 두께 변화의 허용 범위를 확인한다. |
| **P711-IN-138**<br>bfs-input-06-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-138 입력](input-images/bfs-input-06-ink-illustration.png)](input-images/bfs-input-06-ink-illustration.png) | **확대 검수 보류**<br>측면 방향은 대체로 이어진다. 얼굴 회전량과 상체 두께 변화의 허용 범위를 확인한다. |
| **P711-IN-182**<br>bfs-input-06-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-182 입력](input-images/bfs-input-06-oil-painting.png)](input-images/bfs-input-06-oil-painting.png) | **확대 검수 보류**<br>측면 방향은 대체로 이어진다. 얼굴 회전량과 상체 두께 변화의 허용 범위를 확인한다. |

## target-07

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-007**<br>bfs-input-07-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-007 입력](input-images/bfs-input-07-watercolor.png)](input-images/bfs-input-07-watercolor.png) | **확대 검수 보류**<br>사선 상반신과 회색 상의가 이어진다. 몸 굴곡과 입 벌림에 변화가 있다. |
| **P711-IN-051**<br>bfs-input-07-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-051 입력](input-images/bfs-input-07-clay-render.png)](input-images/bfs-input-07-clay-render.png) | **확대 검수 보류**<br>사선 상반신과 회색 상의가 이어진다. 몸 굴곡과 입 벌림에 변화가 있다. |
| **P711-IN-095**<br>bfs-input-07-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-095 입력](input-images/bfs-input-07-ink-illustration.png)](input-images/bfs-input-07-ink-illustration.png) | **확대 검수 보류**<br>사선 상반신과 회색 상의가 이어진다. 몸 굴곡과 입 벌림에 변화가 있다. |
| **P711-IN-139**<br>bfs-input-07-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-139 입력](input-images/bfs-input-07-oil-painting.png)](input-images/bfs-input-07-oil-painting.png) | **확대 검수 보류**<br>사선 상반신과 회색 상의가 이어진다. 몸 굴곡과 입 벌림에 변화가 있다. |
| **P711-IN-183**<br>bfs-input-07-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-183 입력](input-images/bfs-input-07-soft-photo.png)](input-images/bfs-input-07-soft-photo.png) | **확대 검수 보류**<br>사선 상반신과 회색 상의가 이어진다. 몸 굴곡과 입 벌림에 변화가 있다. |

## target-08

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-008**<br>bfs-input-08-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-008 입력](input-images/bfs-input-08-clay-render.png)](input-images/bfs-input-08-clay-render.png) | **확대 검수 보류**<br>사선 방향은 이어지나 상의 밑단·노출되는 허리와 상체 비례가 달라 보인다. |
| **P711-IN-052**<br>bfs-input-08-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-052 입력](input-images/bfs-input-08-ink-illustration.png)](input-images/bfs-input-08-ink-illustration.png) | **확대 검수 보류**<br>사선 방향은 이어지나 상의 밑단·노출되는 허리와 상체 비례가 달라 보인다. |
| **P711-IN-096**<br>bfs-input-08-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-096 입력](input-images/bfs-input-08-oil-painting.png)](input-images/bfs-input-08-oil-painting.png) | **확대 검수 보류**<br>사선 방향은 이어지나 상의 밑단·노출되는 허리와 상체 비례가 달라 보인다. |
| **P711-IN-140**<br>bfs-input-08-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-140 입력](input-images/bfs-input-08-soft-photo.png)](input-images/bfs-input-08-soft-photo.png) | **확대 검수 보류**<br>사선 방향은 이어지나 상의 밑단·노출되는 허리와 상체 비례가 달라 보인다. |
| **P711-IN-184**<br>bfs-input-08-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-184 입력](input-images/bfs-input-08-watercolor.png)](input-images/bfs-input-08-watercolor.png) | **확대 검수 보류**<br>사선 방향은 이어지나 상의 밑단·노출되는 허리와 상체 비례가 달라 보인다. |

## target-09

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-009**<br>bfs-input-09-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-009 입력](input-images/bfs-input-09-ink-illustration.png)](input-images/bfs-input-09-ink-illustration.png) | **확대 검수 보류**<br>측면과 상의는 이어진다. 사진풍의 옷 기장과 입력별 상체 두께를 확인한다. |
| **P711-IN-053**<br>bfs-input-09-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-053 입력](input-images/bfs-input-09-oil-painting.png)](input-images/bfs-input-09-oil-painting.png) | **확대 검수 보류**<br>측면과 상의는 이어진다. 사진풍의 옷 기장과 입력별 상체 두께를 확인한다. |
| **P711-IN-097**<br>bfs-input-09-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-097 입력](input-images/bfs-input-09-soft-photo.png)](input-images/bfs-input-09-soft-photo.png) | **확대 검수 보류**<br>측면과 상의는 이어진다. 사진풍의 옷 기장과 입력별 상체 두께를 확인한다. |
| **P711-IN-141**<br>bfs-input-09-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-141 입력](input-images/bfs-input-09-watercolor.png)](input-images/bfs-input-09-watercolor.png) | **확대 검수 보류**<br>측면과 상의는 이어진다. 사진풍의 옷 기장과 입력별 상체 두께를 확인한다. |
| **P711-IN-185**<br>bfs-input-09-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-plus-90-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-185 입력](input-images/bfs-input-09-clay-render.png)](input-images/bfs-input-09-clay-render.png) | **확대 검수 보류**<br>측면과 상의는 이어진다. 사진풍의 옷 기장과 입력별 상체 두께를 확인한다. |

## target-10

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-010**<br>bfs-input-10-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-010 입력](input-images/bfs-input-10-oil-painting.png)](input-images/bfs-input-10-oil-painting.png) | **확대 검수 보류**<br>고각도 전신 배치와 발 위치는 대체로 대응한다. 목·어깨·시선·손의 세부 확인이 필요하다. |
| **P711-IN-054**<br>bfs-input-10-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-054 입력](input-images/bfs-input-10-soft-photo.png)](input-images/bfs-input-10-soft-photo.png) | **확대 검수 보류**<br>고각도 전신 배치와 발 위치는 대체로 대응한다. 목·어깨·시선·손의 세부 확인이 필요하다. |
| **P711-IN-098**<br>bfs-input-10-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-098 입력](input-images/bfs-input-10-watercolor.png)](input-images/bfs-input-10-watercolor.png) | **확대 검수 보류**<br>고각도 전신 배치와 발 위치는 대체로 대응한다. 목·어깨·시선·손의 세부 확인이 필요하다. |
| **P711-IN-142**<br>bfs-input-10-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-142 입력](input-images/bfs-input-10-clay-render.png)](input-images/bfs-input-10-clay-render.png) | **확대 검수 보류**<br>고각도 전신 배치와 발 위치는 대체로 대응한다. 목·어깨·시선·손의 세부 확인이 필요하다. |
| **P711-IN-186**<br>bfs-input-10-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-186 입력](input-images/bfs-input-10-ink-illustration.png)](input-images/bfs-input-10-ink-illustration.png) | **확대 검수 보류**<br>고각도 전신 배치와 발 위치는 대체로 대응한다. 목·어깨·시선·손의 세부 확인이 필요하다. |

## target-11

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-011**<br>bfs-input-11-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-011 입력](input-images/bfs-input-11-soft-photo.png)](input-images/bfs-input-11-soft-photo.png) | **확대 검수 보류**<br>높은 정면 시점과 발 배치는 이어진다. 얼굴 크기와 표정·입 벌림이 달라 보인다. |
| **P711-IN-055**<br>bfs-input-11-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-055 입력](input-images/bfs-input-11-watercolor.png)](input-images/bfs-input-11-watercolor.png) | **확대 검수 보류**<br>높은 정면 시점과 발 배치는 이어진다. 얼굴 크기와 표정·입 벌림이 달라 보인다. |
| **P711-IN-099**<br>bfs-input-11-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-099 입력](input-images/bfs-input-11-clay-render.png)](input-images/bfs-input-11-clay-render.png) | **확대 검수 보류**<br>높은 정면 시점과 발 배치는 이어진다. 얼굴 크기와 표정·입 벌림이 달라 보인다. |
| **P711-IN-143**<br>bfs-input-11-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-143 입력](input-images/bfs-input-11-ink-illustration.png)](input-images/bfs-input-11-ink-illustration.png) | **확대 검수 보류**<br>높은 정면 시점과 발 배치는 이어진다. 얼굴 크기와 표정·입 벌림이 달라 보인다. |
| **P711-IN-187**<br>bfs-input-11-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png) | [![P711-IN-187 입력](input-images/bfs-input-11-oil-painting.png)](input-images/bfs-input-11-oil-painting.png) | **확대 검수 보류**<br>높은 정면 시점과 발 배치는 이어진다. 얼굴 크기와 표정·입 벌림이 달라 보인다. |

## target-12

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-012**<br>bfs-input-12-watercolor | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-012 입력](input-images/bfs-input-12-watercolor.png)](input-images/bfs-input-12-watercolor.png) | **확대 검수 보류**<br>높은 사선 시점과 몸·발 배치는 이어진다. 몸 비례와 입 벌림을 확인한다. |
| **P711-IN-056**<br>bfs-input-12-clay-render | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-056 입력](input-images/bfs-input-12-clay-render.png)](input-images/bfs-input-12-clay-render.png) | **확대 검수 보류**<br>높은 사선 시점과 몸·발 배치는 이어진다. 몸 비례와 입 벌림을 확인한다. |
| **P711-IN-100**<br>bfs-input-12-ink-illustration | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-100 입력](input-images/bfs-input-12-ink-illustration.png)](input-images/bfs-input-12-ink-illustration.png) | **확대 검수 보류**<br>높은 사선 시점과 몸·발 배치는 이어진다. 몸 비례와 입 벌림을 확인한다. |
| **P711-IN-144**<br>bfs-input-12-oil-painting | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-144 입력](input-images/bfs-input-12-oil-painting.png)](input-images/bfs-input-12-oil-painting.png) | **확대 검수 보류**<br>높은 사선 시점과 몸·발 배치는 이어진다. 몸 비례와 입 벌림을 확인한다. |
| **P711-IN-188**<br>bfs-input-12-soft-photo | [![Mira 목표](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png)](../sec-02/p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-plus-45-native1024-v1-size-1024x1024-seed-62294-steps-4.png) | [![P711-IN-188 입력](input-images/bfs-input-12-soft-photo.png)](input-images/bfs-input-12-soft-photo.png) | **확대 검수 보류**<br>높은 사선 시점과 몸·발 배치는 이어진다. 몸 비례와 입 벌림을 확인한다. |

## target-13

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-013**<br>bfs-input-13-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-background-01.png)](training-images/p7-5-11-mira-v2-background-01.png) | [![P711-IN-013 입력](input-images/bfs-input-13-clay-render.png)](input-images/bfs-input-13-clay-render.png) | **확대 검수 보류**<br>도서관 선반 배치는 대체로 이어진다. 일부 화풍에서 인물과 배경의 표현 방식이 섞이며 입력별 몸 비례가 달라진다. |
| **P711-IN-057**<br>bfs-input-13-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-background-01.png)](training-images/p7-5-11-mira-v2-background-01.png) | [![P711-IN-057 입력](input-images/bfs-input-13-ink-illustration.png)](input-images/bfs-input-13-ink-illustration.png) | **확대 검수 보류**<br>도서관 선반 배치는 대체로 이어진다. 일부 화풍에서 인물과 배경의 표현 방식이 섞이며 입력별 몸 비례가 달라진다. |
| **P711-IN-101**<br>bfs-input-13-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-background-01.png)](training-images/p7-5-11-mira-v2-background-01.png) | [![P711-IN-101 입력](input-images/bfs-input-13-oil-painting.png)](input-images/bfs-input-13-oil-painting.png) | **확대 검수 보류**<br>도서관 선반 배치는 대체로 이어진다. 일부 화풍에서 인물과 배경의 표현 방식이 섞이며 입력별 몸 비례가 달라진다. |
| **P711-IN-189**<br>bfs-input-13-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-background-01.png)](training-images/p7-5-11-mira-v2-background-01.png) | [![P711-IN-189 입력](input-images/bfs-input-13-watercolor.png)](input-images/bfs-input-13-watercolor.png) | **확대 검수 보류**<br>도서관 선반 배치는 대체로 이어진다. 일부 화풍에서 인물과 배경의 표현 방식이 섞이며 입력별 몸 비례가 달라진다. |

## target-14

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-014**<br>bfs-input-14-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-background-02.png)](training-images/p7-5-11-mira-v2-background-02.png) | [![P711-IN-014 입력](input-images/bfs-input-14-ink-illustration.png)](input-images/bfs-input-14-ink-illustration.png) | **확대 검수 보류**<br>공원 배치가 이어진다. 사진풍·점토·펜화 인물에 비해 배경의 원래 그림 표현이 많이 남아 전체 화풍 전환 여부를 확인해야 한다. |
| **P711-IN-058**<br>bfs-input-14-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-background-02.png)](training-images/p7-5-11-mira-v2-background-02.png) | [![P711-IN-058 입력](input-images/bfs-input-14-oil-painting.png)](input-images/bfs-input-14-oil-painting.png) | **확대 검수 보류**<br>공원 배치가 이어진다. 사진풍·점토·펜화 인물에 비해 배경의 원래 그림 표현이 많이 남아 전체 화풍 전환 여부를 확인해야 한다. |
| **P711-IN-102**<br>bfs-input-14-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-background-02.png)](training-images/p7-5-11-mira-v2-background-02.png) | [![P711-IN-102 입력](input-images/bfs-input-14-soft-photo.png)](input-images/bfs-input-14-soft-photo.png) | **확대 검수 보류**<br>공원 배치가 이어진다. 사진풍·점토·펜화 인물에 비해 배경의 원래 그림 표현이 많이 남아 전체 화풍 전환 여부를 확인해야 한다. |
| **P711-IN-146**<br>bfs-input-14-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-background-02.png)](training-images/p7-5-11-mira-v2-background-02.png) | [![P711-IN-146 입력](input-images/bfs-input-14-watercolor.png)](input-images/bfs-input-14-watercolor.png) | **확대 검수 보류**<br>공원 배치가 이어진다. 사진풍·점토·펜화 인물에 비해 배경의 원래 그림 표현이 많이 남아 전체 화풍 전환 여부를 확인해야 한다. |
| **P711-IN-190**<br>bfs-input-14-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-background-02.png)](training-images/p7-5-11-mira-v2-background-02.png) | [![P711-IN-190 입력](input-images/bfs-input-14-clay-render.png)](input-images/bfs-input-14-clay-render.png) | **확대 검수 보류**<br>공원 배치가 이어진다. 사진풍·점토·펜화 인물에 비해 배경의 원래 그림 표현이 많이 남아 전체 화풍 전환 여부를 확인해야 한다. |

## target-15

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-015**<br>bfs-input-15-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-background-03.png)](training-images/p7-5-11-mira-v2-background-03.png) | [![P711-IN-015 입력](input-images/bfs-input-15-oil-painting.png)](input-images/bfs-input-15-oil-painting.png) | **확대 검수 보류**<br>카페의 책상·창·화분 배치는 대체로 이어진다. 수채화의 가장자리 소실과 인물·배경 화풍의 일치 여부를 확인한다. |
| **P711-IN-059**<br>bfs-input-15-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-background-03.png)](training-images/p7-5-11-mira-v2-background-03.png) | [![P711-IN-059 입력](input-images/bfs-input-15-soft-photo.png)](input-images/bfs-input-15-soft-photo.png) | **확대 검수 보류**<br>카페의 책상·창·화분 배치는 대체로 이어진다. 수채화의 가장자리 소실과 인물·배경 화풍의 일치 여부를 확인한다. |
| **P711-IN-103**<br>bfs-input-15-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-background-03.png)](training-images/p7-5-11-mira-v2-background-03.png) | [![P711-IN-103 입력](input-images/bfs-input-15-watercolor.png)](input-images/bfs-input-15-watercolor.png) | **확대 검수 보류**<br>카페의 책상·창·화분 배치는 대체로 이어진다. 수채화의 가장자리 소실과 인물·배경 화풍의 일치 여부를 확인한다. |
| **P711-IN-147**<br>bfs-input-15-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-background-03.png)](training-images/p7-5-11-mira-v2-background-03.png) | [![P711-IN-147 입력](input-images/bfs-input-15-clay-render.png)](input-images/bfs-input-15-clay-render.png) | **확대 검수 보류**<br>카페의 책상·창·화분 배치는 대체로 이어진다. 수채화의 가장자리 소실과 인물·배경 화풍의 일치 여부를 확인한다. |
| **P711-IN-191**<br>bfs-input-15-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-background-03.png)](training-images/p7-5-11-mira-v2-background-03.png) | [![P711-IN-191 입력](input-images/bfs-input-15-ink-illustration.png)](input-images/bfs-input-15-ink-illustration.png) | **확대 검수 보류**<br>카페의 책상·창·화분 배치는 대체로 이어진다. 수채화의 가장자리 소실과 인물·배경 화풍의 일치 여부를 확인한다. |

## target-16

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-016**<br>bfs-input-16-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-background-04.png)](training-images/p7-5-11-mira-v2-background-04.png) | [![P711-IN-016 입력](input-images/bfs-input-16-soft-photo.png)](input-images/bfs-input-16-soft-photo.png) | **확대 검수 보류**<br>사무실 배치가 이어지지만 입력별 몸 비례와 입 벌림이 다르다. 배경까지 화풍이 전환됐는지 추가 확인한다. |
| **P711-IN-060**<br>bfs-input-16-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-background-04.png)](training-images/p7-5-11-mira-v2-background-04.png) | [![P711-IN-060 입력](input-images/bfs-input-16-watercolor.png)](input-images/bfs-input-16-watercolor.png) | **확대 검수 보류**<br>사무실 배치가 이어지지만 입력별 몸 비례와 입 벌림이 다르다. 배경까지 화풍이 전환됐는지 추가 확인한다. |
| **P711-IN-104**<br>bfs-input-16-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-background-04.png)](training-images/p7-5-11-mira-v2-background-04.png) | [![P711-IN-104 입력](input-images/bfs-input-16-clay-render.png)](input-images/bfs-input-16-clay-render.png) | **확대 검수 보류**<br>사무실 배치가 이어지지만 입력별 몸 비례와 입 벌림이 다르다. 배경까지 화풍이 전환됐는지 추가 확인한다. |
| **P711-IN-148**<br>bfs-input-16-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-background-04.png)](training-images/p7-5-11-mira-v2-background-04.png) | [![P711-IN-148 입력](input-images/bfs-input-16-ink-illustration.png)](input-images/bfs-input-16-ink-illustration.png) | **확대 검수 보류**<br>사무실 배치가 이어지지만 입력별 몸 비례와 입 벌림이 다르다. 배경까지 화풍이 전환됐는지 추가 확인한다. |
| **P711-IN-192**<br>bfs-input-16-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-background-04.png)](training-images/p7-5-11-mira-v2-background-04.png) | [![P711-IN-192 입력](input-images/bfs-input-16-oil-painting.png)](input-images/bfs-input-16-oil-painting.png) | **확대 검수 보류**<br>사무실 배치가 이어지지만 입력별 몸 비례와 입 벌림이 다르다. 배경까지 화풍이 전환됐는지 추가 확인한다. |

## target-17

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-061**<br>bfs-input-17-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-background-07.png)](training-images/p7-5-11-mira-v2-background-07.png) | [![P711-IN-061 입력](input-images/bfs-input-17-clay-render.png)](input-images/bfs-input-17-clay-render.png) | **확대 검수 보류**<br>단색 배경과 정면 상반신이 기준이다. 수채화의 배경 패턴 생성과 점토의 입 벌림이 눈에 띈다. |
| **P711-IN-105**<br>bfs-input-17-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-background-07.png)](training-images/p7-5-11-mira-v2-background-07.png) | [![P711-IN-105 입력](input-images/bfs-input-17-ink-illustration.png)](input-images/bfs-input-17-ink-illustration.png) | **확대 검수 보류**<br>단색 배경과 정면 상반신이 기준이다. 수채화의 배경 패턴 생성과 점토의 입 벌림이 눈에 띈다. |
| **P711-IN-149**<br>bfs-input-17-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-background-07.png)](training-images/p7-5-11-mira-v2-background-07.png) | [![P711-IN-149 입력](input-images/bfs-input-17-oil-painting.png)](input-images/bfs-input-17-oil-painting.png) | **확대 검수 보류**<br>단색 배경과 정면 상반신이 기준이다. 수채화의 배경 패턴 생성과 점토의 입 벌림이 눈에 띈다. |
| **P711-IN-193**<br>bfs-input-17-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-background-07.png)](training-images/p7-5-11-mira-v2-background-07.png) | [![P711-IN-193 입력](input-images/bfs-input-17-soft-photo.png)](input-images/bfs-input-17-soft-photo.png) | **확대 검수 보류**<br>단색 배경과 정면 상반신이 기준이다. 수채화의 배경 패턴 생성과 점토의 입 벌림이 눈에 띈다. |

## target-18

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-018**<br>bfs-input-18-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-background-08.png)](training-images/p7-5-11-mira-v2-background-08.png) | [![P711-IN-018 입력](input-images/bfs-input-18-clay-render.png)](input-images/bfs-input-18-clay-render.png) | **확대 검수 보류**<br>갈색 배경과 사선 상반신이 기준이다. 수채화의 여백·화면 점유와 유화 배경의 추상 무늬를 확인한다. |
| **P711-IN-062**<br>bfs-input-18-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-background-08.png)](training-images/p7-5-11-mira-v2-background-08.png) | [![P711-IN-062 입력](input-images/bfs-input-18-ink-illustration.png)](input-images/bfs-input-18-ink-illustration.png) | **확대 검수 보류**<br>갈색 배경과 사선 상반신이 기준이다. 수채화의 여백·화면 점유와 유화 배경의 추상 무늬를 확인한다. |
| **P711-IN-106**<br>bfs-input-18-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-background-08.png)](training-images/p7-5-11-mira-v2-background-08.png) | [![P711-IN-106 입력](input-images/bfs-input-18-oil-painting.png)](input-images/bfs-input-18-oil-painting.png) | **확대 검수 보류**<br>갈색 배경과 사선 상반신이 기준이다. 수채화의 여백·화면 점유와 유화 배경의 추상 무늬를 확인한다. |
| **P711-IN-150**<br>bfs-input-18-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-background-08.png)](training-images/p7-5-11-mira-v2-background-08.png) | [![P711-IN-150 입력](input-images/bfs-input-18-soft-photo.png)](input-images/bfs-input-18-soft-photo.png) | **확대 검수 보류**<br>갈색 배경과 사선 상반신이 기준이다. 수채화의 여백·화면 점유와 유화 배경의 추상 무늬를 확인한다. |
| **P711-IN-194**<br>bfs-input-18-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-background-08.png)](training-images/p7-5-11-mira-v2-background-08.png) | [![P711-IN-194 입력](input-images/bfs-input-18-watercolor.png)](input-images/bfs-input-18-watercolor.png) | **확대 검수 보류**<br>갈색 배경과 사선 상반신이 기준이다. 수채화의 여백·화면 점유와 유화 배경의 추상 무늬를 확인한다. |

## target-19

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-019**<br>bfs-input-19-ink-illustration | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-02.png)](validation/images/p7-5-11-mira-v2-evaluation-02.png) | [![P711-IN-019 입력](input-images/bfs-input-19-ink-illustration.png)](input-images/bfs-input-19-ink-illustration.png) | **확대 검수 보류**<br>강가 벤치와 손을 든 동작은 이어진다. 손가락·컵 없는 손의 동작 및 인물과 배경 화풍의 일관성을 추가 검수한다. |
| **P711-IN-063**<br>bfs-input-19-oil-painting | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-02.png)](validation/images/p7-5-11-mira-v2-evaluation-02.png) | [![P711-IN-063 입력](input-images/bfs-input-19-oil-painting.png)](input-images/bfs-input-19-oil-painting.png) | **확대 검수 보류**<br>강가 벤치와 손을 든 동작은 이어진다. 손가락·컵 없는 손의 동작 및 인물과 배경 화풍의 일관성을 추가 검수한다. |
| **P711-IN-107**<br>bfs-input-19-soft-photo | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-02.png)](validation/images/p7-5-11-mira-v2-evaluation-02.png) | [![P711-IN-107 입력](input-images/bfs-input-19-soft-photo.png)](input-images/bfs-input-19-soft-photo.png) | **확대 검수 보류**<br>강가 벤치와 손을 든 동작은 이어진다. 손가락·컵 없는 손의 동작 및 인물과 배경 화풍의 일관성을 추가 검수한다. |
| **P711-IN-151**<br>bfs-input-19-watercolor | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-02.png)](validation/images/p7-5-11-mira-v2-evaluation-02.png) | [![P711-IN-151 입력](input-images/bfs-input-19-watercolor.png)](input-images/bfs-input-19-watercolor.png) | **확대 검수 보류**<br>강가 벤치와 손을 든 동작은 이어진다. 손가락·컵 없는 손의 동작 및 인물과 배경 화풍의 일관성을 추가 검수한다. |
| **P711-IN-195**<br>bfs-input-19-clay-render | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-02.png)](validation/images/p7-5-11-mira-v2-evaluation-02.png) | [![P711-IN-195 입력](input-images/bfs-input-19-clay-render.png)](input-images/bfs-input-19-clay-render.png) | **확대 검수 보류**<br>강가 벤치와 손을 든 동작은 이어진다. 손가락·컵 없는 손의 동작 및 인물과 배경 화풍의 일관성을 추가 검수한다. |

## target-20

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-020**<br>bfs-input-20-oil-painting | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-04.png)](validation/images/p7-5-11-mira-v2-evaluation-04.png) | [![P711-IN-020 입력](input-images/bfs-input-20-oil-painting.png)](input-images/bfs-input-20-oil-painting.png) | **확대 검수 보류**<br>복도 전신·코트·화분은 이어진다. 손의 위치, 단추와 코트 길이, 작은 얼굴의 시선은 확대 검수가 필요하다. |
| **P711-IN-064**<br>bfs-input-20-soft-photo | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-04.png)](validation/images/p7-5-11-mira-v2-evaluation-04.png) | [![P711-IN-064 입력](input-images/bfs-input-20-soft-photo.png)](input-images/bfs-input-20-soft-photo.png) | **확대 검수 보류**<br>복도 전신·코트·화분은 이어진다. 손의 위치, 단추와 코트 길이, 작은 얼굴의 시선은 확대 검수가 필요하다. |
| **P711-IN-108**<br>bfs-input-20-watercolor | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-04.png)](validation/images/p7-5-11-mira-v2-evaluation-04.png) | [![P711-IN-108 입력](input-images/bfs-input-20-watercolor.png)](input-images/bfs-input-20-watercolor.png) | **확대 검수 보류**<br>복도 전신·코트·화분은 이어진다. 손의 위치, 단추와 코트 길이, 작은 얼굴의 시선은 확대 검수가 필요하다. |
| **P711-IN-152**<br>bfs-input-20-clay-render | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-04.png)](validation/images/p7-5-11-mira-v2-evaluation-04.png) | [![P711-IN-152 입력](input-images/bfs-input-20-clay-render.png)](input-images/bfs-input-20-clay-render.png) | **확대 검수 보류**<br>복도 전신·코트·화분은 이어진다. 손의 위치, 단추와 코트 길이, 작은 얼굴의 시선은 확대 검수가 필요하다. |
| **P711-IN-196**<br>bfs-input-20-ink-illustration | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-04.png)](validation/images/p7-5-11-mira-v2-evaluation-04.png) | [![P711-IN-196 입력](input-images/bfs-input-20-ink-illustration.png)](input-images/bfs-input-20-ink-illustration.png) | **확대 검수 보류**<br>복도 전신·코트·화분은 이어진다. 손의 위치, 단추와 코트 길이, 작은 얼굴의 시선은 확대 검수가 필요하다. |

## target-21

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-021**<br>bfs-input-21-soft-photo | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-05.png)](validation/images/p7-5-11-mira-v2-evaluation-05.png) | [![P711-IN-021 입력](input-images/bfs-input-21-soft-photo.png)](input-images/bfs-input-21-soft-photo.png) | **확대 검수 보류**<br>미술관·초록 셔츠의 방향은 대체로 이어진다. 수채화에서 장면이 사라졌고 다른 입력은 배경 화풍과 몸 굴곡을 확인해야 한다. |
| **P711-IN-109**<br>bfs-input-21-clay-render | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-05.png)](validation/images/p7-5-11-mira-v2-evaluation-05.png) | [![P711-IN-109 입력](input-images/bfs-input-21-clay-render.png)](input-images/bfs-input-21-clay-render.png) | **확대 검수 보류**<br>미술관·초록 셔츠의 방향은 대체로 이어진다. 수채화에서 장면이 사라졌고 다른 입력은 배경 화풍과 몸 굴곡을 확인해야 한다. |
| **P711-IN-153**<br>bfs-input-21-ink-illustration | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-05.png)](validation/images/p7-5-11-mira-v2-evaluation-05.png) | [![P711-IN-153 입력](input-images/bfs-input-21-ink-illustration.png)](input-images/bfs-input-21-ink-illustration.png) | **확대 검수 보류**<br>미술관·초록 셔츠의 방향은 대체로 이어진다. 수채화에서 장면이 사라졌고 다른 입력은 배경 화풍과 몸 굴곡을 확인해야 한다. |
| **P711-IN-197**<br>bfs-input-21-oil-painting | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-05.png)](validation/images/p7-5-11-mira-v2-evaluation-05.png) | [![P711-IN-197 입력](input-images/bfs-input-21-oil-painting.png)](input-images/bfs-input-21-oil-painting.png) | **확대 검수 보류**<br>미술관·초록 셔츠의 방향은 대체로 이어진다. 수채화에서 장면이 사라졌고 다른 입력은 배경 화풍과 몸 굴곡을 확인해야 한다. |

## target-22

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-022**<br>bfs-input-22-watercolor | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-06.png)](validation/images/p7-5-11-mira-v2-evaluation-06.png) | [![P711-IN-022 입력](input-images/bfs-input-22-watercolor.png)](input-images/bfs-input-22-watercolor.png) | **확대 검수 보류**<br>컵을 양손으로 잡은 동작과 창틀은 이어진다. 손가락·컵 테두리·표정 및 배경 화풍 전환을 확대 검수한다. |
| **P711-IN-066**<br>bfs-input-22-clay-render | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-06.png)](validation/images/p7-5-11-mira-v2-evaluation-06.png) | [![P711-IN-066 입력](input-images/bfs-input-22-clay-render.png)](input-images/bfs-input-22-clay-render.png) | **확대 검수 보류**<br>컵을 양손으로 잡은 동작과 창틀은 이어진다. 손가락·컵 테두리·표정 및 배경 화풍 전환을 확대 검수한다. |
| **P711-IN-110**<br>bfs-input-22-ink-illustration | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-06.png)](validation/images/p7-5-11-mira-v2-evaluation-06.png) | [![P711-IN-110 입력](input-images/bfs-input-22-ink-illustration.png)](input-images/bfs-input-22-ink-illustration.png) | **확대 검수 보류**<br>컵을 양손으로 잡은 동작과 창틀은 이어진다. 손가락·컵 테두리·표정 및 배경 화풍 전환을 확대 검수한다. |
| **P711-IN-154**<br>bfs-input-22-oil-painting | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-06.png)](validation/images/p7-5-11-mira-v2-evaluation-06.png) | [![P711-IN-154 입력](input-images/bfs-input-22-oil-painting.png)](input-images/bfs-input-22-oil-painting.png) | **확대 검수 보류**<br>컵을 양손으로 잡은 동작과 창틀은 이어진다. 손가락·컵 테두리·표정 및 배경 화풍 전환을 확대 검수한다. |
| **P711-IN-198**<br>bfs-input-22-soft-photo | [![Mira 목표](validation/images/p7-5-11-mira-v2-evaluation-06.png)](validation/images/p7-5-11-mira-v2-evaluation-06.png) | [![P711-IN-198 입력](input-images/bfs-input-22-soft-photo.png)](input-images/bfs-input-22-soft-photo.png) | **확대 검수 보류**<br>컵을 양손으로 잡은 동작과 창틀은 이어진다. 손가락·컵 테두리·표정 및 배경 화풍 전환을 확대 검수한다. |


## target-24

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-024**<br>bfs-input-24-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-02.png)](training-images/p7-5-11-mira-v2-expression-02.png) | [![P711-IN-024 입력](input-images/bfs-input-24-ink-illustration.png)](input-images/bfs-input-24-ink-illustration.png) | **확대 검수 보류**<br>벌어진 입과 사선 방향은 이어진다. 눈썹 움직임, 몸 비례와 목 길이의 세부 대응을 확인한다. |
| **P711-IN-068**<br>bfs-input-24-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-02.png)](training-images/p7-5-11-mira-v2-expression-02.png) | [![P711-IN-068 입력](input-images/bfs-input-24-oil-painting.png)](input-images/bfs-input-24-oil-painting.png) | **확대 검수 보류**<br>벌어진 입과 사선 방향은 이어진다. 눈썹 움직임, 몸 비례와 목 길이의 세부 대응을 확인한다. |
| **P711-IN-112**<br>bfs-input-24-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-02.png)](training-images/p7-5-11-mira-v2-expression-02.png) | [![P711-IN-112 입력](input-images/bfs-input-24-soft-photo.png)](input-images/bfs-input-24-soft-photo.png) | **확대 검수 보류**<br>벌어진 입과 사선 방향은 이어진다. 눈썹 움직임, 몸 비례와 목 길이의 세부 대응을 확인한다. |
| **P711-IN-156**<br>bfs-input-24-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-02.png)](training-images/p7-5-11-mira-v2-expression-02.png) | [![P711-IN-156 입력](input-images/bfs-input-24-watercolor.png)](input-images/bfs-input-24-watercolor.png) | **확대 검수 보류**<br>벌어진 입과 사선 방향은 이어진다. 눈썹 움직임, 몸 비례와 목 길이의 세부 대응을 확인한다. |
| **P711-IN-200**<br>bfs-input-24-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-02.png)](training-images/p7-5-11-mira-v2-expression-02.png) | [![P711-IN-200 입력](input-images/bfs-input-24-clay-render.png)](input-images/bfs-input-24-clay-render.png) | **확대 검수 보류**<br>벌어진 입과 사선 방향은 이어진다. 눈썹 움직임, 몸 비례와 목 길이의 세부 대응을 확인한다. |

## target-25

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-025**<br>bfs-input-25-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-03.png)](training-images/p7-5-11-mira-v2-expression-03.png) | [![P711-IN-025 입력](input-images/bfs-input-25-oil-painting.png)](input-images/bfs-input-25-oil-painting.png) | **확대 검수 보류**<br>치아가 보이는 미소는 이어지나 목표보다 눈을 더 크게 뜨고 입 벌림도 달라져 표정 보존을 추가 확인한다. |
| **P711-IN-069**<br>bfs-input-25-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-03.png)](training-images/p7-5-11-mira-v2-expression-03.png) | [![P711-IN-069 입력](input-images/bfs-input-25-soft-photo.png)](input-images/bfs-input-25-soft-photo.png) | **확대 검수 보류**<br>치아가 보이는 미소는 이어지나 목표보다 눈을 더 크게 뜨고 입 벌림도 달라져 표정 보존을 추가 확인한다. |
| **P711-IN-113**<br>bfs-input-25-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-03.png)](training-images/p7-5-11-mira-v2-expression-03.png) | [![P711-IN-113 입력](input-images/bfs-input-25-watercolor.png)](input-images/bfs-input-25-watercolor.png) | **확대 검수 보류**<br>치아가 보이는 미소는 이어지나 목표보다 눈을 더 크게 뜨고 입 벌림도 달라져 표정 보존을 추가 확인한다. |
| **P711-IN-157**<br>bfs-input-25-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-03.png)](training-images/p7-5-11-mira-v2-expression-03.png) | [![P711-IN-157 입력](input-images/bfs-input-25-clay-render.png)](input-images/bfs-input-25-clay-render.png) | **확대 검수 보류**<br>치아가 보이는 미소는 이어지나 목표보다 눈을 더 크게 뜨고 입 벌림도 달라져 표정 보존을 추가 확인한다. |
| **P711-IN-201**<br>bfs-input-25-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-03.png)](training-images/p7-5-11-mira-v2-expression-03.png) | [![P711-IN-201 입력](input-images/bfs-input-25-ink-illustration.png)](input-images/bfs-input-25-ink-illustration.png) | **확대 검수 보류**<br>치아가 보이는 미소는 이어지나 목표보다 눈을 더 크게 뜨고 입 벌림도 달라져 표정 보존을 추가 확인한다. |


## target-27

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-027**<br>bfs-input-27-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-05.png)](training-images/p7-5-11-mira-v2-expression-05.png) | [![P711-IN-027 입력](input-images/bfs-input-27-watercolor.png)](input-images/bfs-input-27-watercolor.png) | **확대 검수 보류**<br>목표의 올라간 안쪽 눈썹과 처진 입꼬리가 입력에서 약해지거나 다른 표정으로 보인다. |
| **P711-IN-071**<br>bfs-input-27-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-05.png)](training-images/p7-5-11-mira-v2-expression-05.png) | [![P711-IN-071 입력](input-images/bfs-input-27-clay-render.png)](input-images/bfs-input-27-clay-render.png) | **확대 검수 보류**<br>목표의 올라간 안쪽 눈썹과 처진 입꼬리가 입력에서 약해지거나 다른 표정으로 보인다. |
| **P711-IN-115**<br>bfs-input-27-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-05.png)](training-images/p7-5-11-mira-v2-expression-05.png) | [![P711-IN-115 입력](input-images/bfs-input-27-ink-illustration.png)](input-images/bfs-input-27-ink-illustration.png) | **확대 검수 보류**<br>목표의 올라간 안쪽 눈썹과 처진 입꼬리가 입력에서 약해지거나 다른 표정으로 보인다. |
| **P711-IN-159**<br>bfs-input-27-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-05.png)](training-images/p7-5-11-mira-v2-expression-05.png) | [![P711-IN-159 입력](input-images/bfs-input-27-oil-painting.png)](input-images/bfs-input-27-oil-painting.png) | **확대 검수 보류**<br>목표의 올라간 안쪽 눈썹과 처진 입꼬리가 입력에서 약해지거나 다른 표정으로 보인다. |
| **P711-IN-203**<br>bfs-input-27-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-05.png)](training-images/p7-5-11-mira-v2-expression-05.png) | [![P711-IN-203 입력](input-images/bfs-input-27-soft-photo.png)](input-images/bfs-input-27-soft-photo.png) | **확대 검수 보류**<br>목표의 올라간 안쪽 눈썹과 처진 입꼬리가 입력에서 약해지거나 다른 표정으로 보인다. |


## target-29

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-029**<br>bfs-input-29-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-07.png)](training-images/p7-5-11-mira-v2-expression-07.png) | [![P711-IN-029 입력](input-images/bfs-input-29-ink-illustration.png)](input-images/bfs-input-29-ink-illustration.png) | **확대 검수 보류**<br>놀란 입 모양이 이어지는 후보도 있으나 원형 입·눈썹 모양이 입력에 따라 달라져 추가 검수가 필요하다. |
| **P711-IN-073**<br>bfs-input-29-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-07.png)](training-images/p7-5-11-mira-v2-expression-07.png) | [![P711-IN-073 입력](input-images/bfs-input-29-oil-painting.png)](input-images/bfs-input-29-oil-painting.png) | **확대 검수 보류**<br>놀란 입 모양이 이어지는 후보도 있으나 원형 입·눈썹 모양이 입력에 따라 달라져 추가 검수가 필요하다. |
| **P711-IN-117**<br>bfs-input-29-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-07.png)](training-images/p7-5-11-mira-v2-expression-07.png) | [![P711-IN-117 입력](input-images/bfs-input-29-soft-photo.png)](input-images/bfs-input-29-soft-photo.png) | **확대 검수 보류**<br>놀란 입 모양이 이어지는 후보도 있으나 원형 입·눈썹 모양이 입력에 따라 달라져 추가 검수가 필요하다. |
| **P711-IN-161**<br>bfs-input-29-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-07.png)](training-images/p7-5-11-mira-v2-expression-07.png) | [![P711-IN-161 입력](input-images/bfs-input-29-watercolor.png)](input-images/bfs-input-29-watercolor.png) | **확대 검수 보류**<br>놀란 입 모양이 이어지는 후보도 있으나 원형 입·눈썹 모양이 입력에 따라 달라져 추가 검수가 필요하다. |
| **P711-IN-205**<br>bfs-input-29-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-expression-07.png)](training-images/p7-5-11-mira-v2-expression-07.png) | [![P711-IN-205 입력](input-images/bfs-input-29-clay-render.png)](input-images/bfs-input-29-clay-render.png) | **확대 검수 보류**<br>놀란 입 모양이 이어지는 후보도 있으나 원형 입·눈썹 모양이 입력에 따라 달라져 추가 검수가 필요하다. |

## target-30

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-030**<br>bfs-input-30-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-01.png)](training-images/p7-5-11-mira-v2-lighting-01.png) | [![P711-IN-030 입력](input-images/bfs-input-30-oil-painting.png)](input-images/bfs-input-30-oil-painting.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 목선·몸 비례와 조명 차이가 단순 화풍 차이인지 확인한다. |
| **P711-IN-074**<br>bfs-input-30-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-01.png)](training-images/p7-5-11-mira-v2-lighting-01.png) | [![P711-IN-074 입력](input-images/bfs-input-30-soft-photo.png)](input-images/bfs-input-30-soft-photo.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 목선·몸 비례와 조명 차이가 단순 화풍 차이인지 확인한다. |
| **P711-IN-118**<br>bfs-input-30-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-01.png)](training-images/p7-5-11-mira-v2-lighting-01.png) | [![P711-IN-118 입력](input-images/bfs-input-30-watercolor.png)](input-images/bfs-input-30-watercolor.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 목선·몸 비례와 조명 차이가 단순 화풍 차이인지 확인한다. |
| **P711-IN-162**<br>bfs-input-30-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-01.png)](training-images/p7-5-11-mira-v2-lighting-01.png) | [![P711-IN-162 입력](input-images/bfs-input-30-clay-render.png)](input-images/bfs-input-30-clay-render.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 목선·몸 비례와 조명 차이가 단순 화풍 차이인지 확인한다. |
| **P711-IN-206**<br>bfs-input-30-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-01.png)](training-images/p7-5-11-mira-v2-lighting-01.png) | [![P711-IN-206 입력](input-images/bfs-input-30-ink-illustration.png)](input-images/bfs-input-30-ink-illustration.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 목선·몸 비례와 조명 차이가 단순 화풍 차이인지 확인한다. |

## target-31

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-031**<br>bfs-input-31-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-02.png)](training-images/p7-5-11-mira-v2-lighting-02.png) | [![P711-IN-031 입력](input-images/bfs-input-31-soft-photo.png)](input-images/bfs-input-31-soft-photo.png) | **확대 검수 보류**<br>창가 사선 인물과 창틀이 기준이다. 수채화는 창 배경이 사라졌고 다른 입력은 표정과 그림자 대응을 확인한다. |
| **P711-IN-119**<br>bfs-input-31-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-02.png)](training-images/p7-5-11-mira-v2-lighting-02.png) | [![P711-IN-119 입력](input-images/bfs-input-31-clay-render.png)](input-images/bfs-input-31-clay-render.png) | **확대 검수 보류**<br>창가 사선 인물과 창틀이 기준이다. 수채화는 창 배경이 사라졌고 다른 입력은 표정과 그림자 대응을 확인한다. |
| **P711-IN-163**<br>bfs-input-31-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-02.png)](training-images/p7-5-11-mira-v2-lighting-02.png) | [![P711-IN-163 입력](input-images/bfs-input-31-ink-illustration.png)](input-images/bfs-input-31-ink-illustration.png) | **확대 검수 보류**<br>창가 사선 인물과 창틀이 기준이다. 수채화는 창 배경이 사라졌고 다른 입력은 표정과 그림자 대응을 확인한다. |
| **P711-IN-207**<br>bfs-input-31-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-02.png)](training-images/p7-5-11-mira-v2-lighting-02.png) | [![P711-IN-207 입력](input-images/bfs-input-31-oil-painting.png)](input-images/bfs-input-31-oil-painting.png) | **확대 검수 보류**<br>창가 사선 인물과 창틀이 기준이다. 수채화는 창 배경이 사라졌고 다른 입력은 표정과 그림자 대응을 확인한다. |

## target-32

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-076**<br>bfs-input-32-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-03.png)](training-images/p7-5-11-mira-v2-lighting-03.png) | [![P711-IN-076 입력](input-images/bfs-input-32-clay-render.png)](input-images/bfs-input-32-clay-render.png) | **확대 검수 보류**<br>창틀 그림자가 있는 역광 장면이다. 수채화·펜화는 배경의 창 그림자가 사라졌다. |
| **P711-IN-164**<br>bfs-input-32-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-03.png)](training-images/p7-5-11-mira-v2-lighting-03.png) | [![P711-IN-164 입력](input-images/bfs-input-32-oil-painting.png)](input-images/bfs-input-32-oil-painting.png) | **확대 검수 보류**<br>창틀 그림자가 있는 역광 장면이다. 수채화·펜화는 배경의 창 그림자가 사라졌다. |
| **P711-IN-208**<br>bfs-input-32-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-03.png)](training-images/p7-5-11-mira-v2-lighting-03.png) | [![P711-IN-208 입력](input-images/bfs-input-32-soft-photo.png)](input-images/bfs-input-32-soft-photo.png) | **확대 검수 보류**<br>창틀 그림자가 있는 역광 장면이다. 수채화·펜화는 배경의 창 그림자가 사라졌다. |

## target-33

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-033**<br>bfs-input-33-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-04.png)](training-images/p7-5-11-mira-v2-lighting-04.png) | [![P711-IN-033 입력](input-images/bfs-input-33-clay-render.png)](input-images/bfs-input-33-clay-render.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 상체 굴곡·배경의 밝은 띠·입 벌림의 대응을 확인한다. |
| **P711-IN-077**<br>bfs-input-33-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-04.png)](training-images/p7-5-11-mira-v2-lighting-04.png) | [![P711-IN-077 입력](input-images/bfs-input-33-ink-illustration.png)](input-images/bfs-input-33-ink-illustration.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 상체 굴곡·배경의 밝은 띠·입 벌림의 대응을 확인한다. |
| **P711-IN-121**<br>bfs-input-33-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-04.png)](training-images/p7-5-11-mira-v2-lighting-04.png) | [![P711-IN-121 입력](input-images/bfs-input-33-oil-painting.png)](input-images/bfs-input-33-oil-painting.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 상체 굴곡·배경의 밝은 띠·입 벌림의 대응을 확인한다. |
| **P711-IN-165**<br>bfs-input-33-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-04.png)](training-images/p7-5-11-mira-v2-lighting-04.png) | [![P711-IN-165 입력](input-images/bfs-input-33-soft-photo.png)](input-images/bfs-input-33-soft-photo.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 상체 굴곡·배경의 밝은 띠·입 벌림의 대응을 확인한다. |
| **P711-IN-209**<br>bfs-input-33-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-04.png)](training-images/p7-5-11-mira-v2-lighting-04.png) | [![P711-IN-209 입력](input-images/bfs-input-33-watercolor.png)](input-images/bfs-input-33-watercolor.png) | **확대 검수 보류**<br>정면·회색 상의는 이어진다. 상체 굴곡·배경의 밝은 띠·입 벌림의 대응을 확인한다. |

## target-34

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-034**<br>bfs-input-34-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-06.png)](training-images/p7-5-11-mira-v2-lighting-06.png) | [![P711-IN-034 입력](input-images/bfs-input-34-ink-illustration.png)](input-images/bfs-input-34-ink-illustration.png) | **확대 검수 보류**<br>푸른 실내 조명이 기준이다. 수채화는 밝은 종이 여백으로 바뀌고 다른 입력은 창틀·빛 배치의 대응을 확인한다. |
| **P711-IN-078**<br>bfs-input-34-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-06.png)](training-images/p7-5-11-mira-v2-lighting-06.png) | [![P711-IN-078 입력](input-images/bfs-input-34-oil-painting.png)](input-images/bfs-input-34-oil-painting.png) | **확대 검수 보류**<br>푸른 실내 조명이 기준이다. 수채화는 밝은 종이 여백으로 바뀌고 다른 입력은 창틀·빛 배치의 대응을 확인한다. |
| **P711-IN-122**<br>bfs-input-34-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-06.png)](training-images/p7-5-11-mira-v2-lighting-06.png) | [![P711-IN-122 입력](input-images/bfs-input-34-soft-photo.png)](input-images/bfs-input-34-soft-photo.png) | **확대 검수 보류**<br>푸른 실내 조명이 기준이다. 수채화는 밝은 종이 여백으로 바뀌고 다른 입력은 창틀·빛 배치의 대응을 확인한다. |
| **P711-IN-166**<br>bfs-input-34-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-06.png)](training-images/p7-5-11-mira-v2-lighting-06.png) | [![P711-IN-166 입력](input-images/bfs-input-34-watercolor.png)](input-images/bfs-input-34-watercolor.png) | **확대 검수 보류**<br>푸른 실내 조명이 기준이다. 수채화는 밝은 종이 여백으로 바뀌고 다른 입력은 창틀·빛 배치의 대응을 확인한다. |
| **P711-IN-210**<br>bfs-input-34-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-06.png)](training-images/p7-5-11-mira-v2-lighting-06.png) | [![P711-IN-210 입력](input-images/bfs-input-34-clay-render.png)](input-images/bfs-input-34-clay-render.png) | **확대 검수 보류**<br>푸른 실내 조명이 기준이다. 수채화는 밝은 종이 여백으로 바뀌고 다른 입력은 창틀·빛 배치의 대응을 확인한다. |

## target-35

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-035**<br>bfs-input-35-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-07.png)](training-images/p7-5-11-mira-v2-lighting-07.png) | [![P711-IN-035 입력](input-images/bfs-input-35-oil-painting.png)](input-images/bfs-input-35-oil-painting.png) | **확대 검수 보류**<br>역광 윤곽이 입력마다 약해지거나 정면 조명으로 보인다. 조명 보존과 화풍 전환의 허용 범위를 확인한다. |
| **P711-IN-079**<br>bfs-input-35-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-07.png)](training-images/p7-5-11-mira-v2-lighting-07.png) | [![P711-IN-079 입력](input-images/bfs-input-35-soft-photo.png)](input-images/bfs-input-35-soft-photo.png) | **확대 검수 보류**<br>역광 윤곽이 입력마다 약해지거나 정면 조명으로 보인다. 조명 보존과 화풍 전환의 허용 범위를 확인한다. |
| **P711-IN-123**<br>bfs-input-35-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-07.png)](training-images/p7-5-11-mira-v2-lighting-07.png) | [![P711-IN-123 입력](input-images/bfs-input-35-watercolor.png)](input-images/bfs-input-35-watercolor.png) | **확대 검수 보류**<br>역광 윤곽이 입력마다 약해지거나 정면 조명으로 보인다. 조명 보존과 화풍 전환의 허용 범위를 확인한다. |
| **P711-IN-167**<br>bfs-input-35-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-07.png)](training-images/p7-5-11-mira-v2-lighting-07.png) | [![P711-IN-167 입력](input-images/bfs-input-35-clay-render.png)](input-images/bfs-input-35-clay-render.png) | **확대 검수 보류**<br>역광 윤곽이 입력마다 약해지거나 정면 조명으로 보인다. 조명 보존과 화풍 전환의 허용 범위를 확인한다. |
| **P711-IN-211**<br>bfs-input-35-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-07.png)](training-images/p7-5-11-mira-v2-lighting-07.png) | [![P711-IN-211 입력](input-images/bfs-input-35-ink-illustration.png)](input-images/bfs-input-35-ink-illustration.png) | **확대 검수 보류**<br>역광 윤곽이 입력마다 약해지거나 정면 조명으로 보인다. 조명 보존과 화풍 전환의 허용 범위를 확인한다. |

## target-36

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-036**<br>bfs-input-36-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-08.png)](training-images/p7-5-11-mira-v2-lighting-08.png) | [![P711-IN-036 입력](input-images/bfs-input-36-soft-photo.png)](input-images/bfs-input-36-soft-photo.png) | **확대 검수 보류**<br>사선·회색 상의는 이어진다. 얼굴과 상의의 하이라이트·몸 굴곡·입 벌림을 추가 확인한다. |
| **P711-IN-080**<br>bfs-input-36-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-08.png)](training-images/p7-5-11-mira-v2-lighting-08.png) | [![P711-IN-080 입력](input-images/bfs-input-36-watercolor.png)](input-images/bfs-input-36-watercolor.png) | **확대 검수 보류**<br>사선·회색 상의는 이어진다. 얼굴과 상의의 하이라이트·몸 굴곡·입 벌림을 추가 확인한다. |
| **P711-IN-124**<br>bfs-input-36-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-08.png)](training-images/p7-5-11-mira-v2-lighting-08.png) | [![P711-IN-124 입력](input-images/bfs-input-36-clay-render.png)](input-images/bfs-input-36-clay-render.png) | **확대 검수 보류**<br>사선·회색 상의는 이어진다. 얼굴과 상의의 하이라이트·몸 굴곡·입 벌림을 추가 확인한다. |
| **P711-IN-168**<br>bfs-input-36-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-08.png)](training-images/p7-5-11-mira-v2-lighting-08.png) | [![P711-IN-168 입력](input-images/bfs-input-36-ink-illustration.png)](input-images/bfs-input-36-ink-illustration.png) | **확대 검수 보류**<br>사선·회색 상의는 이어진다. 얼굴과 상의의 하이라이트·몸 굴곡·입 벌림을 추가 확인한다. |
| **P711-IN-212**<br>bfs-input-36-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-lighting-08.png)](training-images/p7-5-11-mira-v2-lighting-08.png) | [![P711-IN-212 입력](input-images/bfs-input-36-oil-painting.png)](input-images/bfs-input-36-oil-painting.png) | **확대 검수 보류**<br>사선·회색 상의는 이어진다. 얼굴과 상의의 하이라이트·몸 굴곡·입 벌림을 추가 확인한다. |

## target-37

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-037**<br>bfs-input-37-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-01.png)](training-images/p7-5-11-mira-v2-outfit-01.png) | [![P711-IN-037 입력](input-images/bfs-input-37-watercolor.png)](input-images/bfs-input-37-watercolor.png) | **확대 검수 보류**<br>정면 남색 스웨터와 단순 배경이 기준이다. 사진풍·펜화는 확대 비교했고 나머지는 목선·입 벌림을 추가 확인한다. |
| **P711-IN-081**<br>bfs-input-37-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-01.png)](training-images/p7-5-11-mira-v2-outfit-01.png) | [![P711-IN-081 입력](input-images/bfs-input-37-clay-render.png)](input-images/bfs-input-37-clay-render.png) | **확대 검수 보류**<br>정면 남색 스웨터와 단순 배경이 기준이다. 사진풍·펜화는 확대 비교했고 나머지는 목선·입 벌림을 추가 확인한다. |
| **P711-IN-125**<br>bfs-input-37-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-01.png)](training-images/p7-5-11-mira-v2-outfit-01.png) | [![P711-IN-125 입력](input-images/bfs-input-37-ink-illustration.png)](input-images/bfs-input-37-ink-illustration.png) | **실험용 채택**<br>확대 비교에서 정면·열린 눈·약하게 벌어진 입, 남색 스웨터와 상반신 배치가 대응하고 얼굴·긴 머리·펜화 표현으로 변환됐다. 미세한 입 벌림·의복 선 차이를 허용한 질적 후보 채택이다. |
| **P711-IN-169**<br>bfs-input-37-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-01.png)](training-images/p7-5-11-mira-v2-outfit-01.png) | [![P711-IN-169 입력](input-images/bfs-input-37-oil-painting.png)](input-images/bfs-input-37-oil-painting.png) | **확대 검수 보류**<br>정면 남색 스웨터와 단순 배경이 기준이다. 사진풍·펜화는 확대 비교했고 나머지는 목선·입 벌림을 추가 확인한다. |
| **P711-IN-213**<br>bfs-input-37-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-01.png)](training-images/p7-5-11-mira-v2-outfit-01.png) | [![P711-IN-213 입력](input-images/bfs-input-37-soft-photo.png)](input-images/bfs-input-37-soft-photo.png) | **실험용 채택**<br>확대 비교에서 정면·열린 눈·약하게 벌어진 입과 남색 둥근 목 스웨터·상반신 배치가 대체로 대응한다. 얼굴·헤어와 사진 표현은 달라졌다. 목선의 세부 차이가 있어 첫 학습 후보로만 채택하며 정밀 정렬을 보장하지 않는다. |

## target-38

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-038**<br>bfs-input-38-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-02.png)](training-images/p7-5-11-mira-v2-outfit-02.png) | [![P711-IN-038 입력](input-images/bfs-input-38-clay-render.png)](input-images/bfs-input-38-clay-render.png) | **확대 검수 보류**<br>흰 셔츠의 칼라·단추와 사선 방향이 이어진다. 입력별 입 벌림과 목 비례를 확인한다. |
| **P711-IN-082**<br>bfs-input-38-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-02.png)](training-images/p7-5-11-mira-v2-outfit-02.png) | [![P711-IN-082 입력](input-images/bfs-input-38-ink-illustration.png)](input-images/bfs-input-38-ink-illustration.png) | **확대 검수 보류**<br>흰 셔츠의 칼라·단추와 사선 방향이 이어진다. 입력별 입 벌림과 목 비례를 확인한다. |
| **P711-IN-126**<br>bfs-input-38-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-02.png)](training-images/p7-5-11-mira-v2-outfit-02.png) | [![P711-IN-126 입력](input-images/bfs-input-38-oil-painting.png)](input-images/bfs-input-38-oil-painting.png) | **확대 검수 보류**<br>흰 셔츠의 칼라·단추와 사선 방향이 이어진다. 입력별 입 벌림과 목 비례를 확인한다. |
| **P711-IN-170**<br>bfs-input-38-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-02.png)](training-images/p7-5-11-mira-v2-outfit-02.png) | [![P711-IN-170 입력](input-images/bfs-input-38-soft-photo.png)](input-images/bfs-input-38-soft-photo.png) | **확대 검수 보류**<br>흰 셔츠의 칼라·단추와 사선 방향이 이어진다. 입력별 입 벌림과 목 비례를 확인한다. |
| **P711-IN-214**<br>bfs-input-38-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-02.png)](training-images/p7-5-11-mira-v2-outfit-02.png) | [![P711-IN-214 입력](input-images/bfs-input-38-watercolor.png)](input-images/bfs-input-38-watercolor.png) | **확대 검수 보류**<br>흰 셔츠의 칼라·단추와 사선 방향이 이어진다. 입력별 입 벌림과 목 비례를 확인한다. |

## target-39

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-039**<br>bfs-input-39-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-03.png)](training-images/p7-5-11-mira-v2-outfit-03.png) | [![P711-IN-039 입력](input-images/bfs-input-39-ink-illustration.png)](input-images/bfs-input-39-ink-illustration.png) | **확대 검수 보류**<br>버건디 카디건과 회색 이너·사선 방향이 이어진다. 눈썹·입꼬리가 표정 변화인지 외형 차이인지 확인한다. |
| **P711-IN-083**<br>bfs-input-39-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-03.png)](training-images/p7-5-11-mira-v2-outfit-03.png) | [![P711-IN-083 입력](input-images/bfs-input-39-oil-painting.png)](input-images/bfs-input-39-oil-painting.png) | **확대 검수 보류**<br>버건디 카디건과 회색 이너·사선 방향이 이어진다. 눈썹·입꼬리가 표정 변화인지 외형 차이인지 확인한다. |
| **P711-IN-127**<br>bfs-input-39-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-03.png)](training-images/p7-5-11-mira-v2-outfit-03.png) | [![P711-IN-127 입력](input-images/bfs-input-39-soft-photo.png)](input-images/bfs-input-39-soft-photo.png) | **확대 검수 보류**<br>버건디 카디건과 회색 이너·사선 방향이 이어진다. 눈썹·입꼬리가 표정 변화인지 외형 차이인지 확인한다. |
| **P711-IN-171**<br>bfs-input-39-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-03.png)](training-images/p7-5-11-mira-v2-outfit-03.png) | [![P711-IN-171 입력](input-images/bfs-input-39-watercolor.png)](input-images/bfs-input-39-watercolor.png) | **확대 검수 보류**<br>버건디 카디건과 회색 이너·사선 방향이 이어진다. 눈썹·입꼬리가 표정 변화인지 외형 차이인지 확인한다. |
| **P711-IN-215**<br>bfs-input-39-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-03.png)](training-images/p7-5-11-mira-v2-outfit-03.png) | [![P711-IN-215 입력](input-images/bfs-input-39-clay-render.png)](input-images/bfs-input-39-clay-render.png) | **확대 검수 보류**<br>버건디 카디건과 회색 이너·사선 방향이 이어진다. 눈썹·입꼬리가 표정 변화인지 외형 차이인지 확인한다. |

## target-40

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-040**<br>bfs-input-40-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-04.png)](training-images/p7-5-11-mira-v2-outfit-04.png) | [![P711-IN-040 입력](input-images/bfs-input-40-oil-painting.png)](input-images/bfs-input-40-oil-painting.png) | **확대 검수 보류**<br>정면 재킷과 이너가 기준이다. 수채화의 얼굴 방향이 사선으로 바뀌었고 다른 입력은 단추·몸 비례를 확인한다. |
| **P711-IN-084**<br>bfs-input-40-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-04.png)](training-images/p7-5-11-mira-v2-outfit-04.png) | [![P711-IN-084 입력](input-images/bfs-input-40-soft-photo.png)](input-images/bfs-input-40-soft-photo.png) | **확대 검수 보류**<br>정면 재킷과 이너가 기준이다. 수채화의 얼굴 방향이 사선으로 바뀌었고 다른 입력은 단추·몸 비례를 확인한다. |
| **P711-IN-172**<br>bfs-input-40-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-04.png)](training-images/p7-5-11-mira-v2-outfit-04.png) | [![P711-IN-172 입력](input-images/bfs-input-40-clay-render.png)](input-images/bfs-input-40-clay-render.png) | **확대 검수 보류**<br>정면 재킷과 이너가 기준이다. 수채화의 얼굴 방향이 사선으로 바뀌었고 다른 입력은 단추·몸 비례를 확인한다. |
| **P711-IN-216**<br>bfs-input-40-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-04.png)](training-images/p7-5-11-mira-v2-outfit-04.png) | [![P711-IN-216 입력](input-images/bfs-input-40-ink-illustration.png)](input-images/bfs-input-40-ink-illustration.png) | **확대 검수 보류**<br>정면 재킷과 이너가 기준이다. 수채화의 얼굴 방향이 사선으로 바뀌었고 다른 입력은 단추·몸 비례를 확인한다. |

## target-41

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-041**<br>bfs-input-41-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-05.png)](training-images/p7-5-11-mira-v2-outfit-05.png) | [![P711-IN-041 입력](input-images/bfs-input-41-soft-photo.png)](input-images/bfs-input-41-soft-photo.png) | **확대 검수 보류**<br>초록 터틀넥과 사선 방향은 이어진다. 몸 굴곡과 시선·입 벌림을 추가 확인한다. |
| **P711-IN-085**<br>bfs-input-41-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-05.png)](training-images/p7-5-11-mira-v2-outfit-05.png) | [![P711-IN-085 입력](input-images/bfs-input-41-watercolor.png)](input-images/bfs-input-41-watercolor.png) | **확대 검수 보류**<br>초록 터틀넥과 사선 방향은 이어진다. 몸 굴곡과 시선·입 벌림을 추가 확인한다. |
| **P711-IN-129**<br>bfs-input-41-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-05.png)](training-images/p7-5-11-mira-v2-outfit-05.png) | [![P711-IN-129 입력](input-images/bfs-input-41-clay-render.png)](input-images/bfs-input-41-clay-render.png) | **확대 검수 보류**<br>초록 터틀넥과 사선 방향은 이어진다. 몸 굴곡과 시선·입 벌림을 추가 확인한다. |
| **P711-IN-173**<br>bfs-input-41-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-05.png)](training-images/p7-5-11-mira-v2-outfit-05.png) | [![P711-IN-173 입력](input-images/bfs-input-41-ink-illustration.png)](input-images/bfs-input-41-ink-illustration.png) | **확대 검수 보류**<br>초록 터틀넥과 사선 방향은 이어진다. 몸 굴곡과 시선·입 벌림을 추가 확인한다. |
| **P711-IN-212**<br>bfs-input-41-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-05.png)](training-images/p7-5-11-mira-v2-outfit-05.png) | [![P711-IN-212 입력](input-images/bfs-input-41-oil-painting.png)](input-images/bfs-input-41-oil-painting.png) | **확대 검수 보류**<br>초록 터틀넥과 사선 방향은 이어진다. 몸 굴곡과 시선·입 벌림을 추가 확인한다. |

## target-42

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-042**<br>bfs-input-42-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-06.png)](training-images/p7-5-11-mira-v2-outfit-06.png) | [![P711-IN-042 입력](input-images/bfs-input-42-watercolor.png)](input-images/bfs-input-42-watercolor.png) | **확대 검수 보류**<br>데님 재킷의 칼라·주머니·단추와 사선 방향이 이어진다. 입 벌림과 손이 없는 프레임 경계를 확인한다. |
| **P711-IN-086**<br>bfs-input-42-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-06.png)](training-images/p7-5-11-mira-v2-outfit-06.png) | [![P711-IN-086 입력](input-images/bfs-input-42-clay-render.png)](input-images/bfs-input-42-clay-render.png) | **확대 검수 보류**<br>데님 재킷의 칼라·주머니·단추와 사선 방향이 이어진다. 입 벌림과 손이 없는 프레임 경계를 확인한다. |
| **P711-IN-130**<br>bfs-input-42-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-06.png)](training-images/p7-5-11-mira-v2-outfit-06.png) | [![P711-IN-130 입력](input-images/bfs-input-42-ink-illustration.png)](input-images/bfs-input-42-ink-illustration.png) | **확대 검수 보류**<br>데님 재킷의 칼라·주머니·단추와 사선 방향이 이어진다. 입 벌림과 손이 없는 프레임 경계를 확인한다. |
| **P711-IN-174**<br>bfs-input-42-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-06.png)](training-images/p7-5-11-mira-v2-outfit-06.png) | [![P711-IN-174 입력](input-images/bfs-input-42-oil-painting.png)](input-images/bfs-input-42-oil-painting.png) | **확대 검수 보류**<br>데님 재킷의 칼라·주머니·단추와 사선 방향이 이어진다. 입 벌림과 손이 없는 프레임 경계를 확인한다. |
| **P711-IN-218**<br>bfs-input-42-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-06.png)](training-images/p7-5-11-mira-v2-outfit-06.png) | [![P711-IN-218 입력](input-images/bfs-input-42-soft-photo.png)](input-images/bfs-input-42-soft-photo.png) | **확대 검수 보류**<br>데님 재킷의 칼라·주머니·단추와 사선 방향이 이어진다. 입 벌림과 손이 없는 프레임 경계를 확인한다. |

## target-43

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-043**<br>bfs-input-43-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-07.png)](training-images/p7-5-11-mira-v2-outfit-07.png) | [![P711-IN-043 입력](input-images/bfs-input-43-clay-render.png)](input-images/bfs-input-43-clay-render.png) | **확대 검수 보류**<br>정면 보라색 블라우스가 이어진다. 사진풍은 입이 더 닫히고 어깨·목선 형태가 달라 보인다. |
| **P711-IN-087**<br>bfs-input-43-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-07.png)](training-images/p7-5-11-mira-v2-outfit-07.png) | [![P711-IN-087 입력](input-images/bfs-input-43-ink-illustration.png)](input-images/bfs-input-43-ink-illustration.png) | **확대 검수 보류**<br>정면 보라색 블라우스가 이어진다. 사진풍은 입이 더 닫히고 어깨·목선 형태가 달라 보인다. |
| **P711-IN-131**<br>bfs-input-43-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-07.png)](training-images/p7-5-11-mira-v2-outfit-07.png) | [![P711-IN-131 입력](input-images/bfs-input-43-oil-painting.png)](input-images/bfs-input-43-oil-painting.png) | **확대 검수 보류**<br>정면 보라색 블라우스가 이어진다. 사진풍은 입이 더 닫히고 어깨·목선 형태가 달라 보인다. |
| **P711-IN-175**<br>bfs-input-43-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-07.png)](training-images/p7-5-11-mira-v2-outfit-07.png) | [![P711-IN-175 입력](input-images/bfs-input-43-soft-photo.png)](input-images/bfs-input-43-soft-photo.png) | **확대 검수 보류**<br>정면 보라색 블라우스가 이어진다. 사진풍은 입이 더 닫히고 어깨·목선 형태가 달라 보인다. |
| **P711-IN-219**<br>bfs-input-43-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-07.png)](training-images/p7-5-11-mira-v2-outfit-07.png) | [![P711-IN-219 입력](input-images/bfs-input-43-watercolor.png)](input-images/bfs-input-43-watercolor.png) | **확대 검수 보류**<br>정면 보라색 블라우스가 이어진다. 사진풍은 입이 더 닫히고 어깨·목선 형태가 달라 보인다. |

## target-44

| 관리번호 · 입력 ID | Mira 목표 | 생성 입력 후보 | 현재 검수 의견 |
| --- | --- | --- | --- |
| **P711-IN-044**<br>bfs-input-44-ink-illustration | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-08.png)](training-images/p7-5-11-mira-v2-outfit-08.png) | [![P711-IN-044 입력](input-images/bfs-input-44-ink-illustration.png)](input-images/bfs-input-44-ink-illustration.png) | **확대 검수 보류**<br>회색 후드와 끈·사선 방향이 이어진다. 펜화는 눈썹 각도와 입 벌림이 커 표정 보존을 보류한다. |
| **P711-IN-088**<br>bfs-input-44-oil-painting | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-08.png)](training-images/p7-5-11-mira-v2-outfit-08.png) | [![P711-IN-088 입력](input-images/bfs-input-44-oil-painting.png)](input-images/bfs-input-44-oil-painting.png) | **확대 검수 보류**<br>회색 후드와 끈·사선 방향이 이어진다. 펜화는 눈썹 각도와 입 벌림이 커 표정 보존을 보류한다. |
| **P711-IN-132**<br>bfs-input-44-soft-photo | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-08.png)](training-images/p7-5-11-mira-v2-outfit-08.png) | [![P711-IN-132 입력](input-images/bfs-input-44-soft-photo.png)](input-images/bfs-input-44-soft-photo.png) | **확대 검수 보류**<br>회색 후드와 끈·사선 방향이 이어진다. 펜화는 눈썹 각도와 입 벌림이 커 표정 보존을 보류한다. |
| **P711-IN-176**<br>bfs-input-44-watercolor | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-08.png)](training-images/p7-5-11-mira-v2-outfit-08.png) | [![P711-IN-176 입력](input-images/bfs-input-44-watercolor.png)](input-images/bfs-input-44-watercolor.png) | **확대 검수 보류**<br>회색 후드와 끈·사선 방향이 이어진다. 펜화는 눈썹 각도와 입 벌림이 커 표정 보존을 보류한다. |
| **P711-IN-220**<br>bfs-input-44-clay-render | [![Mira 목표](training-images/p7-5-11-mira-v2-outfit-08.png)](training-images/p7-5-11-mira-v2-outfit-08.png) | [![P711-IN-220 입력](input-images/bfs-input-44-clay-render.png)](input-images/bfs-input-44-clay-render.png) | **확대 검수 보류**<br>회색 후드와 끈·사선 방향이 이어진다. 펜화는 눈썹 각도와 입 벌림이 커 표정 보존을 보류한다. |

## 폐기 확정 번호

입력 이미지와 생성 기록은 삭제되었으며 아래 번호는 재생성하지 않는다. Mira 목표 이미지와 원래 생성 항목·코드는 보존한다.

- **P711-IN-017** · `bfs-input-17-watercolor`: 사용자 폐기 확정.
- **P711-IN-023** · `bfs-input-23-clay-render`: 사용자 폐기 확정.
- **P711-IN-026** · `bfs-input-26-soft-photo`: 사용자 폐기 확정.
- **P711-IN-028** · `bfs-input-28-clay-render`: 사용자 폐기 확정.
- **P711-IN-032** · `bfs-input-32-watercolor`: 사용자 폐기 확정.
- **P711-IN-048** · `bfs-input-04-oil-painting`: 사용자 폐기 확정.
- **P711-IN-065** · `bfs-input-21-watercolor`: 사용자 폐기 확정.
- **P711-IN-067** · `bfs-input-23-ink-illustration`: 사용자 폐기 확정.
- **P711-IN-070** · `bfs-input-26-watercolor`: 사용자 폐기 확정.
- **P711-IN-072** · `bfs-input-28-ink-illustration`: 사용자 폐기 확정.
- **P711-IN-075** · `bfs-input-31-watercolor`: 사용자 폐기 확정.
- **P711-IN-092** · `bfs-input-04-soft-photo`: 사용자 폐기 확정.
- **P711-IN-111** · `bfs-input-23-oil-painting`: 사용자 폐기 확정.
- **P711-IN-114** · `bfs-input-26-clay-render`: 사용자 폐기 확정.
- **P711-IN-116** · `bfs-input-28-oil-painting`: 사용자 폐기 확정.
- **P711-IN-120** · `bfs-input-32-ink-illustration`: 사용자 폐기 확정.
- **P711-IN-128** · `bfs-input-40-watercolor`: 사용자 폐기 확정.
- **P711-IN-136** · `bfs-input-04-watercolor`: 사용자 폐기 확정.
- **P711-IN-145** · `bfs-input-13-soft-photo`: 사용자 폐기 확정.
- **P711-IN-155** · `bfs-input-23-soft-photo`: 사용자 폐기 확정.
- **P711-IN-158** · `bfs-input-26-ink-illustration`: 사용자 폐기 확정.
- **P711-IN-160** · `bfs-input-28-soft-photo`: 사용자 폐기 확정.
- **P711-IN-177** · `bfs-input-01-oil-painting`: 사용자 폐기 확정.
- **P711-IN-180** · `bfs-input-04-clay-render`: 사용자 폐기 확정.
- **P711-IN-199** · `bfs-input-23-watercolor`: 사용자 폐기 확정.
- **P711-IN-202** · `bfs-input-26-oil-painting`: 사용자 폐기 확정.
- **P711-IN-204** · `bfs-input-28-watercolor`: 사용자 폐기 확정.

[재생성 제외 목록 JSON](p7-5-11-input-generation-exclusions.json)
