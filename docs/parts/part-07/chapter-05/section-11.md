# P7-5.11 화풍·연속성 보정: 국소 편집과 참조 역할을 분리해 고치기

> Section ID: `P7-5.11`
> Version: `v2026.09.05`

같은 캐릭터의 컷을 국소 편집으로 고칠 수 있을까? 이 절에서는 한 장이 그럴듯한지를 보지 않고, 아래 네 계약을 동시에 확인했다. 실험은 하나의 도구를 고르는 과정이 아니라, 어느 계약이 깨지는지 찾아 다음 입력의 역할을 좁히는 과정이었다.

| 계약 | 확인할 질문 |
| --- | --- |
| structure | 카메라, 인체 동작, 거리와 가림이 장면 의도에 맞는가? |
| identity | 얼굴과 신체 비율이 같은 캐릭터로 읽히는가? |
| outfit | 재킷·상의·바지·신발·가방의 형태와 레이어가 유지됐는가? |
| style | 기준 선화·색·질감의 범위 안에 있는가? |

여기서 **계약**은 생성기에 요구하는 문장이 아니라, 결과를 보고 사람이 판정하는 약속이다. structure는 “카메라와 몸의 큰 배치가 맞는가”, identity는 “같은 사람으로 보이는가”, outfit은 “옷과 소품의 형태·겹침이 맞는가”, style은 “기준 그림 방식과 어울리는가”로 읽는다. 한 항목의 일치가 다른 항목의 이탈을 덮어쓰지 않는다.

!!! abstract "실험 결론"

    국소 편집은 이미 성립한 수평 레이어를 부분 보정할 수 있었지만, 새 카메라가 만드는 3D 가림 관계를 재구성하지는 못했다. 고각도 guide, 얼굴, 완성 착장을 서로 다른 입력 역할로 나눈 Qwen 편집은 고정 guide 범위에서 네 계약을 함께 확인하는 비교가 되었다. 다만 당시 얼굴·착장 기준 파일은 폐기했으므로, 공개한 결과 이미지는 비교 관찰 기록이며 그대로 재실행하는 기준물은 아니다. OpenPose 동작·구도 조건은 P7-5.13으로 분리한다.

OpenPose map을 통한 동작·구도 변경의 관찰과 한계는 [P7-5.13 OpenPose 맵으로 캐릭터 동작과 구도 변경을 시험하기](section-13.md)에서 다룬다. 이 절은 그 실험 뒤에 남은 국소 보정과 reference 편집 경로를 비교한다.

## 국소 보정은 새 카메라의 3D 가림 관계를 만들지 못했다

> **이 보조 실험이 확인한 것:** mask·VTON은 이미 성립한 수평 레이어를 부분 보정할 수 있어도, 고각도에서 새로 보이거나 가려지는 전신 관계를 재구성하지는 못한다.

고각도에서 문제를 국소 영역만 고쳐 해결할 수 있는지도 확인했다. 자동 DiffEdit mask는 머리와 신발까지 퍼져 재킷만 고치지 못했다. FitDiT에는 고각도 원본의 카메라·자세·하체를 고정하고 상반신만 감싼 좁은 mask와 완성 착장을 주었지만, 재킷은 회색 덩어리와 짧은 흰 앞면으로 바뀌고 가방·strap이 사라졌다. CatVTON은 수평 전면에서 재킷 레이어를 부분적으로 전달했지만, 고각도 전신을 다시 구성하는 증거는 아니었다.

| DiffEdit 자동 mask | FitDiT 고각도 상반신 | CatVTON 수평 재킷 |
| --- | --- | --- |
| ![DiffEdit 자동 mask 실패](../../../assets/part-07/chapter-05/p7-5-11-diffedit-first-probe-contact-sheet.png) | ![FitDiT 고각도 상반신 착장 교체](../../../assets/part-07/chapter-05/p7-5-11-fitdit-high-angle-upperbody-complete-outfit-review-sheet.png) | ![CatVTON 전면 재킷 비교](../../../assets/part-07/chapter-05/p7-5-11-catvton-jacket-contact-sheet.png) |
| 편집 범위가 전신으로 확산 | 어깨·재킷·가방의 새 가림 관계가 재현되지 않음 | 수평 재킷 레이어가 일부 유지됨 |

