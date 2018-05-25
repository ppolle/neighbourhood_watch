from django.conf.urls import url
from . import views


urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^createHood/$', views.createHood, name='createHood'),
    url(r'^editHood/(\d+)',views.editHood,name="editHood"),
    url(r'^createBusiness/$',views.createBusiness,name= 'createBusiness'),
    url(r'^allBusinesses/$',views.businessIndex,name= 'allBusinesses'),
    url(r'^profile/$',views.profile,name = 'profile'),
    url(r'^editProfile/$',views.editProfile,name= 'editProfile'),
    url(r'^editBusiness/(\d+)',views.editBusiness,name = 'editBusiness'),
    url(r'^search/$',views.search,name= 'search'),
    url(r'^join/(\d+)',views.join,name = 'joinHood'),
    url(r'^Hood-Home/(\d+)',views.hoodHome,name = 'hoodHome'),
]
