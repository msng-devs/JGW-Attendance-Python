import json


class TestUtils:
    @staticmethod
    def add_header(client, uid, role_id):
        client.credentials(HTTP_USER_PK=uid, HTTP_ROLE_PK=role_id)
        return client

    @staticmethod
    def create_test_data(client, url, data):
        client = TestUtils.add_header(client, "test_member_uid_123456789012", 4)

        response = client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        return (
            response.json()["id"]
            if "id" in response.json()
            else list(response.json().values())[0]
        )

    @staticmethod
    def verify_response_data(response, expected_data):
        for key, value in expected_data.items():
            assert response.data[key] == value
