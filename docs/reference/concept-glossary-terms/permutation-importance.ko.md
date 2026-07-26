<a id="permutation-importance"></a>

### 순열 중요도(permutation importance)

- 뜻: permutation importance는 특정 특징 값을 무작위로 섞은 뒤 모델 성능이 얼마나 떨어지는지 보고 특징의 중요도를 추정하는 방법입니다.
- 왜 중요한가: MDI가 모델 내부 분기 사용량을 요약한다면, permutation importance는 그 특징이 깨졌을 때 실제 예측 성능이 얼마나 흔들리는지 확인합니다.
- 함께 볼 개념: `특징 중요도(feature importance)`, `랜덤포레스트(random forest)`, `상관 특성(correlated features)`
- 중심 Section: `P4-15.2`
- 등장 Section: `P4-15.2`
