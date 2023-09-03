from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer
from apps.utils.permissions import get_auth_header, check_permission


class AddEvent(APIView):
    def post(self, request):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventList(APIView):
    def get(self, request):
        uid, role_id = get_auth_header(request)
        query_params = request.query_params

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        if not request.query_params:
            events = Event.objects.all()
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
                "event_datetime": ("startDateTime", "endDateTime"),
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
            events = Event.objects.filter(*like_queries, **filters)

        # Pagination
        page_size = int(query_params.get("size", 1000))
        page_number = int(query_params.get("page", 1))
        sort_option = query_params.get("sort", "id,desc").split(",")
        if len(sort_option) == 1:
            sort_option.append("desc")

        sort_field = sort_option[0]
        sort_direction = "" if sort_option[1].lower() == "asc" else "-"

        events = events.order_by(f"{sort_direction}{sort_field}")
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        events = events[start_index:end_index]

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetail(APIView):
    def get(self, request, eventId):
        uid, role_id = get_auth_header(request)

        event = get_object_or_404(Event, id=eventId)

        serializer = EventSerializer(event)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, eventId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        event = get_object_or_404(Event, id=eventId)
        event.delete()

        return Response(
            {"message": "Event deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request, eventId):
        uid, role_id = get_auth_header(request)

        # RBAC - 4(임원진) 확인
        check_permission(uid, role_id)

        event = get_object_or_404(Event, id=eventId)

        serializer = EventSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
