from django.utils import timezone
from django.test import TestCase

from datetime import timedelta

from apps.common.models import Member, Role
from apps.timetable.models import TimeTable
from apps.event.models import Event
from apps.attendance.models import AttendanceType, Attendance

from core.scheduler import update_attendance_type_apr, update_absent_attendance_info


class SchedulerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.roles = [
            Role.objects.create(id=1, name="ROLE_GUEST"),
            Role.objects.create(id=2, name="ROLE_USER0"),
            Role.objects.create(id=3, name="ROLE_USER1"),
            Role.objects.create(id=4, name="ROLE_ADMIN"),
            Role.objects.create(id=5, name="ROLE_DEV"),
        ]

        cls.attendance_type = [
            AttendanceType.objects.create(id=1, name="UNA"),
            AttendanceType.objects.create(id=2, name="APR"),
            AttendanceType.objects.create(id=3, name="ABS"),
            AttendanceType.objects.create(id=4, name="ACK"),
        ]

        cls.members = [
            Member.objects.create(
                id="test_probationary_member_123",
                name="test_member_name_3",
                email="test_member_email_3@example.com",
                role=cls.roles[1],
                status=True,
            ),
        ]

    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            index="Test Index",
            start_date_time=timezone.now() - timedelta(days=2),
            end_date_time=timezone.now() - timedelta(days=1)
        )
        self.time_table = TimeTable.objects.create(
            name="Test Time Table",
            index="Test Index",
            event=self.event,
            start_date_time=timezone.now(),
            end_date_time=timezone.now() + timedelta(days=1)
        )
        self.outdated_time_table = TimeTable.objects.create(
            name="Test Outdated Time Table",
            index="Test Index",
            event=self.event,
            start_date_time=timezone.now() - timedelta(days=2),
            end_date_time=timezone.now() - timedelta(days=1)
        )
        self.attendance = Attendance.objects.create(
            member=self.members[0],
            time_table=self.time_table,
            attendance_type=self.attendance_type[0],
            index="Test Index"
        )
        self.outdated_attendance = Attendance.objects.create(
            member=self.members[0],
            time_table=self.outdated_time_table,
            attendance_type=self.attendance_type[1],
            index="Test Index"
        )

    def test_update_attendance_type_apr(self):
        update_attendance_type_apr()
        self.attendance.refresh_from_db()
        self.assertEqual("APR", self.attendance.attendance_type.name)

    def test_update_absent_attendance_info(self):
        update_absent_attendance_info()
        self.outdated_attendance.refresh_from_db()
        self.assertEqual("ABS", self.outdated_attendance.attendance_type.name)


# class AttendanceSchedulerTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # 테스트케이스 단계에서 로그가 쌓이는지 확인하기 위해 로깅 레벨을 설정
#         logging.disable(logging.NOTSET)

#         cls.pull_socket = TestUtils.make_test_pull_socket(host="127.0.0.1", port=5555)

#         cls.roles = [
#             Role.objects.create(id=1, name="ROLE_GUEST"),
#             Role.objects.create(id=2, name="ROLE_USER0"),
#             Role.objects.create(id=3, name="ROLE_USER1"),
#             Role.objects.create(id=4, name="ROLE_ADMIN"),
#             Role.objects.create(id=5, name="ROLE_DEV"),
#         ]

#         cls.members = [
#             Member.objects.create(
#                 id="test_member_uid_123456789012",
#                 name="이준혁",
#                 email="bbbong9@gmail.com",
#                 role=cls.roles[3],
#                 status=True,
#             ),
#         ]

#         cls.attendance_type = [
#             AttendanceType.objects.create(id=1, name="test_attendance_type_1"),
#         ]

#         cls.events = [
#             Event.objects.create(
#                 id=1,
#                 name="test_event_1",
#                 index="test event index 1",
#                 start_date_time="2022-08-04T04:16:00Z",
#                 end_date_time="2022-08-04T04:16:00Z",
#             ),
#         ]

#         cls.timetables = [
#             TimeTable.objects.create(
#                 name="test_timetable_1",
#                 index="test timetable index 1",
#                 event=cls.events[0],
#                 start_date_time="2022-08-04T04:16:00Z",
#                 end_date_time="2022-08-04T04:16:00Z",
#             ),
#         ]

#     def setUp(self):
#         self.client = APIClient()
#         self.test_member_uid = "test_member_uid_123456789012"
#         self.test_role_id = 4

#     def test_add_attendance_scheduler(self):
#         attendance_url = reverse("attendance_list_create")

#         # given
#         self.client = TestUtils.add_header(
#             self.client, self.test_member_uid, self.test_role_id
#         )

#         attendance_data = {
#             "member_id": self.test_member_uid,
#             "attendance_type_id": 1,
#             "time_table_id": 1,
#             "index": "this is test attendance",
#         }

#         # when
#         response = self.client.post(
#             attendance_url,
#             data=json.dumps(attendance_data),
#             content_type="application/json",
#         )

#         # then
#         # expected_data = {
#         #     "index": self.attendance_data["index"],
#         #     "attendance_type_id": self.attendance_data["attendance_type_id"],
#         #     "member_id": self.attendance_data["member_id"],
#         #     "time_table_id": self.attendance_data["time_table_id"],
#         # }

#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # TestUtils.verify_response_data(response, expected_data)
#         print(response.json())
#         TestUtils.send_mail(self.pull_socket)

#     def tearDown(self):
#         pass

#     @classmethod
#     def tearDownClass(cls):
#         # 로그 레벨을 다시 원래대로 돌려놓음
#         logging.disable(logging.CRITICAL)
#         super().tearDownClass()
