# 9.2 근거 검토 메모

이 문서는 `docs/chapters/chapter-09/section-02.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 9.1의 이미지 인식(image recognition)과 표현 학습(representation learning)을 이어 받아, 딥러닝 패러다임이 객체 검출(object detection), 음성 생성(speech generation), 음성 합성(TTS)으로 확산된 흐름을 설명합니다.
- YOLO, WaveNet, Deep Voice를 LLM의 직접 계보가 아니라 딥러닝 확산의 주변 근거로 정리합니다.
- 알고리즘 구현보다 문제 재구성의 관점을 설명합니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Redmon et al., `You Only Look Once: Unified, Real-Time Object Detection` | `.tmp/section-9-2-evidence/yolo-1506.02640.pdf`, `.txt` | 객체 검출을 bounding boxes와 class probabilities를 예측하는 single neural network/regression problem으로 재구성, end-to-end 최적화, real-time 처리 |
| van den Oord et al., `WaveNet: A Generative Model for Raw Audio` | `.tmp/section-9-2-evidence/wavenet-1609.03499.pdf`, `.txt` | raw audio waveform을 생성하는 fully probabilistic autoregressive model, TTS 적용, parametric/concatenative baseline보다 자연스러운 음성 보고 |
| Arik et al., `Deep Voice: Real-time Neural Text-to-Speech` | `.tmp/section-9-2-evidence/deep-voice-1702.07825.pdf`, `.txt` | TTS 파이프라인의 주요 구성요소를 neural network로 구성, real-time inference 필요성 |
| `management/authoring/deep-learning-paradigm.md` | 저장소 관리 메모 | YOLO, WaveNet, Deep Voice를 LLM 직접 계보가 아닌 딥러닝 패러다임 확산 사례로 분류 |
| `docs/chapters/chapter-09/section-01.md` | 저장소 본문 | 이미지 인식과 표현 학습, AlexNet 전환점 설명과 연결 |

## 확인한 원문 위치

- `.tmp/section-9-2-evidence/yolo-1506.02640.txt`
  - 객체 검출을 bounding boxes와 class probabilities 예측 회귀 문제로 재구성한다는 설명: 7-15행 부근
  - 45 FPS, Fast YOLO 150 FPS 이상의 실시간 처리 설명: 16-20행, 74-83행 부근
  - 객체 검출의 분리된 구성요소를 single neural network로 통합한다는 설명: 111-117행 부근
  - 전통적 detection pipeline이 robust features, classifiers, bounding box adjustment 등을 포함한다는 설명: 445-474행 부근
- `.tmp/section-9-2-evidence/wavenet-1609.03499.txt`
  - raw audio waveforms를 생성하는 deep neural network, fully probabilistic/autoregressive 설명: 1-16행 부근
  - raw audio waveform에서 joint probability를 조건부 확률 곱으로 분해한다는 설명: 48-56행 부근
  - TTS에서 statistical parametric, concatenative systems보다 자연스러운 음성을 보고했다는 설명: 247-288행 부근
  - WaveNet이 waveform level에서 직접 동작하는 deep generative model이라는 결론: 378-384행 부근
- `.tmp/section-9-2-evidence/deep-voice-1702.07825.txt`
  - production-quality TTS system constructed entirely from deep neural networks 설명: 16-25행 부근
  - 전통적 TTS가 complex multi-stage pipelines와 heuristics에 기반한다는 설명: 48-60행 부근
  - Deep Voice의 주요 TTS 구성요소: 156-178행 부근
  - inference에서 text -> phonemes -> duration/F0 -> audio synthesis로 이어지는 흐름: 206-214행 부근
  - real-time inference가 production-quality TTS에 필요하다는 설명: 78-88행, 144-155행 부근
  - neural approaches가 high-quality TTS engine의 모든 구성요소에 가능하다는 결론: 751-768행 부근

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 객체 검출은 이미지 분류와 달리 범주와 위치를 함께 예측한다 | YOLO 논문의 bounding boxes와 class probabilities 설명 | 유지 |
| YOLO는 객체 검출을 단일 신경망의 예측 문제로 재구성했다 | YOLO 논문의 single neural network, regression problem, end-to-end 설명 | 유지 |
| WaveNet은 raw audio waveform을 확률적 autoregressive 방식으로 생성했다 | WaveNet 논문의 fully probabilistic/autoregressive raw audio 설명 | 유지 |
| Deep Voice는 TTS 파이프라인 구성요소를 신경망 기반으로 전환했다 | Deep Voice 논문의 five major building blocks와 neural networks 설명 | 유지 |
| 세 사례는 LLM 직접 계보가 아니라 딥러닝 패러다임 확산의 주변 근거다 | `deep-learning-paradigm.md`의 경계 기준 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 9.1 | 이미지 인식과 표현 학습, AlexNet 전환점 |
| 9.2 | YOLO, WaveNet, Deep Voice를 통한 딥러닝 패러다임 확산 사례 |
| 9.3 | LLM의 직접 계보와 주변 근거 구분 |
| 10.2 | 텍스트, 이미지, 음성 생성의 공통 직관 |
| Part 4 | CNN, autoregressive model, sequence model, TTS 구성요소의 세부 구조 |

## 보수화한 표현

- “YOLO가 LLM 발전을 이끌었다”라고 쓰지 않았습니다. YOLO는 객체 검출 사례로 제한했습니다.
- “WaveNet이 LLM의 직접 조상이다”라고 쓰지 않았습니다. raw audio 순차 생성의 사례로만 설명했습니다.
- “Deep Voice가 완전한 end-to-end TTS를 완성했다”라고 쓰지 않았습니다. 전통적 파이프라인 구조를 유지하면서 구성요소를 신경망으로 바꿔 간 사례로 설명했습니다.
- “딥러닝이 모든 수작업 파이프라인을 없앴다”라고 쓰지 않았습니다. 일부 특징, 후보 생성, 규칙, 파이프라인을 학습 가능한 구조로 옮기는 흐름으로 제한했습니다.
- 모델 성능 수치는 논문 맥락에서만 언급하고, 현대 성능으로 일반화하지 않았습니다.

## 남은 검토 사항

- 9.3에서 LLM 직접 계보를 정리할 때 Seq2Seq, Attention, Transformer를 별도 근거로 다시 내려받아 검토합니다.
- 10.2에서 생성의 공통 직관을 다룰 때 WaveNet과 언어 모델의 공통점과 차이를 다시 분리합니다.
- Part 4에서 CNN, autoregressive model, dilated convolution, TTS 파이프라인을 기술적으로 확장합니다.
