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
