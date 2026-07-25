<a id="import-statement"></a>

### import 문(import statement)

- 뜻: Python 코드 안에서 설치된 모듈이나 패키지를 현재 코드에서 사용할 수 있게 불러오는 문장입니다. `import numpy as np`는 NumPy를 `np`라는 이름으로 쓰겠다는 뜻입니다. 즉 import 문은 패키지를 설치하는 명령이 아니라, 이미 준비된 코드를 현재 실행 문맥에 연결하는 Python 문장입니다.
- 왜 중요한가: 초심자는 `pip install`과 `import`를 같은 준비 과정으로 묶어 오해하기 쉽기 때문입니다. import 문을 구분하면 패키지 설치는 환경 관리이고, import는 Python 코드 실행 안의 연결 단계라는 점을 분리할 수 있습니다. 이 개념이 있어야 Colab 코드 셀, 로컬 터미널, Python 파일에서 무엇을 어디에 써야 하는지 더 안정적으로 판단합니다.
- 함께 볼 개념: `패키지(package)`, `pip`, `넘파이(NumPy)`
- 중심 Section: `P2-3.5`
- 등장 Section: `P2-3.6`
