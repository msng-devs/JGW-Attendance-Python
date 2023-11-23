# TODO: created_by, modified_by 수정 - 유저가 생성해도 system으로 설정이 되는 듯?
# --------------------------------------------------------------------------
# Event Application의 Views를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

from rest_framework import generics, mixins

from .models import Event
from .serializers import EventSerializer

from core import permissions

from apps.utils import decorators
from apps.utils import documentation as docs
from apps.utils import filters as filters
from apps.utils.paginations import CustomBasePagination

logger = logging.getLogger("django")


class EventList(generics.ListAPIView, generics.CreateAPIView):
    """
    다수 Event를 조회하는 API

    세부 사항은 swagger docs에 기재되어 있습니다.
    """

    queryset = Event.objects.all().order_by("-id")
    serializer_class = EventSerializer
    pagination_class = CustomBasePagination
    filterset_class = filters.EventFilter

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
        단일 Event를 등록

        ---
        RBAC - 4(어드민)

        해당 API를 통해 신규 Event를 추가할 수 있습니다.
        """
        return self.create(request, *args, **kwargs)


class EventDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"
    lookup_url_kwarg = "event_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsUser()]
        return [permissions.IsAdminOrSelf()]

    @decorators.methods_swagger_decorator
    def get(self, request, *args, **kwargs):
        """
        단일 Event를 조회

        ---
        RBAC - 1(Guest) 이상
        """
        return self.retrieve(request, *args, **kwargs)

    @decorators.methods_swagger_decorator
    def put(self, request, *args, **kwargs):
        """
        단일 Event를 업데이트

        ---
        RBAC - 4(임원진)

        부분 업데이트를 지원합니다.
        """
        return self.update(request, *args, **kwargs, partial=True)

    @decorators.methods_swagger_decorator
    def delete(self, request, *args, **kwargs):
        """
        단일 Event를 제거

        ---
        RBAC - 4(임원진)
        """
        return self.destroy(request, *args, **kwargs)


EventList.__doc__ = docs.get_event_doc()
