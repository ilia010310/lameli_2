from django.urls import path
from apps.about.views import AboutUsView, ContactsView, call_back

app_name = 'about'

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('call_back/', call_back, name='call_back'),
    path('', AboutUsView.as_view(), name='about_us'),

]
