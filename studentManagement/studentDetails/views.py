from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class StudentBasicView(APIView):

    def get(self, request):

        try:
            data = request.data
            student_id = data.get("student_id")

            if student_id is not None:
                student_details = StudentBasicDetails.objects.filter(student_id=student_id)
            else:
                student_details = StudentBasicDetails.objects.filter(student_enrolled=True)

            return Response(
                {"status": True, "data": {"student_details": StudentBasicSerializer(student_details, many=True).data},
                 "message": {}})

        except Exception as e:
            return Response(
                {"status": False, "data": {}, "message": {"exceptional_error": f"{e}"}})

    def post(self, request):
        try:
            student_detail = request.data
            student_serializer = StudentBasicSerializer(data=student_detail)
            if student_serializer.is_valid():
                student_saved_detail = StudentBasicSerializer.save()
                student_detail["student_id"] = student_saved_detail.student_id
                return Response({"status": True, "data": {"student_detail": student_detail}})
            return Response({"status": False, "data": {}, "message": {"data_invalid": student_serializer.errors}})

        except Exception as e:
            return Response(
                {"status": False, "data": {}, "message": {"exceptional_error": e}})

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

