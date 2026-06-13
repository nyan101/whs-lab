import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, parse_qsl

DB_PATH = Path(__file__).parent / 'My Chrome History'

WEBKIT_EPOCH = datetime(1601, 1, 1)

def webkit_to_kst(ts: int) -> datetime:
    return WEBKIT_EPOCH + timedelta(microseconds=ts) + timedelta(hours=9)

def defang(s: str) -> str:
    return (s.replace('http://', 'hxxp://')
             .replace('https://', 'hxxps://')
             .replace('.', '[.]'))


# ----- 검색엔진 → 검색어 파라미터 키 매핑 -----
SEARCH_ENGINES = {
    'google.com':       'q',
    'www.google.com':   'q',
    'duckduckgo.com':   'q',
    'www.bing.com':     'q',
    'www.baidu.com':    'wd',
    'yandex.com':       'text',
    'search.naver.com': 'query',
}


# ----- 1. 데이터 로드 (visit_time과 url 조인하여 시간순) -----
con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("""
    SELECT v.visit_time, u.url
    FROM visits v JOIN urls u ON v.url = u.id
    WHERE v.visit_time > 0
    ORDER BY v.visit_time ASC
""")
rows = cur.fetchall()
con.close()
print(f'[+] {len(rows)} rows loaded')
print()


# ----- 2. 검색어 추출 (엔진별 최신순) -----
print('[+] Search timeline (latest per engine)')

# engine -> [(time, query), ...]
searches = defaultdict(list)
for ts, url in rows:
    p = urlparse(url)
    key = SEARCH_ENGINES.get(p.netloc)
    if not key or not p.query:
        continue
    params = dict(parse_qsl(p.query))
    q = params.get(key, '').strip()
    if q:
        searches[p.netloc].append((webkit_to_kst(ts), q))

for engine in sorted(searches.keys()):
    items = searches[engine]

    counts = {}        # 검색어 → 횟수
    latest_time = {}   # 검색어 → 가장 최근 시각
    for dt, q in items:
        counts[q] = counts.get(q, 0) + 1
        if q not in latest_time or dt > latest_time[q]:
            latest_time[q] = dt

    queries_sorted = sorted(counts.keys(), key=lambda q: latest_time[q], reverse=True)

    print(f'\n[{defang(engine)}] {len(items)} hits, {len(counts)} unique queries')
    for q in queries_sorted[:50]:
        print(f'  {latest_time[q]:%Y-%m-%d %H:%M}  (x{counts[q]:3d})  {q[:70]}')
print()
