# Part 6 오픈 체크리스트

작성일: 2026-07-21

이 문서는 Part 6 개편 후 남은 원고 품질 점검 항목을 관리한다. 기준 문서는 `management/authoring/part-06-restructure-proposal.md`이다.

## 적용 기준

- Part 6은 토큰이 아니라 생성형 AI 산출물에서 시작한다.
- LLM은 생성형 AI 전체가 아니라 대표 사례로 둔다.
- 각 Section은 비교, 구분, 판정, 기록 읽기 중 하나의 학습 산출물을 남겨야 한다.
- Chapter와 Section 분량은 균등하게 맞추지 않는다. 중요도, 학습 병목, 후속 회수 빈도, 흡수구간 필요성으로 판단한다.
- strict build는 배포 전 또는 큰 구조 패치 종료 후 한 번에 확인한다.

## 구조 적용 체크

- [x] 기존 Part 6 원고 아카이브 생성
- [x] 기준 목차 문서 생성
- [x] 새 Chapter 1 추가
- [x] 토큰 장을 P6-2.1~P6-2.5로 통합 재구성
- [x] 기존 Section을 새 번호 체계로 재정렬
- [x] release notes를 새 Section ID 기준으로 초기 정리
- [x] 각 Module 첫 Section의 낯섦 완충 문단 정밀 검토
- [x] Python 예제, CSV, 그래프, Mermaid가 새 Section 중심 감각을 지지하는지 재검토
- [x] 내부 링크와 개념사전 링크 정밀 점검
- [x] 다국어 index/summary/nav 동기화 검토
- [ ] 배포 전 strict build 확인

## Module별 후속 검토

| Module | 후속 검토 질문 |
| --- | --- |
| Module 1 | 생성형 AI 산출물, LLM 대표 경로, 후보 선택 반복이 초심자에게 충분히 분리되어 보이는가? |
| Module 2 | 토큰 장 통합 후 정의, token ID, 토큰화 영향, 활용, 보충학습의 흐름이 자연스러운가? |
| Module 3 | Transformer/GPT/next-token 설명이 구조 이름 나열이 아니라 다음 후보 생성 감각으로 읽히는가? |
| Module 4 | 학습과 조정이 방법 이름 나열이 아니라 무엇을 배우고 맞추는가로 읽히는가? |
| Module 5 | 프롬프트 한계에서 RAG와 벡터 DB로 넘어가는 이유가 충분히 열리는가? |
| Module 6 | 도구 사용, 함수 호출, 에이전트, MCP, 하네스가 제품 기능 목록처럼 보이지 않는가? |
| Module 7 | 좋은 답변과 서비스 가능한 답변의 차이가 평가, 운영, 실패 대응으로 이어지는가? |
| Module 8 | 발전사와 BERT가 본류 뒤의 배경 지도 역할을 하는가? |
