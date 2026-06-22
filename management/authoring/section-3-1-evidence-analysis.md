# 3.1 근거 분석: 규칙 기반 시스템의 강점과 한계

이 문서는 `docs/chapters/chapter-03/section-01.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 가능한 자료를 `.tmp/section-3-1-evidence/` 아래에 내려받아 확인했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Buchanan, Shortliffe, `Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project` | `.tmp/section-3-1-evidence/mycin-book.html`, `mycin-chapter-01.pdf`, `mycin-chapter-15.pdf`, `mycin-chapter-31.pdf` | MYCIN, 지식 기반, 규칙, 추론 절차, 설명 기능, 지식 공학, EMYCIN의 근거 |
| Stanford Encyclopedia of Philosophy, `Logic-Based Artificial Intelligence` | `.tmp/section-3-1-evidence/sep-logic-ai.html` | 논리 기반 AI, 지식 표현, 대규모 형식화와 구현 가능 추론의 배경 근거 |
| AIMA 4판 목차 | `.tmp/section-3-1-evidence/aima-contents.html` | 전문가 시스템이 AI 역사에서 별도 항목으로 다뤄지고, 지식·추론·불확실성·머신러닝이 AI 교재 안에서 함께 배치된다는 보조 근거 |
| Saez Trigueros et al., `Face Recognition: From Traditional to Deep Learning Methods` | `.tmp/section-3-1-case-studies/face-recognition-traditional-to-deep-learning.pdf` | 얼굴인식의 전통적 방법이 hand-crafted features, geometry-based, holistic, feature-based, hybrid methods를 포함한다는 근거 |
| Minaee et al., `Going Deeper Into Face Detection: A Survey` | `.tmp/section-3-1-case-studies/face-detection-survey.pdf` | 얼굴검출의 초기 접근이 hand-crafted features, Haar Cascades, HOG 등에 기반했고 uncontrolled environments에서 한계가 있었다는 근거 |
| Kamci et al., `Lane Detection For Prototype Autonomous Vehicle` | `.tmp/section-3-1-case-studies/lane-detection-prototype-autonomous-vehicle.pdf` | 차선 추적 자율주행 프로토타입이 ROI, Canny, Sobel, Hough transform, 각도 기반 제어를 사용하는 사례 |
| Skut et al., `A Flexible Rule Compiler for Speech Synthesis` | `.tmp/section-3-1-case-studies/rule-compiler-speech-synthesis.pdf` | TTS에서 규칙 집합을 FST로 컴파일해 결정적 장치로 구현하는 사례 |
| Krizhevsky et al., `ImageNet Classification with Deep Convolutional Neural Networks` | `.tmp/section-3-1-evidence/alexnet-imagenet-2012.pdf`, `.txt` | 딥러닝 부흥이 대규모 데이터, 깊은 모델, GPU 구현, 병렬 처리와 함께 설명될 수 있다는 보조 근거 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| 규칙 기반 시스템은 사실, 규칙, 지식 기반, 추론 엔진, 설명 기능으로 설명할 수 있다 | MYCIN 책 1장 텍스트에서 knowledge base, conditional rules, explanation subsystem, inference rules가 함께 설명됨 | 유지 |
| MYCIN은 규칙 기반 전문가 시스템의 대표 실험으로 볼 수 있다 | MYCIN 책 HTML 제목과 서문이 `Rule-Based Expert Systems` 및 MYCIN 실험을 명시함 | 유지 |
| 규칙은 설명과 검토에 유리하다 | MYCIN 15장은 규칙을 설명 목적의 편리한 단위로 설명하고, consultation 중 규칙 기반 설명을 제공한다고 설명함 | 유지 |
| 규칙 기반 시스템은 지식 획득과 지식 공학 문제가 중요하다 | MYCIN 1장과 15장은 전문가 지식을 지식 기반으로 옮기는 과정, knowledge engineering, knowledge acquisition facilities를 다룸 | 유지 |
| 규칙은 모듈식으로 추가·수정 가능하지만, 충돌·누락·검증 문제가 생긴다 | MYCIN 15장은 rule update, syntactic validity, contradiction, subsumption, debugging을 설명함 | 유지 |
| 전문가 시스템은 좁은 도메인에 강하지만 일반화에는 주의가 필요하다 | MYCIN 15장은 성공한 시스템도 좁은 도메인에서 강하다고 설명함 | 유지 |
| 규칙 기반 시스템과 머신러닝은 역할이 다르며 현대 시스템에서 함께 쓰일 수 있다 | 본문 자체의 일반화. AIMA 목차가 지식·추론·불확실성·머신러닝을 함께 배치하고, 기존 2.3 근거와 연결됨 | 유지하되 과도한 표준 주장처럼 단정하지 않음 |
| 구매 승인, 운영 알림, 위험 거래, 고객 문의 분류 예시는 규칙의 장점과 한계를 보여 준다 | 자체 예시. 특정 외부 시스템의 실제 규칙이 아니라 개념 설명을 위한 일반화 예시 | 유지하되 실제 업무 규칙이나 의료·보안 처방처럼 쓰지 않음 |
| 얼굴인식은 순수 규칙 기반이라기보다 기하학적 특징·수작업 특징 기반 접근으로 표현해야 한다 | Saez Trigueros et al.은 전통적 얼굴인식 방법을 geometry-based, holistic, feature-based, hybrid methods로 분류함 | `규칙 기반`으로 단정하지 않고 `손으로 설계한 특징`으로 정제 |
| 얼굴검출의 전통적 접근은 hand-crafted features와 분류기를 사용했고, 비통제 환경에서 한계가 있었다 | Minaee et al.은 Haar Cascades, HOG 같은 hand-crafted features를 언급하고 uncontrolled environments의 한계를 설명함 | 유지 |
| 자율주행의 일부 차선 추적 문제는 영상 처리와 조향 규칙으로 구현할 수 있다 | Kamci et al.은 ROI, Canny, Sobel, Hough transform, 차선 각도 기반 진행 방향 결정을 설명함 | `자율주행 전체`가 아니라 `차선 추적 프로토타입`으로 제한 |
| TTS는 규칙 기반 접근이 성공적으로 쓰인 영역으로 볼 수 있다 | Skut et al.은 TTS 규칙을 FST로 컴파일해 결정적 장치로 구현하는 방법을 설명함 | 유지하되 자연스러운 음성 전체를 규칙만으로 해결했다고 쓰지 않음 |
| “규칙 기반 -> 기호 기반 -> 신경망”이라는 사용자 직관은 보정이 필요하다 | 2.1과 2.2의 근거상 기호 기반 AI가 더 넓고, 규칙 기반은 그 구현 방식 중 하나다. 2.3과 기존 user-claim-evidence-map은 신경망·딥러닝을 데이터와 표현 학습의 흐름으로 설명한다 | 본문에는 `기호 기반 AI -> 규칙 기반 시스템`과 `시대적 조건 변화 -> 데이터 기반 학습과 신경망 중요성 강화`로 정리 |
| 연구 중심의 이동과 역할 변화는 아이디어 변화만이 아니라 물리적 성능 변화와도 관련된다 | AlexNet 논문은 ImageNet 120만 학습 이미지, 6천만 파라미터, 효율적인 GPU 구현, 두 GTX 580 GPU 학습, 더 빠른 GPU와 더 큰 데이터셋 가능성을 직접 언급함 | 3.1에서는 상세 기술사가 아니라 접근법의 중심성이 바뀐 배경 조건으로만 짧게 반영 |

## 주의한 표현

- MYCIN의 성능을 현대 의료 AI 수준으로 일반화하지 않았습니다.
- 전문가 시스템이 실제 임상에 배포되었다거나 현대 의료 판단을 대체했다는 식으로 쓰지 않았습니다.
- 규칙 기반 AI가 실패했고 머신러닝이 승리했다는 단순한 도식은 피했습니다.
- `IF-THEN`은 대표적 설명 방식으로만 다루고, 모든 규칙 기반 시스템이 동일 문법을 쓴다고 쓰지 않았습니다.
- 현대 AI 서비스에서 규칙이 필요하다는 설명은 서비스 설계 관점의 일반화이며, 특정 제품의 내부 구조로 단정하지 않았습니다.
- 보강한 업무 승인, 운영 알림, 위험 거래, 고객 문의 예시는 학습용 자체 예시입니다. 특정 회사, 의료기관, 금융기관, 보안 시스템의 실제 운영 기준이 아닙니다.
- 얼굴인식을 `규칙 기반`이라고 직접 단정하지 않고, `기하학적 특징`, `수작업 특징`, `전통적 방법`으로 표현했습니다.
- 자율주행 사례는 전체 자율주행 문제가 아니라 차선 검출·차선 추적 프로토타입으로 범위를 제한했습니다.
- TTS는 규칙 기반 처리의 성공 사례로 소개하되, 현대 TTS의 자연스러움과 표현력은 딥러닝 기반 접근으로 크게 발전했다는 점을 후속 절에서 다룰 수 있도록 열어 두었습니다.
- 얼굴인식, 자율주행, TTS 사례는 3.1의 도메인 안에서만 사용합니다. 즉 각 분야의 기술사를 설명하는 것이 아니라, 규칙과 수작업 특징의 강점과 한계를 보여 주는 짧은 사례로 제한합니다.
- 사용자의 “규칙 기반이 기호 기반으로 흘러갔다”는 표현은 공개 본문에 직접 노출하지 않습니다. 독자에게는 `기호 기반 AI`가 더 넓은 역사적 흐름이고, `규칙 기반 시스템`은 그 대표 구현 중 하나라는 구조로 설명합니다.
- 신경망은 기호 기반 AI의 단순한 후속 단계로 쓰지 않았습니다. 신경망 연구는 오래 병렬로 존재했고, 데이터·계산 자원·학습 알고리즘의 발전과 함께 중요성과 중심성이 커진 흐름으로 표현했습니다.
- 시대 변화는 `교체`보다 `연구 중심의 이동`과 `역할 변화`로 표현합니다. `재배치`라는 표현은 저자적 설명으로만 제한하고, 표준 학술 용어처럼 보이지 않게 주의합니다. 특정 접근이 사라졌다고 쓰지 않고, 어떤 문제와 환경에서 더 강하게 쓰이게 되었는지 설명합니다.
- 물리적 성능 변화는 중요한 조건으로 다루되, 딥러닝 확산을 하드웨어만의 결과로 설명하지 않습니다. 데이터 축적, 학습 알고리즘, 벤치마크, 오픈소스 도구, 연구 커뮤니티의 변화가 함께 작용한 것으로 표현합니다.
- 현대 AI 서비스 예시는 3.1에서 아키텍처 설명으로 확장하지 않습니다. 권한, 검증, 안전, 배포 조건처럼 규칙이 계속 필요한 영역을 보여 주는 데만 사용하고, RAG, Tool use, Agent의 구조는 Chapter 14로 넘깁니다.

## 본문에 넣지 않은 내용

- MYCIN의 certainty factor 수식과 확률적 해석 논쟁은 6장 불확실성 또는 확률 추론 절에서 다루는 편이 적절합니다.
- DENDRAL, XCON, CADUCEUS 등 개별 전문가 시스템의 상세 역사는 별도 사례 절이 생길 때 다룹니다.
- 지식 표현 형식, default logic, nonmonotonic logic은 2.2 또는 이후 불확실성·추론 절에서 다룹니다.
- ALVINN, VaMoRs, VaMP 같은 자율주행 역사 사례는 9장 또는 11장 계보 설명에서 더 직접적으로 다룹니다. 3.1에서는 규칙·수작업 특징 기반 접근의 한계 사례로만 짧게 사용합니다.
- Klatt, MITalk, DECtalk 계열 TTS 역사는 중요한 사례지만 이번 본문에는 직접 넣지 않았습니다. 원문 접근이 제한되어 있어, 현재는 Skut et al.의 공개 논문을 TTS 규칙 처리 근거로 사용했습니다.
- AlexNet은 물리적 성능 변화의 보조 근거로 짧게만 언급했습니다. GPU, MapReduce, Transformer의 병렬 처리 같은 상세 기술사는 딥러닝 패러다임, 대규모 학습 인프라, LLM 역사 절에서 별도 근거를 내려받아 다루는 편이 적절합니다.

## 검증 필요

- 전문가 시스템의 한국어 용어 사용은 2.1의 KCI 검색 메모와 연결해 필요 시 보강합니다.
- DENDRAL과 XCON을 본문에서 자세히 다루려면 1차 자료나 신뢰도 높은 역사 자료를 추가로 내려받아야 합니다.
- 물리적 성능 변화의 세부 근거를 확장하려면 AlexNet 논문, MapReduce 논문, Transformer 논문, 딥러닝 교재 또는 주요 학술 survey를 `.tmp/`에 내려받아 별도 분석합니다.
- 현대 AI 서비스에서 규칙과 모델이 결합되는 구체적 아키텍처는 Chapter 14에서 공식 문서 또는 시스템 설계 자료를 근거로 다시 검토합니다.

## 출처

- Bruce G. Buchanan, Edward H. Shortliffe (eds.), [Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project](https://people.dbmi.columbia.edu/~ehs7001/Buchanan-Shortliffe-1984/MYCIN%20Book.htm), Addison-Wesley, 1984, 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Richmond H. Thomason, [Logic-Based Artificial Intelligence](https://plato.stanford.edu/entries/logic-ai/), substantive revision 2024-02-27, 확인 날짜: 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html), 확인 날짜: 2026-06-22.
- Daniel Saez Trigueros, Li Meng, Margaret Hartnett, [Face Recognition: From Traditional to Deep Learning Methods](https://arxiv.org/abs/1811.00116), arXiv:1811.00116, 2018, 확인 날짜: 2026-06-22.
- Shervin Minaee, Ping Luo, Zhe Lin, Kevin Bowyer, [Going Deeper Into Face Detection: A Survey](https://arxiv.org/abs/2103.14983), arXiv:2103.14983, 2021, 확인 날짜: 2026-06-22.
- Sertap Kamci, Dogukan Aksu, Muhammed Ali Aydin, [Lane Detection For Prototype Autonomous Vehicle](https://arxiv.org/abs/1912.05220), arXiv:1912.05220, 2019, 확인 날짜: 2026-06-22.
- Wojciech Skut, Stefan Ulrich, Kathrine Hammervold, [A Flexible Rule Compiler for Speech Synthesis](https://arxiv.org/abs/cs/0403039), arXiv:cs/0403039, 2004, 확인 날짜: 2026-06-22.
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, [ImageNet Classification with Deep Convolutional Neural Networks](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html), NeurIPS, 2012, 확인 날짜: 2026-06-22.
