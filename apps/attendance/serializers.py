# --------------------------------------------------------------------------
# Attendance Application의 Serializer를 정의한 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from rest_framework import serializers

from .models import Attendance, AttendanceType, AttendanceCode
from apps.common.models import Member


class AttendanceSerializer(serializers.ModelSerializer):
    time_table_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "time_table_id -> 해당 필드는 필수입니다.",
            "invalid": "time_table_id -> 해당 필드는 양수만 입력 가능합니다.",
        },
    )

    member_id = serializers.CharField(
        required=True,
        min_length=28,
        max_length=28,
        error_messages={
            "required": "member_id -> 해당 필드는 필수입니다.",
            "min_length": "member_id -> 해당 필드는 28자이여야합니다.",
            "max_length": "member_id -> 해당 필드는 28자이여야합니다.",
        },
    )

    attendance_type_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "attendance_type_id -> 해당 필드는 필수입니다.",
            "invalid": "attendance_type_id -> 해당 필드는 양수만 입력 가능합니다.",
        },
    )

    index = serializers.CharField(
        max_length=255, error_messages={"max_length": "index -> 해당 필드는 255자 이하여야합니다."}
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "modified_datetime",
            "modified_by",
            "index",
            "attendance_type_id",
            "member_id",
            "time_table_id",
        ]

    def validate_member_id(self, value):
        """
        Check if the given member_id exists in the Member model.
        """
        if not Member.objects.filter(id=value).exists():
            raise serializers.ValidationError("해당 멤버는 존재하지 않습니다.")
        return value


class AttendanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceType
        fields = ["id", "name"]


class AttendanceCodeAddRequestSerializer(serializers.Serializer):
    exp_sec = serializers.IntegerField(
        required=True,
        max_value=2592000,
        min_value=-1,
        error_messages={
            "required": "exp_sec -> 해당 필드는 필수입니다.",
            "max_value": "exp_sec -> 설정가능한 최대 유효 시간은 2592000(초) 입니다.",
            "min_value": "exp_sec -> 해당 필드에 음수는 사용할 수 없습니다. 만약 영구적인 출결 코드를 발급할려면 (-1)을 입력하세요.",  # noqa E501
        },
    )


class AttendanceCodeSerializer(serializers.ModelSerializer):
    time_table_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "time_table_id -> 해당 필드는 필수입니다.",
            "invalid": "time_table_id -> 해당 필드는 양수만 입력 가능합니다.",
        },
    )

    class Meta:
        model = AttendanceCode
        fields = ["code", "time_table_id", "expire_at"]

    def validate_code(self, value):
        if AttendanceCode.objects.filter(code=value).exists():
            raise serializers.ValidationError("이미 존재하는 출석 코드입니다.")
        return value
