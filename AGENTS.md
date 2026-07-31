# AGENTS.md

이 문서는 AI 에이전트가 이 저장소에서 가장 먼저 확인하는 초기 라우팅 문서다. 세부 절차와 반복 체크 항목은 `management/` 아래의 관리 문서와 가이드라인 문서로 분리한다.

## 저장소 목적

- 이 저장소는 AI를 다시 학습하기 위한 내용을 커리큘럼 순서로 정리해 정적 웹 책으로 만드는 프로젝트다.
- 대상 독자는 AI를 처음 공부하는 사람, 오래전에 AI 개론이나 기초 과목을 배웠지만 개념을 많이 잊은 사람, AI 도구와 서비스 경험은 있지만 더 깊이 이해하고 싶은 비전공자를 포함한다.
- 초심자는 기본적으로 `대학 학사 교육을 받지 않았을 수 있는 독자`를 기준으로 판단한다.
- 책의 목적은 단순 자료 수집이 아니라, 기초 복구부터 머신러닝, 딥러닝, LLM/생성형 AI, 프로젝트까지 이어지는 재학습 경로를 만드는 것이다.
- 이 책은 AI 도구를 통해 만들어지지만, AI가 생성한 내용은 항상 검토 대상이다.
- Codex는 이 책의 제작 과정과 LLM 에이전트 관점을 설명하는 핵심 도구이므로, 역할과 한계를 책 안에서 명시적으로 다룬다.

## 기본 관점

- 사용자의 개인적 이해, 기억, 비유는 `작업 가설`로 보존한다.
- 표준 교과서, 논문, 공식 문서, 신뢰 가능한 자료와 연결되는 설명은 `표준적 설명`으로 정리한다.
- 표준 설명과 충돌하거나 근거가 부족한 내용은 `검증 필요`로 분리한다.
- 사용자의 직관은 `개인적 표현 -> 일반화된 질문 -> 표준 개념 -> 초심자가 따라갈 설명 흐름 -> 검증 필요 지점`의 순서로 일반화한다.
- 개인적 학습 경험은 머리말, 장 도입부, 회고성 설명에 사용할 수 있다. 개념 설명 본문에서는 검증 가능한 용어와 근거로 연결한다.

## 먼저 확인할 문서

- 관리 문서 전체 구조: `management/README.md`
  - `management/` 아래 문서가 어떤 역할을 맡는지 먼저 찾을 때 본다.
- 작업별 가이드라인 인덱스: `management/guidelines/README.md`
  - 현재 작업에 어떤 세부 가이드를 적용해야 하는지 고를 때 본다.
- 저장소 구조, 브랜치, 배포, 검증 기준: `management/guidelines/repository-management-guidelines.md`
  - 파일 위치, `dev`/`main` 구분, 빌드 실행 여부, 커밋 제외 대상을 판단할 때 본다.
- 원고 작성 세부 절차: `management/guidelines/manuscript-writing-workflow.md`
  - Part/Section 초안 작성, 큰 문단 재구성, 초심자 보강, 사례·연습 배치를 판단할 때 본다.
- Section 메타데이터 관리: `management/guidelines/section-metadata-guidelines.md`
  - `Section ID`, 제목 앞 인덱스, `Version`, 릴리즈노트 연결을 확인할 때 본다.
- 릴리즈노트 파일 관리: `management/release-notes/sections/README.md`
  - Section 릴리즈노트 파일 위치, 파일명, 항목 형식을 확인할 때 본다.
- 출처, 근거, 저작권, 예측성 내용 기준: `management/guidelines/source-copyright-guidelines.md`
  - 외부 자료를 반영하거나 인용, 재서술, 전망 문장을 작성할 때 본다.
- 개념사전 작성 기준: `management/guidelines/concept-glossary-guidelines.md`
  - 개념사전 항목 추가·수정, 표제어 통일, 중심 Section과 등장 Section을 정리할 때 본다.
- Python 예제 작성 기준: `management/guidelines/python-example-guidelines.md`
  - Python 예제를 추가·수정하거나 코드 블록 유지 여부를 판단할 때 본다.
- 차트·그래프·도식 기준: `management/guidelines/chart-guidelines.md`
  - Mermaid, SVG, 그래프, 시각화 자산을 추가·수정하거나 형식을 고를 때 본다.
- 영어 번역 기준: `management/guidelines/english-translation-guidelines.md`
  - 영어판 Section 작성, 용어 대응, 다국어 링크, 공통 릴리즈노트 반영을 확인할 때 본다.
- 중국어 간체 번역 기준: `management/guidelines/chinese-translation-guidelines.md`
  - 중국어 간체판 Section 작성, 용어 대응, 다국어 링크, 공통 릴리즈노트 반영을 확인할 때 본다.
- Section별 중심 학습 산출물 추적: `management/guidelines/section-learning-focus-guidelines.md`
  - Section 중심 질문, 학습 산출물, Part 체크포인트 항목의 대응을 맞출 때 본다.

## 작업 전 원칙

- 작업 전에는 현재 브랜치와 변경 범위를 확인한다.
- 관련 없는 기존 변경을 되돌리거나 함께 커밋하지 않는다.
- 원고 수정, 예제 추가, 도식 추가, 번역, 목차 변경처럼 전용 가이드가 있는 작업은 해당 가이드를 먼저 확인한다.
- Section 본문 작업은 `Section ID`를 기준으로 추적한다.
- Section 본문을 수정했다면 본문 메타데이터와 릴리즈노트 연결을 함께 확인한다. 다만 개념사전은 전용 가이드에 따라 릴리즈노트 연결 대상에서 제외한다.
- 작업 완료 전에는 변경 파일, 본문 구조, 링크, 메타데이터, 릴리즈노트 정합성을 확인한다.

## 반드시 지킬 경계

- `dev`는 일반 작성과 편집 브랜치이고, `main`은 배포 브랜치다.
- `main`에 push되면 GitHub Actions Pages 배포가 실행된다.
- 사용자가 `main에 반영`, `배포`, `배포 페이지 갱신`, `main으로 푸시`처럼 명시적으로 지시한 경우에만 `main`에 push한다.
- 사용자 요청이나 명시된 검증 단계 없이 임의의 빌드 명령을 실행하지 않는다.
- `.tmp/`는 외부 자료 원문 확인을 위한 임시 작업공간이며 커밋하지 않는다.
- `site/`는 빌드 산출물이며 명시적 지시 없이 커밋하지 않는다.
- 외부 자료를 참조하거나 인용하면 반드시 출처를 남긴다.
- 출처가 없는 AI 생성 설명은 검증된 사실처럼 단정하지 않는다.
- 판단이 애매한 저작권 사안은 `검증 필요`로 표시하고 원문 사용을 보류한다.
