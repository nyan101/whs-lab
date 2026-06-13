import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import platform
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / 'My Chrome History'

# Chrome 시간값(WebKit timestamp)은 1601-01-01 UTC 기준 마이크로초.
# UTC 시각을 구한 뒤 한국 시간(+9h)으로 변환
WEBKIT_EPOCH = datetime(1601, 1, 1)

def webkit_to_kst(ts: int) -> datetime:
    return WEBKIT_EPOCH + timedelta(microseconds=ts) + timedelta(hours=9)


# ----- 1. 방문 시각만 추출 -----
con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("""
    SELECT visit_time
    FROM visits
    WHERE visit_time > 0
    ORDER BY visit_time ASC
""")
visit_times = [webkit_to_kst(r[0]) for r in cur.fetchall()]
con.close()
print(f'[+] {len(visit_times)} visits loaded (converted to KST)')


# ----- 2. 일자 범위 결정 -----
start_date = visit_times[0].date()
end_date = visit_times[-1].date()
num_days = (end_date - start_date).days + 1
print(f'[+] period: {start_date} ~ {end_date} ({num_days} days)')


# ----- 3. 행렬 채우기 (행: 시간 0-23, 열: 일자 0..num_days-1) -----
matrix = np.zeros((24, num_days), dtype=int)
for dt in visit_times:
    day_idx = (dt.date() - start_date).days
    matrix[dt.hour, day_idx] += 1


# ----- 4. 시각화 -----
if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 일자가 많아도 가독성 유지: 일수에 비례해 그래프 너비 결정 (최소 12)
fig, ax = plt.subplots(figsize=(max(12, num_days * 0.18), 8))
im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', interpolation='nearest')
fig.colorbar(im, ax=ax, label='visits')

# Y축: 시간 (KST)
ax.set_yticks(range(24))
ax.set_yticklabels([f'{i:02d}' for i in range(24)])
ax.set_ylabel('hour (KST)')

# X축: 주 1회 (월요일마다) 라벨
xtick_positions = []
xtick_labels = []
for i in range(num_days):
    d = start_date + timedelta(days=i)
    if d.weekday() == 0:  # 월요일
        xtick_positions.append(i)
        xtick_labels.append(d.strftime('%m-%d'))
ax.set_xticks(xtick_positions)
ax.set_xticklabels(xtick_labels, rotation=45, ha='right')
ax.set_xlabel('date (Mondays)')

# 주말 열 배경 강조 (토=파랑, 일=빨강 계열, 반투명)
# axvspan(x_start, x_end): 세로 띠를 그림. 셀 중앙이 정수 i이므로 양쪽 0.5씩.
for i in range(num_days):
    d = start_date + timedelta(days=i)
    if d.weekday() == 5:    # 토요일
        ax.axvspan(i - 0.5, i + 0.5, color='steelblue', alpha=0.15)
    elif d.weekday() == 6:  # 일요일
        ax.axvspan(i - 0.5, i + 0.5, color='crimson', alpha=0.15)

# 셀 경계선: imshow는 셀 중앙이 정수 좌표라, 경계는 -0.5, 0.5, 1.5 ...
# minor tick을 셀 경계에 두고 그 위치에만 격자선을 그림.
ax.set_xticks(np.arange(-0.5, num_days, 1), minor=True)
ax.set_yticks(np.arange(-0.5, 24, 1), minor=True)
ax.grid(which='minor', color='gray', linewidth=0.3, alpha=0.5)
ax.tick_params(which='minor', length=0)

# 각 칸에 숫자 표시 (0은 생략, 진한 배경엔 흰 글씨)
vmax = matrix.max()
for hour in range(24):
    for day in range(num_days):
        count = matrix[hour, day]
        if count > 0:
            color = 'white' if count > vmax * 0.5 else 'black'
            ax.text(day, hour, str(count),
                    ha='center', va='center', color=color, fontsize=6)

ax.set_title(f'Chrome activity heatmap ({start_date} ~ {end_date}, KST)')
plt.tight_layout()
plt.show()
