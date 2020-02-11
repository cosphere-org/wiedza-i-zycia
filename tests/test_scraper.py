import hashlib
import os
import time
from unittest import TestCase

from bs4 import BeautifulSoup
import httpretty
import pytest


from scraper import (
    change_to_summary_link,
    get_article_author_date,
    get_article_dict,
    get_edition_date,
    get_edition_dict,
    get_image,
    get_image_name,
    get_link_list,
    get_soup,
    get_table_of_contents,
    save_image_file,
)


class GetSoupTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixture(self, mocker):
        self.mocker = mocker

    @httpretty.activate
    def test_get_soup(self):

        sleep = self.mocker.patch.object(time, 'sleep')

        httpretty.register_uri(
            httpretty.GET,
            'https://www.wiz.pl/134.html',
            status=200,
            body='<div>welcome in wiz</div>')

        bs = get_soup('https://www.wiz.pl/134.html')

        assert sleep.call_count == 1
        assert bs == BeautifulSoup(
            b'<div>welcome in wiz</div>',
            'html.parser')


class GetImageTestCase(TestCase):

    def test_get_image__no_images_in_html(self):

        image = get_image(
            BeautifulSoup(
                b'<div>welcome in wiz</div>',
                'html.parser'),
            'my-image')

        assert image is None

    @httpretty.activate
    def test_get_image__single_image_in_html(self):

        httpretty.register_uri(
            httpretty.GET,
            (
                'https://www.wiz.pl/images/'
                'e5781trrt4633ed2i85q3yhu6achbwrgqow398e.jpg'),
            status=200,
            body='my.maxi.pokaz.bytes')

        image = get_image(
            BeautifulSoup(
                b'''
                    <img
                        style="margin-top: 10px;"
                        class="maxi-pokaz"
                        src="images/e5781trrt4633ed2i85q3yhu6achbwrgqow398e.jpg"
                        border="0">
                ''',  # noqa
                'html.parser'),
            'maxi-pokaz')

        assert image == b'my.maxi.pokaz.bytes'

    @httpretty.activate
    def test_get_image__many_images_in_html_always_return_first_one(self):

        httpretty.register_uri(
            httpretty.GET,
            'https://www.wiz.pl/elephant.jpg',
            status=200,
            body='my.elephant.bytes')
        httpretty.register_uri(
            httpretty.GET,
            'https://www.wiz.pl/lion.png',
            status=200,
            body='my.lion.bytes')
        httpretty.register_uri(
            httpretty.GET,
            'https://www.wiz.pl/cat.jpeg',
            status=200,
            body='my.cat.bytes')

        image = get_image(
            BeautifulSoup(
                b'''
                    <div>
                        <img class="my-image" src="elephant.jpg">
                        <img class="my-image" src="lion.png">
                        <img class="my-image" src="cat.jpeg">
                    </div>
                ''',
                'html.parser'),
            'my-image')

        assert image == b'my.elephant.bytes'


class SaveImageFileTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixture(self, mocker, tmpdir):
        self.mocker = mocker
        self.tmpdir = tmpdir

    def test_save_image_file(self):

        self.mocker.patch.object(
            os, 'getcwd').return_value = str(self.tmpdir)

        save_image_file(b'my.image.content')

        assert self.tmpdir.listdir() == [self.tmpdir.join('img')]
        expected_hash = hashlib.md5(b'my.image.content').hexdigest()
        expected_name = f'{expected_hash}.jpg'

        assert self.tmpdir.join('img').listdir() == [
            self.tmpdir.join('img').join(expected_name)
        ]
        assert self.tmpdir.join('img').join(
            expected_name).read('rb') == b'my.image.content'


class GetImageNameTestCase(TestCase):

    def test_get_image_name(self):
        assert get_image_name(b'test_image.content') == hashlib.md5(
            b'test_image.content').hexdigest() + '.jpg'


class GetArticleAuthorDate(TestCase):

    def test_get_article_author_date(self):
        wiz_author_date = BeautifulSoup(
            '''
            <div class="dodano-2" style="float: left;
            margin-bottom: 1px;">Autor: <strong>Magdalena
            Nowicka-Franczak</strong>
            |  dodano: 2019-04-24</div>
            '''.replace("\n", ""), 'html.parser')
        assert get_article_author_date(wiz_author_date) == (
            'Magdalena Nowicka-Franczak', '2019-04-24')

        wiz_author_date = BeautifulSoup(
            '''
            <div class="dodano-2" style="float: left;
            margin-bottom: 1px" ;="">dodano: 2019-03-20</div>
            '''.replace("\n", ""), 'html.parser')
        assert get_article_author_date(wiz_author_date) == (
            None, '2019-03-20')


