from django.contrib.auth.views import login as auth_login

def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember', False):
            request.session.set_expiry(0)
    return auth_login(request, *args, **kwargs)
