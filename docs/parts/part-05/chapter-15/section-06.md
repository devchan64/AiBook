# P5-15.6 VAE는 이미지를 어떤 잠재 표현으로 바꾸는가

> Section ID: `P5-15.6`
> Version: `v2026.08.28`

P5-15.4의 디퓨전은 노이즈 상태를 반복해서 복원하는 알고리즘이고, P5-15.5의 U-Net·DiT는 그 복원 방향을 예측하는 네트워크 선택입니다. latent diffusion에서는 그 반복 계산을 픽셀이 아니라 latent 표현에서 수행합니다. 이때 이미지와 latent 표현 사이를 잇는 장치가 VAE(variational autoencoder, 변분 오토인코더) 계열입니다.

이 절의 질문은 **VAE는 일반 autoencoder와 무엇이 다르고, 왜 생성에 쓸 수 있는 latent 공간을 만들며, latent diffusion에서는 어느 계산을 맡는가**입니다.

## autoencoder는 다시 만들 수 있는 표현을 배운다

일반 autoencoder는 입력 이미지 `x`를 encoder가 보통 더 압축된 표현 `z`로 바꾸고, decoder가 `z`에서 원래와 비슷한 이미지 `x_hat`를 다시 만들도록 학습합니다. 핵심 신호는 입력과 복원 결과의 차이입니다. 다만 latent 표현이라는 말이 항상 차원 수가 더 작다는 뜻은 아닙니다. 여기서는 반복 생성 계산에 쓰기 좋은 표현 공간이라는 역할을 먼저 봅니다.

| 구성요소 | 하는 일 | 이 절에서 먼저 볼 기준 |
| --- | --- | --- |
| encoder | 이미지 `x`를 latent 표현 `z`로 바꾼다 | 어떤 정보를 더 작은 표현에 남길까 |
| latent 표현 | encoder가 남긴 중간 좌표 | 비슷한 입력이 어떤 방식으로 모일까 |
| decoder | `z`를 이미지 `x_hat`로 복원한다 | 남긴 정보로 원래 장면을 얼마나 되살릴까 |
| 재구성 손실 | `x`와 `x_hat`의 차이를 잰다 | 입력을 잃지 않도록 하는 학습 신호 |

이 구조만으로도 입력을 복원하는 표현은 배울 수 있습니다. 하지만 encoder가 만든 latent 좌표들이 흩어져 있거나 빈 곳이 많으면, 임의의 좌표 하나를 골라 decoder에 넣었을 때 자연스러운 이미지를 만들기 어렵습니다. **복원 잘하기**와 **새 좌표에서 생성하기**는 같은 요구가 아닙니다.

## VAE는 좌표 하나 대신 분포를 만든다

VAE의 encoder는 이미지마다 latent 좌표 하나를 바로 내놓는 대신, 그 이미지에 대응하는 분포의 평균 `mu`와 퍼짐 `sigma`를 예측합니다. 이 분포에서 샘플한 `z`를 decoder에 넣어 복원합니다.

```mermaid
--8<-- "assets/part-05/chapter-15/vae-latent-diffusion-flow-ko.mmd"
```

| VAE에서 나오는 값 | 뜻 | 흔한 오해 |
| --- | --- | --- |
| `mu` | 이 입력이 놓일 latent 분포의 중심 | 완성 이미지를 뜻하는 값이 아니다 |
| `sigma` | 중심 주변의 퍼짐 정도 | 품질 점수나 노이즈 예측값이 아니다 |
| `z` | `mu`, `sigma`, 무작위값으로 만든 latent 샘플 | 디퓨전의 시간 단계별 노이즈 상태와 같은 말이 아니다 |
| `x_hat` | decoder가 `z`에서 복원한 이미지 | 디퓨전 모델의 최종 생성 결과와 항상 같지는 않다 |

학습 중에는 보통 다음처럼 표준 정규분포에서 뽑은 `epsilon`을 이용해 `z`를 만듭니다.

\[
z = \mu + \sigma \odot \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I)
\]

이 표현은 무작위 샘플링을 하면서도 `mu`와 `sigma`를 만드는 encoder까지 손실의 영향을 전달하기 위한 재매개변수화(reparameterization) 감각입니다. 여기서 `epsilon`은 VAE의 latent 샘플을 만들 때 쓰는 난수이며, P5-15.4에서 시간 단계별 이미지 상태에 섞던 디퓨전 노이즈와 역할·위치가 다릅니다.

## 재구성과 KL 손실은 서로 다른 요구를 지킨다

VAE 학습은 대략 재구성 손실과 KL divergence 항을 함께 봅니다.

\[
L = L_{reconstruction} + D_{KL}\bigl(q(z\mid x)\;||\;\mathcal{N}(0, I)\bigr)
\]

