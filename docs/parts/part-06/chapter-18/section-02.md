# P6-18.2 직접 계보와 주변 근거

> Section ID: `P6-18.2`
> Version: `v2026.07.07`

P6-18.1에서는 LLM 발전사를 큰 흐름으로 정리했습니다. 하지만 여기서 한 가지 구분이 더 필요합니다.

모든 딥러닝 발전사가 곧바로 LLM의 직접 계보인 것은 아니다.

이 절은 그 구분을 다룹니다.

직접 계보(direct lineage)는 현재 LLM 구조와 학습 방식으로 직접 이어지는 흐름이고, 주변 근거(surrounding evidence)는 딥러닝 확산과 계산 패러다임 변화를 설명하지만 LLM 구조 자체의 조상이라고 단정하기 어려운 흐름입니다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 무엇을 LLM의 직접 계보라고 부를 수 있는가?
- 무엇은 딥러닝 확산의 중요한 사례이지만 직접 계보라고 하기는 어려운가?
- 이런 구분이 왜 학습자에게 중요한가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- 모든 주변 분야 논문 열거
- 음성, 비전, 추천 모델의 상세 발전사
- 멀티모달 모델의 최신 계보

모든 주변 분야 논문 열거와 음성, 비전, 추천 모델의 상세 발전사는 여기서 다루지 않습니다. 대신 이 절의 직접 계보 구분은 앞서 읽은 P6-3.1, P6-4.1과 뒤의 P6-19.1에서 Transformer, GPT, BERT를 구조 비교로 다시 읽을 때 쓰입니다. 음성, 비전, 멀티모달 계보 전체를 따로 따라가는 일은 이 책의 현재 본편 범위 밖에 둡니다.

이 절에서는 `모든 AI 발전을 LLM 역사로 한 줄에 늘어놓는 오해`를 줄입니다. 동시에 구조 설명과 배경 설명을 어느 지점에서 갈라 읽어야 하는지도 함께 분명히 둡니다.

지금 읽는 층위는 `본류 복습 뒤의 계보 구분 배경 층위`입니다. 앞 절이 큰 발전사 지도를 그렸다면, 여기서는 그 지도 안에서 `직접 구조 계보`와 `주변 확산 근거`를 어디서 가를지 질문이 더 좁아집니다. 아직 새 본류를 추가하는 단계는 아니고, 바로 뒤의 BERT 비교 장과 앞서 읽은 Transformer·GPT 본류를 더 과장 없이 다시 해석하게 만드는 정리 단계에 가깝습니다.

| 먼저 끝내야 하는 본류 | 이 배경 축에서 다시 가르는 것 | 다시 돌아가 확인할 위치 |
| --- | --- | --- |
| Transformer, GPT, 사전학습, RAG까지의 생성 중심 흐름 | 무엇이 LLM의 직접 계보고 무엇이 딥러닝 확산의 주변 근거인가 | P6-3.1, P6-4.1, P6-19.1 |

이 표의 핵심은 이 절을 `새 역사 목록`으로 읽지 않는 데 있습니다. 여기서는 이름을 더 많이 외우기보다, 앞서 읽은 본류 설명을 `직접 구조 조상`과 `주변 배경`으로 분리해 과장 없이 다시 말할 수 있게 되는지만 잡으면 충분합니다.

이 절은 Part 6에서 직접 계보(direct lineage)와 주변 근거(surrounding evidence)를 대표로 구분하는 Section입니다. LLM 구조의 직접 조상과 딥러닝 확산의 배경 사례를 같은 선 위에 두지 않게 만드는 기준선을 여기서 세웁니다.

## 이 절의 목표

- 직접 계보와 주변 근거를 구분할 수 있습니다.
- LLM 발전사를 과장 없이 설명할 수 있습니다.
- 딥러닝 확산 사례가 왜 중요하지만 직접 조상은 아닐 수 있는지 설명할 수 있습니다.
- 앞서 읽은 Transformer 설명을 더 분명한 위치에서 다시 정리할 수 있습니다.

## 왜 이런 구분이 필요한가

