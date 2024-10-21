from django.test import TestCase
from ..models import Course

class CourseTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            code="CS101", 
            name="Intro to Computer Science", 
            semester="Fall", 
            year=2023, 
            seats=30
        )
    
    def test_course_creation(self):
        self.assertEqual(self.course.code, "CS101")
        self.assertEqual(self.course.name, "Intro to Computer Science")
        self.assertEqual(self.course.semester, "Fall")
        self.assertEqual(self.course.year, 2023)
        self.assertEqual(self.course.seats, 30)
        self.assertTrue(self.course.is_open)
