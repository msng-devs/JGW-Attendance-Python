# --------------------------------------------------------------------------
# Event Application의 테스트케이스를 정의한 모듈입니다.
#
# :class AttendanceSchedulerTest: Attendance Application의 Scheduler를 테스트합니다.
# :class AttendanceApiTest: Attendance Application의 Endpoint를 테스트합니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

import json

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Attendance, AttendanceType
from apps.timetable.models import TimeTable
from apps.event.models import Event
from apps.common.models import Role, Member
from apps.utils.test_utils import TestUtils


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


class AttendanceApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트케이스 단계에서 로그가 쌓이는지 확인하기 위해 로깅 레벨을 설정
        logging.disable(logging.NOTSET)

        cls.roles = [
            Role.objects.create(id=1, name="ROLE_GUEST"),
            Role.objects.create(id=2, name="ROLE_USER0"),
            Role.objects.create(id=3, name="ROLE_USER1"),
            Role.objects.create(id=4, name="ROLE_ADMIN"),
            Role.objects.create(id=5, name="ROLE_DEV"),
        ]

        cls.members = [
            Member.objects.create(
                id="test_member_uid_123456789012",
                name="test_admin_name",
                email="test_admin_email@example.com",
                role=cls.roles[3],
                status=True,
            ),
            Member.objects.create(
                id="test_member_uid_987654321098",
                name="another_admin_name",
                email="another_admin_email@example.com",
                role=cls.roles[3],
                status=True,
            ),
            Member.objects.create(
                id="test_not_admin_member_123456",
                name="test_member_name_2",
                email="test_member_email_2@example.com",
                role=cls.roles[2],
                status=True,
            ),
            Member.objects.create(
                id="test_probationary_member_123",
                name="test_member_name_3",
                email="test_member_email_3@example.com",
                role=cls.roles[1],
                status=True,
            ),
        ]

        cls.attendance_type = [
            AttendanceType.objects.create(id=1, name="test_attendance_type_1"),
            AttendanceType.objects.create(id=2, name="test_attendance_type_2"),
        ]

        cls.events = [
            Event.objects.create(
                id=1,
                name="test_event_1",
                index="test event index 1",
                start_date_time="2022-08-04T04:16:00Z",
                end_date_time="2022-08-04T04:16:00Z",
            ),
            Event.objects.create(
                id=2,
                name="test_event_2",
                index="test event index 2",
                start_date_time="2022-08-04T04:16:00Z",
                end_date_time="2022-08-04T04:16:00Z",
            ),
        ]

        cls.timetables = [
            TimeTable.objects.create(
                name="test_timetable_1",
                index="test timetable index 1",
                event=cls.events[0],
                start_date_time="2022-08-04T04:16:00Z",
                end_date_time="2022-08-04T04:16:00Z",
            ),
            TimeTable.objects.create(
                name="test_timetable_2",
                index="test timetable index 2",
                event=cls.events[1],
                start_date_time="2022-08-04T04:16:00Z",
                end_date_time="2022-08-04T04:16:00Z",
            ),
        ]

    def setUp(self):
        self.client = APIClient()
        self.test_member_uid = "test_member_uid_123456789012"
        self.test_role_id = 4

        # Create a test attendance
        self.attendance_data = {
            "member_id": self.test_member_uid,
            "attendance_type_id": 1,
            "time_table_id": 1,
            "index": "this is test attendance",
        }
        self.attendance_id = TestUtils.create_test_data(
            self.client, reverse("attendance_list_create"), self.attendance_data
        )

        self.attendance_data_not_admin = {
            "member_id": "test_not_admin_member_123456",
            "attendance_type_id": 1,
            "time_table_id": 1,
            "index": "test attendance 1",
        }
        self.attendance_data_not_admin_2 = {
            "member_id": "test_not_admin_member_123456",
            "attendance_type_id": 1,
            "time_table_id": 2,
            "index": "test attendance 2",
        }

        self.another_attendance_id = TestUtils.create_test_data(
            self.client,
            reverse("attendance_list_create"),
            self.attendance_data_not_admin,
        )
        self.another_attendance_id_2 = TestUtils.create_test_data(
            self.client,
            reverse("attendance_list_create"),
            self.attendance_data_not_admin_2,
        )

    def test_add_attendance(self):
        attendance_url = reverse("attendance_list_create")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        attendance_data = {
            "member_id": self.test_member_uid,
            "attendance_type_id": 1,
            "time_table_id": 1,
            "index": "this is test attendance",
        }

        # when
        response = self.client.post(
            attendance_url,
            data=json.dumps(attendance_data),
            content_type="application/json",
        )

        # then
        expected_data = {
            "index": self.attendance_data["index"],
            "attendance_type_id": self.attendance_data["attendance_type_id"],
            "member_id": self.attendance_data["member_id"],
            "time_table_id": self.attendance_data["time_table_id"],
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_attendance_admin_self(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.attendance_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        expected_data = {
            "index": "this is test attendance",
            "attendance_type_id": 1,
            "member_id": self.test_member_uid,
            "time_table_id": 1,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_attendance_admin_not_self(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.another_attendance_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        expected_data = {
            "index": "test attendance 1",
            "attendance_type_id": 1,
            "member_id": "test_not_admin_member_123456",
            "time_table_id": 1,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_attendance_not_admin_not_self(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.attendance_id}
        )

        # given
        self.client = TestUtils.add_header(self.client, self.test_member_uid, 3)

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        expected_data = {
            "index": "this is test attendance",
            "attendance_type_id": 1,
            "member_id": self.test_member_uid,
            "time_table_id": 1,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_attendance_not_admin_self(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.another_attendance_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, "test_not_admin_member_123456", 3
        )

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, self.attendance_data_not_admin)

    def test_get_attendances_self(self):
        attendance_url = reverse("attendance_list_create")
        attendance_url += f"?memberID={self.test_member_uid}"

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 1)

    def test_get_all_filtered_attendances(self):
        attendance_url = reverse("attendance_list_create")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            attendance_url,
            {"memberID": self.test_member_uid},
            content_type="application/json",
        )

        response_2 = self.client.get(
            attendance_url,
            {"timeTableID": 1},
            content_type="application/json",
        )

        # then
        response_data = response.json()
        response_data_2 = response_2.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 1)
        self.assertEqual(
            response.data.get("results")[0].get("member_id"), self.test_member_uid
        )

        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data_2)
        self.assertEqual(len(response_data_2.get("results")), 2)
        self.assertEqual(response_2.data.get("results")[0].get("time_table_id"), 1)

    def test_get_all_paginated_attendances(self):
        attendance_url = reverse("attendance_list_create")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        for i in range(10):
            attendance_data = {
                "member_id": self.test_member_uid,
                "attendance_type_id": 1,
                "time_table_id": 1,
                "index": f"this is test attendance {i}",
            }
            TestUtils.create_test_data(
                self.client, reverse("attendance_list_create"), attendance_data
            )

        # when
        response = self.client.get(
            attendance_url,
            {"page": 1, "page_size": 1},
            content_type="application/json",
        )

        response_2 = self.client.get(
            attendance_url,
            {"page": 1, "page_size": 10},
            content_type="application/json",
        )

        # then
        response_data = response.json()
        response_data_2 = response_2.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 1)

        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data_2)
        self.assertEqual(len(response_data_2.get("results")), 10)
        self.assertEqual(response_data_2.get("previous"), None)
        self.assertEqual(
            response_data_2.get("next"),
            "http://testserver/attendance/api/v1/attendance/?page=2&page_size=10",
        )

    def test_get_attendances_not_self(self):
        attendance_url = reverse("attendance_list_create")
        attendance_url += "?memberID=test_not_admin_member_123456"

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json())

    def test_get_attendances_auth_error(self):
        attendance_url = reverse("attendance_list_create")
        attendance_url += "?memberID=test_not_admin_member_123456"

        # given
        self.client = TestUtils.add_header(self.client, self.test_member_uid, 3)

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_data.get("message"), "해당 정보를 열람할 권한이 없습니다.")

    def test_get_attendances_not_admin(self):
        attendance_url = reverse("attendance_list_create")
        attendance_url += "?memberID=test_probationary_member_123"

        # given
        self.client = TestUtils.add_header(
            self.client, "test_probationary_member_123", 2
        )

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json())

    def test_delete_attendance(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.attendance_id}
        )

        # given
        self.client = TestUtils.add_header(self.client, self.test_member_uid, 4)

        # when
        response = self.client.delete(
            attendance_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Attendance.objects.filter(id=self.attendance_id).exists())

    def test_delete_attenance_auth_error(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.attendance_id}
        )

        # given
        self.client = TestUtils.add_header(self.client, "not_admin_user", 2)

        # when
        response = self.client.delete(
            attendance_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_attendance(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.attendance_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        update_data = {"attendance_type_id": 2, "index": "변경된 내용"}

        # when
        response = self.client.put(
            attendance_url,
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["index"], "변경된 내용")
        self.assertEqual(response.data["attendance_type_id"], 2)

    def test_update_attendance_auth_error(self):
        attendance_url = reverse(
            "attendance_detail", kwargs={"attendanceId": self.attendance_id}
        )

        # given
        self.client = TestUtils.add_header(self.client, self.test_member_uid, 2)

        update_data = {"attendance_type_id": 2, "index": "변경된 내용"}

        # when
        response = self.client.put(
            attendance_url,
            data=update_data,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_attendance_types(self):
        # given
        attendance_url = reverse("get_attendance_type")

        self.client = TestUtils.add_header(
            self.client, "test_probationary_member_123", 2
        )

        # when
        response = self.client.get(
            attendance_url,
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 2)

    @classmethod
    def tearDownClass(cls):
        # 로그 레벨을 다시 원래대로 돌려놓음
        logging.disable(logging.CRITICAL)
        super().tearDownClass()
