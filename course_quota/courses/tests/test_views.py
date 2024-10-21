from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Course, QuotaRequest
from ..forms import UserRegistrationForm

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.student_user = User.objects.create_user(username='student', password='student123')
        self.course = Course.objects.create(code="CS101", name="Intro to Computer Science", semester="Fall", year=2023, seats=30)

    def test_course_quota_requests(self):
        self.client.login(username='admin', password='admin123')
        url = reverse('course_quota_requests', args=[self.course.code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_quota_requests.html')

    def test_quota_requests_list_no_access(self):
        url = reverse('quota_requests_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_quota_requests_list_admin_access(self):
        self.client.login(username='admin', password='admin123')
        url = reverse('quota_requests_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/quota_requests_list.html')

    def test_approve_quota_request(self):
        self.client.login(username='admin', password='admin123')
        quota_request = QuotaRequest.objects.create(student=self.student_user, course=self.course)
        url = reverse('approve_quota_request', args=[quota_request.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(QuotaRequest.objects.get(id=quota_request.id).is_approved)
        self.assertEqual(Course.objects.get(code="CS101").seats, 29)

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/home.html')

    def test_course_list_view(self):
        self.client.login(username='student', password='student123')
        url = reverse('course_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')

    def test_request_quota(self):
        self.client.login(username='student', password='student123')
        url = reverse('request_quota', args=[self.course.code])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(QuotaRequest.objects.filter(student=self.student_user, course=self.course).exists())

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/register.html')
        response = self.client.post(url, {'username': 'new_user', 'password': 'new_password'})
        self.assertEqual(response.status_code, 302)

    def test_student_login_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/login.html')
        response = self.client.post(url, {'username': 'student', 'password': 'student123'})
        self.assertEqual(response.status_code, 302)

    def test_my_quota_requests_view(self):
        self.client.login(username='student', password='student123')
        url = reverse('my_quota_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/my_quota_requests.html')

    def test_cancel_quota_request(self):
        self.client.login(username='student', password='student123')
        quota_request = QuotaRequest.objects.create(student=self.student_user, course=self.course, is_approved=True)
        url = reverse('cancel_quota_request', args=[quota_request.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(QuotaRequest.objects.filter(id=quota_request.id).exists())
        self.assertEqual(Course.objects.get(code="CS101").seats, 31)

    def test_admin_dashboard_view(self):
        self.client.login(username='admin', password='admin123')
        url = reverse('admin_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/admin_dashboard.html')

    def test_my_enrolled_courses_view(self):
        self.client.login(username='student', password='student123')
        url = reverse('my_enrolled_courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/my_enrolled_courses.html')
    def test_register_invalid_data(self):
        url = reverse('register')
        response = self.client.post(url, {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/register.html')
        self.assertFormError(response, 'form', 'username', 'This field is required.')
    def test_student_login_invalid(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/login.html')
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password.')
    def test_my_quota_requests_empty(self):
        self.client.login(username='student', password='student123')
        url = reverse('my_quota_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/my_quota_requests.html')
        self.assertContains(response, 'You have no quota requests.')
    def test_cancel_quota_request_unauthorized(self):
        other_student = User.objects.create_user(username='other_student', password='other123')
        quota_request = QuotaRequest.objects.create(student=other_student, course=self.course)
        self.client.login(username='student', password='student123')
        url = reverse('cancel_quota_request', args=[quota_request.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # Forbidden
    def test_cancel_quota_request_not_approved(self):
        self.client.login(username='student', password='student123')
        quota_request = QuotaRequest.objects.create(student=self.student_user, course=self.course, is_approved=False)
        url = reverse('cancel_quota_request', args=[quota_request.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(QuotaRequest.objects.filter(id=quota_request.id).exists())

class RegisterViewTestCase(TestCase):
    
    def test_register_view_get(self):
        """
        Test the GET request to the register view to ensure the form is rendered.
        """
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/register.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)
    
    def test_register_view_post_valid(self):
        """
        Test the POST request with valid data to ensure a new user is created and redirected.
        """
        url = reverse('register')
        form_data = {
            'username': 'new_user',
            'password': 'new_password',
            'password2': 'new_password'  # Assuming password confirmation
        }
        response = self.client.post(url, form_data)
        
        # Check for redirect after successful registration
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # Check if the user was created
        self.assertTrue(User.objects.filter(username='new_user').exists())

    def test_register_view_post_invalid(self):
        """
        Test the POST request with invalid data (e.g., empty fields) to ensure form errors.
        """
        url = reverse('register')
        form_data = {
            'username': '',
            'password': '',
            'password2': ''  # Assuming password confirmation field exists
        }
        response = self.client.post(url, form_data)

        # Check the form is rendered again with errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/register.html')
        self.assertFalse(User.objects.filter(username='').exists())
        self.assertFormError(response, 'form', 'username', 'This field is required.')


