# 외부 입력 45장 · 1600스텝 LoRA 시각 검수표

366쌍 중 학습 347쌍으로 학습한 새 LoRA의 결과다. 기존 공개 어댑터와 구분한다. 입력 45장은 학습 입력과 해시가 겹치지 않으며, 목표 얼굴 이미지는 추론에 전달하지 않았다.

기반 모델: Qwen-Image-Edit-2511. LoRA 강도 1.0, 시드 62294, 추론 20스텝, CFG 4.0, 출력·참조 VAE 512×512, 크롭 없음.

체크포인트 SHA-256: `9cddfaec307af146ce5311669c2e0ab42fdf68abe836364fa329e32861e9e37e`

45장 생성과 파일 무결성 검증은 완료했다. **시각적 품질 판정은 미확정**이며 아래 표를 보며 검수한다. 관리번호는 기존 P712-CAM 번호를 유지한다.

얼굴·헤어·화풍이 Mira에 가까운지, 특히 ±45°·±90°에서 입력 얼굴의 앞뒤 길이를 그대로 따르는지 확인한다. 동시에 방향·표정·자세·의상·배경·구도 보존을 확인한다. 미적용 결과는 이번 표에 없으므로 개선 폭을 정량적으로 단정하지 않는다.

| 관리번호 · 입력 조건 | 입력 | LoRA 적용 · 1600스텝 |
| --- | --- | --- |
| P712-CAM-001 · man / low / -90° | ![P712-CAM-001 입력](../sec-12/codex-camera-inputs-v1/man-low-minus-90-512.png) | ![P712-CAM-001 적용](codex-camera-lora-366-v1/man-low-minus-90-lora.png) |
| P712-CAM-002 · man / low / -45° | ![P712-CAM-002 입력](../sec-12/codex-camera-inputs-v1/man-low-minus-45-512.png) | ![P712-CAM-002 적용](codex-camera-lora-366-v1/man-low-minus-45-lora.png) |
| P712-CAM-003 · man / low / 0° | ![P712-CAM-003 입력](../sec-12/codex-camera-inputs-v1/man-low-zero-512.png) | ![P712-CAM-003 적용](codex-camera-lora-366-v1/man-low-zero-lora.png) |
| P712-CAM-004 · man / low / 45° | ![P712-CAM-004 입력](../sec-12/codex-camera-inputs-v1/man-low-plus-45-512.png) | ![P712-CAM-004 적용](codex-camera-lora-366-v1/man-low-plus-45-lora.png) |
| P712-CAM-005 · man / low / 90° | ![P712-CAM-005 입력](../sec-12/codex-camera-inputs-v1/man-low-plus-90-512.png) | ![P712-CAM-005 적용](codex-camera-lora-366-v1/man-low-plus-90-lora.png) |
| P712-CAM-006 · man / level / -90° | ![P712-CAM-006 입력](../sec-12/codex-camera-inputs-v1/man-level-minus-90-512.png) | ![P712-CAM-006 적용](codex-camera-lora-366-v1/man-level-minus-90-lora.png) |
| P712-CAM-007 · man / level / -45° | ![P712-CAM-007 입력](../sec-12/codex-camera-inputs-v1/man-level-minus-45-512.png) | ![P712-CAM-007 적용](codex-camera-lora-366-v1/man-level-minus-45-lora.png) |
| P712-CAM-008 · man / level / 0° | ![P712-CAM-008 입력](../sec-12/codex-camera-inputs-v1/man-level-zero-512.png) | ![P712-CAM-008 적용](codex-camera-lora-366-v1/man-level-zero-lora.png) |
| P712-CAM-009 · man / level / 45° | ![P712-CAM-009 입력](../sec-12/codex-camera-inputs-v1/man-level-plus-45-512.png) | ![P712-CAM-009 적용](codex-camera-lora-366-v1/man-level-plus-45-lora.png) |
| P712-CAM-010 · man / level / 90° | ![P712-CAM-010 입력](../sec-12/codex-camera-inputs-v1/man-level-plus-90-512.png) | ![P712-CAM-010 적용](codex-camera-lora-366-v1/man-level-plus-90-lora.png) |
| P712-CAM-011 · man / elevated / -90° | ![P712-CAM-011 입력](../sec-12/codex-camera-inputs-v1/man-elevated-minus-90-512.png) | ![P712-CAM-011 적용](codex-camera-lora-366-v1/man-elevated-minus-90-lora.png) |
| P712-CAM-012 · man / elevated / -45° | ![P712-CAM-012 입력](../sec-12/codex-camera-inputs-v1/man-elevated-minus-45-512.png) | ![P712-CAM-012 적용](codex-camera-lora-366-v1/man-elevated-minus-45-lora.png) |
| P712-CAM-013 · man / elevated / 0° | ![P712-CAM-013 입력](../sec-12/codex-camera-inputs-v1/man-elevated-zero-512.png) | ![P712-CAM-013 적용](codex-camera-lora-366-v1/man-elevated-zero-lora.png) |
| P712-CAM-014 · man / elevated / 45° | ![P712-CAM-014 입력](../sec-12/codex-camera-inputs-v1/man-elevated-plus-45-512.png) | ![P712-CAM-014 적용](codex-camera-lora-366-v1/man-elevated-plus-45-lora.png) |
| P712-CAM-015 · man / elevated / 90° | ![P712-CAM-015 입력](../sec-12/codex-camera-inputs-v1/man-elevated-plus-90-512.png) | ![P712-CAM-015 적용](codex-camera-lora-366-v1/man-elevated-plus-90-lora.png) |
| P712-CAM-016 · woman / low / -90° | ![P712-CAM-016 입력](../sec-12/codex-camera-inputs-v1/woman-low-minus-90-512.png) | ![P712-CAM-016 적용](codex-camera-lora-366-v1/woman-low-minus-90-lora.png) |
| P712-CAM-017 · woman / low / -45° | ![P712-CAM-017 입력](../sec-12/codex-camera-inputs-v1/woman-low-minus-45-512.png) | ![P712-CAM-017 적용](codex-camera-lora-366-v1/woman-low-minus-45-lora.png) |
| P712-CAM-018 · woman / low / 0° | ![P712-CAM-018 입력](../sec-12/codex-camera-inputs-v1/woman-low-zero-512.png) | ![P712-CAM-018 적용](codex-camera-lora-366-v1/woman-low-zero-lora.png) |
| P712-CAM-019 · woman / low / 45° | ![P712-CAM-019 입력](../sec-12/codex-camera-inputs-v1/woman-low-plus-45-512.png) | ![P712-CAM-019 적용](codex-camera-lora-366-v1/woman-low-plus-45-lora.png) |
| P712-CAM-020 · woman / low / 90° | ![P712-CAM-020 입력](../sec-12/codex-camera-inputs-v1/woman-low-plus-90-512.png) | ![P712-CAM-020 적용](codex-camera-lora-366-v1/woman-low-plus-90-lora.png) |
| P712-CAM-021 · woman / level / -90° | ![P712-CAM-021 입력](../sec-12/codex-camera-inputs-v1/woman-level-minus-90-512.png) | ![P712-CAM-021 적용](codex-camera-lora-366-v1/woman-level-minus-90-lora.png) |
| P712-CAM-022 · woman / level / -45° | ![P712-CAM-022 입력](../sec-12/codex-camera-inputs-v1/woman-level-minus-45-512.png) | ![P712-CAM-022 적용](codex-camera-lora-366-v1/woman-level-minus-45-lora.png) |
| P712-CAM-023 · woman / level / 0° | ![P712-CAM-023 입력](../sec-12/codex-camera-inputs-v1/woman-level-zero-512.png) | ![P712-CAM-023 적용](codex-camera-lora-366-v1/woman-level-zero-lora.png) |
| P712-CAM-024 · woman / level / 45° | ![P712-CAM-024 입력](../sec-12/codex-camera-inputs-v1/woman-level-plus-45-512.png) | ![P712-CAM-024 적용](codex-camera-lora-366-v1/woman-level-plus-45-lora.png) |
| P712-CAM-025 · woman / level / 90° | ![P712-CAM-025 입력](../sec-12/codex-camera-inputs-v1/woman-level-plus-90-512.png) | ![P712-CAM-025 적용](codex-camera-lora-366-v1/woman-level-plus-90-lora.png) |
| P712-CAM-026 · woman / elevated / -90° | ![P712-CAM-026 입력](../sec-12/codex-camera-inputs-v1/woman-elevated-minus-90-512.png) | ![P712-CAM-026 적용](codex-camera-lora-366-v1/woman-elevated-minus-90-lora.png) |
| P712-CAM-027 · woman / elevated / -45° | ![P712-CAM-027 입력](../sec-12/codex-camera-inputs-v1/woman-elevated-minus-45-512.png) | ![P712-CAM-027 적용](codex-camera-lora-366-v1/woman-elevated-minus-45-lora.png) |
| P712-CAM-028 · woman / elevated / 0° | ![P712-CAM-028 입력](../sec-12/codex-camera-inputs-v1/woman-elevated-zero-512.png) | ![P712-CAM-028 적용](codex-camera-lora-366-v1/woman-elevated-zero-lora.png) |
| P712-CAM-029 · woman / elevated / 45° | ![P712-CAM-029 입력](../sec-12/codex-camera-inputs-v1/woman-elevated-plus-45-512.png) | ![P712-CAM-029 적용](codex-camera-lora-366-v1/woman-elevated-plus-45-lora.png) |
| P712-CAM-030 · woman / elevated / 90° | ![P712-CAM-030 입력](../sec-12/codex-camera-inputs-v1/woman-elevated-plus-90-512.png) | ![P712-CAM-030 적용](codex-camera-lora-366-v1/woman-elevated-plus-90-lora.png) |
| P712-CAM-031 · toddler / low / -90° | ![P712-CAM-031 입력](../sec-12/codex-camera-inputs-v1/toddler-low-minus-90-512.png) | ![P712-CAM-031 적용](codex-camera-lora-366-v1/toddler-low-minus-90-lora.png) |
| P712-CAM-032 · toddler / low / -45° | ![P712-CAM-032 입력](../sec-12/codex-camera-inputs-v1/toddler-low-minus-45-512.png) | ![P712-CAM-032 적용](codex-camera-lora-366-v1/toddler-low-minus-45-lora.png) |
| P712-CAM-033 · toddler / low / 0° | ![P712-CAM-033 입력](../sec-12/codex-camera-inputs-v1/toddler-low-zero-512.png) | ![P712-CAM-033 적용](codex-camera-lora-366-v1/toddler-low-zero-lora.png) |
| P712-CAM-034 · toddler / low / 45° | ![P712-CAM-034 입력](../sec-12/codex-camera-inputs-v1/toddler-low-plus-45-512.png) | ![P712-CAM-034 적용](codex-camera-lora-366-v1/toddler-low-plus-45-lora.png) |
| P712-CAM-035 · toddler / low / 90° | ![P712-CAM-035 입력](../sec-12/codex-camera-inputs-v1/toddler-low-plus-90-512.png) | ![P712-CAM-035 적용](codex-camera-lora-366-v1/toddler-low-plus-90-lora.png) |
| P712-CAM-036 · toddler / level / -90° | ![P712-CAM-036 입력](../sec-12/codex-camera-inputs-v1/toddler-level-minus-90-512.png) | ![P712-CAM-036 적용](codex-camera-lora-366-v1/toddler-level-minus-90-lora.png) |
| P712-CAM-037 · toddler / level / -45° | ![P712-CAM-037 입력](../sec-12/codex-camera-inputs-v1/toddler-level-minus-45-512.png) | ![P712-CAM-037 적용](codex-camera-lora-366-v1/toddler-level-minus-45-lora.png) |
| P712-CAM-038 · toddler / level / 0° | ![P712-CAM-038 입력](../sec-12/codex-camera-inputs-v1/toddler-level-zero-512.png) | ![P712-CAM-038 적용](codex-camera-lora-366-v1/toddler-level-zero-lora.png) |
| P712-CAM-039 · toddler / level / 45° | ![P712-CAM-039 입력](../sec-12/codex-camera-inputs-v1/toddler-level-plus-45-512.png) | ![P712-CAM-039 적용](codex-camera-lora-366-v1/toddler-level-plus-45-lora.png) |
| P712-CAM-040 · toddler / level / 90° | ![P712-CAM-040 입력](../sec-12/codex-camera-inputs-v1/toddler-level-plus-90-512.png) | ![P712-CAM-040 적용](codex-camera-lora-366-v1/toddler-level-plus-90-lora.png) |
| P712-CAM-041 · toddler / elevated / -90° | ![P712-CAM-041 입력](../sec-12/codex-camera-inputs-v1/toddler-elevated-minus-90-512.png) | ![P712-CAM-041 적용](codex-camera-lora-366-v1/toddler-elevated-minus-90-lora.png) |
| P712-CAM-042 · toddler / elevated / -45° | ![P712-CAM-042 입력](../sec-12/codex-camera-inputs-v1/toddler-elevated-minus-45-512.png) | ![P712-CAM-042 적용](codex-camera-lora-366-v1/toddler-elevated-minus-45-lora.png) |
| P712-CAM-043 · toddler / elevated / 0° | ![P712-CAM-043 입력](../sec-12/codex-camera-inputs-v1/toddler-elevated-zero-512.png) | ![P712-CAM-043 적용](codex-camera-lora-366-v1/toddler-elevated-zero-lora.png) |
| P712-CAM-044 · toddler / elevated / 45° | ![P712-CAM-044 입력](../sec-12/codex-camera-inputs-v1/toddler-elevated-plus-45-512.png) | ![P712-CAM-044 적용](codex-camera-lora-366-v1/toddler-elevated-plus-45-lora.png) |
| P712-CAM-045 · toddler / elevated / 90° | ![P712-CAM-045 입력](../sec-12/codex-camera-inputs-v1/toddler-elevated-plus-90-512.png) | ![P712-CAM-045 적용](codex-camera-lora-366-v1/toddler-elevated-plus-90-lora.png) |
