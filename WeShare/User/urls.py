
from . import views
from django.urls import path

urlpatterns = [
    path('hello',views.hellouser),
    path('',views.login),
    path('register',views.register),
    path('info',views.info),
    path('successfull',views.successfull),
    path('home',views.home),
    path('logout',views.logout),
    path('addpost',views.addpost),
    path('about',views.about),
    path('timeline',views.timeline),
    path('photos',views.photos),
    path('forgot',views.forgot),
    path('updatepassword',views.updatepassword),
    path('save',views.save),
    path('friends/<id>',views.friends),
    path('following/<id>',views.following),
    path('editprofile/<id>',views.editprofile),
    path('edited/<id>',views.edited),
    path('finalpass',views.finalpass),




    #admin section 
    path('Admin',views.helloadmin),
]
