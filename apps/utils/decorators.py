from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def common_swagger_decorator(func):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="uid",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="User ID",
            ),
            openapi.Parameter(
                name="role_id",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Role ID",
            ),
        ]
    )
    def _decorated(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)

    return _decorated
