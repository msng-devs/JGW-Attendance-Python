# flake8: noqa
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
from django.conf import settings
from django.urls import path, include

from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

from apps.utils.documentation import CustomOpenAPISchemaGenerator

api_description = """
# 소개
해당 API를 사용하여 학회의 행사와 타임테이블을 관리하거나, 출결을 관리할 수 있습니다.

해당 API를 사용하기 위해서 아래 요소들을 알고 있어야 합니다.

## Event(행사)
Event는 학회에서 진행하는 행사를 의미합니다. 예) 1학기 세미나, 동계 워크샵 등

출결 및 타임테이블을 생성하기 위해서는 이 행사를 우선적으로 생성해야 합니다.

## TimeTable(시간표)
TimeTable은 행사에 속하는 시간표를 의미합니다. 실제 자람의 세미나 출결관리를 예로 들어 살펴보겠습니다.

'1학기 세미나' 라는 Event(행사)가 있습니다. 자람 회원이라면 아시겠지만, 세미나라는 행사는 하루만 진행하는 행사가 아닙니다. 주마다 한번씩 진행하죠.

따라서 1주차,2주차,3주차 …​ 이런식으로 시간표를 생성하고 각각의 주마다 출결 확인을 합니다.

즉 이러한 time table 별로 출결을 등록하는 방식으로 동작합니다. 따라서 time table을 생성할 때에는 함께 '미결' 출결 정보를 생성하는 것을 권장합니다.

## Attendance(출결)
Attendance는 출결을 의미합니다. 위에서 언급했듯이 timeTable별로 출결을 관리할 수 있습니다. 단, 한개의 timeTable에는 회원당 1개의 출결 정보만 기록할 수 있다는 것을 명심하세요.

## AttendanceType(출결 타입)
AttendanceType은 출결 타입을 의미합니다. 미결,출결,결석,출석 인정으로 구성됩니다. 위에서 살펴본 Attendance의 출결 유형을 구분하기 위해 사용합니다.

## Attendance Code(출결 코드)
attendanceCode는 출결 코드를 의미합니다. 해당 코드를 사용하여 일반 사용자가 출결을 등록할 수 있습니다.

동작방식은 대학교의 출결 형태를 떠올리면 쉽습니다.

1. 위에서 살펴본 time table(시간표)에 관리자(임원진)이 출결 코드를 발급합니다.

2. 발급된 출결 코드를 사용하여 일반 사용자가 출결을 등록합니다.

단 출결 코드는 아래 제약 사항을 가집니다.

 * 초 단위로 유효시간을 설정해야 하며 최대 2592000초(30일)까지 설정할 수 있습니다.(영구적인 코드 발급이 가능하지만, 권장하지 않습니다.)

 * 한 Time Table(시간표)에는 한개의 출결코드를 가질 수 있습니다.\n
"""

v1_api_patterns = [
    path("attendance/", include("apps.attendance.urls")),
    path("event/", include("apps.event.urls")),
    path("timetable/", include("apps.timetable.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("attendance/api/v1/", include(v1_api_patterns)),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="JGW Attendance Management System API",
        default_version="v1",
        description=api_description,
        contact=openapi.Contact(email="bbbong9@gmail.com"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
    patterns=urlpatterns,
    generator_class=CustomOpenAPISchemaGenerator,
)

if settings.DEBUG:
    urlpatterns += [
        # Swagger Docs
        path(
            "attendance/api/v1/swagger<format>/",
            schema_view_v1.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "attendance/api/v1/swagger/",
            schema_view_v1.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "attendance/api/v1/redoc/",
            schema_view_v1.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
