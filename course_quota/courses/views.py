from django.shortcuts import render, redirect
from .models import Course, QuotaRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

@staff_member_required
def course_quota_requests(request, course_code):
    course = get_object_or_404(Course, code=course_code)
    requests = QuotaRequest.objects.filter(course=course, is_approved=True)
    return render(request, 'courses/course_quota_requests.html', {'course': course, 'requests': requests})

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def quota_requests_list(request):
    requests = QuotaRequest.objects.filter(is_approved=False)
    return render(request, 'courses/quota_requests_list.html', {'requests': requests})

@login_required
@user_passes_test(is_admin)
def approve_quota_request(request, request_id):
    quota_request = QuotaRequest.objects.get(id=request_id)
    quota_request.is_approved = True
    quota_request.save()

    # ลดจำนวนที่นั่งใน course
    course = quota_request.course
    course.seats -= 1
    course.save()

    return redirect('quota_requests_list')


def home(request):
    return render(request, 'courses/home.html')


@login_required
def course_list(request):
    courses = Course.objects.filter(is_open=True)
    context = {
        'courses': courses,
        'user': request.user
    }
    return render(request, 'courses/course_list.html', context)

@login_required
def request_quota(request, course_code):
    course = get_object_or_404(Course, code=course_code)
    existing_request = QuotaRequest.objects.filter(student=request.user, course=course).first()
    if not existing_request and course.seats > QuotaRequest.objects.filter(course=course).count():
        QuotaRequest.objects.create(student=request.user, course=course)
    return redirect('course_list')

# @login_required
# def course_requests(request, course_id):
#     course = Course.objects.get(id=course_id)
#     requests = QuotaRequest.objects.filter(course=course)
#     return render(request, 'courses/course_requests.html', {'course': course, 'requests': requests})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'courses/register.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})

@login_required
def my_quota_requests(request):
    requests = QuotaRequest.objects.filter(student=request.user)
    return render(request, 'courses/my_quota_requests.html', {'requests': requests})

@login_required
def cancel_quota_request(request, request_id):
    quota_request = QuotaRequest.objects.get(id=request_id)
    if quota_request.student == request.user:
        course = quota_request.course
        course.seats += 1
        course.save()
        quota_request.delete()
    return redirect('my_quota_requests')

@staff_member_required
def admin_dashboard(request):
    courses = Course.objects.all()
    course_data = []
    for course in courses:
        student_count = QuotaRequest.objects.filter(course=course, is_approved=True).count()
        course_data.append({
            'course': course,
            'student_count': student_count
        })
    return render(request, 'courses/admin_dashboard.html', {'course_data': course_data})

@login_required
def my_enrolled_courses(request):
    requests = QuotaRequest.objects.filter(student=request.user, is_approved=True)
    return render(request, 'courses/my_enrolled_courses.html', {'requests': requests})
