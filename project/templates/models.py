import os
import nepali_datetime
from django.db import models


BLANK_NULL = {"blank": True, "null": True, "on_delete": models.SET_NULL}


class PaperStatusChoices(models.TextChoices):
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"
    PROCESSING = "Processing", "Processing"
    UNKNOWN = "Unknown", "Unknown"
    DRAFT = "DRAFT", "DRAFT"


class PriorityChoices(models.TextChoices):
    LOW = "low", "low"
    MEDIUM = "medium", "medium"
    HIGH = "high", "high"
    URGENT = "urgent", "urgent"


class Paper(models.Model):
    fiscal_year = models.ForeignKey("branches.FiscalYear", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(blank=True, null=True)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)
    date = models.CharField(max_length=10, blank=True)
    paper_count = models.CharField(max_length=10)
    draft = models.BooleanField(default=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    sender_phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    receiving_department = models.CharField(max_length=255, blank=True, null=True)
    receiving_department_id = models.PositiveIntegerField(blank=True, null=True)
    settlement_branch = models.CharField(max_length=255, blank=True, null=True)
    settlement_branch_id = models.PositiveBigIntegerField(blank=True, null=True)
    attachment = models.JSONField(default=list)
    created_by = models.ForeignKey("users.User", **BLANK_NULL)
    chalani_number = models.CharField(max_length=255, blank=True, null=True)
    received_date = models.CharField(max_length=10, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_fullname = models.CharField(max_length=255, blank=True, null=True)
    created_by_organization = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ("serial_number", "branch", "fiscal_year")
        ordering = ("-id",)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = nepali_datetime.date.today().strftime("%Y-%m-%d")
            self.received_date = nepali_datetime.date.today().strftime("%Y-%m-%d")
        return super().save()


class SerialNumber(models.Model):
    """this also works as related branch"""
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="serialnumbers")
    organization = models.ForeignKey("branches.Department", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField()


class PaperDocument(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="untitled")
    file = models.FileField()
    no_pages = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", **BLANK_NULL)

    def delete(self, *args, **kwargs):
        os.remove(self.file.path)


class FAQ(models.Model):
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
