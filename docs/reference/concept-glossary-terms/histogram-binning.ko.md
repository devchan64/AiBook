<a id="histogram-binning"></a>

### 히스토그램 비닝(histogram binning)

- 뜻: 연속값을 원본 값 하나하나로 모두 보지 않고 여러 구간(bin)으로 묶어 계산하는 방식입니다. 부스팅에서는 분할 후보 계산을 더 빠르고 메모리 효율적으로 만들기 위해 자주 사용됩니다.
- 왜 중요한가: 그래디언트 부스팅은 stage마다 분할을 반복해서 찾기 때문에 데이터가 커질수록 계산 비용이 빠르게 늘어납니다. histogram binning은 약간의 근사를 받아들이는 대신 더 빠르게 반복할 수 있게 해 주며, LightGBM 같은 구현의 실무 감각을 이해하는 데 필요합니다.
- 함께 볼 개념: `분포(distribution)`, `그래디언트 부스팅(gradient boosting)`, `근사 검색(approximate search)`
- 중심 Section: `P4-16.3`
- 등장 Section: `P4-16.3`
