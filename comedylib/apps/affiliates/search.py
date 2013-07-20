import random

from django.conf import settings

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
        raw_results = self.api.search_n(no_of_results, Keywords=keyword,
                                        SearchIndex='Video')
        return self._format(raw_results)

    def _format(self, raw_results):
        results = []
        for raw_result in raw_results:
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
        results = []
        for searcher in self.searchers:
            results.extend(searcher.search(no_of_results, keyword))

        # If we don't have any search results, we just return
        # an empty list
        if not results:
            return results

        # If we have fewer results than the number expected, we
        # return all of them
        if randomly:
            if len(results) <= no_of_results:
                return results
            return random.sample(results, no_of_results)
        else:
            if len(results) <= no_of_results:
                return results
            return results[:no_of_results]


offer_searcher = OfferSearcher()
amazon_searcher = AmazonSearcher(
    settings.AMAZON_ACCESS_KEY,
    settings.AMAZON_SECRET_KEY,
    settings.AMAZON_ASSOCIATE_TAG
)
offer_searcher.register(amazon_searcher)
