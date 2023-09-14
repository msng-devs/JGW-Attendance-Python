from django.utils.six import text_type

from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.exceptions import PermissionDenied

from apps.common.models import Role


def get_auth_header(request):
    uid = request.META.get("HTTP_USER_PK", b"")
    role_id = request.META.get("HTTP_ROLE_PK", b"")

    if isinstance(uid, text_type) and isinstance(role_id, text_type):
        uid = uid.encode(HTTP_HEADER_ENCODING)
        role_id = role_id.encode(HTTP_HEADER_ENCODING)

    return uid, role_id


def check_permission(uid, role_id, target_member_id=None):
    try:
        admin_role_id = Role.objects.get(name="ROLE_ADMIN").id

        # 해당 유저의 role을 가져와 권한 확인
        if role_id < admin_role_id:
            if not target_member_id or uid != target_member_id:
                raise PermissionDenied("FORBIDDEN_ROLE")

    except Role.DoesNotExist:
        raise PermissionDenied("Admin role not found.")
