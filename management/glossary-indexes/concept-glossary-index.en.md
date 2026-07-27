# 영어 개념사전 인덱스

이 파일은 영어 표준 용어, 약어, 원문 레퍼런스 표제어를 `docs/reference/concept-glossary-terms/`의 단어별 원고으로 연결하는 보조 인덱스다.

정의는 이 파일에 중복 작성하지 않는다. 대표 정의는 단어별 원고 파일과 해당 `중심 Section`을 기준으로 확인한다.

| Index Term | Representative Entry | English Base Term | Core Section | File Slug | Anchor | Verification Reference | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| action | action | action | P1-8.3 | action | action | P1-14.3 source context | Execution unit an agent or system chooses to perform in a state |
| actual target | actual target | actual target | P3-9.9 | actual-target | actual-target | P3-9.9 source context | Result the problem truly wants to know, reduce, or predict |
| algorithm | algorithm | algorithm | P4-3.1 | algorithm | algorithm | AIMA, P4-3.1 source context | Defined step-by-step procedure for solving a problem |
| baseline | baseline | baseline | P3-7.3 | baseline | baseline | BLS base period, NCI baseline context | Reference point used to read a current value or model score by comparison rather than in isolation |
| baseline model | baseline model | baseline model | P4-8.2 | baseline-model | baseline-model | P4-8.2 source context | Simplest comparison model or score that candidate models should beat |
| comparability | comparability | comparability | P3-2.3 | comparability | comparability | P3-2.3 source context | Degree to which values, samples, models, or conditions can be interpreted on the same basis |
| cross-validation | cross-validation | cross-validation | P4-4.2 | cross-validation | cross-validation | scikit-learn Cross-validation, P4-4.2 source context | Method that splits available data multiple times and evaluates models or settings on different validation portions |
| confusion matrix | confusion matrix | confusion matrix | P4-6.1 | confusion-matrix | confusion-matrix | P4-6.1 source context | Table that reads classification errors by actual and predicted label |
| data modeling | data modeling | data modeling | P3-1.1 | data-modeling | data-modeling | P3-1.1 source context | Redesigning source data into samples, features, comparisons, and output structures for a question |
| data leakage | data leakage | data leakage | P2-12.3 | data-leakage | data-leakage | P2-12.3 source context | Problem where information unavailable at prediction time enters training or evaluation |
| data science | data science | data science | P3-1.1 | data-science | data-science | P3-1.1 source context | Broad workflow for collecting, cleaning, representing, modeling, and interpreting data |
| error cost | error cost | error cost | P3-9.12 | error-cost | error-cost | Google ML Glossary thresholding, P3-9.12 source context | Operational burden assigned differently to each error type when interpreting thresholds and decisions |
| evaluation design | evaluation design | evaluation design | P3-9.13 | evaluation-design | evaluation-design | P3-9.13 source context | Choosing the data split, metric, and comparison condition that fit the problem structure |
| evaluation data | evaluation data | evaluation data | P4-4.1 | evaluation-data | evaluation-data | P4-4.1 source context | Data kept out of direct model training and used to check how the trained model behaves |
| false negative | false negative | false negative | P3-9.12 | false-negative | false-negative | Google ML Glossary false negative, P3-9.12 source context | Case that is actually positive but is judged negative by the model or rule |
| false positive | false positive | false positive | P3-9.12 | false-positive | false-positive | Google ML Glossary false positive, P3-9.12 source context | Case that is actually negative but is judged positive by the model or rule |
| group split | group split | group split | P3-9.13 | group-split | group-split | scikit-learn grouped cross-validation, P3-9.13 source context | Splitting data so records from the same entity or group do not appear on both evaluation sides |
| intervention feedback | intervention feedback | intervention feedback | P3-8.7 | intervention-feedback | intervention-feedback | P3-8.7 source context | Feedback structure where review rules or operational actions change later data and labels |
| interpretation boundary | interpretation boundary | interpretation boundary | P3-8.2 | interpretation-boundary | interpretation-boundary | P3-1.2 source context | Limit on how far a data result or comparison can be stated |
| label consistency | label consistency | label consistency | P3-9.6 | label-consistency | label-consistency | P3-9.6 source context | Degree to which labels with the same meaning repeat for the same event or similar conditions |
| label prediction | label prediction | label prediction | P3-9.1 | label-prediction | label-prediction | P3-9.1 source context | Stronger problem setup where an input case is used to predict a stable target label |
| learning-based approach | learning-based approach | learning-based approach | P4-1.2 | learning-based-approach | learning-based-approach | P4-1.2 source context | Approach that fits a model's judgment criterion from input-output examples |
| missing value | missing value | missing value | P3-5.5 | missing-value | missing-value | P3-5.5 source context | Empty value or record position that may require filling, flagging, or pulling a sample back from comparison |
| output structure | output structure | output structure | P3-2.2 | output-structure | output-structure | P3-1.1 source context | Designed result frame for comparison reports, review queues, or target candidates |
| policy | policy | policy | P1-8.3 | policy | policy | P1-14.3 source context | Criterion or function for choosing an action from the current state or observation |
| precision | precision | precision | P1-13.4 | precision | precision | P4-6.1 source context | Share of predicted positive cases that are actually positive |
| prediction contract | prediction contract | prediction contract | P3-9.7 | prediction-contract | prediction-contract | P3-9.7 source context | Prediction-problem agreement that closes input definition, result definition, time-point availability, and reproducibility together |
| prompt | prompt | prompt | P1-12.1 | prompt | prompt | OpenAI prompt engineering, GPT-3 paper | Full input bundle that sets the current response conditions |
| proxy target | proxy target | proxy target | P3-9.9 | proxy-target | proxy-target | Google ML Glossary proxy labels, P3-9.9 source context | Substitute column used like a target when the actual target is unavailable or late |
| probability estimate | probability estimate | probability estimate | P1-7.3 | probability-estimate | probability-estimate | P1-7.3 source context | Number meant to be read like a probability, requiring separate calibration judgment |
| representation learning | representation learning | representation learning | P1-3.3 | representation-learning | representation-learning | representation learning review | Learning useful internal representations from data rather than predefining all features |
| ranking | ranking | ranking | P1-13.2 | ranking | ranking | P1-13.2 source context | Ordering candidates by score or priority rather than only choosing one correct label |
| recall | recall | recall | P1-13.4 | recall | recall | P4-6.1 source context | Share of actual positive cases that the model successfully catches |
| regression | regression | regression | P1-8.1 | regression | regression | P1-8.1 source context | Modeling task that predicts a continuous numeric value or score |
| sampling bias | sampling bias | sampling bias | P2-5.3 | sampling-bias | sampling-bias | P2-5.3 source context | State where the observed sample does not represent the population well and is skewed in a particular direction |
| selective labels | selective labels | selective labels | P3-8.6 | selective-labels | selective-labels | KDD 2017 selective labels problem | Labels observed only for cases that passed through prior review or decision paths |
| rule-based approach | rule-based approach | rule-based approach | P1-2.1 | rule-based-approach | rule-based-approach | P1-2.1 source context | Approach where people explicitly write judgment rules before applying them |
| source data | source data | source data | P3-1.1 | source-data | source-data | P3-1.1 source context | Starting record before redesign into an analysis or learning problem |
| state | state | state | P1-7.1 | state | state | P1-14.3 source context | Current information and conditions used to choose the next action |
| target | target | target | P1-8.1 | target | target | P2-12.3 source context | Answer column or goal value a model is meant to predict |
| time split | time split | time split | P3-9.13 | time-split | time-split | FPP3 time series cross-validation, P3-9.13 source context | Splitting time-ordered data so later cases are evaluated using only earlier information |
| token | token | token | P6-2.1 | token | token | P6-2.1 source context | Basic computational unit into which text is split for model processing |
| tokenization | tokenization | tokenization | P6-2.2 | tokenization | tokenization | P3-6.2 source context | Converting raw text or segment structure into a token sequence |
| vocabulary | vocabulary | vocabulary | P6-2.2 | vocabulary | vocabulary | P6-2.2 source context | Internal list of token pieces and IDs used by a tokenizer |
| chunk | chunk | chunk | P1-13.1 | chunk | chunk | P1-13.1 source context | Smaller text unit cut from a longer document for search or retrieval |
| distance | distance | distance | P2-3.4 | distance | distance | P2-3.4 source context | Numerical standard for how far apart two vectors are in representation space |
| similarity search | similarity search | similarity search | P1-13.2 | similarity-search | similarity-search | information retrieval context | Finding nearby vector candidates for a question or document representation |
| validation data | validation data | validation data | P2-6.2 | validation-data | validation-data | P2-6.2 source context | Data used during model development to check and adjust model settings |
| variable transformation | variable transformation | variable transformation | P3-6.1 | variable-transformation | variable-transformation | P3-6.1 source context | Converting the same structure or value into a comparison-ready expression |
| vector | vector | vector | P2-3.1 | vector | vector | P2-3.1 source context | Ordered numerical values read as one computable representation unit |
| vector database | vector database | vector database | P6-12.1 | vector-database | vector-database | vector database context | System that manages vector storage, indexes, metadata, filtering, and updates |
| vectorization | vectorization | vectorization | P2-11.3 | vectorization | vectorization | P2-11.3 source context | Expressing repeated computation as an array-level operation |
| word2vec | word2vec | word2vec | P1-11.1 | word2vec | word2vec | Mikolov et al. 2013, P1-11.1 source context | Method family for learning word embeddings from neighboring-word context |
| contrastive learning | contrastive learning | contrastive learning | P6-3.3 | contrastive-learning | contrastive-learning | SimCLR, SBERT context | Learning representation placement from pairs that should become close or far apart |
| nearest neighbor | nearest neighbor | nearest neighbor | P1-13.2 | nearest-neighbor | nearest-neighbor | P1-13.2 source context | Candidate closest to a query or reference vector under a distance or similarity rule |
| retrieval-augmented generation, RAG | retrieval-augmented generation, RAG | retrieval-augmented generation, RAG | P1-13.3 | retrieval-augmented-generation-rag | retrieval-augmented-generation-rag | RAG paper | Structure that retrieves external evidence and attaches it to the model input before generation |
| long-context | long-context | long-context | P6-4.5 | long-context | long-context | long-context design context | Design problem of preserving and using information from long inputs |
| context window | context window | context window | P6-4.2 | context-window | context-window | P6-4.2 source context | Maximum token range a model can keep available during one input-output computation |
| next-token prediction | next-token prediction | next-token prediction | P1-10.2 | next-token-prediction | next-token-prediction | LLM generation context | Computing likely next token candidates from the current context and continuing one token at a time |
| sampling | sampling | sampling | P5-15.3 | sampling | sampling | P5-15.3 source context | Procedure that selects one actual output piece from a candidate distribution |
| self-attention | self-attention | self-attention | P5-13.2 | self-attention | self-attention | Transformer context | Attention mechanism where each token updates its representation from relationships with other tokens in the same sequence |
| softmax | softmax | softmax | P2-2.4 | softmax | softmax | P2-2.4 source context | Function that normalizes multiple scores into comparable values that sum to 1 |
| Transformer | Transformer | Transformer | P1-11.3 | transformer | transformer | Attention Is All You Need | Attention-based neural architecture family that compares sequence positions without recurrence |
