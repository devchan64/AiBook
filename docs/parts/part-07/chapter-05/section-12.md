# P7-5.12 보충학습: ANNY Blender 리그에 MoMask 애니메이션 적용하기

> Section ID: `P7-5.12`
> Version: `v2026.09.28`

[5.11](section-11.md)에서 준비한 몸체에는 아직 걸음의 순서가 없다. 이번에는 **생성형 모션 모델이 만든 움직임을 그 몸체에 적용하는 과정**을 살펴본다. ‘사람이 걷는다’는 설명에서 시간에 따른 자세를 생성하는 일과, 생성된 자세를 ANNY 리그가 표현하게 하는 일을 구분하는 것이 핵심이다.

먼저 MoMask가 무엇을 생성하는지 이해하고, 관절 좌표를 포즈 맵으로 확인한다. 이어 축·기준 자세·본 대응을 맞춰 리그를 움직이고 결과를 검수한다. 포즈 맵은 관절을 읽는 별도 예제이며 리타기팅의 필수 입력은 아니다. [5.13](section-13.md)에서는 이와 같은 리그의 렌더 이미지를 캐릭터의 자세를 바꾸는 안내로 사용한다.

## 1. 생성형 모델은 시간에 따른 동작을 만든다

MoMask는 텍스트를 조건으로 3D 사람 동작을 생성하는 모델이다. 설명용으로 ‘사람이 앞으로 걷는다’는 문장을 생각해 보자. 필요한 출력은 한 장의 걷는 그림이 아니라, 골반이 이동하고 팔다리가 교대하는 **자세의 시간 순서**다. 같은 설명을 해도 가능한 걸음의 모양은 여러 가지다. 문장은 동작의 의미를 알려 주지만 모든 관절의 위치를 직접 지정하지는 않는다.

