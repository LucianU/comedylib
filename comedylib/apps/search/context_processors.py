from haystack.forms import SearchForm

def search_forms(request):
    return {'search_form': SearchForm()}
