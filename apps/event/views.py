# --------------------------------------------------------------------------
# Event Application의 Views를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer
from apps.utils.permissions import IsAdminOrSelf
from apps.utils.decorators import common_swagger_decorator
from apps.utils.paginations import CustomBasePagination
from apps.utils import filters as filters
from apps.utils import documentation as docs

logger = logging.getLogger("django")


class AddEvent(APIView):
    """
    단일 Event를 등록

    ---
    RBAC - 4(어드민)

    해당 API를 통해 신규 Event를 추가할 수 있습니다.
    """

    permission_classes = [IsAdminOrSelf]
    serializer_class = EventSerializer

    @common_swagger_decorator
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventList(generics.ListAPIView):
    """
    다수 Event를 조회하는 API

    세부 사항은 swagger docs에 기재되어 있습니다.
    """

    queryset = Event.objects.all().order_by("-id")
    permission_classes = [IsAdminOrSelf]
    serializer_class = EventSerializer
    pagination_class = CustomBasePagination
    filterset_class = filters.EventFilter

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    Event API

    ---
    event 를 추가하고, 삭제하고, 수정하는 API를 제공합니다.
    """

    queryset = Event.objects.all()
    permission_classes = [IsAdminOrSelf]
    serializer_class = EventSerializer
    lookup_field = "id"
    lookup_url_kwarg = "eventId"

    @common_swagger_decorator
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @common_swagger_decorator
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    @common_swagger_decorator
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


EventList.__doc__ = docs.get_event_doc()
