
import hashlib
# import json
import os
import re
import requests
import time

from bs4 import BeautifulSoup


# @piotrek FIXME: move to the env.sh
MAIN_URL = "https://www.wiz.pl/"


def get_soup(url):
    time.sleep(float(os.environ['REQUEST_LAG_SECONDS']))
    html = requests.get(url).content

    return BeautifulSoup(html, "html.parser")


def get_image(soup, class_name):

    img_soup = soup.find(
        'img',
        {'class': class_name},
        {'src': re.compile(r'(\.jpg|\.png|\.jpeg|\.svg)$')})

    if img_soup:
        response = requests.get(str(MAIN_URL) + str(img_soup['src']))

        if response.status_code == 200:
            return response.content


def save_image_file(image_content):

    image_dir_path = os.path.join(os.getcwd(), 'img')

    if not os.path.exists(image_dir_path):
        os.mkdir(image_dir_path)

    filename = hashlib.md5(image_content).hexdigest()
    image_path = os.path.join(image_dir_path, str(filename) + '.jpg')
    with open(image_path, 'wb') as f:
        f.write(image_content)


# def get_img_name(img_from_request):
#     return str(hashlib.md5(img_from_request.content).hexdigest()) + '.jpg'


# def get_article_dict(soup, link):
#     article_title = soup.title.get_text()
#     article_body = soup.find('div', class_="box-teksty-pokaz")
#     p_dict = dict()
#     for id, paragraph_text in enumerate(article_body.find_all('p')):
#         p_dict['p' + str(id)] = paragraph_text.get_text()
#     article_author_date = article_body.find(
#         'div', class_="dodano-2").get_text()
#     img_from_request = get_img_from_request(soup, 'maxi-pokaz')
#     save_img_file(img_from_request)
#     article_dic = {
#         "title": str(article_title),
#         "author and date": str(article_author_date),
#         "article_link": str(link),
#         "article_img": str(get_img_name(img_from_request)),
#         "body": p_dict
#     }
#     return article_dic


# def get_link_list(reg, soup):
#     link_list = set()
#     # test------------------------------------------------
#     # number = 10
#     # ----------------------------------------------------
#     for link in soup.find_all('a', href=re.compile(reg)):
#         # if number == 0:
#         # break
#         # number -= 1
#         if 'href' in link.attrs:
#             link_list.add(str(MAIN_URL) + link.attrs['href'])
#     return link_list


# def change_to_summary_link(edition_link):
#     return re.sub(r'\/(\d{2}),', '/19,', edition_link, flags=re.IGNORECASE)


# def get_edition_date(soup):
#     edition_title_date = soup.find('div', attrs={'style': 'margin-top: 0px;'})  # noqa
#     edition_date = "NONE"
#     if edition_title_date:
#         edition_date = re.findall(
#             r'\d{2}/[12]\d{3}', str(edition_title_date.get_text()))
#     return edition_date[0]


# def get_edition_dict(soup, link):
#     edition_summary_dict = dict()
#     summary_body = soup.find('div', class_="box-czasopisma-pokaz")
#     for p in summary_body.find_all('p'):
#         if p:
#             for strong_tag in p.find_all('strong'):
#                 if strong_tag:
#                     text = re.sub(
#                         r'<br\/>|<\/strong>|<\/em>|<em>',
#                         '',
#                         str(strong_tag.next_sibling))
#                     edition_summary_dict[str(strong_tag.text)] = text
#                     # czasami będzie wpisane none
#                     # trzeba poprawić to next_sibling
#     img_from_request = get_img_from_request(soup, "maxi-pokaz-cz")
#     save_img_file(img_from_request)
#     edition_date = get_edition_date(soup)
#     edition_dict = {
#         'edition_date': str(edition_date),
#         'edition_link': str(link),
#         'edition_summary': edition_summary_dict,
#         'edition_cover_image': str(get_img_name(img_from_request))
#     }
#     return edition_dict


# def get_json_page_dict(edition_list_page):
#     edition_list_links = get_link_list(
#         '(10,.+html)$', get_soup(edition_list_page))
#     page_dict = dict()
#     for edition_link in edition_list_links:
#         article_list_links = get_link_list('8,.+html', get_soup(edition_link))  # noqa
#         article_list = list()
#         for article_link in article_list_links:
#             article_soup = get_soup(article_link)
#             article_list.append({
#                 str(article_soup.title.get_text()): get_article_dict(
#                     article_soup, article_link)
#             })
#         edition_dict = get_edition_dict(
#             get_soup(change_to_summary_link(edition_link)), edition_link)
#         edition_dict['articles'] = article_list
#         edition_date = get_edition_date(
#             get_soup(change_to_summary_link(edition_link)))
#         page_dict[str(edition_date)] = edition_dict
#     return page_dict


# def save_json_file(edition_list_page):
#     article_json = get_json_page_dict(edition_list_page)
#     with open('data.json', 'w+') as f:
#         json.dump(article_json, f)


# edition_list_page = "https://www.wiz.pl/18.html"
# print("czas oczekiwania ok. 10 min.")
# save_json_file(edition_list_page)
