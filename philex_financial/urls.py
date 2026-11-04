from django.contrib import admin
from django.urls import path
from finance import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
    path("owner/verifications/", views.owner_verifications, name="owner_verifications"),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/register/", views.register, name="register"),
    path("records/", views.records, name="records"),
    path("records/add/", views.add_record, name="add_record"),
    path("reports/", views.reports, name="reports"),
]
