import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, parse_qsl

DB_PATH = Path(__file__).parent / 'My Chrome History'

WEBKIT_EPOCH = datetime(1601, 1, 1)

def webkit_to_kst(ts):
    return WEBKIT_EPOCH + timedelta(microseconds=ts) + timedelta(hours=9)


# 언어 코드 → 한글 이름
LANG_NAMES = {
    'auto':  '자동감지',
    'ko':    '한국어',
    'en':    '영어',
    'ja':    '일본어',
    'zh-CN': '중국어(간체)',
    'zh-TW': '중국어(번체)',
    'es':    '스페인어',
    'fr':    '프랑스어',
    'de':    '독일어',
    'ru':    '러시아어',
    'vi':    '베트남어',
    'th':    '태국어',
    'ar':    '아랍어',
    'ny':    '치체와어',
    'zu':    '줄루어',
}

def lang_name(code):
    return f'{code}({LANG_NAMES.get(code, "?")})'


# ----- 1. 데이터 로드 -----
con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("""
    SELECT v.visit_time, u.url
    FROM visits v JOIN urls u ON v.url = u.id
    WHERE u.url LIKE '%translate.google%'
      AND u.url LIKE '%text=%'
    ORDER BY v.visit_time ASC
""")
rows = cur.fetchall()
con.close()
print(f'[+] {len(rows)} translate requests')
print()


# ----- 2. URL에서 sl, tl, text 추출 -----
records = []  # [(시각, sl, tl, 원문)]
for ts, url in rows:
    p = urlparse(url)
    params = dict(parse_qsl(p.query))
    text = params.get('text', '').strip()
    if not text:
        continue
    records.append((webkit_to_kst(ts), params.get('sl', ''), params.get('tl', ''), text))


# ----- 3. 같은 원문이 여러 번 기록된 경우 묶기 -----
# 키: (sl, tl, 원문)  →  값: [횟수, 가장 최근 시각]
counts = {}
latest_time = {}
for dt, sl, tl, text in records:
    key = (sl, tl, text)
    counts[key] = counts.get(key, 0) + 1
    if key not in latest_time or dt > latest_time[key]:
        latest_time[key] = dt


# ----- 4. 최근 시각 순으로 출력 -----
keys_sorted = sorted(counts.keys(), key=lambda k: latest_time[k], reverse=True)

import textwrap

WRAP_WIDTH = 80
INDENT = '    '

print(f'[+] Translation timeline ({len(counts)} unique entries, latest first)')
print()
for key in keys_sorted:
    sl, tl, text = key
    dt = latest_time[key]
    cnt = counts[key]
    print(f'{dt:%Y-%m-%d %H:%M}  (x{cnt:2d})  {lang_name(sl)} → {lang_name(tl)}')
    for line in text.splitlines() or ['']:
        wrapped = textwrap.wrap(line, width=WRAP_WIDTH) or ['']
        for w in wrapped:
            print(f'{INDENT}{w}')
    print()