최근에는 AI를 곧바로 LLM과 연결해 이해하는 경향이 강합니다. 이때 다음과 같은 혼동이 생기기 쉽습니다.

- 딥러닝이 유명해진 모든 사건이 곧바로 LLM 계보다
- 음성 모델, 객체 검출 모델, 강화학습 모델이 모두 같은 직선 위에 있다
- `신경망이니까 다 같은 역사다`

이렇게 설명하면 큰 분위기는 잡히지만, 구조적 이해는 흐려집니다.

더 안전한 설명은 다음입니다.

- 어떤 흐름은 LLM 구조와 학습 목표로 직접 이어진다
- 어떤 흐름은 딥러닝 패러다임의 확산과 계산 자원의 중요성을 보여 주는 배경 증거다

## 직접 계보는 무엇인가

여기서는 다음 흐름을 LLM의 직접 계보로 봅니다.

1. 언어 모델(language model)
2. 임베딩과 분산 표현(distributed representation)
3. RNN, LSTM, Seq2Seq
4. Attention
5. Transformer
6. 사전학습(pretraining)
7. GPT, BERT 같은 Transformer 계열 언어 모델

이 흐름의 공통점은 분명합니다.

- 언어를 입력으로 다루고
- 토큰이나 단어의 순서와 문맥을 계산하며
- 다음 토큰 예측 또는 언어 표현 학습으로 이어지고
- 현재 LLM 구조와 직접 연결됩니다

즉, 이들은 `LLM 내부 구조와 학습 방식`의 조상으로 설명할 수 있습니다.

## 주변 근거는 무엇인가

반면 다음과 같은 사례는 매우 중요하지만, 직접 계보라고 단정하는 데는 주의가 필요합니다.

- AlexNet과 이미지 인식 혁신
- YOLO 같은 객체 검출(object detection) 계열
- WaveNet, Deep Voice 같은 음성 생성(speech generation) 계열
- AlphaGo, AlphaZero 같은 탐색과 강화학습의 대표 사례

이 사례들은 다음 점에서 중요합니다.

- 딥러닝이 실제 성능 전환을 만들 수 있음을 사회적으로 보여 주었고
- GPU와 대규모 계산 자원의 중요성을 강화했으며
- 학습 기반 접근이 다양한 도메인으로 확산되는 흐름을 만들었습니다

하지만 이들을 곧바로 `LLM의 직접 조상`이라고 쓰면 경계가 흐려집니다.

## Deep Voice나 YOLO는 왜 직접 계보가 아닌가

예를 들어 Deep Voice는 음성 생성(speech synthesis) 분야에서 중요한 사례입니다. YOLO는 실시간 객체 검출에서 대표적인 전환점입니다.

이 둘은 모두 딥러닝 패러다임의 확산을 보여 주지만, 현재 LLM의 직접 구조를 형성한 핵심 언어 모델 계보와는 다릅니다.

더 안전한 설명은 다음입니다.

- Deep Voice, YOLO는 `딥러닝이 다양한 입력과 출력 도메인에서 강해졌다`는 주변 근거다
- Transformer 기반 LLM의 직접 구조사는 `언어 모델링과 Attention 계열`에서 더 직접적으로 찾아야 한다

즉, 관련은 있지만 같은 선 위에 그대로 놓으면 안 됩니다.

## 왜 주변 근거도 여전히 중요한가

그렇다고 주변 근거를 빼 버리면 또 다른 문제가 생깁니다. LLM은 언어 모델만 조용히 발전해서 갑자기 등장한 것이 아니기 때문입니다.

주변 근거는 다음 질문에 답해 줍니다.

- 왜 딥러닝이 사회적으로 신뢰와 투자를 받게 되었는가?
- 왜 병렬 처리와 GPU가 중요해졌는가?
- 왜 데이터 규모, 모델 규모, 계산 규모가 함께 커졌는가?

즉, 주변 근거는 `구조적 조상`은 아니지만 `역사적 분위기와 인프라 조건`을 설명합니다.

## 이 절을 어디까지 읽으면 충분한가

