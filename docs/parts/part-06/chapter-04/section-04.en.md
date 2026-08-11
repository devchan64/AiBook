# P6-4.4 Supplement: KV Cache and Repeated Generation

> Section ID: `P6-4.4`
> Version: `v2026.07.26`

_Subtitle: Which attention computations does KV cache reuse in repeated generation?_

In P6-4.2, we saw that attention and the context window connect to input-range constraints, and in P6-4.3, we organized how multi-head attention and positional representations reinforce context reading. The next name that often blocks readers is `KV cache`.

Why does a long conversation or long generation become slower even with the same structure?

The standard for answering this question is the view of `whether some previous computation is reused`. Here, we read KV cache as that reuse device.

## Computation Reused by KV Cache

- Why does KV cache connect to conversational generation speed?
- Is KV cache a device that changes the model's meaning, or a device that reduces repeated computation?
- Why does KV cache become more important as the context window gets longer?

The problem to close first here is `how the already computed front part is reused in repeated generation`.

| What we handle now | What is passed to later chapters or later parts |
| --- | --- |
| The basic meaning of KV cache, which stores part of previous computation and reuses it in the next step | Cache-management methods by actual serving engine |
| The sense that projection burden is reduced while preserving the same result | Operating-latency and cost-optimization judgment |

The context-window constraint itself was already explained in the main flow, P6-4.2, and the impact of KV cache on operating latency and cost is recovered again in P6-18.1. The problem of maintaining long context itself and sparse attention are separate long-context design problems.

This distinction must be fixed so KV cache can be read not as `a function that changes the meaning of the answer`, but as `a device that produces the same result with less recomputation`. The reason KV cache connects to perceived speed in long conversations or long code generation is also explained by this standard.

## Why Is KV Cache Important?

In conversational generation, the model makes one token, then makes the next token again. If previous computation is redone from the beginning every time, it is very inefficient.

KV cache can be understood as a device that improves speed when generating the next token by reusing some attention-related values calculated earlier.

If this standard is reduced to one sentence, it is as follows.

`What should not be recomputed while preserving the same result?`

Because repeated generation burden also grows as the context window gets longer, KV cache is especially likely to connect to perceived speed in long conversations or long code generation.

This explanation becomes clearer if translated into an everyday scene. When continuing a reply in a long messenger conversation, or continuing to generate the next line while looking at a long code file, people usually feel that they are `continuing while keeping in mind what they already saw earlier`. So it is easy to expect responses to continue at roughly similar speed. But if the model recalculates all previously seen tokens in the same way from the beginning every time it makes one new token, the burden of making the next token grows together as the conversation grows longer.

In other words, when first reading KV cache, hold onto it as follows.

- `When making a new token, does the model completely recalculate the front part from the beginning?`
- Or `does it store some already computed front part and add only what is newly needed?`

KV cache is closer to the second side. The core is that it is more a `reuse device that avoids recalculating the already seen front part` than a `new intelligence that changes meaning`.

This standard keeps you from misunderstanding KV cache as `a function that makes the model understand better`. What you should see first is not `does the answer become smarter`, but `how much repeated computation is reduced in the process of making the same answer`.

## What Changes and What Does Not Change?

The most important distinction when first reading KV cache is separating `does the model become smarter` from `does the same computation repeat less`.

What KV cache first changes is not the meaning of the answer or reasoning ability, but the amount of repeated computation needed before the same answer comes out. As the conversation becomes longer, the number of previous tokens increases. So if the front part is projected again into keys and values every time, the burden grows with each new token. The cache stores this front-part computation and changes the flow toward adding only the computation needed for newly appended tokens.

So questions such as `does turning on KV cache make the answer more accurate`, `does it suddenly reason more intelligently`, or `does turning it off make the answer wrong and turning it on make it correct` are a little off the core. A safer standard is separating `the content of the answer` from `the repeated work needed to produce the answer`.

In other words, when understanding KV cache, you should see both `what answer came out` and `how many times the front part was recalculated to make that answer`.

## Why Does the Difference Feel Larger as the Context Window Gets Longer?

When people say KV cache is especially important in long contexts, it is often received only as `long contexts are naturally slow`. But there is a more concrete reason here.

When the context is short, the number of tokens seen earlier is not large, so recalculating the front part may be a relatively small burden. Conversely, when a conversation grows or long code generation continues, the size of `the already passed front part` also grows every time one new token is made. Without a cache, `the long prefix already seen earlier` is recalculated for every new token.

This difference can be understood as follows.

- Short context: the front part being recalculated is still short
- Long context: the front part being recalculated is already long
- So the longer the context, the greater the perceived difference of `whether the front part is not redone`

