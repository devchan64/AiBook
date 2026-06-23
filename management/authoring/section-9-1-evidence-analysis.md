# 9.1 근거 검토 메모

이 문서는 `docs/chapters/chapter-09/section-01.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 3.3과 4.3의 표현(representation) 설명을 이어 받아, 이미지 인식(image recognition) 사례에서 표현 학습(representation learning)이 왜 중요해졌는지 설명합니다.
- 수작업 특징(hand-crafted features)과 학습된 표현(learned representation)을 구분합니다.
- AlexNet을 2010년대 딥러닝 확산의 대표 전환점으로 소개하되, 딥러닝의 최초 사례나 LLM의 직접 조상처럼 과장하지 않습니다.
- CNN(convolutional neural network)은 직관 수준으로만 설명하고, 합성곱·풀링·역전파 수식은 후속 딥러닝 장으로 넘깁니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Krizhevsky et al., `ImageNet Classification with Deep Convolutional Neural Networks` | `.tmp/section-3-1-evidence/alexnet-imagenet-2012.pdf`, `.tmp/section-3-1-evidence/alexnet-imagenet-2012.txt` | ImageNet 120만 학습 이미지, 1000개 범주, 6천만 파라미터, 65만 뉴런, 5개 convolutional layers, GPU 구현, 두 GTX 580 GPU 학습 |
| LeCun, Bengio, Hinton, `Deep learning` | `.tmp/user-claim-evidence/lecun-bengio-hinton-deep-learning.html` | 딥러닝을 여러 층의 표현 학습으로 설명, 시각적 물체 인식과 객체 검출 성능 개선, AlexNet을 컴퓨터 비전의 전환점으로 평가 |
| Bengio, Courville, Vincent, `Representation Learning: A Review and New Perspectives` | `.tmp/section-3-3-evidence-bengio-representation-learning.html` | 머신러닝 성능이 데이터 표현에 크게 의존한다는 설명 |
| Saez Trigueros et al., `Face Recognition: From Traditional to Deep Learning Methods` | `.tmp/section-3-1-case-studies/face-recognition-traditional-to-deep-learning.pdf`, `.txt` | 전통적 얼굴인식 방법의 hand-crafted features, geometry-based, holistic, feature-based, hybrid methods와 CNN 기반 deep learning methods로의 이동 |
| `docs/chapters/chapter-03/section-03.md` | 저장소 본문 | 규칙 기반 접근과 표현 학습의 기본 구분 |
| `docs/chapters/chapter-04/section-03.md` | 저장소 본문 | 특징(feature), 표현(representation), 파라미터(parameter)의 기본 위치 |
| `management/authoring/deep-learning-paradigm.md` | 저장소 관리 메모 | 이미지 인식 사례를 LLM 직접 계보가 아닌 딥러닝 패러다임 확산의 주변 근거로 다루는 기준 |

## 확인한 원문 위치

- `.tmp/section-3-1-evidence/alexnet-imagenet-2012.txt`
  - 120만 학습 이미지와 1000개 범주, 6천만 파라미터, 65만 뉴런, 5개 convolutional layers와 GPU 구현: 13-21행 부근
  - ImageNet 1500만 이미지, 2만2000개 범주와 대규모 데이터 배경: 37-40행, 73-78행 부근
  - 현재 GPU와 최적화된 2D convolution 구현이 큰 CNN 학습을 가능하게 했다는 설명: 53-60행 부근
  - GPU 메모리 한계, 두 GPU 분산 학습, GPU 병렬화: 140-156행 부근
  - 5-6일 동안 두 NVIDIA GTX 580 3GB GPU에서 훈련했다는 설명: 338행 부근
  - 첫 convolutional layer가 학습한 kernels와 색/방향 선택 특성: 295-300행, 396-401행 부근
  - 마지막 hidden layer의 feature activation으로 이미지 유사성을 볼 수 있다는 설명: 408-416행 부근
- `.tmp/user-claim-evidence/lecun-bengio-hinton-deep-learning.html`
  - 딥러닝이 여러 층으로 여러 추상 수준의 표현을 학습한다는 설명: 329행, 354행, 869행 부근
  - 시각적 물체 인식과 객체 검출 성능 개선 설명: 329행, 869행 부근
  - AlexNet이 컴퓨터 비전 커뮤니티에서 딥러닝 채택을 촉발한 돌파구였다는 참고문헌 주석: 1714행 부근
- `.tmp/section-3-3-evidence-bengio-representation-learning.html`
  - 머신러닝 알고리즘의 성공이 데이터 표현에 크게 의존한다는 초록: 29-40행, 178행 부근
- `.tmp/section-3-1-case-studies/face-recognition-traditional-to-deep-learning.txt`
  - 전통적 방법이 hand-crafted features와 전통적 ML 기법에 기반했다는 설명: 10-18행, 50-70행 부근
  - 전통적 얼굴인식 방법이 geometry-based, holistic, feature-based, hybrid methods를 포함한다는 설명: 122-140행 부근
  - CNN 기반 방법이 얼굴인식에서 많이 쓰이고, deep learning methods가 특징을 학습한다는 설명: 617-637행 부근

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 이미지 인식은 조명, 자세, 배경, 가림, 범주 다양성 때문에 수작업 규칙으로 쓰기 어렵다 | 얼굴인식 survey의 전통적 방법과 real-world variation 설명, 자체 예시 | 유지. 자체 예시는 개념 설명용 |
| 수작업 특징은 사람이 볼 단서를 미리 정하는 방식이다 | 얼굴인식 survey의 hand-crafted features, geometry/holistic/feature-based methods | 유지 |
| 표현 학습은 입력을 모델이 다루기 좋은 표현으로 바꾸는 과정을 데이터에서 함께 배우는 접근이다 | Bengio et al. 표현 학습 리뷰, 3.3/4.3 기존 본문 | 유지 |
| 딥러닝은 여러 층의 표현을 학습한다 | LeCun et al. Nature 리뷰 | 유지 |
| CNN은 이미지의 지역 패턴을 여러 층에서 조합하는 구조로 입문 설명 가능하다 | LeCun et al. Nature 리뷰의 convolutional nets 설명, AlexNet의 convolutional layer 구조 | 유지하되 수식 설명은 제외 |
| AlexNet은 대규모 데이터, 깊은 CNN, GPU, 학습 기법이 결합된 전환점이다 | AlexNet 논문과 Nature 리뷰 참고문헌 주석 | 유지 |
| 이미지 인식 사례는 LLM의 직접 계보가 아니다 | `management/authoring/deep-learning-paradigm.md`의 도메인 경계 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 3.3 | 규칙 기반 접근과 표현 학습의 개념적 차이 |
| 4.3 | 특징, 표현, 파라미터의 모델링 용어 정리 |
| 9.1 | 이미지 인식 사례를 통해 딥러닝 표현 학습의 전환점 설명 |
| 9.2 | 객체 검출과 음성 생성 사례를 딥러닝 패러다임 확산의 주변 근거로 설명 |
| 9.3 | LLM의 직접 계보와 주변 근거 구분 |
| Part 4 | CNN, 역전파, 손실 함수, 옵티마이저, GPU 병렬 처리의 세부 구조 |

## 보수화한 표현

- “AlexNet이 딥러닝을 시작했다”라고 쓰지 않았습니다. 신경망과 CNN 연구는 이전에도 있었고, AlexNet은 대표적 전환점으로만 설명했습니다.
- “이미지 인식이 LLM을 만들었다”라고 쓰지 않았습니다. 이미지 인식은 딥러닝 패러다임 확산의 주변 근거로 제한했습니다.
- “CNN이 사람의 시각을 그대로 재현한다”라고 쓰지 않았습니다. 이미지의 지역 패턴을 계층적으로 다루는 계산 구조로만 설명했습니다.
- “모델 내부 표현이 항상 사람이 이해하는 단계로 나뉜다”라고 쓰지 않았습니다. 픽셀-모서리-부분-범주 흐름은 입문용 단순화로 표시했습니다.
- “수작업 특징은 낡고 무가치하다”라고 쓰지 않았습니다. 안정적 조건과 적은 데이터에서는 여전히 유용할 수 있다고 남겼습니다.

## 남은 검토 사항

- CNN의 합성곱, 풀링, ReLU, feature map은 Part 4에서 별도 수식과 그림으로 다룹니다.
- GPU 병렬 처리의 자세한 설명은 Part 4의 GPU와 병렬 처리 절에서 AlexNet, CUDA/GPU 자료를 추가로 확인해 다룹니다.
- 9.2에서는 YOLO, WaveNet, Deep Voice를 각각 직접 계보가 아니라 딥러닝 패러다임 확산 사례로 검토합니다.