class GetArticleDictTestCase(TestCase):

    def setUp(self):
        self.article_dict_lack = get_article_dict(BeautifulSoup(
            b'''
            <html>
                <body>
                    <p>This is a paragraph.</p>
                    <p>This is another paragraph.</p>
                </body>
            </html>
            ''',
            'html.parser'), 'https://www.wiz.pl')

        self.article_dict_full = get_article_dict(BeautifulSoup(
            '''
            <html>
                <body>
                    <div class="box-teksty-pokaz">
                        <div class="naglowek-teksty">Moc kłamstwa, urok plotki,
                        smak zemsty</div>
                        <div class="dodano-2">Autor: Przemek Berg | dodano:
                        2016-12-09</div>
                        <p>This is a paragraph.</p>
                        <p>This is another paragraph.</p>
                    </div>
                </body>
            </html>
            '''.encode('utf8'),
            'html.parser'), 'https://www.wiz.pl')

        self.article_dict_full = get_article_dict(BeautifulSoup(
            '''
            <html>
                <body>
                    <div class="box-teksty-pokaz">
                        <div class="naglowek-teksty">Moc kłamstwa, urok plotki,
                         smak zemsty</div>
                        <div class="dodano-2">Autor: Przemek Berg | dodano:
                        2016-12-09</div>
                        <p>This is a paragraph.</p>
                        <p>This is another paragraph.</p>
                    </div>
                </body>
            </html>
            ''',
            'html.parser'), 'https://www.wiz.pl')

    def test_get_article_dict__no_title(self):
        assert self.article_dict_lack.get('title') == 'None'

    def test_get_article_dict__no_article(self):
        assert self.article_dict_lack.get('body') == []

    def test_get_article_dict__no_author_and_date(self):
        assert self.article_dict_lack.get('author_and_date') == 'None'


class GetLinkListTestCase(TestCase):

    def test_get_link_list__no_links(self):
        links = get_link_list(
            '(10,.+html)$',
            BeautifulSoup(
                b'''
                <html>
                    <body>
                        <p>This is a paragraph.</p>
                        <p>This is another paragraph.</p>
                    </body>
                </html>
                ''',
                'html.parser'))
        for link in links:
            assert link is None

    def test_get_link_list__find_all_links(self):
        links = get_link_list(
            '(10,.+html)$',
            BeautifulSoup(
                b'''
                <html>
                    <body>
                        <p>This is a paragraph.</p>
                        <p>This is another paragraph.</p>
                        <a href='10,271.html'>
                        <a href='10,161.html'>
                        <a href='10,261.html'>
                        <a href='10,291.html'>
                    </body>
                </html>
                ''',
                'html.parser'))
        for link in links:
            assert link is not None


class ChangeToSummaryLinkTestCase(TestCase):

    def test_change_to_summary_link(self):
        assert change_to_summary_link(
            "https://www.wiz.pl/10,269.html") == 'https://www.wiz.pl/19,269.html' # noqa
        assert change_to_summary_link(
            "https://www.wiz.pl/10,251.html") == 'https://www.wiz.pl/19,251.html' # noqa


class GetEditionDateTestCase(TestCase):

    def test_get_edition_date__no_edition_date(self):
        assert get_edition_date(
            BeautifulSoup(
                b'''
                <html>
                    <body>
                        <p>This is a paragraph.</p>
                        <p>This is another paragraph.</p>
                        <a href='10,271.html'>
                        <a href='10,161.html'>
                        <a href='10,261.html'>
                        <a href='10,291.html'>
                    </body>
                </html>
                ''',
                'html.parser')) is None

    def test_get_edition_date__is_edition_date(self):
        assert get_edition_date(
            BeautifulSoup(
                '''
                <html>
                    <body>
                        <p>This is a paragraph.</p>
                        <p>This is another paragraph.</p>
                        <a href='10,271.html'>
                        <a href='10,161.html'>
                        <a href='10,261.html'>
                        <a href='10,291.html'>
                        <div style="margin-top: 0px;">
                            <div>Wiedza i Życie  03/2019</div>
                        </div>
                    </body>
                </html>
                ''',
                'html.parser')) == '03/2019'


