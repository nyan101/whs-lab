# whs-lab

## 사전 준비

### (권장) uv 설치

**Windows(Powershell)**

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Windows(WSL), Linux, MacOS**

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

uv를 설치한 경우, `pyproject.toml` 파일이 위치한 폴더에서 `uv sync` 를 실행하시면 필요한 파이썬 바이너라와 패키지들이 자동으로 설치됩니다.

### Python 직접 설치

https://www.python.org/downloads/ 에서 각자 환경에 맞는 버전 설치 권장