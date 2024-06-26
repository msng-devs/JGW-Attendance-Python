# flake8: noqa: E501
# --------------------------------------------------------------------------
# Swagger Docs Generator가 읽을 수 있는 형태로 문서를 정의하는 모듈입니다.
#
# @author 이준혁(39기) bbbong9@gmail.com
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Documentation Methods
# --------------------------------------------------------------------------
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {"name": "attendance", "description": "출결 정보를 조회 및 관리할 수 있는 api 입니다."},
            {"name": "event", "description": "event 를 추가하고, 삭제하고, 수정하는 API를 제공합니다."},
            {
                "name": "timetable",
                "description": "TimeTable 및 AttendanceCode을 추가하고, 삭제하고, 수정하는 API를 제공합니다.",
            },
        ]

        return swagger


def description_query_param():
    description = """\n
## Query parameters (공통 설명)
**주의!** 모든 option들은 단 한개의 인자만 수용가능합니다!

 * (O) "?memberID=456465456&timeTableID=1"

 * (X) "?memberID=456465456,456456456465&timeTableID=1,123123"

또한 모든 Option들은 And로 동작합니다.

예를 들어 Attendance API에서, "?memberID=456465456&timeTableID=1"라는 인자가 있다면,\
memberID가 "456465456"이고, timeTableID가 1인 Attendance를 찾습니다.
"""
    return description


# 표: param name, type, description
def description_equal_query(item_name="item", params=None):
    base_description = f"""\n
## Equal Query Options
조건과 일치한 모든 {item_name}를 확인할 수 있습니다.

해당 옵션들은 입력된 값과 완전히 일치 되는 경우를 탐색합니다.

"createdBy = 'system'" 옵션을 제공하면, createdBy가 "system"인 {item_name}들을 조회합니다.\n
"""

    # 표 생성
    table_header = "|param name|type|description|\n|---|---|---|\n"
    table_rows = ""

    if params:
        for param, details in params.items():
            table_rows += f"|{param}|{details['type']}|{details['description']}|\n"

    return base_description + table_header + table_rows


# 표: param name, type, start range param, end range param, description
def description_range_query(item_name="item", params=None):
    base_description = f"""\n
## Range Query Options
해당 옵션들을 사용하여 {item_name}요소를 범위 설정하여 검색할 수 있습니다.

예를들어, "createdDateTime" 옵션을 검색하고 싶다면, "startCreatedDateTime"으로 시작 범위를 설정하고\
"endCreatedDateTime"으로 종료 범위를 설정하여 검색할 수 있습니다.

* 시작 범위와 종료 범위가 모두 입력되었다면, 해당 범위를 탐색합니다.

* 시작 범위만 입력됬을 경우, 해당 시작범위에서 최대 범위(9999-12-31 59:59:59)에 해당하는 범위를 탐색합니다.

* 종료 범위만 입력됬을 경우, 최소 범위("1000-01-01 00:00:00")에서 종료 범위까지에 해당하는 범위를 탐색합니다.\n
"""

    # 표 생성
    table_header = "|param name|type|start range param|end range param|description|\n|---|---|---|---|---|\n"
    table_rows = ""

    if params:
        for param, details in params.items():
            table_rows += f"|{param}|{details['type']}|{details['start_range_param']}|{details['end_range_param']}|{details['description']}|\n"

    return base_description + table_header + table_rows


# 표: param name, type, description
def description_like_query(item_name="item", params=None):
    base_description = f"""\n
## Like Query Options
조건과 유사한 모든 {item_name}를 확인할 수 있습니다.

해당 옵션들을 사용하면, 해당 문자열을 포함하는 {item_name}를 조회합니다.

예를 들어 "이것은 세미나입니다"라는 index가 있다고 가정합시다.

"index" 인자로 "세미나" 이라는 값을 주었다면, index에 "출결"이라는 글자가 들어가는 {item_name}들을 찾습니다.\n
"""

    # 표 생성
    table_header = "|param name|type|description|\n|---|---|---|\n"
    table_rows = ""

    if params:
        for param, details in params.items():
            table_rows += f"|{param}|{details['type']}|{details['description']}|\n"

    return base_description + table_header + table_rows


