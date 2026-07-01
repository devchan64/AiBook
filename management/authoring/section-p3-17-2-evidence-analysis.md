# P3-17.2 군집 결과 해석 주의점 근거 메모

## Section 역할

- Part 3 Module 6 Chapter 17의 두 번째 절입니다.
- 17.1에서 클러스터링의 기본 직관을 설명한 뒤, 군집 결과를 과신하지 않는 해석 원칙을 정리합니다.
- 초심자에게 군집을 `정답`이 아니라 `가설 제안`으로 읽는 태도를 주는 절입니다.

## 핵심 주장

1. 군집 결과는 정답 클래스와 다르며, 자동으로 의미가 확정되지 않는다.
2. cluster ID는 보통 순위나 등급을 뜻하지 않는다.
3. 특징 선택, 스케일, 거리 정의, 파라미터에 따라 군집 결과는 달라질 수 있다.
4. 클러스터링은 인과관계를 자동으로 설명하지 않는다.
5. 군집 결과를 정책으로 바로 연결하기보다, 후속 검토와 도메인 확인의 출발점으로 쓰는 편이 안전하다.

## 근거 출처

### 1) scikit-learn User Guide - Clustering

- 문서: `2.3. Clustering`
- URL: https://scikit-learn.org/stable/modules/clustering.html
- 확인 날짜: 2026-06-27

### 2) scikit-learn User Guide - Common pitfalls and recommended practices

- 문서: `11. Common pitfalls and recommended practices`
- URL: https://scikit-learn.org/stable/common_pitfalls.html
- 확인 날짜: 2026-06-27

## 제외한 내용

- 군집 품질 지표의 계산법
- 안정성(stability) 검증의 세부 절차
- semi-supervised clustering
- causal discovery와 clustering의 관계

이 내용은 심화 학습이나 후속 프로젝트 파트에서 다시 다룰 수 있습니다.
