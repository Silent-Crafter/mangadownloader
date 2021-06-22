import requests.exceptions
from requests import get
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image


class MangaDownloader:

    _class = {
        'manganelo': 'reader-content',
        'readm': 'img-responsive scroll-down'
    }

    def __init__(self, source: str = 'manganelo', url: str = '', filename: str = '',
                 images: list = None, folder: Path = Path()) -> None:
        if images is None:
            images = []
        self.url = url
        self.filename = filename
        self.images = images
        self.newimages = []
        self.folder = folder
        self.manga = {
            'urls': [],
            'filenames': [],
        }
        self.source = source

    def get_manga(self, url: str = None) -> list:
        """
        Returns a list of urls of images to download

        :param url: url to get list from. Currently, only manganelo.com is supported
        :return: list of urls containing images
        :rtype: list
        """
        if url is not None:
            self.url = url

        self.source = self.url.split('.')[1]

        try:
            resp = get(self.url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            self.images = soup.find_all('img', class_=self._class[self.source])  # class_='reader-content'

        except requests.exceptions.ConnectionError:
            print('Network error occurred. Please check the URL/your connection')
            exit()

        except requests.exceptions.MissingSchema as ms:
            print(ms)
            exit()

        if len(self.images):
            for i in range(len(self.images)):
                self.images[i] = self.images[i].get('src')

            if self.source == 'readm':
                for i in range(len(self.images)):
                    self.images[i] = 'https://www.readm.org' + self.images[i]

            print(f'\nPages: {len(self.images)}')

            return self.images

        else:
            print('manga/chapter not found.')
            self.images = []
            return []

    def run_downloader(self, images: list, url: str, filename: str = 'temp') -> None:
        """

        :param images: list of urls of images
        :param url: url to use as a referer
        :param filename: filename of the pdf. also used to create a folder to store temp images.Default: temp
        """

        self.url = url
        self.images = images
        self.filename = filename
        self.folder = Path('.', f'{self.filename}')

        print('downloading...')

        if not self.folder.exists():
            self.folder.mkdir()

        try:
            for i in range(len(self.images)):
                file = Path('.', f'{self.folder}', f'{i+1}.jpg')

                if not file.exists():
                    with get(self.images[i], stream=True, headers={'referer': self.url}) as img:
                        with open(file, 'wb') as f:
                            for chunk in img.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)

                            print(self.images[i])

        except KeyboardInterrupt:
            self.cleanup()
            #: exit()

    def convert_to_pdf(self, images: list, filename: str) -> None:

        self.images = images
        self.filename = filename

        if self.folder.exists():

            for i in range(len(self.images)):
                file = Path('.', f'{self.filename}', f'{i+1}.jpg')
                image = Image.open(file)

                image.load()
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image)

                self.newimages.append(background)
                file.unlink()

            self.newimages[0].save(f'{self.filename}.pdf', save_all=True, append_images=self.newimages[1:])

            self.folder.rmdir()

            self.images = []
            self.newimages = []

            print(f'saved to {self.filename}.pdf\n')

    def cleanup(self):

        for i in range(len(self.images)):
            file = Path(self.folder, f'{i+1}.jpg')
            if file.exists():
                file.unlink()

        self.folder.rmdir()
        self.images = []

    def download_manga(self, manga: dict = None) -> None:
        try:
            if manga is not None:
                self.manga = manga

            if not self.manga['urls']:
                raise self.InvalidManga

            for i in range(len(self.manga['urls'])):
                self.images = self.get_manga(self.manga['urls'][i])

                if not self.images == []:
                    self.run_downloader(images=self.images, url=self.url, filename=self.manga['filenames'][i])
                    self.convert_to_pdf(images=self.images, filename=self.manga['filenames'][i])

        except self.InvalidManga:
            print('invalid manga provided')

    def get_filename(self, url: str = None, optional_string: str = ''):

        self.source = url.split('.')[1]

        if optional_string != '':
            optional_string += '-'

        if self.source == 'manganelo':
            if url is not None:
                return optional_string + url.split('/')[-1]
            else:
                return optional_string + self.url.split('/')[-1]

        elif self.source == 'readm':
            if url is not None:
                return f"{optional_string}chapter-{url.split('/')[-2]}"
            else:
                return f"{optional_string}chapter-{self.url.split('/')[-2]}"

        else:
            print('unknown source. trying with the default')
            if url is not None:
                return url.split('/')[-1]
            else:
                return self.url.split('/')[-1]

    class InvalidManga(Exception):
        pass


if __name__ == '__main__':

    downloader = MangaDownloader()

    _manga = downloader.manga

    urls = _manga['urls']
    filenames = _manga['filenames']

    try:
        for count in range(int(input('How many chapters?: '))):
            link = input(f'{count + 1}) URL: ')
            if not link == '':
                fname = link.split('/')[-1]
                urls.append(link)
                filenames.append(fname)

    except KeyboardInterrupt:
        print('\nInput aborted. downloading given URLs instead...')

    except ValueError:
        print('please enter a number')
        exit()

    downloader.download_manga()
