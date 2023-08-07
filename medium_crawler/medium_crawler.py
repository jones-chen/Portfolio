import requests
from bs4 import BeautifulSoup

# 目标URL
url = 'https://medium.com/@jones_room'

# 发起请求
response = requests.get(url)

# 解析HTML内容
soup = BeautifulSoup(response.content, 'html.parser')

# 找到所有的文章标题元素
title_elements = soup.find_all('h2', class_='be')
print(title_elements)

# 提取并打印文章标题
for index, title_element in enumerate(title_elements, 1):
    title_text = title_element.get_text()
    print(f"Article {index}: {title_text}")
