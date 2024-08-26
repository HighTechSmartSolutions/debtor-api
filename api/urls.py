from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import Action

urlpatterns = [
    path('action', Action.as_view(), name='Action'),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

# urlpatterns = format_suffix_patterns(urlpatterns)