In other words, saying KV cache matters more as the context window gets longer is closer to meaning `the value of not repeatedly recalculating the already seen long front part grows`, not `it understands long input better`.

## Cases and Examples

### Case 1. When a Chat-Style Coding Assistant Gradually Slows Down

Imagine a coding assistant that continues through several turns while looking at the same code file. People expect the next answer to continue at a similar speed because the same file is being viewed. But if previous token relationships are recalculated from the beginning every time, response latency can become noticeably larger as turns become longer.

When making the first answer, the preceding context is short, so the difference may not be felt much. But after several turns accumulate, such as file explanation, function modification, failed test logs, and another modification request, `the front part that already passed before making one new answer now` becomes long. Without cache, that long front part must be recalculated for every next token. With cache, the already computed front part is stored and only the newly needed part is added.

The result to check in this case is whether `as the conversation becomes longer, cache reuse appears as a difference in perceived latency`. The standard to hold is changing `why does it get slower as the conversation becomes longer` from something like `the model gets tired` into the question `does it compute the already seen front part again for every new token`.

### Case 2. When Draft Generation Continues Based on a Long Document

Imagine inserting a long policy document, creating a summary draft, refining that draft, and then asking again to explain only exception clauses. Because the same document continues to be referenced, it is easy to expect speed to stay roughly similar. But if tokens seen earlier are recalculated from the beginning every time, the burden of the next step grows with the context length.

If draft generation does not end once and continues as `summary -> refinement -> explain a specific exception again`, in practice a similar long preceding context is repeatedly referenced across several steps. What matters here is not `does referencing the document for a long time make it smarter`, but `does it avoid recalculating the same long preceding context repeatedly`.

The result to check in this case is `why a reuse device becomes more important when the same context continues to be used`. The practical value of KV cache appears more clearly when generation accumulates over several steps on top of that context than at the moment a long document is inserted once.

## Standards Revisited in Failure Scenes

To make the explanation so far firmer, it is useful to also see the failure scenes KV cache is meant to prevent.

| Failure scene first visible | Question to reread from the KV cache view | Why it matters |
| --- | --- | --- |
| Answers become slower as the conversation gets longer | `Is the long prefix already seen being computed again for every new token?` | Because repeated computation accumulates |
| In long code generation, generating the next line stutters more as the front part gets longer | `Is the already computed front part being stored?` | Because front-context recomputation burden grows for each new line |
| Speed drops as long-document draft revision continues | `Is there a reuse device when the same context continues across steps?` | Because a similar long context is reread across several steps |

The purpose of this table is not to explain every speed problem with KV cache alone. It is to make you first recall, when seeing the phenomenon `it gets slower as it gets longer`, whether the structure repeatedly recalculates the front part that was already seen.

## Practice and Examples

The goal of this example is to show `what KV cache actually stores and how much recomputation it prevents as generation becomes longer`. Token IDs are passed through small embeddings and query/key/value projections to confirm that the last token's attention result stays the same regardless of cache, while the reprojection amount decreases. Then we also see how the saving changes when prefix length changes.

The core comparison is as follows.

- Without cache, whenever making a new token, all tokens so far are transformed into K/V again.
- With cache, previous tokens' K/V are stored, and only the new token's K/V is added.
- The last attention output of both methods should be the same. What changes is `how much was recalculated`.

The code below uses prefix tokens already seen and newly generated tokens to follow. In the result, check together the K/V matrix shape recalculated at each step without cache and the last-token attention result, the K/V cache shape maintained when cache is used and the last-token attention result, the number of tokens projected at each step in both methods, total projected token count and saving ratio, and how the reprojection saving ratio changes when prefix length changes.

The core to check is that KV cache reduces projection burden in later steps by reusing computation results from previous tokens. The attention result does not change depending on whether the cache exists; the number of tokens projected again before making the same result changes. The longer the prefix or the more generation steps there are, the greater the effect of `not recalculating the front part`.

The diagram below first compresses the computation flow this example compares. Without cache, every time a new token is made, the front part is transformed into K/V again. With KV cache, K/V of the already seen prefix are stored, and only K/V of the new token are added.

```mermaid
--8<-- "assets/part-06/chapter-04/p6-c04-s04-kv-cache-flow-en.mmd"
```

