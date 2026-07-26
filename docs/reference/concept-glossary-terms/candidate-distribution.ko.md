<a id="candidate-distribution"></a>

### 후보 분포(candidate distribution)

- 뜻: 현재 문맥이나 조건에서 다음에 나올 수 있는 여러 후보와 그 상대적인 그럴듯함을 함께 본 분포입니다. 후보가 모두 같은 가능성으로 놓여 있는 것이 아니라, 어떤 후보는 강하고 어떤 후보는 약하게 놓입니다.
- 왜 중요한가: LLM 생성은 완성 문장을 한 번에 꺼내는 과정이 아니라, 현재 문맥에서 후보 분포를 만들고 실제 조각을 선택한 뒤 새 문맥에서 다시 후보 분포를 만드는 반복입니다. 이 개념이 있어야 sampling, temperature, next-token prediction을 단순 설정값이 아니라 생성 흐름을 읽는 도구로 볼 수 있습니다.
- 함께 볼 개념: `샘플링(sampling)`, `다음 토큰 예측(next-token prediction)`, `문맥(context)`, `temperature`
- 중심 Section: `P6-1.3`
- 등장 Section: `P6-4.1`
