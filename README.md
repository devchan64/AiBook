# AiBook

AiBook은 AI를 다시 배우기 위한 정적 웹 책 프로젝트입니다. AI를 처음 공부하는 사람, 예전에 AI 개론을 배웠지만 개념이 흐릿해진 사람, AI 도구는 써 봤지만 내부 원리를 더 알고 싶은 비전공자가 같은 흐름으로 다시 학습할 수 있게 구성합니다.

## 배포 페이지

[https://devchan64.github.io/AiBook/](https://devchan64.github.io/AiBook/)

## 주요 문서

- 독자용 소개: [`docs/index.md`](docs/index.md)
- 독자용 목차: [`docs/table-of-contents.md`](docs/table-of-contents.md)
- 개념사전: [`docs/reference/concept-glossary.md`](docs/reference/concept-glossary.md)
- 전역 작업 기준: [`AGENTS.md`](AGENTS.md)
- 관리 문서 인덱스: [`management/README.md`](management/README.md)

이 저장소의 목표는 자료를 많이 모으는 것이 아니라, `AI 개론과 지형도 -> 기초 복구 -> 데이터 모델링 -> 머신러닝 -> 딥러닝 -> LLM과 생성형 AI -> 프로젝트`로 이어지는 재학습 경로를 만드는 것입니다. 설명은 초심자가 따라올 수 있어야 하지만, 쉬운 비유만으로 끝내지 않고 표준 용어와 검증 가능한 근거에 연결합니다.

## 책의 구성

- **Part 1. AI 개론과 지형도**: AI의 범위, 역사, 규칙과 학습의 차이, LLM 사용 경험의 기본 요소를 잡습니다.
- **Part 2. 기초 복구**: 수학, Python, 데이터 도구, 실행 환경을 AI 모델 계산을 읽는 데 필요한 만큼 복구합니다.
- **Part 3. 데이터 모델링**: 원천데이터를 학습 가능한 입력과 비교 가능한 결과 구조로 정리합니다.
- **Part 4. 머신러닝**: 문제 설정, 데이터 분리, 학습, 평가, 대표 알고리즘을 하나의 공통 구조로 봅니다.
- **Part 5. 딥러닝**: 신경망 계산, 역전파(backpropagation), CNN, RNN, attention, Transformer로 이어지는 구조를 다룹니다.
- **Part 6. LLM과 생성형 AI**: 토큰, 프롬프트, 생성 설정, 임베딩, 검색, RAG, 에이전트, 평가를 연결합니다.
- **Part 7. 프로젝트**: 앞에서 배운 개념을 작은 산출물로 만들고, 실행 로그와 평가 기준으로 검증합니다.

## 대상 독자와 작성 관점

대상 독자는 대학 수준의 수학, 프로그래밍, 시스템 기초를 이미 안다고 가정하지 않습니다. 다만 핵심 용어는 논문, 공식 문서, 해외 강의, API 문서에서 다시 찾을 수 있도록 가능한 한 한국어(English) 형식으로 연결합니다.

개인적인 직관은 초안의 출발점이 될 수 있지만, 본문에서는 다음 층위를 구분합니다.

- `표준적 설명`: 교과서, 논문, 공식 문서, 신뢰 가능한 자료와 연결되는 설명
- `작업 가설`: 이해를 돕는 개인적 비유나 임시 설명
- `검증 필요`: 표준 설명과 충돌하거나 근거가 아직 충분하지 않은 부분

AI 도구는 커리큘럼 구성, 자료 조사, 초안 작성, 비교 정리, 다이어그램 작성, 문서 구조화를 돕습니다. Codex는 이 과정에서 초안 생성과 검토 보조를 수행하는 LLM 에이전트 관점의 도구로 다룹니다. 생성형 AI의 출력은 항상 검토 대상입니다.

## 저장소 구조

- `docs/`: 독자에게 배포할 책 본문과 공개 자산
- `docs/index.md`, `docs/table-of-contents.md`: 한국어 소개와 목차
- `docs/index.en.md`, `docs/table-of-contents.en.md`: 영어 소개와 목차
- `docs/index.zh.md`, `docs/table-of-contents.zh.md`: 중국어 간체 소개와 목차
- `docs/parts/part-XX/`: Part별 본문
- `docs/reference/concept-glossary.md`: 한국어 개념사전
- `docs/reference/concept-glossary.en.md`: 영어 개념사전
- `docs/assets/`: 본문에서 쓰는 이미지, Mermaid, 차트 자산의 공용 루트
- `docs/stylesheets/`, `docs/javascripts/`: 사이트 보조 스타일과 스크립트
- `management/`: 집필 기준, 조사 자료, 근거 분석, 릴리즈노트
- `management/guidelines/`: 원고 작성, 메타데이터, 차트, 예제, 번역, 개념사전 가이드
- `management/glossary-indexes/`: 개념사전의 한글, 영문, 중국어 보조 인덱스
- `management/release-notes/sections/`: Section 단위 개정 이력
- `management/tools/`: 집필, 근거 수집, 번역 검수를 돕는 관리 스크립트
- `.tmp/`: 외부 자료 확인용 임시 작업공간. 커밋하지 않습니다.
- `site/`, `site-dev/`: MkDocs 빌드 산출물. 명시적 지시 없이 커밋하지 않습니다.

배포 목차는 `mkdocs.yml`의 `nav`에서 관리합니다. 관리 문서와 조사 메모는 배포 목차에 연결하지 않습니다.

## 관리 도구

관리 도구의 자세한 사용법은 [`management/tools/README.md`](management/tools/README.md)를 봅니다.

- 근거 원문 수집: [`management/tools/evidence_collector.py`](management/tools/evidence_collector.py)
  - 원고 Markdown 페이지에 연결된 외부 URL을 찾아 `.tmp/evidence/` 아래에 다운로드합니다.
  - 실제 다운로드 전에는 `--dry-run`으로 수집 대상만 확인할 수 있습니다.
- 번역 게이트웨이 리포트: [`management/tools/translation_quality_report.py`](management/tools/translation_quality_report.py)
  - 한국어 원문과 영어·중국어 번역본을 대조해 추가 번역이나 집중 검수가 필요한 파일을 초기에 걸러냅니다.
  - Ollama 기반 검수는 모델이 필요하며, 모델이 없으면 `--pull-model`로 내려받을 수 있습니다.

## 작업 기준

작업 전에는 [`AGENTS.md`](AGENTS.md)를 먼저 확인합니다. 어떤 가이드를 열어야 할지 헷갈리면 [`management/guidelines/rules-and-guidelines-summary.md`](management/guidelines/rules-and-guidelines-summary.md)를 봅니다.

- 원고 작성과 큰 구조 수정: [`management/guidelines/manuscript-writing-workflow.md`](management/guidelines/manuscript-writing-workflow.md)
- Section ID, Version, 릴리즈노트 연결: [`management/guidelines/section-metadata-guidelines.md`](management/guidelines/section-metadata-guidelines.md)
- 릴리즈노트 파일 형식: [`management/release-notes/sections/README.md`](management/release-notes/sections/README.md)
- 개념사전: [`management/guidelines/concept-glossary-guidelines.md`](management/guidelines/concept-glossary-guidelines.md)
- Python 예제: [`management/guidelines/python-example-guidelines.md`](management/guidelines/python-example-guidelines.md)
- 차트와 다이어그램: [`management/guidelines/chart-guidelines.md`](management/guidelines/chart-guidelines.md)
- 영어 번역: [`management/guidelines/english-translation-guidelines.md`](management/guidelines/english-translation-guidelines.md)
- 중국어 간체 번역: [`management/guidelines/chinese-translation-guidelines.md`](management/guidelines/chinese-translation-guidelines.md)

본문 Section을 수정했다면 제목 아래 `Section ID`와 `Version`을 확인하고, 대응 릴리즈노트를 같은 작업 안에서 갱신합니다. `docs/table-of-contents.md`와 `docs/reference/concept-glossary.md`는 전용 규칙에 따라 별도 Section 릴리즈노트를 운영하지 않습니다.

## 브랜치와 배포

- `dev`: 일반 작성과 편집 브랜치
- `main`: 배포 브랜치

일반적인 문서 작성, 초안 추가, 구조 변경, 커밋, 푸시는 `dev`에서 진행합니다. `main`에 push하면 GitHub Actions가 GitHub Pages 배포를 실행하므로, `main` 반영은 배포 작업으로 취급합니다.

## 로컬 실행

처음 환경을 준비할 때는 다음 순서로 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./.venv/bin/python -m mkdocs serve
```

기본 로컬 주소는 `http://127.0.0.1:8000`입니다.

개발 중 반복 확인할 때는 `mkdocs.dev.yml`을 사용하면 출력 디렉터리를 `site-dev/`로 분리하고 일부 플러그인 부담을 줄일 수 있습니다.

```bash
BUILD_ONLY_LOCALE=ko \
MKDOCS_ENABLE_GIT_REVISION=false \
MKDOCS_ENABLE_MINIFY=false \
./.venv/bin/python -m mkdocs serve -f mkdocs.dev.yml
```

이 경우 기본 로컬 주소는 `http://127.0.0.1:9000`입니다. `BUILD_ONLY_LOCALE`에는 `ko`, `en`, `zh`를 지정할 수 있고, 지정하지 않으면 전체 locale을 빌드합니다. 검색 인덱스까지 끄고 싶다면 `MKDOCS_ENABLE_SEARCH=false`를 추가할 수 있습니다.

## 빌드 검증

기본 빌드 확인 명령은 다음과 같습니다.

```bash
./.venv/bin/python -m mkdocs build
```

MkDocs 관련 명령은 시스템 `python3` 대신 `./.venv/bin/python -m mkdocs ...` 형식을 우선 사용합니다. Mermaid 원본을 `docs/assets/.../*.mmd`에서 수정할 때는 `--dirty` 없이 일반 `serve` 또는 `build`로 확인하는 편이 안전합니다.

## GitHub Pages 배포

배포 페이지는 [https://devchan64.github.io/AiBook/](https://devchan64.github.io/AiBook/)입니다.

1. GitHub 저장소의 `Settings > Pages`에서 `Build and deployment`의 `Source`를 `GitHub Actions`로 설정합니다.
2. `main` 브랜치에 push하면 `.github/workflows/deploy.yml`이 정적 사이트를 빌드하고 GitHub Pages에 배포합니다.
