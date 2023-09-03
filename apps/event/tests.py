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
        cls.roles = [
            Role.objects.create(id=1, name='ROLE_GUEST'),
            Role.objects.create(id=2, name='ROLE_USER0'),
            Role.objects.create(id=3, name='ROLE_USER1'),
            Role.objects.create(id=4, name='ROLE_ADMIN'),
            Role.objects.create(id=5, name='ROLE_DEV'),
        ]

        cls.members = [
            Member.objects.create(
                id="test_member_uid_123456789012",
                name="test_admin_name",
                email="test_admin_email",
                role=cls.roles[3],
                status=True,
            ),
            Member.objects.create(
                id="test_not_admin_member_123456",
                name="test_member_name_2",
                email="test_member_email_2",
                role=cls.roles[2],
                status=True,
            ),
            Member.objects.create(
                id="test_probationary_member_123",
                name="test_member_name_3",
                email="test_member_email_3",
                role=cls.roles[1],
                status=True,
            ),
        ]

        cls.attendance_type = [
            AttendanceType.objects.create(id=1, name="test_attendance_type_1"),
            AttendanceType.objects.create(id=2, name="test_attendance_type_2"),
        ]

    def setUp(self):
        self.client = APIClient()
        self.test_member_uid = "test_member_uid_123456789012"
        self.test_role_id = 4

        # Create a test event
        self.event_data = {
            "name": "test event",
            "index": "this is test event index",
            "start_date_time": "2022-08-04T04:16:00Z",
            "end_date_time": "2022-08-04T04:16:00Z",
        }
        self.event_id = TestUtils.create_test_data(
            self.client, reverse("add_event"), self.event_data
        )

        self.another_event_data = {
            "name": "test event 2",
            "index": "this is another test event index",
            "start_date_time": "2022-08-04T04:16:00Z",
            "end_date_time": "2022-08-04T04:16:00Z",
        }
        TestUtils.create_test_data(
            self.client, reverse("add_event"), self.another_event_data
        )

    def test_add_event(self):
        event_url = reverse("add_event")

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
        )

        event_data = {
            "name": "Test Event",
            "index": "Test Index",
            "start_date_time": "2022-08-04T04:16:00Z",
            "end_date_time": "2022-08-04T04:16:00Z",
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
        event_url = reverse("event_detail", kwargs={"eventId": self.event_id})

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
        self.assertEqual(len(response_data), 2)

    def test_get_all_event_with_query_params(self):
        # TODO: Make test case for query params
        pass

    def test_delete_event(self):
        event_url = reverse("event_detail", kwargs={"eventId": self.event_id})

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
        event_url = reverse("event_detail", kwargs={"eventId": self.event_id})

        # given
        self.client = TestUtils.add_header(
            self.client, self.test_member_uid, self.test_role_id
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
