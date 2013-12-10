import logging
import urllib
import urlparse

from gdata.service import RequestError
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
    try:
        entry = yt_service.GetYouTubeVideoEntry(video_id=ident)
    except RequestError, e:
        logging.info("Error occurred while trying to retrieve video %s. "
                     "Got message %s" % (ident, e))
        return
    thumb = urllib.urlopen(entry.media.thumbnail[0].url).read()
    return thumb

sources = {
    'youtube.com': get_youtube_thumb,
}


def set_video_thumb(instance):
    # Finding the source of the video, to know where to retrieve
    # the thumbnail from
    url_bits = urlparse.urlparse(instance.url)
    source = url_bits.netloc.strip('www.')
    querydict = urlparse.parse_qs(url_bits.query)

    # This only applies to Youtube
    v_param = querydict.get('v')
    if v_param is not None:
        ident = v_param[0]
    else:
        logging.warning('Invalid Youtube URL %s' % instance.url)
        return instance

    thumb = sources[source](ident)
    if thumb is not None:
        instance.picture.save('%s_%s' % (source, ident), ContentFile(thumb))
    return instance
