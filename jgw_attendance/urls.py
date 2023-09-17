"""
URL configuration for jgw_attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

v1_api_patterns = [
    path("attendance/", include("apps.attendance.urls")),
    path("event/", include("apps.event.urls")),
    path("timetable/", include("apps.timetable.urls")),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="JGW Attendance Management System API",
        default_version="v1",
        description="해당 API를 사용하여 학회의 행사와 타임테이블을 관리하거나, 출결을 관리할 수 있습니다.\n\n해당 API를 사용하기 위해서 아래 요소들을 알고 있어야 합니다.",
        contact=openapi.Contact(email="bbbong9@gmail.com"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
    patterns=v1_api_patterns,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("attendance/api/v1/", include(v1_api_patterns)),
    # Swagger Docs
    path(
        "swagger<format>/",
        schema_view_v1.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/", schema_view_v1.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
