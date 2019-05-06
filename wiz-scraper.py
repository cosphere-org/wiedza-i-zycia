import json
import os
import re
import requests
import shutil
import time

from bs4 import BeautifulSoup

REQUEST_LAG_SECONDS = .200
MAIN_URL = "https://www.wiz.pl/"

def get_article_soup(url):
    time.sleep(REQUEST_LAG_SECONDS)
    html = requests.get(url).content
    return BeautifulSoup(html, "html.parser")

def get_article_author_date(article_body):
    article_author_date = article_body.find('div', class_="dodano-2").get_text()
    for a in article_body.find_all('div', class_="dodano-2"):
        if article_author_date != a.get_text():
            article_author_date="error"
            break
    return article_author_date

def article_to_dict(soup):
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
    if not os.path.exists(os.getcwd()+"/img/"):
        os.mkdir("img")
    img_element = article_body.find('img', {'src': re.compile(r'jpg')})
    if img_element:
        img_src = img_element['src']
        img = requests.get(str(main_url)+str(img_src), stream=True)
        if img.status_code == 200:
            with open(os.getcwd()+"/img/"+str(article_title)+".jpg", 'wb') as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)  

def get_link_list(reg, soup):
    link_list = set()
    for link in soup.find_all('a', href=re.compile(reg)):
        if 'href' in link.attrs:
            link_list.add(str(MAIN_URL)+link.attrs['href'])        
    return link_list

def get_json_page_dict(edition_list_page):
    edition_list_page_reg = '(10,.+html)$'
    article_list_page_reg = '8,.+html'
    page_dict = dict()
    page_dict_id = 0
    edition_list_links = get_link_list(edition_list_page_reg, get_article_soup(edition_list_page))
    for edition_link in edition_list_links:
        article_list_links = get_link_list(article_list_page_reg, get_article_soup(edition_link))
        for article_link in article_list_links:
            page_dict[str(page_dict_id)] = article_to_dict(get_article_soup(article_link))
            page_dict_id += 1
    return page_dict

def get_json_file(edition_list_page):
    article_json = json.dumps(get_json_page_dict(edition_list_page))
    with open('page.json', 'w+') as out_f:
        json.dump(article_json, out_f)


edition_list_page = "https://www.wiz.pl/18.html"
print("czas oczekiwania ok. 10 min.")
get_json_file(edition_list_page)