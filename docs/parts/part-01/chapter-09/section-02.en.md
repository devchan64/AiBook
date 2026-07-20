# P1-9.2 Object Detection and Speech Generation Cases

> Section ID: `P1-9.2`
> Version: `v2026.07.20`

Section 9.1 used image recognition and representation learning to show why deep learning became an important turning point. Image classification asked `what is this image?`

This section explains how the deep-learning paradigm spread into other problem types. The first case is `object detection`. The second is `speech generation`. `TTS` appears only as a supporting context connected to WaveNet.

The central question is:

> beyond image classification,  
> how did deep learning reframe problems such as locating objects and generating sound?

> object detection and speech-generation cases are not the direct ancestors of LLMs; they are surrounding evidence that deep learning replaced hand-built pipelines with learned structures across many input and output problems

This section groups `object detection`, `bounding boxes`, `YOLO`, `speech generation`, `WaveNet`, and `TTS` as cases where the deep-learning paradigm expanded into different output structures. The contrast between `image recognition` and `learned representation` was introduced in 9.1, and the boundary from the direct lineage of LLMs is made explicit again in 9.3.

These terms can sound as if they all belong directly to the history of generative AI. A quick separation helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| object detection | finding both what is there and where it is | a case with a more complex output structure than classification |
| bounding box | a rectangle marking an object's location | the basic output form of detection |
| YOLO | a case that treated detection as one prediction problem | a representative end-to-end reframing |
| speech generation | generating audio over time | a case of sequence generation in another domain |
| WaveNet | a model that generated raw audio probabilistically | the representative speech-generation example |
| TTS | turning text into speech | a supporting application context only |

The minimum distinction to keep is:

- detection means `location + category`
- YOLO predicts them together
- WaveNet is sequence generation for audio
- TTS is only a supporting context here

This section does not implement YOLO or WaveNet. Terms such as `mAP`, `dilated convolution`, `autoregressive model`, and `vocoder` appear only by name and role. Systems such as Deep Voice remain supporting examples rather than the main subject.

This section also does not explain these cases as the direct lineage of `LLMs`. The direct line of LLM development belongs elsewhere: statistical language models, word embeddings, RNN/LSTM, Seq2Seq, Attention, Transformers, and pretrained language models.

It also does not repeat the image-recognition case from 9.1. The focus here is `problem reframing`. In other words, how did deep learning expand beyond classification into:

- predicting `location and category together`
- generating `time-ordered waveforms`

The baseline definition here is:

> in image, location, waveform, and speech problems, deep learning widened the use of trainable structures that reduce hand-built features and multi-stage pipelines

## Reading Location Prediction and Sequential Generation

- Understand how object detection differs from image classification.
- Read YOLO as a case that reframed object detection as one neural-network prediction problem.
- Read WaveNet as a case that generated raw audio waveforms with a probabilistic autoregressive approach.
- Understand TTS only as a supporting application context where speech-generation models meet actual speech synthesis.
- Distinguish these cases from the direct lineage of LLMs.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| object detection asks not only `what is present?` but also `where is it?` | This is the quickest way to separate detection from classification. | It is enough to understand that both category and location must be produced. |
| YOLO is a case that bundled many detection stages into one prediction problem | This shows how deep learning restructured pipelines. | It is enough to know that candidate finding and classification were pulled into a single learned system. |
| speech-generation cases such as WaveNet are surrounding evidence, not direct LLM ancestors | This keeps the historical flow from being mixed together. | It is enough to understand them as evidence that deep learning spread into many output problems. |

## Classification and Detection Are Different

`Image classification` usually predicts a category for the image as a whole.

> input: one image  
> output: a category such as cat, car, or person

`Object detection` is harder by one step. It asks not only what exists in the image, but also where it exists.

> input: one image  
> output: object category + location

For a road photo:

| Problem | Question | Output |
| --- | --- | --- |
| image classification | what kind of scene is this image? | road, intersection, parking lot |
| object detection | what objects are in the image, and where are they? | locations of cars, people, signs |

The location is usually represented by a `bounding box`, a rectangle that marks the area occupied by the object inside the image.

Object detection therefore has a more complex output structure than image recognition. Several objects may exist at once, and each one needs both a category and a location. That is why older detection systems often used multi-stage pipelines: generate candidate regions, extract features, apply classifiers, and then refine positions.

## YOLO Reframed Detection as One Prediction Problem

`YOLO` is a representative case that reframed object detection as a prediction problem for a single neural network. Redmon, Divvala, Girshick, and Farhadi explain that while earlier object detectors often reused classifiers for detection, YOLO treats detection as a `regression problem` that predicts bounding boxes and class probabilities directly.

At the introductory level, the key shift is:

| View | Traditional detection pipeline | YOLO's view |
| --- | --- | --- |
| problem setup | candidate-region search, feature extraction, classification, box refinement | predict bounding boxes and class probabilities from the image in one shot |
| optimization | multiple stages need separate adjustment | the whole structure can be trained end to end |
| strength | stages can be easier to inspect separately | faster processing and a simpler integrated structure |
| caution | full-system tuning can become complex | small objects and precise localization may still be harder |

The YOLO paper explains that one neural network predicts both bounding boxes and class probabilities directly from the full image. Because the pipeline is a single network, it can be optimized end to end. The original paper also emphasized real-time processing.

The important point is not only `it was fast`. The deeper shift is:

> detection was no longer treated only as a chain of hand-built steps;  
> it was reframed as one trainable prediction problem

