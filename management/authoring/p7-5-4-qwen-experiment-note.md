# P7-5.4 Qwen 구도·화풍·캐릭터 일관성 실험 노트

작성일: 2026-08-16

## 목적

Qwen-Image-Edit-2509에서 `구도`, `화풍`, `캐릭터 identity·착장`을 서로 다른 입력 역할로 둘 때 어떤 계약이 유지·충돌하는지 확인한다. 후보를 제작 승인 자산이나 LoRA 학습 입력으로 자동 승격하지 않는다. 사람 검수에서 네 계약이 모두 통과한 경우에만 다음 단계 입력 후보로 기록한다.

## 현재 증거

| 조건 | 입력 역할 | 확인된 관찰 | 현재 판정 |
| --- | --- | --- | --- |
| 고각도 보행, 3입력, seed `62294/62295` | guide / 얼굴 / 완성 착장 | 두 seed에서 고각도 보행·얼굴·착장·가방 strap이 함께 남았다. | 사람 검수 완료. 고정 guide·보행 범위의 P7-5.4 참조 증거만 승인. |
| 고각도 보행, style clause, seed `62294` | 같은 3입력 / prompt의 화풍 문장만 추가 | 선화와 색 번짐이 기존 고각도 결과보다 P7-5.1의 수채화 기준에 가까워 보인다. | 관찰 단계. 동일 seed의 baseline과 계약별 사람 검수가 필요. |
| P7-5.3 Scene C, 3입력, seed `62294` | storyboard / 얼굴 / 완성 착장 | 공중 split leap·청록 단발·재킷·바지·가방은 대체로 남았지만, 자갈 바닥이 사진 질감으로 남았다. | 화풍 계약 미통과 후보. 사람 검수 대기. |
| P7-5.3 Scene C, 4입력, seed `62294` | storyboard / 얼굴 / 완성 착장 / 화풍 이미지 | 화풍 입력을 더하자 실사 인물·검은 머리·검은 의상으로 바뀌었다. | identity·outfit·style 계약 미통과 후보. 사람 검수 대기. |
| P7-5.3 Scene C, guide-first B1, seed `62294` | 수채화화 guide / 얼굴 / 완성 착장 | 중간 guide의 배경은 수채화화됐지만 익명 인물의 검은 머리·검은 의상이 남았다. 최종 3입력도 그 인물을 교체하지 않고 유지했다. | identity·outfit 계약의 명백한 실패 후보. 교차 seed는 실행하지 않음. 사람 검수 대기. |
| P7-5.3 Scene C, identity-free 구조 guide B2, seed `62294/62295` | depth 실루엣 기반 구조 guide / 얼굴 / 완성 착장 | 두 seed 모두 청록 단발, 흰 재킷, 청록 와이드 바지, 흰 운동화, 남색 crossbody bag·strap, split leap와 분리 그림자를 함께 만들었다. | 사람 검수 완료. 제한된 구조 guide 조건의 교차 seed 통과. |
| P7-5.3 Scene A, identity-free 구조 guide B2, seed `62294` | depth 기반 협곡 구조 guide / 얼굴 / 완성 착장 | 캐릭터·착장·수채화는 유지했지만, 양쪽 협곡 벽과 고각도 공간 구조가 한쪽 절벽과 넓은 여백으로 단순화됐다. | structure 계약 미통과 후보. 교차 seed 미실행. |
| P7-5.3 Scene B, identity-free 구조 guide B2, seed `62294` | depth 기반 평지 구조 guide / 얼굴 / 완성 착장 | 캐릭터·착장·수채화·평지와 낮은 수평선은 남았지만, 원래의 곧은 양쪽 다리 split leap가 한쪽 다리를 굽힌 도약으로 바뀌었다. | 사용자 검수: 구도만 통과, 캐릭터·소품·화풍 탈락. 착장 보류. 교차 seed 미실행. |

### 세 스토리보드에 대한 결론

세 Scene에 공통 적용 가능한 화풍·구도·캐릭터 재현 경로는 확인하지 못했다. Scene C는 두 seed와 사람 검수에서 제한 조건의 통과 사례였지만, Scene A는 협곡 기하가, Scene B는 정확한 split-leap 포즈가 유지되지 않았다. 따라서 이 방식의 결과를 세 스토리보드 전체의 일관된 화풍이나 재현성 증거로 일반화하지 않으며, P7-5.3 승인 스토리보드를 대체하거나 공통 제작 규칙으로 승격하지 않는다.

### 원인 분석

1. **구조 조건을 실제 제어 조건이 아니라 RGB 참고 이미지로 바꿨다.** B2 guide는 depth map을 수채화색·입자·반투명 실루엣으로 렌더링한 이미지다. 따라서 원래 depth의 거리값·경계·정확한 관절 위치는 Qwen에 강제 조건이 아니라 해석해야 할 시각 단서가 됐다. Qwen-Image-Edit-2509은 depth·edge·keypoint ControlNet 조건을 별도로 지원하지만, 이번 B2 실행은 그 경로를 쓰지 않았다.
2. **identity-free 처리와 장면 보존 사이에 정보 손실이 생겼다.** 원본 인물 RGB를 제거한 것은 B1의 검은 의상·실사 인물 고착을 막았지만, 같은 처리로 인물의 세부 자세와 배경의 식별 가능한 기하도 약해졌다. Scene A의 두 협곡 벽·깊이 관계와 Scene B의 곧은 두 다리 split leap는 이 손실에 민감했다.
3. **세 이미지의 역할은 분리했지만, 결과 계약은 여전히 경쟁한다.** 첫 이미지는 장면·카메라·포즈·화풍을, 둘째는 얼굴·헤어를, 셋째는 전신 의상·가방을 요구한다. 모델은 1–3 입력에서 가장 좋은 성능을 목표로 설계됐지만, 이는 세 계약의 픽셀 수준 보존을 보장하지 않는다. 실제 출력은 비교적 강한 identity·outfit 단서를 우선하며, 장면 기하와 해부학적 포즈를 자연스러운 단일 이미지로 다시 해석했다.
4. **Scene C가 우연히 더 적합한 구조였다.** 수직 시점, 균일한 자갈 바닥, 분리된 그림자, 크게 보이는 실루엣은 적은 구조 단서로도 복원할 수 있다. 반대로 Scene A는 다중 배경 평면과 협곡 벽의 배치가 핵심이고, Scene B는 수평선·여백·정확한 다리 각도가 동시에 필요하다. 그래서 C의 통과는 B2 방식 일반의 증거가 아니라 낮은 구조 복잡도에서만 성립한 사례다.
5. **현재 재현성 표본은 불균형하다.** C만 두 seed와 사람 검수를 통과했고, A/B는 첫 seed에서 명백한 structure 실패라 두 번째 seed를 생략했다. 이는 합리적인 중단 근거이지만 A/B의 확률적 성공률을 수치화한 결과는 아니다.

다음 가설은 화풍·identity·outfit 참조는 유지하되, 구도·관절은 RGB guide 대신 depth 또는 keypoint ControlNet으로 명시적으로 고정하는 것이다. 이 가설은 새 비교 설계를 먼저 만들고, `구조 제어 방식` 하나만 B2와 바꿔 검증한다.

### 개선 실험: Qwen depth-ControlNet 1단계

`InstantX/Qwen-Image-ControlNet-Union`의 depth 조건을 Qwen-Image-Edit-2509 Nunchaku FP4 transformer와 결합했다. B2의 수채화 RGB guide 대신 P7-5.3 원본 depth map을 `control_image`로 넣고, `controlnet_conditioning_scale 0.9`, seed `62294`, 40 step을 고정했다. 이 단계는 다중 reference edit 파이프라인이 아니므로 얼굴·완성 착장 이미지를 입력하지 않고, 같은 특징을 텍스트로만 지정한 **구조 제어 사전 검증**이다.

| Scene | 개선 전 B2에서 깨진 계약 | depth-ControlNet 관찰 | 현재 판정 |
| --- | --- | --- | --- |
| A | 양쪽 협곡 벽·고각도 공간 구조 | 양쪽 협곡 벽과 split leap가 다시 나타났다. | 구조는 개선됐지만 청록 헤어가 검은색으로 바뀌어 identity 계약 미통과. |
| B | 곧은 양쪽 다리 split leap | 평지·수평선·곧은 split leap가 다시 나타났다. 인물 크기는 원래 storyboard보다 커졌다. | pose·배경은 개선됐지만 framing·identity 계약 미통과. |
| C | 수직 bird's-eye 시점 | split leap와 분리 그림자는 나타났지만 수직 시점이 비스듬한 근거리 시점으로 바뀌었다. | camera·identity 계약 미통과. |

- **확인된 개선:** depth를 RGB guide가 아니라 ControlNet 조건으로 넣으면 A/B의 배경 기하와 leap 포즈가 B2보다 강하게 유지된다.
- **남은 한계:** 이 ControlNet pipeline은 이번 구성에서 얼굴·완성 착장 reference를 함께 받지 않는다. 텍스트의 `petrol-teal bob`은 세 장면 모두 검은 머리로 재해석됐다. 따라서 이 결과는 세 Scene의 최종 4계약 통과가 아니며, 다음 단계는 ControlNet 결과를 guide로 하여 Qwen Edit reference 보정을 추가할 때 구조가 다시 무너지지 않는지 별도로 검증해야 한다.

### 개선 실험: ControlNet guide → Qwen Edit reference 보정

depth-ControlNet 1단계의 출력을 첫 번째 guide로 사용하고, Qwen Edit에 얼굴 reference와 완성 착장 reference를 두 번째·세 번째 입력으로 넣었다. 세 장면은 seed `62294`, 40 step, `true_cfg_scale 4.0`을 고정했다.

| Scene | 관찰 | 사람 검수 전 판정 |
| --- | --- | --- |
| A | 협곡의 양쪽 벽, split leap, 청록 단발, 흰 재킷·청록 바지·흰 운동화·남색 bag/strap, 수채화 선화가 함께 남았다. | 사람 검수: 구도 통과, 캐릭터·화풍·소품 탈락. 교차 seed 미실행. |
| B | 평지·낮은 수평선·split leap·청록 단발·완성 착장·수채화는 남았지만 인물 크기가 승인 storyboard의 약 40%보다 크다. | 사람 검수: 구도 통과, 캐릭터·화풍·소품 탈락. 교차 seed 미실행. |
| C | 청록 단발·완성 착장·도약·분리 그림자는 남았지만, 수직 bird's-eye 시점이 비스듬한 근거리 시점으로 바뀌었다. | 사람 검수: 화풍·소품 통과, 캐릭터·구도 탈락. 교차 seed 미실행. |

