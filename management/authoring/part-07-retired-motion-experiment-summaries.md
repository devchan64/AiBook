# 폐기한 5.14~5.16 관련 실험 요약

2026-09-28 사용자 요청으로 미사용 sec-15 자산 127개(16,425,994바이트)를 삭제했다. 아래는 삭제 전 README의 이력 보존용 사본이며, 그 안의 보존 상태·경로·재사용 설명은 당시 기록이다. 현재 해당 파일은 없고 재검수할 수 없다. sec-14·sec-16 자산 디렉터리는 이미 없었다.

## 2026-09-19-momask-v4

````text
# P7-5.14 MoMask v4: 실제 전진과 접지 상태를 함께 보는 걷기

2026-09-19 실행 완료. 새 프롬프트 두 조건 × 시드 3개, 총 6개 모션. **짧은 전진 지시에서는 지면 근처에서 시작해 약 2.55~3.02m 이동했다.** 시작·종료 정지와 잔여 발 움직임이 있어 완전한 지속 보행 성공으로 판정하지 않는다.

## 설계 개선

- `travel`: `A person walks in a straight line across the room.`
- `grounded_travel`: `A person walks in a straight line across the room, starting with both feet on the floor and continuously moving forward.`
- 두 조건 사이에서 프롬프트만 변경했다. 96프레임·20fps, 시드 10107/10108/10109, mask 18 steps·CFG 4, residual CFG 5, temperature 1, top-k threshold 0.9, batch 1을 유지한다.
- 공식 생성·역정규화·원 관절 복원 경로를 대조했다. 루트 속도와 회전을 별도로 적분한 결과도 복원 골반 궤적과 1e-5m 이내에서 일치했다. 루트 이동을 제거하는 처리는 없다. BVH/IK·발 높이 보정·인위적 전진 이동은 적용하지 않는다.
- 클립마다 달라지던 화면 폭을 개선해 **6개 결과에 같은 고정 세계 좌표 화면 범위**를 적용했다. 확대·축소나 추적 카메라로 전진 여부를 판단하지 않는다.
- 추론 전에 초기 최저 발 높이 ≤4cm, 골반 수평 순이동 ≥1m를 탐색용 선별 기준으로 정했다. 생체역학적 합격 기준이 아니며 별도 육안·접촉 검수가 필요하다.
- 과거 폐기된 산출물을 복구하거나 기준군으로 재사용하지 않았다. 모델 가중치와 공식 생성 방식을 재사용했다.

## 결과

| 조건·시드 | 초기 발 높이(cm) | 수평 순이동(m) | 양발 4cm 초과 프레임 | 발목 앞뒤 교대 | 초기 높이·이동 선별 |
| --- | --- | --- | --- | --- | --- |
| grounded_travel-10107 | 0.6 | 0.03 | 4 | 8 | 미통과 |
| grounded_travel-10108 | -0.8 | 0.03 | 3 | 8 | 미통과 |
| grounded_travel-10109 | 0.2 | 0.11 | 0 | 8 | 미통과 |
| travel-10107 | 0.2 | 2.91 | 0 | 4 | 통과 |
| travel-10108 | 0.2 | 3.02 | 0 | 4 | 통과 |
| travel-10109 | 0.2 | 2.55 | 0 | 3 | 통과 |

`travel` 세 결과는 초기 부유가 작고 실제로 전진했다. 다만 첫 약 1.2초는 정지에 가깝고 후반에도 멈춘다. 골반 속도 0.1m/s를 넘는 구간은 시드별 약 23~24번부터 81~85번 부근까지다. 처음부터 끝까지 지속되는 걷기로 해석하지 않는다.

`grounded_travel` 세 결과는 바닥과 지속 이동 설명을 덧붙였지만 수평 순이동이 약 2.7~10.8cm에 그쳐 제자리 걷기에 가깝다. 긴 프롬프트가 항상 더 잘 제어한다는 근거는 얻지 못했다. 어느 추가 단어가 영향을 주었는지는 이 두 조건만으로 분리할 수 없다.

접촉을 직접 알 수 없어 발목·발끝 중 낮은 관절이 추정 바닥 2.5cm 이내인 연속 프레임을 골라 발끝 수평 속도를 계산했다. `travel`의 실제 이동 구간에서 중앙값은 약 0.079~0.127m/s다. 지지 발이 완전히 고정됐다고 판정할 수 없으며, 이 수치는 착지·이탈도 섞인 높이 기반 대리지표다. `grounded_travel`의 전체 근접 구간 중앙값은 약 1.20~1.31m/s로 컸다. 바닥은 클립 전체 발 관절 높이의 1백분위수이므로 실제 신발 밑창·지면 측정이 아니다.

