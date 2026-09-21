# SCAIL-v1 실험 결과 요약 — 폐기

상태: 사용자 지시로 2026-09-19 폐기. 개별 프레임 품질 부족으로 제작용 결과에 채택하지 않았다.

- SCAIL-Preview Q4_K_M, 512×512, 33프레임·20fps, seed 23123134, CFG 5, 40 steps, shift 3.
- CFG의 positive·negative 양쪽에 같은 참조 latent를 전달한 수정에서 안개 같은 흐림이 크게 개선됐고 사용자가 이를 확인했다. 기존 ComfyUI 경로는 negative 참조를 0으로 채웠다.
- 걷기 동작은 유지됐으나 얼굴·머리 형태 변화와 손발 디테일 부족이 남았다. 사용자는 프레임 단위 품질이 부족하다고 판정했다.
- steps·shift 조절, BF16/FP32 디코딩, Q6 변경으로는 흐림을 충분히 해결하지 못했다. 단일 클립 관측으로 일반화하지 않는다.
- 최종 실행 시간 약 39.4분, peak allocated VRAM 약 3.22 GiB. 전체 장치 메모리 사용량과는 다르다.
- 영상·이미지·상세 로그·실행 스크립트는 삭제했다. 다음 SCAIL-2 실험에서 재사용하는 참조·포즈·입력 준비 기록은 `../2026-09-20-scail2-multiref-v1/`로 이관했다. 공용 모델 캐시는 유지한다.

근거 코드: [공식 SCAIL, revision 518074f](https://github.com/zai-org/SCAIL/blob/518074fbe8838eeda05b7a72462eac2c089feec2/wan/scail.py). 시각 산출물은 폐기되어 이 요약만으로 재검수할 수 없다.
