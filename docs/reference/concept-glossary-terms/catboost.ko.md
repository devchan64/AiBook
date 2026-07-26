<a id="catboost"></a>

### CatBoost

- 뜻: 범주형 특징(categorical feature)을 다루는 흐름과 ordered boosting을 강조하는 그래디언트 부스팅 라이브러리입니다. 범주형 데이터 처리와 target leakage 완화가 주요 설계 관점으로 자주 언급됩니다.
- 왜 중요한가: CatBoost는 부스팅 구현 선택에서 `범주형 데이터를 얼마나 안전하게 다룰 것인가`가 별도의 기준이 될 수 있음을 보여 줍니다. 범주형 열이 많거나 target encoding의 누수가 걱정되는 장면에서 왜 다른 구현 감각이 필요한지 이해하게 해 줍니다.
- 함께 볼 개념: `그래디언트 부스팅(gradient boosting)`, `범주형 특징(categorical feature)`, `누수(leakage)`
- 중심 Section: `P4-16.3`
- 등장 Section: `P4-16.3`
