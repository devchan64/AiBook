# Part 7 웹툰 제작 파이프라인 조사 노트

이 문서는 Part 7의 생성형 이미지 실습을 `모델 기능 비교`에서 `짧은 웹툰 시퀀스를 완성하는 제작 흐름`으로 고치기 위한 편집용 조사 노트다. 독자용 원고가 아니며, 실제 원고에는 확인한 도구의 역할과 검증 산출물만 남긴다.

## 작업 목표와 파이프라인 경계

목표는 skeleton 또는 동작 영상을 만드는 일이 아니라, **같은 캐릭터가 서로 다른 장소·카메라·자세의 웹툰 이미지 컷에서 같은 인물로 읽히게 하는 제작 파이프라인**이다. pose, 손·발 contact, 목·시선 정보는 전신 동작이 필요한 컷을 위한 제어 입력과 검수 자료일 뿐, 독자에게 제시할 최종 산출물은 항상 웹툰 이미지 컷이다.

이 목표의 최소 흐름은 다음과 같이 둔다.

1. 자체 제작 캐릭터의 다각도 전신·얼굴·의상 기준서와 장소별 배경 원본을 승인한다.
2. 컷의 서사 목적에 따라 `pose-first`, `face-first`, `camera/background-first`, `object-first` 중 시작 원본을 고른다.
3. 전신 동작 컷에서는 사람 검수를 통과한 driving motion 또는 3D blockout에서 body pose, 목-머리 방향, 손목, 발 접지와 camera/depth/line 입력을 만든다.
4. character LoRA 또는 참조 기반 identity 제어, 구조 조건, 장면 prompt를 분리해 한 컷을 생성한다.
5. 얼굴·눈·앞머리, 손·소품, 발·접지처럼 실패 원인이 다른 영역을 mask inpaint 또는 직접 작화로 보정한다.
6. 서로 다른 배경과 카메라를 포함한 4컷 contact sheet에서 인물성, 공간 연속성, pose, 시선, 손·발 접점, 말풍선 여백을 각각 판정한다.

따라서 관절 수가 충분한지의 질문은 3단계의 입력 적합성을 판단하는 질문이며, 그것만 통과해도 웹툰 컷 파이프라인이 성공한 것으로 보지 않는다.

## 현재 예제가 전달하지 못한 것

현재 P7-5.2의 OpenPose와 IP-Adapter 예제는 각각 pose 입력과 참조 이미지를 확인한다. 이전의 간이 2D cutout rig는 부품 회전에서 관절·가림이 자연스럽지 않아 최종 제작 경로에서 제외했다. 그러나 다음 연결이 없어서 독자가 이 결과만으로 웹툰 제작 가능성을 판단하기 어렵다.

1. 한 컷의 좋은 결과를 골라 다음 컷의 기준 자산으로 승인하는 단계가 없다.
2. 배경, 카메라, 인물 전신 pose를 먼저 설계하고 생성 입력으로 내보내는 단계가 없다.
3. 얼굴, 눈, 손, 머리카락, 의상처럼 실패 원인이 다른 영역을 분리해 고치는 단계가 없다.
4. 완성 컷을 나란히 놓고 캐릭터와 공간의 연속성을 판정하는 시퀀스 검수가 없다.
5. 말풍선 여백, 식자, 세로 스크롤 배치까지 포함한 최종 컷 산출물이 없다.

따라서 기존 결과는 최종 웹툰 예제가 아니라 이후 파이프라인의 일부를 검증한 기술 실험으로 위치를 낮춘다. OpenPose 매트릭스는 `공간 제어 입력이 바뀌는가`, IP-Adapter 매트릭스는 `참조 이미지가 큰 외형 반복성을 보강하는가`, Blender armature blockout은 `전신 관절과 카메라를 다시 렌더할 수 있는가`만 보여 준다.

## 새 파이프라인 구성에 의미가 있었던 실험

아래 목록은 웹툰 완성 품질을 통과한 사례 목록이 아니다. 실제 실행으로 **다음 파이프라인에서 지켜야 할 입력 계약, 실행 게이트, 검수 방법**을 확정한 실험만 남긴다. 결과 PNG가 없거나 품질이 탈락한 경우에도, 이후에 같은 잘못된 조합을 반복하지 않게 했다면 설계 근거로 유지한다.

| 실험 | 실제로 확인한 사실 | 새 파이프라인에 반영한 결정 | 판정 |
| --- | --- | --- | --- |
| SDXL OpenPose pose·장소·프레이밍 매트릭스 | 같은 인물 서술에서도 관절 지도와 장면 지시를 바꾸면 전신 배치와 화면 크기가 바뀔 수 있었다. 그러나 장소·camera 변화와 함께 얼굴, 머리, 의상, 손의 동일성이 무너졌다. | `pose map`은 인물 정체성의 근거가 아니라 구조 검수용 보조 입력으로만 둔다. OpenPose 단독 생성은 최종 웹툰 컷 경로에서 제외한다. | 구조 제어의 부분 확인, identity 탈락 |
| 같은 조건의 IP-Adapter 추가 비교 | 참조 이미지를 넣으면 단발과 의상 색 같은 큰 외형은 일부 반복됐지만, 얼굴 세부, 후드 배색, 카메라 변화 뒤의 체형은 유지되지 않았다. | identity는 한 장의 reference adapter 효과로 판정하지 않는다. 전신·다각도 face·의상 기준서를 먼저 승인하고, 여러 컷에서 따로 채점한다. | 큰 외형 보강만 확인 |
| Blender blockout -> Canny/ControlNet 생성 비교 | blockout의 포즈와 렌즈·화면 크기 차이는 일부 전달됐지만, Canny만으로는 장소, 인물성, 손·소품 접점을 함께 유지할 수 없었다. | camera·구도는 shot 원본에서 고정하고 생성 모델에는 line/depth 같은 구조 보조 입력을 준다. 구조 제어와 identity·작화 제어를 한 도구의 성공으로 간주하지 않는다. Blender는 생성형 AI의 기본 경로가 아니라 필요할 때 shot 원본을 만드는 보조 도구로 한정한다. | 구조 입력의 부분 확인, 최종 컷 탈락 |
| MotionGPT 보행 및 MotionGPT -> OpenPose -> SDXL 연결 | 관절 좌표의 전진량·보폭 수치는 통과했지만, 사람 검수에서 지지발, 체중 이동, 팔 스윙, 몸통 균형이 부자연스러웠다. 이를 OpenPose로 옮겨도 정체성과 자연스러운 보행은 복구되지 않았다. | 동작 원본은 수치 validator만으로 승인하지 않는다. 사람 눈으로 전신·손목·발 접지·목-머리 방향을 먼저 통과한 driving video 또는 pose sequence만 사용한다. | 동작 품질 게이트 확정 |
| 전신 character 기준 이미지 생성 시도 | SDXL 후보에는 복제 인물 또는 잘린 발이 나타나, 전신 비율·의상·발·crop을 비교할 기준 원본이 없었다. | pose·camera 실험보다 먼저 다각도 전신 character sheet를 승인한다. 승인되지 않은 한 장을 pose transfer의 identity 기준으로 쓰지 않는다. | 기준 자산 선행 게이트 확정 |
| Qwen-Image-Edit-2511 저메모리 실행 | character sheet, target pose·camera 정지 이미지, 장면 지시를 준비했지만 8 GB에서 text encoder 단계의 VRAM 부족으로 PNG를 만들지 못했다. FP8 변형도 해당 모델 구성에서 실행되지 않았다. | 품질 매트릭스 전에 `peak VRAM, 실행 시간, 오류, PNG 저장`을 확인하는 실행 성립 게이트를 둔다. 결과가 없으면 pose·identity 품질을 논하지 않는다. | 8 GB 실행 게이트 탈락 |
| FLUX.2 Klein 4B 공식 CLI 실행 | Qwen3 text encoder 다음에 보조 Mistral 모델을 GPU에 적재하면서 메모리 부족이 발생했고 이미지 생성까지 도달하지 못했다. | 모델 카드의 VRAM 수치만으로 채택하지 않는다. 실제 CLI의 보조 모델과 peak VRAM을 포함해 측정한다. | 8 GB 실행 게이트 탈락 |
| FLUX.1 Kontext dev·JoyAI 저메모리 경로의 가중치 확인 | FLUX.1은 주 가중치만 23.8 GB이며 PNG 전 중단됐다. JoyAI는 최소 약 50.6 GB 다운로드가 필요했다. | VRAM과 별도로 `로컬 디스크·가중치 캐시·재실행 시간`을 채택 조건에 넣는다. 현 환경에서는 대형 reference-edit 모델을 반복 실험 도구로 삼지 않는다. | 운영성 게이트 확정 |

이 실험들이 합쳐서 남긴 결론은 간단하다. 새 경로의 시작점은 `OpenPose`, `LLM`, `Blender rig`, 특정 확산 모델이 아니라 **승인된 character sheet와 shot 원본**이다. 그 뒤에 실행 성립 게이트를 통과한 생성 모델만 붙이고, 구조·identity·화풍·국소 보정을 분리해 네 개의 품질 게이트로 판정한다.

## 핵심 판단

웹툰은 동영상이 아니라 정지 컷의 순서다. 그러므로 사람 동작 영상 모델을 바로 최종 해답으로 두면, 캐릭터 동일성, 컷의 카메라, 말풍선 여백, 배경 연속성을 한 번에 잃기 쉽다. 리깅이나 animation 도구는 최종 동영상을 만들기보다 **전신 pose와 카메라를 재현 가능한 입력으로 고정하는 도구**로 둔다.

상용 서비스와 연구 결과가 보여 주는 안정성은 한 모델이 모든 문제를 푼다는 뜻이 아니라, identity, pose, camera, style, retouch를 분리한 제작 공정의 결과로 해석한다. 이 공정의 구성 요소에는 공개 도구와 공개 연구 구현이 충분히 존재한다. 따라서 Part 7은 `완전 무인 웹툰 생성`을 약속하지 않고, **자체 제작 캐릭터로 4컷 시퀀스를 사람이 승인·보정하며 완성하는 적정 수준의 공개 도구 기반 파이프라인**을 목표로 삼는다.

이 목표에서 가능한 범위와 사람의 작업을 분명히 나눈다.

| 항목 | 공개 도구 기반으로 목표에 포함 | 사람의 승인·보정이 필수인 이유 |
| --- | --- | --- |
| 전신 pose와 카메라 | Blender armature blockout과 pose/line/depth control image | 극단 원근과 가림에서 생성 결과가 구조를 놓칠 수 있음 |
| 얼굴과 표정 | 다각도 face sheet, 참조 adapter 후보, 얼굴·눈 inpaint | 만화식 옆얼굴, 표정, 앞머리는 컷별 기준서 대조가 필요함 |
| 화풍과 색 | style sheet, 고정 checkpoint/adapter, lineart와 색상 보정 | 모델·LoRA·후처리 변경이 누적되면 style drift가 생김 |
| 손·소품·가림 | blockout, 마스크 inpaint, Krita 직접 보정 | 물리적 접촉과 손가락은 작은 오류도 서사를 깨뜨림 |
| 최종 웹툰 읽기 | 레이어 식자, 세로 배열, contact sheet 검수 | 말풍선 여백과 컷 간 호흡은 생성 모델의 품질 지표가 아님 |

즉 공개 도구 경로의 성공 기준은 "생성 결과가 처음부터 완벽하다"가 아니라, 실패가 발생했을 때 어느 기준 원본을 고쳐 다음 컷에도 재사용할 수 있는가다.

생성 AI는 아래 파이프라인에서 두 역할로 제한한다.

- 배경과 캐릭터의 초안 후보를 여러 개 만든다.
- 고정한 전신 pose, 카메라, 마스크 안에서 질감 또는 국소 영역을 보정한다.

인물의 정체성과 컷의 공간 구조는 생성 결과의 우연한 일치에 맡기지 않는다. 캐릭터 기준서, 장면 블로킹 파일, 컷 기록, 최종 검수표가 각각 기준 원본이 된다.

## LLM pose director 경로

`한국어 컷 지시 -> LLM pose DSL -> schema·의미 validator -> pose/camera resolver -> Blender blockout` 경로를 시험했다. 직접 관절 각도를 언어 모델에게 자유 출력하게 하면 작은 LLM에서 예시 값 복사, 존재하지 않는 bone, 행동 의미 불일치가 발생했다. 제한된 enum으로 바꾼 뒤 형식과 카메라 제약은 통과했지만, 표 제시의 손·팔 연결과 보행의 지지·체중 이동이 부자연스러웠다. 따라서 이 구현은 웹툰 포즈 리깅 예제로 채택하지 않으며, 더 적합한 motion/SMPL 모델 또는 검증된 pose transfer 경로를 찾기 전까지 조사 후보로만 유지한다.

재검토할 경로에서 LLM은 최종 그림이나 관절값을 만드는 대신 **콘티의 자연어를 수정 가능한 shot intent로 컴파일**한다. 그 출력에는 prompt, model id, raw response, validation result를 남기되, 실제 움직임은 motion model 또는 driving video가 제안하고 사람이 승인한다. MotionGPT는 text-to-motion을 `(nframe, 22, 3)` motion으로 내보내고, ChatPose는 LLM에서 SMPL parameter를 생성하는 연구이므로, 나중에 더 복잡한 동작 모델을 붙일 때도 같은 검증 경계를 유지한다.

2026-08-01에 공식 `OpenMotionLab/MotionGPT-base`로 `a person walks forward one foot in front of the other`를 GPU에서 생성했다. 고정 seed의 152-frame, 22-joint 출력은 전진 거리와 양 발목의 변화, 반대 위상 보폭이라는 수치 조건은 통과했다. 그러나 keyframe을 사람 눈으로 검토하면 지지발, 체중 이동, 팔 스윙, 몸통 균형이 자연스러운 보행으로 읽히지 않았다. 또한 22관절 전신 skeleton은 손가락, 손목 회전, 팔 비틀림, 소품을 잡는 손의 접점을 표현하지 못한다. **수치 신호와 관절 수만으로 자연스러운 동작을 판정할 수 없다는 실패 사례**로만 기록하며, 실행 코드·관절 배열·contact sheet·실행 기록은 보존하지 않는다. 이 motion은 이후 pose transfer 입력으로도 사용하지 않는다.

### 8 GB GPU의 MotionGPT -> OpenPose ControlNet 연결 실패

MotionGPT 보행 4개 frame을 서로 다른 yaw로 투영해 OpenPose 조건 이미지로 만들고, SDXL + `xinsir/controlnet-openpose-sdxl-1.0`에 동일한 인물 서술과 서로 다른 장소·카메라 지시를 넣었다. `512 x 768`, 24 step에서 일반 CPU offload는 VRAM이 26 MB 부족해 중단됐고, sequential CPU offload로 패널을 분리 생성해 실행 자체는 가능했다. 그러나 결과는 같은 인물이 아니었다. 머리·후드·의상 색이 바뀌고, 한 패널에는 추가 인물이 생겼으며, 걷기 자세도 관절 시퀀스의 지지발·체중 이동을 읽을 수 있는 수준으로 유지되지 않았다.

따라서 이 조합은 `3D motion -> 2D pose map -> 단일 정지 이미지 확산`이라는 연결이 가능함을 보여 주는 기술 확인일 뿐, 웹툰용 pose transfer 성공 사례가 아니다. 참조 기반 identity 제어 또는 개인화 학습 없이 OpenPose만 추가해도 **동일 인물성 게이트를 통과할 수 없음**을 재확인했다. 생성 이미지와 임시 스크립트는 보존하지 않는다. 다음 후보는 기준 캐릭터 이미지와 구동 pose/video를 함께 받는 전용 사람 애니메이션 모델이며, MimicMotion은 이 환경에서 필요한 SVD 가중치가 gated 상태라 실행할 수 없다.

### 기준 캐릭터 초안도 전신 게이트에서 탈락

MimicMotion의 `reference full-body image + DWPose sequence` 입력 계약을 확인한 뒤, SDXL로 자체 제작 전신 캐릭터 기준 이미지 후보 세 장을 만들었다. 두 후보는 하나의 캔버스에 복제 인물이 함께 생성됐고, 나머지 후보는 얼굴·상체는 읽을 수 있었지만 발이 잘렸다. `full body`, `one person only`와 복제·crop 음성 조건을 함께 주어도 이 해상도·base model 조합에서 전신 기준서로 승인할 수 있는 이미지가 나오지 않았다.

따라서 이 결과도 보존하지 않는다. 전신 기준 이미지가 없으면 포즈 트랜스퍼가 출력하더라도 전신 비율, 의상, 발, crop의 일관성을 판정할 기준이 없다. 다음 실행은 먼저 다각도 전신 character sheet를 안정적으로 만들 수 있는 개인화 모델 또는 승인된 자체 제작 원본을 확보한 뒤에만 수행한다.

단일 전신 OpenPose를 먼저 고정한 `512 x 768` SDXL ControlNet 실행에서는 한 명의 전신과 발이 보이는 정면 후보가 생성됐다. 그러나 이 입력은 어깨-팔꿈치-손목까지만 있는 body pose이고 손가락·손바닥·손목 방향을 포함하지 않는다. 정면 한 장의 전신 노출은 다각도 얼굴·손·의상 기준서나 웹툰 캐릭터 일관성을 검증하지 못하며, 이후 pose-transfer 입력 원본으로도 충분하지 않다. 따라서 이 이미지, pose 입력, 실행 코드는 보존하지 않는다.

