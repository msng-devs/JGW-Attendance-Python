# TODO: 출결 기한이 만료된 경우, ACK로 출석을 하지 않은 유저들의 출석 정보를 ABS로 업데이트.
# --------------------------------------------------------------------------
# Attendance Application의 Views를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

from django.conf import settings

from rest_framework import mixins, generics
from rest_framework.exceptions import PermissionDenied

from .models import AttendanceType, Attendance
from .serializers import AttendanceSerializer, AttendanceTypeSerializer
from apps.common.models import Member
from apps.utils.permissions import get_auth_header, IsAdminOrSelf, IsProbationaryMember
from apps.utils import decorators
from apps.utils.paginations import CustomBasePagination
from apps.utils import filters as filters
from apps.utils.scheduler import send_mail
from apps.utils import documentation as docs

logger = logging.getLogger("django")


class GetAttendanceType(generics.ListAPIView):
    """
    출결 종류를 조회하는 API

    세부 사항은 swagger docs에 기재되어 있습니다.
    """

    queryset = AttendanceType.objects.all().order_by("-id")
    permission_classes = [IsAdminOrSelf]
    serializer_class = AttendanceTypeSerializer
    pagination_class = CustomBasePagination
    filterset_class = filters.AttendanceTypeFilter

    @decorators.common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AttendanceListCreate(generics.ListCreateAPIView):
    """
    다수 Attendance를 조회하는 API

    세부 사항은 swagger docs에 기재되어 있습니다.
    """

    queryset = Attendance.objects.all().order_by("-id")
    serializer_class = AttendanceSerializer
    pagination_class = CustomBasePagination
    filterset_class = filters.AttendanceFilter

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrSelf()]
        return [IsProbationaryMember()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.uid, modified_by=self.request.uid)

        if not getattr(settings, "TESTING_MODE", False):
            # 메일 발송
            target_member = Member.objects.filter(id=self.request.uid)
            to_email = target_member.values_list("email", flat=True)[0]
            send_mail(
                to=to_email,
                subject="[자람 그룹웨어] 새로운 출석 정보가 등록되었습니다.",
                template="plain_text",
                args={
                    "content": "새로운 출석 정보가 등록되었습니다. 자세한 내용은 자람 그룹웨어를 확인해주세요.",
                    "subject": "새로운 출석 정보가 등록되었습니다",
                },
                service_name="AttendanceService",
            )

    @decorators.common_swagger_decorator
    def get(self, request, *args, **kwargs):
        uid, role_id = get_auth_header(request)

        # 권한 체크
        member_id_param = request.query_params.get("memberID")
        if member_id_param and member_id_param != uid and role_id < 4:
            raise PermissionDenied("해당 정보를 열람할 권한이 없습니다.")

        return self.list(request, *args, **kwargs)

    @decorators.methods_swagger_decorator
    def post(self, request, *args, **kwargs):
        """
        신규 Attendance추가

        ---
        RBAC - 4(어드민)

        해당 API를 통해 신규 Attendance를 추가할 수 있습니다.
        """
        return self.create(request, *args, **kwargs)


class AttendanceDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Attendance.objects.all()
    permission_classes = [IsAdminOrSelf]
    serializer_class = AttendanceSerializer
    lookup_field = "id"
    lookup_url_kwarg = "attendanceId"

    @decorators.methods_swagger_decorator
    def get(self, request, *args, **kwargs):
        """
        단일 Attendance를 조회

        ---
        RBAC - 2(수습 회원) 이상

        자신의 정보를 조회할 때는 role이 2(수습 회원)이어도 괜찮습니다.
        다만, 다른 사람의 정보를 조회할 때는 role이 4(임원진)이어야 합니다.
        """
        return self.retrieve(request, *args, **kwargs)

    @decorators.methods_swagger_decorator
    def put(self, request, *args, **kwargs):
        """
        Attendance를 업데이트

        ---
        RBAC - 4(어드민)

        부분 업데이트를 지원합니다.
        """
        return self.update(request, *args, **kwargs, partial=True)

    @decorators.methods_swagger_decorator
    def delete(self, request, *args, **kwargs):
        """
        Attendance를 제거

        ---
        RBAC - 4(어드민)
        """
        return self.destroy(request, *args, **kwargs)


GetAttendanceType.__doc__ = docs.get_attendance_type_doc()
AttendanceListCreate.__doc__ = docs.get_attendance_doc()
