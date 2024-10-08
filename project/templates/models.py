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
    page_count = models.PositiveIntegerField(default=0)
    draft = models.BooleanField(default=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    sender_phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey("users.User", **BLANK_NULL)
    chalani_number = models.CharField(max_length=255, blank=True, null=True)
    paper_date = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_fullname = models.CharField(max_length=255, blank=True, null=True)
    first_reponder = models.ForeignKey("users.User", related_name="reponses", **BLANK_NULL,)
    created_by_organization = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ("serial_number", "branch", "fiscal_year")
        ordering = ("-id",)
    def __get_serialnum(self):
        qs = self.__class__.objects.filter(fiscal_year=self.fiscal_year)
        qs = qs.filter(branch=self.branch)
        if qs.exists():
            return qs.latest("serial_number").serial_number + 1
        return 1
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.serial_number = self.__get_serialnum()
        if not self.date:
            self.date = nepali_datetime.date.today().strftime("%Y-%m-%d")
        return super().save()


class RelatedBranch(models.Model):
    """branches over which a paper has been sent/forwarded"""
    paper = models.ForeignKey(
        Paper, on_delete=models.CASCADE, related_name="serialnumbers"
    )
    fiscal_year = models.ForeignKey("branches.FiscalYear", on_delete=models.CASCADE)
    department = models.ForeignKey("branches.Department", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField()
    remarks = models.CharField(max_length=255, default="N/A")
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        from templates import services

        self.fiscal_year = self.paper.fiscal_year
        if self.active:
            self.paper.serialnumbers.update(active=False)
        self.serial_number = services.get_serialnum(self)
        return super().save(*args, **kwargs)

class PaperDocument(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="documents")
    subject = models.CharField(max_length=255, default="untitled")
    receiving_department = models.CharField(max_length=255, blank=True, null=True)
    receiving_branch = models.CharField(max_length=255, blank=True, null=True)
    sending_branch = models.CharField(max_length=255, blank=True, null=True)
    sending_department = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    chalani_no = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", **BLANK_NULL)

    def delete(self, *args, **kwargs):

        os.remove(self.file.path)


class FAQ(models.Model):
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
