# 🎮 Windows AutoClicker Master Pro

윈도우 온라인 상태 유지를 위한 가장 강력하고 정밀한 마우스 오토클리커입니다.  
사용자 친화적인 GUI 환경에서 클릭 간격, 실행 타이머, 조합 단축키 및 실시간 통계 기능을 제공합니다.

---

## ✨ 핵심 기능 (Key Features)

- **정밀한 시간 제어**: 시(H), 분(M), 초(S), 밀리초(ms) 단위의 개별 입력 칸 제공.
- **실행 타이머 (Timer)**: 지정된 시간이 경과하면 프로그램이 자동으로 안전하게 종료됨.
- **조합 단축키 (Combination)**: `Ctrl`, `Shift`, `Alt` 등을 포함한 전역 조합키 드롭다운 선택.
- **확장형 통계 대시보드**: 총 클릭 횟수, 경과 시간, 남은 시간 및 클릭 수를 실시간으로 확인.
- **자리비움 방지 (Jiggle)**: 클릭 직전 미세하게 마우스를 움직여 윈도우 상태 감지 우회.
- **안전장치 (Fail-Safe)**: 마우스를 모니터 구석으로 밀면 즉시 비상 정지.

---

## 🚀 시작하기 (Getting Started)

### 1. 사전 준비 (개발자용)
- **Python 3.12+** 및 **Poetry**가 설치되어 있어야 합니다.

### 2. 설치 및 실행
```powershell
# 의존성 설치
poetry install

# GUI 실행
poetry run python autoclicker.py
```

### 3. EXE 파일 빌드
```powershell
# PyInstaller를 이용한 클린 빌드
.\venv\Scripts\pyinstaller --noconfirm --onefile --windowed --name "DiscordAutoClicker" --collect-all customtkinter autoclicker.py
```

---

## 🛠 사용 방법 (Usage)

1. **클릭 간격**: 마우스를 얼마나 자주 클릭할지 설정합니다.
2. **총 실행 시간**: 프로그램이 작동할 전체 시간을 설정합니다. (0 입력 시 무제한)
3. **단축키**: 보조키(Modifier)와 기본키(Key)를 조합하여 시작/종료 키를 정합니다.
4. **통계**: '통계 보기' 버튼을 눌러 실시간 진행 상황을 확인하세요.

---

## ⚠️ 주의 사항
- `FAILSAFE` 기능이 활성화되어 있습니다. 오동작 시 마우스를 모니터 가장 구석으로 밀면 즉시 중단됩니다.
- 클릭 간격이 너무 빠를 경우 시스템 부하가 발생할 수 있습니다 (권장: 5초 이상).
