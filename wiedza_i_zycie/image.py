
import hashlib
import os
import re
import click

import requests


class Image:

    def __init__(self, main_url, page, class_name):
        self.main_url = main_url
        self.page = page
        self.class_name = class_name

    def download(self):

        img = self.page.find(
            'img',
            {'class': self.class_name},
            {'src': re.compile(r'(\.jpg|\.png|\.jpeg|\.svg)$')})

        if img:
            url = os.path.join(self.main_url, img['src'])
            response = requests.get(url)

            if response.status_code == 200:
                self.content = response.content

                try:
                    return self.save()

                except AttributeError:
                    click.secho(f'[ERROR] No Image for: {url}', fg='red')

                    return None

    def save(self):

        images_path = os.path.join(
            os.path.dirname(__file__), 'data', 'images')
        if not os.path.exists(images_path):
            os.mkdir(images_path)

        filename = f'{hashlib.md5(self.content).hexdigest()}.jpg'
        with open(os.path.join(images_path, filename), 'wb') as f:
            f.write(self.content)

        return filename
