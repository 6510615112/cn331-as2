from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Course, QuotaRequest

class QuotaRequestTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create(username="test_student")
        self.course = Course.objects.create(
            code="CS101", 
            name="Intro to Computer Science", 
            semester="Fall", 
            year=2023, 
            seats=30
        )
    
    def test_quota_request_creation(self):
        quota_request = QuotaRequest.objects.create(student=self.student, course=self.course)
        self.assertEqual(quota_request.student, self.student)
        self.assertEqual(quota_request.course, self.course)
        self.assertTrue(quota_request.requested_at)
        self.assertFalse(quota_request.is_approved)
        
    def test_approve_quota_request(self):
        quota_request = QuotaRequest.objects.create(student=self.student, course=self.course)
        quota_request.is_approved = True
        quota_request.save()
        self.assertTrue(QuotaRequest.objects.get(id=quota_request.id).is_approved)
