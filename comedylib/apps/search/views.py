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
            sorted(uniques.itervalues(), key=lambda x: x.score, reverse=True),
            key=lambda x: x.model_name
        )
        return grouped_results
