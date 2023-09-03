from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
    NotAuthenticated,
)
import datetime


def _check_error_code(exc):
    match exc:
        # VALIDATION ERRORS
        case ValidationError():
            error_code = "AT-VALD-001"
        # SQL ERRORS
        case IntegrityError():
            error_code = "AT-SQL-001"
        case ObjectDoesNotExist():
            error_code = "AT-SQL-002"
        # VALUE ERRORS
        case ValueError():
            error_code = "AT-VAL-001"
        case TypeError():
            error_code = "AT-VAL-002"
        case KeyError():
            error_code = "AT-VAL-003"
        case IndexError():
            error_code = "AT-VAL-004"
        # AUTHENTICATION ERRORS
        case PermissionDenied():
            error_code = "AT-AUTH-001"
        case NotAuthenticated():
            error_code = "AT-AUTH-002"
        case AttributeError():
            error_code = "AT-AUTH-003"
        # DATABASE ERRORS
        case ConnectionError():
            error_code = "AT-DB-001"
        case TimeoutError():
            error_code = "AT-DB-002"
        case ConnectionRefusedError():
            error_code = "AT-DB-003"
        case ConnectionAbortedError():
            error_code = "AT-DB-004"
        case ConnectionResetError():
            error_code = "AT-DB-005"
        case BrokenPipeError():
            error_code = "AT-DB-006"
        case _:
            error_code = "AT-GEN-000"  # General error code as default

    return error_code


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_code = _check_error_code(exc=exc)

        custom_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "status": response.status_code,
            "error": response.reason_phrase,
            "code": error_code,
            "message": str(exc),
            "path": context["request"].path,
        }
        response.data = custom_data

    return response
