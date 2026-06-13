import platform
import shutil
from pathlib import Path

SYSTEM = platform.system()
HOME = Path.home()

if SYSTEM == 'Windows':
    SRC = HOME / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data' / 'Default' / 'History'
elif SYSTEM == 'Darwin':  # macOS
    SRC = HOME / 'Library' / 'Application Support' / 'Google' / 'Chrome' / 'Default' / 'History'
elif SYSTEM == 'Linux':
    SRC = HOME / '.config' / 'google-chrome' / 'Default' / 'History'
else:
    raise SystemExit(f'[-] Unsupported OS: {SYSTEM}')

DST = Path(__file__).parent / 'My Chrome History'

print(f'[+] OS: {SYSTEM}')
print(f'[+] source: {SRC}')
print(f'[+] dest:   {DST}')
print()

if not SRC.exists():
    print(f'[-] History file not found.')
    print(f'    Chrome may not have been used yet, or a different profile is in use.')
    raise SystemExit(1)

try:
    shutil.copy(SRC, DST)
    size_mb = DST.stat().st_size / (1024 * 1024)
    print(f'[+] copy done ({size_mb:.1f} MB)')
except PermissionError:
    print(f'[-] Permission error — the file may be locked because Chrome is running.')
    print(f'    Quit Chrome completely and try again.')
    raise SystemExit(1)
except Exception as e:
    print(f'[-] copy failed: {e}')
    raise SystemExit(1)
