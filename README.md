# 니얼굴

니얼굴은 실시간으로 카메라에 비춰지는 사람의 얼굴에 이미지를 표시해주는 프로그램입니다.

## 실행 조건

- Python 3.8 이상(그 이하는 작동을 보장하지 않음)
- opencv-python 라이브러리 설치

```bash
pip install opencv-python
```

## 사용법

show_realtime_detection.py를 실행하면 0번 카메라를 사용하며 버튼으로 상호작용할 수 있습니다.

- A - 얼굴인식 모드 토글
- B - 눈 인식 모드 토글(얼굴인식 모드 켜져있을 때)
- C - 페페 오버레이 모드 토글(얼굴인식 모드 켜져있을 때)
- D - 이사장님 오버레이 모드 토글(얼굴인식 모드가 켜져있고, 페페 오버레이 모드가 꺼져있을 때)

![사용법](/assets/yourface.gif)

테스트에 사용된 얼굴은 리포지토리 주인의 얼굴입니다.