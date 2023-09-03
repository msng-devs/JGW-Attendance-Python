from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import AttendanceType, Attendance
from .serializers import AttendanceSerializer, AttendanceTypeSerializer
from apps.utils.permissions import get_auth_header, check_permission


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"
    max_page_size = 200
    page_query_param = "page"
    ordering = "-id"  # Default ordering


class AddAttendance(APIView):
    def post(self, request):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        data_with_meta = request.data.copy()
        data_with_meta["created_by"] = uid
        data_with_meta["modified_by"] = uid

        serializer = AttendanceSerializer(data=data_with_meta)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAttendanceType(APIView):
    def get(self, request):
        # Allow all
        uid, role_id = get_auth_header(request)

        attendance_types = AttendanceType.objects.all()
        serializer = AttendanceTypeSerializer(attendance_types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendanceList(APIView):
    def get(self, request):
        # TODO: query param 없을 때 분기 처리
        uid, role_id = get_auth_header(request)
        query_params = request.query_params

        # 권한 체크
        member_id_param = query_params.get("memberID")
        if member_id_param and member_id_param != uid and role_id < 4:
            return Response(
                {"detail": "FORBIDDEN_ROLE"}, status=status.HTTP_403_FORBIDDEN
            )

        # 쿼리 필터 작성
        filters = {}
        param_to_field_mapping = {
            "memberID": "member_id",
            "timeTableID": "time_table_id",
            "createdBy": "created_by",
            "modifiedBy": "modified_by",
            "attendanceTypeID": "attendance_type_id",
        }

        for param, field_name in param_to_field_mapping.items():
            if query_params.get(param):
                filters[field_name] = query_params.get(param)

        # Range query handling
        date_range_queries = [
            ("startCreatedDateTime", "endCreatedDateTime", "created_datetime"),
            ("startModifiedDateTime", "endModifiedDateTime", "modified_datetime"),
        ]

        for start_param, end_param, field_name in date_range_queries:
            start_date = query_params.get(start_param)
            end_date = query_params.get(end_param)

            if start_date:
                filters[f"{field_name}__gte"] = start_date

            if end_date:
                filters[f"{field_name}__lte"] = end_date

        # Like query handling
        if "index" in query_params:
            filters["index__icontains"] = query_params["index"]

        # 결과 가져오기 및 페이지네이션
        attendances = Attendance.objects.filter(**filters)
        # TODO: Pagenation 개선
        # page = self.pagination_class().paginate_queryset(attendances, request)
        # if page is not None:
        #     serializer = AttendanceSerializer(page, many=True)
        #     return self.pagination_class().get_paginated_response(serializer.data)

        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendanceDetail(APIView):
    def get(self, request, attendanceId):
        uid, role_id = get_auth_header(request)
        query_params = request.query_params

        # 권한 체크
        member_id_param = query_params.get("memberID")
        if member_id_param and member_id_param != uid and role_id < 4:
            return Response(
                {"detail": "FORBIDDEN_ROLE"}, status=status.HTTP_403_FORBIDDEN
            )

        attendance = get_object_or_404(Attendance, id=attendanceId)

        serializer = AttendanceSerializer(attendance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, attendanceId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        # attendance 객체 가져오기
        attendance = get_object_or_404(Attendance, id=attendanceId)

        # 객체 삭제
        attendance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, attendanceId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        # attendance 객체 가져오기
        attendance = get_object_or_404(Attendance, id=attendanceId)

        # 데이터 업데이트
        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(modified_by=uid)  # 수정한 사용자를 저장
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
