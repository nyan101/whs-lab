# uv add tqdm
from tqdm import tqdm
import requests
from pprint import pprint

total_comments = []
num_posts = 100
for post_id in tqdm(range(1, num_posts + 1)):
    url = f'http://board.nyan101.com/comments/{post_id}'
    response = requests.get(url)
    comments = response.json()
    total_comments.extend(comments)

pprint(total_comments)
print(f'[+] get {len(total_comments)} comments')
