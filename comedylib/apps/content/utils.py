import logging
import urllib
import urlparse

import gdata.youtube.service

from django.core.files.base import ContentFile

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -- %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

def get_youtube_thumb(ident):
    logging.info("Retrieving thumbnail for video id %s from Youtube..." %
                  ident)
    yt_service = gdata.youtube.service.YouTubeService()
    entry = yt_service.GetYouTubeVideoEntry(video_id=ident)
    thumb = urllib.urlopen(entry.media.thumbnail[0].url).read()
    return thumb

sources = {
    'youtube.com': get_youtube_thumb,
}


def set_video_thumb(instance):
    url_bits = urlparse.urlparse(instance.url)
    source = url_bits.netloc.strip('www.')
    querydict = urlparse.parse_qs(url_bits.query)

    ident = querydict['v'][0]
    thumb = sources[source](ident)
    instance.picture.save('%s_%s' % (source, ident), ContentFile(thumb))
    return instance
