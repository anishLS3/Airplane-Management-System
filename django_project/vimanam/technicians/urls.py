from django.urls import path
from . import views

app_name = "technicians"

urlpatterns = [
    path(r"d/", views.get_context_data, name="getContextData"),
    path(r"d/<str:ssn>/", views.get_technician_data, name="getTechnicianData"),
]