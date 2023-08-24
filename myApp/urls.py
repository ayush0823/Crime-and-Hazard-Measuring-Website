from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('postIncident/', views.PostIncident, name='PostIncident'),
    path('postProperty/', views.PostProperty, name='PostProperty'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('seeprofile/<str:ProfileID>', views.SeeProfiles, name='SeeProfiles'),
    path('changePassword/', views.Changepassword, name='Changepassword'),
    path('upvote/<str:PostID>', views.Upvote, name='Upvote'),
    path('downvote/<str:PostID>', views.Downvote, name='Downvote'),
    path('IncidentFeed/', views.IncidentFeed, name='IncidentFeed'),
    path('PropertyFeed/', views.PropertyFeed, name='PropertyFeed'),
    path('searchIncident/', views.SearchIncident, name='SearchIncident'),
    path('searchProperty/', views.SearchProperty, name='SearchProperty'),
    path('myPosts/', views.myPost, name='myPost'),
    path('SeeIncident/<str:PostID>', views.SeeIncident, name='SeeIncident'),
    path('SeeProperty/<str:PostID>', views.SeeProperty, name='SeeProperty')
]