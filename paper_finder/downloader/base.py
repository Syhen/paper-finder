# -*- coding: utf-8 -*-
"""
create on 2019-04-21 上午1:26

author @heyao
"""
import os

import requests
from pypac import PACSession
from pypac.parser import PACFile
from requests import Session
from requests.auth import HTTPProxyAuth


class BasePaperDownloader(object):
    DOMAIN = 'Base'
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/73.0.3683.86 Safari/537.36"

    def __init__(self, pac_url, username=None, password=None, force_download_pac=False, bath_path=None):
        self.pac_url = pac_url
        self.username = username
        self.password = password
        self.pac = self._load_pac(force_download=force_download_pac)
        self.bath_path = bath_path or ""

    def _download_pac(self):
        response = requests.get(self.pac_url)
        content = response.content
        return content

    def _load_pac(self, force_download=False):
        if not os.path.isfile("m100.pac") or force_download:
            pac_content = self._download_pac()
            with open("m100.pac", "w") as f:
                f.write(pac_content.decode("utf8"))
        with open("m100.pac", "r") as f:
            pac = PACFile(f.read())
        return pac

    def _download_url(self, url, user_agent=None, use_pac=False, headers=None):
        user_agent = user_agent or self.DEFAULT_USER_AGENT
        headers = headers or {}
        download_headers = {
            "User-Agent": user_agent,
        }
        download_headers.update(headers)
        if use_pac:
            session = PACSession(pac=self.pac, proxy_auth=HTTPProxyAuth(self.username, self.password))
        else:
            session = Session()
        response = session.get(url, headers=download_headers)
        return response
