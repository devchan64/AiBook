<a id="oob-score"></a>

### oob_score

- 뜻: bootstrap 과정에서 특정 트리의 학습에 들어가지 않은 out-of-bag 샘플을 이용해 랜덤포레스트의 내부 평가 신호를 계산할지 정하는 설정입니다.
- 왜 중요한가: OOB는 별도 검증처럼 보이는 감각을 일부 제공하지만, 모든 평가 절차를 대체하는 만능 기준은 아닙니다. bootstrap 구조에서 자연스럽게 생기는 보조 확인 수단으로 읽어야 합니다.
- 함께 볼 개념: `부트스트랩(bootstrap)`, `랜덤포레스트(random forest)`, `검증(validation)`, `테스트(test)`
- 중심 Section: `P4-15.3`
- 등장 Section: `P4-15.1`, `P4-15.3`
