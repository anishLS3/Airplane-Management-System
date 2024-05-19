from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path(r"", views.get_context_data, name="getContextData"),
]