from django.conf.urls import url, include



try:
    code_count = settings.HACKREF_CHARACTER_COUNT
except:
    code_count = 8


from .views import CodeTrackingView

from profiles.views import home

urlpatterns = [
    url(r'^(?P<code>[\w0-9]{0,' + str(code_count) + '})/$', 
            CodeTrackingView.as_view(), 
            name="ref-code-redirect"),
]
