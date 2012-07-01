from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from .views import DashboardView

urlpatterns = patterns('',
    url(
        r'^$',
        staff_member_required(DashboardView.view('dashboard')),
        name='mwt_dashboard'
    ),

    url(
        r'^tests/',
        staff_member_required(DashboardView.view('tests')),
        name='mwt_tests'
    ),

    url(
        r'^testruns/',
        staff_member_required(DashboardView.view('testruns')),
        name='mwt_testruns'
    ),
)
