import logging

import string
import random
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
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
from apps.utils.permissions import (
    IsAdminOrSelf,
    IsProbationaryMember,
)
from apps.utils.decorators import common_swagger_decorator
from apps.utils.paginations import CustomBasePagination
from apps.utils import filters as filters
from apps.utils import constants as constant

logger = logging.getLogger("django")


class AddTimeTable(APIView):
    """
    신규 TimeTable 추가

    ---
    RBAC - 4(어드민)

    해당 API를 통해 신규 TimeTable을 추가할 수 있습니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """

    permission_classes = [IsAdminOrSelf]
    serializer_class = TimeTableSerializer

    @common_swagger_decorator
    def post(self, request, *args, **kwargs):
        data_with_meta = request.data.copy()
        data_with_meta["created_by"] = request.uid
        data_with_meta["modified_by"] = request.uid

        serializer = self.serializer_class(data=data_with_meta)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAttendanceCode(APIView):
    """
    AttendanceCode로 출결 등록

    ---
    RBAC - 2(수습 회원)

    해당 API를 통해 Attendance Code로 출결을 등록할 수 있습니다.

    ## Parameter 설명
        - timetableId: 출결을 등록할 TimeTable의 ID

    * @author 이준혁(39기) bbbong9@gmail.com
    """

    register_attendance_type = 1
    permission_classes = [IsProbationaryMember]
    serializer_class = AttendanceSerializer

    @common_swagger_decorator
    def post(self, request, timetableId):
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

        attendance_serializer = self.serializer_class(data=data)
        if attendance_serializer.is_valid():
            attendance_serializer.save()

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
            return Response(attendance_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            attendance_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class TimeTableList(generics.ListAPIView):
    """
    다수 TimeTable 조회

    ---
    Auth - 인증 필요 (문서 설명 수정 예정)

    여러 time table들을 조회, 페이징, 정렬, 필터링을 통해 조회할 수 있습니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """

    queryset = TimeTable.objects.all().order_by("-id")
    permission_classes = [IsAdminOrSelf]
    serializer_class = TimeTableSerializer
    pagination_class = CustomBasePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.TimeTableFilter

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TimeTableDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    TimeTable API

    ---
    TimeTable을 조회하고, 삭제하고, 수정하는 API를 제공합니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """

    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [IsAdminOrSelf]
    lookup_field = "id"
    lookup_url_kwarg = "timetableId"

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @common_swagger_decorator
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    @common_swagger_decorator
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AttendanceCodeDetail(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    AttendanceCode API

    ---
    출결 코드를 추가하고, 삭제하고, 사용하는 API를 제공합니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """

    queryset = TimeTable.objects.all()
    serializer_class = AttendanceCodeSerializer
    permission_classes = [IsAdminOrSelf]
    lookup_field = "id"
    lookup_url_kwarg = "timetableId"

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        timetableId = kwargs.get("timetableId")

        time_table = get_object_or_404(TimeTable, id=timetableId)
        attendance_code = AttendanceCodeService.get_code_by_time_table(time_table.id)

        if not attendance_code:
            raise NotFound("Code not found")

        serializer = super().get_serializer(attendance_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @common_swagger_decorator
    def post(self, request, *args, **kwargs):
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

    @common_swagger_decorator
    def delete(self, request, *args, **kwargs):
        timetableId = kwargs.get("timetableId")

        time_table = get_object_or_404(TimeTable, id=timetableId)

        attendance_code = AttendanceCodeService.get_code_by_time_table(time_table.id)

        if not attendance_code:
            raise NotFound("Code not found")

        return self.destroy(request, *args, **kwargs)
