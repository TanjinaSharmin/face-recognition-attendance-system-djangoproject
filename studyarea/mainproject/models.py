from django.db import models
import os
from uuid import uuid4
from django.contrib.auth.models import User

# Create your models here.


# -------------------------------------- image rename function  --------------------------------------------------

def path_and_rename(instance, filename):
    upload_to = 'images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.stu_id:
        filename = '{}.{}'.format(instance.stu_id, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)



class ExtraField(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stu_id = models.CharField(max_length=250)
    stu_img = models.ImageField(upload_to=path_and_rename, blank=True)


    def __str__(self):
        return str(self.stu_id)

    def delete(self, *args, **kwargs):
        self.stu_img.delete()
        super().delete(*args, **kwargs)







# ----------------------------------- UserOTP Model ------------------------------------------------

class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    otp = models.SmallIntegerField()

    def __str__(self):
        return str(self.otp)

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=40, primary_key=True)
    course_code = models.CharField(max_length=40)
    class_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.course_name)

class JoinCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course)



class CreatePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250)
    file = models.FileField(upload_to='', blank=True, default=1)
    text = models.CharField(max_length=10, default="posted to")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="user_like")

    def __str__(self):
        return str(self.caption)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likepost = models.ForeignKey(CreatePost, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.likepost)

class DeletePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deletepost = models.ForeignKey(CreatePost, on_delete=models.CASCADE)


class CommentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(CreatePost, related_name="comments", on_delete=models.CASCADE)
    commentbody = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.commentbody)
    


def path_and_renamecsv(instance, filename):
    upload_to = 'attendance'
    ext = filename.split('.')[-1]
    # get filename
    if instance.date:
        filename = '{}.{}'.format(instance.date, ext)
    return os.path.join(upload_to, filename)


class UploadCsv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csvfile = models.FileField(upload_to=path_and_renamecsv, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.CharField(max_length=250)

    def __str__(self):
        return str(self.csvfile)


    def delete(self, *args, **kwargs):
        self.csvfile.delete()
        super().delete(*args, **kwargs)


class GiveAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    csvfile = models.ForeignKey(UploadCsv, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    date = models.CharField(max_length=250)
    time = models.CharField(max_length=250)



