from django.urls import path
from .views import StudentBasicView

urlpatterns = [
    path('student_details/', StudentBasicView.as_view()),
]
