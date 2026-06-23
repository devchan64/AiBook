# Section 11.3 근거 검토: Transformer와 사전학습 LLM

## 검토 목적

- 11.3의 중심 질문은 “현대 LLM은 어떻게 Transformer와 사전학습 위에서 커졌는가?”입니다.
- 이 메모는 Transformer, contextual representation, pretraining, fine-tuning, BERT/GPT 차이, zero-shot/few-shot/in-context learning 설명의 근거를 확인하기 위한 관리 자료입니다.
- 본문은 입문용 설명이므로 수식과 내부 구현은 최소화하고, 개념의 경계와 역사적 연결을 우선합니다.

## 확인한 자료

원문 PDF와 추출 텍스트는 `.tmp/section-11-3-evidence/` 아래에 내려받아 확인했습니다.

| 자료 | 반영 판단 |
| --- | --- |
| Vaswani et al., *Attention Is All You Need*, 2017 | Transformer가 recurrence와 convolution 없이 attention 중심 구조를 사용했고, self-attention과 positional encoding을 사용한다는 설명의 핵심 근거입니다. |
| Peters et al., *Deep contextualized word representations*, 2018 | ELMo를 문맥 의존 단어 표현(contextualized word representation)의 근거로 사용했습니다. |
| Howard and Ruder, *Universal Language Model Fine-tuning for Text Classification*, 2018 | language model pretraining 후 target task fine-tuning 흐름의 근거로 사용했습니다. |
| Radford et al., *Improving Language Understanding by Generative Pre-Training*, 2018 | GPT가 Transformer decoder와 generative pre-training, task-specific fine-tuning을 결합했다는 설명의 근거입니다. |
| Devlin et al., *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*, 2018 | BERT가 Transformer encoder, masked language model, bidirectional representation, fine-tuning 흐름을 사용한다는 설명의 근거입니다. |
| Radford et al., *Language Models are Unsupervised Multitask Learners*, 2019 | GPT-2가 zero-shot setting과 자연어 기반 task conditioning을 강조했다는 설명의 근거입니다. |
| Brown et al., *Language Models are Few-Shot Learners*, 2020 | GPT-3의 zero-shot, one-shot, few-shot, in-context learning, 그리고 가중치 업데이트 없는 task specification 설명의 근거입니다. |

## 본문 반영 기준

- Transformer는 “Attention이 전부”라는 구호보다, recurrence와 convolution 없이 self-attention을 중심에 놓은 구조라는 점을 우선 설명했습니다.
- positional encoding은 Transformer가 순서를 모르는 모델이라는 오해를 피하기 위해, 위치 정보를 별도로 더하는 장치로 설명했습니다.
- BERT와 GPT는 “이해 모델”과 “생각 모델”처럼 의인화하지 않고, encoder 중심 흐름과 decoder 중심 흐름으로 구분했습니다.
- pretraining은 사실 저장이나 검증 과정이 아니라, 대규모 텍스트에서 언어 패턴과 표현을 학습하는 절차로 제한했습니다.
- GPT-2와 GPT-3는 prompt engineering 본문으로 확장하지 않고, 자연어 입력과 예시가 과업 지정 방식으로 작동할 수 있음을 보여 준 전환점으로만 소개했습니다.
- GPT-3의 few-shot 설명은 “모델이 새 과업을 실제로 학습한다”로 단정하지 않고, 논문이 언급한 한계와 불확실성을 함께 반영했습니다.
- GPT-3.5와 ChatGPT는 11.3 본문에서 제외했습니다. 이 주제는 Transformer와 사전학습 구조 설명보다 Codex, agent, AI 도구 사용 경험으로 넘어가는 후속 장의 연결부에 더 적합합니다.
- 사용자가 기억한 “문장의 맥락을 파악하고 이어 나가는 흐름의 변화”는 11.3 본문이 아니라 `management/authoring/gpt-3-5-evidence-notes.md`에 별도 메모로 보존했습니다.

## 용어 검토

- `Transformer`, `self-attention`, `positional encoding`, `pretraining`, `fine-tuning`, `Encoder`, `Decoder`, `Encoder-Decoder`, `contextual representation`, `autoregressive language model`, `masked language model`, `zero-shot`, `one-shot`, `few-shot`, `in-context learning`은 한영 병기했습니다.
- `층위(level)` 표현은 이 절에서 필수적으로 사용하지 않았습니다.
- `layer` 구조 설명은 수식적 내부 구조로 들어가지 않기 위해 본문에서 깊게 다루지 않았습니다.

## 주의한 오해

- `Transformer = LLM 전체`로 쓰지 않았습니다.
- `LLM = AI 전체`로 쓰지 않았습니다.
- `사전학습 = 사실을 외워 정확히 답하는 과정`으로 쓰지 않았습니다.
- `Attention = 인간의 의식적 주의`로 쓰지 않았습니다.
- `in-context learning = 가중치 업데이트`로 쓰지 않았습니다.
- BERT와 GPT를 우열 관계나 인간적 능력 차이로 설명하지 않았습니다.
- GPT-3.5/ChatGPT의 대화 경험을 11.3의 Transformer 구조 설명 근거로 사용하지 않았습니다.

## Section 경계 검토

- 11.3은 11.1과 11.2에서 다룬 언어 모델, 임베딩, sequence modeling, Attention의 후속 흐름만 다룹니다.
- prompt 작성법은 이후 LLM과 prompt 관련 장으로 넘깁니다.
- RAG, vector search, service architecture는 이후 서비스 아키텍처 장으로 넘깁니다.
- Transformer 내부 수식과 multi-head attention의 상세 계산은 딥러닝/LLM 심화에서 다루는 것이 적절합니다.
- LoRA, instruction tuning, RLHF 같은 후속 기법은 Part 1에서는 이름을 남기더라도 자세한 설명은 12장 이후가 적절합니다.
- GPT-3.5/ChatGPT의 제품 경험, prompt 작성법, agent형 사용 방식은 11.3보다 이후 prompt, Codex, agent, AI 도구 사용 경험을 다루는 장에서 확장하는 것이 적절합니다.

## 참고 자료

- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), arXiv, 2017, 확인 날짜: 2026-06-23.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365), arXiv, 2018, 확인 날짜: 2026-06-23.
- Jeremy Howard, Sebastian Ruder, [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146), arXiv, 2018, 확인 날짜: 2026-06-23.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), OpenAI, 2018, 확인 날짜: 2026-06-23.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805), arXiv, 2018, 확인 날짜: 2026-06-23.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), OpenAI, 2019, 확인 날짜: 2026-06-23.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), arXiv, 2020, 확인 날짜: 2026-06-23.
