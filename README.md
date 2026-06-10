# whs-lab

## 사전 준비

### Python 설치

https://www.python.org/downloads/ 에서 각자 환경에 맞는 버전 설치 권장

### (Optional) uv 설치

**Windows(Powershell)**

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Windows(WSL), Linux, MacOS**

```
curl -sSL https://install.python-poetry.org | python3 -
```

poetry를 설치한 경우, `pyproject.toml` 파일이 위치한 폴더에서 `poetry install` 을 실행하시면 필요한 패키지들이 자동으로 설치됩니다.

(별도 패키지 관리도구를 설치하지 않은 경우 `pip install -r requirements.txt` 로도 설치 가능합니다)
