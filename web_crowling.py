import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []  # 데이터를 저장할 빈 리스트

for post_number in range(100000, 100178):  # 원하는 범위 설정
    url = f'https://www.pgr21.com/freedom/{post_number}'
    resp = requests.get(url, verify=False)

    print(post_number)

    # 오류 처리를 통해 페이지가 존재하지 않는 경우 건너뛰기
    if resp.status_code != 200:
        print(f"Skipping post {post_number} (Page not found)")
        continue

    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    article_text = soup.find("div", class_="articleArea")
    
    # article_text가 None이면 페이지를 건너뛰기
    if article_text is None:
        print(f"Skipping post {post_number} (No article text)")
        continue

    article_text = article_text.get_text()
    article_text = article_text.replace("\n","")

    subject_element = soup.find("td", text="Subject")
    title = subject_element.find_next("td").text.strip()

    name_element = soup.find("td", text="Name")
    name = name_element.find_next("td").text.strip()

    data.append([post_number, title, name, article_text])

# 데이터를 DataFrame으로 변환
df = pd.DataFrame(data, columns=["Post Number", "Title", "Name", "Article"])

# 엑셀 파일로 저장
df.to_excel('data.xlsx', index=False)