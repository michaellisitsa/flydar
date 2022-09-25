from django.urls import path, include
from backend.core import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"pestTrap", views.PestTrapViewSet)
router.register(r"profile", views.UserViewSet2, basename="Profile")

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/", include(router.urls)),
    path("pest-trap-registration/", views.pest_trap_registration, name="pest-trap-registration"),
    path("pest-trap-table/", views.pest_trap_table, name="pest-trap-table")
]
