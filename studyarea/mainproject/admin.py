from django.contrib import admin
from .models import ExtraField, UserOTP, Course, JoinCourse, CreatePost, Like, CommentPost,\
    DeletePost, UploadCsv, GiveAttendance

# Register your models here.


admin.site.register(UserOTP)
admin.site.register(ExtraField)
admin.site.register(Course)
admin.site.register(JoinCourse)
admin.site.register(CreatePost)
admin.site.register(Like)
admin.site.register(DeletePost)
admin.site.register(CommentPost)
admin.site.register(UploadCsv)
admin.site.register(GiveAttendance)


