from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, QuotaRequest

class CourseTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            code="CN331",
            name="Software Engineering",
            semester="1",
            year=2024,
            seats=30,
            is_open=True
        )

    def test_course_str_method(self):
        self.assertEqual(str(self.course), "CN331")

class QuotaRequestTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="teststudent", password="password123")
        self.course = Course.objects.create(
            code="CN331",
            name="Software Engineering",
            semester="1",
            year=2024,
            seats=30,
            is_open=True
        )
        self.quota_request = QuotaRequest.objects.create(
            student=self.student,
            course=self.course,
            is_approved=False
        )

    def test_quota_request_str_method(self):
        self.assertEqual(str(self.quota_request), "CN331")
