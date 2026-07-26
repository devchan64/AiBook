# Section Release Note

- Section ID: `P3-index`
- Source File: `docs/parts/part-03/index.md`

### v2026.07.25
- 링크 정합성: 한국어판의 `샘플(sample)` 링크가 실제 항목이 포함된 `07-siot` 색인을 가리키도록 수정했다.
- 다국어 링크 정리: 중국어 간체판의 샘플, 특징, 기준선, 비교 리포트, 타깃 링크가 한국어 자음별 색인이 아니라 중국어 병음 색인을 가리키도록 정리했다.
- 번역 반영 상태: 한국어판과 중국어 간체판 링크 경로 반영 완료. 영어판은 기존 영문 색인 링크를 유지하고 본문 `Version`을 동기화했다.
- 관련 자산: 변경 없음.
- 원문 기준 버전: `v2026.07.25`

### v2026.07.20
- 구조 정리: 한국어판, 영어판, 중국어 간체판에서 진행 메타 성격의 목적·읽는 순서·범위 제목을 데이터 모델링의 역할, 문제 구조 흐름, 닫을 경계가 드러나는 제목으로 정리했다.
- 번역 반영 상태: 영어판과 중국어 간체판 반영 완료.
- 원문 기준 버전: `v2026.07.20`
- 변경 이유: 순차 저작권 검토 과정에서 Part 3 시작 페이지의 표준 개념 근거 축과 말미 참고문헌의 대응을 다시 확인했다.
- 본문 반영 내용: 한국어, 영어, 중국어 간체판 본문 `Version`을 `v2026.07.20`으로 갱신하고 기존 출처 확인일을 2026-07-20으로 갱신했다. 본문 표에서 근거 축으로 언급한 Fayyad/KDD와 BLS base period 자료를 세 언어 참고문헌에 추가했다.
- 저작권 검토: Part 3 대표 사례, 원천 로그에서 운영 산출물로 이어지는 표, 데이터 모델링 spine 표는 내부 커리큘럼 흐름에 맞춘 자체 구성 요약이며, 외부 자료의 목차·표·문장을 대체할 정도의 복제는 확인되지 않았다.
- 출처 확인: NASEM 자료에서 데이터과학 학부 교육의 핵심 원칙과 커리큘럼 관점을 확인했다. Google ML Glossary에서 sample, feature, label, label leakage 용어 기준을 확인했다. W3C PROV-Overview에서 provenance, reproducibility, versioning, derivation 축을 확인했다. Fayyad/Piatetsky-Shapiro/Smyth KDD 자료와 BLS CPI base period 설명은 본문 표의 근거 축 누락을 메우는 참고문헌으로 보강했다.
- 번역 동기화 메모: 영어판과 중국어 간체판도 같은 출처 보강과 확인일 갱신을 반영했다.
- 번역 반영 상태: 한국어, 영어, 중국어 간체판 반영 완료.
- 관련 자산: 변경 없음.
- 원문 기준 버전: `v2026.07.20`

### v2026.07.12
- 본문 반영: 집필 순서만 예고하는 `다음 ... 연결` 계열 표지를 제거했다. 본문 메타데이터 버전도 함께 갱신했다.
- 번역 동기화 메모: 영어판과 중국어 간체판에 최신 Part 3 시작 페이지 구조와 메타형 연결 예고 제거를 반영했다. 중국어 간체판 `index.zh.md`에서는 같은 날 표 머리글의 `这个 Part` 표현도 `这一 Part`로 통일했다. / reflected in English and Simplified Chinese on 2026-07-12

### v2026.07.10
- 본문 반영: Part 2와 Part 3의 기본기 점검 관계를 도입부에 합치고, 중반의 흐름 설명도 `정의 고정 -> 표 재구성 -> 해석 경계` 축이 한 번에 읽히도록 재배치했다.
- 번역 동기화 메모: preserve the tighter overview that binds Part 2 linkage, Part 3 responsibility, and the three-part spine into a single flow. / reflected in English and Simplified Chinese on 2026-07-10

### v2026.07.08
- 본문 반영: Chapter 단위 표와 파이프라인 도식을 걷어내고, `역할과 순서 고정 / 비교 구조 재구성 / 해석과 문제 마감`의 3단계 표로 압축해, Part 3 입구에서 큰 흐름과 남기는 구조만 먼저 보이도록 정리했다.
- 본문 반영: `원천 로그 -> 동작 요약 표 -> 최근/기준선 비교표 -> 운영 산출물` 기준표를 추가해, Part 3의 대표 사례가 같은 원천데이터를 서로 다른 행 의미와 산출물 구조로 다시 표현하는 흐름이라는 점을 입구에서 바로 확인할 수 있게 정리했다.
- 번역 동기화 메모: keep the overview centered on Part 3's scope and flow, with only a brief high-level bridge to later learning sections. / pending

### v2026.07.07
- 본문 반영: 도입부와 전체 흐름 설명에서 중복되는 설계 문단을 줄이고, 긴 질문 축 나열을 핵심 묶음으로 압축했다. 말미의 `짧은 점검`은 제거하고, Part 4·5 연결 설명도 입력 구조와 문제 경계를 닫는 수준으로 간소화했다.
- 본문 반영: Part 3 시작 페이지의 전체 흐름을 `10개 Chapter`에서 `9개 Chapter` 구조로 다시 정리했다. 마지막 흐름도 `Chapter 9 안에서 문제 유형 구분과 뒤 Part 연결을 함께 닫는 구조`로 바꾸고, 관련 요약 표와 짧은 점검 문구도 함께 조정했다.
- 번역 동기화 메모: translation should update the displayed `P3-index` version together with the current ten-chapter overview baseline. / pending

### v2026.07.06
- 본문 반영: 3.1과 3.2를 Part 내 최초 개념 설명 위치로 두고, 이후 용어 혼동 시 개념사전이 기준 참조점이 된다는 설명으로 연결 문장을 다듬었다.
- 본문 반영: `Section ID`, `Version` 메타데이터를 추가했다. / 데이터 정리, 특징 설계, 샘플링, 추론, 문제 구조화 소개 문장을 `차례로 확인합니다`로 조정했다. / `DSS/BI/DW/OLAP` 배경 축 설명과 반복 질문 축 소개 문장을 직접 진술형으로 다듬어 Part 3 오버뷰가 데이터 모델링 판단 구조를 바로 설명하도록 정리했다.
- 번역 동기화 메모: translation should reflect the updated ten-chapter structure and preserve the added self-check prompts about problem-expression flow and Part 4 handoff. / pending
