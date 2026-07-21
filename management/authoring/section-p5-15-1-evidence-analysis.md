# P5-15.1 근거 확인 메모

- 대응 Section: `P5-15.1`
- 본문 파일: `docs/parts/part-05/chapter-15/section-01.md`
- 확인 날짜: 2026-07-21
- 임시 원문 보관: `.tmp/section-p5-15-1-evidence/`

## 다운로드한 원문

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016.
  - Index: `.tmp/section-p5-15-1-evidence/deeplearningbook-index.html`
  - Chapter 5 `Machine Learning Basics`: `.tmp/section-p5-15-1-evidence/deeplearningbook-ml.html`
  - Chapter 20 `Deep Generative Models`: `.tmp/section-p5-15-1-evidence/deeplearningbook-generative-models.html`
- Chloe Autio, Reva Schwartz, Jesse Dunietz, Shomik Jain, Martin Stanley, Elham Tabassi, Patrick Hall, Kamie Roberts, `Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile`, NIST AI 600-1, 2024.
  - PDF: `.tmp/section-p5-15-1-evidence/nist-ai-600-1-generative-ai-profile.pdf`
  - 공식 페이지: `https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence`
  - DOI: `https://doi.org/10.6028/NIST.AI.600-1`
- Tom B. Brown et al., `Language Models are Few-Shot Learners`, NeurIPS 2020.
  - PDF: `.tmp/section-p5-15-1-evidence/brown-et-al-2020-language-models-are-few-shot-learners.pdf`
  - 공식 페이지: `https://papers.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html`

## 확인한 근거

- Index 원문에서 Chapter 5 `Machine Learning Basics`와 Chapter 20 `Deep Generative Models`의 공개 HTML 위치를 확인했다.
- Chapter 5에서는 분류가 입력을 여러 범주 중 하나로 대응시키는 과제이며, 분류 모델이 클래스별 확률 분포를 출력할 수 있다는 설명을 확인했다. 이는 P5-15.1의 `라벨`과 `점수·확률` 중심 출력 설명을 뒷받침한다.
- Chapter 20에서는 deep generative model이 여러 변수에 대한 확률 분포를 표현하고, 일부 모델은 그 분포에서 샘플을 뽑는 절차를 지원한다는 설명을 확인했다. 이는 P5-15.1이 P5-15.2 후보 분포와 P5-15.3 샘플링으로 이어지는 구조를 뒷받침한다.
- Chapter 20의 생성 모델 평가 논의에서는 현실적인 샘플 생성이 목표 중 하나이지만, 샘플의 시각적 품질만으로 모델을 충분히 평가하기 어렵고 의도한 사용 맥락에 맞는 평가 기준이 필요하다는 설명을 확인했다. 이는 P5-15.1의 `생성물은 사람이 읽고 검토할 대상`이라는 교육적 프레이밍을 보조한다.
- NIST AI 600-1에서는 생성형 AI를 입력 데이터의 구조와 특성을 모방해 파생된 합성 콘텐츠를 생성하는 AI 모델 부류로 정의하고, 이미지·비디오·오디오·텍스트 등 디지털 콘텐츠를 예로 든다. 이는 P5-15.1이 생성형 AI의 출력 경험을 `사용자가 읽고 검토할 생성물`로 잡는 설명을 보강한다.
- Brown et al. 2020에서는 GPT-3를 autoregressive language model로 제시하고, 과제를 텍스트 상호작용으로 지정해 번역, 질문답변, cloze 같은 작업을 수행한다고 설명한다. 이는 P5-15.1에서 자세한 GPT 사용법은 Part 6로 넘기되, 언어 생성이 후보 출력 선택과 실제 텍스트 산출로 이어진다는 다리 설명을 보조한다.

## 본문 반영 판단

- P5-15.1의 중심 주장은 `분류/예측 출력`과 `생성물 출력`의 차이를 초심자가 읽을 수 있게 잡는 것이다. 다운로드한 원문은 이 차이를 직접 같은 표현으로 설명하지는 않지만, 분류 출력의 범주·확률 관점과 생성 모델의 분포·샘플링 관점을 각각 지지한다.
- `사용자가 읽고 고칠 수 있는 문장·이미지·코드`라는 표현은 원문 직접 인용이 아니라 본문 흐름에 맞춘 저자 해설이다. 근거는 생성 모델 평가에서 샘플 품질과 사용 목적에 맞는 평가 기준을 함께 보아야 한다는 논의로 제한해 연결한다.
- NIST AI 600-1은 생성형 AI의 현대적 산출물 범위를 확인하는 보조 근거로 사용한다. 다만 이 문서는 위험관리 프로파일이므로, P5-15.1에서 딥러닝 내부 계산 설명의 주 근거로 과도하게 쓰지 않는다.
- Brown et al. 2020은 GPT 계열 언어 모델과 텍스트 기반 과제 수행의 대표 연구 근거로 사용한다. 다음 토큰 예측, 프롬프트, 실제 서비스 사용법은 P5-15.1에서 길게 풀지 않고 P5-15.2, P5-15.3, Part 6에서 회수한다.
- VAE, GAN, diffusion 같은 개별 생성 모델 계열은 P5-15.1의 중심 질문을 넘어서므로 이 Section의 출처 목록에는 넣지 않는다. 후보 분포와 샘플링의 더 자세한 근거는 P5-15.2와 P5-15.3에서 회수한다.
