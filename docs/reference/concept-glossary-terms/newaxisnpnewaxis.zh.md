<a id="newaxisnpnewaxis"></a>

## newaxis，np.newaxis

- 含义：`newaxis` 或 `np.newaxis` 会给 NumPy 数组增加一个长度为 1 的轴，但不改变底层值。
- 为什么重要：它帮助有意对齐 shape 以使用广播，并避免把 shape 问题误读成值问题。
- 相关概念：`广播`，`shape`，`共享底层对象`
- 中心 Section：`P2-11.4`
- 出现 Section：`P2-12.1`