이 절의 역할은 새 구조를 하나 더 배우는 데 있지 않습니다. 앞의 직접 계보와 주변 근거 구분만 선명하게 잡히면, 뒤의 BERT, GPT, RAG 설명을 읽을 때 구조 설명과 배경 설명을 덜 섞게 됩니다.

우선 다음 두 줄만 남기고 넘어가도 충분합니다.

- language modeling, attention, Transformer, pretraining은 직접 계보에 가깝다
- 비전·음성·강화학습의 대표 성과는 중요하지만 주로 배경 설명으로 읽는다

## 직접 계보와 주변 근거를 나눠 그리면

```mermaid
flowchart TD
  A["language modeling"]
  B["embeddings"]
  C["RNN / Seq2Seq"]
  D["attention"]
  E["Transformer"]
  F["pretrained LLM"]

  G["computer vision breakthroughs"]
  H["speech generation breakthroughs"]
  I["large-scale compute trend"]

  A --> B --> C --> D --> E --> F
  G -. surrounding evidence .-> F
  H -. surrounding evidence .-> F
  I -. enabling background .-> F
```

이 도식의 목적은 한 가지입니다.

`한 줄 역사`와 `배경 조건`을 구분해서 읽게 하는 것.

## 사례로 보기

### 사례 1. Transformer 설명

강의자가 Transformer를 소개하면서 첫 슬라이드에 `AlexNet -> YOLO -> GPU -> Transformer`를 한 줄로 적었다고 해 보겠습니다. 듣는 사람은 유명한 이름이 시간순으로 놓여 있으면 모두 같은 계보라고 받아들이기 쉽습니다. 하지만 이렇게 설명하면 정작 `왜 Seq2Seq만으로는 긴 문장에서 앞 정보를 뒤까지 잘 전달하기 어려웠는가`, `왜 attention이 필요했는가`라는 직접 구조 문제가 빠져 버립니다. 사람의 기존 기준은 `유명한 사건을 많이 안다`였지만, 더 중요한 기준은 `바로 앞 구조의 어떤 한계를 다음 구조가 해결했는가`입니다. 그래서 먼저 긴 문장 번역에서 앞 문맥이 뒤에서 약해지는 장면을 보여 주고, 그 다음에 attention과 Transformer를 붙여야 설명이 닫힙니다. 여기서 바뀌는 점은 `유명한 사건이 많이 등장하는가`를 보던 기준에서 `직전 구조의 병목과 다음 구조의 해결이 실제로 이어지는가`를 보는 기준으로 이동한다는 것입니다. 그래서 이 사례에서 확인해야 할 결과는 유명 사건 나열보다, 바로 앞 구조의 병목을 설명한 뒤에야 Transformer 전환 이유가 실제로 더 분명해지는가입니다.

### 사례 2. GPU 설명

사용자가 `LLM이 왜 가능해졌나요?`라고 묻자 발표자가 GPU 사진과 서버 랙만 길게 보여 주는 장면을 떠올려 보겠습니다. 듣는 사람은 계산 장비가 커졌다는 설명만 들어도 `결국 GPU가 모델 원리까지 만든 것`처럼 느끼기 쉽습니다. 하지만 GPU는 `더 크게 돌리게 한 조건`이지, `attention으로 어떤 문맥을 비교하고 어떤 토큰을 더 보게 만드는가`를 설명하는 구조 자체는 아닙니다. 사람이 기존에 쓰던 단순 기준은 `잘 돌아가게 만든 요소`와 `무엇을 계산하게 만든 아이디어`를 한데 묶는 것이지만, 이 둘은 다른 층위입니다. 예를 들어 GPU가 아무리 많아도 attention 구조 설명이 빠지면 왜 LLM이 긴 문맥을 읽는지 이해할 수 없습니다. 여기서 바뀌는 점은 `계산 자원이 커졌는가`를 보던 기준에서 `배경 조건과 구조 원리가 실제로 분리되어 설명되는가`를 보는 기준으로 이동한다는 것입니다. 그래서 이 사례에서 확인해야 할 결과는 계산 규모를 키운 배경 설명과 모델 구조 설명이 실제로 분리되어 읽히는가입니다.

