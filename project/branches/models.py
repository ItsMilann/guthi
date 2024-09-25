from django.db import models


class Branch(models.Model):
    district_en = models.CharField(max_length=255, blank=True, null=True)
    district_np = models.CharField(max_length=255, blank=True, null=True)
    name_np = models.CharField(blank=True, null=True, max_length=255)
    name_en = models.CharField(blank=True, null=True, max_length=255)
    fullname_np = models.CharField(blank=True, null=True, max_length=255)
    fullname_en = models.CharField(blank=True, null=True, max_length=255)
    address_np = models.CharField(blank=True, null=True, max_length=255)
    address_en = models.CharField(blank=True, null=True, max_length=255)
    province_np = models.CharField(blank=True, null=True, max_length=255)
    province_en = models.CharField(blank=True, null=True, max_length=255)
    slogan_np = models.CharField(blank=True, null=True, max_length=255)
    slogan_en = models.CharField(blank=True, null=True, max_length=255)
    phone_np = models.CharField(blank=True, null=True, max_length=255)
    phone_en = models.CharField(blank=True, null=True, max_length=255)
    email = models.CharField(blank=True, null=True, max_length=255)
    main_logo = models.CharField(max_length=2083, blank=True, null=True)
    campaign_logo = models.CharField(max_length=2083, blank=True, null=True)
    users = models.JSONField(default=dict)
    code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ("name_en", "name_np")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name_np
        return super().save(*args, **kwargs)
    

class Department(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="branches")
    name_np = models.CharField(blank=True, null=True, max_length=255)
    name_en = models.CharField(blank=True, null=True, max_length=255)
    alias = models.CharField(blank=True, null=True, max_length=255)
    address_np = models.CharField(blank=True, null=True, max_length=255)
    address_en = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(blank=True, null=True, max_length=255)
    phone_np = models.CharField(blank=True, null=True, max_length=255)
    phone_en = models.CharField(blank=True, null=True, max_length=255)
    slogan_np = models.CharField(blank=True, null=True, max_length=255)
    slogan_en = models.CharField(blank=True, null=True, max_length=255)
    main_logo = models.CharField(max_length=2083, blank=True, null=True)
    campaign_logo = models.CharField(max_length=2083, blank=True, null=True)


class FiscalYear(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    @classmethod
    def active(cls):
        qs = cls.objects.filter(is_active=True)
        if not qs.exists():
            raise Exception("no active fiscal year")
        return qs.latest("id")

    def save(self, *ar, **kw):
        if self.is_active:
            FiscalYear.objects.all().update(is_active=False)
        return super().save(*ar, **kw)


class FeatEntity(models.TextChoices):
    BE = "BE", "BE"
    FE = "FE", "FE"
    FB = "FB", "FB"


class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    enabled = models.BooleanField(default=False)
    description = models.CharField(max_length=255, default="")
    entity = models.CharField(max_length=10, choices=FeatEntity.choices, default=FeatEntity.BE)

    @classmethod
    def get(cls, name: str):
        return cls.objects.get(name=name)

    @classmethod
    def is_enabled(cls, name: str) -> bool:
        instance = cls.get(name)
        return instance.enabled
