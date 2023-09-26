# JGW-Penalty-Python
@author 이준혁(39기) bbbong9@gmail.com

자람 그룹웨어의 출결 관리 시스템입니다.

해당 프로젝트는 Django로 작성되었으며, 추후 FastAPI로 변경될 예정입니다(날짜 미정, version 1 배포 이후 예정).

## 현재 스택 (Version 1, v1)

 - Framework : Django + Django REST Framework
 - Database : MariaDB

## 추후 변경할 스택 (Version 2, v2)

 - Framework : FastAPI + sqlalchemy(asyncIO)
 - Database : MariaDB

# About Service (현재 버전 기준)

## 1. Stack
* Framework: Django, Python
* DB: MariaDB
* Container: Docker
* CI/CD: Github Actions & Jenkins

## 2. Directory Tree
```
├── .github (sources of github templates)
├── apps (Django Applications' sources)
│   ├── attendance
│   ├── common (Django manage.py 명령어 및 기본/공통 모델 정의)
│   ├── event
│   ├── timetable
│   └── utils
├── docs (static API Documents)
├── jgw_attendance
│   └── settings
│       ├── base (base settings)
│       ├── settings_dev.py (settings for development environment)
│       └── settings_prod.py (settings for production environment)
├── logs (logs of Django, auto-generated)
│   └── logfiles ...
├── scripts (scripts for building containers, run tests, etc ...)
│   ├── running_devserver.sh (run development server)
│   └── running_test.sh (running all tests)
├── venv (libraries for python & Django, auto-generated)
├── .env (Contains Secrets)
├── .gitignore
├── .pylintrc (pylint configuration)
├── Dockerfile (scripts for building container)
├── manage.py
├── README.md
├── requirements.txt (dependency files)
└── setup.cfg (project configuration)
```

## 3. API Docs
API endpoint에 대한 설명이 기재되어 있습니다.
Online(개발 서버 실행 환경) 또는 Offline(정적 YAML 파일)으로 확인 가능합니다.

1. Online   
  다음 명령어로 8000포트에 개발 서버를 실행한 후 하단 링크를 통해 문서를 확인합니다: `bash scripts/running_devserver.sh`
 - [Swagger Docs](http://127.0.0.1:8000/attendance/api/v1/swagger/)
 - [Redoc Docs](http://127.0.0.1:8000/attendance/api/v1/redoc/)
 - [JSON Docs](http://127.0.0.1:8000/attendance/api/v1/swagger.json)
 - [Download Docs at your local](http://127.0.0.1:8000/attendance/api/v1/swagger.yaml)

2. Offline   
  오프라인 환경에서 API 문서를 확인하려면 `docs/apidocs.yaml` 파일을 참고하시면 됩니다.

## 4. DB Schemas
추가예정

## 5. 개발 환경 구성

### 필수 환경
 - Python 3.10.10 버전 이상 혹은 해당 버전의 Python
 - Git
 - Docker
 - MySQL or MariaDB

### 환경 구성
1. 현재 github repository를 작업할 Local 디렉토리에 clone: `git clone https://github.com/msng-devs/JGW-Attendance-Python.git`
2. 디렉토리에 python 가상 환경을 구성: `python -m venv venv`
3. python 가상 환경으로 접속: 
   - Mac / Linux: `source venv/bin/activate`
   - Window: `.venv/Scripts/activate`
4. 의존성 설치: `pip install -r requirements.txt`
5. IDE가 venv 속 python과 linter로 pylint를 사용하도록 변경: `depends on your IDE environment.`
6. .env 파일 저장
7. logs 폴더 생성: `mkdir logs`
