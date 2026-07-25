<a id="nondeterministic"></a>

### 비결정적(nondeterministic)

- 뜻: 같은 입력이나 상태에서도 결과가 하나로 고정되지 않을 수 있는 성질입니다. 하나의 규칙 경로만 있는 것이 아니라, 여러 다음 상태나 결과 가능성이 열려 있는 조건이라고 볼 수 있습니다. 즉 비결정적이라는 말은 `반드시 하나의 다음 결과로 닫히지 않는다`는 구조를 가리키며, 곧바로 무작위 선택을 뜻하는 것은 아닙니다.
- 왜 중요한가: 규칙이 모자라서 여러 경로가 가능한 경우, 무작위 요소가 들어간 경우, 외부 상태에 따라 실행이 달라지는 경우를 한데 섞지 않고 읽는 출발점이 되기 때문입니다. 이 개념이 있어야 `정답이 하나로 결정되지 않는다`는 말이 언제는 탐색 문제를 뜻하고 언제는 확률적 생성이나 시스템 실행 차이를 뜻하는지 더 조심해서 구분하게 됩니다. 또한 비결정적을 이해해야 `결과가 여러 개일 수 있다`와 `그중 하나를 무작위로 고른다`를 다른 층위로 읽게 됩니다.
- 함께 볼 개념: `무작위(random)`, `확률적 과정(stochastic process)`, `불확실성(uncertainty)`
- 중심 Section: `P1-6.2`

--8<-- "reference/concept-glossary-terms/comparison-result.ko.md"


--8<-- "reference/concept-glossary-terms/comparison-report.ko.md"


--8<-- "reference/concept-glossary-terms/comparison-table.ko.md"


--8<-- "reference/concept-glossary-terms/confidential-information.ko.md"
