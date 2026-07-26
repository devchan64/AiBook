<a id="lightgbm"></a>

### LightGBM

- 뜻: 대규모 표 형식 데이터에서 효율적인 그래디언트 부스팅 결정트리 학습을 목표로 한 부스팅 라이브러리입니다. histogram 기반 분할, leaf-wise 성장, GOSS, EFB 같은 효율화 전략이 대표적으로 언급됩니다.
- 왜 중요한가: LightGBM은 같은 부스팅이라도 `더 빠르고 가볍게 반복하기 위한 구현 선택`이 있다는 점을 보여 줍니다. 특히 stage가 많고 데이터가 클 때, 속도와 메모리 절충이 모델 선택의 중요한 기준이 될 수 있음을 이해하게 해 줍니다.
- 함께 볼 개념: `그래디언트 부스팅(gradient boosting)`, `히스토그램 비닝(histogram binning)`, `과적합(overfitting)`
- 중심 Section: `P4-16.3`
- 등장 Section: `P4-16.3`
