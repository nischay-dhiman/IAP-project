# Create your views here.
# Import necessary classes
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from .forms import InterestForm, OrderForm, LoginForm, RegisterForm
from .models import Topic, Course, Interest, Order


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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                request.session['last_login'] = str(datetime.now())
                nextUrl = request.POST.get("next")
                response = HttpResponseRedirect(reverse('index'))
                if nextUrl:
                    response = HttpResponseRedirect(nextUrl)
                # response.set_cookie('last_login', datetime.now() , max_age=3600)
                login(request, user)
                return response
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        context = {'form': LoginForm()}
        return render(request, 'newdjangoProject/login.html', context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse('Registration Unsuccessful. Invalid Information')
    form = RegisterForm()
    return render(request, 'newdjangoProject/register.html', context={'form': form})


@login_required
def user_logout(request):
    # logout(request)  # COMMENTING FOR PART 2C
    del request.session['last_login']
    response = HttpResponseRedirect(reverse('newdjangoProject:index'))
    # response.delete_cookie('last_login')
    return response


@login_required(login_url='/myapp/login/')
def myaccount(request):
    user = get_user(request)
    if hasattr(user, 'student'):
        student = user.student
        context = {
            'interested_in_topics': student.interested_in_topics,
            'bought_courses': student.bought_courses,
            'first_name': student.first_name,
            'last_name': student.last_name
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
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'newdjangoProject/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
        return render(request, 'newdjangoProject/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})


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
