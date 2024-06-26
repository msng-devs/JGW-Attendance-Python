# --------------------------------------------------------------------------
# TimeTable Application의 테스트케이스를 정의한 모듈입니다.
#
# :class TimeTableApiTest: TimeTable Application의 Endpoint를 테스트합니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging
import json

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import TimeTable
from apps.common.models import Role, Member
from apps.utils.test_utils import TestUtils
from apps.event.models import Event
from apps.attendance.models import AttendanceType, AttendanceCode


class TimeTableApiTest(TestCase):
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
            AttendanceType.objects.create(id=1, name="UNA"),
            AttendanceType.objects.create(id=2, name="APR"),
            AttendanceType.objects.create(id=3, name="ABS"),
            AttendanceType.objects.create(id=4, name="ACK"),
        ]

        cls.events = [
            Event.objects.create(
                id=1,
                name="test_event_name_1",
                start_date_time="2022-08-04 04:16:00",
                end_date_time="2022-08-04 04:16:00",
                index="test_event_index_1",
            ),
            Event.objects.create(
                id=2,
                name="test_event_name_2",
                start_date_time="2022-08-04 04:16:00",
                end_date_time="2022-08-04 04:16:00",
                index="test_event_index_2",
            ),
        ]

    def setUp(self):
        self.client = APIClient()
        self.test_member_uid = "test_member_uid_123456789012"
        self.test_role_id = 4

        # Create a test timetable
        self.timetable_data = {
            "name": "Test Timetable",
            "start_date_time": "2022-08-04 04:16:00",
            "end_date_time": "2022-08-04 04:16:00",
            "event_id": 1,
            "index": "Test Index",
        }
        self.timetable_id = TestUtils.create_test_data(
            self.client, reverse("timetable_list_create"), self.timetable_data
        )

        self.another_timetable_data = {
            "name": "Test Timetable 2",
            "start_date_time": "2022-08-04 04:16:00",
            "end_date_time": "2022-08-04 04:16:00",
            "event_id": 2,
            "index": "Test Index 2",
        }
        self.another_timetable_id = TestUtils.create_test_data(
            self.client, reverse("timetable_list_create"), self.another_timetable_data
        )

        self.attendance_code = TestUtils.create_test_data(
            self.client,
            reverse(
                "attendance_code_detail", kwargs={"timetable_id": self.timetable_id}
            ),
            {"exp_sec": 30},
        )

    def test_add_timetable(self):
        timetable_url = reverse("timetable_list_create")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        timetable_data = {
            "name": "Test Timetable",
            "start_date_time": "2022-08-04 04:16:00",
            "end_date_time": "2022-08-04 04:16:00",
            "event_id": 1,
            "index": "Test Index",
        }

        # when
        response = self.client.post(
            timetable_url,
            data=json.dumps(timetable_data),
            content_type="application/json",
        )

        # then
        expected_data = {
            "name": "Test Timetable",
            "start_date_time": "2022-08-04T04:16:00",
            "end_date_time": "2022-08-04T04:16:00",
            "event_id": 1,
            "index": "Test Index",
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_timetable_by_id(self):
        timetable_url = reverse(
            "timetable_detail", kwargs={"timetable_id": self.timetable_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            timetable_url,
            content_type="application/json",
        )

        # then
        expected_data = {
            "name": "Test Timetable",
            "start_date_time": "2022-08-04T04:16:00",
            "end_date_time": "2022-08-04T04:16:00",
            "event_id": 1,
            "index": "Test Index",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_all_timetable(self):
        timetable_url = reverse("timetable_list_create")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            timetable_url,
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 2)

    def test_get_all_filtered_timetable(self):
        timetable_url = reverse("timetable_list_create")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            timetable_url,
            {"eventID": 1},
            content_type="application/json",
        )

        response_2 = self.client.get(
            timetable_url,
            {"eventID": 1, "timeTableID": 1},
            content_type="application/json",
        )

        # then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data.get("results")), 1)

        response_data_2 = response_2.json()
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_2.get("results")), 1)

    def test_get_all_paginated_timetable(self):
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=1)

        for i in range(10):
            TimeTable.objects.create(
                name=f"Test {i}",
                start_date_time=start_time,
                end_date_time=end_time,
                event_id=1,
                index="Test Index",
                created_by=self.members[0].id,
                modified_by=self.members[0].id,
            )

        for i in range(11, 20):
            TimeTable.objects.create(
                name=f"Test {i}",
                start_date_time=start_time,
                end_date_time=end_time,
                event_id=2,
                index="Test Index",
                created_by=self.members[1].id,
                modified_by=self.members[1].id,
            )

        timetable_url = reverse("timetable_list_create")

        # given
        self.client = TestUtils.add_header(
            self.client, "test_member_uid_987654321098", 4
        )

        # when
        response = self.client.get(
            timetable_url,
            content_type="application/json",
        )

        params = {"page": 2, "page_size": 10}
        response_nextpage = self.client.get(
            timetable_url,
            params,
            content_type="application/json",
        )

        # then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data.get("results")), 10)
        self.assertEqual(response_data.get("previous"), None)
        self.assertEqual(
            response_data.get("next"),
            "http://testserver/attendance/api/v1/timetable/?page=2",
        )

        response_data_2 = response_nextpage.json()
        self.assertEqual(response_nextpage.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data_2.get("results")), 10)
        self.assertEqual(
            response_data_2.get("previous"),
            "http://testserver/attendance/api/v1/timetable/?page=1&page_size=10",
        )
        self.assertEqual(
            response_data_2.get("next"),
            "http://testserver/attendance/api/v1/timetable/?page=3&page_size=10",
        )

    def test_delete_timetable(self):
        timetable_url = reverse(
            "timetable_detail", kwargs={"timetable_id": self.timetable_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.delete(
            timetable_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TimeTable.objects.filter(id=self.timetable_id).exists())

    def test_update_timetable(self):
        timetable_url = reverse(
            "timetable_detail", kwargs={"timetable_id": self.timetable_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, "test_member_uid_987654321098", 4
        )

        update_data = {"index": "this is updated test timetable index"}

        # when
        response = self.client.put(
            timetable_url,
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # then
        expected_data = {
            "name": "Test Timetable",
            "start_date_time": "2022-08-04T04:16:00",
            "end_date_time": "2022-08-04T04:16:00",
            "event_id": 1,
            "index": "this is updated test timetable index",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, expected_data)

    def test_publish_timetable_attendancecode(self):
        timetable_url = reverse(
            "attendance_code_detail", kwargs={"timetable_id": self.another_timetable_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        request_data = {"exp_sec": 30}

        # when
        response = self.client.post(
            timetable_url,
            data=json.dumps(request_data),
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get("code"))

    def test_register_attendancecode(self):
        timetable_url = reverse(
            "attendance_code_register", kwargs={"timetable_id": self.timetable_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, "test_probationary_member_123", 2
        )

        code_data = AttendanceCode.objects.get(time_table_id=self.attendance_code)

        attendance_data = {"code": code_data.code}

        # when
        response = self.client.post(
            timetable_url,
            data=json.dumps(attendance_data),
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["index"], "출결 코드를 통해 처리된 출결 정보 입니다.")
        self.assertEqual(response_data["attendance_type_id"], 4)

    def test_get_timetable_attendancecode(self):
        timetable_url = reverse(
            "attendance_code_detail", kwargs={"timetable_id": self.timetable_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            timetable_url,
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data.get("code"))

    def test_delete_timetable_attendancecode(self):
        timetable_url = reverse(
            "attendance_code_detail", kwargs={"timetable_id": self.timetable_id}
        )

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.delete(
            timetable_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AttendanceCode.objects.filter(time_table_id=self.timetable_id).exists()
        )

    @classmethod
    def tearDownClass(cls):
        # 로그 레벨을 다시 원래대로 돌려놓음
        logging.disable(logging.CRITICAL)
        super().tearDownClass()
