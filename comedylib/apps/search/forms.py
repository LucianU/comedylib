from haystack.forms import SearchForm

class WildcardSearchForm(SearchForm):
    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.filter(
            text__startswith=self.cleaned_data['q']
        )

        if self.load_all:
            sqs = sqs.load_all()
        return sqs
