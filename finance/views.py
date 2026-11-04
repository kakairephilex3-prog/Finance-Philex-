from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from .forms import RegisterForm, FinancialRecordForm
from .models import FinancialRecord, CustomerVerification

def home(request):
    return render(request, "finance/home.html")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm(request)
    return render(request, "finance/auth.html", {"form": form, "heading": "Welcome back", "button": "Sign in"})

def logout_view(request):
    logout(request)
    return redirect("home")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerVerification.objects.get_or_create(
                customer=user,
                defaults={"status": CustomerVerification.Status.PENDING}
            )
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "finance/auth.html", {
        "form": form,
        "heading": "Create your account",
        "button": "Create account"
    })

@login_required
def dashboard(request):
    qs = FinancialRecord.objects.filter(owner=request.user)
    totals = {key: qs.filter(record_type=key).aggregate(v=Sum("amount"))["v"] or Decimal("0.00")
              for key, _ in FinancialRecord.RecordType.choices}
    net_result = totals["INCOME"] - totals["EXPENSE"]
    verification = None

    if not request.user.is_staff and not request.user.is_superuser:
        verification, created = CustomerVerification.objects.get_or_create(
            customer=request.user
        )

    context = {
        "capital": totals["CAPITAL"],
        "income": totals["INCOME"],
        "expenses": totals["EXPENSE"],
        "net_result": net_result,
        "recent": qs[:5],
        "verification": verification,
    }

    return render(request, "finance/dashboard.html", context)

@login_required
def records(request):
    return render(request, "finance/records.html",
                  {"records": FinancialRecord.objects.filter(owner=request.user)})

@login_required
def add_record(request):
    if not request.user.is_staff and not request.user.is_superuser:
        verification, created = CustomerVerification.objects.get_or_create(
            customer=request.user
        )

        if verification.status != CustomerVerification.Status.APPROVED:
            messages.error(
                request,
                "Your account must be approved before adding financial records."
            )
            return redirect("dashboard")

    if request.method == "POST":
        form = FinancialRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner = request.user
            record.save()
            messages.success(request, "Financial record saved.")
            return redirect("records")
    else:
        form = FinancialRecordForm(initial={"record_date": timezone.localdate()})
    return render(request, "finance/form.html", {"form": form, "heading": "Add a financial record"})

@login_required
def reports(request):
    qs = FinancialRecord.objects.filter(owner=request.user)
    income = qs.filter(record_type="INCOME").aggregate(v=Sum("amount"))["v"] or Decimal("0.00")
    expenses = qs.filter(record_type="EXPENSE").aggregate(v=Sum("amount"))["v"] or Decimal("0.00")
    capital = qs.filter(record_type="CAPITAL").aggregate(v=Sum("amount"))["v"] or Decimal("0.00")
    return render(request, "finance/reports.html", {
        "income": income, "expenses": expenses, "capital": capital,
        "net_result": income-expenses,
    })


from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model


@user_passes_test(lambda user: user.is_authenticated and user.is_superuser, login_url='login')
def owner_dashboard(request):
    User = get_user_model()

    customers = User.objects.filter(is_staff=False, is_superuser=False)

    records = FinancialRecord.objects.all()

    totals = {
        "capital": records.filter(record_type="CAPITAL").aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00"),

        "income": records.filter(record_type="INCOME").aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00"),

        "expenses": records.filter(record_type="EXPENSE").aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00"),
    }

    context = {
        "customer_count": customers.count(),
        "active_customers": customers.filter(is_active=True).count(),
        "inactive_customers": customers.filter(is_active=False).count(),
        "pending_verifications": CustomerVerification.objects.filter(
            status="PENDING"
        ).count(),
        "approved_verifications": CustomerVerification.objects.filter(
            status="APPROVED"
        ).count(),
        "rejected_verifications": CustomerVerification.objects.filter(
            status="REJECTED"
        ).count(),
        "record_count": records.count(),
        "totals": totals,
        "recent_customers": customers.order_by("-date_joined")[:10],
        "recent_records": records.select_related("owner")[:10],
    }

    return render(request, "finance/owner_dashboard.html", context)


@user_passes_test(lambda user: user.is_authenticated and user.is_superuser, login_url='login')
def owner_verifications(request):
    User = get_user_model()

    if request.method == "POST":
        verification = get_object_or_404(
            CustomerVerification,
            pk=request.POST.get("verification_id"),
            customer__is_staff=False,
            customer__is_superuser=False
        )

        action = request.POST.get("action")
        note = request.POST.get("review_note", "").strip()[:500]

        if action == "approve":
            verification.status = CustomerVerification.Status.APPROVED
        elif action == "reject":
            verification.status = CustomerVerification.Status.REJECTED
        else:
            messages.error(request, "Invalid verification action.")
            return redirect("owner_verifications")

        verification.reviewed_by = request.user
        verification.reviewed_at = timezone.now()
        verification.review_note = note
        verification.save()

        messages.success(request, "Customer verification updated.")
        return redirect("owner_verifications")

    verifications = CustomerVerification.objects.select_related(
        "customer", "reviewed_by"
    ).filter(
        customer__is_staff=False,
        customer__is_superuser=False
    ).order_by("-created_at")

    return render(request, "finance/owner_verifications.html", {
        "verifications": verifications
    })
