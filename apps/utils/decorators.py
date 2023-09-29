# --------------------------------------------------------------------------
# swagger 문서를 위한 decorator를 정의하는 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def common_swagger_decorator(func):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="uid",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 UID 입니다.",
            ),
            openapi.Parameter(
                name="role_id",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 Role ID입니다.",
            ),
        ],
    )
    def _decorated(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)

    return _decorated


def methods_swagger_decorator(func):
    doc_string = func.__doc__.split("---")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="uid",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 UID 입니다.",
            ),
            openapi.Parameter(
                name="role_id",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 Role ID입니다.",
            ),
        ],
        operation_summary=doc_string[0],
        operation_description=doc_string[1],
    )
    def _decorated(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)

    return _decorated


def attendance_code_register_swagger_decorator(func):
    from apps.attendance.serializers import (
        AttendanceCodeRegisterRequestSerializer,
        AttendanceSerializer,
    )

    @swagger_auto_schema(
        request_body=AttendanceCodeRegisterRequestSerializer,
        responses={
            201: openapi.Response(
                description="", schema=AttendanceSerializer
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                name="uid",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 UID 입니다.",
            ),
            openapi.Parameter(
                name="role_id",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 Role ID입니다.",
            ),
        ],
    )
    def _decorated(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)

    return _decorated


def attendance_code_add_swagger_decorator(func):
    from apps.attendance.serializers import (
        AttendanceCodeSerializer,
    )
    doc_string = func.__doc__.split("---")

    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                description="", schema=AttendanceCodeSerializer
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                name="uid",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 UID 입니다.",
            ),
            openapi.Parameter(
                name="role_id",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="요청을 보내는 유저의 Role ID입니다.",
            ),
        ],
        operation_summary=doc_string[0],
        operation_description=doc_string[1],
    )
    def _decorated(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)

    return _decorated
