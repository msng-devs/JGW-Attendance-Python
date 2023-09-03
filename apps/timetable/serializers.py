from rest_framework import serializers

from .models import TimeTable
from apps.event.models import Event


class TimeTableSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        min_length=1,
        max_length=50,
        error_messages={
            "required": "name -> 해당 필드는 필수 입니다.",
            "min_length": "name -> 해당 필드는 최소 1자리 이상이여야 합니다.",
            "max_length": "name -> 해당 필드는 50자 이하여야 합니다.",
        },
    )

    index = serializers.CharField(
        required=False,
        max_length=200,
        error_messages={"max_length": "index -> 해당 필드는 200자 이하여야 합니다."},
    )

    event_id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "event_id -> 해당 필드는 필수입니다.",
            "min_value": "event_id -> 해당 필드는 양수만 입력 가능합니다.",
        },
    )

    start_date_time = serializers.DateTimeField(
        required=True, error_messages={"required": "start_date_time -> 해당 필드는 필수입니다."}
    )

    end_date_time = serializers.DateTimeField(
        required=True, error_messages={"required": "end_date_time -> 해당 필드는 필수입니다."}
    )

    def to_internal_value(self, data):
        internal_value = super(TimeTableSerializer, self).to_internal_value(data)
        event_id = data.get("event_id")
        if event_id is not None:
            try:
                event = Event.objects.get(id=event_id)
                internal_value["event"] = event
            except Event.DoesNotExist:
                raise serializers.ValidationError(
                    {"event_id": "이 ID를 가진 Event가 존재하지 않습니다."}
                )

        return internal_value

    def update(self, instance, validated_data):
        event = validated_data.pop("event", None)
        instance = super().update(instance, validated_data)
        if event:
            instance.event = event
            instance.save()
        return instance

    class Meta:
        model = TimeTable
        fields = [
            "id",
            "name",
            "index",
            "event_id",
            "start_date_time",
            "end_date_time",
            "modified_datetime",
            "modified_by",
        ]
