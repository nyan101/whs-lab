# uv add matplotlib
# uv add numpy
import numpy as np
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm
from datetime import datetime
from pprint import pprint

total_comments = []
num_posts = 100
for post_id in tqdm(range(1, num_posts + 1)):
    url = f'http://board.nyan101.com/comments/{post_id}'
    response = requests.get(url)
    comments = response.json()
    total_comments.extend(comments)

print(f'[+] get {len(total_comments)} comments')
print()

# 댓글 데이터 처리
# 계정별 댓글 목록 정리용
print(f'[+] processing...')
user_comments = {}
for comment in total_comments:
    author_id = comment['author_id']
    # 해당 댓글이 처음 등장한 경우 빈 리스트 초기화
    if author_id not in user_comments:
        user_comments[author_id] = []
    user_comments[author_id].append(comment)

# 계정 목록 출력
print(f'[+] get {len(user_comments.keys())} users')
print(f'[+] users : {user_comments.keys()}')
print()

# 시각화 대상 선정(첫 게정)
target_user_id = list(user_comments.keys())[0]
target_user_name = user_comments[target_user_id][0]['author_name']

# 시간대별 댓글 수 행렬 초기화(24시간 x 7일)
activity_matrix = np.zeros((24, 7), dtype=int)

for comment in user_comments[target_user_id]:
    # 댓글 작성 시간 추출
    dt = datetime.strptime(comment['created_at'], '%Y-%m-%d %H:%M')
    # 요일 계산
    weekday = dt.weekday()  # 0: 월요일, 6: 일요일
    # 시간대 계산
    hour = dt.hour
    # 해당 시간대의 댓글 수 증가
    activity_matrix[hour, weekday] += 1



# 시간대별 댓글 수 행렬 시각화
plt.figure(figsize=(6, 8))

# 한글폰트 깨짐 방지 (Windows에서는 'Malgun Gothic', MacOS에서는 'AppleGothic')
#plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['font.family'] ='AppleGothic'
plt.rcParams['axes.unicode_minus'] =False

# 그래프 표시
plt.imshow(activity_matrix, cmap='YlOrRd', aspect='auto')
plt.colorbar(label='활동 횟수')

# X축 눈금 설정(요일)
weekdays = ['월', '화', '수', '목', '금', '토', '일']
plt.xticks(range(7), weekdays)

# Y축 눈금 설정(시간대)
hours = [f'{i:02d}' for i in range(24)]
plt.yticks(range(24), hours)

# 그래프 제목 설정
plt.title(f'User #{target_user_id}({target_user_name})의 활동 패턴')

# 각 칸에 숫자 표시
"""
for hour in range(24):
    for weekday in range(7):
        if activity_matrix[hour, weekday] > 0:
            plt.text(weekday, hour, str(activity_matrix[hour, weekday]), ha='center', va='center', color='black')
"""

plt.tight_layout()
plt.show()
#plt.savefig(f'./{target_user_id}({target_user_name}).png', dpi=300, bbox_inches='tight')


