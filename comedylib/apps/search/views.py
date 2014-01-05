from haystack.views import SearchView


class CustomSearchView(SearchView):
    """
    Changes the name of the 'page' context object so that it can be
    used with the pagination template.
    """
    def get_context_data(self, **kwargs):
        context = super(CustomSearchView, self).get_context_data(**kwargs)
        context['page_obj'] = context['page']
        return context
