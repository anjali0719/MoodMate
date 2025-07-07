from django.urls import path
from journals.views import test_view

urlpatterns = [
    path("", test_view, name="test-view"),
]
