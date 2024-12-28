from django.test import TestCase
import logging as log

from .models import StudentBasicDetails

logger = log.getLogger(__name__)


class StudentBasicTestCase(TestCase):
    def test_enroll_student(self):
        s1 = StudentBasicDetails.objects.create(student_first_name='Shiv', student_last_name='Sharma',
                                                student_gender='M', student_DOB='1997-12-12', student_section='A',
                                                student_class='I')
        print("Test")
        print(logger.name)
        print(f"Strident created successfully with first name {s1.student_first_name} and id {s1.student_id} and "
                    f"enroll id {s1.student_enrollment}")
