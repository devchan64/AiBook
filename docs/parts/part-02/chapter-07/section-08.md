# P2-7.8 보충학습: 셸 실행 흐름 읽기

> Section ID: `P2-7.8`
> Version: `v2026.09.08`

셸의 `|`는 한 명령의 출력을 다음 명령의 입력으로 연결합니다. `>`와 `<`는 출력과 입력을 파일에 연결하고, 환경 변수(environment variable)는 프로그램에 설정값을 전달합니다. 아래 셸 명령은 Bash 기준이며 `python`으로 Python을 실행할 수 있다고 가정합니다.

## 표준 입력과 표준 출력

명령줄 프로그램은 표준 입력(standard input)으로 데이터를 받고, 표준 출력(standard output)으로 결과를 보낼 수 있습니다. 터미널에서 직접 실행할 때는 보통 키보드와 화면에 연결되지만, 파일이나 다른 프로그램으로 연결을 바꿀 수 있습니다.

아래 코드를 `read_numbers.py`로 저장합니다. 한 줄에 숫자 하나가 들어오는 입력을 읽고 합계를 출력합니다. `10`, `20`, `30`이 입력되면 `60`이 나옵니다.

```python
import sys

# 표준 입력에서 한 줄씩 받아 정수로 바꾼 뒤 합합니다.
numbers = [int(line) for line in sys.stdin if line.strip()]
print(sum(numbers))
```

Bash에서 다음 명령으로 입력 파일 `numbers.txt`를 만듭니다. `\n`은 printf가 줄바꿈으로 바꾸는 표기입니다.

```bash
printf '10\n20\n30\n' > numbers.txt
```

## 파이프로 명령 연결하기

`cat`은 파일 내용을 표준 출력으로 보냅니다. `|`로 연결하면 그 내용이 Python 프로그램의 표준 입력이 됩니다.

```bash
cat numbers.txt | python read_numbers.py
```

출력은 `60`입니다. 파일 내용을 화면에 보여 준 뒤 사람이 다시 입력하는 대신 두 프로그램이 데이터를 주고받습니다. 뒤 프로그램이 표준 입력을 읽도록 작성되어 있어야 이 연결이 의미가 있습니다.

파이프는 명령들을 단순히 순서대로 실행하라는 표기가 아닙니다. 앞 명령의 표준 출력을 뒤 명령의 표준 입력에 연결합니다. 오류 메시지에 쓰는 표준 오류(standard error)는 기본적으로 이 연결에 포함되지 않습니다.

## 파일로 입력과 출력 연결하기

`<`를 쓰면 `cat` 없이도 같은 파일을 Python의 표준 입력에 연결할 수 있습니다.

```bash
python read_numbers.py < numbers.txt
```

화면 대신 `total.txt`에 결과를 저장하려면 `>`를 함께 사용합니다.

```bash
python read_numbers.py < numbers.txt > total.txt
```

명령이 성공하면 화면에는 합계가 보이지 않고, `total.txt`에 `60`과 줄바꿈이 저장됩니다. `cat total.txt`로 내용을 확인할 수 있습니다.

| Bash 표기 | 동작 |
| --- | --- |
| `< input.txt` | 파일을 표준 입력에 연결 |
| `> output.txt` | 표준 출력을 파일에 기록, 기존 내용은 덮어씀 |
| `>> output.txt` | 표준 출력을 파일 끝에 추가 |
| `2> errors.log` | 표준 오류를 별도 파일에 기록 |

`python train.py > train.log`도 표준 출력만 저장합니다. 오류 메시지까지 모두 그 파일에 들어간다고 가정하면 안 됩니다. 파일 경로는 현재 작업 폴더를 기준으로 해석됩니다.

## 명령을 셸 스크립트로 저장하기

반복할 명령을 `run_summary.sh`에 저장할 수 있습니다.

```bash
python read_numbers.py < numbers.txt > total.txt
cat total.txt
```

세 파일이 있는 폴더에서 다음 명령을 실행하면 Bash가 스크립트를 읽어 합계를 저장하고 출력합니다.

```bash
bash run_summary.sh
```

셸 스크립트(shell script)는 셸이 해석하는 명령 파일입니다. Python 코드를 저장하는 `.py` 파일과는 해석하는 프로그램이 다릅니다.

