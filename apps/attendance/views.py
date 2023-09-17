import logging

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination

from .models import AttendanceType, Attendance
from .serializers import AttendanceSerializer, AttendanceTypeSerializer
from apps.common.models import Member
from apps.utils.permissions import get_auth_header, check_permission
from apps.utils.scheduler import send_mail

logger = logging.getLogger("django")


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"
    max_page_size = 200
    page_query_param = "page"
    ordering = "-id"  # Default ordering


class AddAttendance(APIView):
    """
    신규 AttendanceCode 추가

    ---
    RBAC - 4(어드민)

    해당 API를 통해 신규 AttendanceCode를 추가할 수 있습니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """

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

            # 메일 발송
            target_member = Member.objects.filter(id=uid)
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


class GetAttendanceType(APIView):
    """
    다수 attendanceType를 조회

    ---
    등록되어 있는 모든 AttendanceType를 확인할 수 있습니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """
    def get(self, request):
        # Allow all
        uid, role_id = get_auth_header(request)

        attendance_types = AttendanceType.objects.all()
        serializer = AttendanceTypeSerializer(attendance_types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendanceList(APIView):
    """
    다수 Attendance를 조회

    ---
    RBAC - 2(수습 회원) 이상

    자신의 정보를 조회할 때는 role이 2(수습 회원)이어도 괜찮습니다.
    다만, 다른 사람의 정보를 조회할 때는 role이 4(임원진)이어야 합니다.

    ---
    Query Options, 혹은 Page Options 등을 사용하여 attendance를 조회하거나, pagination 작업을 수행할 수 있습니다.

    주의! 모든 option들은 단 한개의 인자만 수용가능합니다!

    (O) "?memberID=456465456&timeTableID=1"

    (X) "?memberID=456465456,456456456465&timeTableID=1,123123"

    또한 모든 Option들은 And로 동작합니다.

    만약 "?memberID=456465456&timeTableID=1"라는 인자가 있다면, memberID가 "456465456"이고, timeTableID가 1인 Attendance를 찾습니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """
    def get(self, request):
        # TODO: query param 없을 때 분기 처리
        uid, role_id = get_auth_header(request)
        query_params = request.query_params

        # 권한 체크
        member_id_param = query_params.get("memberID")
        if member_id_param and member_id_param != uid and role_id < 4:
            raise PermissionDenied("해당 정보를 열람할 권한이 없습니다.")

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
    """
    AttendanceCode API

    ---
    출결 코드를 추가하고, 삭제하고, 사용하는 API를 제공합니다.

    * @author 이준혁(39기) bbbong9@gmail.com
    """
    def get(self, request, attendanceId):
        uid, role_id = get_auth_header(request)
        query_params = request.query_params

        # 권한 체크
        member_id_param = query_params.get("memberID")
        if member_id_param and member_id_param != uid and role_id < 4:
            raise PermissionDenied("해당 정보를 열람할 권한이 없습니다.")

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
