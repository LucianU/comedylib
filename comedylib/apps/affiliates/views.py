import json

from django.http import HttpResponse
from django.views.generic import View

from affiliates.search import offer_searcher


class Offers(View):
    def get(self, *args, **kwargs):
        keyword = self.request.GET.get('keyword')
        if keyword is not None:
            offers = offer_searcher.search(keyword, no_of_results=2)
        else:
            return HttpResponse(
                json.dumps({'status': 'ERROR', 'msg': 'Missing keyword'}),
                content_type='application/json',
            )
        return HttpResponse(json.dumps(offers), content_type='application/json')
