<a id="feature-definition-identity"></a>
<a id="glossary-feature-definition-identity"></a>

### 특징 정의 동일성(feature-definition identity)

- 뜻: 두 열이나 두 행의 특징이 같은 이름을 쓰는지를 넘어서, 같은 단위, 같은 생성 규칙, 같은 수집 버전, 같은 운영 정의를 따르는지 확인하는 기준입니다. 열 이름이 같아도 측정 방식이나 계산 규칙이 바뀌면 같은 특징 정의라고 보기 어렵습니다.
- 왜 중요한가: 기준선 비교와 모델 입력은 같은 의미의 특징끼리 묶인다는 전제가 있어야 해석됩니다. 특징 정의 동일성을 확인하지 않으면 센서 변경, 단위 변경, 구간 규칙 변경으로 생긴 차이를 실제 현상 변화나 모델 문제로 오해할 수 있습니다. 이 기준이 있어야 같은 열 이름 아래에 서로 다른 정의가 섞였는지 먼저 점검할 수 있습니다.
- 함께 볼 개념: `특징(feature)`, `기준선(baseline)`, `비교 가능성(comparability)`, `데이터 품질 점검(data quality check)`
- 중심 Section: `P3-6.6`
- 등장 Section: `P3-6.6`
