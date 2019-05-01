import json
import time
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import urllib.request
import re

def get_article_html(url):
    time.sleep(.200)
    html = urlopen(url)
    return html

def get_article_autor_date(article_body): 
    article_autor_date = article_body.find('div', class_="dodano-2").get_text()
    for a in article_body.find_all('div', class_="dodano-2"):
        if article_autor_date != a.get_text():
            article_autor_date="error"
    return article_autor_date
    
def article_to_dict(html):
    soup = BeautifulSoup(html, "html.parser")
    article_title = (soup.title).get_text()
    article_body = soup.find('div', class_="box-teksty-pokaz")
    """pewnie brzydko tego tutaj uzyc, ale nie chce jeszcze raz robic urlopen
    ani BeautifulSoup - nie wiem jak to sie powino zrobic
    i atrybut  statycznie przekazany oj..."""
    get_article_img(article_body, "https://www.wiz.pl/", article_title)
    #----------------------------
    p_dict = dict()
    for id, paragraph_text in enumerate(article_body.find_all('p')):
        p_dict['p'+str(id)]=paragraph_text.get_text()
    article_dic = {
        "title": article_title,
        "autor and date": get_article_autor_date(article_body),
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


main_url = "https://www.wiz.pl/"
url = "https://www.wiz.pl/8,2084.html"
get_json_file(url)