```python
# Example comparing projection burden between recalculating every time without KV cache and reusing previous K/V with cache.
import numpy as np

token_to_id = {
    "user": 0,
    "login": 1,
    "error": 2,
    "reproduce": 3,
    "done": 4,
}

embedding_table = np.array(
    [
        [1.0, 0.2, 0.0],
        [0.5, 1.0, 0.1],
        [1.2, 0.8, 0.4],
        [0.3, 1.1, 0.9],
        [0.7, 0.4, 1.3],
    ]
)

W_k = np.array(
    [
        [0.8, 0.1],
        [0.2, 0.7],
        [0.5, 0.6],
    ]
)

W_v = np.array(
    [
        [0.3, 0.9],
        [0.6, 0.2],
        [0.4, 0.8],
    ]
)

W_q = np.array(
    [
        [0.7, 0.2],
        [0.1, 0.8],
        [0.6, 0.5],
    ]
)

prefix_token_ids = [token_to_id["user"], token_to_id["login"], token_to_id["error"]]
generated_token_ids = [token_to_id["reproduce"], token_to_id["done"]]

def project_to_kv(token_ids):
    embeddings = embedding_table[token_ids]
    keys = embeddings @ W_k
    values = embeddings @ W_v
    return keys, values

def project_query(token_id):
    embedding = embedding_table[[token_id]]
    return embedding @ W_q

def attention_for_last_token(query, keys, values):
    scores = (query @ keys.T) / np.sqrt(keys.shape[1])
    shifted = scores - np.max(scores)
    weights = np.exp(shifted) / np.sum(np.exp(shifted))
    context = weights @ values
    return weights, context

def decode_without_cache(prefix_ids, new_ids):
    seen_ids = prefix_ids[:]
    projected_token_count = 0
    step_logs = []

    for new_id in new_ids:
        seen_ids.append(new_id)
        keys, values = project_to_kv(seen_ids)
        query = project_query(new_id)
        weights, context = attention_for_last_token(query, keys, values)
        projected_token_count += len(seen_ids)
        step_logs.append((new_id, len(seen_ids), keys, values, weights, context))

    return step_logs, projected_token_count

def decode_with_cache(prefix_ids, new_ids):
    cached_keys, cached_values = project_to_kv(prefix_ids)
    projected_token_count = len(prefix_ids)
    step_logs = [
        (
            "prefix_loaded",
            len(prefix_ids),
            cached_keys.copy(),
            cached_values.copy(),
            None,
            None,
        )
    ]

    for new_id in new_ids:
        new_keys, new_values = project_to_kv([new_id])
        cached_keys = np.vstack([cached_keys, new_keys])
        cached_values = np.vstack([cached_values, new_values])
        query = project_query(new_id)
        weights, context = attention_for_last_token(query, cached_keys, cached_values)
        projected_token_count += 1
        step_logs.append((new_id, 1, cached_keys.copy(), cached_values.copy(), weights, context))

    return step_logs, projected_token_count

def projection_counts(prefix_length, generated_length):
    no_cache_count = sum(prefix_length + step for step in range(1, generated_length + 1))
    with_cache_count = prefix_length + generated_length
    saved_ratio = 1 - (with_cache_count / no_cache_count)
    return no_cache_count, with_cache_count, saved_ratio

no_cache_logs, no_cache_count = decode_without_cache(prefix_token_ids, generated_token_ids)
with_cache_logs, with_cache_count = decode_with_cache(prefix_token_ids, generated_token_ids)
saved_ratio = round(1 - (with_cache_count / no_cache_count), 3)

print("[without cache]")
for token_id, projected_now, keys, values, weights, context in no_cache_logs:
    print("new_token_id =", token_id)
    print("projected_now =", projected_now)
    print("keys_shape =", keys.shape, "values_shape =", values.shape)
    print("attention_weights =", np.round(weights, 3))
    print("context =", np.round(context, 3))
    print("last_key_row =", np.round(keys[-1], 2))
    print("last_value_row =", np.round(values[-1], 2))

print("[with cache]")
for token_id, projected_now, keys, values, weights, context in with_cache_logs:
    print("step =", token_id)
    print("projected_now =", projected_now)
    print("keys_shape =", keys.shape, "values_shape =", values.shape)
    if token_id != "prefix_loaded":
        print("attention_weights =", np.round(weights, 3))
        print("context =", np.round(context, 3))
        print("last_key_row =", np.round(keys[-1], 2))
        print("last_value_row =", np.round(values[-1], 2))

print("step_output_match_1 =", np.allclose(no_cache_logs[0][5], with_cache_logs[1][5]))
print("step_output_match_2 =", np.allclose(no_cache_logs[1][5], with_cache_logs[2][5]))

print("no_cache_projected_token_count =", no_cache_count)
print("with_cache_projected_token_count =", with_cache_count)
print("saved_ratio =", saved_ratio)

print("[projection count by prefix length]")
for prefix_length in [3, 20, 100]:
    no_cache_total, with_cache_total, ratio = projection_counts(
        prefix_length=prefix_length,
        generated_length=5,
    )
    print(
        f"prefix_length={prefix_length}, generated_length=5, "
        f"without_cache={no_cache_total}, with_cache={with_cache_total}, "
        f"saved_ratio={ratio:.3f}"
    )
```

