# --------------------------------------------------------------------------
# AttendanceCode(출석코드)를 생성, 삭제, 조회하는 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
from apps.attendance.models import AttendanceCode
from apps.attendance.serializers import AttendanceCodeSerializer

from core.exceptions import AlreadyHasCodeError, InvalidAttendanceCodeError


class AttendanceCodeService:
    @staticmethod
    def create_code(serializer: AttendanceCodeSerializer):
        validated_data = serializer.validated_data
        time_table_id = validated_data.get("time_table_id")

        # 기존 코드가 있는지 확인
        existing_code = AttendanceCode.objects.filter(
            time_table_id=time_table_id
        ).first()
        if existing_code:
            raise AlreadyHasCodeError

        new_code = AttendanceCode(
            code=validated_data.get("code"),
            time_table_id=time_table_id,
            expire_at=validated_data.get("expire_at"),
        )
        new_code.save()

        return {
            "time_table_id": time_table_id,
            "code": new_code.code,
            "expire_at": new_code.expire_at,
        }

    @staticmethod
    def revoke_code(time_table_id):
        try:
            existing_code = AttendanceCode.objects.get(time_table_id=time_table_id)
            existing_code.delete()
        except AttendanceCode.DoesNotExist:
            raise InvalidAttendanceCodeError

    @staticmethod
    def get_code_by_time_table(time_table_id):
        try:
            existing_code = AttendanceCode.objects.get(time_table__id=time_table_id)

            return existing_code
        except AttendanceCode.DoesNotExist:
            raise InvalidAttendanceCodeError