이 표의 판정은 AI 예비 관찰이며, `A/B/C × structure/identity/outfit/style`의 최종 통과 여부는 사람 검수로만 확정한다.

#### 사람 검수에 근거한 결론 (2026-08-17)

- A는 구도만 통과했고 캐릭터·화풍·소품이 탈락했다.
- B는 구도만 통과했고 캐릭터·화풍·소품이 탈락했다.
- C는 화풍·소품은 통과했지만 캐릭터·구도가 탈락했다.
- 세 장면 모두 첫 seed에서 필수 계약 중 하나 이상이 탈락했으므로, 교차 seed 재실행은 통과 재현성을 증명하는 데 의미가 없어 실행하지 않았다. 의상 계약은 사용자가 명시적으로 판정하지 않았지만, 각 장면에 이미 다른 필수 계약 탈락이 있어 최종 판정에는 영향을 주지 않는다.
- 결론적으로 **ControlNet depth → Qwen Edit reference 보정은 A/B의 구도는 개선했으나, A/B/C 전체에서 구도·캐릭터·화풍·소품을 동시에 만족하는 공통 재현 경로를 만들지 못했다.** 이 결과를 P7-5.3 승인 storyboard 대체, 공통 제작 규칙, LoRA 학습 입력으로 승격하지 않는다.

### 후속 원인 가설과 통제 개선: 캐릭터 참조의 시점 부족

후속 분석에서는 A/B의 구도 통과와 캐릭터·화풍·소품 탈락이 함께 나타난 점에 주목했다. ControlNet 1단계 출력에는 이미 렌더된 인물의 머리·의상 RGB가 남아 있고, 최종 Edit에는 정면 얼굴만 넣었다. 특히 공중 도약의 옆·사선 얼굴에서는 첫 입력의 인물 RGB와 정면 얼굴 reference가 경쟁할 수 있다. 따라서 다음 가설은 **정면 단일 얼굴 reference가 비정면 장면에서 identity를 충분히 고정하지 못한다**이다.

| 항목 | 기존 A | 개선 A |
| --- | --- | --- |
| 첫 입력 | 동일한 A depth-ControlNet 출력 | 동일 |
| 셋째 입력·프롬프트·seed·step | 동일한 완성 착장 / 동일 / `62294` / `40` | 동일 |
| 둘째 입력 | 768×768 정면 얼굴 1장 | 같은 총 캔버스 768×768 안의 정면·좌측 프로필 2패널 |

- 처음 만든 2048×1024 시트는 기준 입력보다 면적이 두 배여서 GPU 실행이 출력 전 종료했다. 이는 결과 후보가 아니라 **입력 크기 교란을 발견한 사전 검증 실패**로 기록하며, 사람 검수나 계약 판정에 사용하지 않는다.
- 1024×1024로 축소한 두 번째 시트도 기준선의 실제 얼굴 입력(768×768)보다 컸으므로 무효 처리했다. 유효 조건은 두 패널을 384×384로 축소해 총 입력 캔버스를 기준선과 같은 768×768로 맞췄다. 이로써 비교에서 바뀌는 내용 변수는 캐릭터 reference의 시점 수뿐이다.
- 유효 A 출력은 생성 후 기존 A와 함께 사람 검수한다. identity가 통과해도 화풍·소품 중 하나가 탈락하면 공통 경로로 승격하지 않는다. 첫 seed가 모든 계약을 통과할 때만 seed `62295`를 추가해 재현성을 확인한다.
- 2026-08-17 현재 2048×1024 및 1024×1024 시트 실행은 PNG·run JSON을 남기지 못했다. 이는 해상도 교란 조건의 실패이므로 모델 실패나 계약 탈락으로 해석하지 않는다. 768×768 유효 조건으로 재개한다.

#### 유효 A 단일 변수 실행 결과 (사람 검수 대기)

- 실행 ID: `p7-5-4-qwen-scene-a-controlnet-guide-face-sheet`
- 고정 조건: A depth-ControlNet guide SHA-256 `b3037ae…21fbd69`, 같은 완성 착장 reference, prompt, seed `62294`, 40 step, `true_cfg_scale 4.0`.
- 변경 조건: 기존 768×768 정면 얼굴 1장 대신, 동일 768×768 캔버스의 정면·좌측 프로필 2패널 시트(SHA-256 `eb22750c…c124f3`).
- 실행 결과: `scene-a-controlnet-guide-face-sheet-seed-62294-steps-40.png`, SHA-256 `1a2890ac…3ebf15`, 1,151.73초.
- AI 예비 관찰: 기존 A의 구도·흰 재킷·청록 바지·남색 crossbody bag은 대체로 유지됐지만, 후보의 헤어는 청록 대신 검은색으로 나타났다.
- 사람 검수(2026-08-17): **구도 통과, 캐릭터·소품·화풍 탈락**. 의상은 별도 판정하지 않았다. 따라서 768×768 2시점 시트는 이 A 조건에서 identity·소품·화풍 계약을 개선했다는 증거가 아니며, 후보를 승격하지 않는다.

GPU 실행 중 발생한 OOM은 서로 겹친 이전 Qwen 프로세스가 각각 약 2.4GB를 점유한 상태에서 text encoder가 추가 1.02GB를 요구한 데서 발생했다. 잔류 프로세스를 종료하고 GPU 여유 약 6.85GB 상태에서 분리 세션으로 유효 실행을 완료했다. OOM 시도는 후보로 사용하지 않는다.

