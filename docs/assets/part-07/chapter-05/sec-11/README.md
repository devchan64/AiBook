# P7-5.11 학습 자료 폴더

원고: [Mira 얼굴·헤어 LoRA 학습](../../../../parts/part-07/chapter-05/section-11.md)

- `training-images/`: 학습용 보충 PNG 28개만 관리한다. 5.2의 공유 원본 12개는 `../sec-02/`에서 참조한다.
- `validation/images/`: 학습에서 제외한 검증 PNG 4개.
- 이 폴더의 JSON: 데이터 목록·분할·생성 조건·학습 설정·비교 계획.
- `results/`: 보충 이미지의 원본 생성 기록.
- `checkpoint-matrix-evaluation/`, `memorization-evaluation/`, `identity-evaluation/`, `neutral-ablation-evaluation/`: 평가 입력·결과·검수 및 비교 근거.

[현재 학습·검증 목록](p7-5-11-mira-lora-reviewed-v2.json)

[통합 A/B 비교 계획](p7-5-11-ab-comparison-plan.json)

원고·코드·목록에서 참조하는 5.11 전용 자산과 실행 의존 파일을 이 폴더에서 관리한다. 참조되지 않는 실험 자료와 불필요한 호환 링크는 폐기했다. 학습 패키지와 원본 기록에서 사용하는 이전 경로의 호환 링크는 유지한다. 원본 결과 JSON·JSONL의 실행 당시 경로와 해시는 보존한다. 새 패키지는 현재 목록으로 준비한다.

실행 캐시·체크포인트는 저장소 루트 `.tmp/p7-5-11/`, 다운로드 모델은 `.tmp/download/`에서 관리한다.
