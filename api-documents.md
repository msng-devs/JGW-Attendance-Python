---
description: JGW-Attendance-Python API는 자람 그룹웨어의 출결 관리 시스템 API입니다.
---

# API Documents

Gitbook의 API method document에 example value가 제대로 표시되지 않는 경우, 다음 YAML 파일을 OpenAPI(Swagger) 뷰어로 확인하시길 바랍니다.

(링크 삽입 필요)



## 소개

해당 API를 사용하여 학회의 행사와 타임테이블을 관리하거나, 출결을 관리할 수 있습니다.

해당 API를 사용하기 위해서 아래 요소들을 알고 있어야 합니다.



### Event(행사)

Event는 학회에서 진행하는 행사를 의미합니다. 예) 1학기 세미나, 동계 워크샵 등

출결 및 타임테이블을 생성하기 위해서는 이 행사를 우선적으로 생성해야 합니다.



### TimeTable(시간표)

TimeTable은 행사에 속하는 시간표를 의미합니다. 실제 자람의 세미나 출결관리를 예로 들어 살펴보겠습니다.

'1학기 세미나' 라는 Event(행사)가 있습니다. 자람 회원이라면 아시겠지만, 세미나라는 행사는 하루만 진행하는 행사가 아닙니다. 주마다 한번씩 진행하죠.

따라서 1주차,2주차,3주차 …​ 이런식으로 시간표를 생성하고 각각의 주마다 출결 확인을 합니다.

즉 이러한 time table 별로 출결을 등록하는 방식으로 동작합니다. 따라서 time table을 생성할 때에는 함께 '미결' 출결 정보를 생성하는 것을 권장합니다.



### Attendance(출결)

Attendance는 출결을 의미합니다. 위에서 언급했듯이 timeTable별로 출결을 관리할 수 있습니다. 단, 한개의 timeTable에는 회원당 1개의 출결 정보만 기록할 수 있다는 것을 명심하세요.



### AttendanceType(출결 타입)

AttendanceType은 출결 타입을 의미합니다. 미결,출결,결석,출석 인정으로 구성됩니다. 위에서 살펴본 Attendance의 출결 유형을 구분하기 위해 사용합니다.



### Attendance Code(출결 코드)

attendanceCode는 출결 코드를 의미합니다. 해당 코드를 사용하여 일반 사용자가 출결을 등록할 수 있습니다.

동작방식은 대학교의 출결 형태를 떠올리면 쉽습니다.

1. 위에서 살펴본 time table(시간표)에 관리자(임원진)이 출결 코드를 발급합니다.
2. 발급된 출결 코드를 사용하여 일반 사용자가 출결을 등록합니다.

단 출결 코드는 아래 제약 사항을 가집니다.

* 초 단위로 유효시간을 설정해야 하며 최대 2592000초(30일)까지 설정할 수 있습니다.(영구적인 코드 발급이 가능하지만, 권장하지 않습니다.)
* 한 Time Table(시간표)에는 한개의 출결코드를 가질 수 있습니다.

{% swagger src=".gitbook/assets/apidocs.yaml" path="/attendance/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/attendance/" method="post" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/attendance/attendanceType/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/attendance/{attendanceId}/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/attendance/{attendanceId}/" method="put" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/attendance/{attendanceId}/" method="delete" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/event/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/event/" method="post" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/event/{eventId}/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/event/{eventId}/" method="put" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/event/{eventId}/" method="delete" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/" method="post" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/{timetableId}/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/{timetableId}/" method="put" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/{timetableId}/" method="delete" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/{timetableId}/attendanceCode/" method="get" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/{timetableId}/attendanceCode/" method="post" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/{timetableId}/attendanceCode/" method="delete" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}

{% swagger src=".gitbook/assets/apidocs.yaml" path="/timetable/{timetableId}/attendanceCode/register/" method="post" %}
[apidocs.yaml](.gitbook/assets/apidocs.yaml)
{% endswagger %}
