<a id="prediction-contract"></a>
<a id="glossary-prediction-contract"></a>

### 예측 계약(prediction contract)

- 뜻: 예측 문제에서 어떤 값을 입력으로 쓰고, 어떤 결과를 맞히며, 어느 시점까지의 정보만 사용할 수 있는지를 함께 닫아 둔 약속입니다. 열 이름만 나누는 것이 아니라 각 열이 언제 생기는지, 운영 시점에서도 같은 방식으로 만들 수 있는지까지 포함합니다.
- 왜 중요한가: 예측 시점 이후에 생기는 값이 입력에 섞이면 점수는 좋아 보여도 실제 운영 예측 문제는 깨집니다. 예측 계약이 있어야 특징, 목표 후보, 시간 경계, 누수 방지, 재현 가능성을 한 묶음으로 점검할 수 있습니다.
- 함께 볼 개념: `특징(feature)`, `목표 라벨 후보(target candidate)`, `데이터 누수(data leakage)`, `재현성(reproducibility)`
- 중심 Section: `P3-9.7`
- 등장 Section: `P3-9.7`
