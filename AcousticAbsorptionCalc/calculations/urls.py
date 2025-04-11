from django.urls import path

from .views import AcousticCalculationView

urlpatterns = [
    path(
        "api/calculate/", AcousticCalculationView.as_view(), name="acoustic-calculate"
    ),
]