### 고해상도 후속 가설과 설계

768×768 시트는 동일 캔버스 안에서 정면·프로필을 각각 384×384까지 줄였기 때문에, 얼굴·헤어의 식별 단서가 사라져 guide에 남은 익명 인물 RGB가 더 우세했을 가능성이 있다. Qwen 공식 문서는 다중 이미지 편집의 최적 범위를 1–3 입력 이미지로 안내하고, 본 실험의 3입력 구성(guide·캐릭터·의상)은 그 범위 안이다. 따라서 입력 수·순서·prompt·guide·의상·seed·step은 고정하고, **둘째 입력의 2시점 시트만 768×768에서 1024×1024로 높인다**. 두 얼굴 패널은 각각 512×512가 된다.

- 비교 대상: 위 768×768 2시점 A 결과.
- 단일 변경 변수: 캐릭터 2시점 시트의 전체 해상도 및 각 패널의 유효 해상도.
- 고정: A depth-ControlNet guide, 완성 착장 reference, prompt, seed `62294`, 40 step, `true_cfg_scale 4.0`, guidance scale `1.0`.
- 판정: 사람 검수에서 구도·캐릭터·소품·화풍을 모두 통과해야만 고해상도 시트가 이 A 조건의 유효 개선으로 기록된다. 하나라도 탈락하면 교차 seed를 실행하지 않고, 해상도 증가가 이 계약 충돌을 해결하지 못했다고 제한적으로 결론 낸다.