That reflects the wider deep-learning pattern. In 9.1, the model learned image representations. In YOLO, the same pattern expands into a problem where the model must answer both `what is it?` and `where is it?`

## Speech Generation Can Be Seen as Predicting the Next Sample

Images have spatial structure. Speech has temporal structure. Speech is a signal that records changes in air pressure over time, and digital audio stores it as a sequence of samples.

If we simplify `speech generation`, the question becomes:

> given the audio samples so far,  
> how should we generate the next audio sample?

This connects to the intuition of `generation` that Chapter 10 develops later. Text generation predicts the next token from previous tokens. Audio generation can predict the next sample from previous samples. Of course, text and audio have different data structures, so they are not `the same model`. The shared intuition here is only `sequential output generation`.

## WaveNet Is a Case of Generating Raw Audio Directly

`WaveNet` is a raw-audio generation model introduced by DeepMind. van den Oord and colleagues describe WaveNet as a deep neural network that generates raw audio waveforms and as a fully probabilistic autoregressive model.

Here, `raw audio waveform` means the model operates close to the actual audio signal over time rather than only over predesigned acoustic features. WaveNet models the joint probability of the waveform by factorizing it into conditional predictions of the next sample given the previous ones.

The introductory baseline is:

> WaveNet did not treat speech only as small prerecorded units to stitch together;  
> it treated the waveform itself as a probabilistic sequence-generation problem

The WaveNet paper reports that when applied to TTS, it produced more natural speech than earlier statistical parametric systems and concatenative systems. It also notes that raw audio is a high-resolution time signal, often involving at least 16,000 samples per second, so long-range temporal dependencies matter.

The shift it shows can be summarized like this:

| Earlier view | What WaveNet demonstrated |
| --- | --- |
| speech handled through hand-designed features, vocoders, or unit selection | the waveform itself becomes the target of generation |
| many assumptions and hand-built pipeline stages | the neural network learns temporal dependencies and predicts the next sample |
| limited naturalness in some previous approaches | raw-audio generation opened the possibility of more natural sound |

WaveNet is not an LLM. But it is a strong example of the idea:

> generate the next output sequentially

in the domain of audio waveforms.

## TTS Appears Only as Supporting Context

`TTS` is an important field, but it is not the main subject of this section. In 3.1, TTS briefly appeared as an area where rule-based processing had also worked successfully. Here, we only keep the narrower point that WaveNet showed the possibility of raw-audio generation when applied to speech synthesis.

Neural TTS systems such as Deep Voice can be read as cases where components of older TTS pipelines were replaced by neural-network-based components. But going deep into that would turn 9.2 into a history of speech synthesis, which is not the goal here. So the safer summary is:

> TTS is not the central case in this section.  
> It only helps confirm that parts of speech-synthesis pipelines also shifted toward neural-network components.

## What These Cases Share

YOLO and WaveNet solve different problems:

| Case | Domain | Input | Output | Shift it demonstrated |
| --- | --- | --- | --- | --- |
| YOLO | object detection | image | object location and category | detection reframed as one neural-network prediction problem |
| WaveNet | speech generation | previous audio samples and optional conditions | next audio sample | raw audio modeled as probabilistic sequence generation |

The common point is not `deep learning solved every problem in one universal way`. The safer generalization is:

> across many domains, deep learning strengthened the move from hand-designed features, candidate generation, rules, and fixed pipelines toward trainable neural-network structures

This appeared differently in image classification, object detection, and speech generation. TTS is the supporting application context where that shift met real speech-synthesis systems. All of them also connect back to the AlexNet case in 9.1 because they became powerful when large data, compute, model structure, and training methods came together.

## Distinguishing These Cases from the Direct Lineage of LLMs

The cases in this section are not the direct lineage of LLMs.

> YOLO -> LLM  
> WaveNet -> LLM  
> TTS system -> LLM

Writing the history that way creates confusion. YOLO belongs to object detection. WaveNet belongs to raw-audio generation. TTS systems belong to speech synthesis. The direct lineage of LLMs should be explained through language modeling, sequence modeling, Seq2Seq, Attention, Transformers, and pretraining.

Still, these cases show an important background:

> deep learning was not a trend limited to one field;  
> it spread across image, location, speech, and language problems through representation learning and end-to-end trainable structures

Seen that way, LLMs do not look like a technology that appeared from nowhere. Their direct lineage is different, but the broader credibility of that lineage grew in part because deep learning had already shown repeated success across many domains during the 2010s.

## Checklist

- I can explain how object detection differs from image classification.
- I can describe YOLO as a case that reframed object detection as a single neural-network prediction problem.
- I can describe WaveNet as a case that generated raw audio waveforms probabilistically and sequentially.
- I can keep TTS as a supporting context rather than the main subject of 9.2.
- I do not treat YOLO, WaveNet, or TTS systems as the direct lineage of LLMs.
- I can explain whether the task asks both `what` and `where`, or whether the output is a time-ordered audio signal.
- I can read each case as `surrounding evidence` rather than `direct lineage`, without overstating the historical connection.

## Sources and Further Reading

- Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi, [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640){: target="_blank" rel="noopener noreferrer" }, arXiv, 2015, accessed 2026-06-23.
- Aaron van den Oord et al., [WaveNet: A Generative Model for Raw Audio](https://arxiv.org/abs/1609.03499){: target="_blank" rel="noopener noreferrer" }, arXiv, 2016, accessed 2026-06-23.
- Sercan O. Arik et al., [Deep Voice: Real-time Neural Text-to-Speech](https://arxiv.org/abs/1702.07825){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, accessed 2026-06-23. Supporting TTS example.
