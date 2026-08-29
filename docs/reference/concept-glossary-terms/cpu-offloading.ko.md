<a id="cpu-offloading"></a>

### CPU offloading(CPU 오프로딩)

- 뜻: 모델 실행 중 모든 가중치와 중간 계산을 GPU VRAM에 계속 올려 두지 않고, 당장 쓰지 않는 module이나 가중치를 CPU 메모리 쪽에 두었다가 필요한 시점에 GPU로 옮기는 메모리 운용 방식입니다.
- 왜 중요한가: 큰 이미지 생성 모델이나 언어 모델을 제한된 GPU 메모리에서 실행할 때, 실행 가능성과 품질 판정을 분리해서 기록하게 해 주기 때문입니다. CPU offloading은 out-of-memory 위험을 줄일 수 있지만, 모델의 prompt 이해력이나 생성 품질을 직접 높이는 방법은 아닙니다.
- 함께 볼 개념: `계산 한계(computational limit)`, `텐서(tensor)`, `추론(inference)`, `오픈웨이트 모델(open-weight model)`
- 중심 Section: `P6-21.2`
- 등장 Section: `P7-5.1`, `P7-5.2`, `P7-5.3`, `P7-5.11`
