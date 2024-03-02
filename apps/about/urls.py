from django.urls import path
from apps.about.views import AboutUsView, ContactsView

app_name = 'about'

urlpatterns = [
    path('', AboutUsView.as_view(), name='about_us'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
