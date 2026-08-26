# P7-5.8 텍스트 모션으로 12개 OpenPose 키프레임 준비하기

> Section ID: `P7-5.8`
> Version: `v2026.08.27`

정지 pose 한 장은 현재 P7-5.2의 OpenPose 구조 입력으로 만들 수 있다. 걷기처럼 시간에 따라 팔·다리·골반의 관계가 바뀌는 동작은 pose 이미지 12장을 각각 따로 생성하면 접지와 이동 순서가 쉽게 끊긴다. 이 절은 **텍스트에서 먼저 3D 관절 모션을 만들고, 그 시퀀스에서 12개 2D OpenPose 키프레임을 뽑기 위한 실험 조건**을 준비한다. 여기서는 모델 가중치를 아직 내려받거나 실행하지 않는다.

## 1. 키프레임은 완성 이미지가 아니라 시간 순서가 있는 구조 입력이다

이 실험의 첫 출력은 사람이 그려진 PNG가 아니라 프레임마다 관절 좌표가 있는 모션 배열이다. MoMask는 텍스트와 모션 길이를 `설명#포즈 수` 형식으로 받아, 생성 모션을 `(프레임 수, 22, 3)` 관절 배열과 stick-figure/BVH 결과로 저장한다. 따라서 생성된 3D 관절을 같은 camera로 2D에 투영한 뒤에만 각 프레임을 OpenPose guide로 쓸 수 있다. [MoMask 공식 구현](https://github.com/centersymmetry/momask){: target="_blank" rel="noopener noreferrer"}

```mermaid
flowchart LR
    A["텍스트: 앞으로 걷는다"] --> B["MoMask 3D 모션\n48 × 22 × 3"]
    B --> C["4프레임 간격 추출\n12개 키프레임"]
    C --> D["같은 camera로 2D 투영"]
    D --> E["OpenPose body-only\nPNG·좌표 JSON"]
    E --> F["이미지 생성의\n프레임별 구조 입력"]
```

OpenPose는 이 경로에서 동작을 새로 만드는 모델이 아니다. 프레임별 `pose_keypoints_2d`를 JSON으로 기록하고 body·face·hand를 각각 분리할 수 있는 2D 키포인트 형식으로 쓴다. 첫 실험은 동작·카메라 검수를 분리하기 위해 body-only를 사용한다. [OpenPose JSON 출력 형식](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/02_output.md){: target="_blank" rel="noopener noreferrer"}

## 2. 8GB GPU에서는 작은 모션 경로부터 확인한다

| 후보 | 이 실험에서 보는 기능 | 8GB에서의 처리 |
| --- | --- | --- |
| MoMask | 텍스트와 포즈 수로 3D 관절 모션 생성 | 첫 실행 후보. batch 1, 48포즈 한 시퀀스만 실행 |
| MDM 50-step | text-to-motion의 비교 기준, in-between 편집 | MoMask가 실행 또는 길이 제어에서 막힐 때의 비교 후보 |
| LLaMA 기반 MotionGPT | text·초기 pose·key pose 조건을 포함한 모션 생성 | 별도 대형 언어 모델 가중치가 필요하므로 8GB 첫 실험에서는 제외 |

MoMask 공개 문서는 길이를 포즈 수로 지정하고 4의 배수로 맞추며, `12` 같은 짧은 길이도 받을 수 있다고 설명한다. 하지만 최소 VRAM 수치는 공개하지 않는다. 따라서 이 절은 “8GB에서 동작한다”는 결론을 미리 쓰지 않고, **batch 1의 짧은 단일 시퀀스가 실제로 생성되는가**를 첫 확인 항목으로 둔다. [MoMask 실행 안내](https://github.com/centersymmetry/momask/blob/main/README.md){: target="_blank" rel="noopener noreferrer"}

MDM은 단일 CUDA GPU 환경을 전제로 하며, 50-step 모델과 `motion_length` 제어를 제공한다. 다만 출력 길이가 초 단위이므로 정확히 12포즈를 요청하는 첫 비교에는 MoMask보다 한 단계 뒤에 둔다. [MDM 공식 구현](https://github.com/GuyTevet/motion-diffusion-model){: target="_blank" rel="noopener noreferrer"}

LLaMA 기반 MotionGPT 구현은 별도 LLaMA 가중치 준비를 요구한다. 이는 key pose 조건을 다루는 후속 후보로는 유용하지만, 8GB에서 “짧은 보행 시퀀스가 나오는가”만 먼저 확인하는 이 실험의 첫 설치 대상으로 늘리지 않는다. [MotionGPT 구현의 가중치 준비 안내](https://github.com/qiqiApink/MotionGPT){: target="_blank" rel="noopener noreferrer"}

## 3. 걷기는 48포즈를 만들고 12장을 뽑는다

MoMask의 예시 기준 모션은 20fps다. 12포즈를 직접 생성하면 약 0.6초여서 한 보행 주기의 발 접지·체중 이동을 읽기에는 짧을 수 있다. 이번 준비에서는 먼저 48포즈를 생성하고 네 프레임마다 하나를 뽑는다. 이렇게 하면 약 2.4초의 원 모션에서 12개의 균등한 구조 키프레임을 얻는다.

| 항목 | 고정 값 | 이유 |
| --- | --- | --- |
| 텍스트 입력 | `A person walks forward#48` | 텍스트와 길이를 한 파일에 고정 |
| 원 모션 | 48 poses, 20fps | 보행의 시간 흐름을 남김 |
| 키프레임 | 12장 | 이미지 생성에 전달할 구조 수 |
| 추출 인덱스 | `0, 4, 8, …, 44` | 시작·끝 규칙이 명시된 균등 추출 |
| 입력 구조 | body-only OpenPose | 얼굴·손 세부가 동작 해석을 덮지 않게 분리 |

12장은 걷기 동작의 완성도나 캐릭터 identity를 보장하지 않는다. 첫 검수에서는 두 발의 접지, 좌우 다리 교대, 팔의 반대 흔들림, 골반의 연속 이동, 프레임 간 갑작스러운 사지 교체만 본다. 캐릭터 얼굴·착장·화풍은 P7-5.1·P7-5.2의 참조가 맡으며, 키프레임 모션이 이 역할을 대체하지 않는다.

## 4. 실행 전에 입력 파일과 샘플링 계획을 고정한다

아래 준비 코드는 가중치·데이터셋을 설치하지 않고 MoMask 입력 파일과 실험 계획 JSON만 `.tmp/`에 만든다. 실제 추론은 다음 단계에서 별도 실행 기록으로 남긴다.

<details id="p7-5-8-momask-preparation" class="aibook-lazy-source" data-source="/AiBook/assets/part-07/chapter-05/p7_5_8_prepare_momask_walk_keyframes.py" data-language="python">
<summary>MoMask 보행 키프레임 준비 코드 보기</summary>
<div class="aibook-lazy-source__body">펼치면 Python 원문을 불러옵니다.</div>
</details>

```bash
.venv/bin/python docs/assets/part-07/chapter-05/p7_5_8_prepare_momask_walk_keyframes.py
```

생성되는 `experiment-plan.json`에는 아직 `prepared_not_run` 상태만 남는다. MoMask 결과의 실제 배열 모양, peak VRAM, 실행 시간, 카메라 투영 규칙, OpenPose 매핑표는 추론이 끝난 뒤에만 result JSON으로 기록한다.

## 체크리스트

- 텍스트 모션 모델의 3D 관절 시퀀스와 OpenPose의 2D 구조 guide를 서로 다른 단계로 구분했는가?
- 12포즈를 직접 생성하는 대신 48포즈에서 12장을 추출하는 이유를 설명할 수 있는가?
- 8GB 조건에서 아직 확인하지 않은 최소 VRAM·실행 시간·출력 품질을 결론처럼 쓰지 않았는가?
- 첫 실행의 batch, 프레임 수, seed, 모델·가중치 버전, peak VRAM을 result JSON에 남길 준비가 되었는가?
- body-only 키프레임이 얼굴 identity·착장·화풍의 기준을 대체하지 않는가?

## 출처와 참고 자료

- centersymmetry, [MoMask 공식 구현](https://github.com/centersymmetry/momask){: target="_blank" rel="noopener noreferrer"}, 확인일: 2026-08-27.
- Guy Tevet et al., [MDM: Human Motion Diffusion Model 공식 구현](https://github.com/GuyTevet/motion-diffusion-model){: target="_blank" rel="noopener noreferrer"}, 확인일: 2026-08-27.
- Zhang et al., [MotionGPT 구현](https://github.com/qiqiApink/MotionGPT){: target="_blank" rel="noopener noreferrer"}, 확인일: 2026-08-27.
- CMU Perceptual Computing Lab, [OpenPose JSON output](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/02_output.md){: target="_blank" rel="noopener noreferrer"}, 확인일: 2026-08-27.
