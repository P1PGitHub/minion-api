import random

from django.db import models
from django.utils.text import slugify
import pytz
import uuid

TIMEZONE_CHOICES = zip(pytz.all_timezones, pytz.all_timezones)


class Team(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    logo_ref = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Logo Ref"
    )
    address1 = models.CharField(
        verbose_name="street address 1", max_length=255)
    address2 = models.CharField(
        verbose_name="street address 2", max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    email = models.EmailField(max_length=255)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)

    cw_company = models.CharField(
        max_length=255, unique=True, blank=True, null=True, verbose_name="CW company")

    timezone = models.CharField(
        max_length=255, default='UTC', choices=TIMEZONE_CHOICES
    )

    stale_report_age = models.PositiveSmallIntegerField(
        default=7
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.name:
                slug_candidate = slugify(self.name)
                valid_slug = False
                for _ in range(0, 10):
                    if not Team.objects.filter(slug=slug_candidate).exists():
                        valid_slug = True
                        break
                    else:
                        rand_hex = str(hex(random.randint(0, 65535)))[2:]
                        slug_candidate = slugify(
                            self.name, allow_unicode=True
                        ) + f"-{rand_hex}"
                if not valid_slug:
                    raise ValidationError(
                        "Cannot create a valid slug for this team."
                    )
                self.slug = slug_candidate
                super(Team, self).save(*args, **kwargs)
            else:
                raise ValidationError("A company name is required.")
        else:
            super(Team, self).save(*args, **kwargs)

    def get_full_address(self):
        if self.address2:
            return f"{self.address1} {self.address2}, {self.city}, {self.state} {self.zip_code}"

    def __str__(self):
        return self.name
