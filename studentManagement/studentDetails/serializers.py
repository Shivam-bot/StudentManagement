from rest_framework import serializers
from .models import StudentParentsDetails, StudentContactDetails, StudentBasicDetails
import studentManagement.customValidations as customValidations
import logging as log

# log.basicConfig(level=log.DEBUG, format= )


class StudentParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentParentsDetails
        fields = ("student_parent_name", 'student_parent_relation','student_parent_id')

    def validate(self, data):
        parent_name = data.get("student_parent_name")
        if customValidations.CustomValidations.check_string_pattern(parent_name, "[a-zA-Z a-zA-Z]"):
            raise serializers.ValidationError({"status": False, "error_message":
                {"student_parent_name": "Parents name should be consist of first name and last name."}})
        return data


class StudentContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentContactDetails
        exclude = ("contact_created_date", "contact_updated_date" )

    def validate(self, data):
        contact_mob_no = data.get("contact_mob_no")
        alternate_mob_no = data.get("contact_alternate_mob_no")

        if contact_mob_no is not None:
            customValidations.CustomValidations.integer_value_length(contact_mob_no, 10)
            customValidations.CustomValidations.integer_starts_from(contact_mob_no, 6)

        if alternate_mob_no is not None:
            customValidations.CustomValidations.integer_value_length(alternate_mob_no, 10)
            customValidations.CustomValidations.integer_starts_from(alternate_mob_no, 6)

        return data


class StudentBasicSerializer(serializers.ModelSerializer):

    parents_details = StudentParentsSerializer(many=True, required=True)
    contact_details = StudentContactSerializers(many=False, required=True)

    class Meta:
        model = StudentBasicDetails
        exclude = ('student_enrolled', 'student_enrollment')

    def create(self, validated_data):
        parents_details = validated_data.pop("parents_details")
        print(parents_details, "<<<<<parents details")
        contact_details = validated_data.pop("contact_details")
        print("Contact details", contact_details)
        print(validated_data)
        student_details = StudentBasicDetails.objects.create(**validated_data)
        print("Student details saved")
        contact_query = StudentContactDetails.objects.create(student_id=student_details, **contact_details)
        contact_details["contact_id"] = contact_query.contact_id
        print("Contact details saved")

        parents_details = StudentParentsDetails.save_all(parents_details, student_details.student_id)
        print("parents details saved")
        validated_data["student_id"] = student_details.student_id
        validated_data["parents_details"] = parents_details
        validated_data["contact_details"] = contact_details

        return validated_data
