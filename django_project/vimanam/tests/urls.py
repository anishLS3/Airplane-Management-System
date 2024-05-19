from django.urls import path
from . import views

app_name = "tests"

urlpatterns = [
    path(r"d/", views.get_context_data, name="getContextData"),
    path(r"d/<str:test_num>/", views.get_test_data, name="getTestData")
]