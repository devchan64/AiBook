# P2-12.3 准备学习数据集的直观理解

> Section ID: `P2-12.3`
> Version: `v2026.09.15`

## 预测时点与输入列

学习数据集把模型使用的输入与需要预测的答案配对。即使是同一张学生表，在考试前预测是否通过，与考试后根据分数计算是否通过，可使用的列也不同。

| 列 | 考前预测是否通过时的角色 |
| --- | --- |
| `student_id` | 区分学生的标识 |
| `region` | 预测时已知的类别输入候选 |
| `absences` | 截至预测时点的缺勤次数输入候选 |
| `score` | 尚未参加的考试结果，因此排除在输入之外 |
| `passed` | 需要预测的答案 |

考试前无法知道最终分数。如果仅仅因为历史记录里有分数就将其作为输入，训练便获得了实际预测时不可用的信息，这就是数据泄漏。如果最终是否通过由分数标准决定，那么根据分数判断是否通过，可以直接通过应用该标准来计算。

## 输入 X 与目标 y

`X` 是输入特征表，`y` 是目标，也就是答案集合。在下表中，选择考试前的地区和缺勤次数作为输入候选，把通过状态分离为目标。

```python
import pandas as pd

df = pd.DataFrame(
    {
        "student_id": ["S001", "S002", "S003", "S004"],
        "region": ["Seoul", "Busan", "Seoul", "Busan"],
        "absences": [1, 5, 0, 2],
        "score": [82, 45, 90, 73],
        "passed": ["yes", "no", "yes", "yes"],
    }
)

X = df[["region", "absences"]]
y = df["passed"]

print(X)
print(y)
print(X.shape, y.shape)
```

`X` 包含四名学生的地区和缺勤次数，`y` 包含 `["yes", "no", "yes", "yes"]`。形状分别为 `(4, 2)` 和 `(4,)`，表示四名学生、每人两个特征，以及对应的四个答案。需要同时处理 `X` 和 `y`，避免行顺序变化后把学生与其他人的答案配对。

```mermaid
--8<-- "assets/part-02/chapter-12/x-y-split-flow-zh.mmd"
```

`student_id` 用于连接记录时识别学生。如果没有依据认为编号本身能够解释学习表现，就应将它排除在输入之外。若把 `passed` 也作为输入，模型便能直接读到答案，无法有效评估预测能力。

## 分离训练、验证与测试数据

训练数据用于学习模型规则，验证数据用于比较模型类型或设置，测试数据则留到选择结束后进行最终评估。如果训练和评估使用同一批记录，就难以区分记住已有记录的效果与预测新记录的能力。

```mermaid
--8<-- "assets/part-02/chapter-12/train-val-test-flow-zh.mmd"
```

对于来自不同学生的独立记录，可以用 `train_test_split` 随机划分。若同一学生有重复记录，或数据具有时间顺序，就需要考虑学生分组或时间顺序。仅随机划分行，并不能阻断所有泄漏。

## 案例：把 36 名学生分为 27 名与 9 名

