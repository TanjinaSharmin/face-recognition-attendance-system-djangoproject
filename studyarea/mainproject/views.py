import datetime
from datetime import date
from django.shortcuts import render, HttpResponse, redirect,  get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserOTP, Course, CreatePost, Like, CommentPost, DeletePost,\
    UploadCsv, GiveAttendance, ExtraField, JoinCourse
from django.contrib.auth import authenticate,  login, logout
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
import random
import cv2
import numpy as np
import face_recognition
import os
import glob
import pandas as pd
from datetime import datetime
import random
import string
import array
import csv

# Create your views here.

# ------------------------------------ home function ---------------------------------
def home(request):
    return render(request, 'signup.html')


# ------------------------------------ signupteacher function--------------------------------
def signupteacher(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)

            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                messages.success(request, "Successfully Signup")
                return redirect('/loginhome')

            else:
                messages.warning(request, "You enter worng OTP")
                return render(request, 'signup.html', {'otp': True, 'user': user})

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "username is already exists please try unique username")
            return redirect('/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already exists")
            return redirect('/')

        if len(username) < 5:
            messages.error(request, "Username mustbe more than 5 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('/')

        if len(password) < 8:
            messages.error(request, "Password mustbe more than 8 characters ")
            return redirect('/')

        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('/')

        else:
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()
            # otp create
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            message = f"Hello {user.username},\n Your OTP is {user_otp}\n Thanks!"
            send_mail(
                "EDUMAAT - Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently = False
            )

            return render(request, 'signup.html', {'otp': True, 'user': user})

    else:
        messages.error(request, "Try again")
        return redirect('/')

# ------------------------------------ signupstudent function--------------------------------
def signupstudent(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)

            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                messages.success(request, "Successfully Signup")
                return redirect('/loginhome')

            else:
                messages.warning(request, "You enter worng OTP")
                return render(request, 'signup.html', {'otp': True, 'user': user})

        username = request.POST['username']
        email = request.POST['email']
        stu_id = request.POST['stu_id']
        stu_img = request.FILES['stu_img']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "username is already exists please try unique username")
            return redirect('/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already exists")
            return redirect('/')

        if len(username) < 5:
            messages.error(request, "Username mustbe more than 5 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('/')

        if ExtraField.objects.filter(stu_id=stu_id).exists():
            messages.error(request, "This student id is already exists you are already registered")
            return redirect('/')

        if len(password) < 8:
            messages.error(request, "Password mustbe more than 8 characters ")
            return redirect('/')

        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('/')

        else:
            user = User.objects.create_user(username, email, password)
            extenduser = ExtraField(user=user, stu_id=stu_id, stu_img=stu_img)
            user.is_active = False
            user.save()
            extenduser.save()
            # otp create
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            message = f"Hello {user.username},\n Your OTP is {user_otp}\n Thanks!"
            send_mail(
                "EDUMAAT - Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently = False
            )

            return render(request, 'signup.html', {'otp': True, 'user': user})

    else:
        messages.error(request, "Try again")
        return redirect('/')

# ---------------------------------------- resendOTP function -------------------------------------

def resendOTP(request):
    if request.method == 'GET':
        user = request.GET['user']
        if User.objects.filter(username= user).exists() and not User.objects.get(username= user).is_active:
            user = User.objects.get(username=user)
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            message = f"Hello {user.username},\n Your OTP is {user_otp}\n Thanks!"
            send_mail(
                "EDUMAAT - Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            return HttpResponse("Resend")

    return HttpResponse("Can not send OTP")


# -------------------------------- loginhome function -----------------------------------------

def loginhome(request):
    return render(request, 'login.html')

# -------------------------------- loginteacher function ----------------------------------

def loginteacher(request):

    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)

            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                login(request, user)
                messages.success(request, "Successfully Login")
                return redirect('/teacherhome')

            else:
                messages.warning(request, "You enter worng OTP")
                return render(request, 'login.html', {'otp': True, 'user': user})

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/teacherhome')

        elif not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/loginhome")

        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username=username)
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            message = f"Hello {user.username},\n Your OTP is {user_otp}\n Thanks!"
            send_mail(
                "EDUMAAT - Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return render(request, 'login.html', {'otp': True, 'user': user})

        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/loginhome")

# --------------------------------- loginstudent function --------------------------------------------

def loginstudent(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)

            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                login(request, user)
                messages.success(request, "Successfully Login")
                return redirect('/studenthome')

            else:
                messages.warning(request, "You enter worng OTP")
                return render(request, 'login.html', {'otp': True, 'user': user})

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/studenthome')

        elif not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/loginhome")

        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username=username)
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            message = f"Hello {user.username},\n Your OTP is {user_otp}\n Thanks!"
            send_mail(
                "EDUMAAT - Verify Your Email",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return render(request, 'login.html', {'otp': True, 'user': user})

        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/loginhome")

# --------------------------------- logout_user function ------------------------------------------

def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('/')

# -------------------------------------- teacherhome function -------------------------------------

def teacherhome(request):
    user = request.user
    course = Course.objects.filter(user=user)

    context = {'user': user, 'course': course}

    return render(request, 'teacherhome.html', context)


def course(request):
    if request.method == 'POST':
        coursename = request.POST['name']
        coursecode = request.POST['coursecode']
        number = 6 # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=number))




        if Course.objects.filter(course_name=coursename).exists():
            messages.error(request, "Course is already exists, please try unique name")
            return redirect('/teacherhome')

        if request.user.is_authenticated:
            user = request.user
            create_obj = Course(course_name=coursename, course_code=coursecode, user=user, class_code=code)
            create_obj.save()
            messages.success(request, "Successfully added")
            return redirect("/teacherhome")

    else:
        messages.error(request, "Something went wrong please try again")
        return redirect("/teacherhome")

def insidecourse(request, coursename):
    if request.user.is_authenticated:
        user = request.user
        insidecourse = Course.objects.filter(course_name=coursename)
        code = Course.objects.filter(course_name=coursename).first().class_code
        posts = CreatePost.objects.filter(course=coursename)
        today_date = date.today()
        today = today_date.strftime("%d/%m/%Y")
        csvfile = UploadCsv.objects.filter(course=coursename)

        context = {'coursename': coursename, 'insidecourse': insidecourse, 'code': code, 'posts': posts, 'today_date': today_date, 'csvfile': csvfile}
        return render(request, 'insidecourse.html', context)
    else:
        return render(request, 'insidecourse.html')


def createpost(request, coursename):
    if request.method == 'POST':
        coursecaption = request.POST['course_caption']
        coursefile = request.FILES.get('course_file', '')
        course_id = request.POST['course_name']
        course = Course.objects.get(course_name=course_id)

        if request.user.is_authenticated:
            user = request.user
            post_obj = CreatePost(caption=coursecaption, file=coursefile, user=user, course=course)
            post_obj.save()
            messages.success(request, "Successfully posted")
            return redirect(f'/insidecourse/{coursename}')
    else:
        messages.error(request, "Something went wrong please try again")
        return redirect(f'/insidecourse/{coursename}')


def likepost1(request, coursename):

    if request.method == 'POST':
        user = request.user
        likepost_id = request.POST.get('post_id')
        likepost_obj = CreatePost.objects.get(id=likepost_id)

        if user in likepost_obj.likes.all():
            likepost_obj.likes.remove(user)

        else:
            likepost_obj.likes.add(user)

        if request.user.is_authenticated:
            like_obj = Like(user=user, likepost=likepost_obj)
            like_obj.save()
            return redirect(f'/insidecourse/{coursename}')

def deletepage(request, pk):
    if request.user.is_authenticated:
        post = CreatePost.objects.filter(id=pk)
        return render(request, 'deletepost.html', {'post': post})

def deletepost1(request, pk):
    if request.user.is_authenticated:
        delpost_obj = CreatePost.objects.get(id=pk)
        delpost_obj.delete()
        messages.info(request, 'post deleted')
        return redirect(f'/deletepage/{pk}')

def deletecsvpage(request, pk):
    csv = UploadCsv.objects.filter(id=pk)
    return render(request, 'deletecsv.html', {'csv': csv})

def deletecsv(request, pk):
    if request.user.is_authenticated:
        delcsv_obj = UploadCsv.objects.get(id=pk)
        delcsv_obj.delete()
        messages.info(request, 'csvfile deleted')
        return redirect(f'/deletecsvpage/{pk}')

def deletecoursepage(request, coursename):
    if request.user.is_authenticated:
        course = Course.objects.filter(course_name=coursename)
        return render(request, 'deletecourse.html', {'course': course})

def deletecourse(request, coursename):
    if request.user.is_authenticated:
        delcsv_obj = Course.objects.filter(course_name=coursename)
        delcsv_obj.delete()
        messages.info(request, 'course deleted')
        return redirect('/teacherhome')

def editpage(request):
    user = request.user
    extra = ExtraField.objects.get(user=user)
    edituser = User.objects.get(username=user)

    context = {'user': user, 'edituser': edituser, 'extra': extra}
    return render(request, 'edit-account.html', context)

def editstupage(request):
    user = request.user
    ext = ExtraField.objects.get(user=user)
    edituser = User.objects.get(username=user)


    context = {'user': user, 'edituser': edituser, 'ext': ext}
    return render(request, 'edit-studentaccount.html', context)


def edituser(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.error(request, "username is already exists please try unique username")
            return redirect('/editpage')
        if len(username) < 5:
            messages.error(request, "Username mustbe more than 5 characters")
            return redirect('/editpage')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('/editpage')

        if username:
            User.objects.filter(username=user).update(username=request.POST.get('username'))
            messages.success(request, 'Successfully updated')
            return redirect('/editpage')

        else:
            messages.error(request, 'Cannot update')
            return redirect('/editpage')



def editstuuser(request):
    user = request.user
    extra = ExtraField.objects.get(user=user)
    st_id = extra.stu_id
    st_img = extra.stu_img

    # deleting old uploaded image.
    image_path = extra.stu_img.path
    if os.path.exists(image_path):
        os.remove(image_path)

    if request.method == 'POST':
        username = request.POST.get('username')
        stu_id = request.POST.get('stu_id')
        stu_img = request.FILES.get('stu_img')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already exists please try unique username")
            return redirect('/editstupage')
        if len(username) < 5:
            messages.error(request, "Username mustbe more than 5 characters")
            return redirect('/editstupage')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('/editstupage')

        if ExtraField.objects.filter(stu_id=stu_id).exists():
            messages.error(request, 'Student ID is already exists')
            return redirect('/editstupage')

        if username and stu_id and stu_img:
            User.objects.filter(username=user).update(username=request.POST.get('username'))
            ExtraField.objects.filter(stu_id=st_id).update(stu_id=request.POST.get('stu_id'))
            ExtraField.objects.filter(stu_img=st_img).update(stu_img=stu_img)
            update_profile = ExtraField.objects.get(user=request.user)
            update_profile.stu_id = stu_id
            update_profile.stu_img = stu_img
            update_profile.save()
            messages.success(request, 'Successfully updated')
            return redirect('/editstupage')

        else:
            messages.error(request, 'Cannot update')
            return redirect('/editstupage')




def addcomment1(request, coursename):
    if request.method == 'POST':
        user = request.user
        comment_id = request.POST.get('post_id')
        comment_obj = CreatePost.objects.get(id=comment_id)
        comment = request.POST.get('comment')

        allcomment_obj = CommentPost(user=user, posts=comment_obj, commentbody=comment)
        allcomment_obj.save()
        return redirect(f'/insidecourse/{coursename}')



# ---------------------------------------- studenthome function ---------------------------------------

def studenthome(request):
    user = request.user
    join_course = JoinCourse.objects.filter(user=user)
    return render(request, 'studenthome.html', {'join_course': join_course})


def stu_insidecourse(request, coursename):
    stu_insidecourse= JoinCourse.objects.filter(course=coursename)
    stuinsidecourse= Course.objects.filter(course_name=coursename)
    posts = CreatePost.objects.filter(course=coursename)
    csvfile = UploadCsv.objects.filter(course=coursename)
    context = {'coursename': coursename, 'stuinsidecourse': stuinsidecourse,  'posts': posts, 'csvfile': csvfile,
               'stu_insidecourse': stu_insidecourse}
    return render(request, 'stuinsidecourse.html', context)

def join_page(request):
    user = request.user
    course = JoinCourse.objects.filter(user=user)
    allcourse = Course.objects.all()
    return render(request, 'join_page.html', {'course': course, 'allcourse': allcourse})

def join(request):
    if request.method == 'POST':
        user = request.user
        join_id = request.POST.get('join')
        join_obj = Course.objects.get(course_name=join_id)

        if JoinCourse.objects.filter(user=user, course=join_obj).exists():
            messages.error(request, "Already joined")
            return redirect('/join_page')

        if request.user.is_authenticated:
            joincourse_obj = JoinCourse(user=user, course=join_obj)
            joincourse_obj.save()
            messages.success(request, 'Successfully joined')
            return redirect('/studenthome')

        else:
            messages.error(request, 'Can not join')
            return redirect('/studenthome')

def checkclasscode(request, coursename):
    if request.user.is_authenticated:
        code = Course.objects.filter(course_name=coursename).first().class_code

        if request.method == 'POST':
            class_code = request.POST['code']
            if class_code == code:
                return redirect(f'/stu_insidecourse/{coursename}')

            else:
                messages.error(request, 'Invalid classcode')
                return redirect('/studenthome')


def seepost(request, pk):
    if request.method == 'POST':
        coursecaption = request.POST['course_caption']
        coursefile = request.FILES.get('course_file', '')
        course_id = request.POST['course_name']
        coursename = Course.objects.get(id=course_id)

        if request.user.is_authenticated:
            user = request.user
            post_obj = CreatePost(caption=coursecaption, file=coursefile, user=user, course=coursename)
            post_obj.save()
            messages.success(request, "Successfully posted")
            return redirect(f'/stu_insidecourse/{pk}')
    else:
        messages.error(request, "Something went wrong please try again")
        return redirect(f'/stu_insidecourse/{pk}')

def likepost2(request, coursename):

    if request.method == 'POST':
        user = request.user
        likepost_id = request.POST.get('post_id')
        likepost_obj = CreatePost.objects.get(id=likepost_id)

        if user in likepost_obj.likes.all():
            likepost_obj.likes.remove(user)

        else:
            likepost_obj.likes.add(user)

        if request.user.is_authenticated:
            like_obj = Like(user=user, likepost=likepost_obj)
            like_obj.save()
            return redirect(f'/stu_insidecourse/{coursename}')


def addcomment2(request, coursename):
    if request.method == 'POST':
        user = request.user
        comment_id = request.POST.get('post_id')
        comment_obj = CreatePost.objects.get(id=comment_id)
        comment = request.POST.get('comment')

        allcomment_obj = CommentPost(user=user, posts=comment_obj, commentbody=comment)
        allcomment_obj.save()
        return redirect(f'/stu_insidecourse/{coursename}')

def uploadcsv(request, coursename):
    if request.method == 'POST':
        file = request.FILES['csvfile']
        csvname = request.POST['csvname']
        course_id = request.POST['course_name']
        course_name = Course.objects.get(course_name=course_id)

        if request.user.is_authenticated:
            user = request.user
            upload_obj = UploadCsv(csvfile=file, user=user, course=course_name, date=csvname)
            upload_obj.save()
            messages.success(request, "Successfully uploaded")
            return redirect(f'/insidecourse/{coursename}')

        else:
            messages.error(request, 'Upload failed')
            return redirect(f'/insidecourse/{coursename}')

def attendancecsv(request, coursename):
    attendance = GiveAttendance.objects.filter(course=coursename)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={coursename}.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Time', 'Date'])
    studs = attendance.values_list('name','time', 'date')
    for std in studs:
        writer.writerow(std)
    return response


def giveattendance(request, coursename):
    if request.method == 'POST':

        path = 'C:\\python\\djangoproject\\studyarea\\media\\images'
        images = []
        personName = []
        myList = os.listdir(path)
        print(myList)

        for curr_img in myList:
            current_img = cv2.imread(f'{path}/{curr_img}')
            images.append(current_img)
            personName.append(os.path.splitext(curr_img)[0])
        print(personName)

        def faceEncodings(images):
            encodeList = []

            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                print(encode)
                encodeList.append(encode)
            return encodeList

        encodeListKnown = (faceEncodings(images))
        print("All encodings complete!")




        def attendance(name):

            time_now = datetime.now()
            time = time_now.strftime('%H:%M:%S')
            date = time_now.strftime('%d/%m/%Y')

            path = 'C:\\python\\djangoproject\\studyarea\\media\\attendance'
            files = glob.glob(path + "/*.csv")
            for filename in files:
                with open(filename, 'r+')as f:
                    myDataList = f.readlines()
                    nameList = []
                    for line in myDataList:
                        entry = line.split(',')
                        nameList.append(entry[0])


                    if name not in nameList:
                        f.writelines(f'\n{name}, {time}, {date}')



                    file_id = request.POST['csv_file']
                    csv_file = UploadCsv.objects.get(csvfile=file_id)
                    course_id = request.POST['course_name']
                    course_name = Course.objects.get(course_name=course_id)
                    stu_id = name
                    today_date = date
                    today_time = time

                    if GiveAttendance.objects.filter(name=name, csvfile=csv_file).exists():
                        return redirect(f'/stu_insidecourse/{coursename}')

                    if request.user.is_authenticated:
                        user = request.user
                        attendance_obj = GiveAttendance(csvfile=csv_file, course=course_name, user=user, name=stu_id, date=today_date, time=today_time)
                        attendance_obj.save()


        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

            facesCurrentFrame = face_recognition.face_locations(faces)
            encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

            for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)



                if matches[matchIndex]:

                    name = personName[matchIndex]


                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
                    attendance(name)


            cv2.imshow("Camera", frame)
            if cv2.waitKey(1000) == 13:
                break
        cap.release()
        cv2.destroyAllWindows()
        messages.info(request, "The frame has been stop")
        return redirect(f'/stu_insidecourse/{coursename}')


def checkattendance(request, coursename):
    attendance = GiveAttendance.objects.filter(course=coursename)
    return render(request, 'checkattendance.html', {'attendance': attendance, 'coursename': coursename})



