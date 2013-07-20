import random

from django.conf import settings

from amazon.api import AmazonAPI


class AmazonSearcher(object):
    def __init__(self, access_key, secret_key, associate_tag):
        self.access_key = access_key
        self.access_secret = secret_key
        self.associate_tag = associate_tag
        self.api = AmazonAPI(access_key, secret_key, associate_tag)

    def search(self, keyword, no_of_results):
        # The results for "Video" and "DVD" seem to be the same, so I'll
        # use "Video"
        return self.api.search_n(no_of_results, keyword, SearchIndex='Video')


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
            results.append(searcher.search(no_of_results, keyword))

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
