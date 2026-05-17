from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check-email/', views.check_email, name='check_email'),
    path('apply/', views.apply, name='apply'),
    path('applied/', views.applied_pending, name='applied_pending'),
    path('download/', views.download, name='download'),
    path('report-bug/', views.report_bug, name='report_bug'),
    path('bug-reported/', views.bug_reported, name='bug_reported'),
]
