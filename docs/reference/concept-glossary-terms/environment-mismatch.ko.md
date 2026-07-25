<a id="environment-mismatch"></a>

### 환경 불일치(environment mismatch)

- 뜻: 패키지를 설치한 실행 환경과 코드를 실행하는 실행 환경이 서로 다른 상태입니다. 예를 들어 시스템 Python에 NumPy를 설치했지만 프로젝트 가상환경으로 실행하거나, Colab 런타임에 설치한 패키지를 로컬 PC에도 있는 것으로 착각하는 경우가 여기에 해당합니다.
- 왜 중요한가: `pip install은 성공했는데 import는 실패한다`는 초심자 오류의 핵심 원인일 때가 많기 때문입니다. 환경 불일치를 이해하면 설치 성공 여부만 보지 않고, 그 설치가 현재 코드를 실행하는 Python과 같은 환경을 기준으로 했는지 확인하게 됩니다. 결국 이 개념은 패키지 문제를 `설치했나`에서 `어디에 설치했고 어디에서 실행했나`로 바꿔 읽게 만드는 점검 기준입니다.
- 함께 볼 개념: `가상환경(virtual environment)`, `실행 환경(runtime)`, `import 문(import statement)`
- 중심 Section: `P2-7.9`
- 등장 Section:
