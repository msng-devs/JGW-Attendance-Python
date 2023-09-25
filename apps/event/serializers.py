# --------------------------------------------------------------------------
# Event Application의 Serializer를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        min_length=1,
        max_length=50,
        error_messages={
            "required": "name -> 해당 필드는 필수입니다.",
            "min_length": "name -> 해당 필드는 최소 1자리 이상이여야 합니다.",
            "max_length": "name -> 해당 필드는 50자 이하여야 합니다.",
        },
    )

    index = serializers.CharField(
        required=False,
        max_length=255,
        error_messages={"max_length": "index -> 해당 필드는 255자 이하여야 합니다."},
    )

    start_date_time = serializers.DateTimeField(
        required=True, error_messages={"required": "start_date_time -> 해당 필드는 필수입니다."}
    )

    end_date_time = serializers.DateTimeField(
        required=True, error_messages={"required": "end_date_time -> 해당 필드는 필수입니다."}
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "index",
            "start_date_time",
            "end_date_time",
        ]
