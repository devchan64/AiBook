# SCAIL-2 DPO 512p 결과 요약 — 폐기

2026-09-20 사용자 지시에 따라 결과 요약만 남기고 영상·프레임·상세 로그를 폐기했다.

- SCAIL-2 Q4_K_M + 공식 bias-aware DPO strength 1.0. 512×512, 33프레임·20fps, seed 23123134, CFG 5, 40 steps, shift 3.
- 원본 DPO 800개 tensor를 변환해 모델의 400개 대상에 적용했다. 기본 실험과 입력·마스크·실행 revision 일치를 확인했다.
- 걷기와 큰 의상 특징은 유지됐으나 손·신발 디테일 부족, 얼굴·머리·셔츠 실루엣 변화, 배경 질감이 남았다. 이 조건에서 DPO만으로 개별 프레임 품질이 해결됐다고 판정하지 않았다.
- 약 39.0분, PyTorch peak allocated 2.92 GiB / reserved 3.58 GiB. 33개 PNG 해시와 영상 프레임 수·해상도·fps 확인 완료.
- 출력 저장 후 무시된 ComfyUI ON_DETACH 소멸자 오류가 있었다. 종료 코드 0과 산출물 무결성을 확인했다.
- 다음 704p 실험에 필요한 입력·코드·모델 기록은 `../2026-09-20-scail2-multiref-v1/`로 이관했다. 공용 모델 캐시는 유지한다. 삭제한 영상의 재검수는 요약만으로 불가능하다.

출처: [SCAIL-2 공식 DPO](https://github.com/zai-org/SCAIL-2/tree/wan-scail2), [공식 가중치](https://huggingface.co/zai-org/SCAIL-2/blob/main/model/bias-aware-dpo-lora.pt).
