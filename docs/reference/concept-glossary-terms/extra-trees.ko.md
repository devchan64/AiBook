<a id="extra-trees"></a>

### Extra Trees(Extremely Randomized Trees)

- 뜻: Extra Trees는 여러 결정트리를 모아 예측을 평균내는 트리 앙상블입니다. 랜덤포레스트와 비슷하지만, 각 분기에서 threshold 후보를 더 무작위로 뽑아 숲 전체의 다양성을 키우는 쪽에 더 가깝습니다.
- 왜 중요한가: 랜덤포레스트 바로 옆에서 비교해 볼 수 있는 가까운 후보입니다. 기본 설정에서는 `bootstrap=False`이므로 OOB가 자동으로 따라오지 않는다는 점도 함께 구분해야 합니다.
- 함께 볼 개념: `랜덤포레스트(random forest)`, `best split`, `random threshold`, `bootstrap`, `oob_score`
- 중심 Section: `P4-15.4`
- 등장 Section: `P4-15.4`
