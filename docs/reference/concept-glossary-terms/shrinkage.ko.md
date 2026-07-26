<a id="shrinkage"></a>

### 수축(shrinkage)

- 뜻: 그래디언트 부스팅에서 각 단계 약한 학습기(weak learner)의 보정을 학습률(learning rate)로 줄여 반영하는 전략입니다. 새 단계가 만든 correction을 그대로 모두 더하지 않고, 작은 비율만 반영해 모델이 천천히 움직이게 합니다.
- 왜 중요한가: 부스팅은 남은 오차를 계속 줄이기 때문에 한 단계 보정이 너무 강하면 훈련 데이터의 잡음까지 빠르게 따라갈 수 있습니다. shrinkage는 보정 속도를 늦춰 과한 수정과 과적합 위험을 줄이는 기본 제어 장치입니다. 다만 learning rate를 작게 잡으면 보통 더 많은 단계가 필요하므로 `n_estimators`와 함께 읽어야 합니다.
- 함께 볼 개념: `그래디언트 부스팅(gradient boosting)`, `학습률(learning rate)`, `과적합(overfitting)`
- 중심 Section: `P4-16.2`
- 등장 Section: `P4-16.2`
