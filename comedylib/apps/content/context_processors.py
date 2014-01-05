from urllib import urlencode

from django.template.defaultfilters import escape


def get_params(request):
    """
    Returns the current GET params in urlencoded form with the
    exception of the 'page' param which will be set in the template.
    This enables using pagination with filtering based on GET params.
    """
    params = dict(request.GET)
    params.pop('page', None)
    context = {'get_params': escape(urlencode(params, doseq=True))}
    return context

