# -*- coding: utf-8 -*-
"""
create on 2019-04-21 上午1:35

author @heyao
"""

from __future__ import print_function

import base64
import os

from lxml.etree import HTML

from paper_finder.downloader.base import BasePaperDownloader


class CnkiPaperDownloader(BasePaperDownloader):
    DOMAIN = 'Cnki'

    def __init__(self, pac_url, username=None, password=None, force_download_pac=False, bath_path=None):
        super(CnkiPaperDownloader, self).__init__(pac_url, username, password, force_download_pac, bath_path)
        self.basic_auth = 'Basic %s' % base64.b64encode(('%s:%s' % (username, password)).encode('utf8'))

    def _download_homepage(self, url, user_agent=None):
        response = self._download_url(url, user_agent, use_pac=True, headers={'Proxy-Authorization': self.basic_auth})
        return response.content

    def parse_filename(self, html):
        sel = HTML(html)
        filename = sel.xpath('//h2[@class="title"]/text()')[0]
        return filename

    def _parse_homepage(self, html):
        sel = HTML(html)
        href = sel.xpath('//a[@id="pdfDownF"]/@href')[0]
        return 'http://kns.cnki.net' + href

    def _get_pdf_url(self, url):
        return url

    def _download_pdf(self, url, filename):
        response = self._download_url(url, use_pac=True, headers={'Proxy-Authorization': self.basic_auth})
        with open(filename, "wb") as f:
            f.write(response.content)
        return True

    def download(self, url, user_agent=None):
        print("download homepage:", url)
        home_html = self._download_homepage(url, user_agent)
        pdf_redirect_url = self._parse_homepage(home_html)
        filename = self.parse_filename(home_html)
        print("download successfully, pdf title is:", filename)
        pdf_url = self._get_pdf_url(pdf_redirect_url)
        print("redirect to pdf download url:", pdf_url)
        self._download_pdf(pdf_url, os.path.join(self.bath_path, '%s.pdf' % filename))
        print("download successfully!")
        return True


if __name__ == '__main__':
    # downloader = CnkiPaperDownloader()
    # downloader.download("https://kns.cnki.net/KCMS/detail/10.1108.TP.20190416.0959.286.html")
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("urls", nargs="+")
    args = parser.parse_args()

    paper_downloader = CnkiPaperDownloader()

    for url in args.urls:
        paper_downloader.download(url)

