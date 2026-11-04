from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import FinancialRecord

User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomerAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("-date_joined",)


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = (
        "record_date",
        "owner",
        "record_type",
        "amount",
        "description",
    )

    list_filter = ("record_type", "record_date")

    search_fields = (
        "owner__username",
        "owner__email",
        "description",
        "reference",
    )

    readonly_fields = ("created_at",)


from .models import CustomerVerification


@admin.register(CustomerVerification)
class CustomerVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "status",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    )

    list_filter = ("status", "created_at")

    search_fields = (
        "customer__username",
        "customer__email",
    )

    readonly_fields = ("created_at",)

    actions = ["approve_customers", "reject_customers"]

    @admin.action(description="Approve selected customers")
    def approve_customers(self, request, queryset):
        from django.utils import timezone

        queryset.update(
            status="APPROVED",
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Reject selected customers")
    def reject_customers(self, request, queryset):
        from django.utils import timezone

        queryset.update(
            status="REJECTED",
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
