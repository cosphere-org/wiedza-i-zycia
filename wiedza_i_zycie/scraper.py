'''wiedza i zycie - scraper'''
import hashlib
import json
import os
import re
import time
import requests

from bs4 import BeautifulSoup


def get_soup(url):
    time.sleep(float(os.environ['REQUEST_LAG_SECONDS']))
    html = requests.get(url).content
    print('---request---')

    return BeautifulSoup(html, "html.parser")


def get_image(soup, class_name):

    img_soup = soup.find(
        'img',
        {'class': class_name},
        {'src': re.compile(r'(\.jpg|\.png|\.jpeg|\.svg)$')})

    if img_soup:
        response = requests.get(str(os.environ['MAIN_URL']) + str(img_soup['src']))

        if response.status_code == 200:
            return response.content


def save_image_file(image_content):

    image_dir_path = os.path.join(os.getcwd(), 'img')

    if not os.path.exists(image_dir_path):
        os.mkdir(image_dir_path)
    if image_content:
        filename = hashlib.md5(image_content).hexdigest()
        image_path = os.path.join(image_dir_path, str(filename) + '.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_content)


def get_image_name(image_content):
    if image_content:
        return str(hashlib.md5(image_content).hexdigest()) + '.jpg'


def get_article_author_date(article_body):
    article_author_date = article_body.find(
            'div', class_="dodano-2").get_text()

    if article_author_date: 
        author = r'(Autor: (?P<author>(\w+[\s-])+\w+))'
        date = r'(dodano: (?P<date>(\d+[,-:\.\s]){3}))'

        article_author = re.search(author, article_author_date)
        if article_author:
            article_author = article_author.group('author')
        article_date = re.search(date, article_author_date)
        if article_date:
            article_date = article_date.group('date')
        return (article_author, article_date)



def get_article_dict(soup, link):
    try:
        article_title = soup.title.get_text()
    except AttributeError:
        article_title = None
    try:
        article_body = soup.find('div', class_="box-teksty-pokaz")
    except AttributeError:
        article_body = None
   
    p_list = list()
    article_author = None 
    article_date = None
    if article_body:
        for paragraph_text in article_body.find_all('p'):
            p_list.append(paragraph_text.get_text())

        article_author, article_date = get_article_author_date(article_body)

    image_content = get_image(soup, 'maxi-pokaz')
    save_image_file(image_content)

    article_dic = {
        "title": str(article_title),
        "article_author": str(article_author),
        "article_date": str(article_date),
        "article_link": str(link),
        "article_img": str(get_image_name(image_content)),
        "body": p_list
    }
    return article_dic


def get_link_list(reg, soup):
    link_list = set()
    # test------------------------------------------------
    #number = 10
    # ----------------------------------------------------
    for link in soup.find_all('a', href=re.compile(reg)):
        # if number == 0:
        #     break
        # number -= 1
        if 'href' in link.attrs:
            link_list.add(str(os.environ['MAIN_URL']) + link.attrs['href'])
    return link_list


def change_to_summary_link(edition_link):
    return re.sub(r'\/(\d{2}),', '/19,', edition_link, flags=re.IGNORECASE)


def get_edition_date(soup):
    edition_title_date = soup.find('div', attrs={'style': 'margin-top: 0px;'})  # noqa
    if edition_title_date:
        edition_date = re.findall(
            r'\d{2}/[12]\d{3}', str(edition_title_date.get_text()))
        return edition_date[0]


def get_table_of_contents(table):
    table_of_contents_list = list()
    if table:
        pretty_table = BeautifulSoup(re.sub(
                        r'<br\/>|<\/em>|<em>|\n', '', str(table)),
                        'html.parser')
    for strong in pretty_table.find_all("strong"):
        if strong:
            table_of_contents_list.append(
                dict({
                    'title' : str(strong.text),
                    'subTitle' : str(strong.next_sibling)
                    }))
    return  table_of_contents_list


def get_edition_dict(soup, link):
    summary_body = soup.find('div', class_="box-czasopisma-pokaz")
    if summary_body:
        table = summary_body.find('div', attrs={'style': 'margin-bottom: 15px'})
        table_of_contents_list = None
        if table:
            table_of_contents_list = get_table_of_contents(table)

    image_content = get_image(soup, "maxi-pokaz-cz")
    save_image_file(image_content)

    edition_dict = {
        'edition_date': str(get_edition_date(soup)),
        'edition_link': str(link),
        'table_of_contents': table_of_contents_list,
        'edition_cover_image': str(get_image_name(image_content))
    }
    return edition_dict


def get_json_page_dict():
    page_list = list()
    edition_list_links = get_link_list(
        '(10,.+html)$', 
        get_soup(os.environ['EDITION_LIST_PAGE']))
    if edition_list_links:
        for edition_link in edition_list_links:
            article_list_links = get_link_list('8,.+html', get_soup(edition_link))  # noqa
           
            article_list = list()
            for article_link in article_list_links:
                article_soup = get_soup(article_link)
                article_list.append(get_article_dict(article_soup, article_link))

            edition_dict = get_edition_dict(
                get_soup(change_to_summary_link(edition_link)), 
                edition_link)
            edition_dict['articles'] = article_list
            edition_date = get_edition_date(
                get_soup(change_to_summary_link(edition_link)))
            page_list.append(edition_dict)
        return page_list
    else: 
        return 'No links'


def save_json_file():
    article_json = get_json_page_dict()
    with open('data.json', 'w+') as f:
        json.dump(article_json, f)


print("czas oczekiwania powyżej 5 min.")
save_json_file()