## 환경 변수로 설정값 전달하기

환경 변수는 프로그램을 실행할 때 전달하는 이름과 값의 쌍입니다. 예를 들어 데이터 폴더를 코드 밖에서 정할 수 있습니다.

Bash에서 다음 명령을 실행합니다.

```bash
export BOOK_DATA_DIR="./data"
```

`export`는 이후 이 셸에서 실행하는 자식 프로세스에 값을 전달하도록 합니다. 이미 실행 중인 다른 터미널의 환경까지 바꾸는 것은 아닙니다.

아래 코드를 `show_config.py`에 저장하고 같은 셸에서 `python show_config.py`를 실행하면 `./data`가 출력됩니다.

```python
import os

# 환경 변수가 없을 때는 미설정 상태를 출력합니다.
print(os.environ.get("BOOK_DATA_DIR", "not set"))
```

Windows PowerShell에서는 환경 변수를 다음처럼 지정할 수 있습니다.

```powershell
$env:BOOK_DATA_DIR = "./data"
python show_config.py
```

환경 변수 값은 문자열입니다. 경로를 지정했다고 그 폴더가 자동으로 생성되지는 않습니다. API 키 같은 비밀값도 환경 변수로 전달할 수 있지만, 코드나 출력 로그에 그대로 남기지 않아야 합니다.

## 숫자 입력과 저장 방식 바꾸기

`numbers.txt`의 마지막 숫자를 `30`에서 `40`으로 바꾸면 합계가 `60`에서 `70`으로 바뀝니다. 다음 명령을 실행하면 `total.txt`에는 새 합계 `70`만 남습니다.

```bash
python read_numbers.py < numbers.txt > total.txt
```

같은 상태에서 `>`를 `>>`로 바꿔 다시 실행하면 파일에는 `70`이 두 줄로 쌓입니다. 계산 코드는 같고, 셸의 출력 연결 방식만 달라진 결과입니다.

## 명령에서 확인할 변경 대상

| 표기 | 확인할 대상 |
| --- | --- |
| `>` | 덮어쓸 파일 경로 |
| `rm`, `del`, `Remove-Item` | 삭제할 파일과 폴더 |
| `sudo` | 높아진 권한으로 실행할 명령 |
| 비밀값이 든 환경 변수 | 명령 기록·로그·저장소에 값이 남는지 여부 |

PowerShell의 파이프는 명령 간 객체도 전달하며, Bash와 모든 문법이 같지는 않습니다. 특히 위의 `<` 입력 리다이렉션을 PowerShell 명령으로 그대로 옮기지 않습니다.

## 체크리스트

- 셸 스크립트와 Python 스크립트를 해석하는 프로그램을 구분할 수 있다.
- `|`가 표준 출력과 표준 입력을 연결한다고 설명할 수 있다.
- `<`, `>`, `>>`의 파일 읽기·덮어쓰기·추가 동작을 구분할 수 있다.
- 표준 출력과 표준 오류가 별도 통로임을 설명할 수 있다.
- 환경 변수로 전달한 설정값을 Python에서 읽을 수 있다.
- 입력 숫자와 출력 연결 방식을 바꿨을 때 파일 내용이 어떻게 달라지는지 확인할 수 있다.

## 출처와 참고 자료

- GNU Project, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, 확인 날짜: 2026-07-20. Bash의 셸 역할, 파이프라인, 리다이렉션, 변수·환경 변수 문법을 확인하는 근거로 사용했다.
- Microsoft Learn, [about_Pipelines](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_pipelines){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, 확인 날짜: 2026-07-20. PowerShell에서 `|`가 앞 명령 결과를 다음 명령으로 보내는 파이프라인 연산자라는 설명 확인에 사용했다.
- Microsoft Learn, [about_Redirection](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_redirection){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, 확인 날짜: 2026-07-20. PowerShell에서 `>`, `>>`, `n>` 같은 리다이렉션 연산자가 출력 스트림을 파일로 보내거나 추가한다는 설명 확인에 사용했다.
- Microsoft Learn, [about_Environment_Variables](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, 확인 날짜: 2026-07-20. 환경 변수가 운영체제와 프로그램이 사용하는 문자열 설정값이며 자식 프로세스에 전달될 수 있다는 설명 확인에 사용했다.
