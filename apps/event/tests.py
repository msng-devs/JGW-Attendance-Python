# --------------------------------------------------------------------------
# Event Application의 테스트케이스를 정의한 모듈입니다.
#
# :class EventApiTest: Event Application의 Endpoint를 테스트합니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

import json

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Event
from apps.common.models import Role, Member
from apps.utils.test_utils import TestUtils
from apps.attendance.models import AttendanceType


class EventApiTest(TestCase):
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

    def setUp(self):
        self.client = APIClient()
        self.test_member_uid = "test_member_uid_123456789012"
        self.test_role_id = 4

        # Create a test event
        self.event_data = {
            "name": "test event",
            "index": "this is test event index",
            "start_date_time": "2022-08-04 04:16:00",
            "end_date_time": "2022-08-04 04:16:00",
        }
        self.event_id = TestUtils.create_test_data(
            self.client, reverse("event_list"), self.event_data
        )

        self.another_event_data = {
            "name": "test event 2",
            "index": "this is another test event index",
            "start_date_time": "2022-08-04 04:16:00",
            "end_date_time": "2022-08-04 04:16:00",
        }
        TestUtils.create_test_data(
            self.client, reverse("event_list"), self.another_event_data
        )

    def test_add_event(self):
        event_url = reverse("event_list")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        event_data = {
            "name": "Test Event",
            "index": "Test Index",
            "start_date_time": "2022-08-04 04:16:00",
            "end_date_time": "2022-08-04 04:16:00",
        }

        # when
        response = self.client.post(
            event_url,
            data=json.dumps(event_data),
            content_type="application/json",
        )

        # then
        expected_data = {
            "name": "Test Event",
            "index": "Test Index",
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_event_by_id(self):
        event_url = reverse("event_detail", kwargs={"event_id": self.event_id})

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            event_url,
            content_type="application/json",
        )

        # then
        expected_data = {
            "name": "test event",
            "index": "this is test event index",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, expected_data)

    def test_get_all_event(self):
        event_url = reverse("event_list")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            event_url,
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 2)

    def test_get_all_filtered_event(self):
        event_url = reverse("event_list")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.get(
            event_url,
            {"index": "this is test"},
            content_type="application/json",
        )

        response_2 = self.client.get(
            event_url,
            {"name": "test event 2"},
            content_type="application/json",
        )

        # then
        response_data = response.json()
        response_data_2 = response_2.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 1)
        self.assertEqual(response_data.get("results")[0].get("name"), "test event")
        self.assertEqual(
            response_data.get("results")[0].get("index"), "this is test event index"
        )

        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data_2)
        self.assertEqual(len(response_data_2.get("results")), 1)
        self.assertEqual(response_data_2.get("results")[0].get("name"), "test event 2")
        self.assertEqual(
            response_data_2.get("results")[0].get("index"),
            "this is another test event index",
        )

    def test_get_all_paginated_event(self):
        event_url = reverse("event_list")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        for i in range(10):
            event_data = {
                "name": f"test event {i}",
                "index": f"this is test event index {i}",
                "start_date_time": "2022-08-04 04:16:00",
                "end_date_time": "2022-08-04 04:16:00",
            }
            TestUtils.create_test_data(self.client, reverse("event_list"), event_data)

        # when
        response = self.client.get(
            event_url,
            {"page": 1, "page_size": 5},
            content_type="application/json",
        )

        # then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data)
        self.assertEqual(len(response_data.get("results")), 5)
        self.assertEqual(response_data.get("previous"), None)
        self.assertEqual(
            response_data.get("next"),
            "http://testserver/attendance/api/v1/event/?page=2&page_size=5",
        )

    def test_delete_event(self):
        event_url = reverse("event_detail", kwargs={"event_id": self.event_id})

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        # when
        response = self.client.delete(
            event_url,
            content_type="application/json",
        )

        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # DB에서 해당 이벤트가 삭제되었는지 확인
        self.assertFalse(Event.objects.filter(id=self.event_id).exists())

    def test_update_event(self):
        event_url = reverse("event_detail", kwargs={"event_id": self.event_id})

        # given
        self.client = TestUtils.add_header(
            self.client, "test_member_uid_987654321098", 4
        )

        update_data = {"index": "this is updated test event index"}

        # when
        response = self.client.put(
            event_url,
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # then
        expected_data = {
            "name": "test event",
            "index": "this is updated test event index",
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        TestUtils.verify_response_data(response, expected_data)

    @classmethod
    def tearDownClass(cls):
        # 로그 레벨을 다시 원래대로 돌려놓음
        logging.disable(logging.CRITICAL)
        super().tearDownClass()
