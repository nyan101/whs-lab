# uv add beautifulsoup4
from bs4 import BeautifulSoup
import requests
from pprint import pprint

url = 'http://board.nyan101.com/sample/list'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# CSS 선택자를 사용하여 게시글 목록 추출
posts = soup.select('body > div > div.bg-white.rounded-lg.shadow-md.p-6 > ul')[0]

# 게시글 목록에서 제목 추출
titles = posts.select('li > a > div > h3')

pprint(titles)
