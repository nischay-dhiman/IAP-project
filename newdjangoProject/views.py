# Create your views here.
# Import necessary classes
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from newdjangoProject.forms import InterestForm, OrderForm, LoginForm, RegisterForm, ResetPasswordForm, StudentForm
from newdjangoProject.models import Topic, Course, Interest, Order
from django.core.mail import send_mail
from django.contrib.auth.models import User

import random
import string


def do_stuff(user, request, **kwargs):
    request.delete_cookie('last_login')


# user_logged_out.connect(do_stuff)

def index(request):
    user = request.user
    first_name = "User"
    if user.is_authenticated:
        first_name = user.first_name
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'newdjangoProject/index0.html', {'top_list': top_list, 'first_name': first_name})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                request.session['last_login'] = str(datetime.now())
                nextUrl = request.POST.get("next")
                response = HttpResponseRedirect(reverse('index'))
                if nextUrl:
                    response = HttpResponseRedirect(nextUrl)
                response.set_cookie('last_login', datetime.now(), max_age=3600)
                login(request, user)
                return response
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        context = {'form': LoginForm(), 'next': request.GET.get("next")}
        return render(request, 'newdjangoProject/login.html', context)


def register(request):
    msg = ''
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['last_login'] = str(datetime.now())
            messages.success(request, 'Registration Successful!')
            return HttpResponseRedirect(reverse('index'))
        else:
            msg = form.errors
    form = RegisterForm()
    return render(request, 'newdjangoProject/register.html', context={'form': form, 'msg': msg})


@login_required
def user_logout(request):
    del request.session['last_login']
    logout(request)  # COMMENTING FOR PART 2C
    response = HttpResponseRedirect(reverse('index'))
    return response


def forgot_password(request):
    # fetch email and check if user exists and send email for new password
    context = {'form': ResetPasswordForm()}
    return render(request, 'newdjangoProject/forgot_password.html', context)


def send_new_password(request):
    username = request.POST['username']
    user = User.objects.filter(username=username)

    if user:
        user = user[0]
        source = string.ascii_letters + string.digits
        random_password = ''.join((random.choice(source) for i in range(15)))

        user.set_password(random_password)

        user.save()

        print("New password = ", random_password)
        send_mail(
            'New password for My app',
            'Hello User,\n Your new password: ' + random_password,
            'noreply@vhaze.in',
            [user.email],
            fail_silently=False,
        )

    context = {'form': LoginForm(), 'msg': "New password sent successfully"}
    return render(request, 'newdjangoProject/login.html', context)


@login_required(login_url='/myapp/login/')
def myaccount(request):
    user = get_user(request)
    if hasattr(user, 'student'):
        msg = ''
        student = user.student
        if request.method == 'POST':
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                student.avatar = form.cleaned_data['avatar']
                student.save()
                msg = "Your Profile Updated successfully"
            else:
                msg = form.errors

        context = {
            'msg': msg,
            'form': StudentForm(),
            'interested_in_topics': student.interested_in_topics,
            'bought_courses': student.bought_courses,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'user': user,
            'image_url': user.student.avatar_url,
            'email': student.email
        }
        return render(request, 'newdjangoProject/myaccount.html', context)
    else:
        msg = "You are not a registered student!"
        return render(request, 'newdjangoProject/not_student_account.html', {'msg': msg})


def about(request):
    # return HttpResponse('This is an E-learning Website! Search our Topics to find all available Courses')
    response = render(request, 'newdjangoProject/about0.html')
    if request.COOKIES.get('about_visits'):
        response.set_cookie('about_visits', int(
            request.COOKIES['about_visits']) + 1, max_age=300)
    else:
        response.set_cookie('about_visits', 1, max_age=300)

    return response


def detail(request, top_no):
    topic = get_object_or_404(Topic, id=top_no)
    course_list = Course.objects.filter(topic=topic)
    return render(request, 'newdjangoProject/detail0.html', {'topic': topic, 'course_list': course_list})


def placeorder(request):
    msg = ''
    courlist = Course.objects.all()

    def new_order_form(msg=None):
        current_user = get_user(request)
        if current_user.id:
            form = OrderForm(request.POST or None, initial={
                             'student': current_user.student, })
            logged_in = True
        else:
            form = OrderForm()
            logged_in = False

        return render(
            request,
            'newdjangoProject/placeorder.html',
            {'form': form, 'msg': msg, 'courlist': courlist, 'logged_in': logged_in}
        )

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                course = order.course
                if course.price > 150:
                    course.price = course.discount()
                    course.save()
                msg = 'Your course has been ordered successfully.'
                return render(request, 'newdjangoProject/order_response.html', {'msg': msg})
            else:
                msg = 'You exceeded the number of levels for this course.'
        else:
            msg = form.errors

    return new_order_form(msg)


def courses(request):
    course_list = Course.objects.all().order_by('id')
    return render(request, 'newdjangoProject/courses.html', {'course_list': course_list})


def coursedetail(request, course_no):
    course = get_object_or_404(Course, id=course_no)
    context = {'course': course}
    return render(request, 'newdjangoProject/coursedetail.html', context)


def add_interest(request, course_no):
    if request.method == 'POST':
        form = InterestForm(request.POST, request.FILES)
        if form.is_valid():
            interest = Interest()
            interest.interested = form.cleaned_data['interested']
            interest.levels = form.cleaned_data['levels']
            interest.comments = form.cleaned_data['comments']
            interest.save()
            course = get_object_or_404(Course, id=course_no)
            course.interested = F("interested") + 1
            course.save(update_fields=["interested"])

            return render(request, 'newdjangoProject/interest_success.html',
                          {'msg': "Your Interest has been saved successfully."})
        else:
            context = {'form': InterestForm()}
            return render(request, 'newdjangoProject/interest.html', context)
    else:
        context = {'form': InterestForm(), 'course_id': get_object_or_404(
            Course, id=course_no).id}
        return render(request, 'newdjangoProject/interest.html', context)


@login_required
def myorders(request):
    user = get_user(request)
    if hasattr(user, 'student'):
        order_list = Order.objects.filter(student=user.student)
        context = {
            'orders': order_list
        }
        return render(request, 'newdjangoProject/myorders.html', context)
    else:
        msg = "You are not a registered student!"
        return render(request, 'newdjangoProject/not_student_account.html', {'msg': msg})
