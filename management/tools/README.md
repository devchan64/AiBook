# 관리 도구

이 디렉터리는 책 본문 밖에서 사용하는 저장소 관리용 스크립트를 둔다. 공개 배포 본문이나 최종 원고가 아니라, 집필·검수·정리 작업을 돕는 보조 도구다.

## 근거 원문 수집

`evidence_collector.py`는 원고 Markdown 페이지에 연결된 외부 URL을 찾아 `.tmp/evidence/` 아래에 다운로드한다. 목적은 본문에 쓰인 관련 근거를 실제 원문 파일과 메타데이터로 남겨 검토할 수 있게 하는 것이다.

페이지 하나에 연결된 외부 근거를 수집한다.

```bash
./.venv/bin/python management/tools/evidence_collector.py \
  --target docs/parts/part-06/chapter-01/section-01.md
```

실제 다운로드 전에 수집 대상만 확인하려면 `--dry-run`을 붙인다.

```bash
./.venv/bin/python management/tools/evidence_collector.py \
  --target docs/parts/part-06/chapter-01/section-01.md \
  --dry-run
```

산출물은 기본적으로 `.tmp/evidence/<페이지-경로>/`에 저장된다.

- 원문 파일: URL 해시를 앞에 붙인 다운로드 원본
- `<url-hash>-metadata.json`: URL, URL 해시, 수집 위치, HTTP 메타데이터, 파일 경로
- `index.md`: 수집 결과 요약

URL 해시는 원문 URL의 SHA-256 앞 16자리로 만든다. 따라서 같은 실행 라벨 아래에서 같은 링크를 다시 수집하면 기존 파일을 `skipped-existing`으로 표시하고 다시 다운로드하지 않는다. 실제로 다시 내려받아 갱신해야 할 때만 `--overwrite`를 붙인다.

URL을 직접 지정하거나 URL 목록 파일을 지정할 수도 있다.

```bash
./.venv/bin/python management/tools/evidence_collector.py \
  --url https://example.com/paper.pdf \
  --label p6-example-evidence
```

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

- 라인 윈도우 기반 역번역(back-translation)
- 원문 한국어와 역번역 한국어의 토큰 유사도 비교
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

단일 번역 파일만 점검할 때는 `--target`을 사용한다. 번역 파일 경로에 `.en.md` 또는 `.zh.md` suffix가 있으면 `--locale`은 생략할 수 있다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --target docs/parts/part-06/chapter-01/section-01.en.md \
  --model qwen2.5:14b
```

한국어 원문 파일을 기준으로 대응 번역본을 점검할 때는 `--locale`을 함께 지정한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --target docs/parts/part-06/chapter-01/section-01.md \
  --locale en
```

긴 원고는 한 번에 전체 문서를 평가하면 작은 누락이나 문단 단위 의미 이동을 놓칠 수 있다. 기본 Ollama 모드는 먼저 라인 기반 context window를 만들고 번역문을 한국어로 역번역한 뒤, 원문 한국어와 역번역 한국어의 토큰 유사도를 비교한다. 이어서 Markdown 제목 기준 구간 슬라이딩 검수와 전체 파일 판정을 함께 남긴다.

이 스크립트는 게이트웨이로 쓰기 때문에 민감하게 동작하도록 설계한다. 역번역 토큰 유사도는 좋은 번역을 최종 승인하는 지표가 아니라, 추가 번역이나 검수가 필요한 산출물을 초기에 걸러내는 차단 신호다.

구간 크기와 문맥 범위는 다음 옵션으로 조정한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --locale en \
  --root docs/parts/part-06 \
  --segment-max-chars 7000 \
  --context-lines 3
```

역번역 토큰 비교의 라인 윈도우와 민감도는 다음 옵션으로 조정한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --target docs/parts/part-06/chapter-01/section-01.en.md \
  --line-window-size 24 \
  --line-window-stride 16 \
  --back-translation-threshold 0.72 \
  --back-translation-fail-threshold 0.55
```

Ollama 구간 검수는 쓰되 역번역 토큰 비교만 끄려면 `--skip-back-translation`을 붙인다.

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

기본 리포트 위치는 `.tmp/translation-quality/`이다. `.tmp/`는 `.gitignore`로 제외되므로 실행 산출물을 일괄 관리하기 쉽다. 특정 파일로 저장하려면 `--output`을 지정한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --locale zh \
  --root docs/parts \
  --output .tmp/translation-quality/zh-report.md
```

Ollama 실행 전에는 로컬에서 Ollama 서버가 떠 있고 지정한 모델이 준비되어 있어야 한다.

```bash
ollama pull qwen2.5:14b
ollama serve
```

모델이 없을 때 스크립트가 먼저 내려받게 하려면 `--pull-model`을 붙인다. 모델 다운로드는 용량과 시간이 클 수 있으므로 명시적으로 지정한 경우에만 수행한다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --target docs/parts/part-01/chapter-01/section-01.md \
  --locale en \
  --pull-model
```

`--pull-model`은 Ollama의 스트리밍 pull 진행 이벤트를 사용해 다운로드 상태, 퍼센트, 받은 용량을 stderr에 표시한다. 중간에 끊기면 같은 명령을 다시 실행한다. Ollama는 모델 레이어를 로컬 저장소에 캐시하므로 이미 받은 레이어를 재사용하는 방식으로 이어받기 성격을 가진다.

분석 단계의 저수준 로그가 필요하면 `--verbose`를 붙인다. 선택된 파일 수, 파일별 문자 수, 기계 점검 결과, 제목 구간 수, 역번역 라인 윈도우 범위, 리포트 저장 경로가 stderr에 출력된다.

```bash
./.venv/bin/python management/tools/translation_quality_report.py \
  --target docs/parts/part-01/chapter-01/section-01.md \
  --locale en \
  --pull-model \
  --verbose
```