MoMask는 동작을 학습된 작은 코드인 **모션 토큰**의 여러 층으로 표현한다. 생성할 때 텍스트를 조건으로 비어 있는 기본 토큰을 반복해서 채우고, 추가 층의 토큰을 예측해 세부 표현을 더한다. 이 표현을 복원해 모션 데이터를 얻는다. 이미지의 픽셀을 생성하는 모델과 달리 여기서 생성 대상은 몸의 움직임이다. [MoMask 논문](https://arxiv.org/abs/2312.00063){: target="_blank" rel="noopener noreferrer" }

걷기라는 의미가 반영됐는지와 발이 자연스럽게 닿는지는 따로 확인해야 한다. 이 절에서는 이미 생성된 걷기 데이터를 사용해 연결 과정을 살펴본다. 아래 코드는 새 텍스트 모션 추론이 아니라 **저장된 모션을 시각화하고 리그에 적용하는 예제**다. 앞의 문장은 개념 설명용이며 사본의 실제 생성 프롬프트를 인용한 것이 아니다.

### 모션은 위치를, 리그는 몸체와 변형 규칙을 제공한다

MoMask의 HumanML3D 관절 출력은 프레임마다 22개 관절의 3차원 위치를 담는다. ANNY 기준 리그에는 104개 본과 각 본을 따라 변형되는 표면이 있다. 하나는 시간에 따른 관절 위치이고, 다른 하나는 몸을 조절하는 구조다. 두 배열의 번호가 같다고 같은 부위를 뜻하지 않는다.

| 입력 | 사용할 정보 | 그대로 복사할 수 없는 정보 |
| --- | --- | --- |
| MoMask `joints` | 골반의 이동, 관절 사이 방향, 시간 순서 | ANNY 본의 회전값·이름·부모 관계 |
| ANNY Blender 리그 | 체형, 본 길이, 기준 자세, 스키닝 가중치 | 걷기 타이밍과 발 접촉 순서 |
| 대응 프로필 | 원본 관절과 대상 본의 관계, 좌표 변환, 전달 방식 | 입력에 없는 손가락 움직임과 독립적인 시선 |

동작을 서로 다른 골격에 옮기는 작업을 **리타기팅(retargeting)**이라고 한다. 이번 방식은 관절 위치에서 부위별 방향을 계산하고, 그 방향을 대상 리그가 표현할 수 있는 회전으로 바꾼다. ANNY의 체형·본 길이·가중치를 유지하므로 원본 관절과 대상 관절의 절대 위치가 모든 프레임에서 일치하는 방식은 아니다.

```mermaid
flowchart LR
    A["MoMask 관절 모션\n프레임 × 22 × 3"] --> C["축·크기·관절 대응 확인"]
    B["5.11 ANNY 리그\n본·기준 자세·가중치"] --> C
    C --> D["부위 방향 → 본 회전\n골반 변위 → 리그 이동"]
    D --> E["Blender 키프레임 저장"]
    E --> F["동일 리그 다방향 렌더\n접지·교대·변형 검수"]
```

### HumanML3D의 22관절은 무엇을 뜻하는가

여기서 ‘HumanML22’는 HumanML3D에서 사용하는 22관절 구성을 짧게 부르는 표현이다. HumanML3D는 텍스트와 사람의 3D 모션을 연결한 데이터셋이며, 22관절은 SMPL 골격 구성을 따른다. `new_joints`의 관절 위치와 `new_joint_vecs`의 모션 특징 표현은 구분한다. 이 예제는 MoMask가 복원해 저장한 `joints` 위치 배열을 사용한다. [HumanML3D 공식 설명](https://github.com/EricGuoICT/HumanML3D)

`joints[29, 20]`은 0부터 세었을 때 30번째 프레임의 왼쪽 손목 `(x, y, z)`다. 좌우는 화면이 아니라 **움직이는 사람 자신의 좌우**다. 카메라가 돌아가도 왼쪽 손목의 번호는 바뀌지 않는다.

| 번호 | 관절 | 번호 | 관절 |
| --- | --- | --- | --- |
| 0 | 골반 | 11 | 오른발 앞부분 |
| 1 | 왼쪽 엉덩이 | 12 | 목 |
| 2 | 오른쪽 엉덩이 | 13 | 왼쪽 쇄골 |
| 3 | 척추 1 | 14 | 오른쪽 쇄골 |
| 4 | 왼쪽 무릎 | 15 | 머리 |
| 5 | 오른쪽 무릎 | 16 | 왼쪽 어깨 |
| 6 | 척추 2 | 17 | 오른쪽 어깨 |
| 7 | 왼쪽 발목 | 18 | 왼쪽 팔꿈치 |
| 8 | 오른쪽 발목 | 19 | 오른쪽 팔꿈치 |
| 9 | 척추 3 | 20 | 왼쪽 손목 |
| 10 | 왼발 앞부분 | 21 | 오른쪽 손목 |

발 앞부분 한 점은 발가락 각각의 관절이 아니며, 머리 한 점도 눈·코·귀의 위치가 아니다. 그러므로 22관절을 자세한 얼굴·손·발의 제어 신호로 그대로 사용할 수는 없다. 이 번호와 연결 관계는 아래 예제 코드의 `NAMES`·`CHAINS`, ANNY 대응은 저장한 프로필과 대조할 수 있다.

### 프레임 수와 재생 속도도 입력 조건이다

MoMask 원 모션을 20fps로 만들고 모든 프레임을 4fps로 재생하면 동작 시간은 다섯 배로 늘어난다. 이 절의 60프레임은 20fps에서 3초, 4fps에서 15초다. 현재 관리 생성 경로는 전체 프레임을 유지하면서 결과 fps를 4로 기록하므로, 원 모션 속도와 비교할 때 이 차이를 분리해야 한다.

원래 시간 흐름을 유지하려면 20fps를 유지하거나, 프레임을 추출하는 간격에 맞춰 출력 fps를 정해야 한다. 프레임을 줄이면 빠른 발 교대 구간을 놓칠 수 있으므로 전체 모션 검수와 전달용 프레임 구성은 구분한다.

## 2. 22관절에서 OpenPose 형식의 포즈 맵 만들기

OpenPose의 COCO18은 코·목·팔다리·눈·귀를 포함하는 18개 슬롯을 사용한다. 여기서 선택한 것은 COCO18이며 BODY_25나 COCO 데이터셋의 17관절 배열과 같지 않다. JSON의 `pose_keypoints_2d`는 관절마다 `x, y, c`를 차례로 담는다. 실제 검출 결과에서 `c`는 신뢰도지만, 아래 합성 예제에서는 점의 제공 여부를 1 또는 0으로 표시한다. [OpenPose 공식 출력 형식](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/02_output.md)

### 관절 이름을 대응시키고 카메라 평면에 투영한다

| COCO18 슬롯 | 예제의 HumanML22 입력 | 주의점 |
| --- | --- | --- |
| 0 코, 1 목 | 15 머리, 12 목 | 코는 머리 중심으로 대신한다. |
| 2·3·4 오른쪽 어깨·팔꿈치·손목 | 17·19·21 | 오른쪽 팔의 순서를 유지한다. |
| 5·6·7 왼쪽 어깨·팔꿈치·손목 | 16·18·20 | 왼쪽 팔의 순서를 유지한다. |
| 8·9·10 오른쪽 엉덩이·무릎·발목 | 2·5·8 | 발 앞부분은 이 배열에서 제외한다. |
| 11·12·13 왼쪽 엉덩이·무릎·발목 | 1·4·7 | 골반 중심과 엉덩이 관절을 구분한다. |
| 14~17 눈·귀 | 대응 없음 | 좌표와 제공 여부를 0으로 남긴다. |

예제는 원본 관절의 Y축을 위로 해석하고, 수평 회전각 35도의 직교 카메라로 투영한다. 직교 투영은 거리에 따른 원근 크기 변화를 생략하는 방식이다. 60프레임 전체의 범위를 한 번 계산해 512×512 화면에 맞추므로 프레임마다 인물의 크기나 중심을 다시 맞추지 않는다. 화면 좌표는 아래로 갈수록 y가 커지므로 위아래 방향도 뒤집는다.

### 생성 코드와 확인할 출력

- [generate_pose_maps.py](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/generate_pose_maps.py){ .aibook-code-preview }: 관절 선택, 고정 카메라 투영, PNG·GIF와 좌표 JSON 저장.
- [pose-maps.json](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/pose-maps.json): 원 모션·코드 해시, 카메라 조건, 번호 대응과 프레임별 18×3 값.

저장소 루트에서 NumPy와 Pillow가 설치된 Python으로 실행한다. 기존 결과를 덮어쓰지 않도록 새 출력 폴더를 지정한다.

```bash
python docs/assets/part-07/chapter-05/sec-12/anny-momask-walk/code/generate_pose_maps.py \
  --motion docs/assets/part-07/chapter-05/sec-12/anny-momask-walk/inputs/mannequin-motion.npz \
  --output-dir .tmp/humanml22-pose-maps \
  --yaw 35
```

`--yaw 90`으로 다른 폴더에 생성하면 같은 동작이 다른 방향으로 보인다. 팔과 다리가 겹치는 순간을 비교하자. 이 코드는 사진에서 관절을 검출하는 OpenPose 추론을 실행하지 않는다. 이미 알고 있는 3D 관절을 화면으로 투영하므로 가려진 관절도 그리며, 이미지 속 가시성이나 깊이 순서를 판정하지 않는다. 특정 ControlNet 등에서 요구하는 색·선·얼굴·손 표현과 일치하는지는 해당 모델의 전처리 방식으로 별도 확인해야 한다. 신경망 내부의 관절 확률맵이나 PAF도 생성하지 않는다.

### 생성 결과를 비교한다

| 번호를 표시한 HumanML22 입력 | 같은 카메라의 COCO18식 포즈 맵 |
| --- | --- |
| ![HumanML22 관절 번호, 30번째 프레임](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/humanml22-numbered.png) | ![합성 포즈 맵, 같은 프레임](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/pose-0029.png) |

아래는 같은 변환을 전체 60프레임에 적용한 4fps GIF다. 색 선은 부위의 연결을 구분하는 교육용 표현이며 피부·옷·조명은 생성하지 않는다.

![HumanML22에서 투영한 합성 포즈 맵, 60프레임](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/pose-map-4fps.gif)

다음은 같은 실행에서 저장한 PNG 산출물이다. 파일 번호는 0부터 시작한다. 카메라와 화면 배율이 고정된 상태에서 팔·다리의 위치가 어떻게 달라지는지 비교한다. 네 장은 전체 60프레임 중 표본이며, 동작의 연속성은 위 GIF와 함께 확인한다.

| 1번째 프레임 · `pose-0000.png` | 21번째 프레임 · `pose-0020.png` |
| --- | --- |
| ![생성 포즈 맵 1번째 프레임](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/pose-0000.png) | ![생성 포즈 맵 21번째 프레임](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/pose-0020.png) |

| 41번째 프레임 · `pose-0040.png` | 60번째 프레임 · `pose-0059.png` |
| --- | --- |
| ![생성 포즈 맵 41번째 프레임](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/pose-0040.png) | ![생성 포즈 맵 60번째 프레임](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/pose-map-example/pose-0059.png) |

`slime-workflow`의 `render_asset.py`는 다른 경로를 사용한다. 원 MoMask 관절 대신 **리타기팅된 ANNY 본의 위치**를 Blender 카메라에 투영하고, 머리 중심을 코 대신 사용한 14점 좌표를 `openpose-keypoints.json`에 기록한다. 이 기록 자체는 색 선 이미지도, 완전한 OpenPose 검출 JSON도 아니다. 이번 예제는 그 선택·투영 원리를 원본 모션으로 분리해 보여 주며, 뒤에서 살펴볼 신체 렌더 GIF와 동일한 카메라·골격 좌표라고 간주하지 않는다.

## 3. 5.11의 어느 파일을 연결할 것인가

포즈 맵으로 관절의 이동을 확인했으면, 같은 모션을 몸체가 있는 리그에 옮길 준비를 한다.

5.11에 보존한 [등록 리그 사본](../../../assets/part-07/chapter-05/sec-11/anny-neutral-v4/anny-raw-rig.blend)과 [속성에서 다시 생성하는 예제](section-11.md)는 같은 학습 목적을 갖지만 파일 내부 객체 이름까지 같지는 않다.

| 경로 | Armature 객체 | 메시 객체 |
| --- | --- | --- |
| 등록 자산 사본 `anny-raw-rig.blend` | `AnnyAttributesRig` | `AnnyAttributesBody` |
| 5.11 독립 예제의 `body.blend` | `Rig` | `Body` |

검토한 `slime-workflow` 리타기팅 진입점은 등록 사본의 객체 이름을 사용한다. 따라서 예제 출력 파일을 그대로 넣으면 객체를 찾는 부분부터 맞춰야 한다. 실제 연결 시에는 객체 이름뿐 아니라 본 이름·부모 관계·기준 자세·스키닝 가중치가 기대한 구조인지 함께 검사해야 한다. 파일 확장자가 같다는 이유만으로 입력 호환성을 가정하지 않는다.

실행 기록에는 최소한 원 모션 파일 해시, 리그 파일 해시, 대응 프로필·계산 코드의 버전, 선택한 프레임, 원 모션 fps와 출력 fps를 남긴다. 현재 제작 코드의 방식 식별자는 `position-reference-transport-v3`다. 과거 리그를 재생하거나 렌더링할 때는 당시 모션과 리그를 유지하며, 최신 계산 방식으로 다시 만든 것처럼 기록하지 않는다.

## 4. 먼저 축과 이동 크기를 맞춘다

현재 모션 생성 기록의 HumanML3D 좌표는 Y축이 위이고, 5.11의 Blender 리그는 Z축이 위다. 검토한 프로필은 `(x, y, z)`를 `(x, -z, y)`로 바꿔 위쪽 축을 맞춘다. 단순히 Y와 Z만 교환하면 좌표계의 방향까지 달라질 수 있으므로 부호를 포함한 변환을 기록한다. 프로필의 행렬은 직교성과 행렬식도 검사한다.

체형 차이는 이동 크기에도 영향을 준다. 구현은 원본의 왼쪽 엉덩이–무릎 구간과 대상의 대응 본 위치 사이 길이를 비교해 배율을 얻는다. 원본은 모션 전체에서 해당 길이의 평균을 사용한다. 이 배율은 골반의 첫 프레임 대비 변위에 적용한다. 리그 자체의 다리를 프레임마다 늘리는 처리는 아니다.

예를 들어 원본에서 골반이 앞으로 이동하면 대상 리그의 위치에도 그 변화가 전달된다. 첫 프레임 위치를 빼는 것은 시작점을 맞추기 위한 처리이며, 이후의 전진 이동을 모두 지워 제자리 동작으로 만드는 처리와 다르다. 상하 변위도 남기므로 프레임마다 발을 바닥으로 끌어내리는 보정과 구분한다.

좌표 변환 기록에는 변환 전후 관절, 대상 기준 본 위치, 이동 배율, 구간별 방향과 각도를 남긴다. 팔 방향이 예상과 다르면 렌더링 결과만 보고 판단하기 전에 이 중간 자료를 확인할 수 있다.

## 5. 기준 자세 차이와 실제 움직임을 구분한다

기준 자세는 ‘움직이지 않을 때의 골격 방향’을 정의한다. 모션의 첫 프레임이 이미 팔을 흔들거나 무릎을 굽힌 상태라면 이를 중립 자세로 간주할 수 없다. 현재 구현은 출처가 고정된 MoMask BVH 템플릿의 골격 배치로 원본 기준을 정의하고, ANNY 리그의 기준 본 위치·회전과 대응시킨다.

| 부위·전달 방식 | 계산의 목적 | 필요한 구분 |
| --- | --- | --- |
| 팔다리·발의 방향 전달 | 대응 끝점 사이 방향을 따라가게 한다. | 원본 T 자세와 대상의 내려간 팔 자세 차이를 동작으로 중복 적용하지 않는다. |
| 골반·척추 등 기준 대비 변화 전달 | 원본 기준 방향에서 얼마나 달라졌는지를 대상 기준 회전에 적용한다. | 관절 배치 자체의 기울기와 실제 동작 회전을 구분한다. |
| 대응하지 않는 본 | 부모 움직임을 상속하며 기준 로컬 자세를 유지한다. | 손가락 동작을 새로 복원한 것으로 해석하지 않는다. |

관절 두 점을 잇는 방향만으로는 팔의 축을 중심으로 얼마나 비틀렸는지 모두 알 수 없다. 두 개의 독립된 방향을 얻을 수 있는 구간에서는 함께 회전을 계산하고, 한 방향만 있는 구간에서는 이전 방향에서 현재 방향으로 필요한 최소 회전을 연속해서 전달한다. 이는 관측하지 못한 비틀림을 완전히 복구했다는 뜻이 아니다.

회전은 부모 본부터 적용하고, 본의 회전과 리그 전체 이동을 프레임별 키프레임으로 저장한다. 대상 본의 길이와 스케일은 유지한다. 현재 구현에는 동작별 팔 제한, 자동 주먹 자세, 메시 스무딩, 매 프레임 접지 이동이 추가되지 않는다. 따라서 자세를 맞추는 계산과 접지·표면 변형의 품질을 별도로 확인해야 한다.

## 6. 같은 신체로 생성된 걷기 결과와 사본

다음 GIF는 완료 작업의 `down_left` 방향 PNG 60장을 흰 배경에 합성해 4fps GIF로 묶은 것이다. 중간 프레임을 보간하지 않았다. GIF는 자동 반복되므로 마지막에서 처음으로 돌아갈 때의 차이도 함께 관찰한다. 원 MoMask의 20fps 기준으로는 3초 분량이며 이 검토 GIF에서는 15초 동안 느리게 재생된다.

![ANNY 걷기 결과: 60프레임, 4fps, 15초 반복](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/walking-4fps.gif)

<details markdown="1">
<summary>Blender에서 편집하거나 원본 파일 받기</summary>

Blender 파일은 브라우저에서 직접 실행할 수 없으므로 편집용 사본으로 제공한다. 생성 결과는 위 GIF에서 확인할 수 있다.

[Blender 사본 받기](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/mannequin.blend) · [GLB 사본 받기](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/mannequin.glb)

</details>

| 사본·근거 | 확인할 내용 |
| --- | --- |
| [원본 경로와 SHA-256 기록](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/source-record.json) | 완료 작업과 복사 파일의 대응, 5.11 리그와의 일치 |
| [입력 관절 NPZ](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/inputs/mannequin-motion.npz) | 60프레임의 22관절 위치와 고정 기준 골격 |
| [리타기팅 진단](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/review-metrics.json) | 전달 방식, 이동 배율, 방향·회전 진단 |
| [루프 측정](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/loop-validation.json) | 시작·끝 표면 좌표 차이와 검토 필요 상태 |
| [좌표 변환 기록](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/coordinate-transform.json) | 원본 좌표에서 대상 리그로 옮긴 근거 |

루프 기록의 `endpoint_max_error_m`은 약 **0.264m**다. 첫 프레임과 마지막 프레임의 표면 정점 좌표를 비교한 최대 절댓값이며, 발 미끄러짐의 측정치나 자연스러움 점수가 아니다. 따라서 이 사본은 리그 애니메이션 연결 결과로 소개하며 매끄러운 반복 루프의 완성 사례로 확정하지 않는다.

## 7. 리그가 움직인 뒤 확인할 장면

| 확인 대상 | 볼 장면 | 문제가 보이면 먼저 대조할 자료 |
| --- | --- | --- |
| 전진 이동 | 골반과 몸 전체가 같은 방향으로 이동하는가 | 원 골반 변위, 좌표 변환, 이동 배율 |
| 좌우 교대 | 다리가 겹친 뒤 올바른 쪽이 다시 드러나는가 | 원본 관절 번호와 대상 본 대응, 같은 프레임의 다방향 렌더 |
| 접지 | 지지 발이 바닥 위에서 미끄러지거나 파고드는가 | 발 높이·수평 이동, 원 모션과 리타기팅 후 위치 |
| 신체 변형 | 팔꿈치·무릎·어깨가 찢어지거나 심하게 찌그러지는가 | 본 회전·길이, 가중치, 표면 변형 |
| 시간 연속성 | 방향이 갑자기 뒤집히거나 마지막에서 튀는가 | 프레임별 회전 변화, fps, 루프 시작·끝 |

3D 리그에서는 동일한 몸을 여러 카메라로 렌더링할 수 있어, 한 측면에서 가려진 팔다리를 다른 방향으로 확인할 수 있다. 그러나 가림이 3D로 계산된다는 사실이 원본 모션의 타당성이나 피부 변형 품질을 보장하지는 않는다.

현재 구현은 선언한 목표 방향과 실제 본 방향의 차이, 회전 오차, 프레임 간 변화 등을 기록한다. 원본 방향과 대상 방향이 다른 것이 체형·기준 자세를 고려한 의도된 차이인지, 전달 과정의 오류인지 구분해서 읽어야 한다. 작은 계산 오차를 자연스러운 걷기의 합격 점수로 사용하지 않는다.

## 8. 저장된 모션에서 애니메이션을 다시 만드는 코드

걷기 결과에서 각 단계의 역할을 확인했으면, 필요한 범위에서 실행 코드와 기록을 살펴본다.

<details markdown="1">
<summary>구현 확인: 생성기 연결과 실행 방법</summary>

### 실제 생성기에서 단계가 연결되는 위치

이 절은 `slime-workflow`의 리타기팅 구현과 완료된 걷기 결과를 바탕으로 한다. 2026-09-27 생성 작업의 `neutral_v4` 리그 해시가 5.11 등록 사본과 같은 것을 확인했다. 기록은 같은 몸체를 사용했다는 근거이며 모션 품질의 판정은 아니다.

`slime-workflow`의 관리 생성 진입점은 `generators/momask/run_managed_generation.py`다. 이 파일은 모션 생성, 포즈 렌더링, ANNY 렌더링을 별도 프로세스로 연결한다. 신체 애니메이션 경로를 따라가면 다음 역할로 나뉜다.

| 실행 파일·설정 | 실제로 맡는 작업 |
| --- | --- |
| `generate_motion.py` | MoMask 추론과 관절 복원 후 `motion.npz`에 `joints`와 특징 배열을 저장한다. |
| `render_anny_frames.py` | 원 모션 검사, 기준 ANNY 리그 해시 확인, 실행 폴더에 입력·프로필·계산기 사본을 준비한다. |
| `humanml22-anny-retarget.yaml` | 관절 쌍·대상 본·축 변환·기준 골격·전달 방식을 선언한다. |
| `position_retarget.py` | 관측한 부위 방향에서 대상 본 회전을 계산한다. |
| `templates/retarget_loop.py` | Blender에서 리그를 열고 프레임별 회전·이동 키프레임을 적용한다. |
| `templates/render_asset.py` | 저장된 애니메이션 리그를 방향별로 렌더링하고 시작·끝 차이를 기록한다. |

리타기팅 단계는 `mannequin.blend`와 애니메이션을 포함한 `mannequin.glb`를 저장한다. 이는 5.11의 정적 신체 파일과 구분되는 출력이다. 계산 근거는 `coordinate-transform.json`·NPZ, `review-metrics.json`, `retarget-diagnostics.npz`에 남는다. 렌더 단계의 `loop-validation.json`은 시작·끝 표면 차이 측정 기록이며 자동으로 루프 품질을 승인하는 파일이 아니다.

입력 준비 코드가 만드는 `contacts`는 현재 0으로 채운 자리표시 배열이다. 이를 실제 발 접촉 추론 결과로 읽으면 안 된다. 리타기팅 후 다시 추출한 `mannequin-motion.npz` 역시 대상 ANNY 골격에서 얻은 파생 좌표이므로 원 MoMask 관절과 이름·출처를 구분한다.

예제 파일의 **내용보기**를 누르면 원고 안에서 코드를 펼쳐 읽고 복사하거나 내려받을 수 있다. 실행 진입점은 입력 검사부터 Blender·GLB 저장까지 연결하며, 나머지 구현은 완료 작업의 코드 사본이다.

- [generate_animation.py](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/generate_animation.py){ .aibook-code-preview }: 입력 검사, 실행 폴더 준비, 리타기팅 단계 실행과 결과 기록.
- [position_retarget.py](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/position_retarget.py){ .aibook-code-preview }: 관절 방향에서 대상 본 회전을 계산하는 공통 계산기.
- [retarget-profile.yaml](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/retarget-profile.yaml){ .aibook-code-preview }: 관절·본 대응, 기준 골격과 좌표 변환 설정.
- [retarget_loop.py](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/retarget_loop.py){ .aibook-code-preview }: Blender 리그에 프레임별 회전·이동 키프레임 적용.
- [retarget_audit.py](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/retarget_audit.py){ .aibook-code-preview }: 좌표 변환과 리타기팅 근거 기록.
- [run_stage.py](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/run_stage.py){ .aibook-code-preview }: Blender Python 단계 실행과 종료 상태 반환.
- [render_asset.py](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/render_asset.py){ .aibook-code-preview }: 선택 실행하는 네 방향 PNG 렌더링과 루프 측정.

파일들은 같은 `code` 폴더에 내려받고 [라이선스](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/MOMASK-TEMPLATE-LICENSE.txt)도 함께 보존한다. 생성 결과는 새 폴더에만 저장하며 기존 폴더가 있으면 중단한다.

실행용 Python에는 `numpy`, `PyYAML`이 필요하다. `--blender-python`에는 5.11에서 준비한 `bpy==4.5.3`, NumPy, PyYAML이 설치된 Python 실행 파일을 지정한다. 아래 명령은 저장소 루트에서 실행한다.

```bash
python docs/assets/part-07/chapter-05/sec-12/anny-momask-walk/code/generate_animation.py \
  --motion docs/assets/part-07/chapter-05/sec-12/anny-momask-walk/inputs/mannequin-motion.npz \
  --rig docs/assets/part-07/chapter-05/sec-11/anny-neutral-v4/anny-raw-rig.blend \
  --blender-python .venv-anny-blender/bin/python \
  --output-dir .tmp/anny-walk-replay \
  --fps 4
```

먼저 `--dry-run`을 붙이면 입력 배열·경로와 해시를 확인하고 파일을 만들지 않는다. Blender 내부의 객체·본 호환성은 실제 적용 단계에서 확인한다. 기본 fps는 원 모션 시간 기준인 20이며, 위 예제의 `--fps 4`는 사본의 느린 재생 조건을 맞춘다. fps는 프레임의 재생 속도만 바꾸며 관절 배열을 보간하지 않는다.

`--render`를 추가하면 사본 렌더러로 네 방향 PNG와 루프 측정을 만든다. 이 선택 단계는 CUDA/Cycles 환경을 전제로 한다. 기본 실행은 애니메이션 파일 생성까지이며 GIF 변환은 포함하지 않는다. `generation-record.json`에 입력·리그·코드 해시와 실행 상태를 남기고 단계별 로그도 보존한다.

책의 예제는 등록 리그의 `AnnyAttributesRig`·`AnnyAttributesBody` 이름을 사용한다. 5.11 독립 예제로 만든 `Rig`·`Body` 파일을 쓰려면 객체 이름과 골격 호환성을 먼저 맞춰야 한다. 입력은 HumanML22의 Y-up 관절을 가정하며 `contacts`의 0은 접촉 정보가 없는 자리표시다.

검증에서는 저장된 60프레임과 5.11 리그 사본으로 이 진입점을 실행해 Blender·GLB 생성을 확인했다. 검증 범위와 산출물 해시는 [실행 검증 기록](../../../assets/part-07/chapter-05/sec-12/anny-momask-walk/code/verification.json)에 남겼다. 새 MoMask 추론과 CUDA 다방향 재렌더링은 이 검증에 포함하지 않았다.

직접 바꿔 볼 항목은 **fps**다. 서로 다른 출력 폴더에 `--fps 4`와 `--fps 20`으로 저장하고 같은 자세 순서가 다른 속도로 재생되는지 비교하자. 자세의 품질과 재생 속도를 구분하는 연습이다.

</details>

## 체크리스트

- MoMask의 동작 생성과 리타기팅의 골격 변환을 구분할 수 있는가?

- MoMask 관절 위치와 ANNY 본 회전이 서로 다른 표현임을 설명할 수 있는가?
- HumanML22와 COCO18의 번호 대응, 누락된 눈·귀와 머리 대체점을 구분했는가?
- 합성 포즈 맵을 실제 OpenPose 검출 결과나 깊이 정보로 오해하지 않았는가?
- 축 변환과 골반 이동 배율을 기록하고 전진 이동을 유지했는가?
- 모션 첫 프레임을 기준 자세로 오해하지 않았는가?
- 등록 리그와 5.11 예제 출력의 객체 이름·본 구조를 확인했는가?
- 원 모션 fps와 렌더링·재생 fps를 구분했는가?
- 방향 일치·접지·표면 변형·시간 연속성을 따로 검수했는가?

## 출처와 참고 자료

- Guo et al., [MoMask: Generative Masked Modeling of 3D Human Motions](https://arxiv.org/abs/2312.00063){: target="_blank" rel="noopener noreferrer" }, 텍스트 조건의 모션 토큰 생성 방식. 확인일: 2026-09-28.

- [MoMask 공식 구현](https://github.com/centersymmetry/momask){: target="_blank" rel="noopener noreferrer" }, 관절 모션과 20fps 출력 설명. 공식 자료 확인: 2026-09-20.
- [ANNY 공식 구현](https://github.com/naver/anny){: target="_blank" rel="noopener noreferrer" }, 신체 리그와 자세 표현. 공식 자료 확인: 2026-09-27.
- 로컬 구현 검토: `slime-workflow`의 `position_retarget.py`, `humanml22-anny-retarget.yaml`, `templates/retarget_loop.py`, `run_managed_generation.py`, 확인일: 2026-09-27. 본문의 전달 방식·좌표·fps 설명은 이 구현에 대한 설명이며 모든 리타기팅 도구의 공통 규칙이 아니다. 소스 해시는 저장소 관리 기록에 보존한다.
