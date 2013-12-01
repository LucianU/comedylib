from haystack.views import SearchView


class GroupedResultsSearchView(SearchView):
    """
    Groups the search results based on the object model that
    they represent.
    """
    def get_results(self):
        results = super(GroupedResultsSearchView, self).get_results()
        uniques = {}
        for result in results:
            uniques[result.id] = result

        grouped_results = sorted(
            uniques.itervalues(), key=lambda x: (x.score, x.model_name),
            reverse=True,
        )
        return grouped_results