The output below was confirmed with the same values as the body code using Python in the local `.venv`.

An example execution result can be read as follows.

```text
[without cache]
new_token_id = 3
projected_now = 4
keys_shape = (4, 2) values_shape = (4, 2)
attention_weights = [[0.121 0.189 0.317 0.373]]
context = [[0.931 1.197]]
last_key_row = [0.91 1.34]
last_value_row = [1.11 1.21]
new_token_id = 4
projected_now = 5
keys_shape = (5, 2) values_shape = (5, 2)
attention_weights = [[0.095 0.124 0.252 0.24  0.289]]
context = [[0.937 1.369]]
last_key_row = [1.29 1.13]
last_value_row = [0.97 1.75]
[with cache]
step = prefix_loaded
projected_now = 3
keys_shape = (3, 2) values_shape = (3, 2)
step = 3
projected_now = 1
keys_shape = (4, 2) values_shape = (4, 2)
attention_weights = [[0.121 0.189 0.317 0.373]]
context = [[0.931 1.197]]
last_key_row = [0.91 1.34]
last_value_row = [1.11 1.21]
step = 4
projected_now = 1
keys_shape = (5, 2) values_shape = (5, 2)
attention_weights = [[0.095 0.124 0.252 0.24  0.289]]
context = [[0.937 1.369]]
last_key_row = [1.29 1.13]
last_value_row = [0.97 1.75]
step_output_match_1 = True
step_output_match_2 = True
no_cache_projected_token_count = 9
with_cache_projected_token_count = 5
saved_ratio = 0.444
[projection count by prefix length]
prefix_length=3, generated_length=5, without_cache=30, with_cache=8, saved_ratio=0.733
prefix_length=20, generated_length=5, without_cache=115, with_cache=25, saved_ratio=0.783
prefix_length=100, generated_length=5, without_cache=515, with_cache=105, saved_ratio=0.796
```

The core to read in this example is as follows.

- In both methods, `attention_weights` and `context` at the same step match.
- In other words, KV cache is not a device that tries to change the final attention result. It is `a device that makes the same result with less recomputation`.
- The difference is whether K/V for the prefix tokens seen earlier were projected again.
- Without cache, the first new token projects 4 tokens again and the next token projects 5 tokens again. With cache, only 1 new token is additionally projected each time.
- Even when generating the same 5 tokens, the difference between `without_cache` and `with_cache` becomes much larger at prefix lengths 20 and 100 than at prefix length 3.
- So as the prefix gets longer or generation steps increase, the `projected_token_count` difference grows quickly.

![Number of tokens targeted for KV projection by generation step](/AiBook/assets/part-06/chapter-04/kv-cache-step-projection-en.png)

If the reprojection amount by prefix length is drawn, the difference opens as follows. Without cache, the longer the already seen prefix, the faster the amount that must be projected again for each new token grows. With KV cache, the growth is much smaller under the same condition.

![Number of tokens targeted for KV projection by prefix length](/AiBook/assets/part-06/chapter-04/kv-cache-projection-count-en.png)

Here, it is more important to read the comparison direction than the numbers themselves.

- `Did the same context come out?`
- `How much did the number of recalculated tokens differ?`
- `Does this difference seem likely to grow when the preceding context gets longer?`
- `If generated_length is changed from 5 to 20, how do the saving ratio and total reprojection amount change?`

If you can answer these questions, you have begun to read KV cache not only as `a difficult internal model name`, but as `a practical device that prevents recalculating the same front part in long generation`.

## Checklist

- KV cache is a practical device for reducing repeated computation cost in long generation.
- KV cache is a device that makes the same result with less recomputation, rather than changing model meaning.
- As context accumulates in long conversations and long code generation, the perceived value of KV cache grows.
- You should be able to distinguish KV cache and long-context design problems as `computation reduced through reuse` and `clues that must be maintained in long input`.

## Sources and References

- Ashish Vaswani et al., [Attention Is All You Need](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }, NeurIPS 2017, accessed 2026-07-19. Used as basic background evidence for the query, key, and value computations in attention when explaining KV cache.
- Hugging Face, [Cache strategies](https://huggingface.co/docs/transformers/kv_cache){: target="_blank" rel="noopener noreferrer" }, Transformers documentation, accessed 2026-07-19. Used as evidence for the explanation that autoregressive generation stores key-value vectors to reduce recomputation and improve generation performance.