### 사례 3. 생성형 AI 붐

뉴스 기사에서 같은 해에 챗봇, 이미지 생성기, 음성 합성 서비스가 함께 화제가 되는 장면을 생각해 보겠습니다. 사람은 이런 경우 `같이 뜬 기술이면 같은 역사겠지`라고 먼저 묶기 쉽습니다. 하지만 실제로는 사용 경험의 동시성과 구조의 직접 계보를 나눠 봐야 합니다. 예를 들어 고객은 텍스트 생성과 이미지 생성을 모두 `생성형 AI`로 부르지만, 그 안쪽 구조사는 언어 모델 계보와 비전 생성 계보로 더 가깝게 갈라질 수 있습니다. 사람이 보던 단순 기준은 `같은 시기에 유명해졌는가`였지만, 더 중요한 기준은 `어떤 입력과 학습 목표, 어떤 구조 변화가 직접 이어졌는가`입니다. 여기서 바뀌는 점은 `같은 시기에 화제가 되었는가`를 보던 기준에서 `직접 이어지는 구조 계보가 같은가`를 보는 기준으로 이동한다는 것입니다. 그래서 이 사례에서 확인해야 할 결과는 유행의 동시성과 구조의 직접 계보를 실제로 다른 판단 기준으로 설명할 수 있는가입니다.

세 사례를 direct lineage와 surrounding evidence 구분으로 다시 묶으면 다음과 같습니다.

| 장면 | 섞어 읽기 쉬운 것 | 실제로 분리해 봐야 하는 것 |
| --- | --- | --- |
| Transformer 설명 | 유명 사건 나열과 구조 전환 | 직전 병목과 다음 구조의 해결 |
| GPU 설명 | 계산 자원과 모델 원리 | 가능하게 한 배경 조건과 직접 구조 |
| 생성형 AI 붐 | 동시 유행과 직접 계보 | 같은 시기 인기와 실제 구조 계통 |

## 실행 가능한 Python 예제로 보기

이번 예제의 목표는 항목 이름을 외우는 것이 아니라, `어떤 기준으로 direct lineage와 surrounding evidence를 나누는가`를 실제 규칙으로 확인하는 것입니다.

문제 상황:

- LLM 계보를 설명할 때 직접 구조 계보와 주변 배경 조건을 섞어 말하기 쉽다

입력:

- 대표 연구 흐름 7개
- 각 흐름의 입력 도메인, 학습 목표, 현재 LLM과의 연결 정도

출력:

- 자동 분류 결과
- 분류 이유

확인할 개념:

- 같은 AI 역사 항목이라도 현재 LLM 구조와의 직접 연결 정도는 다를 수 있다
- direct lineage와 surrounding evidence를 나누면 역사 설명이 과도하게 뭉개지지 않는다
- 분류 이유를 함께 남겨야 왜 같은 시기 인기와 직접 계보를 구분하는지 설명할 수 있다

입력(input):

위에 정리한 역사 항목 목록을 사용합니다.

