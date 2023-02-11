from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.db import transaction


class StudentBasicView(APIView):

    def get(self, request):

        try:
            data = request.data
            student_id = data.get("student_id")

            if student_id is not None:
                student_details = StudentBasicDetails.objects.filter(student_id=student_id).prefetch_related('studentparentsdetails_set')
            else:
                student_details = StudentBasicDetails.objects.filter(student_enrolled=True).prefetch_related('studentparentsdetails_set')
                print(student_details.query)

            for std in student_details:
                for parents in std.studentparentsdetails_set.all():
                    print(parents.student_parent_id)
                    print(parents.student_parent_name)

            return Response(
                {"status": True, "data": {"student_details": StudentBasicSerializer(student_details, many=True).data},
                 "message": {}})

        except Exception as e:
            return Response(
                {"status": False, "data": {}, "message": {"exceptional_error": f"{e}"}})

    def post(self, request):
        try:
            with transaction.atomic():
                student_detail = request.data
                print(student_detail, "<<<<<")
                student_serializer = StudentBasicSerializer(data=student_detail)
                print(student_serializer, "<<<<<student_serializer")
                if student_serializer.is_valid():
                    print("data verified")
                    student_saved_detail = student_serializer.save()
                    print("student_details_saved")
                    # student_detail["student_id"] = student_saved_detail['student_id']
                    print("student_detail", student_saved_detail, "<<<<<")
                    return Response({"status": True, "data": {"student_detail": student_saved_detail}})
                return Response({"status": False, "data": {}, "message": {"data_invalid": student_serializer.errors}})

        except Exception as e:
            return Response(
                {"status": False, "data": {}, "message": {"exceptional_error": f"Roll Backed everything {e}"}})

    def put(self, request):
        try:
            student_detail = request.data
            student_id = student_detail.get("student_id")
            if student_id is None:
                return Response({"status":False, "data":{}, "message":{"student_id": "Student Id cannot be None"}})
            try:
                student_instance = StudentBasicDetails.objects.get(student_id=student_id)
            except Exception as e:
                return Response({"status": False, "data": {}, "message": {"student_id": f"No Data Exist with given "
                                                                                       f"student Id {student_id}"}})
            student_serializer = StudentBasicSerializer(data=student_detail, instance =student_instance)
            if student_serializer.is_valid():
                student_saved_detail = StudentBasicSerializer.save()
                student_detail["student_id"] = student_saved_detail.student_id
                return Response({"status": True, "data": {"student_detail": student_detail}})
            return Response({"status": False, "data": {}, "message": {"data_invalid": student_serializer.errors}})

        except Exception as e:
            return Response(
                {"status": False, "data": {}, "message": {"exceptional_error": e}})

