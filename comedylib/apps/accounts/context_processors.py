from accounts.forms import SignUpForm, CustomAuthForm


def accounts_forms(request):
    return {'login_form': CustomAuthForm, 'signup_form': SignUpForm}