# 표: param name, type, description
def description_pagination(item_name="item", params=None):
    base_description = f"""\n
## Pagination Options
{item_name} 페이지에 대한 데이터 랜더링 값을 설정할 수 있습니다.

해당 인자를 통해 pagination처리를 할 수 있습니다. Sort Option은 아래 파트를 참고하세요.

**주의!** pagination을 설정하지 않더라도, 모든 request는 1000의 Size로 자동으로 pagination처리가 됩니다! \
만약 1000건 보다 많은 양의 데이터가 필요하다면, size를 지정해주어야합니다.\n
"""

    # 표 생성
    table_header = "|param name|description|size|\n|---|---|---|\n"
    table_rows = ""

    if params:
        for param, details in params.items():
            table_rows += f"|{param}|{details['description']}|{details['size']}|\n"

    return base_description + table_header + table_rows


# 표: param name, type, description
def description_sort(item_name="item", params=None):
    base_description = f"""\n
## Sort Options
다음 옵션들을 사용하여 {item_name} 데이터를 정렬할 수 있습니다.

Sort Option은 "sort" 인자에 제공해야합니다. 위 옵션들과 다르게 Sort Option은 여러 인자들을 입력해도 됩니다.

sort 인자에 모든 Option들을 지정했다면, 마지막 인자로 Sort 방향을 지정해주여야 합니다. ASC(오름 차순), DESC(내립차순) 2가지 옵션이 있습니다. \
만약 옵션을 지정해주지 않았다면, DESC로 동작합니다.

사용예시 "sort=member,asc", "sort=member,timeTable,desc"

**주의!** Sort Option을 지정해주지 않더라도, 기본적으로 id에 대하여 DESC 방향으로 정렬을 진행합니다!\n
"""

    # 표 생성
    table_header = "|param name|description|\n|---|---|\n"
    table_rows = ""

    if params:
        for param, details in params.items():
            table_rows += f"|{param}|{details['description']}|\n"

    return base_description + table_header + table_rows


# --------------------------------------------------------------------------
# Application Documentation Specification
# --------------------------------------------------------------------------


# AttendanceType
def get_attendance_type_doc():
    base_description = """출결 종류를 조회

---
RBAC - 1(게스트) 이상

등록되어 있는 모든 AttendanceType를 확인할 수 있습니다.
"""

    return (
        base_description
        + "\n"
        + description_query_param()
        + "\n"
        + description_equal_query(
            item_name="AttendanceType",
            params={
                "createdBy": {
                    "type": "String",
                    "description": "해당 AttendanceType을 생성한 사람",
                },
                "modifiedBy": {
                    "type": "String",
                    "description": "해당 AttendanceType을 마지막으로 수정한 사람",
                },
            },
        )
        + "\n"
        + description_range_query(
            item_name="AttendanceType",
            params={
                "CreatedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startCreatedDateTime",
                    "end_range_param": "endCreatedDateTime",
                    "description": "해당 AttendanceType이 생성된 시간",
                },
                "ModifiedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startModifiedDateTime",
                    "end_range_param": "endModifiedDateTime",
                    "description": "해당 AttendanceType이 마지막으로 수정된 시간",
                },
                "DATETIME": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startDateTime",
                    "end_range_param": "endDateTime",
                    "description": "해당 AttendanceType의 진행 기간",
                },
            },
        )
        + "\n"
        + description_like_query(
            item_name="AttendanceType",
            params={
                "name": {
                    "type": "String",
                    "description": "해당 AttendanceType의 이름",
                },
                "index": {
                    "type": "String",
                    "description": "해당 AttendanceType에 대한 부연설명",
                },
            },
        )
        + "\n"
        + description_pagination(
            item_name="AttendanceType",
            params={
                "Page의 크기": {
                    "description": "page",
                    "size": "Page의 위치",
                },
            },
        )
        + "\n"
        + description_sort(
            item_name="AttendanceType",
            params={
                "id": {
                    "description": "AttendanceType의 ID에 대하여 정렬합니다.",
                },
                "name": {
                    "description": "AttendanceType의 이름에 대하여 정렬합니다.",
                },
                "index": {
                    "description": "index에 대하여 정렬합니다.",
                },
                "createdDateTime": {
                    "description": "생성된 시간순으로 정렬합니다.",
                },
                "modifiedDateTime": {
                    "description": "마지막으로 수정된 시간 순으로 정렬합니다.",
                },
                "startDateTime": {
                    "description": "시작 시간 순으로 정렬합니다.",
                },
                "endDateTime": {
                    "description": "종료 시간 순으로 정렬합니다.",
                },
                "createdBy": {
                    "description": "생성한자에 대하여 정렬합니다.",
                },
                "modifiedBy": {
                    "description": "마지막으로 수정한자에 대하여 정렬합니다.",
                },
            },
        )
    )


# Attendance
def get_attendance_doc():
    base_description = """다수 Attendance를 조회

---
RBAC - 2(수습 회원) 이상

자신의 정보를 조회할 때는 role이 2(수습 회원)이어도 괜찮습니다.

다만, 다른 사람의 정보를 조회할 때는 role이 4(임원진)이어야 합니다.
"""

    return (
        base_description
        + "\n"
        + description_query_param()
        + "\n"
        + description_equal_query(
            item_name="Attendance",
            params={
                "attendanceTypeID": {
                    "type": "Number",
                    "description": "해당 Attendance의 AttendanceType ID",
                },
                "memberID": {
                    "type": "String",
                    "description": "해당 Attendance의 Member ID",
                },
                "timeTableID": {
                    "type": "Number",
                    "description": "해당 Attendance의 TimeTable ID",
                },
                "createdBy": {
                    "type": "String",
                    "description": "해당 Attendance를 생성한 사람",
                },
                "modifiedBy": {
                    "type": "String",
                    "description": "해당 Attendance를 마지막으로 수정한 사람",
                },
            },
        )
        + "\n"
        + description_range_query(
            item_name="Attendance",
            params={
                "CreatedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startCreatedDateTime",
                    "end_range_param": "endCreatedDateTime",
                    "description": "해당 Attendance가 생성된 시간",
                },
                "ModifiedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startModifiedDateTime",
                    "end_range_param": "endModifiedDateTime",
                    "description": "해당 Attendance가 마지막으로 수정된 시간",
                },
            },
        )
        + "\n"
        + description_like_query(
            item_name="Attendance",
            params={
                "index": {
                    "type": "String",
                    "description": "해당 Attendance의 부연설명",
                },
            },
        )
        + "\n"
        + description_pagination(
            item_name="Attendance",
            params={
                "Page의 크기": {
                    "description": "page",
                    "size": "Page의 위치",
                },
            },
        )
        + "\n"
        + description_sort(
            item_name="Attendance",
            params={
                "id": {
                    "description": "Attendance의 ID에 대하여 정렬합니다.",
                },
                "attendanceType": {
                    "description": "attendanceType의 ID에 대하여 정렬합니다.",
                },
                "member": {
                    "description": "member의 ID에 대하여 정렬합니다.",
                },
                "timeTable": {
                    "description": "timeTable의 ID에 대하여 정렬합니다.",
                },
                "index": {
                    "description": "index에 대하여 정렬합니다.",
                },
                "createdDateTime": {
                    "description": "생성된 시간순으로 정렬합니다.",
                },
                "modifiedDateTime": {
                    "description": "마지막으로 수정된 시간 순으로 정렬합니다.",
                },
                "createdBy": {
                    "description": "생성한자에 대하여 정렬합니다.",
                },
                "modifiedBy": {
                    "description": "마지막으로 수정한자에 대하여 정렬합니다.",
                },
            },
        )
    )


