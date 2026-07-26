<a id="distributed-training"></a>

### 분산 학습(distributed training)

- 뜻: 하나의 학습 작업을 여러 계산 자원이나 worker에 나누어 실행하는 방식입니다. 부스팅에서는 큰 데이터, 많은 stage, 여러 검증 조합을 감당하기 위해 언급됩니다.
- 왜 중요한가: 분산 학습은 모델 철학 자체를 바꾸기보다 긴 반복과 큰 데이터를 운영 가능한 시간 안에 처리하려는 선택입니다. 부스팅에서는 worker별 데이터 분배, stage 기록, 실패 재시작 기준이 일관되어야 결과 비교가 가능해집니다.
- 함께 볼 개념: `GPU`, `그래디언트 부스팅(gradient boosting)`, `검증 데이터(validation data)`
- 중심 Section: `P4-16.3`
- 등장 Section: `P4-16.3`