```python
items = [
    {
        "name": "language modeling",
        "domain": "language",
        "target": "next_token",
        "connects_to_transformer_llm": True,
    },
    {
        "name": "embeddings",
        "domain": "language",
        "target": "representation",
        "connects_to_transformer_llm": True,
    },
    {
        "name": "attention",
        "domain": "language",
        "target": "sequence_alignment",
        "connects_to_transformer_llm": True,
    },
    {
        "name": "Transformer",
        "domain": "language",
        "target": "sequence_modeling",
        "connects_to_transformer_llm": True,
    },
    {
        "name": "YOLO",
        "domain": "vision",
        "target": "object_detection",
        "connects_to_transformer_llm": False,
    },
    {
        "name": "Deep Voice",
        "domain": "speech",
        "target": "speech_generation",
        "connects_to_transformer_llm": False,
    },
    {
        "name": "GPU scaling",
        "domain": "infrastructure",
        "target": "compute_enablement",
        "connects_to_transformer_llm": False,
    },
]


def classify_item(item):
    if item["domain"] == "language" and item["connects_to_transformer_llm"]:
        reason = "언어 입력과 문맥 계산 흐름이 현재 LLM 구조로 직접 이어짐"
        return "direct_lineage", reason

    reason = "LLM 성장을 도왔지만 현재 언어 모델 구조의 직접 조상이라고 보기는 어려움"
    return "surrounding_evidence", reason


grouped = {"direct_lineage": [], "surrounding_evidence": []}

for item in items:
    label, reason = classify_item(item)
    grouped[label].append(item["name"])
    print(
        item["name"],
        "->",
        label,
        "| domain =",
        item["domain"],
        "| target =",
        item["target"],
        "| reason =",
        reason,
    )

print("\n[summary]")
for label, names in grouped.items():
    print(label, "=", names)
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
language modeling -> direct_lineage | domain = language | target = next_token | reason = 언어 입력과 문맥 계산 흐름이 현재 LLM 구조로 직접 이어짐
embeddings -> direct_lineage | domain = language | target = representation | reason = 언어 입력과 문맥 계산 흐름이 현재 LLM 구조로 직접 이어짐
attention -> direct_lineage | domain = language | target = sequence_alignment | reason = 언어 입력과 문맥 계산 흐름이 현재 LLM 구조로 직접 이어짐
Transformer -> direct_lineage | domain = language | target = sequence_modeling | reason = 언어 입력과 문맥 계산 흐름이 현재 LLM 구조로 직접 이어짐
YOLO -> surrounding_evidence | domain = vision | target = object_detection | reason = LLM 성장을 도왔지만 현재 언어 모델 구조의 직접 조상이라고 보기는 어려움
Deep Voice -> surrounding_evidence | domain = speech | target = speech_generation | reason = LLM 성장을 도왔지만 현재 언어 모델 구조의 직접 조상이라고 보기는 어려움
GPU scaling -> surrounding_evidence | domain = infrastructure | target = compute_enablement | reason = LLM 성장을 도왔지만 현재 언어 모델 구조의 직접 조상이라고 보기는 어려움

[summary]
direct_lineage = ['language modeling', 'embeddings', 'attention', 'Transformer']
surrounding_evidence = ['YOLO', 'Deep Voice', 'GPU scaling']
```

그래서 이 예제에서 확인해야 할 결과는 항목 이름을 많이 아는가보다, 역사 설명을 `직접 구조사`와 `주변 확산사`로 실제 기준에 따라 나누어 읽는가입니다.

## 이 예제를 계보 선별 관점으로 다시 보면

이 분류 예제는 역사 서술을 `유명한 이름 나열`로 끝내지 않게 해 줍니다. 어떤 항목이 LLM 구조의 직접 계보를 이루는지, 어떤 항목이 같은 시대의 확산과 기대를 보여 주는 주변 근거인지를 구분해야 이후 역사 설명도 더 선명해집니다.

여기서는 바로 앞의 P6-18.1에서 잡은 큰 발전 흐름을 `무엇이 직접 구조사이고 무엇이 배경 확산사인가`라는 기준으로 더 좁혀 읽습니다. 그래야 여러 딥러닝 성과를 하나의 직선 역사로 뭉뚱그리지 않고, 현재 LLM 구조를 만든 직접 계보를 더 선명하게 구분할 수 있습니다.

하지만 커리큘럼 관점에서는 다음 구분이 더 중요합니다.

- `직접 구조사`: 현재 LLM을 만든 핵심 계보
- `주변 확산사`: 딥러닝이 왜 강해졌고 왜 널리 받아들여졌는지 보여 주는 사례

이 구분이 있어야 Part 6에서 다룬 BERT, GPT, pretraining, prompt, RAG, agent를 다시 떠올릴 때 구조와 분위기를 섞지 않게 됩니다.

## 본류와의 연결

여기까지 구분이 잡히면 앞에서 본 본류 설명을 더 좁은 구조 질문으로 다시 읽을 수 있습니다.

- 그렇다면 LLM 관점에서 Transformer 구조를 다시 보면 무엇이 핵심인가?
- 토큰, context window, causal generation과 연결되는 지점은 어디인가?