전체 576프레임을 수치 분석하고 여섯 결과의 12장 요약을 육안 확인했다. 연속 영상과 전체 PNG는 2026-09-20 사용자 지시로 폐기했다. `travel`을 후속 검수 후보로 두며 캐릭터 영상화는 이번 실험에 포함하지 않았다.

GPU는 RTX 5070 Laptop, 최대 PyTorch 할당 약 0.89GiB였다. 모델 로딩 약 6.35초, 첫 모션 약 1.20초·이후 모션 약 0.089~0.102초이며 초기 실행 비용과 렌더링 비용을 구분한다.


2026-09-20 사용자 지시로 요약 외 모션 배열·영상·프레임·코드·상세 기록을 삭제했다. 후속 multiref 실행에 사용한 렌더링 포즈·마스크는 해당 실험의 입력으로 보존한다. 원 모션 재검수는 불가능하며 동일 조건 자동 재생성에서 제외한다. 관절 모션·포즈 입력의 결론은 P7-5.14 원고에, 이를 재사용한 캐릭터 영상 결과는 P7-5.15 원고에 반영했다.
````

## 2026-09-19-scail-v1

````text
# SCAIL-v1 실험 결과 요약 — 폐기

상태: 사용자 지시로 2026-09-19 폐기. 개별 프레임 품질 부족으로 제작용 결과에 채택하지 않았다.

- SCAIL-Preview Q4_K_M, 512×512, 33프레임·20fps, seed 23123134, CFG 5, 40 steps, shift 3.
- CFG의 positive·negative 양쪽에 같은 참조 latent를 전달한 수정에서 안개 같은 흐림이 크게 개선됐고 사용자가 이를 확인했다. 기존 ComfyUI 경로는 negative 참조를 0으로 채웠다.
- 걷기 동작은 유지됐으나 얼굴·머리 형태 변화와 손발 디테일 부족이 남았다. 사용자는 프레임 단위 품질이 부족하다고 판정했다.
- steps·shift 조절, BF16/FP32 디코딩, Q6 변경으로는 흐림을 충분히 해결하지 못했다. 단일 클립 관측으로 일반화하지 않는다.
- 최종 실행 시간 약 39.4분, peak allocated VRAM 약 3.22 GiB. 전체 장치 메모리 사용량과는 다르다.
- 영상·이미지·상세 로그·실행 스크립트는 삭제했다. 다음 SCAIL-2 실험에서 재사용하는 참조·포즈·입력 준비 기록은 `../2026-09-20-scail2-multiref-v1/`로 이관했다. 공용 모델 캐시는 유지한다.

