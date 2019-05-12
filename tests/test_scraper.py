
import time
from unittest import TestCase
import os
import hashlib

import httpretty
import pytest
from bs4 import BeautifulSoup

from scraper import get_soup, get_image, save_image_file


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
