# 니얼굴

니얼굴은 실시간으로 카메라에 비춰지는 사람의 얼굴에 이미지를 표시해주는 프로그램입니다.

## 실행 조건

- Python 3.8 이상(그 이하는 작동을 보장하지 않음)
- Anaconda 환경
- opencv-python, kivy 라이브러리 설치

```bash
pip install opencv-python
conda install kivy[full]
```

## 사용법

show_realtime_detection.py를 실행하면 0번 카메라를 사용하여 얼굴 위에 이미지를 덮어씌웁니다.

```bash
python show_realtime_detection.py (이미지 경로)
```

![사용법](/assets/yourface.gif)