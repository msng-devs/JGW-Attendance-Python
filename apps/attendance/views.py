# --------------------------------------------------------------------------
# Attendance Application의 Views를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

from django.conf import settings

from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import AttendanceType, Attendance
from .serializers import AttendanceSerializer, AttendanceTypeSerializer
from apps.common.models import Member
from apps.utils.permissions import get_auth_header, IsAdminOrSelf, IsProbationaryMember
from apps.utils.decorators import common_swagger_decorator
from apps.utils.paginations import CustomBasePagination
from apps.utils import filters as filters
from apps.utils.scheduler import send_mail
from apps.utils import documentation as docs

logger = logging.getLogger("django")


class AddAttendance(APIView):
    """
    신규 AttendanceCode 추가

    ---
    RBAC - 4(어드민)

    해당 API를 통해 신규 AttendanceCode를 추가할 수 있습니다.
    """

    permission_classes = [IsAdminOrSelf]
    serializer_class = AttendanceSerializer

    @common_swagger_decorator
    def post(self, request):
        data_with_meta = request.data.copy()
        data_with_meta["created_by"] = request.uid
        data_with_meta["modified_by"] = request.uid

        serializer = self.serializer_class(data=data_with_meta)

        if serializer.is_valid():
            serializer.save()

            if not getattr(settings, "TESTING_MODE", False):
                # 메일 발송
                target_member = Member.objects.filter(id=request.uid)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AttendanceList(generics.ListAPIView):
    """
    다수 Attendance를 조회하는 API

    세부 사항은 swagger docs에 기재되어 있습니다.
    """

    queryset = Attendance.objects.all().order_by("-id")
    permission_classes = [IsProbationaryMember]
    serializer_class = AttendanceSerializer
    pagination_class = CustomBasePagination
    filterset_class = filters.AttendanceFilter

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        print(request.uid)
        uid, role_id = get_auth_header(request)

        # 권한 체크
        member_id_param = request.query_params.get("memberID")
        if member_id_param and member_id_param != uid and role_id < 4:
            raise PermissionDenied("해당 정보를 열람할 권한이 없습니다.")

        return self.list(request, *args, **kwargs)


class AttendanceDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    AttendanceCode API

    ---
    출결 코드를 추가하고, 삭제하고, 사용하는 API를 제공합니다.
    """

    queryset = Attendance.objects.all()
    permission_classes = [IsAdminOrSelf]
    serializer_class = AttendanceSerializer
    lookup_field = "id"
    lookup_url_kwarg = "attendanceId"

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @common_swagger_decorator
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    @common_swagger_decorator
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


GetAttendanceType.__doc__ = docs.get_attendance_type_doc()
AttendanceList.__doc__ = docs.get_attendance_doc()
