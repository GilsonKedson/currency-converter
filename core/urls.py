from django.urls import path
from converter import viewsets

urlpatterns = [
    path('',  viewsets.ConverterViewSet.as_view()),
]
