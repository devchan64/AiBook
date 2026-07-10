# P3-8.6 확정 라벨이 검토된 사례에만 남아 있다면 해석에서 무엇을 함께 적어야 하는가

> Section ID: `P3-8.6`
> Version: `v2026.07.10`

해석 단계에서는 숫자 차이뿐 아니라 `누가 확정 라벨을 얻었는가`도 함께 봐야 할 때가 있습니다. 현실 운영에서는 모든 사건에 같은 깊이의 검토가 들어가지 않습니다. 이상해 보인 일부 사례만 사람이 다시 보고, 그 사례에만 확정 라벨이 남을 수 있습니다. 이 상태를 숨기면 독자는 `라벨이 있는 사례 집합`을 `전체 사건 집합`처럼 읽기 쉽습니다.

확정 라벨이 검토된 사례에만 남아 있다면, 그 라벨은 전체를 대표한다고 바로 읽으면 안 됩니다.

| 보이는 상태 | 해석에서 함께 적어야 하는 것 |
| --- | --- |
| 일부 사례에만 확정 라벨이 있다 | 어떤 기준으로 그 사례들만 검토됐는가 |
| `review_needed=0` 사례는 거의 재확인되지 않았다 | 라벨 없음이 정상인지 미확인인지 |
| 특정 기간·장비에만 라벨이 몰린다 | 라벨 집합의 편중 가능성 |

예를 들어 아래 표를 보겠습니다.

| event_id | review_needed | manually_reviewed | confirmed_root_cause |
| --- | ---: | ---: | --- |
| A | 1 | 1 | sensor_drop |
| B | 1 | 1 | valve_delay |
| C | 0 | 0 | None |
| D | 0 | 0 | None |

이때 `confirmed_root_cause`가 있는 두 건만 보고 전체 운영의 원인 분포를 말하면 과장될 수 있습니다. 왜 A와 B만 사람이 봤는지, C와 D는 정말 정상이라 비었는지, 아니면 단지 아직 안 봤는지를 같이 적어야 합니다.

해석 단계에서는 아래 메모면 충분합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 검토 대상이 되는 기준 | 선택적으로 라벨이 남는 구조를 드러내기 위해 |
| 라벨 없음의 뜻 | 정상과 미확인을 섞지 않기 위해 |
| 라벨 있는 집합의 범위 편중 | 해석 강도를 과장하지 않기 위해 |

여기서 중요한 점은 `선택적으로 붙은 확정 라벨은 해석 근거가 될 수는 있지만, 전체 사건을 대표하는 정답 집합처럼 읽기 전에 검토 경로와 편중을 먼저 적어야 한다`는 사실입니다. 따라서 확정 라벨 표는 `전체 사건의 정답표`가 아니라, 검토 경로를 거친 일부 사건의 확인 결과일 수 있다는 점을 먼저 봐야 합니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. label은 각 example에 붙은 결과 정보라는 기본 틀을 제공하므로, 일부 사례에만 확정 라벨이 남아 있다면 그 라벨 집합이 전체 사건 집합과 같은 범위를 대표하지 않을 수 있다는 이 절의 설명을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. 어떤 결과가 어떤 검토 절차를 거쳐 생성되었는지를 provenance information으로 남기는 관점을 제공하므로, 확정 라벨이 붙은 사례 집합에서는 검토 경로와 라벨 없음의 뜻을 함께 적어야 한다는 이 절의 일반 근거가 됩니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
