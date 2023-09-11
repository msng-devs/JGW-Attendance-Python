import logging

import string
import random
import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import TimeTable
from .serializers import TimeTableSerializer
from apps.attendance.serializers import (
    AttendanceSerializer,
    AttendanceCodeSerializer,
    AttendanceCodeAddRequestSerializer,
)
from apps.utils.attendancecode import AttendanceCodeService
from apps.utils.permissions import get_auth_header, check_permission

logger = logging.getLogger("django")


class AddTimeTable(APIView):
    def post(self, request):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        data_with_meta = request.data.copy()
        data_with_meta["created_by"] = uid
        data_with_meta["modified_by"] = uid

        serializer = TimeTableSerializer(data=data_with_meta)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAttendanceCode(APIView):
    register_attendance_type = 1

    def post(self, request, timetableId):
        uid, role_id = get_auth_header(request)
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
            "member_id": uid,
            "time_table_id": timetableId,
        }

        attendance_serializer = AttendanceSerializer(data=data)
        if attendance_serializer.is_valid():
            attendance_serializer.save()
            return Response(attendance_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            attendance_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class TimeTableList(APIView):
    def get(self, request):
        uid, role_id = get_auth_header(request)
        query_params = request.query_params

        if not request.query_params:
            timetables = TimeTable.objects.all()
        else:
            # 쿼리 필터 작성
            filters = {}

            # Equal Query
            filters = {
                "created_by": query_params.get("createdBy"),
                "modified_by": query_params.get("modifiedBy"),
            }

            filters = {k: v for k, v in filters.items() if v is not None}

            # Range Query
            range_fields = {
                "created_datetime": ("startCreatedDateTime", "endCreatedDateTime"),
                "modified_datetime": ("startModifiedDateTime", "endModifiedDateTime"),
                "timetable_datetime": ("startDateTime", "endDateTime"),
            }

            for field, (start_param, end_param) in range_fields.items():
                start_date = query_params.get(start_param)
                end_date = query_params.get(end_param)
                if start_date:
                    filters[f"{field}__gte"] = start_date
                if end_date:
                    filters[f"{field}__lte"] = end_date

            # Like Query
            like_queries = [
                Q(name__icontains=query_params.get("name")),
                Q(index__icontains=query_params.get("index")),
            ]

            # Result
            timetables = TimeTable.objects.filter(*like_queries, **filters)

        # Pagination
        page_size = int(query_params.get("size", 1000))
        page_number = int(query_params.get("page", 1))
        sort_option = query_params.get("sort", "id,desc").split(",")
        if len(sort_option) == 1:
            sort_option.append("desc")

        sort_field = sort_option[0]
        sort_direction = "" if sort_option[1].lower() == "asc" else "-"

        timetables = timetables.order_by(f"{sort_direction}{sort_field}")
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        timetables = timetables[start_index:end_index]

        serializer = TimeTableSerializer(timetables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TimeTableDetail(APIView):
    def get(self, request, timetableId):
        uid, role_id = get_auth_header(request)

        time_table = get_object_or_404(TimeTable, id=timetableId)

        serializer = TimeTableSerializer(time_table)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, timetableId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        time_table = get_object_or_404(TimeTable, id=timetableId)
        time_table.delete()

        return Response({"message": "Successfully deleted."}, status=status.HTTP_200_OK)

    def put(self, request, timetableId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        time_table = get_object_or_404(TimeTable, id=timetableId)

        serializer = TimeTableSerializer(time_table, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modify_by=uid)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceCodeDetail(APIView):
    def get(self, request, timetableId):
        uid, role_id = get_auth_header(request)

        time_table = get_object_or_404(TimeTable, id=timetableId)
        attendance_code = AttendanceCodeService.get_code_by_time_table(time_table.id)

        if not attendance_code:
            return Response(
                {"error": "Code not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AttendanceCodeSerializer(attendance_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, timetableId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(어드민) 확인
        check_permission(uid, role_id)

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

        serializer = AttendanceCodeSerializer(data=serializer_data)
        if serializer.is_valid():
            response_data = AttendanceCodeService.create_code(serializer)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, timetableId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(어드민) 확인
        check_permission(uid, role_id)

        time_table = get_object_or_404(TimeTable, id=timetableId)

        attendance_code = AttendanceCodeService.get_code_by_time_table(time_table.id)

        if not attendance_code:
            return Response(
                {"error": "Code not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # AttendanceCode 객체 삭제
        attendance_code.delete()

        return Response(
            {"message": "AttendanceCode successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
