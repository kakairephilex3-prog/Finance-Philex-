from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class FinancialRecord(models.Model):
    class RecordType(models.TextChoices):
        CAPITAL = "CAPITAL", "Owner capital added (record only)"
        INCOME = "INCOME", "Business income received"
        EXPENSE = "EXPENSE", "Business expense paid"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="financial_records")
    record_type = models.CharField(max_length=10, choices=RecordType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    description = models.CharField(max_length=180)
    reference = models.CharField(max_length=80, blank=True)
    record_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-record_date", "-created_at"]

    def __str__(self):
        return f"{self.get_record_type_display()} - {self.amount}"


class CustomerVerification(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_verifications_reviewed"
    )

    reviewed_at = models.DateTimeField(null=True, blank=True)

    review_note = models.CharField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.get_status_display()}"
