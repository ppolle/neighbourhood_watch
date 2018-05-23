from django.conf.urls import url
from . import views


urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^createHood/$', views.createHood, name='createHood'),
    url(r'^editHood/(\d+)', views.editHood, name='editHood'),
    url(r'^createBusiness/$',views.createBusiness,name= 'createBusiness'),
]