# P7-5.8 보충학습: OpenPose로 동작과 구도 조건 비교하기

> Section ID: `P7-5.8`
> Version: `v2026.09.11`

캐릭터의 옷과 얼굴을 유지하면서 팔을 올리거나 다리를 교차하게 만들려면, 원하는 동작을 어떻게 전달해야 할까? [P7-5.3](section-03.md)의 캐릭터 편집과 [P7-5.5](section-05.md)의 장면 합성에 이어, 이 보충학습에서는 **관절 배치를 그림으로 주었을 때 생성 결과가 무엇을 따르는지** 살펴본다. SDXL·ControlNet으로 만든 기존 비교 결과를 읽으며 동작, 외형, 카메라 구도를 구분한다.

## 관절 맵을 만들고 ControlNet으로 전달한다

OpenPose는 이미지에서 사람의 관절 위치를 추정하는 도구다. 이 절의 **OpenPose 맵**은 그 위치를 점으로 표시하고, 어깨·팔꿈치·손목처럼 연결된 부위를 선으로 이은 2D 그림을 뜻한다. 점과 선을 직접 배치해 원하는 동작의 맵을 만들 수도 있다. [OpenPose 공식 구현](https://github.com/CMU-Perceptual-Computing-Lab/openpose){: target="_blank" rel="noopener noreferrer" }

이미지 생성에서는 이 맵을 **ControlNet**에 입력한다. ControlNet은 관절 맵이나 윤곽선 같은 추가 조건을 생성 모델에 전달한다. 여기서는 SDXL 계열 모델이 인물을 그릴 때 관절 배치를 참고하도록 사용했다. 관절 위치를 찾는 OpenPose와, 그 맵을 생성 조건으로 사용하는 ControlNet의 역할을 구분하면 입력 흐름을 이해하기 쉽다. [ControlNet 공식 구현](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }

| 입력 | 이 실험에서 맡긴 역할 |
| --- | --- |
| 관절 맵 | 화면 안에서 팔·다리를 놓을 위치 전달 |
| 캐릭터 LoRA·얼굴 참조 | 인물의 외형 반영 |
| 프롬프트 | 인물과 장면을 말로 지정 |
| 배경 윤곽선 | 뒤의 고각도 사례에서 공간의 선과 배치 전달 |

예를 들어 손목 점을 어깨보다 위에 놓으면 팔을 든 동작을 요구할 수 있다. 하지만 같은 점 배치에 짧은 소매를 그릴지 긴 소매를 그릴지는 관절 맵만으로 정해지지 않는다. 아래 비교에서는 먼저 관절 배치를 보고, 옷과 얼굴은 그다음에 살펴본다.

## 동작 배치에 효과가 있었던 결과

### 다리 교차와 팔 올리기

아래 그림의 왼쪽은 저장한 관절 맵, 가운데는 ControlNet을 끈 결과, 오른쪽은 켠 결과다. 관절 조건의 강도를 `0.0`에서 `1.0`으로 바꾸고 나머지 생성 조건을 고정했다.

![저장 우측 쿼터 OpenPose map과 ControlNet off/on 산출물](../../../assets/part-07/chapter-05/p7-5-11-openpose-static-quarter-right-contact-sheet.png)

맵에는 두 다리가 교차하는 배치가 있다. 가운데 인물은 두 발로 나란히 서 있지만, 오른쪽 인물은 다리를 교차하고 한쪽 발을 들어 맵의 배치에 더 가까워졌다. 동시에 재킷 소매와 가방의 형태도 달라졌다. **동작이 맵에 가까워진 정도와 외형이 유지된 정도는 별개의 관찰**이다.

직접 점을 배치한 팔 올리기 맵도 같은 방식으로 비교했다.

![선언형 OpenPose map ControlNet off/on](../../../assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-controlnet-ab-contact-sheet.png)

이 결과에서는 ControlNet을 켰을 때 팔이 맵의 방향을 더 따랐다. 두 비교에서 무릎·발목 또는 어깨·팔꿈치·손목을 순서대로 짚어 보면, 막연히 “자세가 비슷하다”는 인상보다 어느 부위가 반영됐는지 구체적으로 볼 수 있다.

저장 맵 비교는 Animagine XL, `960×1440`, 30스텝, seed `62296`, 캐릭터 LoRA 강도 `0.6`에서 실행했다. 각 비교의 전체 설정은 아래 기록에 있다.

[저장 관절 맵 비교 기록 — JSON](/AiBook/assets/part-07/chapter-05/p7-5-11-openpose-static-quarter-right-report.json)

[팔 올리기 맵 비교 기록 — JSON](/AiBook/assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-controlnet-ab-report.json)

## 외형과 구도 반영이 부족했던 결과

### 얼굴과 착장이 함께 유지되지 않았다

이번에는 얼굴 참조와 캐릭터 LoRA를 함께 사용하는 전신 생성에서 OpenPose 조건을 끄고 켰다.

![SDXL 전신 safe-face 조건의 OpenPose off/on 비교](../../../assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-openpose-ab-contact-sheet.png)

![SDXL safe-face 전신 후보와 기준 얼굴 비교](../../../assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-contact-sheet.png)

다리·몸통의 배치가 맵에 가까워진 결과에서도 머리 길이와 복장이 달라졌다. 얼굴이 자연스럽게 그려졌는지와 기준 인물의 얼굴인지도 구분해야 한다. 청록 단발, 재킷, 와이드 바지, 가방을 각각 비교하면 자세의 개선만으로 캐릭터 전체가 유지됐다고 판단하기 어려운 이유가 드러난다.

이 비교는 Plus Face 얼굴 참조 강도 `0.15`, 캐릭터 LoRA 강도 `0.30`, seed `62295`, CFG `5.0`, `960×1440`, 50스텝을 고정했다. FaceID와 전신 착장 이미지 어댑터는 사용하지 않았다.

[전신 생성 — OpenPose 끔 실행 기록 — JSON](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-without-openpose-960x1440-result.json)

[전신 생성 — OpenPose 켬 실행 기록 — JSON](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-safe-face-with-openpose-960x1440-result.json)

### 카메라 문구만으로 고각도 구도가 만들어지지 않았다

팔을 올리는 동작을 그대로 두고, 위에서 내려다보는 시점인 `high-angle`을 프롬프트에 추가했다.

![선언형 OpenPose map에서 카메라 문구를 바꾼 비교](../../../assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-camera-ab-contact-sheet.png)

이 비교에서는 문구를 추가해도 기대한 고각도 원근이 나타나지 않았다. 이 절의 2D 관절 맵에는 카메라 높이나 관절의 깊이 값이 별도로 들어 있지 않다. 점 배치에서 시점의 단서를 추정할 수는 있어도, 그것만으로 카메라 위치나 팔·몸통의 앞뒤 관계가 하나로 정해지지는 않는다.

[카메라 문구 비교 기록 — JSON](/AiBook/assets/part-07/chapter-05/p7-5-11-openpose-declarative-reach-up-camera-ab-report.json)

### 배경 원근은 일부 남았지만 인물과 동작이 달라졌다

다음 실험에서는 위에서 내려다본 공간을 가진 안내 이미지(guide)를 먼저 만들었다. 아래 이미지는 Animagine으로 만든 익명 인물의 고각도 장면이다.

![익명 인물로 만든 고각도 보행 guide](../../../assets/part-07/chapter-05/p7-5-11-experimental-animagine-high-angle-guide.png)

이 이미지에서 인물의 관절 배치와 배경의 윤곽선을 따로 준비했다. **Canny**는 이미지의 경계를 선으로 나타내는 방식이다. 여기서는 인물을 제외한 배경 Canny로 공간의 원근 단서를 주고, OpenPose 맵으로 동작을 주었다. 안내 이미지의 얼굴·옷 색을 그대로 전달하는 입력은 사용하지 않았다.

![익명 guide·OpenPose·인물 제외 배경 Canny와 SDXL Mira 전이 후보](../../../assets/part-07/chapter-05/p7-5-11-sdxl-anonymous-high-angle-transfer-review-sheet.png)

| SDXL에 준 구조 조건 | 이 실험에서 관찰한 결과 |
| --- | --- |
| 없음 | 기대한 고각도 구도가 사라짐 |
| OpenPose만 사용 | 위쪽 시점의 단서는 일부 남았지만 동작이 앉거나 쪼그린 자세로 바뀜 |
| 배경 Canny만 사용 | 타일 원근은 남았지만 인물 실루엣이 중복됨 |

단일 조건 비교는 SDXL Base 1.0, 캐릭터 LoRA 강도 `0.6`, seed `62431`, 50스텝, `768×1152`로 실행했다. 배경의 타일 원근이 남은 것은 부분적인 효과지만, 목표한 인물과 동작을 함께 반영한 장면은 얻지 못했다.

두 ControlNet을 함께 사용한 추가 실행은 당시 8GB GPU의 순차 CPU 오프로딩 경로에서 완료되지 않았다. 이 사례는 출력이 없으므로 위 표의 품질 비교에 포함하지 않는다.

[고각도 장면 전이 실행 결과 — JSON](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-anonymous-high-angle-transfer-result.json)

[고각도 장면 전이 비교 조건 — JSON](/AiBook/assets/part-07/chapter-05/p7-5-11-sdxl-anonymous-high-angle-transfer-report.json)

이 사례들에서 효과가 확인된 부분은 다리 교차와 팔 올리기의 2D 배치다. 얼굴·착장 유지와 고각도 장면 구성은 목표에 미치지 못했다. 따라서 결과를 비교할 때도 동작 반영과 캐릭터·장면 전체의 재현을 따로 판단한다.

## 체크리스트

- [ ] 관절 맵을 만드는 OpenPose와 이를 생성 조건으로 쓰는 ControlNet의 역할을 설명할 수 있는가?
- [ ] 비교 이미지에서 동작이 반영된 부분과 외형이 달라진 부분을 각각 하나씩 찾을 수 있는가?
- [ ] 2D 관절 배치만으로 카메라 위치와 앞뒤 가림을 확정하기 어려운 이유를 설명할 수 있는가?

## 출처와 참고 자료


- Stability AI, [SDXL Generative Models](https://github.com/Stability-AI/generative-models){: target="_blank" rel="noopener noreferrer" }, GitHub, 확인일: 2026-08-16.
- Cagliostro Research Lab, [Animagine XL 4.0 모델 카드](https://huggingface.co/cagliostrolab/animagine-xl-4.0){: target="_blank" rel="noopener noreferrer" }, Hugging Face, 확인일: 2026-08-16.
- Cao et al., [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose){: target="_blank" rel="noopener noreferrer" }, GitHub, 확인일: 2026-09-11.
- Hu et al., [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685){: target="_blank" rel="noopener noreferrer" }, arXiv, 확인일: 2026-08-16.
- Zhang et al., [ControlNet](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }, GitHub, 확인일: 2026-09-11.
