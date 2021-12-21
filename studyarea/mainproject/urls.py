from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signupteacher', views.signupteacher, name='signupteacher'),
    path('signupstudent', views.signupstudent, name='signupstudent'),
    path('loginhome', views.loginhome, name='loginhome'),
    path('loginteacher', views.loginteacher, name='loginteacher'),
    path('loginstudent', views.loginstudent, name='loginstudent'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('teacherhome', views.teacherhome, name='teacherhome'),
    path('course', views.course, name='course'),
    path('insidecourse/<str:coursename>/', views.insidecourse, name='insidecourse'),
    path('createpost/<str:coursename>/', views.createpost, name='createpost'),
    path("likepost1/<str:coursename>/", views.likepost1, name='like_post1'),
    path("likepost2/<str:coursename>/", views.likepost2, name='like_post2'),
    path("deletepage/<int:pk>/", views.deletepage, name='deletepage'),
    path("deletecsvpage/<int:pk>/", views.deletecsvpage, name='deletecsvpage'),
    path("deletecoursepage/<str:coursename>/", views.deletecoursepage, name='deletecoursepage'),
    path("deletepost1/<int:pk>/", views.deletepost1, name='deletepost1'),
    path("deletecourse/<str:coursename>", views.deletecourse, name='deletecourse'),
    path("deletecsv/<int:pk>", views.deletecsv, name='deletecsv'),
    path("editpage", views.editpage, name='editpage'),
    path("editstupage", views.editstupage, name='editstupage'),
    path("edituser", views.edituser, name='edituser'),
    path("editstuuser", views.editstuuser, name='editstuuser'),
    path("addcomment1/<str:coursename>/", views.addcomment1, name='addcomment1'),
    path("addcomment2/<str:coursename>/", views.addcomment2, name='addcomment2'),
    path('studenthome', views.studenthome, name='studenthome'),
    path('stu_insidecourse/<str:coursename>/', views.stu_insidecourse, name='stu_insidecourse'),
    path('join_page', views.join_page, name='join_page'),
    path('join', views.join, name='join'),
    path('checkclasscode/<str:coursename>/', views.checkclasscode, name='checkclasscode'),
    path('uploadcsv/<str:coursename>/', views.uploadcsv, name='uploadcsv'),
    path('attendancecsv/<str:coursename>/', views.attendancecsv, name='attendancecsv'),
    path('giveattendance/<str:coursename>/', views.giveattendance, name='giveattendance'),
    path('checkattendance/<str:coursename>/', views.checkattendance, name='checkattendance'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgetpassword.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgetpassworddone.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='passwordresetconfirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='passwordresetcomplete.html'), name='password_reset_complete'),
    path('user/resendOTP', views.resendOTP, name='resendOTP'),
    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)