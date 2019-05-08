import hashlib
import json
import os
import re
import requests
import shutil
import time

from bs4 import BeautifulSoup

REQUEST_LAG_SECONDS = .200
MAIN_URL = "https://www.wiz.pl/"

def get_soup(url):
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

    img_element = article_body.find('img', {'src': re.compile(r'jpg')})
    img_src = 'IMG_NOT_FOUND'
    if img_element:
        img_src = img_element['src']
    get_article_img(img_src)

    p_dict = dict()
    for id, paragraph_text in enumerate(article_body.find_all('p')):
        p_dict['p'+str(id)]=paragraph_text.get_text()
    
    article_dic = {
        "title": article_title,
        "author and date": get_article_author_date(article_body),
        "article_img": img_src,
        "body": p_dict
    }
    return article_dic

def get_article_img(img_src):
    if not os.path.exists(os.getcwd()+"/img/"):
        os.mkdir("img")
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

def get_edition_date(soup):
    #print("TYPE!!!!!!!!!: "+str(type(soup)))
    edition_title_date = soup.find('div', attrs={'style': 'margin-top: 0px;'})
    edition_date = "NONE"
    if edition_title_date:
        edition_date = re.findall(r'\d{2}/[12]\d{3}', str(edition_title_date.get_text()))
    return edition_date[0]

def get_edition_dict(soup):
    edition_dict = dict()
    edition_summary_dict = dict()
    edition_date = get_edition_date(soup)
    for p in soup.find_all('p'):
        if p:
            for strong_tag in p.find_all('strong'):
                if strong_tag:
                    edition_summary_dict[strong_tag.text] = strong_tag.next_sibling
                    #czasami będzie wpisane none
                    #trzeba poprawić to next_sibling
    img = soup.find('img', {'class': 'maxi-pokaz-cz'}, {'src': re.compile(r'jpg')})
    img_src = 'IMG_NOT_FOUND'
    if img:
        img_src = img['src']
    edition_dict = {
    'edition_date': edition_date,
    'edition_summary': edition_summary_dict,
    'edition_cover_image': img_src
    }
    return edition_dict

def get_json_page_dict(edition_list_page):
    edition_list_page_reg = '(10,.+html)$'
    article_list_page_reg = '8,.+html'
    page_dict = dict()
    page_dict_id = 0
    edition_list_links = get_link_list(edition_list_page_reg, get_soup(edition_list_page))
    for edition_link in edition_list_links:    
        article_list_links = get_link_list(article_list_page_reg, get_soup(edition_link))
        article_list = list()
        for article_link in article_list_links:
            article_soup = get_soup(article_link)
            article_list.append({str(article_soup.title): article_to_dict(article_soup)})  
        edition_dict = get_edition_dict(get_soup(change_to_summary_link(edition_link)))
        edition_dict['articles'] = str(article_list)
        edition_date = get_edition_date(get_soup(change_to_summary_link(edition_link)))
        page_dict[str(edition_date)] = str(edition_dict)
    return page_dict

def change_to_summary_link(edition_link):
    return re.sub(r'\/(\d{2}),', '/19,', edition_link, flags=re.IGNORECASE)

def get_json_file(edition_list_page):
    article_json = json.dumps(get_json_page_dict(edition_list_page))
    with open('page.json', 'w+') as out_f:
        json.dump(article_json, out_f, indent=2, sort_keys=True)


edition_list_page = "https://www.wiz.pl/18.html"
print("czas oczekiwania ok. 10 min.")
get_json_file(edition_list_page)

#print(get_edition_dict(get_soup("https://www.wiz.pl/19,270.html")))
#print(change_to_summary_link("https://www.wiz.pl/10,270.html"))