使用 [`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview } 中的 36 名学生，准备考前预测是否通过的数据。这里假设学习时间、缺勤次数和测验次数均为截至预测时点已获得的记录。最终分数 `score` 和答案 `passed` 不作为输入。

在仓库根目录运行后，输入形状为 `(36, 3)`，目标形状为 `(36,)`。将 25% 的行，即九名学生，留作测试，其余 27 名用于训练。

```python
from pathlib import Path
from sklearn.model_selection import train_test_split

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

feature_columns = ["study_hours", "absences", "practice_quizzes"]
X = df[feature_columns]
y = df["passed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("train/test shapes:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)
```

```text
X shape: (36, 3)
y shape: (36,)
train/test shapes: (27, 3) (9, 3) (27,) (9,)
```

把 `test_size` 改为 `0.5`，训练和测试各有 18 名学生。改变 `random_state` 可能改变所选学生，但在相同比例下行数不变。以上代码只划分训练和测试集，没有单独建立验证集。若要比较模型设置，应从训练部分再分出验证数据，或使用交叉验证。

`stratify=y` 尽可能让两个集合保留相近的通过与未通过比例。由于人数必须为整数，比例不一定完全一致。如果某一类别的记录太少，或划分后的集合太小，分层划分可能无法完成。固定 `random_state` 是为了在相同输入和执行条件下复现划分，并不能保证一次划分具有代表性。

## 检查输入目标配对与学生重叠

划分前，`X` 和 `y` 中的学生顺序就必须一致。`train_test_split` 不会查找学生 ID 来修复错误配对，而是保留同时传入的数组当前按位置对应的关系。可以通过返回的索引检查对应关系及集合之间的重叠。

```python
print(X_train.index.equals(y_train.index))
print(X_test.index.equals(y_test.index))
print(set(X_train.index).isdisjoint(X_test.index))

train_ids = set(df.loc[X_train.index, "student_id"])
test_ids = set(df.loc[X_test.index, "student_id"])
print(train_ids.isdisjoint(test_ids))
```

```text
True
True
True
True
```

前两个结果表示输入与目标的标签顺序相同，第三个表示行没有重叠，第四个进一步确认学生 ID 也没有重叠。这份 CSV 每名学生只有一行，但重复记录中，不同行仍可能属于同一名学生。此时若要评估对新学生的预测，就应按学生划分。

## 留出九名学生用于验证

从 27 名训练候选学生中再取出九名用于验证，就得到训练 18 名、验证九名、测试九名。测试集不参与第二次划分。

```python
X_fit, X_val, y_fit, y_val = train_test_split(
    X_train, y_train, test_size=9, random_state=42, stratify=y_train
)
print(len(X_fit), len(X_val), len(X_test))
```

```text
18 9 9
```

`test_size=9` 表示九行，`test_size=0.25` 表示输入总行数的 25%。使用这三个集合比较模型时，应以 `X_fit` 学习预处理规则并训练模型，根据验证结果选择设置，再用测试集进行最终评估。这 36 名学生只是用来演示划分过程的小例子，不能据此稳定估计模型性能。

也可以通过文件执行相同的划分与重叠检查。

[p2_12_3_dataset_split_preview.py](/AiBook/assets/part-02/chapter-12/p2_12_3_dataset_split_preview.py)

```bash
python docs/assets/part-02/chapter-12/p2_12_3_dataset_split_preview.py
```

## 从训练数据计算预处理规则

用平均值填补缺失值或进行标准化时，需要从数据中计算平均值、标准差等依据。这些依据只能从训练数据中确定，再将相同规则应用于验证和测试数据。如果计算平均值时包含测试数据，评估信息就会混入训练。

```mermaid
--8<-- "assets/part-02/chapter-12/no-leakage-preprocessing-flow-zh.mmd"
```

假设训练集学习时间为 `[2.0, 4.0, 缺失值]`，测试集为 `[10.0, 缺失值]`。训练集已观测值的平均值为 3，因此两边的缺失值都用 3 填充。

```python
train_hours = pd.Series([2.0, 4.0, None])
test_hours = pd.Series([10.0, None])

fill_value = train_hours.mean()
print(train_hours.fillna(fill_value).tolist())
print(test_hours.fillna(fill_value).tolist())
```

```text
[2.0, 4.0, 3.0]
[10.0, 3.0]
```

若使用全部已观测值，平均值为 `(2 + 4 + 10) / 3`，约 5.33，填入训练集的值便包含测试信息。即使将测试集中的 10 改成 100，从训练集确定的填充值仍应为 3。

在 scikit-learn 中，`fit` 用于学习规则，`transform` 用于应用已学到的规则。不要对测试数据调用预处理器的 `fit` 或 `fit_transform`。

## 用数值列表示类别

地区等字符串类别是否需要转为数值表示，取决于模型。`get_dummies` 为每个地区建立指示列，属于该地区时为 1，否则为 0。下面的小表会生成 Busan 和 Seoul 两列。

```python
regions = pd.DataFrame({"region": ["Seoul", "Busan", "Seoul"]})
encoded = pd.get_dummies(regions, columns=["region"], dtype=int)
print(encoded)
```

```text
   region_Busan  region_Seoul
0             0             1
1             1             0
2             0             1
```

这个独立示例只演示类别表示。分别对训练集和测试集调用 `get_dummies` 时，所含地区不同可能导致生成的列不同。实际训练中，应从训练数据确定类别和列结构，再将同一结构应用于测试数据，并规定如何处理未见过的类别。

## 检查缺失值与类型

检查各列缺失值数量和类型，可以发现需要填补的值或需要转换为数值的列。下面的代码对学生 CSV 的每一列都报告零个缺失值。这只表示值没有缺失，并不能保证记录时点或答案正确。

```python
print(df.isna().sum())
print(df.dtypes)
```

如果数值字段中含有字符串 `"unknown"`，仅用 `isna()` 无法识别这种未录入状态。下面的代码把无法解释为数字的值转换成缺失值。

```python
hours_text = pd.Series(["8.0", "unknown", "6.5"])
hours = pd.to_numeric(hours_text, errors="coerce")
print(hours.isna().tolist())
print(hours.dropna().tolist())
```

```text
[False, True, False]
[8.0, 6.5]
```

`errors="coerce"` 不判断错误字符串的含义，只把它们转换为缺失值。若转换后缺失值数量增加，应检查原始写法和录入错误，再确定处理规则。即使成功读成数字，也可能超出允许范围，例如负数学习时间。

## 检查清单

- 能否用一句话明确预测时点和目标？
- 能否解释为何最终分数不能作为考前输入？
- 能否将输入 `X` 和目标 `y` 的行按同一学生对应？
- 能否区分训练、验证和测试数据的作用？
- 能否解释为何改变测试值不应改变从训练集确定的预处理规则？
- 能否解释类别编码为何需要保持训练集和测试集的列结构一致？
- 能否区分行重叠与学生重叠，并从训练候选中另行划分验证数据？

## 来源与参考资料

- pandas Developers, [pandas.get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-07-20. 类别变量的指示列。
- scikit-learn Developers, [Glossary](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, 查阅日期：2026-07-20. 数组形状、估计器输入约定与 X/y 术语。
- scikit-learn Developers, [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, 查阅日期：2026-09-15. 输入目标联合划分，以及 test_size、random_state 和 stratify。
- scikit-learn Developers, [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, 查阅日期：2026-09-15. 仅从训练集学习预处理规则与防止数据泄漏。
- pandas Developers, [pandas.to_numeric](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-15. errors="coerce" 对数值转换失败的处理.
