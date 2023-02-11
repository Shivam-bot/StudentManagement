from django.db import models

from enum import Enum, unique
import datetime as dt

# Enum defined for gender so in future chances of getting error will be less
# Unique decorator to ensure no value is repeating itself.


@unique
class GenderEnum(Enum):
    Male = "M"
    Female = "F"
    TransGender = "T"
    NotToDisclose = "N"

    @classmethod
    def gender_choices(cls):
        return [(gender.value, gender.name) for gender in cls]


@unique
class RelationsEnum(Enum):
    Father = "Father"
    Mother = "Mother"
    Sibling = "Sibling"
    GrandParents = "GrandParents"

    @classmethod
    def relation_choices(cls):
        return [(relation.value, relation.name) for relation in cls]


def get_standard():

    try:
        standard_details = StandardDetails.objects.all()
        return [(standard_detail.standard, standard_detail.standard) for standard_detail in standard_details] if standard_details.exists() else []
    except Exception as e:
        print(f"{e}")
        return [("I", "I"), ("II", "II"), ("III", "III"), ("VI", "VI"), ("V", "V")]


class StandardDetails(models.Model):

    objects = None
    standard_id = models.AutoField(primary_key=True)
    standard = models.CharField(max_length=15)
    sections = models.JSONField(default=["A", "B"])
    subjects = models.JSONField()
    standard_created_on = models.DateField(auto_now_add=True)
    standard_updated_on = models.DateField(auto_now=True)

    class Meta:
        db_table = "standard_details"


class StudentBasicDetails(models.Model):
    objects = None
    student_id = models.AutoField(primary_key=True)
    student_enrollment = models.CharField(max_length=100, unique=True)
    student_first_name = models.CharField(max_length=30, error_messages="")
    student_last_name = models.CharField(max_length=30, error_messages="", default="")
    student_gender = models.CharField(choices=GenderEnum.gender_choices(), max_length=1, default='N')
    student_DOB = models.DateField()
    student_section = models.CharField(max_length=2)
    student_enrolled = models.BooleanField(default=True)
    student_class = models.CharField(choices=get_standard(), max_length=15)
    student_enrollment_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_basic_details"

    def save(self, *args, **kwargs):
        nowdate_time = dt.datetime.now()
        year =  nowdate_time.year
        print("year", year)
        standard = self.student_class
        print("standard", standard)
        time = nowdate_time.time()
        print("time", time)
        print()
        self.student_enrollment = f"{year}/{standard}/{time}"
        super(StudentBasicDetails, self).save(*args, **kwargs)


class StudentContactDetails(models.Model):
    objects = None
    contact_id = models.AutoField(primary_key=True)
    contact_mob_no = models.BigIntegerField()
    contact_alternate_mob_no = models.BigIntegerField(null=True, blank=True)
    contact_email = models.EmailField()
    contact_alternate_email = models.EmailField(null=True, blank=True)
    student_id = models.OneToOneField(StudentBasicDetails, on_delete=models.SET_NULL, null=True)
    contact_created_date = models.DateField(auto_now_add=True)
    contact_updated_date = models.DateField(auto_now=True)

    class Meta:
        db_table = "student_contact_details"

    def __int__(self):
        return self.contact_id


class StudentParentsDetails(models.Model):
    objects = None
    student_parent_id = models.AutoField(primary_key=True)
    student_parent_name = models.CharField(max_length=100)
    student_parent_relation = models.CharField(choices=RelationsEnum.relation_choices(), max_length=15)
    student_id = models.ForeignKey(StudentBasicDetails, on_delete=models.SET_NULL, null=True)
    student_parent_created_date = models.DateField(auto_now_add=True)
    student_parent_updated_date = models.DateField(auto_now=True)

    class Meta:
        db_table = "student_parents_details"
        unique_together = ("student_parent_name", "student_id", "student_parent_relation")

    def __int__(self):
        return self.student_parent_id

    @staticmethod
    def save_all(parents_details: list, student_id: int):
        return_list = []
        for parent_detail in parents_details:
            print(parent_detail, "parent-details")
            parent_query = StudentParentsDetails.objects.create(student_id_id=student_id, **parent_detail)
            parent_detail["parent_id"] = parent_query.student_parent_id
            return_list.append(parent_detail)
        print(return_list)
        return return_list
