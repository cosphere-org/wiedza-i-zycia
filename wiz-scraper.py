from urllib.request import urlopen, urlretrieve
import json
import re
import time

from bs4 import BeautifulSoup

REQUEST_LAG_SECONDS = .200
MAIN_URL = "https://www.wiz.pl/"

def get_article_html(url):
    time.sleep(REQUEST_LAG_SECONDS)
    return urlopen(url)

def get_article_author_date(article_body): 
    article_author_date = article_body.find('div', class_="dodano-2").get_text()
    for a in article_body.find_all('div', class_="dodano-2"):
        if article_author_date != a.get_text():
            article_author_date="error"
            break
    return article_author_date
    
def article_to_dict(html):
    soup = BeautifulSoup(html, "html.parser")
    article_title = soup.title.get_text()
    article_body = soup.find('div', class_="box-teksty-pokaz")
    
    get_article_img(article_body, MAIN_URL, article_title)

    p_dict = dict()
    for id, paragraph_text in enumerate(article_body.find_all('p')):
        p_dict['p'+str(id)]=paragraph_text.get_text()
    article_dic = {
        "title": article_title,
        "author and date": get_article_author_date(article_body),
        "body": p_dict
    }
    return article_dic

def get_article_img(article_body, main_url, article_title):
    img_src = article_body.find('img', {'src': re.compile(r'jpg')})['src']
    urlretrieve(str(main_url)+str(img_src), str(article_title)+".jpg")

def get_json_file(url):
    article_json = json.dumps(article_to_dict(get_article_html(url)))
    with open('data.json', 'w+') as out_f:  
        json.dump(article_json, out_f)


url = "https://www.wiz.pl/8,2084.html"
get_json_file(url)


