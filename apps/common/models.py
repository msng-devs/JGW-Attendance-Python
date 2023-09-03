from django.db import models
from django.utils import timezone


class Role(models.Model):
    # 해당 권한의 ID(PK)
    id = models.AutoField(primary_key=True)

    # 해당 권한의 명칭("ROLE_" 시작하는 대문자)
    name = models.CharField(max_length=45, null=False, unique=True)


class Member(models.Model):
    # 해당 회원의 UID(Firebase uid) (PK)
    id = models.CharField(max_length=28, primary_key=True)

    # 회원의 실명
    name = models.CharField(max_length=45, null=False)

    # 회원의 이메일
    email = models.EmailField(max_length=255, null=False, unique=True)

    # 회원의 권한 레벨
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False)

    # 회원의 활동 상태
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)


class BaseEntity(models.Model):
    created_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date Time"
    )
    modified_datetime = models.DateTimeField(
        auto_now=True, verbose_name="Modified Date Time"
    )
    created_by = models.CharField(max_length=30, verbose_name="Created By")
    modified_by = models.CharField(max_length=30, verbose_name="Modified By")

    class Meta:
        abstract = True
