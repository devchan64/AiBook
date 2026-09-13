# P7-5.11 학습 자료 폴더

원고: [Mira 얼굴·헤어 LoRA 학습](../../../../parts/part-07/chapter-05/section-11.md)

- `datasets/images/`: 채택한 보충 이미지 32개(학습 28개, 평가 4개).
- `datasets/`: 분할·캡션·파일 해시와 생성 목록·학습 설정.
- `datasets/results/`: 각 이미지의 원본 생성 기록 JSON.

[현재 학습·평가 데이터셋](datasets/p7-5-11-mira-lora-reviewed-v2.json)

[재생성 조건 목록](datasets/p7-5-11-mira-supplement-spec-v2.json)

[실행된 8GB 학습 설정](datasets/p7-5-11-mira-lora-config-v2-8gb.json)

5.2 공유 원본 12개를 추가로 참조하여 학습 타깃은 총 40개다. `datasets/images/`를 통째로 학습 입력으로 사용하면 평가 이미지가 섞이므로 반드시 현재 데이터셋의 `split`을 따른다. 구버전 목록은 판단 이력이며 현재 분할이 아니다.

실험 출력·캐시·학습 체크포인트는 저장소 루트의 `.tmp/p7-5-11/`, 모델 다운로드는 `.tmp/download/`에서 관리한다. 완료된 실행 패키지의 경로는 실행 당시의 기록으로 보존한다. 이동 후 다시 학습하려면 갱신된 데이터셋으로 새 패키지를 준비한다.
