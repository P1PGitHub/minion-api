from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
import uuid


class AccountManager(BaseUserManager):

    def create_user(self, email, first_name=None, last_name=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    team = models.ForeignKey(
        "teams.Team",
        models.SET_NULL,
        related_name="teams",
        related_query_name="team",
        blank=True,
        null=True
    )
    report_admin = models.BooleanField(
        default=False, verbose_name="Report Admin"
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    cw_public = models.CharField(
        max_length=255, verbose_name="CW public key", blank=True, null=True)
    cw_private = models.CharField(
        max_length=255, verbose_name="CW private key", blank=True, null=True)

    first_name = models.CharField(
        verbose_name="first name",
        max_length=255
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=255
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    objects = AccountManager()

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f"{self.last_name}, {self.first_name}"
        else:
            return self.email

    def get_short_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name[0]}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