이 질문은 본류의 P6-3.1 Transformer를 LLM 관점에서 다시 읽게 만듭니다. 즉, 이 절은 새 장으로 밀고 나가는 절이라기보다, 본류를 역사 구분 위에서 다시 정리하는 배경 장입니다.

## 언제 직접 계보와 주변 근거 구분을 먼저 떠올려야 하는가

| 상황 | 먼저 떠올릴 관점 | 왜 중요한가 |
| --- | --- | --- |
| 유명한 AI 사건을 모두 LLM 역사 한 줄로 묶고 싶어질 때 | 구조 조상과 배경 조건을 나눠야 한다는 점 | 같은 딥러닝 성과라도 현재 LLM 구조와 직접 이어지는지, 확산 배경을 설명하는지에 따라 역할이 다릅니다. |
| GPU, YOLO, 음성 생성 사례를 Transformer와 같은 선 위에 놓고 설명하려 할 때 | 직접 구조 계보와 주변 확산 근거는 다른 층위라는 점 | 계산 자원과 사회적 확산은 중요하지만, 언어 모델 구조 자체의 직접 조상과는 구분해 설명해야 과장이 줄어듭니다. |
| BERT, GPT, Transformer를 다시 읽을 때 무엇을 배경으로 볼지 헷갈릴 때 | 이 절이 구조 설명과 배경 설명의 경계선을 잡아 준다는 점 | 직접 계보 구분을 해 두어야 뒤의 비교 장과 앞의 본류 설명을 덜 섞게 됩니다. |

## 이 절에서 기억할 관점

- 직접 계보는 현재 LLM 구조와 학습 방식으로 직접 이어지는 흐름입니다.
- 주변 근거는 딥러닝 확산과 계산 환경 변화를 설명하지만, 곧바로 구조적 조상이라고 단정하기는 어렵습니다.
- 이 구분에서 확인해야 할 결과는 어떤 요소가 현재 LLM 구조의 직접 계보인지, 어떤 요소가 주변 확산 조건인지를 섞지 않고 설명할 수 있는가입니다.
- 앞서 읽은 Transformer를 다시 떠올릴 때 구조적 위치를 더 정확히 잡을 수 있습니다.
- 이 절은 본류를 늦추기 위한 장이 아니라, 뒤 장의 구조 설명을 덜 과장되게 읽기 위한 짧은 배경 장입니다.

## 짧은 점검

- 직접 계보를 `현재 LLM 구조와 학습 방식으로 직접 이어지는 흐름`, 주변 근거를 `확산과 인프라 배경`으로 설명할 수 있어야 합니다.
- 유명한 사건의 동시성이나 영향력과 구조적 조상 여부는 다른 판단 기준이라는 점을 말할 수 있어야 합니다.
- 이 절은 새 역사 목록이 아니라, 본류를 과장 없이 다시 해석하게 만드는 경계선이라는 점을 잡고 있어야 합니다.

## 언제 이 관점을 먼저 떠올려야 하는가

- 직접 계보와 주변 근거를 구분해 설명할 수 있는가?
- YOLO, Deep Voice 같은 사례를 왜 주변 근거로 두는지 말할 수 있는가?
- 왜 Transformer, Attention, language modeling은 직접 계보라고 할 수 있는지 설명할 수 있는가?
- 이 구분이 Part 6 전체 이해에 왜 중요한지 말할 수 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., [Attention Is All You Need](https://papers.nips.cc/paper/7181-attention-is-all-you-need){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2017, 확인 날짜: 2026-07-05.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2018, 확인 날짜: 2026-07-05.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 확인 날짜: 2026-07-05.
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, [ImageNet Classification with Deep Convolutional Neural Networks](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2012, 확인 날짜: 2026-07-05.
- Joseph Redmon et al., [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640){: target="_blank" rel="noopener noreferrer" }, CVPR, 2016, 확인 날짜: 2026-07-05.
- Sercan O. Arik et al., [Deep Voice: Real-time Neural Text-to-Speech](https://proceedings.mlr.press/v70/arik17a.html){: target="_blank" rel="noopener noreferrer" }, ICML, 2017, 확인 날짜: 2026-07-05.