근거 코드: [공식 SCAIL, revision 518074f](https://github.com/zai-org/SCAIL/blob/518074fbe8838eeda05b7a72462eac2c089feec2/wan/scail.py). 시각 산출물은 폐기되어 이 요약만으로 재검수할 수 없다.
````

## 2026-09-19-scail2-v1

````text
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
````

## 2026-09-20-scail2-704-v1

````text
# SCAIL-2 DPO 704p 결과 요약 — 폐기

2026-09-20 사용자 평가: **“품질은 향상되었지만 아직 사용할수 있는 수준은 아니다.”** 품질 향상은 사용자 정성 평가이며 실사용 승인을 뜻하지 않는다. 이후 사용자 지시에 따라 영상·프레임·상세 로그를 폐기하고 이 요약만 남겼다.

- 704×704, 33프레임·20fps, Q4_K_M, DPO strength 1.0, seed 23123134, CFG 5, 40 steps, shift 3.
- 512p 실험과 모델·참조·포즈·마스크·sampling 조건을 유지하고 네이티브 생성 해상도만 높였다. 기존 512p 입력은 내부 리사이즈됐으며 새 참조 정보는 추가되지 않았다.
- 이동 걷기와 큰 캐릭터 특징은 유지됐지만 얼굴·손·신발 세부 경계의 부드러움과 형태 검증 한계가 남았다.
- 약 74.7분, PyTorch peak allocated 4.44 GiB / reserved 5.68 GiB. PNG 33개 해시와 704×704·20fps 영상 프레임 수를 검증했다.
- 출력 저장 후 무시된 ComfyUI 소멸자 TypeError가 있었지만 종료 코드 0과 산출물 무결성을 확인했다.
- 재사용 입력·코드·모델 근거는 `../2026-09-20-scail2-multiref-v1/`로 이관했다. 공용 가중치 캐시는 유지한다. 삭제한 영상은 이 요약만으로 재검수할 수 없다.

출처: [SCAIL-2](https://github.com/zai-org/SCAIL-2/tree/wan-scail2).
````

## 2026-09-20-scail2-dpo-v1

````text
# SCAIL-2 DPO 512p 결과 요약 — 폐기

2026-09-20 사용자 지시에 따라 결과 요약만 남기고 영상·프레임·상세 로그를 폐기했다.

- SCAIL-2 Q4_K_M + 공식 bias-aware DPO strength 1.0. 512×512, 33프레임·20fps, seed 23123134, CFG 5, 40 steps, shift 3.
- 원본 DPO 800개 tensor를 변환해 모델의 400개 대상에 적용했다. 기본 실험과 입력·마스크·실행 revision 일치를 확인했다.
- 걷기와 큰 의상 특징은 유지됐으나 손·신발 디테일 부족, 얼굴·머리·셔츠 실루엣 변화, 배경 질감이 남았다. 이 조건에서 DPO만으로 개별 프레임 품질이 해결됐다고 판정하지 않았다.
- 약 39.0분, PyTorch peak allocated 2.92 GiB / reserved 3.58 GiB. 33개 PNG 해시와 영상 프레임 수·해상도·fps 확인 완료.
- 출력 저장 후 무시된 ComfyUI ON_DETACH 소멸자 오류가 있었다. 종료 코드 0과 산출물 무결성을 확인했다.
- 다음 704p 실험에 필요한 입력·코드·모델 기록은 `../2026-09-20-scail2-multiref-v1/`로 이관했다. 공용 모델 캐시는 유지한다. 삭제한 영상의 재검수는 요약만으로 불가능하다.

출처: [SCAIL-2 공식 DPO](https://github.com/zai-org/SCAIL-2/tree/wan-scail2), [공식 가중치](https://huggingface.co/zai-org/SCAIL-2/blob/main/model/bias-aware-dpo-lora.pt).
````

## 2026-09-20-scail2-multiref-v1

````text
# SCAIL-2 전신 + 근접 참조 대조 실험

2026-09-20 시작. SeedVR2는 사용자 평가상 디테일 개선이 없고 잔상이 추가되어 요약 후 폐기했다. 이번 실험은 생성 단계에서 참조 정보량을 보강한다.

실행 당시 기준은 전신 참조 실험이었다. 해당 기준 결과는 2026-09-20 사용자 지시로 요약 후 폐기했다. 기존 전신 참조에 같은 원본 960×1440의 `[140,110,844,814]` 영역을 리사이즈 없이 잘라 만든 704×704 얼굴·상반신·손 참조 한 장을 추가한다. 두 참조의 identity 색상은 파랑 `[0,0,255]`으로 같으며 각 참조를 별도 VAE latent로 인코딩한다. 포즈·마스크 등 재사용 입력과 다운로드 기록은 이 폴더로 이관해 실제 파일로 보존한다.

고정 조건: SCAIL-2 GGUF Q4_K_M, 공식 DPO strength 1.0, 704×704·33프레임·20fps, 40 steps·CFG 5·shift 3, uni_pc/simple, seed 23123134, 동일 cached text embedding. 근접 참조와 그 참조 마스크 추가만 바꾼다. 전신 참조 마스크는 기존 노드의 nearest-exact 확대와 대응하도록 704로 nearest 확대해 배치한다.

`prepare.py`는 크롭·마스크·해시를 기록한다. `run.py --dry-run`에서 신규 실행 1건을 확인하고 실행했다. 출력은 `multiref-dpo-q4-704/`에 기록한다. 기존 원본 생성은 약 74분이 걸렸으며 이번 실행 시간은 완료 후 확정한다.

평가는 기준 결과와 같은 프레임·동일 표시 크기에서 얼굴, 머리, 옷, 손발 형태, 인물 수, 이동 경로와 잔상을 비교한다. 선이 강조된 것만으로 디테일 개선이라고 판정하지 않는다. 실제 출력·사용자 검수 전에는 성공으로 기록하지 않는다. 다중 참조는 품질 저하 가능성이 있는 실험 기능이며 작은 출력 인물과 손가락 제어 부재는 여전히 남는다.

출처: [SCAIL-2 공식 다중 참조 안내](https://github.com/zai-org/SCAIL-2/tree/wan-scail2#experimental-functions-multi-reference). 실행 구현과 모델 revision은 기준 기록 및 실행 result.json에 남긴다.

실행 완료: 40/40 steps, 총 4788.86초(약 79.8분), 704×704 PNG 33장·20fps MP4 저장 완료. 출력 33장 해시·크기와 영상 33프레임 디코딩을 확인했다. 종료 시 ModelPatcher 소멸자 TypeError가 기록됐지만 출력 저장 및 검증은 완료됐다. 품질은 사용자 검수 대기다. [결과 영상](multiref-dpo-q4-704/animation.mp4), [현재 결과 표본](selected-frames.jpg).

기존 기준 영상을 포함한 비교판도 삭제했다. 삭제 전 비교 관찰은 review.json과 원고에 남기며 현재 직접 재비교는 불가능하다. 실행 당시 result.json과 runner 해시는 수정하지 않았다. prepare.py의 기준 준비 기록 경로만 현재 폴더로 바꿨다. 원 모션 배열은 폐기되어 포즈를 처음부터 재렌더링할 수 없지만 이번 실행에 쓰인 33장 포즈·마스크는 보존한다.
````

## 2026-09-20-scail2-native-ref-v1

````text
# 원본 기반 704p 전신 참조 — 결과 요약 및 폐기

2026-09-20 사용자 지시에 따라 영상·프레임·비교 자료·상세 실행 결과를 폐기했다. 현재 multiref 실험에 쓰인 입력·가중치 근거만 그 실험 폴더로 이관했다.

SCAIL-2 Q4_K_M·DPO 1.0, 704×704·33프레임·20fps, 40 steps·CFG 5·shift 3·seed 23123134. 원본 960×1440에서 전신을 직접 축소해 704 캔버스에 배치했다. 약 73.8분, peak allocated 4.44GiB / reserved 5.68GiB.

사용자 평가: “이제 동작은 확인할수 있을정도는 된것 같다.” 얼굴·손·신발의 세부 표현은 부족하며 최종 외형 품질·손발 정확성 승인은 아니다. 요약은 원고 P7-5.15에 통합했다. 폐기된 영상은 재검수할 수 없고 동일 조건 자동 재생성에서 제외한다.
````

## 2026-09-20-seedvr2-v1

````text
# SeedVR2 v1 — 결과 요약 및 폐기

2026-09-20 사용자 지시에 따라 결과 영상·프레임·비교 이미지·실행 스크립트·상세 로그/JSON을 폐기하고 이 요약만 남겼다. 동일 조건 자동 재생성 대상에서 제외한다.

SCAIL-2 native-ref 704p의 33프레임을 SeedVR2 3B Q8_0로 1024×1024 복원했다. Batch 5, temporal overlap 1, LAB, noise 0, seed 23123134, DiT 32 blocks CPU offload, VAE 타일 512/64. CLI 148.39초, 전체 프로세스 156.71초. RTX 5070 Laptop 8 GB에서 실행했다.

사용자 평가: **“디테일 개선되지 않았다.”** 초기 선명도 개선 해석을 철회한다. 008·024·032 등에서 인물 뒤 복제 잔상이 추가됐고, 원본 024와 직접 대조했다. **디테일 개선 없음과 추가 잔상으로 미채택**이다. 겹침 조정은 잔상 원인 진단일 뿐 디테일 해결 근거가 없다. 기존 SCAIL-2 기준 결과도 후속 사용자 지시로 요약 후 폐기했다. 공용 가중치는 보존한다.

구현: numz/ComfyUI-SeedVR2_VideoUpscaler revision `4490bd1f482e026674543386bb2a4d176da245b9`.
출처: [SeedVR](https://github.com/ByteDance-Seed/SeedVR), [CLI](https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler).

보존 가중치 다운로드 근거:

```json
[
  {
    "repo": "AInVFX/SeedVR2_comfyUI",
    "revision": "ac66d6d98fa49975d893b58c55bff7677191c862",
    "gated": false,
    "file": "seedvr2_ema_3b-Q8_0.gguf",
    "snapshot_file": ".tmp/download/huggingface/hub/models--AInVFX--SeedVR2_comfyUI/snapshots/ac66d6d98fa49975d893b58c55bff7677191c862/seedvr2_ema_3b-Q8_0.gguf",
    "bytes": 3660613984,
    "sha256": "be0d60083a2051a265eb4b77f28edf494e6db67ffc250216f32b72292e5cbd96"
  },
  {
    "repo": "numz/SeedVR2_comfyUI",
    "revision": "09ced71023636e9bc8cdf9cdecfb2625d1e691e8",
    "gated": false,
    "file": "ema_vae_fp16.safetensors",
    "snapshot_file": ".tmp/download/huggingface/hub/models--numz--SeedVR2_comfyUI/snapshots/09ced71023636e9bc8cdf9cdecfb2625d1e691e8/ema_vae_fp16.safetensors",
    "bytes": 501324814,
    "sha256": "20678548f420d98d26f11442d3528f8b8c94e57ee046ef93dbb7633da8612ca1"
  }
]
```
````
