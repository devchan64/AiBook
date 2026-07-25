<a id="runtime-state"></a>

## 运行时状态(runtime state)

- 含义: 运行时状态是当前执行会话中暂时存在的变量、导入的包、内存对象、临时文件等状态。它可能不会完整保存在 notebook 文件里。
- 为什么重要: notebook 文件留下了代码和部分输出，但当前运行时里的变量和临时文件可能在重启后消失。理解运行时状态可以把文件、代码和实际执行会话分开读。
- 相关概念: `运行时(runtime)`, `隐藏状态(hidden state)`, `执行顺序(execution order)`
- 核心 Section: `P2-10.3`
- 出现 Section: `P2-10.2`
