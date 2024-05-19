from django.urls import path
from . import views

app_name = "airplanes"

urlpatterns = [
    path(r"d/", views.get_context_data, name="getContextData"),
    path(r"d/<str:reg_num>/", views.get_airplane_data, name="getAirplaneData"),
]