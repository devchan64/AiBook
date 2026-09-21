# SCAIL-2 기본 실험 결과 요약 — 폐기

2026-09-20 사용자 지시에 따라 결과 요약만 남기고 영상·프레임·상세 실행 기록을 폐기했다.

- SCAIL-2 Q4_K_M, 512×512, 33프레임·20fps, seed 23123134, CFG 5, 40 steps, shift 3. DPO 미적용.
- 화면을 가로지르는 걷기와 흰 셔츠·짙은 청록색 바지의 큰 특징은 관측됐다.
- 손·신발 세부 경계가 부드럽고 얼굴·머리·셔츠 형태가 변했다. 평평한 참조 배경에 없던 얼룩 같은 질감도 생겼다. 개별 프레임 제작 품질을 충족한 결과로 채택하지 않았다.
- 실행 약 38.3분. PyTorch peak allocated 2.92 GiB, reserved 3.70 GiB. 33개 PNG 해시와 512×512·20fps 영상 프레임 수 확인 완료.
- 파일 저장 후 ComfyUI 소멸자에서 무시된 ON_DETACH 오류가 발생했지만 종료 코드 0과 산출물 무결성을 확인했다.
- 한 시드·512p·양자화 기본 모델의 관측이며 704p나 DPO 효과를 평가하지 않는다.
- 재사용 입력과 코드는 `../2026-09-20-scail2-multiref-v1/`로 이관했다. 공용 모델 캐시는 유지한다. 삭제한 영상의 재검수는 이 요약만으로 불가능하다.

출처: [SCAIL-2](https://github.com/zai-org/SCAIL-2/tree/wan-scail2), [GGUF 변환](https://huggingface.co/vantagewithai/SCAIL-2-GGUF-ComfyUI).
