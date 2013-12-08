from django.conf.urls import include, patterns, url

from contact_form.views import ContactFormView

from feedback.forms import FeedbackForm


urlpatterns = patterns('',
    url(r'^$', ContactFormView.as_view(form_class=FeedbackForm),
        name='contact_form'),
    url(r'^', include('contact_form.urls')),
)
