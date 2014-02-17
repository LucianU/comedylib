import random
import urllib2

from django.conf import settings
from django.core.cache import cache
from django.template.defaultfilters import slugify

from amazon.api import AmazonAPI


class AmazonSearcher(object):
    def __init__(self, access_key, secret_key, associate_tag):
        self.access_key = access_key
        self.access_secret = secret_key
        self.associate_tag = associate_tag
        self.api = AmazonAPI(access_key, secret_key, associate_tag)

    def search(self, no_of_results, keyword):
        # The results for "Video" and "DVD" seem to be the same, so I'll
        # use "Video"
        try:
            raw_results = self.api.search_n(no_of_results, Keywords=keyword,
                                            SearchIndex='Video')
        except urllib2.HTTPError:
            return []

        return self._format(raw_results)

    def _passes_filter(self, result):
        # We filter for products without a price, because it means that
        # they're unavailable
        if result.price_and_currency[0] == 'None':
            return False
        return True

    def _format(self, raw_results):
        results = []
        for raw_result in raw_results:
            if not self._passes_filter(raw_result):
                continue

            result = {'title': raw_result.title,
                      'url': raw_result.offer_url,
                      'image_url': raw_result.small_image_url,
                      'price': '$%s' % raw_result.price_and_currency[0]}
            results.append(result)
        return results


class OfferSearcher(object):
    def __init__(self):
        self.searchers = []

    def register(self, searcher):
        self.searchers.append(searcher)

    def search(self, keyword, no_of_results, randomly=True):
        """
        Args:
        keyword - used for the search query
        no_of_results - the number of results that should be returned
        randomly - in case there are more results than desired, this
            specifies whether the results should be chosen randomly;
            if this is False, then the results are chosen starting from
            the beginning of the list
        Returns: a sequence
        """
        cache_key = 'af_k:%s_n:%s_r:%s' % (slugify(keyword), no_of_results,
                                           int(randomly))
        offers = cache.get(cache_key)
        if offers is not None:
            return offers

        results = []
        for searcher in self.searchers:
            results.extend(searcher.search(no_of_results, keyword))

        offers = []
        if results:
            # If we have fewer results than the number expected, we
            # return all of them
            if randomly:
                if len(results) <= no_of_results:
                    offers = results
                else:
                    offers = random.sample(results, no_of_results)
            else:
                if len(results) <= no_of_results:
                    offers = results
                else:
                    offers = results[:no_of_results]

        # We cache even an empty list, because we don't want to hit
        # the provider api for that keyword
        cache.set(cache_key, offers, 60 * 60)
        return offers


offer_searcher = OfferSearcher()
amazon_searcher = AmazonSearcher(
    settings.AMAZON_ACCESS_KEY,
    settings.AMAZON_SECRET_KEY,
    settings.AMAZON_ASSOCIATE_TAG
)
offer_searcher.register(amazon_searcher)