MimicMotion의 공개 코드는 첫 기준 pose와 뒤이은 DWPose frame을 합친 `image_pose` tensor를 입력으로 받는다. MotionGPT 관절을 이 형식의 `(17, 3, 768, 512)` tensor로 변환하는 사전 검증은 shape·범위·frame 변화를 통과했지만, 원본 보행 자체가 미채택이고 DWPose body map에는 손 관절이 없다. 따라서 변환 코드·contact sheet·압축 tensor·실행 기록도 함께 제거한다. 이후에는 전용 animation model 또는 사람이 승인한 driving video에서 **전신·양손·소품 접점까지 시각 검수를 통과한** 동작을 얻고, 손 keypoint 또는 DensePose/SMPL 계열의 더 풍부한 제어를 함께 쓸 때만 입력 계약을 다시 적용한다.

손바닥과 발바닥은 단순한 추가 joint 하나가 아니라 접촉 면이다. 다만 **균형 판정**에는 모든 손가락 관절이 필요하지 않다. 골반·몸통·머리의 정렬, 고관절·무릎·발목, 뒤꿈치·발볼·발가락의 위치, 발바닥 방향과 프레임별 접지 상태가 우선이다. 팔 자세와 상체 균형 보정에는 어깨·팔꿈치·**손목**이 최소로 필요하다. 손목이 있어야 팔의 길이와 굽힘, 몸통과의 관계, 손이 향하는 방향을 판정할 수 있다.

시선 방향에는 몸통에서 **목을 거쳐 머리로 이어지는 joint chain**이 필요하다. 목 좌표 하나만으로는 부족하며, 몸통-목-머리의 상대 회전 또는 방향 벡터가 있어야 고개를 돌렸는지, 숙였는지, 기울였는지를 판정할 수 있다. 눈을 어디에 두는지가 서사에 중요한 close-up에서는 눈·동공의 gaze vector를 별도 조건과 검수 항목으로 더한다.

손가락 관절과 손바닥 방향은 컵을 쥐기, 손잡이를 당기기, 손가락을 펴 보이기처럼 **손의 국소 작화와 물체 접점**이 서사에 보이는 컷에서 추가한다. 발은 바닥을 디디거나 뛰는 장면에서 뒤꿈치·발볼·발가락과 바닥의 depth 또는 mesh 접촉을 함께 검수한다. 따라서 다음 동작 경로의 기본 계약은 `전신 body pose + foot contact/foot landmark + depth 또는 3D mesh`이고, 손·소품 컷에만 `hand keypoint + palm orientation`을 더한다.

### 동작 컷의 표현을 목적별로 고른다

웹툰의 동작 컷에서는 관절점 수가 많다는 사실만으로 자연스러운 동작이나 캐릭터 일관성이 보장되지 않는다. 관절점은 원본 동작과 생성 후보의 누락을 찾아내는 검수 자료로 쓰고, 최종 컷의 동작 원본은 카메라와 접지 정보를 함께 표현할 수 있어야 한다.

| 표현 | 할 수 있는 일 | 남는 한계 | 이 파이프라인에서의 역할 |
| --- | --- | --- | --- |
| 18/25 body pose | 몸통과 팔다리의 큰 윤곽을 빠르게 비교 | 손목 방향, 발바닥, 머리 회전, 가림을 충분히 표현하지 못함 | 최종 동작 원본으로 사용하지 않음 |
| 전신 2D keypoint | 얼굴, 양손, 발의 누락과 프레임별 위치를 검사 | 2D 좌표만으로는 무게 중심, 발바닥 면, 깊이, 카메라 밖 가림을 판정하지 못함 | driving 영상과 생성 후보의 검수, 보조 조건 |
| SMPL-X 계열 body/face/hand 모델 | 몸·얼굴·손의 3D 매개변수 연구와 비교 | 배포 라이선스가 비상업 연구·교육 등으로 제한되고 모델 배포가 허용되지 않음 | 공개 실습 산출물이 아닌 연구 비교 자료 |
| 자체 제작 Blender rig + IK/mesh | 사람이 만든 정밀 pose·카메라·접지 원본을 만들 수 있음 | 생성형 animation model의 필수 입력도, 일관성 보장 장치도 아님 | 필요할 때만 driving video를 만들거나 생성 결과를 비교하는 보조 도구 |

OpenPose의 전신 출력은 몸·손·얼굴·발을 포함하는 135개 keypoint를 제공하고, MMPose도 133개 whole-body keypoint와 hand/face 추정을 제공한다. 이 정보는 손목, 발, 얼굴 landmark가 빠진 입력을 찾아내는 데 유용하다. 그러나 2D keypoint에는 발바닥의 면이나 몸통-목-머리의 상대 회전, 가려진 손의 깊이가 충분히 들어 있지 않다. 따라서 2D keypoint만으로 통과시키지 않는다.

Blender rig가 생성형 AI 모델의 기본 경로로 적합하다는 검증 사례는 확인하지 못했다. 공개 human image animation 사례는 기준 캐릭터 이미지와 driving video 또는 pose sequence를 모델에 넣고, diffusion motion module이 시간적 움직임을 생성하는 구조다. 따라서 이 책의 기본 경로는 **생성형 모델이 만든 또는 사람이 촬영한 driving video**를 우선으로 하고, Blender는 그 입력을 만들 수 없는 경우의 선택적 보조 도구로만 둔다. 비동작 컷은 이 경로에 종속되지 않고, 표정 중심은 `face-first`, 장소와 구도 중심은 `camera/background-first`로 시작한다.

VNCCS는 character sheet, pose, clothing, emotion을 분리해 sprite를 만드는 MIT 공개 ComfyUI pipeline 후보다. 정지 컷 중심의 웹툰에는 StoryDiffusion처럼 장거리 attention을 한 번에 적용하는 방법보다 이 자산 분리 방식이 더 직접적이다. 다만 현재 P7 실행 환경에는 ComfyUI와 그 모델 묶음이 없으므로, 설치 여부를 검증하기 전에는 기본 예제로 채택하지 않는다.

## 네 개의 독립 품질 게이트

아래 네 과제는 한 설정값의 문제가 아니다. 각 컷은 네 게이트를 각각 통과해야 하며, 한 게이트의 통과를 다른 게이트의 통과로 대신하지 않는다.

| 품질 게이트 | 고정할 원본 | 생성 단계에서 쓰는 제어 | 사람이 확인할 결과 | 이 게이트만으로 해결되지 않는 것 |
| --- | --- | --- | --- | --- |
| 포즈·동작 | 기준 캐릭터 전신 sheet와 사람 검수를 통과한 driving video 또는 pose sequence | pose-guided human image animation model의 motion·pose·face 조건 | 지지발, 체중, 손·발, 목·머리 방향, 가림이 콘티와 맞음 | 얼굴 세부, 화풍 |
| 페이스 일관성 | 정면·반측면·측면 얼굴 sheet와 표정 sheet | 캐릭터 LoRA 또는 참조 adapter, 얼굴 마스크 inpaint | 눈 간격, 눈썹, 앞머리, 얼굴형, 표정이 각도별 기준과 맞음 | 전신 pose, 배경 |
| 화풍 일관성 | 선 굵기, 채색, 명암, 색상 팔레트, 금지 질감이 있는 style sheet | 고정 checkpoint/LoRA, lineart 제어, 색상 보정 레이어 | 네 컷의 선, 피부·의상 채색, 광원 해석이 같은 작품처럼 보임 | 같은 인물의 보장 |
| 다이내믹 카메라 | shot별 구도 기준 이미지, driving video frame, lens·높이·방향 기록 | video-to-video 또는 pose/depth/line 조건을 받는 생성 모델 | wide, low angle, 3/4, close-up 전환이 공간·전신 pose와 모순되지 않음 | 얼굴·손의 세부 완성 |

### 포즈 리깅: `그림을 움직이는 일`보다 `전신을 끝까지 설계하는 일`

전신 pose를 먼저 만드는 방식은 신체 접촉, 걷기, 강한 원근처럼 몸 전체의 관계가 핵심인 컷에서 유리하다. 이 분기에서는 인물을 전신으로 pose를 확정하고 이후 카메라가 crop한다. 그러나 얼굴 반응, 대화, 장소 소개는 각각 face-first, camera/background-first로 시작할 수 있으며, 모든 컷에 전신 pose-first를 강제하지 않는다.

- **반복 동작**: 정면·반정면의 팔 들기, 걷기, 고개 돌림은 2D part와 bone/mesh를 재사용한다. `joint anchor`, `part mask`, `draw order`가 기록 원본이다.
- **회전·가림·원근 동작**: 팔이 몸 뒤로 가거나 카메라가 아래에서 올려다보는 컷은 driving video 또는 pose sequence에서 먼저 자연스럽게 성립해야 한다. diffusion animation의 frame은 후보이며, Blender blockout은 그 입력을 별도로 만들어야 할 때만 쓴다.
- **실패 판정**: "손이 그럴듯하다"가 아니라, 손의 주인이 되는 팔과 어깨, 체중을 받는 발, 소품을 잡는 방향이 blockout과 맞는지를 본다.

### 페이스 일관성: 얼굴을 전신의 부수 효과로 두지 않는다

얼굴은 정면 한 장이 아니라 각도와 표정을 포함한 별도 자산이다. 최소한 정면, 좌·우 반측면, 측면, 위·아래 시선, 기본·웃음·놀람·분노 표정을 기준서로 만든다. 눈동자 색, 눈꼬리, 눈썹, 앞머리 갈래, 귀·액세서리 위치처럼 컷에서 검수 가능한 항목을 표시한다.

FaceID IP-Adapter와 InstantID는 얼굴 이미지 또는 embedding을 조건으로 쓰는 공개 연구·구현 후보다. IP-Adapter 저장소는 SDXL용 FaceID 계열을 안내하고, InstantID는 얼굴 embedding과 landmark 조건을 함께 사용한다. 그러나 이러한 adapter는 **후보 생성의 보조 신호**로만 둔다. 만화식 얼굴의 옆모습, 큰 표정 변화, 가림을 자동 보증하지 않으며, 필요한 얼굴 분석 모델과 가중치의 사용 조건도 별도로 확인해야 한다.

따라서 실제 통과 기준은 adapter를 사용했는지가 아니라 다음이다.

1. 컷의 얼굴 각도가 기준서의 어느 view에 해당하는지 기록되어 있는가?
2. 눈, 앞머리, 얼굴형, 귀·액세서리가 그 view의 기준과 맞는가?
3. 표정만 고칠 때 의상, 머리 윤곽, 카메라가 마스크 밖에서 변하지 않았는가?
4. 통과하지 못하면 얼굴을 다시 전체 생성하지 않고 얼굴·눈·앞머리 마스크로 수정할 수 있는가?

### 화풍 일관성: prompt가 아니라 렌더 계약을 고정한다

`anime style`처럼 넓은 prompt는 화풍 기준이 될 수 없다. style sheet에는 최소한 외곽선의 굵기 범위, 그림자 단계 수, 피부·머리·의상 팔레트, 하이라이트 위치, 배경 detail 밀도, 금지 질감을 이미지와 짧은 문장으로 정한다. 모든 컷에 같은 checkpoint, 스타일 LoRA, VAE, lineart 처리, 색상 보정 레이어를 적용하고 변경값을 기록한다.

화풍이 흔들리면 우선 `모델·LoRA·VAE·lineart 입력·색상 보정` 중 무엇이 바뀌었는지 비교한다. 한 컷의 예쁜 렌더를 선택하는 것이 아니라, contact sheet에서 선 굵기, 그림자, 팔레트가 같은 기준을 만족하는지를 판정한다. 캐릭터 특징이 같더라도 사실적 피부 질감이나 다른 선화가 섞이면 화풍 게이트는 실패다.

### 다이내믹 카메라: 카메라 prompt가 아니라 shot 데이터로 제어한다

`low angle`, `wide shot` 같은 prompt만으로는 인물과 배경의 공간 관계를 재현할 수 없다. 카메라가 바뀌는 컷에는 driving frame 또는 구도 기준 이미지와 함께 아래 shot 데이터를 남긴다.

```text
shot_id:
camera_type: eye_level | low_angle | high_angle | over_shoulder
focal_length_mm:
camera_height:
camera_yaw_pitch_roll:
camera_target:
character_full_body_pose:
crop_after_full_body_render:
control_outputs: driving_video | pose | face | depth | lineart
```

공개 animation 모델은 driving video와 pose/depth/face 조건을 받는 경로를 제공한다. 따라서 카메라가 바뀐 동작은 우선 그 구도가 실제로 담긴 driving frame 또는 생성 모델의 후보 영상에서 고른다. Blender의 camera rig는 그 기준 영상을 직접 만들 수 없을 때의 대체 수단일 뿐이다. 이 기록은 극단적인 lens나 자세에서 생성 결과가 못 따라올 때, driving 원본·조건·생성 표현 중 어느 쪽을 고칠지 분리한다.

## 추가 조사: 자연스러운 동작과 정지 컷을 분리하는 공개 도구 경로

2026-08-01에 공식 저장소와 논문을 다시 확인했다. 결론은 `한 장의 캐릭터 그림 + LLM 관절 DSL`보다, 검증된 동작 시퀀스나 driving video를 먼저 만들고 그 안에서 웹툰 컷 후보를 고르는 경로가 자연스러운 걷기·접촉·체중 이동에 더 적합하다는 것이다. 다만 영상 모델의 한 frame을 그대로 완성 컷으로 채택하지 않는다. 선택한 frame은 character sheet, 카메라·배경 원본, 손·소품 마스크의 별도 검수를 다시 통과해야 한다.