세 결과는 같은 실패가 아니다. DiffEdit은 고칠 영역을 충분히 좁히지 못했고, FitDiT는 좁힌 영역 안에서도 새 카메라가 요구한 어깨·가방의 앞뒤 관계를 만들지 못했다. CatVTON은 수평 전면에서 이미 성립한 레이어를 옮긴 사례다. 따라서 마지막 결과를 고각도 전신의 증거로 확장하지 않고, 국소 보정은 구조 관계가 먼저 확보된 뒤에만 쓰는 후보로 남긴다.

이 결과는 mask를 더 정교하게 그리거나 reference를 더 주는 일이 고각도에서 새로 보이거나 가려지는 팔·몸통·다리·가방의 관계를 대신하지 못한다는 뜻이다. 아래 실행 기록은 각 조건을 남긴다.

[p7-5-11-fitdit-high-angle-upperbody-complete-outfit-result.json — JSON — FitDiT 고각도 상반신 실행 기록 보기](/AiBook/assets/part-07/chapter-05/p7-5-11-fitdit-high-angle-upperbody-complete-outfit-result.json)

이 실행 기록이 가리키는 당시 완성 착장 파일도 현재는 폐기되었다. 따라서 이 시트와 JSON은 고각도 국소 보정의 한계를 읽는 역사적 관찰로만 유지하며, 같은 입력을 다시 실행할 수 있는 재현 묶음으로 취급하지 않는다.

## Qwen의 세 입력 역할은 삭제된 기준물과 분리해 다시 기록한다

이 절의 국소 보정과 P7-5.13의 구조 조건 비교는 한 입력에 카메라·얼굴·완성 착장을 함께 맡기지 말아야 한다는 결론을 주었다. 그러나 Qwen-Image-Edit-2509는 그 보조 조건들을 결합하지 않고, 세 이미지 입력 자체의 역할만 분리했다.

| 입력 | 맡긴 정보 |
| --- | --- |
| image 1 | 지붕, 고각도 카메라, 보행 배치 |
| image 2 | 정면 얼굴 identity |
| image 3 | 재킷·바지·신발·가방을 포함한 완성 착장 |

과거의 2입력은 재킷·가방을 잃었고, 역할을 충분히 분리하지 않은 3입력은 분홍 신발·좁은 바지를 만들었다. 이것이 복장 입력을 별도 역할로 고정한 이유다.

| 2입력: 착장·가방 누락 | 역할 미분리 3입력: 신발·바지 드리프트 |
| --- | --- |
| ![Qwen 2입력 고각도 결과](../../../assets/part-07/chapter-05/p7-5-11-qwen-edit-two-input-outfit-loss.png) | ![Qwen 역할 미분리 3입력 결과](../../../assets/part-07/chapter-05/p7-5-11-qwen-edit-three-input-uncompressed-outfit-drift.png) |
| 재킷·가방·strap 이탈 | 흰 운동화·와이드 바지 이탈 |

당시의 얼굴·완성 착장 기준 파일은 이후 캐릭터 자산 정리에서 폐기했다. 따라서 이 시트는 **입력 역할을 섞었을 때와 분리했을 때의 관찰 기록**으로만 읽고, 같은 픽셀을 재현할 수 있는 기준물로 사용하지 않는다.

[p7_5_11_qwen_edit_high_angle_role_comparison.py — Python — guide·얼굴·착장 입력 경로를 명시적으로 받는 Qwen 역할 분리 비교 템플릿 보기](/AiBook/assets/part-07/chapter-05/p7_5_11_qwen_edit_high_angle_role_comparison.py)

현재 코드는 `--guide`, `--face`, `--outfit`으로 새 입력을 명시한다. `two-input`은 guide와 얼굴만, `role-separated`은 완성 착장을 세 번째 입력으로 받는다. 새 결과는 과거 시트와 픽셀 비교하지 않고, 세 입력의 hash·실행 환경·사람 검수 결과를 새 `result.json`에 남긴다.

