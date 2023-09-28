# --------------------------------------------------------------------------
# TimeTable Application의 Views를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

import string
import random
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import TimeTable
from .serializers import TimeTableSerializer
from apps.attendance.serializers import (
    AttendanceSerializer,
    AttendanceCodeSerializer,
    AttendanceCodeAddRequestSerializer,
)
from apps.common.models import Member
from apps.utils.attendancecode import AttendanceCodeService
from apps.utils.scheduler import send_mail
from apps.utils import permissions
from apps.utils import decorators
from apps.utils.paginations import CustomBasePagination
from apps.utils import filters as filters
from apps.utils import documentation as docs

logger = logging.getLogger("django")


class RegisterAttendanceCode(generics.CreateAPIView):
    # TODO: Swagger 문서 개선 - request body param을 code만 입력받도록 수정.
    """
    AttendanceCode로 출결 등록

    ---
    RBAC - 2(수습 회원)

    해당 API를 통해 Attendance Code로 출결을 등록할 수 있습니다.
    """

    register_attendance_type = 1
    permission_classes = [permissions.IsProbationaryMember]
    serializer_class = AttendanceSerializer

    @decorators.common_swagger_decorator
    def create(self, request, *args, **kwargs):
        timetableId = kwargs.get("timetableId")
        time_table = get_object_or_404(TimeTable, id=timetableId)

        code = request.data.get("code")
        if not code:
            return Response(
                {"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        code_info = AttendanceCodeService.get_code_by_time_table(time_table.id)
        if not code_info.code == code:
            return Response(
                {"error": "ATTENDANCE_CODE_NOT_VALID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "attendance_type_id": self.register_attendance_type,
            "created_by": "system",
            "modified_by": "system",
            "index": "출결 코드를 통해 처리된 출결 정보 입니다.",
            "member_id": request.uid,
            "time_table_id": timetableId,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if not getattr(settings, "TESTING_MODE", False):
            # 메일 발송
            target_member = Member.objects.filter(id=request.uid)
            to_email = target_member.values_list("email", flat=True)[0]
            send_mail(
                to=to_email,
                subject="출결 코드를 통해 출결 정보가 처리되었습니다.",
                template="plain_text",
                args={
                    "content": "출결 코드를 통해 출결 정보가 처리되었습니다. 자세한 내용은 자람 그룹웨어를 확인해주세요.",
                    "subject": "출결 코드를 통해 출결 정보가 처리되었습니다",
                },
                service_name="TimeTableService",
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TimeTableListCreate(generics.ListAPIView):
    """
    다수 TimeTable 조회하는 API

    세부 사항은 swagger docs에 기재되어 있습니다.
    """

    queryset = TimeTable.objects.all().order_by("-id")
    serializer_class = TimeTableSerializer
    pagination_class = CustomBasePagination
    filterset_class = filters.TimeTableFilter

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminOrSelf()]
        return [permissions.IsUser()]

    @decorators.common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @decorators.methods_swagger_decorator
    def post(self, request, *args, **kwargs):
        """
        신규 TimeTable 추가

        ---
        RBAC - 4(어드민)

        해당 API를 통해 신규 TimeTable을 추가할 수 있습니다.
        """
        data_with_meta = request.data.copy()
        data_with_meta["created_by"] = request.uid
        data_with_meta["modified_by"] = request.uid

        serializer = self.serializer_class(data=data_with_meta)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeTableDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    lookup_field = "id"
    lookup_url_kwarg = "timetableId"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsUser()]
        return [permissions.IsAdminOrSelf()]

    @decorators.methods_swagger_decorator
    def get(self, request, *args, **kwargs):
        """
        단일 TimeTable 조회

        ---
        RBAC - 1(Guest) 이상
        """
        return self.retrieve(request, *args, **kwargs)

    @decorators.methods_swagger_decorator
    def put(self, request, *args, **kwargs):
        """
        TimeTable 정보 수정

        ---
        RBAC - 4(어드민)

        부분 업데이트를 지원합니다.
        """
        return self.update(request, *args, **kwargs, partial=True)

    @decorators.methods_swagger_decorator
    def delete(self, request, *args, **kwargs):
        """
        단일 TimeTable 삭제

        ---
        RBAC - 4(어드민)
        """
        return self.destroy(request, *args, **kwargs)


class AttendanceCodeDetail(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    # TODO: Refactoring 필요
    queryset = TimeTable.objects.all()
    permission_classes = [permissions.IsAdminOrSelf]
    serializer_class = AttendanceCodeSerializer
    lookup_field = "id"
    lookup_url_kwarg = "timetableId"

    @decorators.methods_swagger_decorator
    def get(self, request, *args, **kwargs):
        """
        AttendanceCode 조회

        ---
        RBAC - 4(어드민)

        해당 API를 통해 해당하는 time table의 AttendanceCode를 조회할 수 있습니다.
        """
        timetableId = kwargs.get("timetableId")

        time_table = get_object_or_404(TimeTable, id=timetableId)
        attendance_code = AttendanceCodeService.get_code_by_time_table(time_table.id)

        if not attendance_code:
            raise NotFound("Code not found")

        serializer = super().get_serializer(attendance_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.methods_swagger_decorator
    def post(self, request, *args, **kwargs):
        """
        신규 AttendanceCode 추가

        ---
        RBAC - 4(어드민)

        해당 API를 통해 신규 AttendanceCode를 추가할 수 있습니다.
        """
        timetableId = kwargs.get("timetableId")

        time_table = get_object_or_404(TimeTable, id=timetableId)

        request_serializer = AttendanceCodeAddRequestSerializer(data=request.data)

        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

        if request_serializer.validated_data["exp_sec"] == -1:
            expire_at = None  # 영구적인 코드
        else:
            expire_at = datetime.datetime.now() + datetime.timedelta(
                seconds=request_serializer.validated_data["exp_sec"]
            )

        serializer_data = {
            "code": code,
            "time_table_id": time_table.id,
            "expire_at": expire_at,
        }

        serializer = super().get_serializer(data=serializer_data)
        if serializer.is_valid():
            response_data = AttendanceCodeService.create_code(serializer)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.methods_swagger_decorator
    def delete(self, request, *args, **kwargs):
        """
        AttendanceCode 삭제

        ---
        RBAC - 4(어드민)

        해당 API를 통해 해당하는 time table의 AttendanceCode를 삭제할 수 있습니다.
        """
        timetableId = kwargs.get("timetableId")

        time_table = get_object_or_404(TimeTable, id=timetableId)

        attendance_code = AttendanceCodeService.get_code_by_time_table(time_table.id)

        if not attendance_code:
            raise NotFound("Code not found")

        return self.destroy(request, *args, **kwargs)


TimeTableListCreate.__doc__ = docs.get_timetable_doc()
