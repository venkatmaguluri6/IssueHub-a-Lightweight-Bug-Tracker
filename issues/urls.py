from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for issues
# When included under /projects/<int:project_pk>/issues/, the 'issues' part is already in the URL
# So we register with empty string to match the base path
router = DefaultRouter()
router.register(r'', views.IssueViewSet, basename='issue')

urlpatterns = [
    path('', include(router.urls)),
]
