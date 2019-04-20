# -*- coding: utf-8 -*-
"""
create on 2019-04-21 上午1:27

author @heyao
"""
from __future__ import print_function

import os

from lxml.etree import HTML

from paper_finder.downloader.base import BasePaperDownloader


class ScienceDirectPaperDownloader(BasePaperDownloader):
    DOMAIN = 'ScienceDirect'

    def __init__(self, pac_url, username=None, password=None, force_download_pac=False, bath_path=None):
        super(ScienceDirectPaperDownloader, self).__init__(pac_url, username, password, force_download_pac, bath_path)

    def _download_homepage(self, url, user_agent=None):
        response = self._download_url(url, user_agent, use_pac=True)
        return response.content

    def parse_filename(self, html):
        sel = HTML(html)
        filename = sel.xpath('//span[@class="title-text"]/text()')[0]
        return filename

    def _parse_homepage(self, html):
        sel = HTML(html)
        href = sel.xpath('//div[@class="PdfDownloadButton"]/a/@href')[0]
        return 'https://www.sciencedirect.com' + href

    def _get_pdf_url(self, url):
        response = self._download_url(url, use_pac=True)
        sel = HTML(response.content)
        pdf_url = sel.xpath('//div[@id="redirect-message"]/p/a/@href')[0]
        return pdf_url

    def _download_pdf(self, url, filename):
        response = self._download_url(url, use_pac=False)
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
    # downloader = ScienceDirectPaperDownloader()
    # downloader.download("https://www.sciencedirect.com/science/article/pii/S1567422317300856")
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("urls", nargs="+")
    args = parser.parse_args()

    paper_downloader = ScienceDirectPaperDownloader()

    for url in args.urls:
        paper_downloader.download(url)