근거: [Qwen-Image-Edit-2509 공식 소개](https://github.com/QwenLM/Qwen-Image/blob/main/Qwen-Image-Edit-2509.md)는 1–3 이미지 입력에서의 최적 성능과 다중 이미지 편집·ControlNet 지원을 설명하며, [공식 모델 카드](https://huggingface.co/Qwen/Qwen-Image-Edit-2509)는 `QwenImageEditPlusPipeline`의 40-step 다중 입력 예시를 제공한다.

#### 고해상도 A 실행 결과 (사람 검수 대기)

- 실행 ID: `p7-5-4-qwen-scene-a-controlnet-guide-face-sheet-1024`
- 결과: `scene-a-controlnet-guide-face-sheet-1024-seed-62294-steps-40.png` (run JSON에 입력 SHA-256·runtime·seed·prompt를 기록).
- AI 예비 관찰: 구도·흰 재킷·청록 바지·남색 bag은 768×768 결과와 같이 남았지만, 헤어는 여전히 검은색이다. 즉 해상도 증가만으로는 guide 인물 RGB와 identity reference의 충돌을 해소하지 못한 것으로 보인다. 사람 검수의 구도·캐릭터·소품·화풍 판정 전에는 이 관찰을 최종 결론으로 사용하지 않는다.
- 사람 검수(2026-08-17): **구도·화풍 통과, 캐릭터·소품 탈락**. 의상은 별도 판정하지 않았다.

### 후속 단일 변수 실험의 결론

| A 조건 | 사람 검수 결과 | 해석 |
| --- | --- | --- |
| 768×768 2시점 시트(각 384×384 패널) | 구도 통과; 캐릭터·소품·화풍 탈락 | 2시점 축소 시트는 identity·소품·화풍을 보장하지 못했다. |
| 1024×1024 2시점 시트(각 512×512 패널) | 구도·화풍 통과; 캐릭터·소품 탈락 | 해상도 증가는 이 A 조건에서 화풍 계약만 개선했으며, identity·소품 충돌을 해소하지 못했다. |

두 실행은 guide·의상 reference·prompt·seed·step을 고정하고 캐릭터 시트 해상도만 바꿨다. 따라서 이 비교가 지지하는 범위는 **A의 2시점 캐릭터 reference에서 768→1024 해상도 증가는 화풍은 개선할 수 있으나 캐릭터·소품 계약의 동시 통과 증거가 아니다**라는 제한된 결론이다. A/B/C의 앞선 사람 검수와 함께 보면, ControlNet→Edit 파이프라인은 장면별로 구도 또는 화풍 일부를 보존해도 네 계약을 동시에 유지하지 못했다. 구도·캐릭터·소품·화풍을 모두 통과한 seed가 없으므로 교차 seed를 실행하지 않으며, 이 경로를 승인 스토리보드 대체·공통 제작 규칙·LoRA 학습 입력으로 승격하지 않는다.

더 높은 해상도를 단독으로 올리는 다음 실험은 우선순위가 낮다. 다음 가설은 해상도가 아니라 **ControlNet guide에 남은 렌더 인물 RGB를 구조 조건에서 분리하는 것**이며, 이 가설을 검증하려면 인물 영역을 신뢰성 있게 제거하거나 keypoint/depth를 최종 Edit의 native ControlNet 조건으로 직접 연결하는 별도 설계가 필요하다. 이는 현재의 해상도 단일 변수 비교와는 다른 실험이다.

### ControlNet guide 인물 RGB 제거 실험의 결론

Scene A ControlNet guide의 렌더 인물을 넓은 수동 포즈 마스크로 중립 실루엣으로 바꿨다. 얼굴·의상·prompt·seed `62294`·40 step은 기존 A와 고정했다. 인물 RGB가 완전히 남지 않도록 한 대신, 인물 주변 배경도 일부 가려지는 제한이 있다.

- 사람 검수(2026-08-17): **구도·소품·화풍 통과, 캐릭터 탈락**. 의상은 별도 판정하지 않았다.
- 인물 RGB를 남긴 ControlNet→Edit 결과는 구도를 지키는 경향이 있지만 캐릭터·소품·화풍이 탈락했다. 인물 RGB를 제거하면 소품·화풍은 통과했으나, 원래의 split-leap·카메라 세부는 약해지고 캐릭터는 여전히 탈락했다.
- 따라서 guide의 렌더 인물 RGB는 소품·화풍 실패에 기여하는 경쟁 신호였다는 증거가 되지만, 제거만으로 identity를 고정하기에는 부족하다. **A에서 구도·캐릭터·소품·화풍의 동시 통과 경로는 확인하지 못했다.**
- 모든 필수 계약을 통과한 첫 seed가 없으므로 교차 seed는 실행하지 않는다. 이 결과를 승인 storyboard 대체·공통 제작 규칙·LoRA 학습 입력으로 승격하지 않는다.

### 인물 마스크 inpaint 경로의 결론

ControlNet Stage 1의 협곡 이미지를 source로 두고, 인물 영역만 흰 mask로 다시 그리는 `QwenImageEditInpaintPipeline` 실험을 실행했다. 현 설치본은 inpaint에 다중 얼굴·의상 reference를 결합하지 못하므로, 청록 턱선 단발·호박색 홍채·착장·가방은 prompt로만 지정했다.

- 사람 검수(2026-08-17): **캐릭터 탈락**. 청록 헤어와 호박색 홍채가 표현되지 않았다. 나머지 계약은 별도 판정하지 않았다.
- 따라서 inpaint는 배경을 보존해도 text-only character 계약을 대체하지 못한다. 특히 얼굴·머리색·홍채색처럼 reference 이미지의 세부 단서가 필요한 identity에는 이 경로를 사용하지 않는다.
- 이 결과는 캐릭터 reference를 유지한 다중 이미지 편집과 inpaint를 현재 로컬 파이프라인 하나로 결합할 수 없다는 구현 한계를 분명히 한다. 다음 후보는 **완성 캐릭터 시트 하나 + 구조 guide**의 2입력 EditPlus 경로이며, 얼굴·의상·가방 단서를 같은 reference에 결합해 입력 역할 경쟁을 줄이는 가설이다.

### 완성 캐릭터 시트 2입력 경로의 결론

정면·프로필 얼굴과 전신 의상·가방을 하나의 1024×1152 캐릭터 시트로 합치고, A ControlNet structure guide와 두 입력만 Qwen Edit Plus에 넣었다. 별도의 의상 입력을 제거한 것이 기존 3입력 대비 유일한 역할 변화다.

- 사람 검수(2026-08-17): **구도만 통과, 캐릭터·소품·화풍 탈락**. 의상은 별도 판정하지 않았다.
- 따라서 참조를 한 장으로 합쳐 입력 수를 3→2로 줄이는 것만으로는 캐릭터 identity·소품·화풍의 계약 충돌을 해소하지 못했다. 캐릭터 시트의 작은 얼굴 보조 패널이 identity 단서로 충분하지 않았거나, 장면 guide의 공간·포즈 조건이 여전히 우선했을 가능성이 있다.
- 이 실패는 교차 seed 통과 가능성을 증명할 수 없으므로 추가 seed를 실행하지 않는다. 현재 Qwen EditPlus 경로에서 scene guide와 독립 identity·outfit reference를 역할별로 조합하는 방식은 A의 네 계약 동시 통과 근거가 없다.

### 입력 순서 반전 비교: 캐릭터 시트 → structure guide

같은 Scene A structure guide와 같은 1024×1152 완성 캐릭터 시트, seed `62294`, 40 step, `true_cfg_scale 4.0`, prompt를 유지한 채 두 입력의 순서만 반전했다. 기존 2입력 실험은 `structure guide → 캐릭터 시트`였고, 이번 조건은 `캐릭터 시트 → structure guide`다. prompt도 첫 이미지를 identity·착장, 둘째 이미지를 협곡·점프·지면으로 한정하도록 순서에 맞춰 바꿨다.

- 실행 기록: `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/scene-a-character-first-structure-second-seed-62294-steps-40-run.json`
- 출력: `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/scene-a-character-first-structure-second-seed-62294-steps-40.png` (SHA-256 `ed8f82ce2bcb1fbb487e9f3a44f0afa3f30074324b7970bdc804afd210589d03`, 685.52초)
- 사람 검수 JSON: `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/scene-a-character-first-structure-second-seed-62294-steps-40-human-review.json`
- 사용자 최종 검수(2026-08-17): **구도·캐릭터·소품·화풍은 모두 통과**. 다만 흰 재킷 안의 회색 이너 탑이 재현되지 않아 착장 계약은 탈락했다.
- 따라서 `캐릭터 시트 → structure guide` 순서 반전은 같은 seed에서 앞선 `structure guide → 캐릭터 시트`의 캐릭터·소품·화풍 탈락을 해소했다. 이 조건에서 입력 순서는 structure guide보다 캐릭터 시트의 identity·소품·화풍 단서를 우선시키는 방향으로 작동한 증거다. 그러나 회색 이너 탑 누락 때문에 완전한 캐릭터 재현 경로·승인 storyboard 대체·LoRA 학습 입력으로 승격하지 않는다.
- 다음 제안: 다른 조건을 바꾸지 않고 출력 해상도만 1024²→1536²로 높여 얼굴 묘사 개선 여부를 비교한다. 다만 EditPlus가 reference 이미지를 고정 크기의 잠재 표현으로 변환하면, 출력 해상도만 높여서는 캐릭터 시트의 얼굴 단서 자체가 부족한 문제를 해결하지 못할 수 있다. 따라서 이 실험은 **얼굴 표현의 해상도 가설**만 검증하며, identity reference의 설계 개선과 혼동하지 않는다.

### 출력 해상도 비교: 1024² → 1280²

캐릭터 시트→structure guide 순서, 같은 두 입력의 SHA-256, seed `62294`, 40 step, `true_cfg_scale 4.0`, prompt와 offload를 고정했다. 출력 해상도만 바꿨다.

- 1536² 사전 시도: 40 step 샘플링은 완료했지만 VAE 복호화에서 추가 `1.27 GiB` 할당이 필요해 RTX 5070 Laptop 8GiB GPU에서 `CUDA out of memory`로 중단됐다. 산출물·사람 검수 JSON은 만들지 못했다.
- 대체 실행: 1280²는 완료했다. 출력 `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/scene-a-character-first-structure-second-1280-seed-62294-steps-40.png`, SHA-256 `8cf4929cf9fac66fbd159753deca7543dd4727b2ff7a025c3c56af829257c7c4`, 934.02초. 실행 기록은 같은 이름의 `-run.json`에 남겼다.
- 사람 검수(2026-08-17): 1280²는 **구도·소품만 통과**, 캐릭터·화풍은 탈락했다. 착장은 별도 판정하지 않았다.
- 결론: 1280²는 1024² 기준선의 네 핵심 계약 동시 통과를 재현하지 못했으므로, 이 조건에서 출력 해상도 증가는 얼굴 표현의 개선책이 아니라 캐릭터·화풍을 후퇴시킨 변수다. 1536²도 복호화 메모리 부족으로 실행 불가였으므로, 해상도를 더 올리는 후속 seed는 실행하지 않는다.

### A·B·C 공통 파이프라인 재현성 비교 (사람 검수 대기)

앞선 장면별·경로별 비교와 분리해, 세 Scene에 같은 파이프라인을 적용했다. 순서는 `완성 캐릭터 시트 → 해당 Scene의 ControlNet structure guide`, seed `62294`, `1280×1280`, 60 step, `true_cfg_scale 4.0`, 동일 모델·offload이고, 장면의 카메라·배경·점프 조건만 prompt와 guide에 맞춰 바꿨다.

| Scene | 출력 SHA-256 | 소요 시간 | 사람 검수 |
| --- | --- | --- | --- |
| A | `57de1661dea0ac508fdd61452a14706b810a98d9a612da88bffbf72a4450e8b2` | 1384.51초 | 대기 |
| B | `e58390a007215bcb213215f489736e09f68900222be4ca5da887421387de5a83` | 1388.33초 | 대기 |
| C | `34e9290be5a6f5b56ff5cf6f87e7cbdace1e5c44e38477341834d7248c40c8cb` | 1377.25초 | 대기 |

- 실행·검수 JSON과 PNG는 `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/`의 `scene-{a,b,c}-character-first-structure-second-1280-steps60-*`에 남겼다.
- 사람 검수에서 각 Scene의 구도·캐릭터·소품·화풍을 같은 기준으로 판정하기 전에는, 이 공통 조건이 장면 간 재현성을 개선했다고 주장하지 않는다.

### 80 step 재실행 (사람 검수 대기)

같은 `1280×1280`, seed `62294`, 캐릭터 시트→structure guide 순서, prompt·model·offload를 고정하고 step만 60→80으로 올렸다. 이는 step 수의 단일 변수 비교다.

| Scene | 출력 SHA-256 | 소요 시간 | 사람 검수 |
| --- | --- | --- | --- |
| A | `eecd7124922e2b1405c64ebd814667e4c3bb8936e8e1c0957a938ba0756d9fa9` | 1691.94초 | 대기 |
| B | `c5f86543b737667f97fe6e8804ab23c4b8fc734f2b9129da3cc67ca83a32a0cf` | 1857.28초 | 대기 |
| C | `ce9e373c675f643b89eaffc8965e53cc0f749da96b5b03b3b3aada3a0979348d` | 1866.67초 | 대기 |

- 산출물·실행 기록·검수 JSON은 `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/scene-{a,b,c}-character-first-structure-second-1280-steps80-*`에 있다.
- 사용자 검수(2026-08-17): 1280 조건은 기존보다 캐릭터·구도·소품을 더 많이 재현했다. 그러나 **A·B의 화풍은 재현하지 못했다.** C의 화풍 계약은 이번 검수에서 별도 통과·탈락을 판정하지 않았다.
- 원인 1 — **참조 자산 선택·역할 배정의 불일치**: 정면 얼굴(`p7-5-2-face-front-reference.png`)·정면 전신(`p7-5-2-fullbody-front-refined-reference.png`)·정면 3/4 전신 자료는 이미 준비돼 있다. 그러나 80-step 실행은 과거의 합성 character sheet와 `front-hip` crop을 사용했으며, 준비된 정면 전신 원본을 별도 착장 입력으로 쓰지 않았다. 따라서 이너 셔츠·가방 strap·신발의 전신 관계가 입력에서 약해졌다.
- 원인 2 — **구도 자산 선택·역할 배정의 불일치**: Scene A·B·C에는 각각 사람 승인 contract와 원본 storyboard RGB·relative depth가 준비돼 있다. 그러나 80-step 최종 Edit는 이 원본 대신 파생 ControlNet structure guide를 썼다. 따라서 바라보는 방향·팔다리 방향·카메라와 공간 조건이 최종 입력에서 약해졌다. 화상 편집 API의 native ControlNet 입력은 아니지만, 다음 기본 경로는 승인 storyboard depth를 직접 Edit 참조로 사용하고 RGB는 통제 비교 조건으로 사용한다.
- 원인 3 — **화풍 참조 역할의 미연결**: P7-5.1 승인 화풍 팩은 고각도·광각·눈높이와 다양한 시간·장소를 이미 제공한다. 그러나 80-step 최종 Edit는 화풍 이미지를 별도 입력 역할로 쓰지 않고 prompt의 화풍 문장에만 의존했다. 화풍 자산 부족이 아니라, 3입력 예산 안에서 character·structure·style 역할을 명시하지 않은 것이 A·B 화풍 실패의 직접 원인 후보다.
- 참고 관찰(사용자 제공 고각도 보행 산출): 청록 단발·황금 홍채·흰 재킷·회색 이너 셔츠·청록 바지·남색 crossbody bag·운동화가 한 전신 이미지에서 함께 보존됐다. 다음 실행은 이미 준비된 **정면 전신과 이너 셔츠가 동시에 보이는 원본 참조**를 사용해야 한다. 이 이미지는 관찰 근거이며, 별도 사용 지시 전에는 다음 Edit 입력으로 자동 사용하지 않는다.
- 결론: 1280은 캐릭터·구도·소품의 상대적 개선 신호지만, A·B의 화풍 실패와 착장·방향 정보 누락 때문에 A·B·C 공통 재현 파이프라인으로 승인하지 않는다. 다음 개선은 step 증가가 아니라 **완성 character sheet(정면 얼굴·전신 착장) + 원본 storyboard depth/RGB + P7-5.1 승인 화풍 참조**를 각 1장씩 3입력으로 사용해 검증해야 한다.

현재 기록 위치:

- 고각도 보행: `.tmp/p7-5-4-qwen-edit-high-angle/`
- 고각도 화풍 문장 비교: `.tmp/p7-5-4-qwen-edit-style-ab/`
- P7-5.3 Scene C 비교: `.tmp/p7-5-4-qwen-edit-p753-scene-c/`
- Scene C guide-first 비교: `.tmp/p7-5-4-qwen-edit-p753-guide-first/`
- Scene C identity-free 구조 guide: `.tmp/p7-5-4-qwen-edit-p753-structure-guide/`
- Scene A/B identity-free 구조 guide 실험: `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/`

## 다음 가설과 최소 비교

Qwen-Image-Edit-2509의 다중 이미지 편집은 1–3 입력을 기본 범위로 둔다. 따라서 Scene C에서 화풍을 네 번째 입력으로 더하는 대신, 먼저 scene guide 자체를 P7-5.1의 승인 화풍으로 변환하고 그 결과를 최종 3입력 편집의 composition guide로 사용한다.

| 단계 | 조건 | 바꾸는 변수 | 반드시 확인할 계약 |
| --- | --- | --- | --- |
| A | Scene C storyboard + P7-5.1 style reference | guide를 수채화 medium으로만 변환 | structure·style. 인물 identity·착장은 이 단계의 평가 대상이 아님. |
| B0 | 원래 Scene C storyboard + 얼굴 + 완성 착장 | 기준선 | structure·identity·outfit·style |
| B1 | A의 stylized guide + 같은 얼굴 + 같은 완성 착장 | guide의 화풍 사전 변환 | structure·identity·outfit·style |

- B0와 B1은 seed `62294`, `62295`를 모두 사용하고, 해상도·step·모델·offload·prompt의 identity·outfit 문장은 고정한다.
- A의 산출물은 B1의 입력 역할을 검증하는 중간 guide이며, 사람 검수 전 승인 스토리보드나 LoRA 입력으로 승격하지 않는다.
- B1에서 두 seed 모두 네 계약을 통과해야만 `새 guide 하나에서의 제한된 재현`으로 기록한다. 한 seed만 통과하거나 구도·화풍 중 하나가 깨지면 후보 실패 원인을 기록하고 다음 변수 하나만 바꾼다.

### guide-first B1의 중단 근거

Stage A seed `62294`는 공중 split leap·분리 그림자·자갈 배경을 남겼지만, 익명 인물이 실사 질감과 검은 의상으로 남았다. 이 중간 guide를 쓴 B1 seed `62294`도 같은 인물을 유지해 얼굴·착장 reference가 인물 교체 역할을 수행하지 못했다. 따라서 B1의 두 번째 seed는 전체 통과 가능성을 판정하는 데 추가 정보가 적어 실행하지 않는다.

다음 가설은 `guide의 인물을 남긴 채 화풍만 바꾸기`가 아니라, 인물 RGB를 포함하지 않는 구조 입력과 별도의 scene medium을 어떻게 제공할지 분리하는 것이다. 이 경로는 새 비교 설계 뒤에만 실행하며, 현재 실패 후보를 승인 자산으로 승격하지 않는다.

### identity-free 구조 guide B2의 교차 seed 결과

P7-5.3 Scene C의 depth map에서 split leap 실루엣만 남기고, 결정적 seed로 만든 수채화 자갈·분리 그림자를 조합했다. 이 guide에는 원본 인물 RGB·얼굴·의상·사진 자갈을 넣지 않았다. 같은 guide, 얼굴 reference, 완성 착장 reference, `40 step`, `true_cfg_scale 4.0`을 고정하고 seed `62294/62295`를 비교했다.

- 두 출력은 청록 턱선 단발, 흰 크롭 재킷, 청록 와이드 바지, 흰 운동화, 남색 crossbody bag과 외부 strap을 유지했다.
- 두 출력 모두 공중 split leap와 그림자를 유지했다. 다만 원래 스토리보드의 사진 질감·세부 자갈 배치는 보존하지 않았고, seed마다 팔·다리와 그림자 형태가 다르다.
- 2026-08-16 검수에서는 seed `62294`, `62295`의 structure·identity·outfit·style이 모두 `통과`로 기록됐다. 그러나 2026-08-17의 seed `62294` 재검수는 **구도만 통과, 캐릭터·소품·화풍 탈락**으로 이 판정을 대체했다. 착장은 이번 재검수에서 별도 판정하지 않았다.
- 따라서 Scene C B2는 더 이상 제한된 교차 seed 통과·재현 가능한 다음 단계 입력 후보로 주장하지 않는다. 원래 Scene C 승인 스토리보드·공통 제작 규칙·LoRA 학습 입력으로 승격하지 않으며, 재사용 전에는 두 seed를 같은 계약표로 다시 검수해야 한다.

## 승인 3입력 direct-depth·화풍 참조 실험 (2026-08-17)

세 장면에 같은 `1280×1280`, `80 step`, seed `62294`를 사용했다. 입력 순서는 **완성 character sheet → 승인 storyboard relative depth → P7-5.1 승인 화풍 이미지**이며, 기존 파생 ControlNet guide와 별도 outfit crop은 쓰지 않았다.

| Scene | 구조 | 캐릭터 | 착장 | 화풍 | 사람 검수 결론 |
| --- | --- | --- | --- | --- | --- |
| A | 탈락 | 탈락 | 탈락 | 탈락 | 협곡·도약·청록 단발·가방은 남았으나, 넓은 고각도 대신 밀집된 근거리 협곡이 됐다. 양쪽 황금 홍채와 회색 이너 셔츠가 확인되지 않고, 선화 중심이라 수채화 계약도 탈락했다. |
| B | 탈락 | 탈락 | 통과 | 통과 | 평지·수평선·여백·도약과 전신 착장·가방 strap, 수채화는 남았다. 그러나 높은 시점·승인 프레이밍이 사라지고 옆얼굴이라 양쪽 황금 홍채를 확인할 수 없다. |
| C | 탈락 | 탈락 | 탈락 | 통과 | overhead split leap·가방·청록 헤어와 수채화는 남았다. 그러나 자갈 바닥·분리된 전신 그림자가 큰 푸른 wash와 무관한 어두운 형태로 대체됐고, 눈·회색 이너 셔츠도 확인되지 않는다. |

- 공통 실행 기록: `storyboard-depth` 직접 참조, character sheet SHA-256 `49f6d2…022`, P7-5.1 atrium style SHA-256 `2ae025…0afa`. prompt 단어 수는 A/B/C 각각 `107/113/114`다.
- A/B/C 모두 가방과 외부 strap은 남았다. 화풍 참조를 세 번째 이미지 역할로 연결하면 B/C의 off-white paper·wash·charcoal contour는 재현 가능했다. 다만 A는 선화 쪽으로 붕괴했다.
- 결론: **승인 3입력 파이프라인은 화풍과 일부 소품 재현을 개선했지만, 세 장면 모두 네 계약을 동시에 통과하지 못했다.** 특히 relative depth를 일반 Edit 참조로 넣는 방식은 카메라·인물 방향·바닥/그림자 세부를 강제하지 못한다. 원본 RGB 조건과 direct-depth 조건을 분리 비교하고, 홍채가 보이는 얼굴 증거를 유지하는 다음 실험이 필요하다.

실행·검수 JSON과 PNG는 `.tmp/p7-5-4-qwen-edit-p753-remaining-scenes/scene-{a,b,c}-approved-three-role-depth-style-1280-steps80-*`에 있다.

## 사람 검수 기록 양식

각 후보에 아래 JSON 필드를 남긴다. `pass`는 사람이 이미지와 대응 입력을 함께 본 뒤에만 쓴다.

```json
{
  "status": "human_review_pending",
  "experiment_id": "p7-5-4-qwen-scene-c-b1",
  "seed": 62294,
  "contracts": {
    "structure": "pending",
    "identity": "pending",
    "outfit": "pending",
    "style": "pending"
  },
  "failure_observations": [],
  "decision": "Do not promote before human review."
}
```

## 재현성 필수 항목

- 모델 ID, Nunchaku rank·정밀도, `nunchaku`·`diffusers`·`torch`·`transformers`·`accelerate` 버전
- 입력 파일 경로와 SHA-256, output SHA-256
- seed, step, 해상도, `true_cfg_scale`, prompt, offload 설정, 소요 시간
- 경고 또는 무시된 설정값과 사람 검수자·검수일

현재 Qwen 스크립트는 패키지 버전·CUDA 상태·입출력 SHA-256을 실행 기록에 남긴다. 이 실험은 RTX 5070 Laptop GPU 환경에서 실행했다.
