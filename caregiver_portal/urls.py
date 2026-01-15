from django.urls import path
from .views import (
    clock_page,
    clock_out,
    add_comment,
    add_mileage,
    weekly_summary,
    admin_payroll,
    admin_payroll_csv,
    client_profile,
)

urlpatterns = [
    path("clock/", clock_page, name="clock_page"),
    path("clock-out/<int:visit_id>/", clock_out, name="clock_out"),
    path("clock-out/<int:visit_id>/add-comment/", add_comment, name="add_comment"),
    path("clock-out/<int:visit_id>/add-mileage/", add_mileage, name="add_mileage"),
    path("weekly/", weekly_summary, name="weekly_summary"),
    path("admin-payroll/", admin_payroll, name="admin_payroll"),
    path("admin-payroll/csv/", admin_payroll_csv, name="admin_payroll_csv"),
    path("clients/<int:client_id>/", client_profile, name="client_profile"),
]
