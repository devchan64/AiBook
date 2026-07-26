<a id="incomplete-negative"></a>
<a id="glossary-incomplete-negative"></a>

### 관측 미완료 음성(incomplete negative)

- 뜻: 아직 충분한 추적 기간이 지나지 않았는데 결과가 보이지 않는다는 이유만으로 0처럼 보이는 사례입니다. 닫힌 음성은 충분히 관측한 뒤에도 결과가 없다고 말할 수 있는 경우이고, 관측 미완료 음성은 아직 그렇게 말할 근거가 부족한 상태입니다.
- 왜 중요한가: 관측 미완료 음성을 닫힌 0으로 학습하면 모델은 최근 사례의 라벨을 과하게 안전한 쪽으로 배울 수 있습니다. 이 개념이 있어야 0을 붙이기 전에 필요한 관측 기간, `pending` 상태, 라벨 확정 기준을 데이터 모델링 조건으로 남기게 됩니다.
- 함께 볼 개념: `라벨 확정 지연(delayed label confirmation)`, `라벨(label)`, `목표 라벨 후보(target candidate)`, `선택적 라벨(selective labels)`
- 중심 Section: `P3-9.10`
- 등장 Section: `P3-9.10`
