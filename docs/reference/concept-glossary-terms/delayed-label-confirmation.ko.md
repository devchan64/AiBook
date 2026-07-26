<a id="delayed-label-confirmation"></a>
<a id="glossary-delayed-label-confirmation"></a>

### 라벨 확정 지연(delayed label confirmation)

- 뜻: 실제 결과는 발생했거나 나중에 확인될 수 있지만, 현재 시점에는 아직 정답 라벨로 닫히지 않은 상태입니다. 즉 값이 없다는 뜻이 아니라, 정답으로 확정되는 시간이 늦다는 문제입니다.
- 왜 중요한가: 라벨 확정 지연을 0이나 결측으로 섞어 버리면 최근 사례가 실제보다 안전해 보이거나, 아직 임시 상태인 값을 확정 라벨처럼 학습에 넣게 됩니다. 이 개념이 있어야 결과가 늦게 닫히는 문제와 결과가 없다고 말할 수 있는 문제를 분리하고, 라벨을 붙이는 기준 시점과 추적 기간을 함께 기록할 수 있습니다.
- 함께 볼 개념: `라벨(label)`, `목표 라벨 후보(target candidate)`, `관측 미완료 음성(incomplete negative)`, `출처 추적(provenance)`
- 중심 Section: `P3-9.10`
- 등장 Section: `P3-9.10`