class GetTableOfContentsTestCase(TestCase):

    def test_get_table_of_contents(self):
        table = BeautifulSoup(
        '''
            <div style="margin-bottom: 15px">
                <strong>Biometeorologia<br></strong>Siódme poty; Andrzej Hołdys<br><br>
                <strong>Fizjologia</strong><br>Kriorewolucja; Katarzyna Kornicka<br><br>
                <strong>Technika</strong><br>Węsząca elektronika; Justyna Jońca<br><br>
            </div>
        ''',  # noqa
        'html.parser')

        assert get_table_of_contents(table)[0] == {
                    'title': "Biometeorologia",
                    'subTitle': "Siódme poty; Andrzej Hołdys"
                    }
        assert get_table_of_contents(table)[1] == {
                    'title': "Fizjologia",
                    'subTitle': "Kriorewolucja; Katarzyna Kornicka"
                    }
        assert get_table_of_contents(table)[2] == {
                    'title': "Technika",
                    'subTitle': "Węsząca elektronika; Justyna Jońca"
                    }

    def test_get_table_of_contents__troublesome_case(self):
        table = BeautifulSoup(
        '''
            <p style="text-align: justify;"><strong>Astronomia</strong><br>Kosmiczny pan i pani Smith; Paweł Ziemnicki<strong><br></strong>
            </p><p style="text-align: justify;"><strong>Astronomia</strong><br>Niebo pełne tajemnic; Przemek Berg<strong><br></strong>
            </p><p style="text-align: justify;"><strong>Technika</strong><br>Dyktafon w pluszaku; Andrzej Janikowski<strong><br></strong>
            </p><p style="text-align: justify;"><strong>Neurobiologia</strong><br>Nieznana połowa mózgu – z dr. Michałem Ślęzakiem, specjalistą od gleju, rozmawia Olga Orzyłowska-Śliwińska<strong><br></strong>
            </p><p style="text-align: justify;"><strong>Chemia</strong><br>Jak to z tlenem było; Krzysztof Orliński</p>
        ''',  # noqa
        'html.parser')

        assert get_table_of_contents(table)[0] == {
                'title': "Astronomia",
                'subTitle': "Kosmiczny pan i pani Smith; Paweł Ziemnicki"
                }
        assert get_table_of_contents(table)[1] == {
                    'title': "Technika",
                    'subTitle': "Dyktafon w pluszaku; Andrzej Janikowski"
                    }
        assert get_table_of_contents(table)[3] == {
                    'title': "Chemia",
                    'subTitle': "Jak to z tlenem było; Krzysztof Orliński"
                    }


class GetEditionDictTestCase(TestCase):

    def test_get_edition_dict__find_summary_body(self):
        assert get_edition_dict(BeautifulSoup(
        '''
        <div class="box-czasopisma-pokaz">
            <img
                class="maxi-pokaz-cz"
                src="images/q7486a3ey2ttwe5ieu1o38hrdw5q6h3r893bgrc.jpg">
            <div style="padding-top: 35px; margin-bottom: 10px;">
                <strong>W numerze m.in.:</strong>
            </div>
                <div style="margin-bottom: 15px"><strong>Biometeorologia<br>
                    </strong>Siódme poty; Andrzej Hołdys<br><br><strong>Fizjologia
                    </strong><br>Kriorewolucja; Katarzyna Kornicka<br><br>
                    <strong>Technika</strong><br>Węsząca elektronika; Justyna Jońca<br><br>
                    <strong>Fizyka</strong><br>Dwa oblicza wody; Justyna Jońca&nbsp;
                </div>
        </div>
        ''',  # noqa
        'html.parser'), 'www.wiz.pl').get("table_of_contents") is not None

    def test_get_edition_dict__no_summary_body(self):
        assert get_edition_dict(
            BeautifulSoup(
                '''
                <div class="box-czasopisma-pokaz">
                    <img class="maxi-pokaz-cz" src="images/
                    q7486a3ey2ttwe5ieu1o38hrdw5q6h3r893bgrc.jpg">
                    <div style="padding-top: 35px; margin-bottom: 10px;">
                        <strong>W numerze m.in.:</strong>
                    </div>
                        <div style="margin-bottom: 15px">

                        </div>
                </div>
                ''',
                'html.parser'), 'www.wiz.pl').get("table_of_contents") == []


class GetJsonPageDictTestCase(TestCase):

    @httpretty.activate
    def test_get_json_page_dict(self):

        httpretty.register_uri(
            httpretty.GET,
            'https://www.wiz.pl/18.html',
            status=200,
            body='''
        <html>
            <body>
                <p>This is a paragraph.</p>
                <p>This is another paragraph.</p>
                <a href='10,271.html'>
                <a href='10,161.html'>
                <div style="margin-top: 0px;"><div>Wiedza i Życie
                03/2019</div></div>
            </body>
        </html>
        ''')

        httpretty.register_uri(
            httpretty.GET,
            'https://www.wiz.pl/10,271.html',
            status=200,
            body='''
        <html>
            <body>
                <p>This is a paragraph.</p>
                <p>This is another paragraph.</p>
                <a href='10,271.html'>
                <a href='10,161.html'>
                <a href='10,261.html'>
                <a href='10,291.html'>
                <div style="margin-top: 0px;"><div>Wiedza i Życie
                03/2019</div></div>
            </body>
        </html>
        ''')

    @httpretty.activate
    def test_get_json_page_dict__no_links(self):

        httpretty.register_uri(
            httpretty.GET,
            'https://www.wiz.pl/18.html',
            status=200,
            body='''
            <html>
                <body>
                </body>
            </html>
            ''')

        # assert get_json_page_dict() == 'No links'


class SaveJsonFileTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixture(self, mocker, tmpdir):
        self.mocker = mocker
        self.tmpdir = tmpdir

    # def test_save_json_file(self):

        # self.mocker.patch.object(
        #     os, 'getcwd').return_value = str(self.tmpdir)
        # save_json_file()

        # assert json.loads(self.tmpdir.join('data.json').read()) == {}
