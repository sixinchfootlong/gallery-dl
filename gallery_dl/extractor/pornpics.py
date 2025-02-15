# -*- coding: utf-8 -*-

# Copyright 2023 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.pornpics.com/"""

from .common import GalleryExtractor, Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?pornpics\.com(?:/\w\w)?"


class PornpicsExtractor(Extractor):
    """Base class for pornpics extractors"""
    category = "pornpics"
    root = "https://www.pornpics.com"
    request_interval = (0.5, 1.5)

    def __init__(self, match):
        super().__init__(match)
        self.item = match.group(1)

    def _init(self):
        self.session.headers["Referer"] = self.root + "/"

    def items(self):
        for gallery in self.galleries():
            gallery["_extractor"] = PornpicsGalleryExtractor
            yield Message.Queue, gallery["g_url"], gallery

    def _pagination(self, url, params=None):
        if params is None:
            # fetch first 20 galleries from HTML
            # since '"offset": 0' does not return a JSON response
            page = self.request(url).text
            for path in text.extract_iter(
                    page, 'class="rel-link" href="', '"'):
                yield {"g_url": self.root + path}
            del page
            params = {"offset": 20}

        limit = params["limit"] = 20

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": url if params["offset"] else self.root + "/",
            "X-Requested-With": "XMLHttpRequest",
        }

        while True:
            galleries = self.request(
                url, params=params, headers=headers).json()
            yield from galleries

            if len(galleries) < limit:
                return
            params["offset"] += limit


class PornpicsGalleryExtractor(PornpicsExtractor, GalleryExtractor):
    """Extractor for pornpics galleries"""
    pattern = BASE_PATTERN + r"(/galleries/(?:[^/?#]+-)?(\d+))"
    example = "https://www.pornpics.com/galleries/TITLE-12345/"

    def __init__(self, match):
        PornpicsExtractor.__init__(self, match)
        self.gallery_id = match.group(2)

    items = GalleryExtractor.items

    def metadata(self, page):
        extr = text.extract_from(page)

        return {
            "gallery_id": text.parse_int(self.gallery_id),
            "slug"      : extr("/galleries/", "/").rpartition("-")[0],
            "title"     : text.unescape(extr("<h1>", "<")),
            "channel"   : extr('>Channel:', '</a>').rpartition(">")[2],
            "models"    : text.split_html(extr(
                ">Models:", '<span class="suggest')),
            "categories": text.split_html(extr(
                ">Categories:", '<span class="suggest')),
            "tags"      : text.split_html(extr(
                ">Tags List:", ' </div>')),
            "views"    : text.parse_int(extr(">Views:", "<").replace(",", "")),
        }

    def images(self, page):
        return [
            (url, None)
            for url in text.extract_iter(page, "class='rel-link' href='", "'")
        ]


class PornpicsTagExtractor(PornpicsExtractor):
    """Extractor for galleries from pornpics tag searches"""
    subcategory = "tag"
    pattern = BASE_PATTERN + r"/tags/([^/?#]+)"
    example = "https://www.pornpics.com/tags/TAGS/"

    def galleries(self):
        url = "{}/tags/{}/".format(self.root, self.item)
        return self._pagination(url)


class PornpicsSearchExtractor(PornpicsExtractor):
    """Extractor for galleries from pornpics search results"""
    subcategory = "search"
    pattern = BASE_PATTERN + r"/(?:\?q=|pornstars/|channels/)([^/&#]+)"
    example = "https://www.pornpics.com/?q=QUERY"

    def galleries(self):
        url = self.root + "/search/srch.php"
        params = {
            "q"     : self.item.replace("-", " "),
            "lang"  : "en",
            "offset": 0,
        }
        return self._pagination(url, params)
