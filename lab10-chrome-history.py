import sqlite3
from pathlib import Path

# Chrome History 주요 테이블:
#   - urls   : 방문한 URL 목록 (id, url, title, visit_count, last_visit_time)
#   - visits : 개별 방문 이벤트 (visit_time, urls.id를 FK로 참조)
#
DB_PATH = Path(__file__).parent / 'My Chrome History'


def defang(url: str) -> str:
    return (url.replace('http://', 'hxxp://')
               .replace('https://', 'hxxps://')
               .replace('.', '[.]'))


# DB 연결
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

N = 50
URL_WIDTH = 100
TITLE_WIDTH = 60

cur.execute(f'SELECT url, title FROM urls LIMIT {N}')
for url, title in cur.fetchall():
    masked = defang(url)
    if len(masked) > URL_WIDTH:
        masked = masked[:URL_WIDTH - 3] + '...'
    title = (title or '')
    if len(title) > TITLE_WIDTH:
        title = title[:TITLE_WIDTH - 3] + '...'
    print(f'{masked:<{URL_WIDTH}} | {title}')

con.close()
