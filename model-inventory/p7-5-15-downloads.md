# P7-5.15 미실험군 가중치 준비

확인일: 2026-09-18. 모델 가중치 사전 다운로드이며 환경 설치·추론·동작 품질 검증과 구분한다. MoMask도 기존에 실행한 기준 모델이 아니라 **미실험 비교군**이다.

| 구성 | 원본 | 용도 |
| --- | --- | --- |
| MoMask HumanML3D | [공식 다운로드 스크립트](https://github.com/centersymmetry/momask/blob/main/prepare/download_models.sh) | RVQ, masked/residual transformer, 길이 예측기, 정규화 통계 |
| CLIP ViT-B/32 | [OpenAI CLIP](https://github.com/openai/CLIP/blob/main/clip/clip.py) | MoMask 텍스트 인코더 |
| Kimodo-SOMA-RP-v1.1 | [NVIDIA](https://huggingface.co/nvidia/Kimodo-SOMA-RP-v1.1) | 3D 모션과 접촉 정보 생성 |
| LLM2Vec MNTP·supervised 어댑터 | [McGill-NLP](https://huggingface.co/McGill-NLP/LLM2Vec-Meta-Llama-3-8B-Instruct-mntp) | Kimodo 텍스트 인코더 구성 |
| Meta-Llama-3-8B-Instruct | [Meta](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) | LLM2Vec 기반 모델. 현재 계정의 접근 권한 부족으로 다운로드 차단 |
| StableAnimator 기본 추론 구성 | [FrancisRing](https://huggingface.co/FrancisRing/StableAnimator) | Animation 가중치, SVD 구성요소, DWPose, Antelopev2 |
| facexlib 검출·파싱 | [공식 구현](https://github.com/xinntao/facexlib) | StableAnimator의 얼굴 정렬·파싱 보조 모델 |

Hugging Face 파일은 `.tmp/download/huggingface/hub/`의 고정 revision snapshot에 저장한다. 직접 배포 파일은 `.tmp/download/artifacts/weight-p7-5-15-*/`에 보관한다. StableAnimator는 공식 기본 추론이 읽는 SVD 구성요소를 받으며 중복되는 FP16 복사본·단일 통합 체크포인트와 데모 영상은 제외한다. MoMask는 이번 48프레임 HumanML3D 실험에 필요한 묶음을 받으며 KIT·평가 전용 자료는 포함하지 않는다.

로컬 다운로드 기록은 `.tmp/download/sources/p7-5-15/*.json`과 각 artifacts 폴더의 `download-record.json`에 둔다. 출처·revision·파일 선택·크기·SHA-256을 기록하고, Hugging Face LFS의 원본 SHA-256 또는 CLIP의 공개 SHA-256이 있으면 대조한다. MoMask ZIP은 CRC 검사 후 압축을 해제하며 로컬 SHA-256을 기록한다. 이 기록만으로 pickle 계열 가중치의 실행 안전성이나 추론 성공을 보장하지 않는다.

## 이용 조건 확인

- Kimodo-SOMA-RP-v1.1 가중치: 저장소의 NVIDIA Open Model License 확인. 코드 라이선스와 가중치 라이선스를 구분한다.
- MoMask·CLIP: 공식 코드의 MIT 라이선스를 확인했다. MoMask 의존 데이터·신체 모델의 조건은 코드 라이선스로 대신하지 않는다.
- StableAnimator의 SVD 기반 모델은 동봉된 Stability AI Community License를 확인했다. StableAnimator 코드의 MIT 표기만으로 전체 가중치의 조건을 판단하지 않는다.
- InsightFace의 Antelopev2 사전학습 가중치는 공식 안내상 비상업 연구용이다. [InsightFace 이용 조건](https://github.com/deepinsight/insightface#license)을 별도로 추적한다.
- Llama 기반 모델은 계정 접근 승인과 해당 모델 조건 확인이 필요하다. 미러로 접근 제한을 우회하지 않는다.

현재는 다운로드 후보이며 공개 실습 자산 생성·배포 채택 전에는 각 의존 모델의 조건을 함께 검토한다. FramePack은 후속 비교 후보로 남기고 이번 주 실험 경로의 다운로드에는 포함하지 않는다.

## 다운로드 결과

- MoMask HumanML3D 묶음과 CLIP, StableAnimator 기본 추론 가중치 및 얼굴 처리 보조 가중치 다운로드 완료.
- Kimodo 본체와 LLM2Vec 어댑터 2개 다운로드 완료. Meta Llama 기반 모델은 계정 접근 권한 부족으로 차단되어 Kimodo 로컬 실행 준비는 부분 완료.
- 추론 및 환경 설치는 실행하지 않음. 개별 파일 해시와 고정 revision은 위 로컬 기록에 보존.

## 기본 추론 경로의 추가 의존성 점검

2026-09-18 공식 소스와 다운로드 기록을 대조했다.

- StableAnimator의 `FaceRestoreHelper`는 초기화 때 ParseNet을 로드하고, 이후 `FaceModel`이 BiSeNet으로 교체한다. 기본 코드에서 발생할 추가 다운로드를 막기 위해 `parsing_parsenet.pth`를 추가로 다운로드하고 SHA-256을 기록했다. 출처: [facexlib FaceRestoreHelper](https://github.com/xinntao/facexlib/blob/master/facexlib/utils/face_restoration_helper.py), [파싱 모델 로더](https://github.com/xinntao/facexlib/blob/master/facexlib/parsing/__init__.py).
- StableAnimator의 기존 23개 snapshot 파일은 존재·크기를 재확인했다. 얼굴 검출 ResNet50, BiSeNet, ParseNet의 별도 파일도 보관한다. 실제 실행 때 각 라이브러리의 경로·캐시를 로컬 파일로 연결해야 한다.
- MoMask `gen_t2m.py`의 RVQ·masked/residual transformer·길이 예측기·정규화 통계·CLIP은 확보했다. 해당 생성 경로에는 KIT 가중치나 정량 평가용 evaluator·GloVe가 필수는 아니다. BVH 템플릿 등 저장소 동봉 자료는 코드 환경 준비 때 함께 확보해야 한다.
- Kimodo의 LLM2Vec 어댑터가 참조하는 Meta Llama 3 기반 모델은 재확인 시에도 접근이 거부됐다. 본체·어댑터만으로 완전한 로컬 텍스트 추론 준비가 끝난 것은 아니다. SOMA 관절·기본 스키닝 자료는 Kimodo 저장소의 assets를 사용하며, 별도 고급 SOMA layer 렌더링 의존성은 이번 기본 관절·포즈 경로에 채택하지 않았다.
- 이번 확인은 모델 파일 의존성 대조다. 세 구현의 소스 설치, Python 패키지 설치, 로컬 경로 연결 및 모델 로딩 검증은 아직 수행하지 않았다.

## 2026-09-19 최초 실행

- 공식 MoMask·StableAnimator 소스를 `.tmp/download/sources/p7-5-15/`에 확보하고 기존 `.venv`의 패키지를 재사용했다. 모델 가중치는 중복 복사하지 않고 로컬 링크로 연결했다.
- MoMask의 48·96프레임 걷기/달리기 12개를 RTX 5070 Laptop GPU에서 생성했다. 실행 리비전·모델 해시·프레임·메모리 기록은 `docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-stableanimator-v1/momask-v*/result.json`에 있다. 공식 BVH 경로는 NumPy 비호환으로 제외했고 생성 함수와 원 관절 복원을 사용했다.
- Kimodo의 Llama 기반 모델 접근은 다시 확인했으나 여전히 `GatedRepoError`다. 다른 배포본으로 대체하지 않았다.
- StableAnimator 기본 추론 소스는 기존 환경에서 import가 가능했다. ONNX Runtime의 CUDA 제공자는 `libcublasLt.so.13` 부재로 CPU로 대체 실행되며, 영상 모델은 PyTorch CUDA 경로를 사용한다. 최종 상태는 `docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-stableanimator-v1/stableanimator-walk-v1/result.json`에 기록한다.

- StableAnimator 걷기·달리기 각 32프레임 생성 완료. `stableanimator-{walk,run}-v1/result.json`에 각각 270.36/260.24초, 최대 PyTorch 할당 약 5.51GiB를 기록했다. 판정은 별도 `review.json`: 걷기 부분 성공, 달리기 신체·포즈 유지 실패.

## MoMask v1 폐기 결정

2026-09-19 사용자 지시로 MoMask v1과 파생 StableAnimator 걷기 산출물을 삭제했다. 위 최초 실행의 개수·시간은 당시 이력이다. 현재는 MoMask v2와 파생 달리기를 보존하며 모델 가중치는 삭제하지 않는다. 폐기 기록: `docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-stableanimator-v1/discarded-experiments.json`.

## MoMask v3 실행

2026-09-19 기존 MoMask 가중치를 재사용해 96프레임 걷기 3개를 생성했다. 추가 다운로드 없음. v2와 가중치 해시·소스·환경·생성 설정을 대조했다. 자산은 `docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-v3/`에 모았다. 부유·하강은 개선됐지만 전진 이동 부족으로 완전한 성공으로 판정하지 않는다.

## 실험 묶음 최종 폐기

2026-09-19 사용자 지시로 MoMask v3와 기존 MoMask·StableAnimator 묶음을 실패로 폐기하고 폴더 전체를 삭제했다. 위 실행 경로·수치는 삭제 전 이력이며 현재 자산 경로가 아니다. 가중치는 보존했다. 후속 framing-v2는 원 입력 삭제로 실행 불가 상태다. [폐기 기록](../management/authoring/part-07-p7-5-15-discarded-experiments.md).

## MoMask v4 새 실험

2026-09-19 기존 가중치로 새 프롬프트 두 조건·3시드 총 6개 모션을 생성했다. 추가 다운로드 없음. 자산은 `docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-v4/`에 모았다. 원 관절·실행 해시·공통 구도 영상·높이/이동/발 속도 진단을 보관한다. 기존 두 실험 묶음의 폐기는 유지한다.

## StableAnimator v3 전진 실험

사용자 지시로 v2 준비 자료를 폐기하고 MoMask v4 `travel-10107`의 움직이는 32프레임을 입력으로 구성했다. 가중치는 재사용하며 추가 다운로드 없음. 새 자산은 `docs/assets/part-07/chapter-05/sec-15/2026-09-19-stableanimator-travel-v3/`에 모았다. 최초 실행은 GPU 메모리 부족으로 실패해 `attempts/01-oom.json`을 보존했고, 다른 GPU 작업을 중단하지 않고 메모리 할당 설정을 조정해 재시도한다. 최종 상태는 `result.json`과 별도 검수 기록을 기준으로 한다.

- v3 재시도 완료: 331.99초, 최대 PyTorch 할당 약 5.48GiB. 가로 이동과 마지막까지 전신 유지가 관측됐으나 참조 재킷·머리 형태 변화와 첫 프레임 잔상이 남았다. `review.json`에서 동작 전달과 캐릭터 유지 판정을 구분했다.

## StableAnimator v4 참조 개선 실험

사용자 지시로 v3를 폐기했다. 새 v4는 기존 정면·오른쪽 측면 참조를 시작 포즈에 근사 정렬하고 얼굴 임베딩이 영벡터가 아닌지 검사한다. 같은 전진 모션·시드의 두 조건이며 가중치는 재사용하고 추가 다운로드는 없다. 자산은 `docs/assets/part-07/chapter-05/sec-15/2026-09-19-stableanimator-reference-v4/`에 모았다.

- v4 두 조건 완료: 정면 267.15초·측면 262.01초, 최대 PyTorch 할당 약 5.48GiB. 측면 초반 머리 형태는 개선됐으나 두 조건 모두 전체 캐릭터 유지 실패로 검수했다.


## StableAnimator 실험 최종 폐기

2026-09-19 사용자 지시로 v4 정면·측면 실험도 캐릭터 외형·팔다리 구조 유지 실패로 폐기하고 자산 폴더 전체를 삭제했다. 위 v1~v4 실행·보관 경로는 과거 이력이며 현재 활성 자산이 아니다. 모델 인벤토리의 v4 실행 소스 참조를 제거했다. MoMask v4, 공용 참조 원본과 다운로드 가중치는 유지한다. [폐기 기록](../management/authoring/part-07-p7-5-15-discarded-experiments.md).
