# 10.2 근거 검토: 다음 출력 생성의 직관

## 검토 목적

10.2는 생성형 AI가 완성된 산출물을 한 번에 꺼내는 것이 아니라, 조건을 바탕으로 산출물을 점진적으로 구성한다는 직관을 설명하는 절이다.

이 절에서는 다음 경계를 둔다.

- 텍스트 생성은 다음 토큰 예측(next-token prediction)과 autoregressive language model 직관으로 설명한다.
- 음성 생성은 WaveNet의 raw audio waveform 생성과 조건부 확률 factorization을 근거로 순차 생성 직관을 설명한다.
- 이미지 생성은 다음 픽셀 예측으로 단순화하지 않는다.
- diffusion model 계열은 노이즈를 점진적으로 복원하는 reverse process로 소개한다.
- sampling, temperature, top-k, top-p, diffusion 수식은 뒤 장으로 넘긴다.

## 확인한 원문

원문 PDF와 추출 텍스트는 `.tmp/section-10-2-evidence/` 아래에 저장했다.

| 자료 | 파일 | 확인 내용 |
| --- | --- | --- |
| Brown et al., GPT-3 | `gpt3-2005.14165.pdf`, `gpt3-2005.14165.txt` | autoregressive language model, predicting what comes next |
| van den Oord et al., WaveNet | `wavenet-1609.03499.pdf`, `wavenet-1609.03499.txt` | raw audio waveform 생성, waveform joint probability를 conditional probability product로 factorization |
| Ho et al., DDPM | `ddpm-2006.11239.pdf`, `ddpm-2006.11239.txt` | denoising diffusion probabilistic model, reverse process |
| Rombach et al., Latent Diffusion Models | `latent-diffusion-2112.10752.pdf`, `latent-diffusion-2112.10752.txt` | latent diffusion, cross-attention conditioning, text-to-image synthesis |

## 자료별 근거 판단

### Brown et al., Language Models are Few-Shot Learners

근거 위치:

- `gpt3-2005.14165.txt` 18행: GPT-3를 175B 파라미터 autoregressive language model로 설명한다.
- 118행: task instance를 보고 what comes next를 예측해 task를 완성하는 설명이 나온다.
- 145행: 175B parameter autoregressive language model을 훈련한다고 설명한다.

본문 반영:

- 텍스트 생성은 앞 문맥을 조건으로 다음 토큰 후보를 계산하고 이어 붙이는 직관으로 설명했다.
- "다음 토큰은 정답 하나가 아니다"라는 혼동 방지 문단을 추가했다.

주의:

- 10.2에서는 GPT-3의 few-shot learning, scaling law, benchmark 결과를 다루지 않는다.
- "next-token prediction"의 sampling 설정은 뒤 장으로 넘긴다.

### van den Oord et al., WaveNet

근거 위치:

- `wavenet-1609.03499.txt` 48행: raw audio waveform을 직접 다루는 generative model을 제안한다고 설명한다.
- 49행: waveform의 joint probability를 conditional probability의 product로 factorization한다고 설명한다.
- 56행 부근: conditional probability distribution을 모델링한다.

본문 반영:

- 음성 생성도 이전 오디오 샘플을 조건으로 다음 오디오 샘플 또는 파형 조각을 생성하는 순차 생성 직관으로 설명했다.
- 텍스트와 음성의 생성 단위가 다름을 표로 구분했다.

주의:

- WaveNet을 LLM의 직접 조상으로 쓰지 않는다.
- 10.2에서는 음성 합성의 세부 네트워크 구조나 TTS 파이프라인을 다루지 않는다.

### Ho et al., Denoising Diffusion Probabilistic Models

근거 위치:

- `ddpm-2006.11239.txt` 68행: reverse process가 learned Gaussian transition을 갖는 Markov chain으로 정의된다고 설명한다.
- 478-479행: reverse process sampling 과정에서 sample quality가 변화하는 과정을 언급한다.
- 518행 부근: reverse process를 사용해 corrupted image를 복원하는 설명이 나온다.

본문 반영:

- 이미지 생성, 특히 diffusion model은 단순한 다음 픽셀 예측이 아니라 노이즈에서 점진적으로 복원하는 과정으로 설명했다.

주의:

- forward process, variational bound, U-Net, noise schedule 수식은 다루지 않는다.
- "이미지는 모두 diffusion으로 생성된다"라고 쓰지 않는다.

### Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models

근거 위치:

- `latent-diffusion-2112.10752.txt` 148행: latent diffusion models를 effective generative model로 제안한다.
- 168-169행: cross-attention 기반 conditioning mechanism으로 text-to-image training에 적용한다고 설명한다.
- 510행: user-defined text prompt로 text-to-image synthesis sample을 제시한다.
- 1602-1610행: text-to-image model에서 conditioning이 cross-attention mechanism을 통해 mapped된다고 설명한다.

본문 반영:

- 텍스트 조건 이미지 생성에서는 text prompt가 조건(condition)으로 사용될 수 있음을 설명했다.
- 이미지 생성은 latent representation과 denoising 과정을 거칠 수 있음을 입문 수준으로만 언급했다.

주의:

- Stable Diffusion 제품명이나 구체적 구현은 이 절에서 다루지 않는다.
- cross-attention의 수식이나 구조는 뒤 Transformer/LLM 장으로 넘긴다.

## 일반화 문구

10.2에서는 다음 문구가 안전하다.

> 생성형 AI는 대체로 조건을 바탕으로 다음 출력 조각을 만들고, 그 결과를 다시 다음 단계의 조건으로 사용하면서 산출물을 구성한다.

단, 이 문구에는 반드시 다음 경계를 붙인다.

> 텍스트 생성은 다음 토큰을 이어 붙이는 설명이 잘 맞지만, 이미지 생성, 특히 diffusion 계열은 노이즈를 점진적으로 복원하는 방식으로 따로 이해해야 한다.

## 도메인 경계

10.2에서 다룬다:

- 다음 출력 생성의 입문용 직관
- 텍스트의 다음 토큰 생성
- 음성의 순차 샘플 생성 직관
- 이미지 diffusion의 점진적 복원 직관
- 사람 검토와 반복 수정 흐름

10.2에서 깊게 다루지 않는다:

- tokenizer와 embedding
- sampling parameter
- Transformer 세부 구조
- diffusion 수식과 U-Net
- prompt engineering
- 생성 결과 평가 지표
