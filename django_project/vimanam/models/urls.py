from django.urls import path
from . import views

app_name = "models"

urlpatterns = [
    path(r"d/", views.get_context_data, name="getContextData"),
    path(r"d/<str:model_num>/", views.get_model_data, name="getModelData"),
]