이 비교의 핵심은 입력 수 자체가 아니라 입력마다 맡긴 정보다. 2입력에서 구조와 얼굴을 우선하면 완성 착장의 레이어가 빠졌고, 역할이 겹친 3입력에서는 착장 단서끼리 충돌해 신발·바지가 바뀌었다. 그래서 다음 조건에서는 guide가 장면 구조만, 얼굴 reference가 identity만, 완성 착장이 옷·가방만 맡도록 서로의 판정 범위를 좁혔다.

당시 seed `62294/62295` 두 후보는 고정한 고각도 guide에서 보행, 얼굴, 재킷·바지·신발·가방과 재킷 바깥 strap이 함께 남는지 관찰한 시트다. 삭제된 입력 기준물을 새 자산으로 바꾼 뒤에는 같은 seed·step·장치 메모리를 결과 보장으로 읽지 않고, 새 실험의 조건으로 다시 기록한다.

| seed `62294` | seed `62295` |
| --- | --- |
| ![Qwen 역할 분리 고각도 후보 seed 62294](../../../assets/part-07/chapter-05/p7-5-11-qwen-edit-high-angle-seed-62294-reference.png) | ![Qwen 역할 분리 고각도 후보 seed 62295](../../../assets/part-07/chapter-05/p7-5-11-qwen-edit-high-angle-seed-62295-reference.png) |
| 네 항목의 일치 관찰 | 같은 입력 역할에서 교차 seed 비교 |

따라서 고정한 보행 guide 범위에서는 **구조용 guide로 카메라·행동·배경을 정하고, 얼굴과 완성 착장을 역할별 reference로 분리하는 경로**에서 네 항목의 일치를 관찰했다. 다른 pose·guide·후면·강한 가림에는 같은 역할 분리를 유지한 새 후보와 사람 검수가 필요하다. 이 과거 결과는 P7-5.5 스토리보드를 자동으로 교체하거나 LoRA 학습 데이터로 사용하지 않는다.

## 체크리스트

- DiffEdit·FitDiT·CatVTON 비교에서 부분 보정에서 관찰된 변화와 새 고각도 전신 컷의 네 항목 일치를 구분한다.
- Qwen 역할 분리 비교에서는 새 guide·얼굴·착장 입력의 hash와 사람 검수를 result.json에 남긴다. 과거 두 seed에서 같은 특징이 보여도, 다른 pose·후면·강한 가림까지 일반화하지 않는다.

## 출처와 참고 자료

- Stability AI, [SDXL Generative Models](https://github.com/Stability-AI/generative-models){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. SDXL Base 1.0의 기준 모델을 확인했다.
- Qwen Team, [Qwen-Image-Edit-2509](https://github.com/QwenLM/Qwen-Image/blob/main/Qwen-Image-Edit-2509.md){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. 1–3 입력 이미지 편집 범위를 확인했다.
- Nunchaku, [Qwen-Image-Edit-2509 실행 예제](https://github.com/nunchaku-ai/nunchaku/blob/main/examples/v1/qwen-image-edit-2509.py){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. FP4 transformer와 offload 기반 로컬 실행 경로를 확인했다.
- Hugging Face, [Diffusers inpainting guide](https://huggingface.co/docs/diffusers/en/using-diffusers/inpaint){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-15. mask 기반 국소 편집의 동작 범위를 참고했다.
- Couairon et al., [DiffEdit](https://arxiv.org/abs/2210.11427){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. text-guided mask 기반 편집의 기본 방법을 확인했다.
- Jiang et al., [FitDiT](https://github.com/BoyuanJiang/FitDiT){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. garment detail virtual try-on의 입력 경계를 확인했다.
- Zheng et al., [CatVTON](https://github.com/Zheng-Chong/CatVTON){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-16. 가상 착장 전이 실험의 구현과 입력 형식을 확인했다.
