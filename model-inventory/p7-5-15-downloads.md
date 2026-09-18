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
