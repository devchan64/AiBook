## PATH

- Meaning: PATH is the list of locations a terminal checks when it tries to find an executable from a command name. When a user types a short name such as `python`, `pip`, or `git`, the shell searches these directories in order.
- Why it matters: PATH separates `the program is not installed` from `the program exists but the shell cannot find it`. It also explains why virtual environments and multiple installed versions can cause the same command name to run different executables in different environments.
- Related concepts: `environment variable`, `interpreter`, `terminal`
- Core Section: `P2-7.9`
- Appears in: `P2-10.2`, `P2-10.3`