수식을 외우기보다 두 항이 막는 실패를 구분하는 것이 중요합니다.

| 손실 항 | 줄이려는 문제 | 너무 약하거나 강할 때의 위험 |
| --- | --- | --- |
| 재구성 손실 | decoder가 입력의 중요한 내용·구조를 잃는 문제 | 너무 약하면 복원이 흐려지고, 너무 강하면 좌표들이 불규칙하게 흩어질 수 있다 |
| KL divergence | 입력마다 제각각인 latent 분포가 표준 정규분포와 너무 멀어지는 문제 | 너무 강하면 복원에 필요한 정보가 줄어들 수 있다 |

KL 항은 모든 이미지의 latent 표현을 한 점에 몰아넣는 규칙이 아닙니다. 서로 다른 입력의 분포가 완전히 제각각 흩어지지 않도록, 생성에서 샘플할 기준 분포와 연결하는 제약입니다. 그래서 VAE는 `압축 도구`일 뿐 아니라, 주변 좌표도 해석 가능한 latent 공간을 만들려는 생성 모델입니다.

## latent diffusion에서 VAE와 디퓨전은 다른 단계다

latent diffusion은 VAE가 만든 latent 표현에서 디퓨전의 노이즈 예측·반복 복원을 수행합니다. VAE는 이미지 표현을 오가고, 디퓨전 복원 네트워크는 그 latent 상태에서 노이즈 방향을 예측합니다.

| 단계 | 주된 모델 | 입력에서 출력으로 | 맡는 질문 |
| --- | --- | --- | --- |
| latent 인코딩 | VAE encoder | 이미지 `x` -> latent `z` | 이미지를 계산하기 쉬운 표현으로 어떻게 옮길까 |
| latent 생성 | 디퓨전 복원기와 scheduler | 노이즈 latent -> 복원 latent | 현재 단계에서 무엇을 제거하며 다음 상태로 갈까 |
| 이미지 복호화 | VAE decoder | 최종 latent -> 이미지 | latent 결과를 사람이 볼 이미지로 어떻게 바꿀까 |

따라서 VAE는 디퓨전의 scheduler도, U-Net·DiT 같은 노이즈 예측기도 아닙니다. 또한 모든 디퓨전 모델이 VAE를 써야 하는 것도 아닙니다. 픽셀 공간에서 직접 디퓨전을 수행하는 모델도 있고, latent diffusion은 반복 계산의 대상 공간을 바꾸는 한 가지 설계입니다.

## 작은 비교로 경계를 확인하기

다음 문장을 보고 어느 부품의 역할인지 연결해 보세요.

| 설명 | 연결할 부품 | 확인 해설 |
| --- | --- | --- |
| `이미지를 latent 표현으로 바꾼다` | VAE encoder | 디퓨전 반복 전의 표현 변환이다 |
| `현재 noisy latent에서 노이즈를 예측한다` | U-Net 또는 DiT | 디퓨전의 복원 방향 예측이다 |
| `예측을 이용해 다음 latent 상태를 계산한다` | scheduler | 학습된 가중치가 아니라 생성 경로 규칙이다 |
| `마지막 latent를 픽셀 이미지로 바꾼다` | VAE decoder | 생성 결과를 사람이 보는 형식으로 바꾸는 단계다 |

이 네 문장을 구분할 수 있으면 `VAE가 이미지를 만든다` 또는 `디퓨전이 VAE를 학습한다`처럼 서로 다른 계산을 한 덩어리로 말하는 오해를 피할 수 있습니다.

## 체크리스트

- autoencoder가 encoder·latent 표현·decoder·재구성 손실로 입력 복원을 학습한다는 점을 설명할 수 있다.
- VAE encoder가 좌표 하나가 아니라 `mu`와 `sigma`로 latent 분포를 만든다는 점을 설명할 수 있다.
- 재구성 손실과 KL divergence가 각각 어떤 요구를 지키는지 구분할 수 있다.
- VAE의 `epsilon`과 디퓨전의 시간 단계별 노이즈를 같은 역할로 섞지 않을 수 있다.
- latent diffusion에서 VAE encoder, 디퓨전 복원기·scheduler, VAE decoder의 역할을 나누어 설명할 수 있다.

## 출처와 참고 자료

- Diederik P. Kingma, Max Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114){: target="_blank" rel="noopener noreferrer" }, ICLR, 2014, 확인 날짜: 2026-08-28. 변분 하한, 재매개변수화, approximate posterior를 학습하는 VAE의 근거로 사용했다.
- Robin Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752){: target="_blank" rel="noopener noreferrer" }, CVPR, 2022, 확인 날짜: 2026-08-28. pretrained autoencoder의 latent 공간에서 디퓨전을 수행하는 설계의 근거로 사용했다.
