# Create your views here.
# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Topic, Course, Student, Order, Interest
from django.http import Http404
from .forms import InterestForm, OrderForm
from django.db.models import F

# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'newdjangoProject/index0.html', {'top_list': top_list})


def about(request):
    # return HttpResponse('This is an E-learning Website! Search our Topics to find all available Courses')
    return render(request, 'newdjangoProject/about0.html')

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

            return render(request, 'newdjangoProject/interest_success.html', {'msg': "Your Interest has been saved successfully."})
        else:
            context = {'form': InterestForm()}
            return render(request, 'newdjangoProject/interest.html', context)
    else:
        context = {'form': InterestForm(), 'course_id': get_object_or_404(Course, id=course_no).id}
        return render(request, 'newdjangoProject/interest.html', context)


