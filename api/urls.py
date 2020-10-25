from django.urls import path

from .views import publication_history

urlpatterns = [path("documents/history", publication_history)]
