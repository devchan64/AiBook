# P7-9.3 Whisper와 MusicGen으로 음성·오디오 모델 입출력 비교하기

> Section ID: `P7-9.3`
> Version: `v2026.07.31`

음성·오디오 모델은 텍스트나 이미지 모델보다 입력과 출력이 눈에 덜 보입니다. 그래서 실습 기록이 더 중요합니다. 이 절에서는 Whisper로 같은 음성을 다른 모델 크기에서 전사하고, MusicGen 계열 모델로 같은 prompt의 음악 생성을 비교하는 확장 실습을 설계합니다.

두 실습은 서로 다른 방향입니다. Whisper는 audio-to-text이고, MusicGen은 text-to-audio입니다. 하지만 둘 다 Part 5와 Part 6에서 배운 시퀀스, 토큰화, 생성, 평가 문제를 다시 확인하게 해 줍니다.

## Whisper 전사 비교

먼저 짧은 음성 파일 하나를 고릅니다. 배경 소음이 거의 없는 파일 하나와, 말이 겹치거나 잡음이 있는 파일 하나를 따로 준비하면 비교가 분명해집니다.

| 비교 축 | 바꿀 값 | 읽어야 할 질문 |
| --- | --- | --- |
| 모델 크기 | tiny, base, small 등 | 모델이 커질수록 누락과 오인식이 줄어드는가 |
| 음성 조건 | 깨끗한 음성, 잡음 있는 음성 | 어떤 조건에서 오류가 늘어나는가 |
| 언어 조건 | 한국어, 영어, 혼합 발화 | 언어 전환에서 오류가 생기는가 |
| 출력 형식 | plain text, timestamp 포함 | 전사 결과를 어디까지 검토할 수 있는가 |

## MusicGen 생성 비교

음악 생성은 정답이 분명하지 않으므로, 감상보다 조건 비교가 먼저입니다.

| 비교 축 | 바꿀 값 | 읽어야 할 질문 |
| --- | --- | --- |
| prompt | 장르, 악기, 분위기 | 어떤 단어가 실제 소리 차이로 이어지는가 |
| duration | 짧은 생성, 긴 생성 | 길이가 늘어날수록 반복이나 붕괴가 생기는가 |
| melody 조건 | 없음, 참조 melody 있음 | 참조 melody가 리듬이나 선율에 반영되는가 |
| seed | 같은 prompt의 seed 변경 | 마음에 드는 결과가 우연인지 반복 가능한지 구분되는가 |

## 최소 실행 예시

Whisper는 명령줄에서 먼저 비교하기 좋습니다. 같은 파일을 작은 모델과 더 큰 모델로 실행하고, 전사 오류를 나란히 적습니다.

```bash
whisper inputs/p7-9-3-clean.wav --model tiny --language Korean
whisper inputs/p7-9-3-clean.wav --model small --language Korean
whisper inputs/p7-9-3-noisy.wav --model small --language Korean
```

Python에서 결과 문장만 확인할 때는 다음처럼 시작할 수 있습니다.

```python
import whisper

model = whisper.load_model("small")
result = model.transcribe("inputs/p7-9-3-noisy.wav", language="ko")
print(result["text"])
```

MusicGen은 같은 prompt에서 duration을 바꾸거나, prompt 문장을 바꾸며 비교합니다.

```python
from audiocraft.data.audio import audio_write
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=8)

prompts = [
    "bright synth pop loop with a steady drum pattern",
    "quiet piano melody with soft ambient texture",
]

wav = model.generate(prompts)

for idx, one_wav in enumerate(wav):
    audio_write(
        f"outputs/p7-9-3-musicgen-{idx}",
        one_wav.cpu(),
        model.sample_rate,
        strategy="loudness",
    )
```

Whisper 결과는 `무엇을 잘못 들었는가`를 보고, MusicGen 결과는 `prompt의 어떤 단어가 실제 소리로 반영되었는가`를 봅니다.

## 기록 양식

```text
run_id:
task_type: speech_to_text / text_to_audio
model:
input_file_or_prompt:
changed_value:
output_file:
observed_result:
failure_seen:
next_trial:
```

Whisper의 `observed_result`에는 `고유명사 누락`, `문장 경계 오류`, `잡음 구간 오인식`처럼 전사 오류를 적습니다. MusicGen의 `observed_result`에는 `악기 반영`, `리듬 반복`, `prompt와 무관한 분위기`처럼 prompt 대비 들리는 차이를 적습니다.

## Part 1~6으로 되돌아가기

| 다시 확인할 개념 | 이 실습에서 보이는 장면 |
| --- | --- |
| Part 3의 입력 단위 | 음성 파일 길이와 구간 분할이 결과 해석을 바꿉니다. |
| Part 5의 시퀀스 모델 | 시간 순서가 있는 입력과 출력은 중간 오류가 뒤 결과에 영향을 줍니다. |
| Part 6의 생성 설정 | 같은 prompt라도 seed와 duration이 생성 결과를 바꿉니다. |
| Part 7의 평가 기록 | 음성·오디오는 감상 대신 오류 유형과 조건 차이를 남겨야 합니다. |

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 음성 입력 | 깨끗한 입력과 어려운 입력을 구분했는가? |
| 모델 조건 | 모델 크기나 생성 조건 중 하나만 바꿨는가? |
| 출력 파일 | 전사 텍스트나 생성 오디오 파일을 남겼는가? |
| 실패 기록 | 누락, 오인식, 반복, prompt 미반영을 구분했는가? |
| 다음 실행 | 다음에 바꿀 조건을 하나로 좁혔는가? |

## 출처와 참고 자료

- OpenAI, [Whisper GitHub 저장소](https://github.com/openai/whisper){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- Meta, [AudioCraft GitHub 저장소](https://github.com/facebookresearch/audiocraft){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
