from haystack.views import SearchView


class CustomSearchView(SearchView):
    """
    Adds the 'page' context object under the name of 'page_obj' as well,
    so that the view can use the pagination template.
    """
    def extra_context(self):
        (paginator, page) = self.build_page()
        return {'page_obj': page}