| 후보 | 확인한 기능 | 이 파이프라인에서 맡길 역할 | 현재 판단 |
| --- | --- | --- | --- |
| [Wan2.2 Wan-Animate](https://github.com/Wan-Video/Wan2.2) | reference character image와 pose·face video를 받아 animation 또는 replacement video를 생성한다. 공식 Diffusers 예시는 `Wan2.2-Animate-14B`를 사용한다. | 사람이 준비하거나 motion 모델이 만든 driving video에서 자연스러운 동작 후보를 만들고 keyframe을 고르는 단계 | 자연스러운 동작 후보로 가장 직접적이다. 다만 14B 모델과 전처리·영상 입력이 필요하므로 현재 8 GB 환경의 기본 실습에는 채택하지 않는다. |
| [Index-AniSora](https://github.com/bilibili/index-anisora) | 공식 저장소는 pose, depth, line art, audio guidance와 character 3D video generation을 제시하며, V3.1의 12 GB VRAM 가능 배포를 안내한다. | 만화·애니메이션 화풍의 동작 후보와 다각도 기준 영상 탐색 | Apache-2.0 코드·가중치 배포는 긍정적이나 현재 8 GB보다 큰 실행 조건이 필요하다. 다음 GPU 환경에서 우선 검증할 후보다. |
| [LTX-Video](https://github.com/Lightricks/ltx-video) | image-to-video, 여러 keyframe, style LoRA를 지원한다. pose/depth/Canny 제어 모델은 공식 저장소에서 13B 계열로 제시한다. | 고정한 keyframe 사이의 짧은 동작 또는 전환 후보 | 2B distilled는 가벼운 영상 초안 후보지만, 확인한 pose 제어는 13B 계열이다. 현재 장비에서 자연스러운 pose 해법으로 단정하지 않는다. |
| [AnimateDiff + ControlNet](https://huggingface.co/docs/diffusers/api/pipelines/animatediff) | 개인화한 SD 1.5 계열 모델에 motion adapter를 결합하고, video-to-video ControlNet에서 원본 video와 control image sequence를 함께 조건으로 받을 수 있다. | character LoRA와 driving video/pose·depth 조건을 결합해 짧은 동작 후보를 생성 | 공개 문서와 재현 가능한 API가 있어 현재 장비에서 우선 검증할 생성형 AI 후보다. 다만 자연스러운 보행과 얼굴·손의 일관성은 실제 결과로 별도 통과해야 한다. |
| [MusePose](https://github.com/TMElyralab/MusePose) | 기준 인물 이미지와 pose sequence로 virtual human video를 생성하며, pose alignment를 제공한다. | reference character에서 pose-transfer 동작 후보를 만드는 비교 대상 | 공개 pose-driven 구현이지만 현재 실습 장비에서의 메모리·만화 화풍·인물성 품질을 아직 검증하지 않았다. |
| [X-Dyna](https://github.com/bytedance/x-dyna) | 기준 이미지, driving video, pose 및 얼굴 제어를 diffusion 기반 animation에 결합한다. | 자연스러운 동작·표정·배경 동역학의 상한을 판단하는 비교 연구 | 공식 저장소가 16 frame에 최소 20 GB VRAM을 명시하므로, 현재 8 GB 장비의 실행 후보에서는 제외한다. |
| [CharaConsist](https://github.com/Murray-Wang/CharaConsist) | FLUX.1 기반의 training-free foreground 일관성과 선택적 background 보존을 목표로 하며, 고정·변경 배경과 story generation 예제를 제공한다. | 정지 컷에서 캐릭터와 배경의 반복성을 검수할 후보 | pose/동작 생성기는 아니다. 동작 후보에서 선택한 컷을 다시 정지 이미지로 정리할 때만 별도 검토한다. FLUX.1과 실행 메모리·가중치 사용 조건을 먼저 확인해야 한다. |
| [ComfyUI VNCCS](https://github.com/AHEKOT/ComfyUI_VNCCS) | 캐릭터, 의상, 감정, sprite, 선택적 LoRA dataset 생성을 단계로 나누며 full-body 기준 이미지를 권장한다. | character sheet와 의상·표정 자산의 후보 생성 및 정리 | 정지 컷의 정체성 기준서를 만드는 보조 도구다. 저장소도 pose preset과 model별 표정 안정성이 완성되지 않았다고 적으므로, 자연스러운 동작 해법으로 쓰지 않는다. |
| [MotionGPT](https://github.com/OpenMotionLab/MotionGPT) 및 [ChatPose](https://yfeng95.github.io/ChatPose/) | MotionGPT는 텍스트에서 연속 3D motion을 생성하는 motion-language 모델이고, ChatPose는 text/image에서 SMPL pose parameter를 생성하는 연구 경로다. | LLM 지시를 관절 enum이 아니라 motion 또는 SMPL 후보로 바꾸는 연구용 전단 | 자연스러운 동작 문제와 직접 맞닿아 있으나, SMPL/데이터/추론 환경과 라이선스를 별도 확인해야 한다. 바로 책의 실행 예제로 채택하지 않는다. |

### 현재 장비에서의 생성 모델 우선순위

현재 GPU는 8 GB VRAM이며, `diffusers 0.37.0`과 `accelerate`는 설치되어 있다. SD 1.5 base model의 전체 snapshot 다운로드는 여러 정밀도 파일까지 받아 2026-08-01 현재 완료되지 않았고, motion adapter와 SD 1.5 OpenPose ControlNet은 아직 캐시에 없다. 다음 실행 준비는 전체 snapshot이 아니라 필요한 fp16 safetensors와 설정 파일만 받도록 제한해야 한다. `animatediff-motion-adapter-v1-5-2`의 fp16 가중치만 약 1.82 GB이므로, 첫 실행은 CPU offload와 VAE slicing을 사용한 작은 해상도·8 frame의 **실행 가능성 시험**으로 한정한다. 이 시험은 자연스러운 웹툰 동작이나 캐릭터 일관성의 예시가 아니며, 그 판정은 뒤이은 실제 contact sheet에서만 한다.

실행 순서는 `기준 캐릭터 이미지 또는 character LoRA -> 짧은 driving video -> pose/depth/face 조건 -> AnimateDiff video-to-video 후보 -> 통과 frame의 정지 컷 보정`이다. 이 순서에서 Blender는 필수 단계가 아니다. 모델이 받아들이는 pose sequence가 필요하지만 촬영 driving video가 없을 때에만, 별도의 제작 보조 도구로 고려한다.

### AnimateDiff 단독 prompt 실행 결과: 미채택

2026-08-01에 SD 1.5 base와 `animatediff-motion-adapter-v1-5-2`를 CPU offload, VAE slicing, attention slicing으로 실행했다. `256 x 384`, 8 frame에서 GPU peak allocation은 약 2.9 GB였고, 6 step은 3.6초, 20 step은 8.9초였다. 따라서 현재 8 GB GPU에서 짧은 AnimateDiff 실행 자체는 가능하다.

그러나 같은 seed와 "전신 만화 캐릭터가 역 플랫폼을 걷는다"는 prompt에서 6 step 결과는 인물·보행·공간을 판독할 수 없었고, 20 step 결과도 사람 대신 역 플랫폼 배경이 대부분을 차지했다. 프레임 간 배경은 변했지만 전신 인물, 지지발, 손목, 목-머리 방향, 캐릭터 정체성은 검증할 수 없었다. 이 결과 이미지와 실행 코드는 보존하지 않는다.

이 실패는 AnimateDiff의 실행 가능성을 웹툰용 동작 생성 가능성으로 확대 해석할 수 없음을 확인한다. 다음 검증은 prompt만으로 걷기를 요구하지 않고, 사람 검수를 통과한 driving video와 기준 캐릭터 이미지, 그리고 pose/face/depth 조건을 함께 넣는 경로여야 한다. 단순 OpenPose 막대 그림만 다시 넣는 실험은 앞선 실패의 반복이므로 채택하지 않는다.

### 실제 driving video의 OpenPose 변환 결과: 입력 계약 미달

MimicMotion 공식 저장소의 전신 dance driving video에서 8개 frame을 뽑아 `controlnet-aux` OpenPose의 `detect_hand=True`, `detect_face=True`로 변환했다. 원본 영상에는 전신, 손목, 발, 머리와 동작 변화가 분명히 보인다. 변환 map에는 어깨-팔꿈치-손목과 다리의 큰 윤곽은 잡혔지만, 작은 해상도에서 손·손가락과 얼굴 landmark는 실질적으로 나타나지 않았다. 발도 발목-발끝 수준의 선뿐이어서 heel/toe 접지 면이나 바닥과의 깊이를 표현하지 못한다.

따라서 이 입력은 원본 영상의 자연스러운 동작을 보존한 **출발 자료**일 뿐, 웹툰 동작 컷의 최종 조건은 아니다. 이 map만으로 AnimateDiff ControlNet 생성은 실행하지 않았다. 다음 후보는 whole-body hand/face detector와 depth 또는 video-to-video 원본을 함께 쓰는 경로이며, 그 결과가 손목·목-머리 방향·발 접지·카메라 변화를 실제로 유지하는지를 먼저 판정해야 한다. 원본 video와 contact sheet, 변환 script는 제3자 인물·미채택 조건이므로 보존하지 않는다.

### OpenPose와 생성형 영상의 결합 사례

OpenPose를 영상 생성에 쓰는 공개 사례는 존재한다. 다만 사례의 공통점은 OpenPose를 최종 인물 표현이나 유일한 동작 원본으로 쓰지 않는다는 것이다.

| 사례 | OpenPose 또는 pose의 역할 | 함께 쓰는 조건 | 웹툰 파이프라인에서의 판단 |
| --- | --- | --- | --- |
| AnimateDiff video-to-video + ControlNet | 원본 video frame과 같은 길이의 OpenPose control image sequence로 공간 윤곽을 조건화 | motion adapter, 원본 video, SD 1.5 계열 checkpoint, 필요 시 character LoRA | 현재 8 GB 환경에서 짧은 실행을 검증할 수 있는 조립식 경로다. OpenPose는 pose 윤곽만 담당하므로 identity·얼굴·손 품질을 별도 조건과 검수로 더해야 한다. |
| ControlVideo | human pose, Canny, depth 같은 ControlNet 조건을 video frame sequence에 적용하고 시간 smoothing을 더함 | 원본 condition video, Stable Diffusion, ControlNet, RIFE | 시간 일관성을 위한 초기 공개 사례다. 기준 캐릭터 identity 경로가 없으므로 웹툰 인물 일관성의 단독 해법은 아니다. |
| MimicMotion | DWPose 기반 confidence-aware pose guidance로 reference image의 인물을 driving motion에 맞춤 | reference image, driving video, Stable Video Diffusion 계열, DWPose | pose map보다 기준 인물 reference가 앞선다는 점이 중요하다. 현재 SVD 접근이 gated이고 DWPose의 손·발·얼굴 품질은 별도 검증이 필요하다. |
| MusePose | reference image와 dance video의 DWPose를 pose alignment한 뒤 image-to-video 생성 | reference image, aligned pose sequence, reference UNet, pose guider | arbitrary dance video를 reference image에 맞추는 alignment를 제공한다. 그러나 공식 한계가 얼굴·복잡 의상 세부 보존과 복잡 배경 flicker를 명시하고, trained model은 비상업 연구 전용이다. |
| X-Dyna | body pose ControlNet으로 동작을 조건화 | reference appearance adapter, driving video, 별도 local face control, motion module | pose만으로 부족한 얼굴·정체성 문제를 별도 모듈로 보완한 사례다. 최소 20 GB VRAM이라 현재 장비에서 실행하지 않는다. |

이 사례들은 다음 경계를 뒷받침한다.

1. **OpenPose는 공간 조건이다.** 팔·다리 위치를 붙잡을 수 있지만 동일 인물, 의상, 화풍, 손의 물체 접점, 발바닥 면, 3D 가림을 보장하지 않는다.
2. **driving video는 시간 조건이다.** 자연스러운 체중 이동과 타이밍을 제공하지만, 원본 인물·배경·카메라를 그대로 가져오는 위험이 있으므로 reference identity와 scene 조건을 분리해야 한다.
3. **identity와 face는 별도 조건이다.** character LoRA 또는 다각도 reference, 얼굴 전용 조건, 국소 inpaint 없이는 OpenPose video 제어만으로 웹툰 캐릭터를 고정할 수 없다.
4. **카메라는 pose map에 들어 있지 않다.** driving frame의 실제 구도, video-to-video 입력, 또는 별도 depth/line/reference를 shot 계약으로 기록해야 한다.

따라서 다음 유효 실험 단위는 `LLM shot intent -> 기준 캐릭터 LoRA 또는 다각도 reference -> 사람 검수 driving video -> pose + face + 원본 video 조건 -> 후보 frame 선택 -> 손·얼굴·머리카락 inpaint -> 서로 다른 장소·카메라의 정지 컷 검수`다. OpenPose는 이 묶음의 한 입력일 뿐, 앞단의 LLM 지시나 최종 웹툰 컷을 대체하지 않는다.

### AnimateDiff video-to-video + OpenPose 실행 결과: 미채택

실제 전신 driving video의 8개 연속 frame과 그 OpenPose map을 함께 넣어 `AnimateDiffVideoToVideoControlNetPipeline`을 실행했다. `256 x 384`, 8 frame, 10 step, `strength=0.45`, ControlNet scale `0.8`에서 약 9.7초, GPU peak allocation 약 4.7 GB로 실행됐다. 즉, 현재 8 GB GPU에서 이 조합의 짧은 추론은 가능하다.

그러나 생성 frame은 원본의 큰 팔 방향과 실내 배경 색 일부만 유지했다. 얼굴이 흐려지거나 변형됐고, 일부 frame은 전신이 잘렸으며 손·발과 의상 경계도 안정적이지 않았다. 후반 frame에서는 인체 형태와 배경 선이 더 크게 붕괴했다. 이는 원본 video와 OpenPose를 함께 넣어도 `전신 pose 유지`, `인물 정체성`, `손·발·얼굴의 국소 품질`, `웹툰 화풍`을 동시에 충족하지 못함을 보여 준다.

이 실험에는 character LoRA나 자체 제작 reference가 없었으므로 캐릭터 일관성 시험은 아니었다. 그럼에도 동작·전신 게이트부터 통과하지 못했으므로, 결과를 웹툰 예제나 다음 단계의 기준 asset으로 채택하지 않는다. 제3자 driving video와 생성 contact sheet, 실행 script는 삭제한다. 다음 실험은 character identity asset을 먼저 확정한 뒤, pose map 외의 face/hand/depth 조건이 실제로 유지되는 모델을 비교하는 방식이어야 한다.

### Animagine XL 정지 identity와 OpenPose 결합 결과: 미채택

`cagliostrolab/animagine-xl-4.0`으로 자체 제작한 전신 만화 캐릭터 후보를 만들었다. `768 x 1152`, 28 step에서 두 후보 중 한 장은 짧은 청록색 단발, 흰 상의와 짙은 재킷, 청록색 바지, 흰 운동화가 보이는 깨끗한 정면 전신으로 나왔다. 이는 이후 기준서의 **초안 후보**로 검토할 품질이지만, 정면 한 장이므로 얼굴 각도·표정·의상 후면·다른 카메라의 동일성을 증명하지 못한다. character sheet나 본문 예제로 보존하지 않는다.

이 후보를 SDXL image-to-image의 초기 이미지로 두고 3/4 및 보행 지시를 두 강도에서 생성했다. 낮은 강도에서는 머리·얼굴·의상은 거의 유지됐지만 자세도 정면 서기에 머물렀다. 높은 강도에서도 유의미한 3/4 또는 보행 자세가 만들어지지 않았고, 얼굴 특징은 오히려 조금 흔들렸다. 따라서 image-to-image만으로는 identity와 pose/camera를 동시에 고정할 수 없었다.

이어 동일 기준 이미지와 실제 driving video에서 얻은 OpenPose map을 `xinsir/controlnet-openpose-sdxl-1.0`에 함께 넣었다. 일반 CPU offload에서는 `768 x 1152`와 `512 x 768` 모두 SDXL UNet과 ControlNet의 동시 상주로 GPU 메모리 부족이 발생했다. `512 x 768`, 15 step에서 VAE slicing/tiling과 sequential CPU offload를 쓰면 13.4초에 실행됐고 PyTorch가 보고한 GPU peak allocation은 약 664 MB였다. 그러나 출력은 기준 캐릭터의 헤어·의상은 대체로 유지한 정면 서기였으며, 입력 map의 들어 올린 팔과 비대칭 다리 자세를 거의 반영하지 않았다.

즉 순차 offload는 현재 8 GB 장비에서 이 결합의 **실행 가능성**만 해결한다. pose transfer 품질, 얼굴·손·발, 카메라 변화는 해결하지 못했으므로 이 결과를 웹툰 컷이나 포즈 트랜스퍼 성공 사례로 채택하지 않는다. 생성 이미지와 실행 script는 삭제하고, 다음 비교에서는 다각도·표정 기준서 또는 character LoRA와 whole-body pose/face/depth 조건을 함께 받는 전용 human animation 경로를 검증해야 한다.

### 다음 실행 준비: IP-Adapter와 OpenPose의 병렬 조건 비교

다음 실행은 앞선 `img2img 초기 이미지 + OpenPose`를 반복하지 않는다. 초기 이미지는 원본 pose를 정면 서기로 끌어당기는 강한 조건이었으므로, 같은 정지 기준 이미지를 **IP-Adapter reference**로만 넣고 OpenPose는 별도 ControlNet 조건으로 넣는다. 현재 캐시에는 SDXL용 `h94/IP-Adapter`와 `xinsir/controlnet-openpose-sdxl-1.0`이 모두 있으므로, 이 비교 자체에는 추가 모델 다운로드가 필요 없다.

실험 입력은 자체 생성한 전신 기준 후보 한 장과, 사람 검수를 통과한 짧은 driving video에서 고른 한 frame의 OpenPose map이다. 기준 후보의 화면 비율, seed, prompt와 negative prompt를 기록하고, target pose는 몸통과 양 팔·다리의 비대칭이 뚜렷하며 전신과 발이 화면 안에 들어온 frame으로 고정한다. 기준 캐릭터와 target pose를 매 실행에 다시 만들지 않아야 조건 강도만 비교할 수 있다.

| 비교 축 | 고정값 | 바꿀 값 | 판정 질문 |
| --- | --- | --- | --- |
| identity 조건 | 같은 기준 이미지, checkpoint, prompt, seed | IP-Adapter scale `0.45`, `0.70` | 단발, 얼굴형, 재킷·바지·신발의 식별 특징이 남는가? |
| pose 조건 | 같은 OpenPose map, 해상도, sampler | ControlNet scale `0.80`, `1.10` | 든 팔, 골반 기울기, 두 다리의 비대칭, 전신 crop이 map과 맞는가? |
| 실행 조건 | `512 x 768`, 15 step, sequential CPU offload | 두 scale의 조합 4개 | 8 GB에서 실행 시간과 GPU 사용량이 반복 가능한가? |

생성 결과는 네 장을 한 contact sheet로만 비교한다. 다음을 모두 만족하는 후보가 하나라도 있을 때만 다음 단계로 간다: (1) 기준 캐릭터의 머리·얼굴·의상 식별 특징을 사람이 같은 인물로 판정할 것, (2) target pose의 든 팔과 비대칭 지지 자세가 명확할 것, (3) 전신과 양발이 잘리지 않을 것, (4) 손가락·발 접지·시선이 아직 불완전하더라도 그 실패 영역이 식별 가능할 것. 어느 조합도 (1)과 (2)를 동시에 통과하지 못하면 scale을 더 넓히지 않고 이 조립식 SDXL 경로를 중단한다.

이 비교가 부분 통과하면 다음 실험은 한 컷의 성공을 확대하지 않고, 같은 캐릭터의 3/4 pose와 다른 장소·카메라 한 장을 추가한다. 두 번째 컷까지 identity와 pose가 유지될 때에만 얼굴·손 inpaint와 camera/depth 조건을 추가한다. 첫 비교가 실패하면 현재 8 GB 환경의 다음 생성 실험은 중단하고, 다각도 character sheet/LoRA 데이터 준비와 16 GB 이상 전용 human animation 모델 검증으로 작업을 옮긴다.

#### 병렬 조건 비교 실행 결과: 부분 통과

2026-08-01에 위 네 조합을 실제로 실행했다. 사람 검수로 고른 driving video의 frame 24는 양팔을 좌우로 벌린 전신 자세이며, OpenPose map도 이 큰 윤곽을 보존했다. `512 x 768`, 15 step, sequential CPU offload에서 각 2개 조합은 43.7초와 44.2초에 끝났고, PyTorch가 보고한 GPU peak allocation은 약 664 MB였다. 따라서 SDXL, IP-Adapter, OpenPose ControlNet의 병렬 조건은 현재 8 GB GPU에서 반복 실행할 수 있다.

네 출력은 모두 청록색 단발, 청록색 바지, 흰 신발 등 기준 이미지의 큰 식별 특징을 유지했고, 양팔을 벌린 자세와 전신 framing도 따랐다. 특히 `IP 0.45 / pose 1.10`은 얼굴·머리·바지와 팔의 큰 구조가 함께 남아 이 제한된 비교에서는 가장 읽기 쉬운 후보였다. 이 비교 출력은 최종 웹툰 컷 품질을 통과하지 못해 PNG를 폐기하고 판단 기록만 남겼다.

그러나 이것은 웹툰 컷 품질의 통과가 아니다. 기준 이미지에 없던 재킷·소매 형태가 출력마다 바뀌고, 손가락·손목 방향은 판독하기 어렵다. target pose도 걷기나 접지 이동이 아닌 정적인 팔 벌림이며, 얼굴의 미세한 동일성, 시선, 3/4 view, 다른 배경·카메라는 아직 시험하지 않았다. 따라서 이 결과는 **OpenPose와 참조 identity를 분리하면 큰 pose와 외형을 동시에 일부 붙잡을 수 있다**는 채택 가능한 중간 결과로만 둔다. 다음 실행은 이 조합의 가장 읽기 쉬운 scale을 고정하고, 같은 캐릭터의 3/4 전신 pose와 다른 장소 한 컷을 만들어 두 컷에서 identity와 pose가 함께 유지되는지 확인한다.

### 다음 방안: 두 컷에서 identity, pose, camera를 분리 검증

앞선 부분 통과의 고정 조건은 `IP-Adapter 0.45`, `OpenPose ControlNet 1.10`, `512 x 768`, 15 step, sequential CPU offload다. 이 수치를 다시 탐색하지 않는다. 다음 실험의 질문은 "한 장에서 팔 pose가 되는가"가 아니라 **같은 기준 캐릭터가 다른 장소와 3/4 camera에서도 같은 인물·다른 동작으로 읽히는가**다.

먼저 현재 한 장뿐인 identity reference를 기준서로 승격하지 않는다. 정면, 좌·우 3/4 전신, 얼굴 close-up, 의상 앞·뒤를 포함한 자체 제작 character sheet를 별도로 승인한다. 청록색 단발과 흰 hair clip, 얼굴형·눈, 짙은 재킷, 흰 상의, 청록색 바지, 흰 신발을 관찰 항목으로 고정하고, 재킷 소매·길이, 바지 폭, clip 위치가 바뀌면 identity 게이트 실패로 기록한다. 앞선 출력에서 이미 이 의상 drift가 보였으므로, sheet가 없는 상태에서 두 번째 컷을 추가해도 성공으로 해석하지 않는다.

| 컷 | 고정할 조건 | 새로 추가할 조건 | 통과 기준 |
| --- | --- | --- | --- |
| A: 검증 기준 컷 | 승인한 character sheet, 위 scale, 양팔이 보이는 전신 pose | 장소 A, 눈높이 정면 | 기준 머리·의상과 큰 팔 pose가 함께 남고 전신이 잘리지 않음 |
| B: 카메라 검증 컷 | 같은 character sheet, 같은 scale, 같은 seed 기록 규칙 | 실제 3/4 driving frame에서 얻은 body pose와 depth 또는 line 조건, 장소 B | 얼굴·어깨·골반이 같은 방향으로 3/4를 이루고, 장소 A와 다른 배경에서도 의상·얼굴이 같은 인물로 읽힘 |

OpenPose는 2D 관절 위치이므로 camera yaw, 렌즈, 몸통의 깊이, 가림을 표현하지 못한다. 따라서 B에는 3/4 구도가 실제로 담긴 driving frame을 먼저 사람 검수로 승인하고, 그 frame에서 얻은 pose 외에 depth 또는 line control image를 추가한다. OpenPose map만 3/4처럼 보이게 수정하거나 prompt에 `three-quarter`만 넣는 방법은 카메라 검증으로 인정하지 않는다. depth/line 조건을 추가한 뒤 8 GB에서 실행되지 않으면, 그 사실도 결과로 기록하고 다중 ControlNet을 억지로 축소하지 않는다.

실행 전에는 다음 기록 묶음을 준비한다.

```text
character-sheet-revision:
panel-A/B-shot-intent:
panel-A/B-driving-frame:
panel-A/B-pose-map:
panel-B-depth-or-line-map:
ip-adapter-reference-images:
checkpoint/controlnet/ip-adapter revisions:
ip_adapter_scale: 0.45
openpose_scale: 1.10
seed, resolution, step, offload mode:
```

두 컷을 나란히 놓고 다음 네 질문에 모두 "예"라고 답할 때만 다음 단계인 얼굴·손 inpaint로 간다: (1) clip, 머리, 얼굴, 재킷, 바지, 신발이 같은 기준서의 인물인가, (2) 각 컷의 팔·다리·전신 crop이 driving 입력과 맞는가, (3) B가 정면을 단순히 옆으로 밀어 놓은 그림이 아니라 3/4 camera와 장소 B의 공간을 읽히게 하는가, (4) 손·발·눈의 실패 위치가 식별 가능한가. 하나라도 아니면 두 컷 예제와 본문 자산으로 채택하지 않고, 실패 원인을 character sheet, pose/depth 입력, identity adapter 중 어디에 있는지 분리한다.

### 다음 대안: character LoRA를 중심으로 경로를 분리한다

두 컷 비교에서 재킷·얼굴·의상 identity가 계속 흔들리면, 참조 이미지를 더 강하게 넣는 대신 **자체 제작 character LoRA**로 identity를 base model에 추가 학습하는 경로로 옮긴다. LoRA는 원래 모델 전체를 다시 학습하지 않고 작은 adapter만 학습하는 방식이며, Diffusers는 SDXL을 포함한 text-to-image와 DreamBooth LoRA 예제를 제공한다. 그러나 `kohya_ss`의 SDXL LoRA 가이드는 최소 12 GB GPU를 권장한다. 따라서 현재 8 GB GPU에서 SDXL/Animagine 기반 LoRA 학습을 기본안으로 두지 않는다.

| 대안 | 필요한 입력과 장비 | 먼저 검증할 산출물 | 채택/중단 기준 |
| --- | --- | --- | --- |
| A. 12 GB 이상 character LoRA | 권리가 명확한 16-32장의 character sheet, caption, trigger token, SDXL 계열 base | 정면·좌/우 3/4·다른 장소의 4장 identity contact sheet | 모든 view에서 얼굴·hair clip·재킷·바지·신발이 기준서와 맞을 때만 OpenPose/depth와 결합 |
| B. 현재 8 GB의 SD 1.5 LoRA feasibility | 같은 dataset을 512 계열로 축소한 복사본, batch 1, gradient checkpointing/CPU offload 여부 기록 | 학습이 중단 없이 끝나는가, trigger token으로 기준 특징이 재생되는가 | 실행 가능성만 확인한다. 3/4 전신의 detail과 화풍이 기준서보다 약하면 최종 웹툰 경로로 승격하지 않음 |
| C. 16 GB 이상 human animation | A를 통과한 LoRA 또는 다각도 reference, 사람 검수 driving video, pose/face/depth | 16 frame의 전신 pose transfer와 keyframe contact sheet | 지지발·손목·목-머리 방향이 연속 frame에서 유지될 때만 정지 컷 후보로 사용 |

대안 A의 dataset은 한 장의 생성 이미지를 증식해 만들지 않는다. 같은 캐릭터의 정면·3/4·측면·후면, 표정, 전신·허리 위, 주요 의상·소품을 사람이 개별 승인한 원본으로 구성한다. 각 caption은 공통 trigger token과 관찰 가능한 특징을 포함하되, pose·장소·camera는 image마다 다르게 기록한다. 그래야 LoRA가 "청록색 단발의 특정 캐릭터"를 배우고, 모든 pose를 정면 서기로 외우는 것을 피할 수 있다. 학습 후에는 training image와 같은 구도를 재생한 한 장이 아니라, 보지 않은 3/4 pose와 다른 장소에서 identity가 유지되는지를 먼저 검수한다.

대안 B는 최종 품질 우회로가 아니라 학습 파이프라인의 작동 여부를 확인하는 제한된 실험이다. SD 1.5 LoRA가 현재 장비에서 끝나더라도, SDXL 기준서와 다른 해상도·화풍·얼굴 detail을 그대로 대체할 수 없다. 이 분리를 지키면 "8 GB에서 학습했다"는 사실을 "웹툰 캐릭터 일관성을 해결했다"로 잘못 확대하지 않는다.

2026-08-01에 현재 GPU에서 SD 1.5 base model의 실제 LoRA forward/backward와 adapter 직렬화를 한 step만 실행했다. `512 x 512`, batch 1, rank 4, UNet gradient checkpointing에서 loss는 `0.1137`, PyTorch가 보고한 GPU peak allocation은 약 `1,915 MB`, 실행 시간은 `1.6초`였다. 즉, 현재 8 GB 환경은 작은 SD 1.5 LoRA의 **학습 경로 자체**를 실행하고 adapter 파일을 만들 수 있다. 하지만 이 probe는 한 장의 중간 reference 이미지와 한 step만 썼으므로 character dataset, 일반화, 재로딩 품질을 전혀 검증하지 않는다. adapter와 실행 script는 보존하지 않으며, 실제 학습을 시작할 조건은 A의 character sheet·caption·held-out 3/4 평가 묶음이 준비된 뒤로 둔다.

#### 3-image SD 1.5 LoRA의 held-out pose 품질 비교: 미채택

실행 경로가 품질로 이어지는지를 확인하기 위해, 이전 IP-Adapter/OpenPose 결과에서 뽑은 3장을 작은 학습 묶음으로 만들고 rank 8 LoRA를 120 step 학습했다. target은 학습에 쓰지 않은 driving video frame 60의 `손을 가슴 앞에 모은` OpenPose map과 bookstore 배경이었다. 동일 seed, 동일 prompt, 동일 ControlNet에서 base SD 1.5와 LoRA를 나란히 생성했다. loss는 첫 `0.02016`에서 마지막 `0.02093`으로 유한하게 유지됐고, peak allocation은 약 `1,938 MB`, 전체 실행은 `41.0초`였다. 따라서 이 비교는 앞선 fp16 optimizer 붕괴가 아닌 유효한 추론 결과다.

held-out 품질 비교에서 LoRA 출력은 기준의 청록색 단발이라는 큰 특징과 팔이 모인 pose를 일부 따르지만, 넓은 청록색 바지와 재킷의 형태·색을 회복하지 못했다. 얼굴·앞머리·hair clip도 base 출력보다 명확히 안정적이지 않으며, 손과 팔의 연결은 두 출력 모두 최종 컷 기준에 미달한다. 따라서 이 LoRA가 `학습하지 않은 pose에서 같은 캐릭터를 유지한다`는 품질 게이트를 통과했다는 증거는 없다. 비교 PNG는 폐기하고 이 판단만 보존한다.

실패 원인은 학습 step 수만이 아니라 dataset의 정의다. 세 장은 이미 의상·재킷이 서로 달라 character identity의 정답 집합이 아니며, 정면·3/4·측면·후면과 얼굴 기준도 없다. 이 결과는 8 GB에서 작은 LoRA를 실행할 수 있다는 기술 확인과, **불완전한 생성 결과를 그대로 LoRA dataset으로 증식하면 identity 품질을 회복하지 못한다**는 품질 반증을 함께 제공한다. 이 adapter와 실행 script는 삭제하며, A의 승인 dataset을 갖추기 전에는 step이나 rank만 늘려 재시도하지 않는다.

#### 전신 + 얼굴 crop 다중 IP-Adapter 비교: 미채택

LoRA 학습 없이 얼굴 조건을 보강할 수 있는지를 확인하기 위해, 같은 IP-Adapter 가중치를 두 번 로드했다. 하나에는 전신 reference, 다른 하나에는 그 reference에서 잘라 확대한 얼굴 crop을 넣고, 학습에 쓰지 않은 frame 60 OpenPose와 동일 seed를 사용했다. 단일 reference는 `[0.45, 0.00]`, 다중 reference는 `[0.35, 0.30]`, OpenPose scale은 `1.10`으로 고정했다. `512 x 768`, 15 step, sequential CPU offload에서 두 출력을 포함한 실행은 `32.2초`, GPU peak allocation은 약 `664 MB`였다.

다중 reference 출력은 단일 reference와 거의 같은 청록색 단발과 큰 전신 pose를 보인다. 그러나 face crop을 더해도 얼굴형·앞머리·hair clip이 더 명확히 고정되지 않았고, prompt에 지정한 재킷은 사라지며 bookstore 배경도 형성되지 않았다. 손은 가슴 앞에 모이는 큰 위치만 맞고 손가락·손목 방향은 검수할 수 없다. 따라서 같은 정면 reference에서 자른 얼굴은 **독립적인 얼굴 기준서가 아니며**, 단일 IP-Adapter의 identity 한계를 해소하지 못한다. 비교 PNG는 폐기했다.

이 결과로 추가 참조 이미지의 수보다 참조의 정보량과 각도가 중요하다는 점을 확인했다. 다음 reference 기반 실험은 같은 이미지 crop을 늘리지 않고, 정면·좌/우 3/4·측면과 표정을 사람이 승인한 별도 face sheet를 먼저 만든 뒤에만 수행한다. 그 전까지 multi-IP-Adapter를 웹툰용 face consistency 해법으로 채택하지 않는다.

#### SDXL과 SD 1.5의 차이 추적: sampling step은 주원인이 아님

앞선 결과만으로 `SDXL은 안 되고 SD 1.5는 된다`고 결론내릴 수는 없다. 두 경로는 모델 계열 외에도 identity 입력, ControlNet, 학습 데이터, 해상도, step, prompt가 한꺼번에 달랐다. 특히 SDXL은 Animagine XL 4.0에 한 장의 IP-Adapter reference를 넣었고, SD 1.5는 서로 의상이 다른 세 장으로 만든 미채택 LoRA를 사용했다. 후자의 출력도 얼굴·의상·손 품질 게이트를 통과하지 못했으므로, SD 1.5가 더 좋은 웹툰 경로라는 비교 근거도 없다.

| 비교 항목 | 기존 SDXL 경로 | 기존 SD 1.5 경로 | 이 비교로 알 수 없는 것 |
| --- | --- | --- | --- |
| identity 조건 | 정면 전신 reference 한 장의 IP-Adapter | 의상이 일치하지 않는 3-image LoRA | 모델 계열만 바꿨을 때의 identity 품질 |
| 구조 조건 | `xinsir` SDXL OpenPose | `lllyasviel` SD 1.5 OpenPose | 동일 pose control의 영향 |
| 생성 설정 | `512 x 768`, 15 step | `512 x 512`, 20 step | 해상도와 step의 독립 영향 |
| 목표 장면 | reference와 충돌하는 재킷, bookstore, 가슴 앞 손 pose | 별도 prompt와 LoRA 비교 | 같은 장면에서의 checkpoint 차이 |

이 혼선을 줄이기 위해 SDXL만 고정한 채, held-out driving video frame 60의 OpenPose map, 같은 전신 reference, 같은 seed, `IP-Adapter 0.45`, `OpenPose 1.10`, `512 x 768`, sequential CPU offload에서 step만 `15`와 `30`으로 바꿨다. 두 생성은 합계 `43.4초`, PyTorch가 보고한 GPU peak allocation 약 `664 MB`에서 끝났다. 두 출력 모두 청록색 단발·넓은 청록색 바지·가슴 앞 손의 큰 위치는 남지만, charcoal jacket은 사라지고 bookstore도 형성되지 않으며 hair clip·손가락·손목은 판독하기 어렵다. 30 step은 윤곽을 조금 더 굳히지만 이 실패를 고치지 않는다. 비교 PNG는 폐기했다.

따라서 이 조건에서 step 수는 주원인이 아니다. 관찰된 차이를 다음 순서로 분리한다.

1. **identity 입력의 충돌**: 전신 reference 자체에는 목표의 charcoal jacket이 없고 밝은 상의가 있다. 단일 IP-Adapter는 그 기준 이미지의 큰 색·의상 분포를 보존하려 하므로, prompt의 재킷 요구와 충돌한다. 먼저 승인 character sheet에 목표 의상 전체를 포함해야 한다.
2. **OpenPose의 표현 한계**: OpenPose는 관절의 큰 위치만 준다. 장소, 렌즈, camera yaw, 옷 주름, 손가락, 머리 장식의 형태를 지정하지 않는다. 그러므로 pose 조건 하나로 bookstore나 3/4 camera, 정밀 손을 기대할 수 없다.
3. **조건 우선순위와 정보 부족**: `OpenPose 1.10`과 한 장의 global reference를 동시에 강하게 쓴 구성에서는 pose와 reference의 큰 특징이 prompt보다 우선하기 쉽다. 같은 이미지의 face crop을 추가했던 실험도 독립적인 얼굴 정보가 없어 이를 해소하지 못했다.
4. **아직 분리하지 못한 기술 조건**: `512 x 768`은 SDXL의 세부 얼굴·손을 검수하기에 제한적일 수 있지만, 이 비교는 고해상도 ablation이 아니다. sequential CPU offload는 메모리 배치 방식일 뿐 같은 denoising 조건의 의미를 바꾸지 않으므로, 위 15/30 결과의 차이를 설명하지 않는다.

후속 비교는 기준 이미지를 먼저 교체한 뒤에만 의미가 있다. 승인한 정면·좌/우 3/4·전신 character sheet에서 재킷·clip·바지·신발을 명시하고, 같은 pose/장소/seed에서 `(a) IP-Adapter 없음`, `(b) IP-Adapter`, `(c) 검증된 character LoRA`를 각각 비교한다. 그 다음 OpenPose에 line 또는 depth 조건을 하나씩 더해 camera와 배경의 기여를 따로 확인한다. 이 순서가 끝나기 전에는 SDXL의 모델 품질 부족, 또는 SD 1.5의 우위라는 해석을 채택하지 않는다.

#### 다양한 driving pose의 OpenPose 입력 검수: 전신 구조만 부분 통과

SDXL 생성에 앞서, 같은 driving video에서 정지(`frame 0`), 한쪽 지지발과 팔 교차(`240`), 양팔 확장(`480`), 몸통 기울기(`720`), 교차 보행 전환(`1040`)의 다섯 전신 frame을 골라 CPU OpenPose detector로 다시 추출했다. 모든 frame에서 사람 한 명과 목-어깨-팔꿈치-손목, 골반-무릎-발목의 큰 연결은 구별됐다. 특히 frame `1040`의 교차 다리와 한쪽으로 뻗은 팔은 map에도 남으므로, 이 다섯 pose는 SDXL 조건 비교의 후보가 된다.

하지만 `include_hand=True`, `include_face=True`로 추출해도 작은 손의 손가락 관절과 눈·시선 방향은 안정적으로 읽히지 않았다. 팔을 크게 벌린 frame `480`도 손목 이후의 정보가 희박하며, 팔을 몸 앞에서 교차한 `240`, `720`에서는 손과 몸통의 가림 순서를 확정할 수 없다. 따라서 이 입력 묶음은 **전신 pose 다양성** 검증에는 쓰되 손·얼굴·시선의 정답 조건으로 쓰지 않는다. 제3자 driving frame을 포함한 임시 contact sheet는 보존하지 않았다.

다음 SDXL 실행은 동일한 identity reference, seed, `IP-Adapter 0.45`, `OpenPose 1.10`, `512 x 768`, 15 step으로 이 다섯 pose를 각각 한 번 생성하고, (1) 머리·바지·신발의 identity, (2) 팔·다리·전신 crop, (3) 손목과 지지발의 판독 가능성, (4) 장소·camera의 drift를 contact sheet에서 따로 기록한다. 현재 CUDA 장치 노드가 없는 상태에서는 이 생성 비교를 실행하지 않고, GPU 접근이 복구된 뒤에만 결과물을 보존한다.

#### 다섯 pose SDXL 생성 비교: identity는 부분 유지, pose 품질은 미채택

CUDA 접근을 복구한 뒤 위 다섯 OpenPose map을 실제로 생성했다. 모든 실행은 같은 Animagine XL 4.0 checkpoint, 같은 identity reference, 같은 seed, `IP-Adapter 0.45`, `OpenPose 1.10`, `512 x 768`, 15 step, sequential CPU offload로 고정했고 pose map만 바꿨다. pose별 실행은 `13.97-14.48초`, 다섯 장 합계는 약 `70.6초`, PyTorch가 보고한 GPU peak allocation은 약 `663.5 MB`였다.

다섯 pose 비교는 중립 서기, 한쪽 지지발·팔 교차, 양팔 확장, 몸통 기울기, 교차 보행 전환을 나란히 확인했다. 청록색 단발·밝은 상의·청록색 바지·흰 신발과 서가 배경은 다섯 장에서 대체로 남아, 단일 reference가 큰 색·의상 실루엣에는 작동함을 확인했다. 그러나 face shape와 hair clip은 흔들리고, reference에 없는 재킷도 여전히 재현되지 않는다. 비교 PNG는 폐기했다.

pose 품질은 통과하지 못했다. 중립 서기는 읽을 수 있지만, frame `240`의 팔 교차와 지지발, `480`의 양팔 확장에는 출력이 맞지 않았고, frame `720`은 몸통을 지나치게 확대해 전신·양발 crop 조건을 깨뜨렸다. frame `1040`은 한쪽 다리와 팔의 동적 변화를 만들었지만, 입력의 교차 보행·팔 방향을 정확히 따르지 않았다. 손가락·손목 방향은 어느 출력에서도 검수할 수 없었다.

따라서 이 조립식 SDXL 경로는 **다양한 pose를 만들어 보이게 할 수는 있지만, 웹툰 컷에 필요한 pose transfer의 정확성과 전신 framing을 보장하지 못한다**. 같은 OpenPose scale을 다시 미세 조정해 성공 사례를 고르지 않는다. 다음 비교는 승인 character sheet를 먼저 준비하고, 같은 다섯 pose에서 OpenPose만 쓴 기준선과 OpenPose + line 또는 depth를 한 조건씩 추가한 결과를 비교해야 한다. driving video의 원본 frame 및 pose map은 제3자 자료이므로 보존하지 않았다.

#### 배경 제거 reference + 빈 배경 생성 비교: pose 개선 없음

배경이 identity reference의 색·구도를 붙잡아 pose를 방해하는지 확인하기 위해, 같은 전신 reference의 회색 배경을 GrabCut foreground 분리로 흰색으로 바꾸고, prompt도 `isolated character, plain white studio background`으로 교체했다. 서가·방·가구는 negative prompt에 넣었다. 나머지는 앞의 다섯 pose 비교와 동일하게 Animagine XL 4.0, seed, `IP-Adapter 0.45`, `OpenPose 1.10`, `512 x 768`, 15 step, sequential CPU offload로 고정했다. 이 비교는 reference 배경과 text scene을 함께 바꿨으므로, 둘의 기여를 각각 분리한 단일 변수 ablation은 아니다.

다섯 출력은 pose별 `13.95-14.38초`, GPU peak allocation 약 `663.5 MB`에서 생성됐다. 서가 배경은 사라졌지만, 모델은 순백 대신 옅은 청록색 단색을 만들었다. 청록색 머리·바지와 흰 상의라는 큰 색상은 남았으나, 얼굴 비율·앞머리·hair clip의 drift는 배경 포함 결과보다 더 크다. GrabCut 결과도 가는 신발 외곽을 일부 잃었으므로, 이 한 장을 webtoon character sheet의 기준 원본으로 승격하지 않는다. 비교 PNG는 폐기했다.

pose 품질도 개선되지 않았다. 중립 서기는 읽히지만 frame `240`의 팔 교차와 지지발, frame `480`의 양팔 확장은 여전히 재현되지 않았다. frame `1040`에서는 뻗은 팔과 들린 다리가 보이지만 입력의 교차 보행·팔 방향과 같지 않고, 손은 여전히 손가락·손목으로 검수할 수 없다. 그러므로 배경을 비우는 것은 scene 합성 전의 **인물 asset 분리 후보**일 수는 있어도, 현재 SDXL + IP-Adapter + OpenPose 경로에서 pose transfer 해법은 아니다.

다음 배경 관련 실험은 두 변수를 함께 바꾸지 않는다. `(a) 원래 reference + 빈 배경 prompt`, `(b) 배경 제거 reference + 기존 bookstore prompt`를 같은 한 pose에서만 비교해 reference 배경과 text scene의 기여를 분리한다. 이 결과가 나오기 전에는 배경 제거가 identity 또는 pose를 좋게 한다는 주장을 채택하지 않는다.

#### 추가 후보: PhotoMaker V2의 다중 ID 입력 경로

[PhotoMaker V2](https://github.com/TencentARC/PhotoMaker)는 한 장 또는 여러 장의 얼굴 입력을 stacked ID embedding으로 묶어, 추가 LoRA 학습 없이 SDXL 계열 base model에서 identity를 보강하는 공개 구현이다. 공식 저장소는 ControlNet/T2I-Adapter와의 결합 경로를 안내하고, 모델 카드는 Apache-2.0을 표기한다. 이 구조는 같은 이미지를 face crop으로 반복한 multi-IP-Adapter보다, 정면·좌/우 3/4·표정처럼 **서로 다른 승인 얼굴 원본**을 하나의 identity 입력으로 다루는 후보가 될 수 있다.

그러나 현재 기본 경로로 채택하지 않는다. 공식 저장소는 최소 11 GB GPU를 안내하며, 설명과 예시는 실제 사람 얼굴의 ID fidelity를 중심으로 한다. 만화식 눈·앞머리·hair clip과 전신 의상·손·camera의 일관성을 보장한다는 근거는 아니다. 따라서 이 대안은 `12 GB 이상 GPU + 자체 제작 다각도 face sheet + OpenPose/depth 또는 line control` 조건이 갖춰질 때만 별도 검증한다.

PhotoMaker V2의 첫 검증은 단일 prompt 결과를 고르는 방식이 아니다. 같은 character sheet의 정면·좌 3/4·우 3/4 얼굴을 ID 입력으로 두고, 학습에 쓰지 않은 3/4 전신 pose와 다른 장소에서 (1) 눈·앞머리·clip의 동일성, (2) 전신 의상·신발, (3) pose와 camera, (4) 손·얼굴의 보정 필요 영역을 contact sheet에서 판정한다. 이 네 항목 중 얼굴만 좋아져도 웹툰 파이프라인 통과로 확대하지 않으며, 얼굴 identity 보강 모듈이라는 제한된 역할로만 채택한다.

### SD 1.5 기반의 별도 정지 컷 파이프라인

SD 1.5 경로는 SDXL 결과가 부족할 때의 저해상도 대체 경로가 아니다. 현재 8 GB GPU에서 `512 x 512`, batch 1, rank 4 LoRA의 실제 forward/backward와 adapter 저장이 실행됐고, SD 1.5 OpenPose ControlNet도 로컬에 있다. 따라서 이 경로의 목적은 **학습 가능한 캐릭터 identity와 검증 가능한 정지 웹툰 컷을 먼저 만들고, motion은 그 뒤에 선택적으로 붙이는 것**이다.

```text
LLM shot intent
  -> 승인 character sheet + dataset manifest
  -> SD 1.5 character LoRA training
  -> full-body pose/camera guide
  -> SD 1.5 LoRA + OpenPose ControlNet panel candidates
  -> face/hand/object mask inpaint
  -> full-body render -> crop -> 4-panel continuity review
  -> (선택) AnimateDiff video-to-video에서 동작 후보와 keyframe만 탐색
```

| 단계 | 고정 원본과 도구 | 산출물 | 통과하지 못하면 |
| --- | --- | --- | --- |
| 0. 캐릭터 계약 | 자체 제작 character sheet, 의상·hair clip·눈·신발의 관찰 항목 | `character-spec.md`, 정면/3-4/측면/후면/표정 승인표 | 생성·학습을 시작하지 않음 |
| 1. 학습 데이터 | 권리가 분명하고 사람이 승인한 16-32장, caption의 trigger token과 pose/camera 기록 | dataset manifest, train/held-out 분리 | 같은 정면 이미지 crop이나 미채택 생성물의 증식은 제외 |
| 2. identity 학습 | SD 1.5 base, character LoRA, batch 1, fp32 adapter optimizer, gradient checkpointing | LoRA checkpoint와 step별 sample 기록 | loss가 유한해도 held-out identity가 흔들리면 step/rank 확대 대신 dataset을 수정 |
| 3. 컷 초안 | LoRA, SD 1.5 OpenPose ControlNet, full-body pose guide | panel별 512 계열 full-body candidate | 팔·다리·전신 crop이 pose guide와 다르면 pose 입력을 고침 |
| 4. 카메라·공간 | 3/4 또는 원근 컷은 사람이 승인한 depth/line guide를 추가 | camera/depth/line 기록과 후보 | OpenPose만 또는 `three-quarter` prompt만으로 camera 통과를 주장하지 않음 |
| 5. 국소 보정 | SD 1.5 inpainting checkpoint, 얼굴·눈·앞머리, 손·소품, 발·접지별 mask | mask, before/after, 수정 prompt | mask 밖의 승인 특징이 변하면 해당 수정은 폐기 |
| 6. 연속성 검수 | 동일 checkpoint/LoRA/negative prompt/색 보정, 4컷 contact sheet | episode contact sheet와 판정표 | identity, pose, camera, 손·발 중 하나라도 불합격이면 주 예제로 채택하지 않음 |

이 경로의 중요한 차이는 **전신을 먼저 만들고 그 뒤 crop한다**는 점이다. 대화 컷도 처음부터 얼굴만 생성하지 않고, 적어도 승인한 전신 또는 허리 위 후보에서 camera crop을 고른다. 그래야 다음 컷의 신발·바지·몸통 방향과 얼굴·시선이 모순되는지를 검수할 수 있다. 얼굴 close-up은 5단계의 별도 inpaint 대상으로 두며, 한 번의 text-to-image 생성에 얼굴·손·전신·배경을 모두 완성시키지 않는다.

카메라 제어는 장면에 따라 두 갈래로 나눈다. 정면/약한 3/4의 단순 컷은 OpenPose 하나와 full-body guide로 먼저 만든다. 강한 3/4, low angle, 소품 가림이 있는 컷은 pose 외에 depth 또는 line guide를 추가한다. 8 GB에서 두 ControlNet의 동시 실행은 아직 품질·메모리를 검증하지 않았으므로, 이를 기본값으로 약속하지 않는다. 실제 실행이 불가능하면 camera guide가 가장 중요한 컷을 먼저 정지 image-to-image/inpaint로 승인하고, 결과를 다른 컷의 기준 원본으로 되돌린다.

AnimateDiff는 이 SD 1.5 LoRA 경로에서 정지 컷을 대체하지 않는다. 공식 Diffusers 문서는 SD 1.4/1.5 기반 personalized model에 motion adapter와 video-to-video ControlNet을 결합할 수 있음을 안내한다. 따라서 4컷 정지 contact sheet가 identity·pose·camera 게이트를 통과한 뒤에만, 사람 검수 driving video와 frame별 pose 조건으로 짧은 동작 후보를 만든다. 영상에서 사람 검수를 통과한 frame은 새 컷의 pose/camera reference가 될 수 있지만, 영상 frame 자체를 최종 웹툰 컷으로 승인하지 않는다.

#### SD 1.5 경로의 첫 검증 순서

1. character sheet와 dataset manifest의 정면·3/4·측면·후면·표정·의상 항목이 모두 채워졌는지 Python으로 검사한다.
2. LoRA 없이, 같은 held-out pose와 배경에서 SD 1.5 + OpenPose의 base 출력을 만든다.
3. 학습 LoRA를 같은 seed, prompt, pose guide에 적용해 base와 contact sheet로 비교한다.
4. 학습 dataset에 없던 3/4 pose와 다른 장소에서도 머리·눈·clip·재킷·바지·신발, 전신 crop을 판정한다.
5. 이 두 컷이 통과한 뒤에만 face/hand/foot mask inpaint를 적용하고, full-body 원본과 crop 결과를 함께 보존한다.

이 순서는 앞선 3-image LoRA 실패를 막는다. `loss가 내려갔다`, `adapter가 저장됐다`, `한 장이 예쁘다`는 어느 것도 품질 통과 조건이 아니다. held-out pose·장소와 4컷 배열에서 character contract가 유지되는지만 채택 근거로 쓴다.

대안 C는 LoRA가 identity를 붙잡은 뒤에만 시작한다. reference image와 pose sequence만 받는 전용 human animation 모델은 자연스러운 동작 후보를 늘릴 수 있지만, 얼굴·손·camera를 자동 완성하지 않는다. 따라서 영상 출력에서 사람 검수를 통과한 frame만 선택하고, A의 character sheet와 대조한 뒤 정지 컷 inpaint로 보낸다. 이 경로는 현재 8 GB 장비에서 억지로 축소하지 않고, 필요한 VRAM을 갖춘 환경에서 별도 검증한다.

### 새 권장 경계

LLM은 다음처럼 **shot intent**만 구조화한다. `left_hand = 0.64` 같은 관절 수치나 직접 rig 회전값은 만들지 않는다.

```text
action: walk_to_door
beat: left_foot_support -> right_foot_swing
body_contact: right_hand near_bag_strap
gaze: door
camera: three_quarter_wide, eye_level
required_full_body: true
candidate_duration: 1.5s
```

motion model 또는 driving video가 여러 연속 자세를 제안하면, 사람은 지지발·체중·손과 소품의 접점·목-머리 방향이 맞는 frame만 승인한다. 승인 frame과 그 pose/face/depth 조건을 생성 모델에 다시 넣어 character LoRA 또는 참조 identity 조건과 결합하고, 그 뒤에만 정지 컷의 inpaint 단계를 적용한다. 이 순서라면 LLM은 의미 있는 콘티 인터페이스로 남되, 자연스러운 인체 역학을 작은 일반 LLM의 임의 관절값이나 Blender rig 조작에 맡기지 않는다.

## 포즈 트랜스퍼 후보 판정

포즈 트랜스퍼는 기준 인물 이미지와 driving pose 또는 motion video를 받아, 기준 인물이 그 동작을 하는 이미지·영상으로 바꾸는 기술이다. 전신 동작을 자연스럽게 제안하는 데에는 평면 cutout 회전보다 적합할 수 있다. 그러나 이것을 웹툰의 최종 컷 생성기로 채택할지는 네 품질 게이트와 사용 조건을 별도로 통과해야 한다.

| 후보 | 확인한 장점 | 웹툰 최종 컷에 부족한 점 | 사용 조건 | 판정 |
| --- | --- | --- | --- | --- |
| MimicMotion | pose guidance로 장기 human motion을 생성하고, 공개 checkpoint와 실행 구성을 제공함 | 얼굴·화풍·소품을 컷 단위로 보정하는 기능과 카메라 연출을 보장하지 않음 | 72 frame 예시는 16GB VRAM, 16 frame U-Net은 8GB 가능하나 VAE decoder는 16GB 또는 CPU 필요. 이 환경은 SVD 저장소 접근이 gated 상태여서 현재 실행 불가 | 짧은 동작 참고 영상 후보 |
| MusePose | 이미지와 pose signal로 virtual human animation을 만드는 공개 구현 | 저장소가 얼굴·복잡한 의상 세부 보존 및 복잡 배경 flicker 한계를 명시함 | 코드 MIT이나 trained model과 test data는 non-commercial research only | 본문 기본/배포 예제 제외 |
| MagicDance/MagicPose | pose와 facial expression retargeting을 함께 다룸 | 프로젝트가 데이터·pose tracker 품질 의존성을 명시하고, 최종 컷의 카메라/스타일 계약을 제공하지 않음 | USC research license | 본문 기본/배포 예제 제외 |
| MagicAnimate/AnimateAnyone 계열 | appearance encoder 또는 reference path로 정체성 보존을 시도함 | 사람 평가에서 복잡 동작과 학습 분포 밖 identity의 동작 일치가 낮게 나왔으며, 공식 구현·가중치 조건이 후보마다 다름 | MagicAnimate 공식 가중치는 appearance encoder 3.43GB, DensePose ControlNet 1.45GB, temporal attention 5.11GB로 합계 13.1GB이며, 별도 SD 1.5·VAE가 필요함. 공식 코드는 이 모듈과 3D U-Net을 동시에 GPU에 올림 | 비교 연구 또는 더 큰 VRAM 환경의 후보 실험에 한정 |
| One-to-All Animation 1.3B | 단일 reference image와 driving video를 받아 alignment-free character animation 및 image pose transfer를 목표로 하며, cartoon data와 1.3B checkpoint를 공개함 | 기준 이미지·pose video를 전용 preprocessing으로 함께 처리하는 video 경로라, 한 장의 최종 정지 컷만 바로 고르는 도구가 아님 | 공식 안내의 경량 경로도 16 GB T4 기준이다. 2026-08-02에 확인한 1.3B adapter는 6.57 GB, 기반 Wan 1.3B Diffusers 패키지는 28.94 GB이며, 공식 inference는 전체 pipeline을 `pipe.to(cuda)`로 올림 | 16 GB 이상에서 first 16 frame 품질 검증을 할 우선 후보. 현재 8 GB의 즉시 실행 경로에서는 제외 |

2025년 외부 평가에서는 AnimateAnyone, MagicAnimate, ExAvatar의 pose-transfer 영상을 보고 원하는 행동을 맞힌 비율이 전체 42.92%였고, source 행동과 일관된다고 판정한 비율은 36.46%였다. 이 수치는 각 프로젝트의 demo나 benchmark가 좋아 보이더라도, 웹툰의 결정적 동작·손·소품·인물성을 자동으로 통과시켜서는 안 된다는 근거다.

### 채택 범위

포즈 트랜스퍼는 다음처럼 제한해서 사용한다.

1. **동작 연구 입력**: 짧은 driving video 또는 pose sequence에서 걷기, 팔 동작, 체중 이동의 후보를 얻는다.
2. **콘티·blockout 보조**: 좋은 frame을 골라 pose, 소품 접점, camera 방향을 사람과 함께 다시 승인한다.
3. **최종 컷의 원본은 아님**: 선택 frame은 face sheet, style sheet, object contact, camera contract와 따로 대조하고, 통과하지 않으면 생성·inpaint 또는 직접 작화 단계로 돌린다.

반대로 최종 컷의 pose를 포즈 트랜스퍼 결과 한 장에서 확정하고, 같은 결과에 얼굴·화풍·다이내믹 카메라를 모두 기대하는 경로는 채택하지 않는다. 이 방식은 현재의 단순 2D cutout보다 자연스러운 동작을 제안할 수는 있어도, 사용자에게 필요한 웹툰 수준의 검수 가능성과 수정 가능성을 제공하지 못한다.

### OpenPose 이후의 확보 기준

현재 `SDXL + IP-Adapter + OpenPose` 정지 이미지 경로는 포즈 트랜스퍼 후보에서 제외한다. 이후 "포즈 트랜스퍼를 확보했다"고 말하려면 전용 모델이 `기준 캐릭터 이미지 + 권리가 확인된 driving video -> 연속 frame`을 처리하고, 서로 다른 최소 세 동작에서 다음을 모두 만족해야 한다: (1) source의 팔·다리·몸통 방향과 지지발을 사람이 같은 행동으로 판정할 것, (2) 전신과 양발이 잘리지 않을 것, (3) 기준 캐릭터의 머리·의상·신발이 연속 frame에서 유지될 것, (4) 손·얼굴의 실패 위치를 후속 inpaint 대상으로 판독할 수 있을 것. 한 동작의 보기 좋은 frame이나 skeleton map 일치만으로는 통과시키지 않는다.

현재 장비에서 다음 실행 경로는 만들지 않는다. One-to-All의 공식 1.3B 경로는 필요한 가중치가 크고 전체 pipeline을 GPU에 적재하므로 8 GB GPU에서 short-clip으로 축소했다고 실행 가능하다는 근거가 없다. CPU offload를 임의로 덧대어 한 장을 만드는 것은 원 구현의 시간·메모리·품질 계약을 바꾸므로, `16 GB 이상 GPU`에서 first 16 frame을 실제로 생성하는 검증을 다음 장비 단계로 둔다. 그 전까지 이 책의 현행 파이프라인은 pose transfer를 해결했다고 주장하지 않는다.

### 전용 pose-transfer 구현 추가 조사

2026-08-02에 공개 구현을 추가로 조사했다. 중요한 차이는 이 후보들이 OpenPose 한 장을 SDXL에 넣는 방식이 아니라, **reference 이미지와 driving video의 공간 정렬·전경 mask·시간축 조건을 함께 처리한다**는 점이다. 따라서 다음 모델은 OpenPose 파이프라인의 scale을 바꾸는 대체물이 아니라, 별도의 video-to-keyframe 생성 경로다.

| 후보 | reference와 동작을 묶는 방식 | 웹툰 파이프라인에서의 의미 | 현재 장비 판정 |
| --- | --- | --- | --- |
| [One-to-All Animation](https://github.com/ssj9596/One-to-All-Animation) | reference image와 driving video를 전용 preprocessing으로 정렬하고, reference extractor와 pose-control을 함께 추론한다. cartoon dataset·1.3B checkpoint를 공개한다. | 현재 후보 중 만화 캐릭터와 image pose transfer를 명시적으로 함께 다룬다. `16 GB 이상`에서 first 16 frame 검증의 우선순위 1이다. | 공식 경량 안내도 16 GB T4 기준. 현재 8 GB에서는 제외 |
| [StableAnimator](https://github.com/Francis-Rings/StableAnimator) | reference image와 pose sequence를 받아 ID-preserving video를 생성하고, face mask 기반 보정 단계를 별도로 둔다. pose는 reference의 체형에 정렬해야 한다. | pose map이 아니라 reference-동작 정렬과 얼굴 보정을 함께 검증해야 한다는 입력 계약의 근거다. | 512x512·프레임 수 축소 옵션은 있으나 공개 문서만으로 8 GB 실행을 보장하지 않음 |
| [SteadyDancer](https://github.com/MCG-NJU/SteadyDancer) | reference image, driving video, positive/negative aligned pose sequence를 받아 I2V 방식으로 첫 frame 보존을 목표로 한다. cartoon/full-body를 포함한 X-Dance benchmark를 공개한다. | reference와 motion의 초기 frame 불일치가 identity drift를 만든다는 현재 실패와 직접 관련 있다. | Wan 기반 14B 경로. 현 8 GB의 실행 후보 아님 |
| [SCAIL-2](https://github.com/zai-org/SCAIL-2) | reference image와 foreground mask, driving video 또는 rendered pose video, frame별 mask video를 한 번에 입력한다. | skeleton만 주는 대신 전경 mask와 실제 driving video를 함께 쓰는 경로다. 소품·다인물·배경 교체까지 확장 가능하다. | 공개 실행은 SCAIL-14B. 현 8 GB의 실행 후보 아님 |
| [X-Dyna](https://github.com/bytedance/x-dyna) | reference appearance adapter, body motion, local face control을 분리해 driving video의 몸·표정을 옮긴다. | 얼굴을 body pose의 부산물로 두지 않는 설계가 필요함을 보여 준다. | 공식 최소 20 GB, 권장 80 GB. 현재 장비 제외 |

이 조사로 확보할 경로는 다음과 같이 좁힌다. **16 GB GPU를 확보하면 One-to-All 1.3B를 먼저 실행해 16 frame의 정지·팔 교차·보행 세 동작을 검증한다.** 그 결과에서 driving action·identity·전신 framing이 동시에 통과할 때만 좋은 keyframe을 웹툰 컷 후보로 넘긴다. 24 GB 이상 환경에서는 얼굴·정렬 문제에 대응하는 X-Dyna 또는 SteadyDancer를 second opinion으로 비교한다. 현재 8 GB에서는 character sheet, shot contract, driving video와 mask의 사람 검수까지만 수행하고, OpenPose 단일 조건 생성으로 pose transfer를 대체하지 않는다.

### driving video 없이 단일 컷을 만드는 대안

driving video는 연속 동작의 자연스러운 체중 이동을 주는 입력일 뿐, 단일 웹툰 컷의 필수 입력은 아니다. 단일 컷에서는 `기준 캐릭터 이미지 + target pose가 담긴 정지 이미지 + 장면/카메라 지시`를 분리해 줄 수 있다. 다만 이 경로는 target pose를 **정확히 전사하는 pose transfer**가 아니라, 목표 구도에 캐릭터를 재구성하는 image-editing 또는 character-replacement 후보임을 명시한다.

| 방법 | 입력 계약 | 강점 | 현재 판단 |
| --- | --- | --- | --- |
| 다중 reference image editing | character sheet와 target pose/reference 이미지를 함께 넣고, LLM이 만든 shot 지시로 인물·의상·배경의 역할을 지정 | driving video 없이 3/4 camera, 소품, 장소가 담긴 한 컷을 바로 만들 수 있다. [FLUX.2 Klein 4B](https://github.com/black-forest-labs/flux2)는 다중 reference editing과 약 8 GB VRAM을 안내한다. | 2026-08-02 공식 CLI 실제 실행에서 Qwen3 4B FP8 text encoder가 GPU 약 6.57 GB를 점유한 뒤, 보조 Mistral Small 24B text model을 GPU에 추가 적재하다가 남은 약 876 MiB에서 1.25 GiB allocation이 실패했다. CPU offload 옵션도 이 보조 모델 적재 이전에는 적용되지 않아 이미지 생성 단계에 도달하지 못했다. 현 8 GB에서는 미채택이며, 16 GB 이상 환경에서 peak VRAM부터 다시 측정하되 성공 조건으로 단정하지 않는다. |
| Qwen-Image-Edit-2511 다중 image 재구성 | character sheet 1~2장과 target pose/장소 정지 이미지, LLM shot 지시를 `edit_image` 목록으로 함께 넣는다 | 공식 모델은 portrait identity, multi-image consistency, 새 viewpoint 생성을 개선 대상으로 밝히며, [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio)는 disk/CPU layer offload 예제를 제공한다. FLUX CLI의 Mistral 보조 모델과는 별개의 경로다. | **2026-08-02 실제 8 GB 미통과.** 공식 disk/CPU offload에서 Qwen text encoder 계산 중 6.88 GB 사용 상태로 추가 130 MiB allocation이 실패했다. 전체 FP8은 VAE의 bf16 입력과 FP8 bias type 불일치, text encoder만 FP8은 Qwen vision convolution의 FP8 cuDNN 미지원으로 실패했다. 57 GB 가중치를 받은 뒤에도 PNG 출력에 도달하지 못했으므로 현 장비 후보에서 제외한다. |
| FLUX.1 Kontext dev reference edit | 승인 character image를 `kontext_images`로 넣고 pose·camera·장소 변화를 자연어로 지시한다 | [DiffSynth-Studio의 공식 저 VRAM 예제](https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux/model_inference_low_vram/FLUX.1-Kontext-dev.py)는 FP8 CPU offload와 bf16 GPU 계산을 사용하며, 같은 reference에서 표정·행동·장소를 바꾸는 호출을 제공한다. | **실행 미판정.** 2026-08-02 실제 probe에서 주 가중치 `flux1-kontext-dev.safetensors` 23.8 GB 다운로드까지만 진행했고, 전송 속도 급락으로 text encoder·VAE 적재와 PNG 생성 전 중단했다. VRAM 통과나 품질 성공으로 기록하지 않는다. 단일 reference이므로 엄밀한 pose transfer의 주 경로도 아니다. |
| JoyAI-Image-Edit 단일 reference edit | 전신 character image 한 장과 자연어 pose·camera·장면 지시 | [공식 저 VRAM 예제](https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/joyai_image/model_inference_low_vram/JoyAI-Image-Edit.py)는 최소 4 GB VRAM과 CPU offload를 명시한다. | **현 장비의 반복 검증 후보에서 제외.** 공식 예제가 요구하는 `transformer.pth` 32.5 GB, `model*.safetensors` 17.5 GB, VAE까지 합쳐 최소 약 50.6 GB의 다운로드가 필요하다. 한 장 입력만 받으므로 다각도 face sheet도 고정하지 못한다. |
| in-context image editing LoRA | `A: 중립 일반 인물`, `B: 목표 동작 일반 인물`, `C: 승인 character sheet`를 넣어 A→B의 시각 변환을 C에 적용한다 | DiffSynth-Studio는 Qwen-Image-Edit-2511용 3-image in-context editing LoRA를 공개했다. 골격 keypoint가 아니라 실제 목표 pose의 변환 예시를 조건으로 쓴다. | **정지 pose transfer의 두 번째 후보.** 동작 예시와 캐릭터 기준서를 분리해 넣을 수 있으나, 전신·손·발·가림·화풍 일관성은 아직 현 장비에서 미검증이다. 첫 경로의 실행 성립 뒤 같은 512 x 768 조건으로 비교한다. |
| FireRed-Image-Edit-1.1 | 1~3장의 참조 이미지와 자연어 편집 지시 | portrait consistency와 multi-element fusion을 목표로 하고, Apache-2.0 코드·가중치를 제공한다. | 최적화한 공식 inference도 30 GB VRAM을 요구한다. 현재 장비에서는 실행하지 않고, 30 GB 이상 환경의 다중 reference 비교 후보로만 유지한다. |
| target 사진의 인물 영역 교체 | target pose가 담긴 정지 사진의 전경 mask에 character reference를 주입하고, 장면은 target 사진에서 유지 | target 이미지가 가진 실제 pose·camera·소품 접점을 활용할 수 있다. video용 [SCAIL-2](https://github.com/zai-org/SCAIL-2)는 이 계약을 mask와 driving video로 확장한다. | 정지 이미지용 공개 구현과 만화 character 품질을 별도로 검증해야 하며, 전신 identity가 자동 보장되지는 않음 |
| depth/line reference 조건 | target pose 이미지에서 depth 또는 line을 만들고 character reference와 결합 | OpenPose보다 몸통 실루엣, 가림, 장소의 원근을 더 많이 담을 수 있다. | identity를 보장하지 않으므로 단독 경로에서 제외. 다중 reference editing의 보조 입력으로만 검증 |
| 전용 reference-to-video transfer | character image와 driving video를 함께 받는 One-to-All, SteadyDancer, X-Dyna 등 | 시간축의 pose·표정·전신 움직임을 평가할 수 있다. | 자연스러운 보행·연속 행동에는 필수 후보지만 현재 8 GB 밖의 장비 단계 |

FLUX.2 실행은 기존 SDXL 비교의 중립 전신 캐릭터 한 장과 `옆으로 내딛고 서가 쪽으로 팔을 뻗는 3/4 전신 컷`이라는 자연어 지시로 시작했다. target pose 정지 이미지까지 넣는 다중 reference 품질 시험에는 도달하지 못했으므로, 이 결과는 pose transfer나 static reposing의 실패 판정이 아니라 **공식 8 GB 실행 경로의 메모리 실패**다. 출력 PNG는 없으며, Qwen3 4B FP8 download 약 4.9 GB만 남았다. 이후 더 큰 GPU에서 다시 시험할 때는 먼저 peak VRAM을 측정하고, 그 뒤 character sheet와 target pose 정지 이미지를 함께 넣어 identity, target pose, 전신 crop, 손목·접지, 3/4 camera를 각각 채점해야 한다.

따라서 현행 작업을 두 갈래로 둔다. **정지 웹툰 컷**은 다중 reference image editing으로 `character sheet + target pose 이미지 + shot intent`를 실험해 video 없이도 어떤 camera와 pose를 만들 수 있는지 평가한다. **연속 동작**은 16 GB 이상에서 전용 reference-to-video transfer로 검증한다. 두 갈래의 산출물을 섞어 "정지 이미지 편집이 자연스러운 동작을 증명했다" 또는 "동작 video가 최종 웹툰 컷 품질을 증명했다"고 확대하지 않는다.

### 8 GB 탐색 계획

이 작업의 제약은 **8 GB VRAM에서 실제로 실행하고 검수 가능한 웹툰 컷을 만드는 것**이다. OpenPose, LLM, Blender, driving video, 특정 base model은 평가 대상이 아니다. 각 도구는 아래 다섯 결과 축을 높일 때만 남긴다.

| 품질 축 | 통과 질문 | 탈락 예시 |
| --- | --- | --- |
| 구도 | 같은 캐릭터가 medium, full body, wide cut에서 의도한 화면 위치와 crop을 유지하는가 | 얼굴만 과도하게 확대되거나 전신이 잘림 |
| 포즈 | target 정지 이미지의 지지발, 몸통 방향, 양팔의 큰 관계가 읽히는가 | 팔·다리 수가 바뀌거나 접지와 가림을 판독할 수 없음 |
| 프로젝션·camera | 정면, 3/4, low/high angle처럼 화면의 투영·시점 변화가 의도와 맞는가 | 장면만 바뀌고 camera 관계가 그대로임 |
| 화풍 | 선, 색, 눈·머리카락 표현, 의상 질감이 같은 작화 규약으로 유지되는가 | 컷마다 사실화·다른 애니 스타일·다른 채색으로 drift |
| 캐릭터 일관성 | 얼굴형, 헤어 실루엣·clip, 의상 구조·색, 체형이 같은 인물로 읽히는가 | 단발색만 비슷하고 얼굴·의상·비율이 다른 인물 |

#### 단계 1: 실행 성립 게이트

`Qwen-Image-Edit-2511 + DiffSynth-Studio`의 disk/CPU offload는 첫 후보로 실제 실행했다. `512 x 768`, character sheet 한 장, target pose·camera 정지 이미지 한 장, 자연어 장면 지시 한 개를 준비했지만 text encoder 연산에서 GPU 메모리 부족으로 PNG를 저장하지 못했다. FP8 계산 변형도 지원되지 않아 현 장비의 실행 성립 게이트에서 탈락했다. 이후 후보도 같은 방식으로 peak VRAM, 실행 시간, 오류 유무와 PNG 저장을 먼저 기록한다. 결과가 없거나 GPU 메모리를 초과하면 품질 비교를 하지 않는다. FLUX.2처럼 추가 보조 모델이 GPU에 무조건 적재되는 경로도 이 게이트에서 제외한다.

`FLUX.1 Kontext dev`는 공식 8 GB offload 경로이지만, 23.8 GB 주 가중치를 내려받은 뒤에도 나머지 구성 요소가 필요해 이번 probe에서는 PNG 생성까지 도달하지 못했다. `JoyAI-Image-Edit`도 공식 최소 4 GB VRAM 안내와 별개로 최소 약 50.6 GB의 가중치 다운로드가 필요하다. 따라서 두 모델을 현 장비의 즉시 반복 실험 수단으로 채택하지 않는다. 다만 둘 다 OpenPose나 LLM을 입력 계약으로 삼지는 않으므로, 충분한 로컬 저장소와 안정적인 가중치 캐시가 확보된 별도 실행 환경에서는 reference edit 품질을 다시 검증할 수 있다.

#### 단계 2: 두 입력의 역할 분리

실행이 성립하면 character sheet는 `누구인가`, target 정지 이미지는 `어떤 pose·camera·장소인가`만 맡기고 같은 seed·해상도·step으로 비교한다. 먼저 target 이미지를 뺀 결과와 넣은 결과를 한 쌍으로 만들어, target이 구도·포즈를 실제로 바꾸면서 character identity를 무너뜨리지 않는지 확인한다. 이 비교에서 두 조건을 동시에 바꾸지 않는다.

#### 단계 3: 다섯 컷 품질 매트릭스

단일 성공 이미지를 채택하지 않는다. 사람 검수로 승인한 target 정지 이미지를 사용해 다음 다섯 컷을 같은 캐릭터 기준서로 생성한다.

| 컷 | 우선 검수 축 |
| --- | --- |
| 정면 medium 대화 컷 | 얼굴·눈·화풍·의상 기준선 |
| 3/4 full-body 정지 컷 | 전신 비율, 양팔·발, crop |
| low-angle wide 이동 컷 | perspective, 지지발, 동적 포즈 |
| high-angle 소품 상호작용 컷 | 손목·소품 접점, 가림, 장소 변화 |
| 측면 또는 후면 전환 컷 | 헤어 실루엣, 의상 후면, viewpoint 변화 |

각 컷은 다섯 품질 축을 `통과`, `부분 통과`, `미통과`로 표기한다. 하나라도 이미지가 예쁘다는 이유로 전체 통과로 올리지 않는다. 다섯 컷에서 캐릭터·화풍이 유지되고, 적어도 세 컷에서 target pose와 camera 관계가 읽힐 때만 다음 경로를 진행한다.

#### 단계 4: in-context pose 변환 비교

기본 다중 image 편집이 실행·품질 게이트를 부분 통과한 경우에만 `A: 일반 인물의 시작 pose`, `B: 일반 인물의 목표 pose`, `C: 캐릭터 기준서`를 이용하는 in-context editing LoRA를 같은 다섯 컷에 적용한다. 이 비교의 질문은 "예시 변환이 target pose를 더 잘 보존하는가"이며, OpenPose를 추가해 성공을 보완하지 않는다.

#### 단계 5: 웹툰 자산 채택과 후처리

전역 구도·포즈·camera·화풍·정체성이 통과한 컷만 face, hand, prop의 제한된 inpaint 후보로 넘긴다. 국소 보정 뒤에는 전신과 얼굴을 다시 확인한다. 전역 실패를 손·얼굴 보정으로 숨기지 않는다. 실행 script, 설정 JSON, 입력 조건, 결과 PNG, 검수표를 함께 남기며, 미통과 결과는 조사 노트만 보존하고 원고 예제 자산에서는 제거한다.

## 권장 파이프라인

| 단계 | 결정할 질문 | 주 산출물 | 공개 도구 후보 | 생성 AI의 위치 | 통과 기준 |
| --- | --- | --- | --- | --- | --- |
| 0. 시퀀스 설계 | 이 장면에서 독자가 무엇을 보아야 하는가? | 4~8컷 콘티, 컷별 감정·행동·대사 여백 표 | Krita 또는 종이 콘티 | 사용하지 않음 | 모든 컷에 인물, 행동, 시점, 말풍선 영역이 적혀 있음 |
| 1. 캐릭터 승인 | 같은 인물의 변하지 않는 특징은 무엇인가? | 정면·반측면·측면 전신 기준서, 표정표, 색상표, 금지 변형 | Krita | 후보 탐색에만 사용 가능 | 각도별 얼굴·머리·의상·색이 승인됨 |
| 2. 시작 원본 선택 | pose, 얼굴 반응, 공간·카메라 중 무엇을 먼저 고정할 것인가? | 각 컷의 승인 원본과 나머지 제어 입력 | Blender, Krita, Grease Pencil | 사용하지 않음 | 컷의 핵심 정보가 시작 원본에서 검수 가능함 |
| 3. 컷 초안 | 구조를 지키며 어떤 그림 표현을 쓸 것인가? | 후보 이미지, workflow JSON, seed, control 이미지 | ComfyUI + ControlNet/IP-Adapter | 후보 생성 | pose, 시점, 배경 위치가 블로킹과 일치함 |
| 4. 국소 보정 | 어느 영역이 기준서에서 벗어났는가? | 얼굴·눈·손·머리카락·의상 마스크, 보정 전후 이미지 | ComfyUI inpaint, Krita | 마스크 안 수정 | 수정 영역 밖의 승인 요소가 바뀌지 않음 |
| 5. 고난도 동작 | 재생성보다 재사용이 더 안전한가? | 레이어 분리 캐릭터, bone/mesh, pose 파일 | Blender Grease Pencil armature 또는 OpenToonz Plastic | 기준 자산 생성에 한정 | 같은 부품과 색이 다음 컷에 실제로 재사용됨 |
| 6. 식자·편집 | 독자가 세로로 읽을 때 컷을 이해하는가? | 세로 스크롤 페이지, 말풍선·효과음 레이어, 출력 PNG | Krita | 사용하지 않음 | 말풍선이 표정·손·중요 소품을 가리지 않음 |
| 7. 연속성 검수 | 네 컷을 함께 보아도 같은 장면인가? | contact sheet, 컷별 판정표, 수정 목록 | Krita 또는 Python contact sheet | 사용하지 않음 | 캐릭터, 광원, 의상, 장소, 시점 전환이 설명 가능함 |

### 0. 시퀀스 설계: 생성 전에 컷의 계약을 만든다

실습의 최소 단위는 독립 이미지 9장이 아니라 다음처럼 연결된 4컷이다.

| 컷 | 서사 역할 | 인물 pose와 카메라 | 말풍선 여백 | 주요 위험 |
| --- | --- | --- | --- | --- |
| 1 | 장소와 인물을 소개 | 전신 wide, 카메라는 눈높이 | 위쪽 25% | 배경과 의상 색이 섞임 |
| 2 | 인물이 움직임 | 전신 3/4 walk, 약한 측면 | 오른쪽 위 | 다리·손 pose, 머리 방향 |
| 3 | 반응을 보임 | 허리 위 3/4, 같은 카메라 축 | 왼쪽 위 | 얼굴·눈·앞머리 |
| 4 | 소품과 행동을 확인 | 손과 소품이 보이는 medium close-up | 아래쪽 | 손가락, 소품 크기, 가림 |

각 컷은 `누가`, `어디에`, `무엇을 하는가`, `어느 쪽을 보는가`, `어디를 비워 둘 것인가`를 문장으로 승인한다. 이것이 prompt가 아닌 콘티 계약이며, 후속 도구가 바뀌어도 유지된다.

### 1. 캐릭터 기준서: 한 장의 참조 사진보다 넓은 기준

기준서는 최소 정면·반측면·측면 전신, 얼굴 close-up, 기본·웃음·놀람 표정, 의상 앞·뒤 색상, 소품 크기를 포함해야 한다. 각 항목에는 관찰 가능한 특징과 금지 변형을 함께 쓴다. 예를 들어 `앞머리 세 갈래`는 관찰 항목이고, `긴 머리 금지`는 실패 판정이다.

이 기준서는 LoRA 학습 데이터 또는 IP-Adapter 참조 이미지의 후보가 될 수 있지만, 먼저 사람 검수용 원본이다. 기존 상업 캐릭터, 실존 인물, 사용 권한이 불명확한 이미지는 기준서와 실습 데이터에 사용하지 않는다.

### 2. 시작 원본 선택: 모든 컷이 pose-first일 필요는 없다

컷의 시작 순서는 서사와 실패 위험에 따라 고른다. 전신 pose-first는 가능한 경로 중 하나이며 일반 규칙이 아니다.

| 시작 방식 | 먼저 승인할 것 | 적합한 컷 | 다음 제어 |
| --- | --- | --- | --- |
| pose-first | 전신 pose, 관절, 소품을 잡는 손 | 걷기, 뛰기, 신체 접촉, 강한 원근 | camera blockout과 face sheet를 결합 |
| face-first | 얼굴 각도, 눈, 표정, 앞머리 | 감정 반응, 대화, close-up | 필요한 몸통·손을 뒤에서 연결 |
| camera/background-first | 지평선, 소실점, 인물 위치, 말풍선 여백 | 장소 소개, 추격, 군중, 강한 low/high angle | pose와 캐릭터를 공간에 맞춤 |
| object-first | 소품의 크기, 손의 접점, 읽히는 정보 | 티켓, 휴대폰, 편지, 도구 | 얼굴·손·카메라를 소품 기준으로 조정 |

현재 Blender armature blockout 실험은 pose-first 분기의 공간 제어만 검증한다. 그 결과를 face-first나 camera/background-first의 품질 증거로 확대 해석하지 않는다.

### pose-first 분기의 공간 블로킹

Blender 장면에는 단순 인체 rig, 바닥, 주요 소품, 카메라만 있어도 된다. 카메라의 초점거리, 높이, yaw/pitch, 인물의 위치와 전신 pose를 컷별로 저장한다. Blender는 카메라·조명·재질로 2D render를 만들며, render layer와 pass를 합성할 수 있다. Freestyle은 mesh와 Z-depth를 바탕으로 선 기반 비사실적 렌더를 만든다. 따라서 이 단계는 다음 컷에도 재사용할 수 있는 pose, line, depth, 구도 입력을 제공한다.

복잡한 원근, 뒤돌기, 팔과 몸통의 가림이 있는 컷은 간이 raster cutout보다 3D 블로킹이 적합하다. 반대로 정면 또는 반정면의 반복 동작은 2D cutout이 더 빠르고 동일성을 강하게 보장할 수 있다.

### 3. 컷 초안: 조건 제어와 참조를 분리한다

ComfyUI의 ControlNet 적용 노드는 별도 제어 이미지를 condition에 적용한다. 이 단계에서는 Blender에서 내보낸 pose, lineart, depth 중 해당 컷에 필요한 하나 또는 둘만 연결한다. IP-Adapter나 캐릭터 LoRA는 `누구인가`의 참조를 보강하지만, 공간 입력과 같은 역할로 기록하지 않는다.

컷 기록에는 적어도 다음을 저장한다.

```text
episode_id:
panel_id:
character_sheet_revision:
scene_blockout_file:
camera_id:
pose_id:
control_images:
character_reference_images:
workflow_json:
checkpoint_and_adapter_versions:
seed:
candidate_files:
selected_candidate:
selection_reason:
```

`selected_candidate`는 사람이 고른 한 파일이며, selection reason에는 "눈 모양은 기준서와 같고, 왼손은 실패"처럼 통과와 수정 대상을 같이 쓴다. seed만 저장해서는 다음 컷의 이유를 재현할 수 없다.

### 4. 국소 보정: 실패 영역별로 마스크를 분리한다

한 번의 재생성으로 손을 고치면 눈, 앞머리, 의상까지 함께 바뀔 수 있다. 따라서 실패 원인을 얼굴·눈, 손·소품, 머리카락, 의상·문양, 배경으로 분리하고, 각 영역을 독립 마스크로 둔다. ComfyUI의 inpainting은 mask와 전용 VAE 인코딩을 사용해 지정 영역을 다시 채우는 흐름을 제공한다. 마스크를 넓게 잡은 이유, 수정한 prompt, 수정 뒤에 다시 확인한 기준서 항목을 컷 기록에 남긴다.

수정 횟수가 늘어도 통과 기준은 "더 예쁘다"가 아니다. 수정 전후를 나란히 두고, 마스크 밖의 승인된 얼굴·의상·카메라가 보존되었는지와 마스크 안 실패가 실제로 고쳐졌는지를 판정한다.

### 5. 동작 후보와 key frame: 생성 모델이 맡을 범위를 정한다

생성된 단일 래스터 이미지를 단순 cutout으로 나누어 회전하는 방식은 자연스러운 관절, 가림, 원근을 보장하지 못하므로 이 파이프라인의 최종 경로에서 제외한다. Blender Grease Pencil의 armature modifier와 OpenToonz Plastic은 artist가 준비한 layer/mesh 자산을 bone weight로 변형할 수 있지만, 이 기능도 flat 생성 이미지 하나를 자동으로 자연스러운 rig로 바꾸는 장치로 설명하지 않는다.

다만 평면 부품은 큰 회전, 새로운 옆얼굴, 복잡한 가림을 자동으로 해결하지 않는다. 그런 컷은 생성형 human image animation 모델의 driving video 또는 pose sequence에서 먼저 후보를 만들고, 통과 frame만 정지 컷으로 채택한다.

- AnimateDiff + ControlNet처럼 character LoRA와 motion/pose 조건을 결합할 수 있는 생성 모델을 우선 검증한다.
- 통과 frame에서만 Krita 또는 inpaint로 손, 얼굴, 머리카락의 국소 영역을 고친다.
- Blender blockout은 적절한 driving 원본을 만들 수 없는 경우에만 비교·보조 자료로 사용한다.

리깅은 `동일 인물을 보장하는 최종 그림 생성기`가 아니며, 이 파이프라인의 기본 생성 도구도 아니다. 생성 모델의 동작 후보를 보완할 수 있는 제한적 제작 선택이다.

### 6. 식자와 세로 배치: 생성 이미지가 아닌 독서 결과를 만든다

완성 컷은 그림 파일만으로 끝나지 않는다. Krita의 레이어 파일에 그림, 말풍선, 대사, 효과음, 컷 간 여백을 분리해 둔다. 말풍선은 콘티에서 비워 둔 공간에만 넣고, 표정과 손·소품을 덮으면 컷을 다시 설계한다. 이 단계는 생성 모델에 맡기지 않는다. 대사나 글자가 이미지에 섞이면 수정성과 번역 가능성이 크게 떨어진다.

### 7. 연속성 검수: 한 컷이 아니라 배열로 판정한다

각 후보를 개별로 평가하지 않고, 선택한 4컷을 contact sheet로 만든다. 다음 질문에 모두 답할 수 있을 때만 초안 시퀀스로 승인한다.

1. 네 컷의 얼굴형, 눈, 머리, 의상, 소품이 기준서와 맞는가?
2. 카메라가 1에서 4로 이동하는 이유를 말할 수 있는가?
3. 배경의 출입구, 창문, 소품, 광원 방향이 연속되는가?
4. 컷 2의 전신 pose와 컷 3의 얼굴 방향이 모순되지 않는가?
5. 말풍선과 대사가 행동과 중요한 시각 정보를 가리지 않는가?
6. 각 실패가 어느 원본(기준서, blockout, control image, mask, 편집 파일)을 수정하면 해결되는지 구분되는가?

## 도구 선택의 최소 구성

| 역할 | 기본 도구 | 대체 도구 | 선택 이유 |
| --- | --- | --- | --- |
| 기준서·직접 보정·식자 | Krita | 다른 레이어 기반 편집기 | 캐릭터 원본과 최종 text layer를 분리함 |
| 전신 pose·카메라·depth/line 입력 | Blender | 손그림 콘티 + ControlNet 입력 | 컷 간 카메라와 공간을 재현할 수 있음 |
| 반복되는 평면 동작 | Blender Grease Pencil | OpenToonz Plastic | 동일 부품의 변형을 명시적으로 기록함 |
| 생성 초안과 국소 보정 | ComfyUI | 직접 사용 가능한 다른 node 기반 UI | workflow, model, control, seed를 파일로 기록 가능 |
| 컷 배열 검수 | Krita contact sheet 또는 작은 Python 스크립트 | 수동 배열 | 한 장씩이 아니라 시퀀스로 실패를 찾음 |

Blender 자체는 GPL로 배포되지만, Blender로 만든 artwork에는 GPL이 적용되지 않는다고 Blender 문서가 설명한다. Krita와 OpenToonz의 코드 라이선스, 그리고 ComfyUI 노드·checkpoint·LoRA·adapter의 라이선스는 서로 별도다. 도구가 공개 소스라는 사실만으로 입력 이미지, 모델 가중치, 결과물의 사용 조건이 자동으로 해결되지는 않으므로, 실제 실습에서는 각 배포물의 모델 카드와 라이선스 파일을 개별 확인한다.

## Part 7 개편 제안

### P7-5.2의 역할을 좁힌다

P7-5.2의 중심 질문은 다음으로 고친다.

> 생성 도구를 조합해 하나의 웹툰 컷을 다시 만들 수 있게 기록하려면, 캐릭터·공간·국소 보정·편집의 기준 원본을 어떻게 나누어야 하는가?

현재의 9컷 OpenPose/IP-Adapter 매트릭스와 간이 rig는 본문 중간의 **제어 신호별 한계 검증**으로 유지한다. 이것들을 최종 웹툰 결과로 제시하지 않는다.

### 새 실습 산출물 후보

새로 만들어야 할 핵심 예제는 최소 4컷의 짧은 시퀀스다. 이 시퀀스에는 아래 파일이 한 묶음으로 있어야 한다.

```text
character-sheet.png
episode-01-board.md
panel-01..04-blockout.(blend 또는 제어 이미지)
panel-01..04-workflow.json
panel-01..04-selected.png
panel-01..04-repair-mask-*.png
episode-01-contact-sheet.png
episode-01-continuity-review.md
episode-01-lettered.png
```

Python 예제는 생성 모델을 새로 구현하는 대신, 위 묶음의 누락 파일과 컷별 기록을 검사하고 contact sheet를 만드는 역할로 둔다. 입력 파일, 컷 ID, 필수 기록값을 바꾸면 검증 결과가 달라져야 한다. 이 방식은 GPU 환경이 없는 독자도 실습의 재현성·연속성 검수 부분을 실행할 수 있게 한다.

### 현재 자산의 처리 원칙

- 현재 P7-5.2의 미채택 pose·참조·Canny·LLM blockout 실험 자산은 모두 삭제했다.
- 실패 원인과 후보 비교는 이 조사 노트에만 유지하며, 이를 웹툰 완성 또는 자연스러운 리깅의 근거로 쓰지 않는다.

## 원고에 남길 출처

- [ComfyUI ControlNetApply 문서](https://docs.comfy.org/built-in-nodes/ControlNetApply): ControlNet 제어 이미지를 condition에 적용하는 node 역할.
- [ComfyUI inpainting 튜토리얼](https://docs.comfy.org/tutorials/basic/inpaint): mask 기반 국소 보정 흐름.
- [IP-Adapter 공식 저장소](https://github.com/tencent-ailab/IP-Adapter): 이미지 prompt와 ControlNet 조합, SDXL FaceID 계열의 연구 구현 후보.
- [InstantID 공식 저장소](https://github.com/instantX-research/InstantID): 얼굴 embedding과 landmark 조건을 함께 쓰는 실험 후보. 필요한 추가 가중치의 사용 조건을 별도 확인해야 함.
- [ComfyUI InstantID 확장](https://github.com/cubiq/ComfyUI_InstantID): SDXL, InsightFace, 추가 ControlNet을 요구하며 maintenance-only 상태인 구현 사례.
- [Blender render 개요](https://docs.blender.org/manual/en/2.90/render/introduction.html): 카메라·조명·재질, render layer/pass, NPR 렌더의 역할.
- [Blender Freestyle 소개](https://docs.blender.org/manual/en/2.90/render/freestyle/introduction.html): mesh와 깊이 정보를 기반으로 하는 선 렌더.
- [Blender Camera Rigs](https://docs.blender.org/manual/id/3.6/addons/camera/camera_rigs.html): focal length와 tracking을 animation 가능한 카메라 rig 사례.
- [Blender Grease Pencil animation](https://docs.blender.org/manual/en/2.93/grease_pencil/animation/introduction.html): frame, deformation, armature animation.
- [Blender Grease Pencil Armature Modifier](https://docs.blender.org/manual/en/5.0/grease_pencil/modifiers/deform/armature.html): bone weight를 이용한 drawing 변형.
- [OpenToonz Plastic Tool](https://opentoonz.readthedocs.io/en/latest/create_animations_using_plastic_tool.html): mesh와 skeleton 기반 drawing 변형.
- [Krita animation 문서](https://docs.krita.org/en/user_manual/animation.html): keyframe, timeline, onion skin을 통한 직접 보정 보조.
- [Blender 라이선스 설명](https://docs.blender.org/manual/en/3.2/getting_started/about/license.html): 프로그램 라이선스와 artwork의 구분.
- [Wan2.2 공식 저장소](https://github.com/Wan-Video/Wan2.2): Wan-Animate의 reference image, pose·face video 입력과 animation/replacement 실행 경로. 확인일: 2026-08-01.
- [One-to-All Animation 공식 저장소](https://github.com/ssj9596/One-to-All-Animation), [1.3B checkpoint](https://huggingface.co/MochunniaN1/One-to-All-1.3b_2), [Wan 1.3B Diffusers base](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B-Diffusers): reference image와 driving video 기반 image pose transfer, cartoon benchmark, 16 GB T4 안내와 2026-08-02 파일 용량 확인. 현재 8 GB에서는 전체 GPU 적재형 공식 구현을 실행 후보로 두지 않음.
- [StableAnimator 공식 저장소](https://github.com/Francis-Rings/StableAnimator): reference image와 정렬 pose sequence, face mask 보정, 512x512/576x1024 추론 설정과 frame 수 축소 안내. 8 GB 실행 가능 여부는 별도 probe 필요. 확인일: 2026-08-02.
- [SteadyDancer 공식 저장소](https://github.com/MCG-NJU/SteadyDancer): reference image, driving video, aligned positive/negative pose 조건 및 cartoon/full-body X-Dance benchmark. Wan 14B 기반이라 현재 8 GB 실행 후보에서 제외. 확인일: 2026-08-02.
- [SCAIL-2 공식 저장소](https://github.com/zai-org/SCAIL-2): reference image·foreground mask·driving/pose video·frame mask video를 함께 받는 SCAIL-14B animation/replacement 경로. 확인일: 2026-08-02.
- [FLUX.2 공식 저장소](https://github.com/black-forest-labs/flux2): Klein 4B의 single/multiple reference image editing, Apache-2.0 및 약 8 GB VRAM 안내. 정지 컷의 다중 reference editing 후보이며 pose transfer 품질은 별도 검증 필요. 확인일: 2026-08-02.
- [Qwen-Image 공식 저장소](https://github.com/QwenLM/Qwen-Image) 및 [Qwen-Image-Edit 안내](https://github.com/QwenLM/Qwen-Image/blob/main/Qwen-Image-Edit.md): Qwen-Image-Edit-2511은 character consistency와 새 viewpoint 생성을 개선 대상으로 제시한다. 자연어 재포즈의 후보이며 관절 정확성은 검증 필요. 확인일: 2026-08-02.
- [DiffSynth-Studio 공식 저장소](https://github.com/modelscope/DiffSynth-Studio) 및 [Qwen-Image-Edit-2511 저 VRAM 예제](https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/qwen_image/model_inference_low_vram/Qwen-Image-Edit-2511.py): transformer·text encoder·VAE를 disk/CPU offload하고 CUDA에서 bf16 계산하는 multi-image edit 경로. 8 GB에서의 실제 peak VRAM과 출력 품질은 별도 실험 필요. 확인일: 2026-08-02.
- [FLUX.1 Kontext dev 저 VRAM 예제](https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux/model_inference_low_vram/FLUX.1-Kontext-dev.py): `kontext_images` reference image에서 표정·행동·장소를 바꾸는 공식 8 GB offload 경로. 2026-08-02 probe는 주 가중치 23.8 GB 다운로드 후 PNG 생성 전 중단했으므로 실행 가능 여부와 품질은 미판정이다. 확인일: 2026-08-02.
- [JoyAI-Image-Edit 저 VRAM 예제](https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/joyai_image/model_inference_low_vram/JoyAI-Image-Edit.py): 단일 edit image와 자연어 지시를 받아 CPU offload로 실행하며 최소 4 GB VRAM을 명시한다. 공식 모델 파일 목록상 transformer 32.5 GB와 UNet shards 17.5 GB 등을 내려받아야 하므로, 현 장비의 즉시 반복 검증 후보에서는 제외한다. 확인일: 2026-08-02.
- [FireRed-Image-Edit 공식 저장소](https://github.com/FireRedTeam/FireRed-Image-Edit): portrait consistency와 multi-image fusion을 목표로 하며, 최적화 inference의 30 GB VRAM 요구를 명시한다. 현 장비의 실행 후보에서는 제외. 확인일: 2026-08-02.
- [Index-AniSora 공식 저장소](https://github.com/bilibili/index-anisora): animation 특화 video generation, pose/depth/line art guidance, V3.1의 12 GB VRAM 안내 및 Apache-2.0 배포. 확인일: 2026-08-01.
- [LTX-Video 공식 저장소](https://github.com/Lightricks/ltx-video): image-to-video, multiple keyframe, style LoRA와 13B pose/depth/Canny control 모델. 확인일: 2026-08-01.
- [CharaConsist 공식 저장소](https://github.com/Murray-Wang/CharaConsist): FLUX.1 기반 training-free character/background consistency와 정지 컷 생성 예제. 확인일: 2026-08-01.
- [VNCCS 공식 저장소](https://github.com/AHEKOT/ComfyUI_VNCCS): character·clothing·emotion·sprite 분리 workflow와 full-body 기준 이미지 권장. 확인일: 2026-08-01.
- [Diffusers AnimateDiff 문서](https://huggingface.co/docs/diffusers/api/pipelines/animatediff): 개인화 SD 모델용 motion adapter와 ControlNet을 결합한 video-to-video pipeline, 원본 video와 control image sequence 조건. 확인일: 2026-08-01.
- [AnimateDiff motion adapter v1.5.2](https://huggingface.co/guoyww/animatediff-motion-adapter-v1-5-2): SD 1.5용 motion adapter와 fp16 가중치 크기 1.82 GB. 확인일: 2026-08-01.
- [Animagine XL 4.0 모델 카드](https://huggingface.co/cagliostrolab/animagine-xl-4.0): SDXL 기반 애니메이션 화풍 모델, 태그 기반 prompt 형식, OpenRAIL++ 사용 조건 및 손·손가락 같은 해부학 한계. 확인일: 2026-08-01.
- [Diffusers LoRA training 문서](https://huggingface.co/docs/diffusers/main/training/lora): frozen base model에 adapter를 추가하는 LoRA 학습, SDXL 지원 및 training/inference 기록 항목. 확인일: 2026-08-01.
- [kohya_ss SDXL LoRA 가이드](https://github.com/bmaltais/kohya_ss/blob/master/docs/LoRA/top_level.md): SDXL의 1024 기준 해상도, UNet-only 권고와 최소 12 GB GPU 권고. 현재 8 GB 장비의 SDXL LoRA 기본안에서 제외하는 근거. 확인일: 2026-08-01.
- [PhotoMaker V2 모델 카드](https://huggingface.co/TencentARC/PhotoMaker-V2/blob/main/README.md) 및 [공식 저장소](https://github.com/TencentARC/PhotoMaker): 여러 ID 입력의 training-free customization, SDXL/ControlNet 결합, Apache-2.0 표기와 최소 11 GB GPU 안내. 만화 face sheet에서의 품질은 별도 검증 필요. 확인일: 2026-08-01.
- [ControlNet 공식 저장소](https://github.com/lllyasviel/ControlNet) 및 [ControlNet 1.1 모델명](https://github.com/lllyasviel/ControlNet-v1-1-nightly): SD 1.5의 OpenPose, depth, line/Canny 같은 구조 조건과 8 GB low-VRAM 모드의 공개 구현. 각 조건은 identity가 아닌 공간·구도 입력으로 사용. 확인일: 2026-08-02.
- [Diffusers Stable Diffusion inpainting 문서](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/inpaint): mask와 prompt를 이용한 국소 보정, 전용 inpainting checkpoint 사용 권고. 확인일: 2026-08-02.
- [Stable Diffusion v1.5 Inpainting 모델 카드](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-inpainting): SD 1.5 계열 mask 기반 inpainting 후보. base model과 사용 조건을 별도 확인. 확인일: 2026-08-02.
- [ControlVideo 공식 저장소](https://github.com/YBYBZhang/ControlVideo): human pose, Canny, depth ControlNet 조건을 video sequence에 적용하는 training-free video generation 구현. 확인일: 2026-08-01.
- [MimicMotion 공식 저장소](https://github.com/Tencent/MimicMotion): reference image, driving video, DWPose 기반 confidence-aware human motion video generation. 확인일: 2026-08-01.
- [MusePose 공식 저장소](https://github.com/TMElyralab/MusePose): reference image와 DWPose sequence의 pose alignment, 얼굴·복잡 의상·배경 flicker 한계 및 모델 사용 조건. 확인일: 2026-08-01.
- [X-Dyna 공식 저장소](https://github.com/bytedance/x-dyna): 기준 이미지, driving video, pose·face 제어를 결합한 human image animation과 16 frame 최소 20 GB VRAM 조건. 확인일: 2026-08-01.
- [OpenPose 공식 저장소](https://github.com/CMU-Perceptual-Computing-Lab/openpose): body·hand·face·foot를 포함하는 135 keypoint 출력과 JSON 좌표·confidence 형식. 동작 입력의 누락 검수에 사용. 확인일: 2026-08-01.
- [MMPose 공식 저장소](https://github.com/open-mmlab/mmpose): 133-keypoint whole-body, hand, face 추정과 3D mesh recovery 연구 구현. 2D 전신 검수 후보. 확인일: 2026-08-01.
- [MMPose inference guide](https://github.com/open-mmlab/mmpose/blob/main/docs/en/user_guides/inference.md): whole-body model alias와 추론 입력 흐름. 확인일: 2026-08-01.
- [Blender Rigify limb controls](https://docs.blender.org/manual/en/4.1/addons/rigging/rigify/rig_types/limbs.html): limb IK의 end control과 회전 제어. 자체 제작 동작 원본의 rig 설계 참고. 확인일: 2026-08-01.
- [SMPL-X 공식 저장소](https://github.com/vchoutas/smplx) 및 [라이선스](https://github.com/vchoutas/smplx/blob/main/LICENSE): body·face·hand 모델과 비상업 연구·교육·예술 용도의 제한, 재배포 금지 조건. 공개 기본 실습 자산에서는 제외. 확인일: 2026-08-01.
- [MotionGPT 공식 저장소](https://github.com/OpenMotionLab/MotionGPT): text-driven 3D motion generation 연구 구현과 MIT 코드 라이선스. 확인일: 2026-08-01.
- [ChatPose 프로젝트](https://yfeng95.github.io/ChatPose/): 텍스트·이미지에서 SMPL pose parameter를 생성하는 LLM 연구 경로. 확인일: 2026-08-01.

## 다음 구현 순서

1. P7-5.2에는 현재 자연스러운 포즈를 입증하는 생성 예제가 없음을 유지하고, 미채택 실험을 다시 본문 자산으로 되돌리지 않는다.
2. 가상의 자체 제작 캐릭터와 서로 다른 장소·카메라를 포함한 4컷 콘티를 기준으로 character sheet와 shot intent 계약을 만든다.
3. 표정·대화 컷은 `face-first` 또는 `camera/background-first`로 시작한다. 다이내믹 전신 컷은 AnimateDiff + ControlNet을 먼저 실행해 기준 캐릭터, driving video, pose·depth 조건을 결합한 짧은 후보 영상을 만든다.
4. OpenPose 또는 MMPose 전신 keypoint는 driving 영상과 후보 frame에서 손목·발·얼굴의 누락을 검사하는 데만 쓰며, keypoint만으로 동작을 통과시키지 않는다.
5. 통과 frame의 pose·face·depth·camera 기록을 남기고 정지 컷 생성과 국소 inpaint를 적용한다. character sheet·배경·화풍 게이트는 별도로 통과시킨다. Blender는 driving 원본을 만들 수 없을 때만 선택적으로 쓴다.
6. 4컷 contact sheet, 연속성 판정표, Python 검증 스크립트와 실제 출력 이미지를 함께 만든 뒤에만 P7-5.2의 주 예제로 채택한다.
