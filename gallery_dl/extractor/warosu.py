# -*- coding: utf-8 -*-

# Copyright 2017-2023 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://warosu.org/"""

from .common import Extractor, Message
from .. import text


class WarosuThreadExtractor(Extractor):
    """Extractor for threads on warosu.org"""
    category = "warosu"
    subcategory = "thread"
    root = "https://warosu.org"
    directory_fmt = ("{category}", "{board}", "{thread} - {title}")
    filename_fmt = "{tim}-{filename}.{extension}"
    archive_fmt = "{board}_{thread}_{tim}"
    pattern = r"(?:https?://)?(?:www\.)?warosu\.org/([^/]+)/thread/(\d+)"
    example = "https://warosu.org/a/thread/12345"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.board, self.thread = match.groups()

    def items(self):
        url = "{}/{}/thread/{}".format(self.root, self.board, self.thread)
        page = self.request(url).text
        data = self.metadata(page)
        posts = self.posts(page)

        if not data["title"]:
            data["title"] = text.unescape(text.remove_html(
                posts[0]["com"]))[:50]

        yield Message.Directory, data
        for post in posts:
            if "image" in post:
                for key in ("w", "h", "no", "time", "tim"):
                    post[key] = text.parse_int(post[key])
                post.update(data)
                yield Message.Url, post["image"], post

    def metadata(self, page):
        boardname = text.extr(page, "<title>", "</title>")
        title = text.extr(page, 'filetitle" itemprop="name">', '<')
        return {
            "board"     : self.board,
            "board_name": boardname.rpartition(" - ")[2],
            "thread"    : self.thread,
            "title"     : title,
        }

    def posts(self, page):
        """Build a list of all post objects"""
        page = text.extr(page, '<div class="content">', '<table>')
        needle = '<table itemscope itemtype="http://schema.org/Comment">'
        return [self.parse(post) for post in page.split(needle)]

    def parse(self, post):
        """Build post object by extracting data from an HTML post"""
        data = self._extract_post(post)
        if "<span>File:" in post:
            self._extract_image(post, data)
            part = data["image"].rpartition("/")[2]
            data["tim"], _, data["extension"] = part.partition(".")
            data["ext"] = "." + data["extension"]
        return data

    @staticmethod
    def _extract_post(post):
        extr = text.extract_from(post)
        return {
            "no"  : extr('id="p', '"'),
            "name": extr('<span itemprop="name">', "</span>"),
            "time": extr('<span class="posttime" title="', '000">'),
            "now" : extr("", "<"),
            "com" : text.unescape(text.remove_html(extr(
                '<blockquote><p itemprop="text">', '</p></blockquote>'
            ).strip())),
        }

    @staticmethod
    def _extract_image(post, data):
        extr = text.extract_from(post)
        data["fsize"] = extr("<span>File: ", ", ")
        data["w"] = extr("", "x")
        data["h"] = extr("", ", ")
        data["filename"] = text.unquote(extr("", "<").rpartition(".")[0])
        extr("<br />", "")
        data["image"] = "https:" + extr('<a href="', '"')
