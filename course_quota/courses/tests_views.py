from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, QuotaRequest

class ViewsTestCase(TestCase):
    def setUp(self):
        # Set up a test client and create sample users and a course
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.student_user = User.objects.create_user(username='student', password='student123')
        self.course = Course.objects.create(code="CS101", name="Intro to Computer Science", semester="Fall", year=2023, seats=30)
        self.quota_request = QuotaRequest.objects.create(student=self.student_user, course=self.course)

    def test_course_quota_requests(self):
        # Test accessing the course quota requests as an admin
        self.client.login(username='admin', password='admin123')
        url = reverse('course_quota_requests', args=[self.course.code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_quota_requests.html')

    def test_quota_requests_list_no_access(self):
        # Test accessing the quota requests list without login (should redirect)
        url = reverse('quota_requests_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_quota_requests_list_admin_access(self):
        # Test accessing the quota requests list as an admin
        self.client.login(username='admin', password='admin123')
        url = reverse('quota_requests_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/quota_requests_list.html')

    def test_approve_quota_request(self):
        # Test approving a quota request and updating the course seat count
        self.client.login(username='admin', password='admin123')
        url = reverse('approve_quota_request', args=[self.quota_request.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(QuotaRequest.objects.get(id=self.quota_request.id).is_approved)
        self.assertEqual(Course.objects.get(code="CS101").seats, 29)

    def test_home_view(self):
        # Test accessing the home page
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/home.html')

    def test_course_list_view(self):
        # Test accessing the course list as a student
        self.client.login(username='student', password='student123')
        url = reverse('course_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')

    def test_request_quota(self):
        # Test requesting a quota for a course
        self.client.login(username='student', password='student123')
        url = reverse('request_quota', args=[self.course.code])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(QuotaRequest.objects.filter(student=self.student_user, course=self.course).exists())

    def test_register_view_get(self):
        # Test accessing the registration page
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/register.html')

    def test_register_view_post(self):
        # Test registering a new user
        url = reverse('register')
        response = self.client.post(url, {'username': 'new_user', 'password': 'password123', 'password2': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='new_user').exists())

    def test_student_login_view_get(self):
        # Test accessing the login page
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/login.html')

    def test_student_login_view_post(self):
        # Test logging in a user
        url = reverse('login')
        response = self.client.post(url, {'username': 'student', 'password': 'student123'})
        self.assertEqual(response.status_code, 302)

    def test_my_quota_requests_view(self):
        # Test accessing the user's quota requests
        self.client.login(username='student', password='student123')
        url = reverse('my_quota_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/my_quota_requests.html')

    def test_cancel_quota_request(self):
        # Test canceling a quota request and updating the course seat count
        self.client.login(username='student', password='student123')
        url = reverse('cancel_quota_request', args=[self.course.code])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(QuotaRequest.objects.filter(id=self.quota_request.id).exists())
        self.assertEqual(Course.objects.get(code="CS101").seats, 30)

    def test_admin_dashboard_view(self):
        # Test accessing the admin dashboard
        self.client.login(username='admin', password='admin123')
        url = reverse('admin_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/admin_dashboard.html')

    def test_my_enrolled_courses_view(self):
        # Test accessing the user's enrolled courses
        self.client.login(username='student', password='student123')
        url = reverse('my_enrolled_courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/my_enrolled_courses.html')
