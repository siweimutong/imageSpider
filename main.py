# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import argparse
import os
import ssl
from bs4 import BeautifulSoup
import urllib.request


class MySpider(object):
    def __init__(self):
        #self.headers = {
        #    'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) '
        #                  'Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
        #}
        self.opener = urllib.request.build_opener()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/55.0.2883.75 Safari/537.36'
        }
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                                 '(KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
        urllib.request.install_opener(self.opener)

    def run(self):
        self.get_target_urls()

    def get_target_urls(self):
        response = requests.get(self._url, headers=self.headers, verify=False)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        imgs = soup.find_all('img')
        # print(imgs)
        img_count = 1
        for img in imgs:
            imgsrc = img.get('ess-data')
            if imgsrc is None:
                continue
            filename = self._folder_path + str(img_count) + "." + imgsrc.split('.')[-1]
            # print(filename)
            if img_count > 0:
                self.get_target_images(imgsrc, filename)
            img_count = img_count + 1
        # print(imgs)

    def get_target_images(self, target_urls, filepath):
        print("Download Pic:" + filepath)
        # print(target_urls)
        urllib.request.urlretrieve(target_urls, filename=filepath)


    def set_url(self, url):
        self._url = url

    def set_folder_path(self, folder_path):
        self._folder_path = folder_path

    _folder_path = ''
    _url = ''


def main(url, folder_path):
    path = folder_path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    spider = MySpider()
    spider.set_folder_path(folder_path)
    spider.set_url(url)
    spider.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'please enter parameters'
    parser.add_argument("-u", "--URL", help="This is the url of web!", dest="url", type=str, default='')
    parser.add_argument("-f", "--Folder", help="This is the url of web!", dest="folder_path", type=str, default='')
    args = parser.parse_args()
    main(args.url, args.folder_path)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
