# P5-15.5 디퓨전 모델에서 attention과 Transformer는 무엇을 맡는가

> Section ID: `P5-15.5`
> Version: `v2026.08.28`

P5-15.4에서는 디퓨전 모델이 노이즈가 섞인 상태와 시간 단계를 입력으로 받아, 노이즈 또는 복원 방향을 예측하도록 학습된다는 점을 보았습니다. 이제 남는 질문은 **텍스트 조건은 반복 복원에 어디서 들어가며, attention과 Transformer는 그 복원 계산에서 무엇을 맡을 수 있는가**입니다.

## 조건은 복원 과정에 방향을 더한다

텍스트 조건이 있는 디퓨전 모델에서는 단순히 `노이즈를 줄여라`만으로 충분하지 않습니다. `어떤 장면`, `어떤 물체`, `어떤 분위기`에 가까워져야 하는지도 반복 복원에 들어가야 합니다. 조건 인코더는 텍스트나 참조 입력을 계산 가능한 표현으로 바꾸고, 복원 네트워크는 현재 노이즈 상태·시간 단계·조건 표현을 함께 참고합니다.

```mermaid
--8<-- "assets/part-05/chapter-15/diffusion-conditioning-structure-ko.mmd"
```

이 도식의 핵심은 프롬프트가 픽셀 배치표가 아니라는 점입니다. 조건은 매 복원 단계에서 참고하는 방향이고, 초기 노이즈와 복원 경로는 여전히 결과 변주에 영향을 줍니다.

## self-attention과 cross-attention은 다른 연결을 다룬다

attention이라는 이름이 같아도 무엇과 무엇을 연결하는지에 따라 역할이 다릅니다.

| 구조 | 먼저 보는 연결 | 디퓨전에서의 역할 감각 |
| --- | --- | --- |
| self-attention | 이미지 잠재 표현의 위치·패치와 다른 위치·패치 | 멀리 떨어진 부분도 함께 참고하며 전역 관계를 반영할 수 있다 |
| cross-attention | 현재 이미지 잠재 표현과 텍스트 같은 조건 표현 | 현재 복원 단계가 조건의 어떤 부분을 참고할지 연결할 수 있다 |

예를 들어 `왼쪽에 붉은 우산을 든 사람`이라는 조건을 처리할 때, cross-attention은 텍스트 조건과 이미지 상태의 연결을 설명하는 데 가깝습니다. 반면 사람·우산·배경의 서로 떨어진 위치 관계를 함께 고려하는 것은 self-attention의 감각에 더 가깝습니다. 실제 모델은 여러 계산을 함께 쓰지만, 두 역할을 하나의 `attention이 이미지를 잘 만든다`는 말로 뭉뚱그리면 조건 처리와 이미지 내부 관계를 구분할 수 없습니다.

## U-Net과 DiT는 복원 네트워크의 서로 다른 선택이다

디퓨전 알고리즘이 복원 네트워크의 이름을 정하지는 않습니다. 어떤 네트워크든 현재 노이즈 상태, 시간 단계, 조건을 받아 노이즈 또는 복원 방향을 예측할 수 있다면 그 자리를 맡을 수 있습니다.

```mermaid
--8<-- "assets/part-05/chapter-15/diffusion-denoiser-comparison-ko.mmd"
```

| 관점 | U-Net 기반 복원기 | Transformer/DiT 기반 복원기 |
| --- | --- | --- |
| 주된 처리 단위 | 해상도를 줄이고 늘리는 특징 맵과 지역 연산 | 잠재 표현을 나눈 패치·토큰과 attention 블록 |
| 조건·시간 입력 | 단계별 특징 계산에 조건과 시간 정보를 반영 | 패치 표현과 조건 표현을 Transformer 계산에 반영 |
| 공통 역할 | 현재 상태에서 노이즈 또는 복원 방향을 예측 | 현재 상태에서 노이즈 또는 복원 방향을 예측 |

이 표는 어느 구조가 항상 더 좋다는 순위표가 아닙니다. P5-14에서 배운 Transformer는 언어 토큰만 처리하는 구조가 아니라, 적절한 입력 표현과 조건 연결을 갖추면 디퓨전의 복원 네트워크로도 쓰일 수 있다는 점을 보여 줍니다.

## latent diffusion은 계산 공간을 바꾸는 선택이다

픽셀 이미지 전체에서 매 단계 복원 계산을 하면 비용이 큽니다. latent diffusion은 VAE encoder로 이미지를 더 압축된 latent 표현으로 바꾼 뒤 그 공간에서 주된 디퓨전 계산을 수행하고, 마지막에 VAE decoder로 사람이 볼 픽셀 이미지로 돌립니다.

| 구성요소 | 역할 | 모든 디퓨전 모델에 항상 필요한가 |
| --- | --- | --- |
| VAE encoder/decoder | 이미지와 압축된 latent 표현을 오간다 | 아니다. latent diffusion에서 계산 비용을 줄이기 위한 선택이다 |
| 조건 인코더 | 텍스트·참조 입력을 조건 표현으로 바꾼다 | 조건부 생성에서는 필요하지만 조건 종류와 구조는 달라질 수 있다 |
| 복원 네트워크 | 노이즈 또는 복원 방향을 예측한다 | 디퓨전 생성의 핵심 역할이지만 U-Net 하나로 고정되지 않는다 |
| scheduler | 다음 복원 상태를 계산한다 | 학습된 네트워크와 구분해야 하는 생성 절차의 규칙이다 |

따라서 Stable Diffusion은 latent diffusion, VAE, text condition, U-Net 계열 복원기를 결합한 대표 사례로 읽을 수 있습니다. 그러나 이 사례의 부품 목록을 디퓨전 모델 전체의 정의로 쓰면 안 됩니다.

## 다음 Part에서 이어질 비교

Part 6의 P6-1.4에서는 텍스트 LLM이 다음 토큰을 순차로 선택하는 생성과, 디퓨전 모델이 전체 노이즈 상태를 반복 복원하는 생성을 비교합니다. 여기서 남길 기준은 간단합니다. **디퓨전은 생성 절차이고, attention과 Transformer는 그 절차 안에서 조건과 관계를 처리할 수 있는 구조 선택이다.**

## 체크리스트

- 조건 인코더, 현재 노이즈 상태, 복원 네트워크, 생성 결과의 연결을 설명할 수 있다.
- self-attention과 cross-attention이 각각 무엇을 연결하는지 구분할 수 있다.
- U-Net과 DiT를 서로 다른 복원 네트워크 선택으로 설명할 수 있다.
- latent diffusion의 VAE가 디퓨전 모델 일반의 필수 부품은 아니라는 점을 설명할 수 있다.
- scheduler와 학습된 복원 네트워크의 역할을 다시 구분할 수 있다.

## 출처와 참고 자료

- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, 확인 날짜: 2026-08-28. latent space, VAE, cross-attention 조건부 생성의 근거로 사용했다.
- William Peebles, Saining Xie, [Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023, 확인 날짜: 2026-08-28. U-Net 대신 잠재 패치를 처리하는 Transformer/DiT 기반 복원기를 설명하는 근거로 사용했다.