# Event
def get_event_doc():
    base_description = """다수 Event를 조회

---
RBAC - 1(게스트) 이상
"""

    return (
        base_description
        + "\n"
        + description_query_param()
        + "\n"
        + description_equal_query(
            item_name="Event",
            params={
                "createdBy": {
                    "type": "String",
                    "description": "해당 event를 생성한 사람",
                },
                "modifiedBy": {
                    "type": "String",
                    "description": "해당 event를 마지막으로 수정한 사람",
                },
            },
        )
        + "\n"
        + description_range_query(
            item_name="Event",
            params={
                "CreatedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startCreatedDateTime",
                    "end_range_param": "endCreatedDateTime",
                    "description": "해당 event가 생성된 시간",
                },
                "ModifiedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startModifiedDateTime",
                    "end_range_param": "endModifiedDateTime",
                    "description": "해당 event가 마지막으로 수정된 시간",
                },
                "DATETIME": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startDateTime",
                    "end_range_param": "endDateTime",
                    "description": "해당 event의 진행 기간",
                },
            },
        )
        + "\n"
        + description_like_query(
            item_name="Event",
            params={
                "name": {
                    "type": "String",
                    "description": "해당 event의 이름입니다.",
                },
                "index": {
                    "type": "String",
                    "description": "해당 event에 대한 부연설명",
                },
            },
        )
        + "\n"
        + description_pagination(
            item_name="Event",
            params={
                "Page의 크기": {
                    "description": "page",
                    "size": "Page의 위치",
                },
            },
        )
        + "\n"
        + description_sort(
            item_name="Event",
            params={
                "id": {
                    "description": "event의 ID에 대하여 정렬합니다.",
                },
                "name": {
                    "description": "event의 이름에 대하여 정렬합니다.",
                },
                "index": {
                    "description": "index에 대하여 정렬합니다.",
                },
                "createdDateTime": {
                    "description": "생성된 시간순으로 정렬합니다.",
                },
                "modifiedDateTime": {
                    "description": "마지막으로 수정된 시간 순으로 정렬합니다.",
                },
                "startDateTime": {
                    "description": "시작 시간 순으로 정렬합니다.",
                },
                "endDateTime": {
                    "description": "종료 시간 순으로 정렬합니다.",
                },
                "createdBy": {
                    "description": "생성한자에 대하여 정렬합니다.",
                },
                "modifiedBy": {
                    "description": "마지막으로 수정한자에 대하여 정렬합니다.",
                },
            },
        )
    )


# TimeTable
def get_timetable_doc():
    base_description = """다수 TimeTable을 조회

---
RBAC - 1(게스트) 이상

여러 time table들을 조회, 페이징, 정렬, 필터링을 통해 조회할 수 있습니다.
"""

    return (
        base_description
        + "\n"
        + description_query_param()
        + "\n"
        + description_equal_query(
            item_name="TimeTable",
            params={
                "eventID": {
                    "type": "Number",
                    "description": "해당 TimeTable이 속한 가지고 있는 Event의 ID",
                },
                "createdBy": {
                    "type": "String",
                    "description": "해당 TimeTable를 생성한 사람",
                },
                "modifiedBy": {
                    "type": "String",
                    "description": "해당 TimeTable를 마지막으로 수정한 사람",
                },
            },
        )
        + "\n"
        + description_range_query(
            item_name="TimeTable",
            params={
                "CreatedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startCreatedDateTime",
                    "end_range_param": "endCreatedDateTime",
                    "description": "해당 TimeTable가 생성된 시간",
                },
                "ModifiedDateTime": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startModifiedDateTime",
                    "end_range_param": "endModifiedDateTime",
                    "description": "해당 TimeTable가 마지막으로 수정된 시간",
                },
                "DATETIME": {
                    "type": "DateTime(yyyy-MM-dd HH:mm:ss)",
                    "start_range_param": "startDateTime",
                    "end_range_param": "endDateTime",
                    "description": "해당 TimeTable의 기간",
                },
            },
        )
        + "\n"
        + description_like_query(
            item_name="TimeTable",
            params={
                "name": {
                    "type": "String",
                    "description": "해당 TimeTable의 이름입니다.",
                },
            },
        )
        + "\n"
        + description_pagination(
            item_name="TimeTable",
            params={
                "Page의 크기": {
                    "description": "page",
                    "size": "Page의 위치",
                },
            },
        )
        + "\n"
        + description_sort(
            item_name="TimeTable",
            params={
                "id": {
                    "description": "TimeTable의 ID에 대하여 정렬합니다.",
                },
                "name": {
                    "description": "TimeTable의 이름에 대하여 정렬합니다.",
                },
                "event": {
                    "description": "TimeTable이 속한 Event",
                },
                "createdDateTime": {
                    "description": "생성된 시간순으로 정렬합니다.",
                },
                "modifiedDateTime": {
                    "description": "마지막으로 수정된 시간 순으로 정렬합니다.",
                },
                "startDateTime": {
                    "description": "시작 시간 순으로 정렬합니다.",
                },
                "endDateTime": {
                    "description": "종료 시간 순으로 정렬합니다.",
                },
                "createdBy": {
                    "description": "생성한자에 대하여 정렬합니다.",
                },
                "modifiedBy": {
                    "description": "마지막으로 수정한자에 대하여 정렬합니다.",
                },
            },
        )
    )
