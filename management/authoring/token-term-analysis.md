# 용어 검토: 토큰(token)의 출처와 LLM에서의 역할

## 검토 목적

`토큰(token)`은 LLM 설명에서 너무 빨리 등장하기 쉬운 용어다. 한국어로는 "단어 조각", "처리 단위", "기호", "표식"이 섞여 이해될 수 있으므로, 다음 세 층으로 구분한다.

- 일반 영어와 어원에서의 token
- 컴퓨터 과학과 NLP에서의 tokenization
- LLM에서의 token, token ID, embedding, next-token prediction
- 기호 기반 AI(symbolic AI)의 symbol과 LLM token의 관계

## 확인한 원문

원문 또는 HTML은 `.tmp/token-evidence/` 아래에 저장했다. 일부 사이트는 `curl` 저장이 403으로 실패했으므로, 본문 근거로 직접 사용하지 않고 보조 확인 대상으로만 둔다.

| 자료 | 로컬 저장 | 검토 내용 |
| --- | --- | --- |
| Etymonline, `token` | `etymonline-token.html` | Old English `tacen`, sign, symbol, evidence, portent 계열 |
| Hugging Face, Tokenization algorithms | `huggingface-tokenizer-summary.html` | subword tokenization, BPE, Unigram, WordPiece |
| OpenAI, `tiktoken` README | `openai-tiktoken-readme.md` | language model은 텍스트가 아니라 token이라는 숫자열을 본다는 설명 |
| Merriam-Webster, `token` | 저장 실패 | 보조 확인 대상. 직접 본문 근거로 사용하지 않음 |
| OpenAI Help, What are tokens and how to count them? | 저장 실패 | 보조 확인 대상. 직접 본문 근거로 사용하지 않음 |

## 어원과 일반 의미

Etymonline은 `token`을 Old English `tacen`에서 온 말로 설명하고, 의미를 sign, symbol, evidence, portent 계열로 제시한다. 또한 `show`, `explain`, `teach`와 관련된 동사 계열과 연결한다.

입문서에서는 이 어원을 다음처럼 일반화할 수 있다.

> token은 원래부터 "그 자체가 전체 의미인 것"이라기보다, 어떤 것을 알아보게 하거나 가리키는 표식, 증거에 가까운 말이다.

이 관점은 LLM 설명에 유용하다. LLM의 token도 사람이 읽는 자연스러운 단어와 동일한 것이 아니라, 모델이 입력과 출력을 처리하기 위해 사용하는 표식 단위다.

## symbolic AI의 symbol과 이어지는가

질문:

> 토큰(token)은 기호 기반 AI(symbolic AI)의 symbol과도 이어지지 않는가?

답은 "느슨하게 이어지지만, 같은 것은 아니다"로 정리하는 것이 안전하다.

2.1에서 기호 기반 AI의 symbol은 컴퓨터가 구분하고 조작할 수 있도록 이름 붙인 명시적 표식이라고 설명했다. 이 넓은 의미에서는 token도 symbol과 이어진다. token은 텍스트의 일부를 모델 vocabulary 안의 항목으로 구분해 주는 표식이고, token ID는 그 표식을 계산 가능한 정수로 바꾼 것이다.

하지만 symbolic AI의 symbol과 LLM의 token은 역할이 다르다.

| 구분 | symbolic AI의 symbol | LLM의 token |
| --- | --- | --- |
| 기본 역할 | 사람이 정의한 개념, 관계, 사실, 규칙을 명시적으로 나타냄 | 텍스트를 모델 vocabulary의 처리 단위로 나눔 |
| 의미 부여 | 사람이 정한 의미와 규칙에 강하게 연결됨 | 학습 데이터와 tokenizer vocabulary에 의해 정해진 이산 단위 |
| 처리 방식 | 규칙, 논리, 탐색, 지식 표현 위에서 조작됨 | token ID, embedding, attention, 확률 분포 계산으로 처리됨 |
| 해석 가능성 | 비교적 사람이 읽고 추적하기 쉬움 | token 자체보다 embedding과 모델 내부 상태에서 의미가 분산됨 |
| 예시 | `환자`, `증상`, `비가 온다`, `규칙 A` | `hello`, `ing`, 공백 포함 조각, 구두점, byte-level token |

따라서 다음 문장이 가장 안전하다.

