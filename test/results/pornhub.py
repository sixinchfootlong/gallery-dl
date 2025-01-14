# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import pornhub
from gallery_dl import exception


__tests__ = (
{
    "#url"     : "https://www.pornhub.com/album/19289801",
    "#category": ("", "pornhub", "gallery"),
    "#class"   : pornhub.PornhubGalleryExtractor,
    "#pattern" : r"https://\w+.phncdn.com/pics/albums/\d+/\d+/\d+/\d+/",
    "#count"   : ">= 300",

    "id"     : int,
    "num"    : int,
    "score"  : int,
    "views"  : int,
    "caption": str,
    "user"   : "Danika Mori",
    "gallery": {
        "id"   : 19289801,
        "score": int,
        "views": int,
        "tags" : list,
        "title": "Danika Mori Best Moments",
    },
},

{
    "#url"     : "https://www.pornhub.com/album/69040172",
    "#category": ("", "pornhub", "gallery"),
    "#class"   : pornhub.PornhubGalleryExtractor,
    "#exception": exception.AuthorizationError,
},

{
    "#url"     : "https://www.pornhub.com/gif/33643461",
    "#category": ("", "pornhub", "gif"),
    "#class"   : pornhub.PornhubGifExtractor,
    "#pattern" : r"https://\w+\.phncdn\.com/pics/gifs/033/643/461/33643461a\.webm",

    "date"     : "dt:2020-10-31 00:00:00",
    "extension": "webm",
    "filename" : "33643461a",
    "id"       : "33643461",
    "tags"     : [
        "big boobs",
        "lana rhoades",
    ],
    "title"    : "Big boobs",
    "url"      : str,
    "user"     : "Lana Rhoades",
},

{
    "#url"     : "https://www.pornhub.com/pornstar/danika-mori",
    "#category": ("", "pornhub", "user"),
    "#class"   : pornhub.PornhubUserExtractor,
},

{
    "#url"     : "https://www.pornhub.com/pornstar/danika-mori/photos",
    "#category": ("", "pornhub", "photos"),
    "#class"   : pornhub.PornhubPhotosExtractor,
    "#pattern" : pornhub.PornhubGalleryExtractor.pattern,
    "#count"   : ">= 6",
},

{
    "#url"     : "https://www.pornhub.com/users/flyings0l0/photos/public",
    "#category": ("", "pornhub", "photos"),
    "#class"   : pornhub.PornhubPhotosExtractor,
},

{
    "#url"     : "https://www.pornhub.com/users/flyings0l0/photos/private",
    "#category": ("", "pornhub", "photos"),
    "#class"   : pornhub.PornhubPhotosExtractor,
},

{
    "#url"     : "https://www.pornhub.com/users/flyings0l0/photos/favorites",
    "#category": ("", "pornhub", "photos"),
    "#class"   : pornhub.PornhubPhotosExtractor,
},

{
    "#url"     : "https://www.pornhub.com/model/bossgirl/photos",
    "#category": ("", "pornhub", "photos"),
    "#class"   : pornhub.PornhubPhotosExtractor,
},

{
    "#url"     : "https://www.pornhub.com/pornstar/danika-mori/gifs",
    "#category": ("", "pornhub", "gifs"),
    "#class"   : pornhub.PornhubGifsExtractor,
    "#pattern" : pornhub.PornhubGifExtractor.pattern,
    "#count"   : ">= 42",
},

{
    "#url"     : "https://www.pornhub.com/users/flyings0l0/gifs",
    "#category": ("", "pornhub", "gifs"),
    "#class"   : pornhub.PornhubGifsExtractor,
},

{
    "#url"     : "https://www.pornhub.com/model/bossgirl/gifs/video",
    "#category": ("", "pornhub", "gifs"),
    "#class"   : pornhub.PornhubGifsExtractor,
},

)
