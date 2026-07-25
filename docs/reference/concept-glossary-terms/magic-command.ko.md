<a id="magic-command"></a>

### 매직 명령(magic command)

- 뜻: Jupyter나 Colab 코드 셀에서 `%pip`처럼 `%` 기호와 함께 쓰는 특수 명령입니다. 일반 Python 문법이라기보다, 노트북 커널이나 실행 환경에 특정 작업을 요청하는 셀용 명령으로 이해하면 됩니다. 즉 매직 명령은 Python 파일에 그대로 넣는 코드가 아니라 노트북 실행 자리에서 쓰는 환경 제어 문장입니다.
- 왜 중요한가: `%pip install numpy`를 Python 코드나 로컬 터미널 명령과 혼동하면 실행 위치 오류가 생기기 때문입니다. 매직 명령을 구분하면 `설치 명령`, `터미널 명령`, `Python import 문`을 서로 다른 실행 자리의 문장으로 읽을 수 있습니다. 이 개념은 Colab 예제를 로컬 PC로 옮길 때 특히 중요합니다.
- 함께 볼 개념: `코드 셀(code cell)`, `pip`, `주피터(Jupyter)`, `콜랩(Colab)`
- 중심 Section: `P2-3.5`
- 등장 Section: `P2-3.6`