> LLM의 token은 넓은 의미에서 컴퓨터가 다루는 표식이라는 점에서 symbol과 이어진다. 그러나 symbolic AI의 symbol처럼 사람이 정의한 의미와 규칙을 직접 조작하는 단위는 아니다. LLM에서 token은 텍스트를 숫자열로 바꾸는 이산 입력 단위이고, 의미는 token 하나에 고정되어 있다기보다 embedding과 모델의 학습된 파라미터 안에 분산되어 있다.

이 관점은 중요한 연결점을 만든다.

```text
symbolic AI:
명시적 symbol + 명시적 rule -> 추론

LLM:
token ID + embedding + 학습된 parameter -> 다음 token 확률 분포
```

둘 다 "컴퓨터가 처리할 수 있는 표식 단위"를 필요로 한다. 그러나 하나는 사람이 정의한 명시적 지식 표현을 조작하고, 다른 하나는 데이터에서 학습된 분산 표현(distributed representation)을 사용한다.

이 때문에 token은 symbolic AI와 neural AI를 이어 보는 좋은 교육용 접점이 될 수 있다. 다만 "LLM은 symbolic AI의 부활이다"처럼 쓰면 과장이다. 더 안전한 표현은 다음이다.

> LLM은 텍스트를 token이라는 이산 표식으로 입력받지만, 그 표식을 symbolic AI처럼 명시적 규칙으로 조작하지는 않는다. token은 symbolic AI의 symbol과 닮은 출발점을 가지지만, LLM 안에서는 embedding과 확률적 예측을 위한 계산 단위로 쓰인다.

## 앞선 개념과 이어지는 지도

토큰을 설명할 때는 앞 장의 개념을 다음 순서로 다시 연결할 수 있다.

```text
symbol
-> label
-> feature
-> representation
-> token
-> token ID
-> embedding
-> next-token probability
```

단, 이 순서는 역사적 계보라기보다 학습자가 개념을 이어 읽기 위한 교육용 지도다.

| 앞선 개념 | 연결되는 질문 | LLM에서 이어지는 표현 |
| --- | --- | --- |
| symbol | 무엇을 컴퓨터가 구분할 수 있는 표식으로 만들 것인가? | token |
| label | 사람이 붙인 구분 기준은 모델 학습에서 어떤 역할을 하는가? | target, expected output |
| feature | 원래 입력에서 모델이 사용할 값은 무엇인가? | token ID, input IDs |
| representation | 원래 데이터를 계산 가능한 형태로 어떻게 바꾸는가? | embedding, hidden representation |
| parameter | 학습으로 조정된 내부 값은 무엇을 바꾸는가? | weight, bias, attention layer parameters |
| probability | 불확실한 후보들을 어떻게 점수화하는가? | next-token probability distribution |

본문에 반영할 때는 다음 경계를 둔다.

- symbol과 token은 모두 표식 단위라는 점에서 연결된다.
- label과 token은 모두 이름표처럼 보일 수 있지만, label은 학습 목표이고 token은 입력/출력 처리 단위다.
- feature와 token ID는 모델이 계산할 수 있는 입력 값이라는 점에서 연결된다.
- representation과 embedding은 원래 데이터를 계산 가능한 내부 형태로 바꾼다는 점에서 연결된다.
- parameter는 token 자체가 아니라 token 표현을 처리하는 학습된 내부 값이다.

## 왜 단어(word)가 아니라 토큰(token)인가

LLM에서 단어(word)만 쓰면 문제가 생긴다.

| 단위 | 장점 | 한계 |
| --- | --- | --- |
| 단어(word) | 사람이 이해하기 쉽다 | 모든 단어 변형과 신조어를 vocabulary에 넣기 어렵다 |
| 문자(character) | 모든 문자열을 표현할 수 있다 | sequence가 길어지고 한 글자 단위의 의미 정보가 약하다 |
| 토큰(token) | 단어와 문자 사이의 절충이 가능하다 | 사람이 보는 단어 경계와 다를 수 있다 |

Hugging Face 문서는 subword tokenization을 단어와 문자 사이의 단위로 설명하고, vocabulary를 작게 유지하면서 의미 있는 조각을 포착한다고 설명한다. 일반 단어는 하나의 token으로 남을 수 있고, 드문 단어나 모르는 단어는 subword로 나뉠 수 있다.

OpenAI의 `tiktoken` README는 language model이 사람이 보는 텍스트가 아니라 token으로 알려진 숫자열을 본다고 설명한다. 또한 BPE(byte pair encoding)를 텍스트를 token으로 변환하는 방식으로 설명하고, reversible/lossless, arbitrary text 처리, 압축, common subword 학습이라는 장점을 제시한다.

## LLM에서 token이 하는 역할

LLM에서 token은 다음 흐름의 첫 단위다.

```text
문자열(text)
-> 토큰화(tokenization)
-> token ID
-> embedding vector
-> Transformer 계산
-> 다음 token의 확률 분포
-> 선택된 token
-> 텍스트로 decode
```

따라서 token은 다음 역할을 한다.

| 역할 | 설명 |
| --- | --- |
| 입력 단위 | 사용자의 문자열을 모델 vocabulary에 있는 단위로 나눈다 |
| 숫자 ID | 모델이 직접 계산할 수 있도록 각 token을 정수 ID로 바꾼다 |
| 임베딩의 키 | token ID는 embedding table에서 벡터를 찾는 인덱스 역할을 한다 |
| 예측 대상 | LLM은 다음 token 후보들의 확률 분포를 계산한다 |
| 비용과 한계 단위 | API와 모델 문맥 길이(context length)는 token 수로 관리되는 경우가 많다 |

## 안전한 설명 문구

본문에서는 다음 문구가 안전하다.

> 토큰(token)은 사람이 읽는 단어와 항상 같지 않다. 원래 token은 표식이나 증거를 뜻하는 말에 가깝고, LLM에서는 텍스트를 모델이 처리할 수 있도록 나눈 기본 단위를 가리킨다. 토큰은 다시 숫자 ID로 바뀌고, 모델은 이 ID의 임베딩을 사용해 다음 토큰의 확률 분포를 계산한다.

더 짧게는 다음처럼 쓸 수 있다.

> LLM에서 token은 "단어"라기보다, 텍스트를 계산 가능한 숫자열로 바꾸기 위한 표식 단위다.

## 피해야 할 설명

| 피할 표현 | 문제 | 대체 표현 |
| --- | --- | --- |
| token은 단어다 | subword, punctuation, whitespace, byte-level token을 설명하지 못함 | token은 모델 vocabulary의 처리 단위다 |
| token은 의미 단위다 | BPE token이 항상 의미를 갖는 것은 아님 | 일부 token은 의미 있는 subword에 가깝지만, 항상 의미 단위는 아니다 |
| token은 글자 조각이다 | 단어 전체가 하나의 token이 될 수도 있음 | token은 단어, 부분 단어, 문자, byte, 특수 기호가 될 수 있다 |
| LLM은 단어를 예측한다 | 실제 구현에서는 token ID 분포를 예측함 | LLM은 다음 token의 확률 분포를 계산한다 |
| LLM token은 symbolic AI의 symbol과 같다 | 표식이라는 공통점은 있지만 처리 방식과 의미 부여가 다름 | token은 symbol과 이어지는 이산 표식이지만, LLM에서는 embedding과 확률 예측의 계산 단위다 |

## 본문 반영 위치

- 9.3에서는 token을 깊게 설명하지 않고, 직접 계보 설명에서 짧은 주석만 둔다.
- Part 5의 `토큰화` 절에서 이 메모를 근거로 본문을 작성한다.
- 5.2의 inference 설명에서 "다음 토큰 후보 계산"을 이미 언급했으므로, 이후 Part 5에서 token ID와 embedding을 연결한다.

## 출처와 참고 자료

- Douglas Harper, [Etymology of token](https://www.etymonline.com/word/token), Online Etymology Dictionary, 확인 날짜: 2026-06-23.
- Hugging Face, [Tokenization algorithms](https://huggingface.co/docs/transformers/en/tokenizer_summary), Transformers documentation, 확인 날짜: 2026-06-23.
- OpenAI, [openai/tiktoken](https://github.com/openai/tiktoken), GitHub, 확인 날짜: 2026-06-23.
- Merriam-Webster, [Token Definition & Meaning](https://www.merriam-webster.com/dictionary/token), 확인 날짜: 2026-06-23. 로컬 저장은 403으로 실패했으므로 보조 확인 대상으로만 둠.
- OpenAI Help Center, [What are tokens and how to count them?](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-do-i-count-them), 확인 날짜: 2026-06-23. 로컬 저장은 403으로 실패했으므로 보조 확인 대상으로만 둠.
