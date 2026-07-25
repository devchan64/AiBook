## ㅋ

--8<-- "reference/concept-glossary-terms/confabulation.ko.md"

--8<-- "reference/concept-glossary-terms/k-nnk-nearest-neighbors.ko.md"

--8<-- "reference/concept-glossary-terms/kv-cache.ko.md"

### QLoRA

- 뜻: LoRA 조정 방식에 양자화(quantization)를 함께 써서, 큰 기반 모델을 더 낮은 메모리 조건에서 다루기 쉽게 하려는 실무 확장입니다. 핵심은 기반 모델 본체를 더 가볍게 들고 있으면서, 적응에 필요한 작은 조정분은 LoRA처럼 따로 학습해 메모리 부담과 적응 유연성을 함께 잡으려는 데 있습니다. 즉 `효율적 조정`과 `효율적 저장`을 결합한 형태라고 볼 수 있습니다.
- 왜 중요한가: LoRA 자체와 메모리 제약 완화가 어떻게 결합되는지 이해해야 제한된 자원에서 어떤 조정 전략을 고를지 설명할 수 있기 때문입니다. 이 개념이 있어야 `조정 가능성`과 `메모리 가능성`을 따로 보지 않고 함께 판단하게 되고, 같은 기반 모델도 하드웨어 제약에 따라 현실적인 조정 방법이 달라진다는 점을 더 분명히 읽게 됩니다. 또한 QLoRA는 `모델이 너무 커서 조정은 불가능하다`는 판단이 절대적인 것이 아니라, 어떤 저장 형식과 적응 방식을 쓰느냐에 따라 현실 조건이 달라질 수 있음을 보여 주는 대표 사례이기도 합니다.
- 함께 볼 개념: `LoRA`, `양자화(quantization)`, `미세조정(fine-tuning)`
- 중심 Section: `P6-9.5`

--8<-- "reference/concept-glossary-terms/caching.ko.md"

--8<-- "reference/concept-glossary-terms/commit.ko.md"

--8<-- "reference/concept-glossary-terms/code-cell.ko.md"

--8<-- "reference/concept-glossary-terms/cosine-similarity.ko.md"

--8<-- "reference/concept-glossary-terms/colab.ko.md"

### 쿼리-키-값(query-key-value, QKV)

- 뜻: attention 계산에서 현재 위치가 무엇을 찾는지 나타내는 query, 각 위치가 어떤 정보인지 알려 주는 key, 실제로 섞어 올 내용을 담는 value를 함께 묶어 부르는 표현입니다. 즉 query는 `무엇을 찾고 싶은가`, key는 `어디가 그 조건에 맞는가`, value는 `그래서 실제로 무엇을 가져올 것인가`를 나누어 맡는 구조입니다.
- 왜 중요한가: attention 직관을 `질문하고, 맞는 위치를 찾고, 그 내용을 가져온다`는 계산 흐름으로 다시 읽게 해 주어, Transformer 설명에서 반복되는 QKV 이름을 덜 추상적으로 만들기 때문입니다. 이 개념이 있어야 attention이 단순 가중합이 아니라, 조회 기준과 내용 전달이 분리된 구조라는 점을 이해하게 됩니다. 또한 QKV를 이해해야 같은 attention 블록 안에서도 `유사도 계산용 정보`와 `실제 전달 내용`이 서로 다른 역할이라는 점을 더 분명하게 읽게 됩니다.
- 함께 볼 개념: `셀프 어텐션(self-attention)`, `멀티헤드 어텐션(multi-head attention)`, `트랜스포머(Transformer)`
- 중심 Section: `P5-13.3`
- 등장 Section: `P5-14.1`, `P6-4.3`

### 큐(queue)

- 뜻: 먼저 들어온 값을 먼저 꺼내는 규칙으로 작동하는 자료구조 또는 추상 자료형입니다. 줄 서기와 비슷하게, 앞에서 기다리던 항목이 먼저 처리되는 `선입선출(FIFO, first-in first-out)` 구조로 이해하면 됩니다. 즉 `도착 순서`를 보존한 채 처리 순서를 정하고 싶을 때 쓰는 기본 장치입니다. 컴퓨터에서는 보통 `뒤에 넣고(enqueue) 앞에서 꺼내는(dequeue)` 흐름으로 설명하며, 이 두 동작이 큐의 핵심을 이룹니다.
- 왜 중요한가: 요청 처리 순서, 작업 대기열, 메시지 전달처럼 `도착한 순서` 자체가 중요한 시스템을 설명할 때 가장 기본적인 모델이 되기 때문입니다. 스택처럼 가장 최근 것을 먼저 꺼내는 구조와 구분해야 작업 흐름과 병목 위치를 더 정확히 읽을 수 있고, 큐 길이가 길어진다는 말이 곧 처리 속도보다 유입 속도가 더 빠르다는 운영 신호라는 점도 함께 이해하게 됩니다. 이 개념이 있어야 운영체제의 작업 스케줄링, 서버의 요청 대기열, 데이터 처리 파이프라인의 버퍼를 볼 때 `무엇이 얼마나 밀리고 있는가`를 순서 관점에서 해석할 수 있습니다.
- 함께 볼 개념: `스택(stack)`, `선형 구조(linear structure)`, `자료구조(data structure)`
- 중심 Section: `P2-9.4`
- 등장 Section: `P3-4.2`

--8<-- "reference/concept-glossary-terms/client.ko.md"

--8<-- "reference/concept-glossary-terms/class.ko.md"

--8<-- "reference/concept-glossary-terms/cluster-label.ko.md"

--8<-- "reference/concept-glossary-terms/key.ko.md"
