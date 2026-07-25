<a id="skip-gram"></a>

### 스킵그램(Skip-gram)

- 뜻: 가운데 단어를 보고 주변 단어들을 예측하도록 학습하는 word2vec 방식의 하나입니다. CBOW가 주변 단어에서 중심 단어를 맞히는 방향이라면, Skip-gram은 중심 단어에서 주변 문맥을 맞히는 방향입니다. 즉 Skip-gram은 `이 단어가 나오면 어떤 주변 단어가 함께 나올 가능성이 큰가`를 이용해 단어 벡터를 학습합니다.
- 왜 중요한가: word2vec의 핵심이 단어 정의를 저장하는 데 있지 않고, 예측 과제를 통해 문맥 통계를 벡터 공간에 옮기는 데 있다는 점을 분명히 해 주기 때문입니다. 이 개념이 있어야 `문맥으로 단어를 배운다`는 표현을 하나의 막연한 절차가 아니라, 입력과 예측 목표가 정해진 학습 문제로 읽을 수 있습니다.
- 함께 볼 개념: `워드투벡(word2vec)`, `연속 bag-of-words(CBOW, continuous bag-of-words)`, `임베딩(embedding)`, `분산 표현(distributed representation)`
- 중심 Section: `P1-11.1`
- 등장 Section:
