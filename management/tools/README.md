# 관리 도구

이 디렉터리는 책 본문 밖에서 사용하는 저장소 관리용 스크립트를 둔다. 공개 배포 본문이나 최종 원고가 아니라, 집필·검수·정리 작업을 돕는 보조 도구다.

## 번역 게이트웨이 리포트

`translation_quality_report.py`는 한국어 원문과 영어 또는 중국어 번역 원고를 파일별로 대조해 Markdown 리포트를 만든다. 이 리포트의 목적은 최종 편집 승인이 아니라, 산출물이 추가 번역이나 집중 검수를 더 거쳐야 하는지 초기에 걸러내는 것이다.

게이트웨이 판정:

- `통과`: 기계 점검과 Ollama 점검에서 즉시 차단 신호가 없는 파일
- `기계 점검 확인 필요`: 메타데이터, 라인 수, 제목, 코드 펜스 차이 같은 구조 신호가 있는 파일
- `번역 검수 필요`: Ollama가 의미 보존, 용어, 링크, 과축약 등을 사람 검수 대상으로 본 파일
- `추가 번역 필요`: 번역 파일 누락 또는 실질적 누락·의미 이동 가능성이 큰 파일

기계 점검 항목:

- `Section ID`, `Version` 일치 여부
- 빈 줄 제외 라인 수 차이와 5% 이상 경고
- 제목 수, 링크 수, 코드 펜스 수 차이
- 번역 파일 누락 여부

Ollama 점검 항목:

- 제목 구간 기반 슬라이딩 검수
- 각 구간에 앞뒤 문맥 일부를 붙인 의미 보존 점검
- 원문 중심 질문과 설명 범위 보존 여부
- 설명 누락, 과축약, 의미 이동
- 용어 구분과 링크 품질
- 파일별 점수, 상태, 게이트웨이 판정, 수정 제안

사용 예:

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --locale en \
  --root docs/parts/part-06 \
  --model qwen2.5:14b
```

긴 원고는 한 번에 전체 문서를 평가하면 작은 누락이나 문단 단위 의미 이동을 놓칠 수 있다. 기본 Ollama 모드는 Markdown 제목을 기준으로 원문과 번역본을 구간화하고, 각 구간에 앞뒤 문맥 일부를 붙여 슬라이딩 방식으로 먼저 점검한 뒤 전체 파일 판정을 함께 남긴다.

구간 크기와 문맥 범위는 다음 옵션으로 조정한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --locale en \
  --root docs/parts/part-06 \
  --segment-max-chars 7000 \
  --context-lines 3
```

Ollama 없이 기계 점검만 실행하려면 다음처럼 실행한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --locale en \
  --root docs/parts/part-06 \
  --skip-llm
```

배치나 CI에서 게이트웨이 차단 신호를 종료 코드로 받고 싶다면 `--fail-on-review`를 붙인다. 이 옵션은 추가 번역 또는 검수가 필요한 파일이 하나라도 있으면 종료 코드 `3`을 반환한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --locale en \
  --root docs/parts/part-06 \
  --fail-on-review
```

기본 리포트 위치는 `management/authoring/translation-quality/`이다. 특정 파일로 저장하려면 `--output`을 지정한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --locale zh \
  --root docs/parts \
  --output management/authoring/translation-quality/zh-report.md
```

Ollama 실행 전에는 로컬에서 Ollama 서버가 떠 있고 지정한 모델이 준비되어 있어야 한다.

```bash
ollama pull qwen2.5:14b
ollama serve
```
