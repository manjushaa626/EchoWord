from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('addblog/', views.addblog, name='addblog'),
    path('blog_save/', views.blog_save, name='blog_save'),
    path('blog_detail/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blog_delete/<int:id>/',views.blog_delete,name='blog_delete'),
    path('blog_edit/<int:id>/',views.blog_edit,name='blog_edit'),
    path('blog_update/<int:pk>',views.blog_update,name='blog_update'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.blogs, name='blogs'),
]